"""
Unified data models for the Work IQ x Task Mining POC.

Defines the source-agnostic activity schema that any event source
(Celonis Task Mining, Microsoft Work IQ, LangChain, CrewAI, etc.)
normalizes into before clustering.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class ActorType(str, Enum):
    HUMAN = "HUMAN"
    AGENT = "AGENT"
    HYBRID = "HYBRID"


class EventSource(str, Enum):
    CELONIS_DESKTOP = "celonis_desktop"
    CELONIS_BROWSER = "celonis_browser"
    WORK_IQ = "work_iq"
    CUSTOM_AGENT = "custom_agent"


@dataclass
class UnifiedActivityEvent:
    """Source-agnostic activity event — the canonical schema that all adapters target."""

    timestamp: str
    event_type: str
    source: str
    actor_type: str
    actor_id: str
    application: str
    url: Optional[str] = None
    title: Optional[str] = None
    context: dict = field(default_factory=dict)
    case_correlation_id: Optional[str] = None
    dom_path: Optional[str] = None
    event_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def feature_text(self) -> str:
        """Produce a text representation for ML vectorization."""
        parts = [
            self.application or "",
            self.event_type or "",
            self.title or "",
            self.context.get("prompt", ""),
            self.context.get("tool", ""),
            self.context.get("output", ""),
            self.url or "",
        ]
        return " ".join(p for p in parts if p)


@dataclass
class TaskInstance:
    """A clustered semantic task — the output of AI-based task clustering."""

    task_id: str
    task_label: str
    case_id: str
    start_time: str
    end_time: str
    duration_seconds: float
    event_count: int
    actor_type: str          # HUMAN / AGENT / HYBRID
    human_pct: float
    agent_pct: float
    applications: list[str] = field(default_factory=list)
    events: list[UnifiedActivityEvent] = field(default_factory=list)
    cluster_id: int = -1
    user_id: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["events"] = [e.to_dict() for e in self.events]
        return d


@dataclass
class ProcessVariant:
    """A unique sequence of task labels observed across cases."""

    variant_id: str
    task_sequence: list[str]
    case_ids: list[str]
    frequency: int
    avg_duration_seconds: float
    has_agent_steps: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ProcessIntelligence:
    """Top-level PiG output — everything needed for the dashboard."""

    task_instances: list[TaskInstance]
    variants: list[ProcessVariant]
    total_cases: int = 0
    total_events: int = 0
    agent_adoption_rate: float = 0.0
    avg_cycle_time_seconds: float = 0.0
    avg_cycle_time_with_agent: float = 0.0
    avg_cycle_time_without_agent: float = 0.0
    unique_task_labels: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "task_instances": [t.to_dict() for t in self.task_instances],
            "variants": [v.to_dict() for v in self.variants],
            "total_cases": self.total_cases,
            "total_events": self.total_events,
            "agent_adoption_rate": self.agent_adoption_rate,
            "avg_cycle_time_seconds": self.avg_cycle_time_seconds,
            "avg_cycle_time_with_agent": self.avg_cycle_time_with_agent,
            "avg_cycle_time_without_agent": self.avg_cycle_time_without_agent,
            "unique_task_labels": self.unique_task_labels,
        }
