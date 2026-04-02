"""
Flask web server providing:
  - Dashboard UI at /
  - REST API at /api/* for raw data, pipeline results, and analytics
"""

from __future__ import annotations
import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template

from data.generator import generate_contoso_data
from pipeline.adapters import TaskMiningAdapter, WorkIQAdapter
from pipeline.clustering import TaskClusteringEngine
from pipeline.analytics import build_process_intelligence
from pipeline.models import ProcessIntelligence

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"

_cache: dict = {}


def run_pipeline() -> dict:
    """Execute the full pipeline and cache results."""
    if _cache.get("result"):
        return _cache["result"]

    print("\n[1/4] Generating Contoso Financial dummy data...")
    tm_raw, wiq_raw = generate_contoso_data()
    print(f"       Task Mining events: {len(tm_raw)}")
    print(f"       Work IQ events:     {len(wiq_raw)}")

    print("[2/4] Normalizing via source adapters...")
    tm_adapter = TaskMiningAdapter()
    wiq_adapter = WorkIQAdapter()
    tm_unified = tm_adapter.normalize(tm_raw)
    wiq_unified = wiq_adapter.normalize(wiq_raw)
    all_events = sorted(tm_unified + wiq_unified, key=lambda e: e.timestamp)
    print(f"       Unified events:     {len(all_events)}")

    print("[3/4] Running AI-based task clustering (TF-IDF + KMeans)...")
    engine = TaskClusteringEngine(n_clusters=6, gap_threshold_seconds=90)
    task_instances = engine.fit_and_cluster(all_events)
    print(f"       Task instances:     {len(task_instances)}")
    print(f"       Cluster labels:     {list(engine.cluster_labels.values())}")

    print("[4/4] Building Process Intelligence Graph...")
    pig = build_process_intelligence(task_instances, len(all_events))
    print(f"       Process variants:   {len(pig.variants)}")
    print(f"       Agent adoption:     {pig.agent_adoption_rate}%")
    print(f"       Avg cycle (agent):  {pig.avg_cycle_time_with_agent}s")
    print(f"       Avg cycle (manual): {pig.avg_cycle_time_without_agent}s")
    print()

    result = {
        "raw_tm_events": [e for e in tm_raw],
        "raw_wiq_events": [e for e in wiq_raw],
        "unified_events": [e.to_dict() for e in all_events],
        "pig": pig.to_dict(),
    }
    _cache["result"] = result
    return result


def _load_samples() -> dict:
    samples = {}
    for name in ["work_iq_schema", "work_iq_sample_events", "task_mining_sample_events", "unified_activity_schema"]:
        path = SAMPLES_DIR / f"{name}.json"
        if path.exists():
            with open(path) as f:
                samples[name] = json.load(f)
    return samples


@app.route("/")
def dashboard():
    data = run_pipeline()
    samples = _load_samples()
    return render_template(
        "dashboard.html",
        data_json=json.dumps(data),
        samples_json=json.dumps(samples),
    )


@app.route("/api/raw")
def api_raw():
    data = run_pipeline()
    return jsonify({
        "task_mining_events": data["raw_tm_events"],
        "work_iq_events": data["raw_wiq_events"],
    })


@app.route("/api/unified")
def api_unified():
    data = run_pipeline()
    return jsonify(data["unified_events"])


@app.route("/api/pig")
def api_pig():
    data = run_pipeline()
    return jsonify(data["pig"])


@app.route("/api/pipeline")
def api_pipeline():
    data = run_pipeline()
    return jsonify(data)


@app.route("/api/samples")
def api_samples():
    return jsonify(_load_samples())
