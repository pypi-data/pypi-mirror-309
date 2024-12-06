from typing import Optional
import numpy as np
import networkx as nx

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector


def BrickworkLayoutAnsatz(
    num_qubits,
    num_layers=2,
    params=None,
    initial_state: Optional[QuantumCircuit] = None,
):
    # Construct a variational ansatz with a brickwork layout structure.
    qc = QuantumCircuit(num_qubits)
    if initial_state:
        qc = initial_state.compose(qc)
        if not qc:
            raise ValueError("Error when adding initial state.")
        qc.barrier()
    else:
        qc.h(range(num_qubits))

    if params is None:
        num_params = np.ceil(num_layers * (num_qubits - 1) / 2).astype(int)
        params = ParameterVector("θ", num_params)
    param_it = iter(params)

    for layer in range(num_layers):
        start_qubit = layer % 2
        for qubit in range(start_qubit, num_qubits - 1, 2):
            qc.cx(qubit, qubit + 1)
            qc.ry(next(param_it), qubit + 1)

    return qc


class GenericQubitEntangler(QuantumCircuit):
    """
    Construct a generic qubit entangler with connectivity specified by a given graph.

    Specify either `num_qubits` or the connectivity `graph`; when using the former,
    we use the complete graph (all-to-all connectivity). By default, the ansatz uses
    one independent parameter per edge in the graph. However, a parameters can be
    specified.
    """

    def __init__(self, num_qubits=None, graph=None, params=None, initial_state=None):
        # Check / standardize input
        if num_qubits is None and graph is None:
            raise ValueError("Must supply at least one of num_qubits or graph")
        if (
            num_qubits is not None
            and graph is not None
            and num_qubits != graph.number_of_nodes()
        ):
            raise ValueError("num_qubits must equal graph.number_of_nodes()!")

        # Impute the number of qubits
        if initial_state is not None:
            num_qubits = initial_state.num_qubits
        else:
            if graph is None:
                graph = nx.complete_graph(num_qubits)
            num_qubits = graph.number_of_nodes()
        super().__init__(num_qubits)

        # Default initial state is |+>
        if initial_state is None:
            self.h(range(self.num_qubits))
        else:
            self.compose(initial_state, inplace=True)
        self.barrier()

        # Construct entangler
        if params is None:
            params = ParameterVector("θ", graph.number_of_edges())
        for theta, (u, v) in zip(params, graph.edges):
            self.cx(u, v)
            self.ry(theta, v)
            self.cx(u, v)
