"""
Process Intelligence Graph (PiG) builder and analytics engine.

Takes clustered TaskInstances and computes:
  - Process variants (unique task sequences per case)
  - KPIs (cycle times, adoption rates, efficiency gains)
  - Aggregated intelligence for the dashboard
"""

from __future__ import annotations
import uuid
from collections import defaultdict

from pipeline.models import (
    TaskInstance,
    ProcessVariant,
    ProcessIntelligence,
    ActorType,
)
from pipeline.clustering import _parse_ts


def build_process_intelligence(
    task_instances: list[TaskInstance],
    total_raw_events: int,
) -> ProcessIntelligence:
    """Assemble the full PiG output from clustered task instances."""

    case_tasks = _group_by_case(task_instances)
    variants = _extract_variants(case_tasks)

    cases_with_agent = set()
    cases_without_agent = set()
    cycle_times_with = []
    cycle_times_without = []

    for case_id, tasks in case_tasks.items():
        has_agent = any(t.actor_type in (ActorType.AGENT.value, ActorType.HYBRID.value) for t in tasks)
        cycle = _case_cycle_time(tasks)

        if has_agent:
            cases_with_agent.add(case_id)
            cycle_times_with.append(cycle)
        else:
            cases_without_agent.add(case_id)
            cycle_times_without.append(cycle)

    total_cases = len(case_tasks)
    adoption = len(cases_with_agent) / max(total_cases, 1)

    all_labels = sorted(set(t.task_label for t in task_instances))

    all_cycles = cycle_times_with + cycle_times_without

    return ProcessIntelligence(
        task_instances=task_instances,
        variants=variants,
        total_cases=total_cases,
        total_events=total_raw_events,
        agent_adoption_rate=round(adoption * 100, 1),
        avg_cycle_time_seconds=round(_avg(all_cycles), 1),
        avg_cycle_time_with_agent=round(_avg(cycle_times_with), 1) if cycle_times_with else 0,
        avg_cycle_time_without_agent=round(_avg(cycle_times_without), 1) if cycle_times_without else 0,
        unique_task_labels=all_labels,
    )


def _group_by_case(tasks: list[TaskInstance]) -> dict[str, list[TaskInstance]]:
    groups: dict[str, list[TaskInstance]] = defaultdict(list)
    for t in tasks:
        groups[t.case_id].append(t)
    for case_tasks in groups.values():
        case_tasks.sort(key=lambda t: t.start_time)
    return groups


def _extract_variants(case_tasks: dict[str, list[TaskInstance]]) -> list[ProcessVariant]:
    variant_map: dict[str, list[str]] = defaultdict(list)
    variant_durations: dict[str, list[float]] = defaultdict(list)
    variant_has_agent: dict[str, bool] = {}

    for case_id, tasks in case_tasks.items():
        seq = tuple(t.task_label for t in tasks)
        key = " → ".join(seq)
        variant_map[key].append(case_id)
        variant_durations[key].append(_case_cycle_time(tasks))

        has_agent = any(t.actor_type in (ActorType.AGENT.value, ActorType.HYBRID.value) for t in tasks)
        variant_has_agent[key] = has_agent

    variants = []
    for seq_str, case_ids in variant_map.items():
        labels = seq_str.split(" → ")
        variants.append(ProcessVariant(
            variant_id=str(uuid.uuid4())[:8],
            task_sequence=labels,
            case_ids=case_ids,
            frequency=len(case_ids),
            avg_duration_seconds=round(_avg(variant_durations[seq_str]), 1),
            has_agent_steps=variant_has_agent.get(seq_str, False),
        ))

    variants.sort(key=lambda v: v.frequency, reverse=True)
    return variants


def _case_cycle_time(tasks: list[TaskInstance]) -> float:
    if not tasks:
        return 0.0
    start = _parse_ts(tasks[0].start_time)
    end = _parse_ts(tasks[-1].end_time)
    return max((end - start).total_seconds(), 1.0)


def _avg(values: list[float]) -> float:
    return sum(values) / max(len(values), 1)
