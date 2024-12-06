from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Union,
)

import networkx as nx

import matplotlib.pyplot as plt

from ionq.schemas.job import (
    JobRequest,
    WorkloadInput,
    WorkloadType,
    OptimizationWorkload,
    OptimizationMethod,
    OptimizationResult as OptimizationResultSchema,
    JobProgress,
)

from .base import Result, Job, Workload

from .quantum_function import QuantumFunction


if TYPE_CHECKING:
    from .backend import Backend


class OptimizationResult(Result):
    def __init__(
        self,
        minimum_value: float,
        optimal_parameters: List[float],
        progress: JobProgress,
        optimal_bitstrings: Optional[List[str]] = None,
    ):
        self.minimum_value = minimum_value
        self.optimal_parameters = optimal_parameters
        self.progress = progress.progress
        self.optimal_bitstrings = optimal_bitstrings

    def plot_results(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        x = [item.iteration for item in self.progress if item.iteration is not None]
        y = [item.value for item in self.progress if item.value is not None]
        ax.plot(x, y, label="Optimization Progress")

        # Mark the minimum energy point
        min_energy = self.minimum_value
        min_energy_iteration = x[y.index(min_energy)]
        opt_params = [round(param, 3) for param in self.optimal_parameters]
        label = (
            f"Minimum Value: {min_energy}\nOptimal Parameters: {opt_params}\n"
            f"Optimal Bitstrings: {self.optimal_bitstrings[:3] if self.optimal_bitstrings is not None else 'N/A'}"
        )

        ax.axvline(
            min_energy_iteration, color="r", linestyle="--", label="Optimal Iteration"
        )
        ax.text(
            min_energy_iteration, min_energy + 0.1 * (max(y) - min(y)), label, color="r"
        )
        ax.set_ylabel("Value")
        ax.set_xlabel("Iteration")
        ax.set_title("Optimization Result")
        ax.legend()

        if ax is None:
            plt.show()


class OptimizationJob(Job[OptimizationResult]):

    def results(self) -> OptimizationResult:
        if self.id is None:
            raise ValueError("Optimization Job not yet run")
        results = OptimizationResultSchema.parse_obj(self.backend.results(self.id))
        progress = self.backend.get_job_progress(self.id)

        return OptimizationResult(
            minimum_value=results.solution.minimum_value,
            optimal_parameters=results.solution.optimal_parameters,
            progress=progress,
        )


class Optimization(Workload[OptimizationJob]):
    def __init__(
        self,
        quantum_function: QuantumFunction,
        method: str,
        initial_params: Optional[List[Union[float, int]]] = None,
        log_interval: int = 1,
        options: Optional[dict] = None,
        maxiter: Optional[int] = None,
        graph: Optional[nx.Graph] = None,
        variables: Optional[List[str]] = None,
        quadratic_expression: Optional[str] = None,
    ):
        self.quantum_function = quantum_function
        self.method = method
        self.initial_params = initial_params
        self.log_interval = log_interval
        self.options = options
        self.maxiter = maxiter
        self.graph = graph
        self.variables = variables
        self.quadratic_expression = quadratic_expression

    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        return WorkloadInput(
            type=WorkloadType.optimization,
            data=OptimizationWorkload(
                quantum_function=self.quantum_function.to_workload_input().data,
                method=OptimizationMethod(self.method),
                initial_params=self.initial_params,
                log_interval=self.log_interval,
                options=self.options,
                maxiter=self.maxiter,
            ),
        )

    def create_job(self, id: str, job: JobRequest, backend: Backend) -> OptimizationJob:
        return OptimizationJob(id, job, backend)
