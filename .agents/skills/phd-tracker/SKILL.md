---
name: phd-tracker
description: >-
  Use this skill when the user asks to run the PhD tracker, check for new PhD jobs, or update the job database.
---

# PhD Tracker Runbook

Follow these exact steps to update the job database and deliver the daily rundown to the user:

## Steps
1. **Scrape New Jobs**: Run the following scripts from the project root using the project's virtual environment to fetch the latest postings. Wait for them to finish.
   * `./.venv/bin/python extractor.py`
   * `./.venv/bin/python extractor_jobsacuk.py`
2. **Generate Report**: Run the report generation script to parse `jobs_database.json` and generate the latest markdown rundown.
   * `./.venv/bin/python generate_report.py`
3. **Deliver Rundown**: Read the contents of `daily_rundown.md` and present the full rundown beautifully in the chat for the user to review.
