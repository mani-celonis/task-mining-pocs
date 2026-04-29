---
description: Feature request prioritization context — scoring model, context docs, debrief email setup. Loads when working on the feature prioritizer skill or executors.
paths:
  - ".claude/skills/aha-feature-prioritizer/**"
  - ".claude/skills/aha-feature-setup-wizard/**"
  - "src/executors/aha_feature_requests.py"
  - "src/executors/aha_prioritize.py"
  - "src/executors/send_debrief_email.py"
---

# Feature request prioritization — rules

## Config location

All feature request settings live under `feature_requests:` in `.aha-config.yml`. If missing, invoke the setup wizard first.

## Scoring model (weighted, 0–10)

| Factor | Default weight | Source |
|---|---|---|
| `customer_impact` | 0.35 | Endorsement count x customer tier |
| `strategic_alignment` | 0.30 | Idea description vs context docs |
| `engineering_effort` | 0.15 | Keyword heuristic (inverted: small effort = higher score) |
| `time_sensitivity` | 0.10 | Update recency + keywords ("blocked", "cutoff", "deadline") |
| `frequency` | 0.10 | Vote count normalized |

Tiers: HIGH >= 7, MEDIUM 5-7, BACKLOG < 5.

## Context documents

Loaded from `feature_requests.context_docs` paths in `.aha-config.yml`. Product strategy, research, and design docs used to score strategic_alignment.

## Output

Reports saved to `data/feature-priorities/YYYY-MM-DD.md` (gitignored). Never commit these.

## Daily debrief

Via SMTP using `send_debrief_email.py`. Scheduled via macOS launchd at `~/Library/LaunchAgents/com.ahaagent.debrief.plist`. Credentials in `.env` under `SMTP_*` and `DEBRIEF_EMAIL_TO`.

## Safety

- Never update Aha! statuses without explicit user confirmation.
- Never commit `data/feature-priorities/` files.
- Always show dry-run output before activating the launchd job.
