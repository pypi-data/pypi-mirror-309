from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Dict,
    Literal,
    Any,
)


import matplotlib.pyplot as plt

from ionq.schemas.job import (
    JobRequest,
    WorkloadInput,
    WorkloadType,
    CircuitWorkload,
    GateSet,
)

from .base import Result, Job, Workload

if TYPE_CHECKING:
    from .backend import Backend


class CircuitResult(Result):
    def __init__(
        self, probabilities: Dict[str, float], counts: Optional[Dict[str, int]] = None
    ):
        self.counts = counts
        self.probabilities = probabilities

    def top_candidates(self, n: Optional[int] = None) -> List[str]:
        if n is None:
            n = len(self.probabilities)
        return sorted(self.probabilities, key=self.probabilities.get, reverse=True)[:n]  # type: ignore

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(list(self.probabilities.keys()), list(self.probabilities.values()))
        ax.set_ylabel("Probability")
        ax.set_xlabel("State")
        ax.set_title("Circuit Result")

        if ax is None:
            plt.show()


class CircuitJob(Job[CircuitResult]):

    def _get_counts(self, probabilities: Dict[str, float]) -> Optional[Dict[str, int]]:
        if self.details.shots is None:
            return None
        return {k: int(v * self.details.shots) for k, v in probabilities.items()}

    def results(self) -> List[CircuitResult]:
        if self.id is None:
            raise ValueError("Circuit Job not yet run")
        results = self.backend.results(self.id)

        # If the results contain multiple results, create a list of CircuitResult objects
        if all(isinstance(value, dict) for value in results.values()):
            return [
                CircuitResult(
                    probabilities=probabilities,
                    counts=self._get_counts(probabilities),
                )
                for probabilities in results.values()
            ]
        else:
            return [
                CircuitResult(
                    probabilities=results,
                    counts=self._get_counts(results),
                )
            ]


class Circuit(Workload[CircuitJob]):

    gateset: Literal["qis", "native"]

    def __init__(
        self,
        circuits: List[Dict[str, Any]],
        format: str = "ionq.circuit.v0",
        gateset: Literal["qis", "native"] = "qis",
        qubits: Optional[int] = None,
        name: Optional[str] = None,
    ):
        self.circuits = circuits
        self.format = format
        self.gateset = gateset
        self.qubits = qubits
        self.name = name

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return WorkloadInput(
            type=WorkloadType.circuit,
            data=CircuitWorkload(
                format=self.format,
                gateset=GateSet(self.gateset),
                qubits=self.qubits,
                circuits=self.circuits,
            ),
        )

    def create_job(self, id: str, request: JobRequest, backend: Backend) -> CircuitJob:
        return CircuitJob(id, request, backend)
