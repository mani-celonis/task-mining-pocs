"""
AI-based task clustering engine.

Takes a stream of UnifiedActivityEvents and clusters them into semantic
TaskInstances. Uses TF-IDF vectorization of event features + KMeans,
mirroring the ML_JOB / ML_WORKBENCH DataProcessingStrategy in cloud-task-mining.

Within each case, events are grouped temporally and then each group is
assigned to the nearest cluster centroid, producing labeled task instances.
"""

from __future__ import annotations
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import groupby

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

from pipeline.models import UnifiedActivityEvent, TaskInstance, ActorType


# Sensible labels inferred from cluster centroids
_LABEL_TEMPLATES = [
    "Create Sales Order",
    "Review Loan Application",
    "AI Credit Risk Assessment",
    "Draft & Send Approval",
    "Update Customer Record",
    "Document Verification",
    "Compliance Check",
    "Data Entry & Validation",
    "Email Communication",
    "Meeting Follow-up",
]


def _parse_ts(ts: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)


def _compute_actor_type(events: list[UnifiedActivityEvent]) -> tuple[str, float, float]:
    human = sum(1 for e in events if e.actor_type == ActorType.HUMAN.value)
    agent = sum(1 for e in events if e.actor_type == ActorType.AGENT.value)
    total = max(human + agent, 1)
    h_pct = round(human / total * 100, 1)
    a_pct = round(agent / total * 100, 1)
    if human > 0 and agent > 0:
        return ActorType.HYBRID.value, h_pct, a_pct
    if agent > 0:
        return ActorType.AGENT.value, h_pct, a_pct
    return ActorType.HUMAN.value, h_pct, a_pct


class TaskClusteringEngine:
    """
    Two-phase clustering:
      1) Global phase: TF-IDF + KMeans across ALL events to discover task archetypes
      2) Case phase: within each case, segment events temporally and assign segments
         to the nearest archetype, producing TaskInstance objects.
    """

    def __init__(self, n_clusters: int = 6, gap_threshold_seconds: int = 90):
        self.n_clusters = n_clusters
        self.gap_threshold = gap_threshold_seconds
        self.vectorizer = TfidfVectorizer(max_features=200, stop_words="english")
        self.kmeans: KMeans | None = None
        self.cluster_labels: dict[int, str] = {}

    def fit_and_cluster(self, events: list[UnifiedActivityEvent]) -> list[TaskInstance]:
        if not events:
            return []

        texts = [e.feature_text() for e in events]
        tfidf_matrix = self.vectorizer.fit_transform(texts)

        n_clusters = min(self.n_clusters, len(set(texts)))
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = self.kmeans.fit_predict(tfidf_matrix)

        self._assign_labels(events, labels)

        for i, event in enumerate(events):
            event.context["_cluster_id"] = int(labels[i])

        return self._build_task_instances(events)

    def _assign_labels(self, events: list[UnifiedActivityEvent], labels: np.ndarray):
        """Derive human-readable labels for each cluster based on dominant features."""
        cluster_events: dict[int, list[UnifiedActivityEvent]] = defaultdict(list)
        for i, e in enumerate(events):
            cluster_events[int(labels[i])].append(e)

        for cid, evts in cluster_events.items():
            label = self._infer_label(evts, cid)
            self.cluster_labels[cid] = label

    def _infer_label(self, events: list[UnifiedActivityEvent], cluster_id: int) -> str:
        apps = [e.application for e in events]
        types = [e.event_type for e in events]
        titles = [e.title or "" for e in events]
        contexts = [str(e.context) for e in events]
        has_agent = any(e.actor_type == ActorType.AGENT.value for e in events)

        combined = " ".join(apps + types + titles + contexts).lower()

        if "sap" in combined and ("order" in combined or "va01" in combined):
            return "Create Sales Order"
        if has_agent and ("risk" in combined or "credit" in combined or "fico" in combined or "summarize" in combined or "rag" in combined):
            return "AI Credit Risk Assessment"
        if has_agent and ("draft" in combined or "approval" in combined):
            return "Draft & Send Approval"
        if "outlook" in combined and ("loan" in combined or "review" in combined or "inbox" in combined):
            if has_agent:
                return "Draft & Send Approval"
            return "Review Loan Application"
        if "sharepoint" in combined and ("credit" in combined or "report" in combined):
            return "Document Verification"
        if "excel" in combined and ("risk" in combined or "calculator" in combined):
            return "Manual Risk Analysis"
        if "excel" in combined or "sharepoint" in combined:
            return "Document Verification"
        if "outlook" in combined and ("compose" in combined or "new message" in combined):
            return "Email Communication"
        if has_agent and "compliance" in combined:
            return "Compliance Check"
        if "meeting" in combined or "teams" in combined:
            return "Meeting Follow-up"
        if "sap" in combined:
            return "Update Customer Record"

        used = set(self.cluster_labels.values())
        for tmpl in _LABEL_TEMPLATES:
            if tmpl not in used:
                return tmpl
        return f"Task Group {cluster_id + 1}"

    def _build_task_instances(self, events: list[UnifiedActivityEvent]) -> list[TaskInstance]:
        """Segment events by case, then by temporal gaps, then assign cluster labels."""
        case_events: dict[str, list[UnifiedActivityEvent]] = defaultdict(list)
        for e in events:
            key = e.case_correlation_id or "UNKNOWN"
            case_events[key].append(e)

        task_instances = []
        for case_id, evts in case_events.items():
            evts.sort(key=lambda e: e.timestamp)
            segments = self._temporal_segment(evts)

            for segment in segments:
                cluster_id = self._majority_cluster(segment)
                label = self.cluster_labels.get(cluster_id, f"Task {cluster_id}")
                actor_type, h_pct, a_pct = _compute_actor_type(segment)

                start = _parse_ts(segment[0].timestamp)
                end = _parse_ts(segment[-1].timestamp)
                duration = max((end - start).total_seconds(), 1.0)
                apps = sorted(set(e.application for e in segment))

                ti = TaskInstance(
                    task_id=str(uuid.uuid4())[:8],
                    task_label=label,
                    case_id=case_id,
                    start_time=segment[0].timestamp,
                    end_time=segment[-1].timestamp,
                    duration_seconds=round(duration, 1),
                    event_count=len(segment),
                    actor_type=actor_type,
                    human_pct=h_pct,
                    agent_pct=a_pct,
                    applications=apps,
                    events=segment,
                    cluster_id=cluster_id,
                    user_id=segment[0].actor_id,
                )
                task_instances.append(ti)

        return task_instances

    def _temporal_segment(self, events: list[UnifiedActivityEvent]) -> list[list[UnifiedActivityEvent]]:
        """Split a case's events into segments separated by gaps > threshold."""
        if not events:
            return []

        segments: list[list[UnifiedActivityEvent]] = [[events[0]]]
        for i in range(1, len(events)):
            prev_ts = _parse_ts(events[i - 1].timestamp)
            curr_ts = _parse_ts(events[i].timestamp)
            gap = (curr_ts - prev_ts).total_seconds()

            if gap > self.gap_threshold:
                segments.append([events[i]])
            else:
                segments[-1].append(events[i])

        return segments

    @staticmethod
    def _majority_cluster(events: list[UnifiedActivityEvent]) -> int:
        counts: dict[int, int] = defaultdict(int)
        for e in events:
            cid = e.context.get("_cluster_id", -1)
            counts[cid] += 1
        return max(counts, key=counts.get) if counts else -1
