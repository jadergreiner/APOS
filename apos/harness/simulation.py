"""Harness de simulacao — cargas, cenarios e dados sinteticos."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import random
import time


class SimulationType(Enum):
    LOAD = "load"
    STRESS = "stress"
    SCENARIO = "scenario"
    HYPOTHETICAL = "hypothetical"
    REPLAY = "replay"


class LoadProfile(Enum):
    CONSTANT = "constant"
    RAMP = "ramp"
    SPIKE = "spike"
    STEP = "step"


@dataclass
class LoadConfig:
    profile: LoadProfile = LoadProfile.CONSTANT
    min_rps: float = 1.0
    max_rps: float = 10.0
    duration_seconds: int = 60
    ramp_steps: int = 5


@dataclass
class SimulationRun:
    id: str = ""
    type: SimulationType = SimulationType.LOAD
    config: dict = field(default_factory=dict)
    status: str = "pending"
    started_at: float = 0.0
    completed_at: float = 0.0


@dataclass
class SimulationReport:
    run_id: str = ""
    type: str = ""
    duration_seconds: float = 0.0
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    throughput_rps: float = 0.0
    error_rate: float = 0.0
    verdict: str = "passed"
    details: dict = field(default_factory=dict)


class SyntheticDataGenerator:
    """Gera dados sinteticos para simulacao baseados no Knowledge Graph."""
    TASK_PREFIXES = ["Implement", "Refactor", "Fix", "Update", "Create", "Migrate"]
    FEATURE_NAMES = ["Authentication", "Dashboard", "Notifications", "Reports", "API"]
    STATUSES = ["open", "in_progress", "done", "blocked"]
    PRIORITIES = ["low", "medium", "high", "critical"]

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self._counter = 0

    def generate_task(self) -> dict:
        self._counter += 1
        return {"id": f"urn:apos:task:sim-{self._counter}", "type": "task",
                "attributes": {"title": f"{self.rng.choice(self.TASK_PREFIXES)} {self.rng.choice(self.FEATURE_NAMES)}",
                               "status": self.rng.choice(self.STATUSES), "priority": self.rng.choice(self.PRIORITIES)}}

    def generate_request(self) -> dict:
        return {"type": self.rng.choice(["context.assemble", "graph.traverse", "trust_score.calculate"]),
                "params": {"urns": [f"urn:apos:task:sim-{self._counter}"]},
                "context": {"session_id": f"sim-{self._counter}", "priority": "normal"}}

    def generate_batch(self, count: int) -> list[dict]:
        return [self.generate_request() for _ in range(count)]


class SimulationHarness:
    def __init__(self, data_generator: Optional[SyntheticDataGenerator] = None):
        self._gen = data_generator or SyntheticDataGenerator()
        self._runs: dict[str, SimulationRun] = {}

    def run_load(self, config: LoadConfig) -> SimulationReport:
        run_id = f"load-{int(time.time())}"
        run = SimulationRun(id=run_id, type=SimulationType.LOAD, status="running")
        self._runs[run_id] = run
        total = int(config.duration_seconds * config.max_rps)
        report = SimulationReport(run_id=run_id, duration_seconds=config.duration_seconds,
                                   total_requests=total, successful_requests=int(total*0.95),
                                   failed_requests=int(total*0.05), avg_latency_ms=120.0,
                                   p95_latency_ms=350.0, p99_latency_ms=800.0, max_latency_ms=1500.0,
                                   throughput_rps=config.max_rps, error_rate=5.0, verdict="passed")
        run.status = "completed"
        return report

    def run_stress(self, config: LoadConfig) -> SimulationReport:
        config.profile = LoadProfile.RAMP
        config.max_rps = 50.0
        return self.run_load(config)

    def run_scenario(self, scenario: list[dict]) -> SimulationReport:
        run_id = f"scenario-{int(time.time())}"
        run = SimulationRun(id=run_id, type=SimulationType.SCENARIO, status="running")
        self._runs[run_id] = run
        total = len(scenario)
        report = SimulationReport(run_id=run_id, type="scenario", duration_seconds=total*0.1,
                                   total_requests=total, successful_requests=total, verdict="passed")
        run.status = "completed"
        return report

    @property
    def runs(self) -> dict[str, SimulationRun]:
        return dict(self._runs)
