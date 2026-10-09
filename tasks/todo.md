## Task 1: Add `update` command to `phd_tracker.py`

**Description:** Add a new CLI subcommand `update` to `phd_tracker.py` that allows updating a job's status and appending a note to its `timeline`.

**Acceptance criteria:**
- [x] Command supports `--status` to update the job's ATS status (e.g., shortlisted, contacted, applied, interviewing, offered, rejected_post_app).
- [x] Command supports `--note` to append an entry to the job's `timeline` array (with a timestamp).
- [x] Gracefully handles jobs that do not yet have a `timeline` array (initializes it).
- [x] Job updates are saved correctly to `jobs_database.json`.

**Verification:**
- [x] Manual check: Run `python phd_tracker.py update <test_job_id> --status shortlisted --note "Decided to apply"` and verify the JSON database updates correctly.

**Dependencies:** None

**Files likely touched:**
- `phd_tracker.py`

**Estimated scope:** Small: 1 file

---

## Checkpoint: After Task 1
- [x] Database updates properly via the CLI.
- [x] No database truncation or corruption occurs.

---

## Task 2: Update `SKILL.md` with ATS Dual-Mode

**Description:** Modify `.agents/skills/phd-tracker/SKILL.md` to introduce dual modes (Discovery vs. ATS Tracking) so the agent acts as an ATS.

**Acceptance criteria:**
- [ ] Add ATS definitions: statuses (`shortlisted`, `contacted`, `applied`, `interviewing`, `offered`, `rejected_post_app`) and timeline tracking.
- [ ] Clearly define Mode 1 (Discovery): Scraping and evaluating new jobs (the current functionality).
- [ ] Clearly define Mode 2 (ATS / Tracking): Instruct the agent how to use the `update` command to move jobs between statuses, add timeline notes, and display a Kanban-style summary of tracked jobs.
- [ ] Ensure the prompt explicitly instructs the agent to choose the right mode based on the user's request.

**Verification:**
- [ ] Manual check: Review `SKILL.md` to ensure the instructions are unambiguous and properly format the dual modes.

**Dependencies:** 1

**Files likely touched:**
- `.agents/skills/phd-tracker/SKILL.md`

**Estimated scope:** Small: 1 file

---

## Checkpoint: After Task 2
- [ ] The agent instructions successfully encode the new workflow without breaking the old one.

---

## Task 3: Overhaul `README.md` to be a Quickstart Guide

**Description:** Rewrite `README.md` to act as an intuitive, highly user-friendly quickstart guide, emphasizing natural language usage and CLI model selection.

**Acceptance criteria:**
- [ ] Keep the intro brief and focused on what the tool is (Autonomous AI PhD Tracker & ATS).
- [ ] Explain how to select models via the CLI (Claude, ChatGPT, Gemini, etc.).
- [ ] Emphasize that the user just needs to speak to the agent in natural language to track jobs, check the Kanban board, or run discovery.
- [ ] Ensure any mention of cronjobs or background scheduling is removed, focusing purely on agentic chat interaction.

**Verification:**
- [ ] Manual check: Read through `README.md` to ensure it is clear, concise, and accurate to the new capabilities.

**Dependencies:** None (but logically follows 2)

**Files likely touched:**
- `README.md`

**Estimated scope:** Small: 1 file

---

## Checkpoint: Complete
- [ ] All tasks are complete.
- [ ] The full ATS workflow is ready for use.
