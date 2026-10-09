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
2. **Extract Unreviewed**: Extract only the new jobs so you don't have to read the massive database directly. (Note: You can also use `./.venv/bin/python phd_tracker.py extract --status pending` in the future if the user asks you to list pending jobs).
   * `./.venv/bin/python phd_tracker.py extract --status unreviewed`
   * (This creates a tiny `.tmp/unreviewed.json` file for you to read)
3. **Evaluate Jobs**: Read `.tmp/unreviewed.json` and `user_profile.md`. 
   * **Circuit Breaker:** If `.tmp/unreviewed.json` is empty or contains 0 jobs, STOP execution immediately and output "No new jobs found today."
   * For each unreviewed job:
     * Read the job's `description`.
     * Evaluate it strictly against the user profile constraints (e.g., London, Fully Funded).
     * Verify if it aligns with their **applied ML/Ecology interests**.
     * Decide its status: `pending` (good match), `rejected` (poor match), or `manual_review` (if the description is highly ambiguous or you are unsure if it fits).
4. **Update Database**: Create a file named `.tmp/evaluations.json` with a dictionary mapping job IDs to your decisions (e.g. `{"p123": {"status": "pending", "reason": "Matches applied ML interests"}}`). Then run the apply command to securely update the database without writing the entire JSON tree yourself.
   * `./.venv/bin/python phd_tracker.py apply .tmp/evaluations.json`
5. **Supervisor Research**: For every job you just moved to `pending`, you MUST invoke a `research` subagent (using the `invoke_subagent` tool). Do NOT just extract the supervisor's name from the job description. You must instruct the subagent to search the web for the lead supervisor and return a short summary of their background, **primary research interests**, and notable recent publications.
6. **Deliver Rundown**: Output a direct chat message containing a comprehensive daily rundown of ALL newly processed jobs. Do not ask for user input to approve/reject them—just provide the static report.
   * **For Rejected Jobs:** List the Title, a one-line summary, and a clear 1-sentence explanation of why you rejected it.
   * **For Manual Review Jobs:** List the Title, a one-line summary, and specifically explain what information is missing or ambiguous that prevented you from making a decision.
   * **For Pending Jobs (The "One-Stop-Shop" Summary):** Provide a comprehensive breakdown:
     - **Basic Info:** Title (with link), University, and School/Department.
     - **Project Overview:** A small summary of the project and what it entails.
     - **Ideal Candidate:** The specific student profile they are looking for (skills, background, requirements).
     - **Why it Fits:** A one-line summary of why it matches the user's constraints.
     - **Supervisor Profile:** The deep-dive research returned by your subagent (background, interests, publications).
   * If there were no new jobs today, output "No new jobs found today."
