from __future__ import annotations
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Generic,
    TypeVar,
    Optional,
    List,
)


from ionq.schemas.job import (
    JobRequest,
    JobDetails,
    WorkloadInput,
)


if TYPE_CHECKING:
    from .backend import Backend

R = TypeVar("R", bound="Result")
JobType = TypeVar("JobType", bound="Job")


class Job(ABC, Generic[R]):

    details: JobRequest | JobDetails

    def __init__(self, id: str, details: JobRequest | JobDetails, backend: Backend):
        self.id = id
        self.details = details
        self.backend = backend

    @abstractmethod
    def results(self) -> R:
        pass


class Workload(ABC, Generic[JobType]):
    @abstractmethod
    def to_workload_input(
        self,
        params: Optional[List[float]] = None,
    ) -> WorkloadInput:
        pass

    @abstractmethod
    def create_job(self, id: str, job: JobRequest, backend: Backend) -> JobType:
        pass


class Result(ABC):
    @abstractmethod
    def plot_results(self, ax=None):
        pass
