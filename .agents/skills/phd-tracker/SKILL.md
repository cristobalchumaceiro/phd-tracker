---
name: phd-tracker
description: >-
  Use this skill when the user asks to run the PhD tracker, check for new PhD jobs, or update the job database.
---

# PhD Tracker Runbook

Follow these exact steps to update the job database and deliver the daily rundown to the user:

## Steps
1. **Scrape New Jobs**: Run the unified tracker script to fetch the latest postings.
   * `./.venv/bin/python phd_tracker.py scrape`
2. **Extract Unreviewed**: Extract only the new jobs so you don't have to read the massive database directly.
   * `./.venv/bin/python phd_tracker.py get-unreviewed`
   * (This creates a tiny `unreviewed.json` file for you to read)
3. **Evaluate Jobs**: Read `unreviewed.json` and `user_profile.md`. For each unreviewed job:
   * Read the job's `description`.
   * Evaluate it strictly against the user profile constraints (e.g., London, Fully Funded).
   * Verify if it aligns with their **applied ML/Ecology interests**.
   * Decide if it should be `pending` (good match) or `rejected` (poor match).
4. **Update Database**: Create a file named `evaluations.json` with a dictionary mapping job IDs to your decisions (e.g. `{"p123": {"status": "pending", "reason": "Matches applied ML interests"}}`). Then run the apply command to securely update the database without writing the entire JSON tree yourself.
   * `./.venv/bin/python phd_tracker.py apply evaluations.json`
5. **Supervisor Research**: For every job you just moved to `pending`, invoke a `research` subagent (using `invoke_subagent`). Instruct the subagent to research the lead supervisor of the project and return a short summary of their background, **primary research interests**, and notable recent publications.
6. **Deliver Rundown**: Output a direct chat message containing a highly concise daily rundown of ALL newly processed jobs.
   * **For Rejected Jobs:** List the Title, a one-line summary, and a clear 1-sentence explanation of why you rejected it.
   * **For Pending Jobs:** List the Title (with a link), Institution, a one-line summary of the fit, and the Supervisor Profile (based on your subagent's research).
   * If there were no new jobs today, output "No new jobs found today."
