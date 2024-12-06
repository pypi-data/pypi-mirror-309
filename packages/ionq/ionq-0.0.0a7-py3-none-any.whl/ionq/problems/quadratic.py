from typing import List, Union, Optional
import numpy as np
from dataclasses import dataclass
from pydantic import BaseModel, Field

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from tqdm import tqdm
from ionq import Backend
from ionq.jobs.quantum_function import QuantumFunction, QuantumFunctionJob
from ionq.schemas.job import (
    Ansatz,
    WorkloadInput,
    QuantumFunctionInput,
    HamiltonianEnergyQuantumFunction,
    JobRequest,
    HamiltonianPauliTerm,
)
from ionq.utils import ionq_qiskit
from .problem import Problem


@dataclass
class OptimalSolution:
    x: str
    fun: float


class LinearConstraint(BaseModel):
    r"""
    A class to model linear inequality constraints of the form

    .. math::

        a^T x \leq b.

    INPUT:

        - ``coeffs`` -- a list of floats describing the coefficient vector `a`
        - ``rhs`` -- the Right-Hand-Side coefficient `b`
    """

    coeffs: List[float]
    rhs: float


class QuadraticConstraint(BaseModel):
    r"""
    A class to model quadratic inequality constraints of the form

    .. math::

        x^T P x + r^T x \leq c.

    INPUT:

        - ``quadratic_coeff`` -- a list of list of floats describing the
          symmetric matrix `P`
        - ``linear_coeff`` -- a list of floats describing the row vector `r`
        - ``rhs`` -- the Right-Hand-Side coefficient `c`
    """

    quadratic_coeff: List[List[float]]
    linear_coeff: List[float]
    rhs: float


class MatrixLinearConstraint:
    def __init__(self, constraints: List[LinearConstraint]):
        self.linear_coeff = np.array([lc.coeffs for lc in constraints])
        self.rhs_vec = np.array([lc.rhs for lc in constraints])
        self.num_constraints = len(constraints)

    def __iter__(self):
        for coeffs, rhs in zip(self.linear_coeff, self.rhs_vec):
            yield LinearConstraint(coeffs=coeffs.tolist(), rhs=rhs.tolist())

    def compute_violations(self, x: np.ndarray) -> np.ndarray:
        """
        Compute the violations for this matrix constraint.
        """
        if self.num_constraints == 0:
            return np.array([])

        lhs = self.linear_coeff @ x - self.rhs_vec
        vv = np.zeros_like(lhs)
        vv[lhs > 0] = lhs[lhs > 0]
        return vv


class MatrixQuadraticConstraint:
    def __init__(self, constraints: List[QuadraticConstraint]):
        self.quadratic_coeff = np.array([lc.quadratic_coeff for lc in constraints])
        self.linear_coeff = np.array([lc.linear_coeff for lc in constraints])
        self.rhs_vec = np.array([lc.rhs for lc in constraints])
        self.num_constraints = len(constraints)

    def __iter__(self):
        for quad_coeff, lin_coeff, rhs in zip(
            self.quadratic_coeff, self.linear_coeff, self.rhs_vec
        ):
            yield QuadraticConstraint(
                quadratic_coeff=quad_coeff.tolist(),
                linear_coeff=lin_coeff.tolist(),
                rhs=rhs.tolist(),
            )

    def compute_violations(self, x: np.ndarray) -> np.ndarray:
        """
        Compute the violations for this matrix constraint.
        """
        if self.num_constraints == 0:
            return np.array([])

        lhs = x.T @ self.quadratic_coeff @ x + self.linear_coeff @ x - self.rhs_vec
        vv = np.zeros_like(lhs)
        vv[lhs > 0] = lhs[lhs > 0]
        return vv


class QCQPHamiltonianData(BaseModel):
    hamiltonian: List[HamiltonianPauliTerm]
    ansatz: Ansatz
    linear_constraints: Optional[List[LinearConstraint]] = None
    quadratic_constraints: Optional[List[QuadraticConstraint]] = None
    penalty: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.penalty is not None and (
            self.linear_constraints is None and self.quadratic_constraints is None
        ):
            raise ValueError("Constraints must be set if penalty is set")


class QCQPHamiltonianFunction(HamiltonianEnergyQuantumFunction):
    type: str = Field(default="hamiltonian-energy", const=True)
    data: QCQPHamiltonianData


class QCQPObjective(QuantumFunction):
    def __init__(
        self,
        ansatz: Ansatz,
        qp_objective: np.ndarray,
        linear_constraints: List[LinearConstraint] = [],
        quadratic_constraints: List[QuadraticConstraint] = [],
        penalty: Optional[float] = None,
    ):

        self.ansatz = ansatz
        self._qp_objective = qp_objective
        self.linear_constraints = linear_constraints
        self.quadratic_constraints = quadratic_constraints
        self.penalty = penalty

    def get_qubo_objective_as_ising_ham(self) -> SparsePauliOp:
        r"""
        Compute the Ising Hamiltonian obtained by applying the Ising map

        $$x_j \rightarrow \frac{1}{2}(I - \sigma_j^Z),$$

        with $\sigma_j^Z$ denoting the Pauli-$Z$ gate acting on the $j$th
        qubit, to the QUBO objective $x^T Q x$ specified by the symmetric
        2D-NumPy array ``self.qp_objective``.
        """
        if not hasattr(self, "_ising_ham"):
            Q = self._qp_objective
            terms = [("I" * Q.shape[0], 1 / 4 * (Q.sum() + Q.trace()))]

            # Linear terms
            for j, sj in enumerate(
                filter(lambda v: not np.isclose(v, 0), Q.sum(axis=1))
            ):
                lin = "".join(
                    "I" if k != j else "Z" for k in reversed(range(Q.shape[0]))
                )
                terms += [(lin, -1 / 2 * sj)]

            # Quadratic terms
            for i in range(Q.shape[0]):
                for j in range(i + 1, Q.shape[0]):
                    if not np.isclose(Q[i, j], 0):
                        quad = "".join(
                            "I" if k not in [i, j] else "Z"
                            for k in reversed(range(Q.shape[0]))
                        )
                        terms += [(quad, 1 / 2 * Q[i, j])]
            self._ising_ham = SparsePauliOp.from_list(terms)
        return self._ising_ham

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        ising_ham = self.get_qubo_objective_as_ising_ham()
        assert (
            self.ansatz.num_qubits == ising_ham.num_qubits
        ), "Ansatz and Hamiltonian must have the same number of qubits"
        return QuantumFunctionInput(
            data=QCQPHamiltonianFunction(
                data=QCQPHamiltonianData(
                    ansatz=self.ansatz,
                    hamiltonian=ionq_qiskit.to_hamiltonian(ising_ham).terms,
                    linear_constraints=self.linear_constraints or None,
                    quadratic_constraints=self.quadratic_constraints or None,
                    penalty=self.penalty,
                ),
            ),
            params=params,
        )

    def create_job(
        self, id: str, job: JobRequest, backend: Backend
    ) -> QuantumFunctionJob:
        return QuantumFunctionJob(id, job, backend)


class QuadraticProgram(Problem):
    r"""
    A class to solve Quadratically-Constrained Quadratic Programs (QCQPs).

    The ``objective`` $x^T Q x$ may be specified by a symmetric 2D-NumPy array
    (whose diagonal defines objective's linear component) or as the 
    objective of a Qiskit ``QuadraticProgram`` instance.

    Optionally, a list of linear and/or quadratic ``constraints`` may be
    supplied. Each element of ``constraints`` is either a pair ``(A, b)`` or a
    triple ``(P, r, c)``: 

    - if ``len(constraints[j]) == 2``, then ``constraints[j]`` specifies the
      linear inequality $Ax \leq b$; 
    - otherwise, ``constraints[j]`` defines the quadratic inequality
      $x^T P x + r^T x \leq c$.

    Additionally, a ``penalty`` parameter may be provided, which determines the
    magnitude of the penalty terms added to the Ising energies corresponding to
    infeasible states.

    In symbols, this class models the following QCQP:

    $$
    \begin{aligned}
    \min_x \quad & x^T Q x \\
    \text{s.t.} \quad & A_j x \leq b_j, \\
    & x^T P_j x + r_j^T x \leq c, \\
    & x_k \in \{0, 1\}, \quad \forall k.
    \end{aligned}
    $$
    """

    def __init__(
        self,
        objective: np.ndarray,
        linear_constraints: List[LinearConstraint] = [],
        quadratic_constraints: List[QuadraticConstraint] = [],
    ):
        # Standardize objective
        self._qp_objective = objective

        # Initialize constraints handlers
        self._mat_lc = MatrixLinearConstraint(linear_constraints)
        self._mat_qc = MatrixQuadraticConstraint(quadratic_constraints)

    def compute_optimal_solution(self):
        """
        Compute the optimal (feasible) solution of ``self``.

        Currently this method finds the global optimal solution by enumeration.
        """
        if hasattr(self, "_optimal_solution"):
            return self._optimal_solution

        # Find the feasible states
        n = self._qp_objective.shape[0]
        best_soln = (0, 1e100)
        base = np.arange(n, dtype=int)[np.newaxis, ::-1]
        chunk_sz = min(2**n, 2**20)

        # Semi-vectorized loop: iterate over chunks of 2**20 states at a time
        print("Finding optimal solution one batch of states at a time...")
        for chunk_idx in tqdm(np.arange(2 ** max(n - 20, 0))):
            chunk = np.arange(chunk_idx * chunk_sz, (chunk_idx + 1) * chunk_sz)[
                :, np.newaxis
            ]
            states = np.array(2**base & chunk > 0, dtype=int)
            feasible_idx = np.zeros(len(states), dtype=bool)
            for j in np.arange(len(states)):
                feasible_idx[j] = self.is_feasible(states[j])
            X = states[feasible_idx]
            obj_vals = (X * np.dot(X, self._qp_objective)).sum(axis=1)
            chunk_min_idx = obj_vals.argmin()
            if obj_vals[chunk_min_idx] < best_soln[1]:
                best_soln = (X[chunk_min_idx], obj_vals[chunk_min_idx])
        self._optimal_solution = OptimalSolution(
            "".join(map(str, best_soln[0])), best_soln[1]
        )
        return self._optimal_solution

    def compute_violations(self, x: Union[np.ndarray, str]):
        r"""
        Compute the list constraint violations, defined as the positive part of
        $A_j x - b_j$ for every linear inequality and $x^T P x + r_j^T x - c$
        for every quadratic one.
        """
        if isinstance(x, str):
            x = np.array(list(x), dtype=int)

        lc_viol = self._mat_lc.compute_violations(x)
        qc_viol = self._mat_qc.compute_violations(x)
        return np.hstack((lc_viol, qc_viol))

    def evaluate_qp_objective(self, x: Union[np.ndarray, str]) -> float:
        """
        Evaluate the QP objective at the given bit-string ``x``, which may be
        given as a NumPy array or a string.
        """
        if isinstance(x, str):
            x = np.array(list(x), dtype=int)
        return x.T @ self.qp_objective @ x

    @classmethod
    def from_docplex_quadratic_program(cls, docplex_qp):
        """
        Construct a :class:`.QuadraticProgram` instance from a `docplex` QP.
        """
        if docplex_qp.quadratic_constraints:
            raise NotImplementedError(
                "Only linear constraints are currently supported..."
            )

        # Interpret linear constraints
        constraints = list()
        for lc in docplex_qp.linear_constraints:
            ionq_lc = LinearConstraint(coeffs=lc.linear.to_array(), rhs=lc.rhs)

            # Check the type of constraint
            if lc.sense.name == "EQ":
                constraints.append(
                    LinearConstraint(coeffs=-lc.linear.to_array(), rhs=-lc.rhs)
                )
            else:
                print(f"missing constraint with sense {lc.sense.name}")
            constraints.append(ionq_lc)
        return QuadraticProgram(docplex_qp.objective, constraints)

    def is_feasible(self, x: Union[np.ndarray, str]) -> bool:
        """
        Determine if the bit-string ``x`` satisfies the problem constraints.
        """
        if isinstance(x, str):
            x = np.array(list(x), dtype=int)
        return np.allclose(self.compute_violations(x), 0)

    @property
    def linear_constraints(self) -> List[LinearConstraint]:
        """
        Get the constraints of ``self``, if any.
        """
        return list(self._mat_lc)

    @property
    def qp_objective(self) -> np.ndarray:
        """
        Get the symmetric 2D-array describing the objective of ``self``.
        """
        return self._qp_objective

    @property
    def quadratic_constraints(self) -> List[QuadraticConstraint]:
        """
        Get the constraints of ``self``, if any.
        """
        return list(self._mat_qc)

    def quantum_function_objective(
        self, ansatz: QuantumCircuit, penalty: float = 10
    ) -> QCQPObjective:
        """
        Get the :class:`.QuantumFunction` describing `self`'s optimization
        objective.
        """
        return QCQPObjective(
            ansatz=ionq_qiskit.to_ansatz(ansatz),
            qp_objective=self._qp_objective,
            linear_constraints=self.linear_constraints,
            quadratic_constraints=self.quadratic_constraints,
            penalty=penalty,
        )
