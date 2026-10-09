# Implementation Plan: PhD Application Tracking System (ATS) Upgrade

## Overview
Transforming the current PhD tracker into a full Application Tracking System (ATS). This involves adding new statuses and timeline tracking for jobs, updating the agent skill to support dual modes (Reviewing new jobs vs Tracking existing ones), and rewriting the README to serve as an intuitive quickstart guide focusing on natural language interactions and model selection.

## Architecture Decisions
- **Minimal Python Changes**: The `jobs_database.json` will remain the source of truth. We will only add a new `update` subcommand to `phd_tracker.py` to handle adding timeline events and changing status safely without the agent needing to manually parse the entire DB.
- **Backward Compatibility**: Existing jobs without a `timeline` array will be handled gracefully by initializing the array when an event is added.
- **Data Airlock Pattern**: The `.tmp/` data airlock pattern for bulk operations remains intact. The new `update` command will operate directly but will be used for single-job atomic updates.
- **Dual-Mode Skill**: The `SKILL.md` will be updated to handle two primary workflows based on user intent: 
  1. Discovery Mode (running the scrapers and finding new jobs).
  2. Tracking/ATS Mode (updating job status, viewing the Kanban board, shortlisting, and adding timeline events).

## Task List

### Phase 1: Python Foundations
- Task 1: Add `update` command to `phd_tracker.py` for status updates and timeline appending.

### Checkpoint: Foundation
- Python CLI correctly updates job statuses and appends to timelines.
- Existing data structure is uncorrupted.

### Phase 2: AI Skill Upgrade (ATS Logic)
- Task 2: Update `SKILL.md` to implement discovery vs. tracking dual modes and define the ATS statuses.

### Checkpoint: Core Features
- The Agent understands the new ATS statuses and can invoke the `update` command properly.
- The Agent can render a Kanban-style summary of job statuses.

### Phase 3: Documentation and Onboarding
- Task 3: Rewrite `README.md` to act as a clear, user-friendly quickstart guide.

### Checkpoint: Complete
- The README explicitly guides users on selecting models and interacting naturally with the agent.
- All acceptance criteria are met.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Database Corruption | High | Keep using CLI abstractions (`update`, `apply`) instead of letting the LLM edit JSON directly. Handle missing `timeline` arrays safely. |
| Agent Confusion | Med | Clearly separate the two modes in `SKILL.md` so the agent doesn't try to scrape when the user just wants to update a job status. |

## Open Questions
- None at this time.
