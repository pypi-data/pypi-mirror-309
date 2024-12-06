from pydantic import HttpUrl, BaseModel, validator, Field
from typing import List, Dict, Optional, Union, Any, Generic, TypeVar
from enum import Enum
from dataclasses import dataclass
import re
from openqasm3 import parser
from ..defaults import DEFAULT_API_URL


class JobStatus(str, Enum):
    submitted = "submitted"
    ready = "ready"
    running = "running"
    canceled = "canceled"
    deleted = "deleted"
    completed = "completed"
    failed = "failed"


class NoiseModel(str, Enum):
    ideal = "ideal"
    harmony = "harmony"
    aria_1 = "aria-1"
    forte_1 = "forte-1"


class GateSet(str, Enum):
    qis = "qis"
    native = "native"


class TargetOptions(str, Enum):
    simulator = "simulator"
    harmony = "qpu.harmony"
    aria_1 = "qpu.aria-1"
    aria_2 = "qpu.aria-2"
    forte_1 = "qpu.forte-1"


class NoiseOptions(BaseModel):
    model: Optional[NoiseModel] = None
    seed: Optional[int] = None


class ErrorMitigationOptions(BaseModel):
    debias: Optional[bool] = None


class WorkloadType(str, Enum):
    circuit = "circuit"
    quantum_function = "quantum-function"
    optimization = "optimization"


class Ansatz(BaseModel):
    format: str = "qasm"
    data: str
    num_qubits: int

    def __init__(self, **data):

        match = re.search(r"qubit\[(\d+)\]", data["data"])
        if match is None:
            raise ValueError("Invalid QASM: No qubit declaration found")

        data["num_qubits"] = int(match.group(1))

        try:
            parser.parse(data["data"])
        except Exception as e:
            raise ValueError(f"Invalid QASM: {e}")

        super().__init__(**data)


class HamiltonianPauliTerm(BaseModel):
    pauli_string: str
    coefficient: float


@dataclass
class Hamiltonian:
    terms: List[HamiltonianPauliTerm]
    num_qubits: Optional[int]


class QuantumFunction(BaseModel):
    pass


class HamiltonianEnergyData(BaseModel):
    hamiltonian: List[HamiltonianPauliTerm]
    ansatz: Ansatz


T = TypeVar("T")


class WorkloadInput(BaseModel, Generic[T]):
    type: WorkloadType
    data: T


class QuantumFunctionWorkload(WorkloadInput[QuantumFunction]):
    pass


class QuantumFunctionInput(WorkloadInput[QuantumFunction]):
    type: str = Field(default="quantum-function", const=True)
    params: Optional[List[float]] = None


class HamiltonianEnergyQuantumFunction(QuantumFunction):
    type: str = Field(default="hamiltonian-energy", const=True)
    data: HamiltonianEnergyData


class CircuitData(BaseModel):
    qasm: Optional[str] = None
    ore: Optional[Any] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.qasm is None and self.ore is None:
            raise ValueError("Circuit must have qasm or ore")


class CircuitType(str, Enum):
    ore = "ore"
    qis = "qis"
    native = "native"


class OptimizationMethod(str, Enum):
    SPSA = "SPSA"
    Powell = "Powell"
    CG = "CG"
    BFGS = "BFGS"
    Newton_CG = "Newton-CG"
    L_BFGS_B = "L-BFGS-B"
    TNC = "TNC"
    COBYLA = "COBYLA"
    COBYQA = "COBYQA"
    SLSQP = "SLSQP"
    TRUST_CONSTR = "trust-constr"
    DOGLEG = "dogleg"
    TRUST_NCG = "trust-ncg"
    TRUST_EXACT = "trust-exact"
    TRUST_KRYLOV = "trust-krylov"


class OptimizationWorkload(BaseModel):
    quantum_function: QuantumFunction
    method: OptimizationMethod
    initial_params: Optional[List[float]] = None  # temporary setter
    log_interval: Optional[int] = 1
    options: Optional[Dict[str, Any]] = None
    maxiter: Optional[int] = None


class JobConfig(BaseModel):
    target: TargetOptions
    shots: Optional[int] = 100
    noise: Optional[NoiseOptions] = None
    error_mitigation: Optional[ErrorMitigationOptions] = None

    def __init__(self, **data):
        super().__init__(**data)
        if (
            (self.target == TargetOptions.simulator and self.noise is not None)
            or (self.target != TargetOptions.simulator)
            and self.shots is None
        ):
            raise ValueError("Shots must be set for ideal simulator jobs")


class CircuitWorkload(BaseModel):
    format: Optional[str] = "ionq.circuit.v0"
    gateset: Optional[GateSet] = GateSet.qis
    # TODO Improve typing here
    circuits: List[
        Dict[str, Any]
    ]  # Union[List[CircuitList], List[CircuitOperation], None] = None
    qubits: Optional[int] = None

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     if self.qubits == 0:
    #         raise ValueError("Circuit must have at least one qubit")


class JobRequest(BaseModel, Generic[T]):
    name: Optional[str] = None
    metadata: Optional[dict] = None
    shots: Optional[int] = 100
    backend: str
    noise: Optional[NoiseOptions] = None
    workload: WorkloadInput[T]
    error_mitigation: Optional[ErrorMitigationOptions] = None

    class Config:
        schema_extra = {
            "name": "My Awesome Job",
            "metadata": {"custom_key": "a string, maximum 400 chars"},
            "shots": 123,
            "backend": "simulator",
            "noise": {"model": "aria-1", "seed": 1},
            "workload": {
                "type": "circuit",
                "data": {
                    "format": "ionq.circuit.v0",
                    "qubits": 1,
                    "circuits": [{"circuit": {"gate": "h", "target": 0}}],
                },
            },
            "error_mitigation": {"debias": True},
        }


class Progress(BaseModel):
    job_id: str
    status: JobStatus
    finished_at: Optional[str]
    value: Optional[float]
    params: Optional[List[float]]
    iteration: Optional[int]


class JobProgress(BaseModel):
    progress: List[Progress]


class Solution(BaseModel):
    minimum_value: float
    optimal_parameters: List[float]


class QuantumFunctionResult(BaseModel):
    value: Optional[float] = None
    variance: Optional[float] = None


class OptimizationResult(BaseModel):
    solution: Solution


class JobDetails(BaseModel):
    id: str
    name: Optional[str]
    status: JobStatus
    target: Optional[TargetOptions] = TargetOptions.simulator
    noise: Optional[NoiseOptions]
    metadata: Optional[Dict[str, Union[str, int]]]
    shots: Optional[int] = 100
    error_mitigation: Optional[ErrorMitigationOptions]
    gate_counts: Optional[Dict[str, int]]
    qubits: Optional[int]
    cost_usd: Optional[float]
    request: int
    start: Optional[int]
    response: Optional[int]
    execution_time: Optional[int]
    predicted_execution_time: Optional[int]
    children: Optional[List[str]]
    results_url: Optional[HttpUrl]
    failure: Optional[Dict[str, str]]
    warning: Optional[Dict[str, List[str]]]
    circuits: Optional[int]

    @validator("results_url", pre=True)
    def prepend_url_prefix(cls, v: str):
        return DEFAULT_API_URL + v

    class Config:
        schema_extra = {
            "id": "aa54e783-0a9b-4f73-ad2f-63983b6aa4a8",
            "name": "My Awesome Job",
            "status": "completed",
            "target": "qpu.harmony",
            "noise": {"model": "harmony", "seed": 100},
            "metadata": {"custom_key": "a string, maximum 400 chars"},
            "shots": 123,
            "error_mitigation": {"debias": True},
            "gate_counts": {"1q": 8, "2q": 2},
            "qubits": 4,
            "cost_usd": 12.41,
            "request": 1490932820,
            "start": 1490932821,
            "response": 1490932834,
            "execution_time": 13,
            "predicted_execution_time": 13,
            "children": ["aa54e783-0a9b-4f73-ad2f-63983b6aa4a8"],
            "results_url": "/v0.3/jobs/617a1f8b-59d4-435d-aa33-695433d7155e/results",
            "failure": {"error": "An error occurred!", "code": "internal_error"},
            "warning": {
                "messages": [
                    "Warning message 1",
                    "Warning message 2",
                    "etc.",
                ]
            },
            "circuits": 1,
        }


class JobList(BaseModel):
    jobs: List[JobDetails]
    next: Optional[str]

    class Config:
        schema_extra = {
            "jobs": [
                {
                    "id": "aa54e783-0a9b-4f73-ad2f-63983b6aa4a8",
                    "name": "My Awesome Job",
                    "status": "completed",
                    "target": "qpu.harmony",
                    "noise": {"model": "harmony", "seed": 100},
                    "metadata": {"custom_key": "a string, maximum 400 chars"},
                    "shots": 123,
                    "error_mitigation": {"debias": True},
                    "gate_counts": {"1q": 8, "2q": 2},
                    "qubits": 4,
                    "cost_usd": 12.41,
                    "request": 1490932820,
                    "start": 1490932821,
                    "response": 1490932834,
                    "execution_time": 13,
                    "predicted_execution_time": 13,
                    "children": ["aa54e783-0a9b-4f73-ad2f-63983b6aa4a8"],
                    "results_url": "/v0.3/jobs/617a1f8b-59d4-435d-aa33-695433d7155e/results",
                    "failure": {
                        "error": "An error occurred!",
                        "code": "internal_error",
                    },
                    "warning": {"messages": ["<string>"]},
                    "circuits": 1,
                }
            ],
            "next": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
        }


class JobUpdate(BaseModel):
    id: str
    ids: Optional[List[str]]
    status: JobStatus

    class Config:
        schema_extra = {
            "id": "aa54e783-0a9b-4f73-ad2f-63983b6aa4a8",
            "status": "ready",
        }

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None and self.ids is None:
            raise ValueError("Either 'id' or 'ids' must be set")
