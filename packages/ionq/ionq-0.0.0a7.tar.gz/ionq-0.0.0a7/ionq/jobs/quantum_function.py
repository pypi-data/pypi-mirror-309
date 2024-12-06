from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
)

import matplotlib.pyplot as plt

from ionq.schemas.job import (
    JobRequest,
    WorkloadInput,
    QuantumFunctionInput,
    HamiltonianEnergyQuantumFunction,
    HamiltonianEnergyData,
    Hamiltonian,
    Ansatz,
)

from .base import Result, Job, Workload

if TYPE_CHECKING:
    from .backend import Backend


class QuantumFunctionResult(Result):
    def __init__(self, value: float, variance: float):
        self.value = value
        self.variance = variance

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        ax.errorbar(
            ["Value"],
            [self.value],
            yerr=[self.variance],
            fmt="o",
            capsize=10,
        )
        ax.set_ylabel("Value")
        ax.set_title("Quantum Function Result")

        if ax is None:
            plt.show()


class QuantumFunctionJob(Job[QuantumFunctionResult]):

    def results(self) -> QuantumFunctionResult:
        if self.id is None:
            raise ValueError("Quantum Function not yet run")
        results_data = self.backend.results(self.id)

        return QuantumFunctionResult(
            value=results_data["value"],
            variance=results_data["variance"],
        )


class QuantumFunction(Workload[QuantumFunctionJob]):
    pass


class HamiltonianEnergy(QuantumFunction):
    def __init__(
        self,
        ansatz: Ansatz,
        hamiltonian: Hamiltonian,
    ):
        assert (
            ansatz.num_qubits == hamiltonian.num_qubits
        ), "Ansatz and Hamiltonian must have the same number of qubits"
        self.ansatz = ansatz
        self.hamiltonian = hamiltonian

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return QuantumFunctionInput(
            data=HamiltonianEnergyQuantumFunction(
                data=HamiltonianEnergyData(
                    hamiltonian=self.hamiltonian.terms,
                    ansatz=self.ansatz,
                ),
            ),
            params=params,
        )

    def create_job(
        self, id: str, job: JobRequest, backend: Backend
    ) -> QuantumFunctionJob:
        return QuantumFunctionJob(id, job, backend)
