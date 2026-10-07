# Autonomous AI PhD Tracker

An automated pipeline that scrapes academic job boards (FindAPhD, jobs.ac.uk), bypasses bot-protections, and uses a scheduled AI agent to evaluate opportunities against a personal CV. 

The system runs completely autonomously in the background, waking up daily to fetch new roles, conduct AI research on the supervisors, and deliver a concise shortlist of perfect matches directly into your terminal or chat.

## How It Works
1. **The Scraper (`extractor.py`)**: A Python Playwright script that mimics human behavior (randomised delays, scrolling) to bypass Cloudflare. It scrapes job descriptions and saves them to a local JSON database.
2. **The AI Brain (`.agents/skills/phd-tracker/SKILL.md`)**: A custom Antigravity Skill that teaches the agent how to run the tracking pipeline, parse the JSON, and output the daily rundown.

## Files
*   `extractor.py` - The stealth Playwright scraper for FindAPhD.
*   `extractor_jobsacuk.py` - The stealth Playwright scraper for jobs.ac.uk.
*   `.agents/skills/phd-tracker/SKILL.md` - The Antigravity Skill definition.
*   `generate_report.py` - Parses the database and creates the markdown rundown.
*   `user_profile.md` - Your personal background, CV details, and hard constraints for the AI to judge against.
*   `requirements.txt` - Python dependencies.
*   *(Generated)* `jobs_database.json` - Local state machine tracking `unreviewed`, `pending`, and `rejected` jobs.

## Setup & Execution

### 1. Install Dependencies
*(Note: It is highly recommended to name your virtual environment exactly `.venv` as shown below, because the scheduled AI agent is explicitly instructed to execute the scraper from that directory).*
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Your Profile
Rename `user_profile.template.md` to `user_profile.md`. 
Inside, paste your specific FindAPhD search URL at the top, and write out your CV details, research interests, and hard constraints (e.g., location, funding requirements).

### 3. Run the Pipeline
To update the database and get your daily rundown, open the chat window with the Antigravity agent in this workspace and simply ask it to execute the skill:

```
"Run the PhD tracker"
```

Because the skill is built into the workspace (in `.agents/skills/phd-tracker/SKILL.md`), the agent will automatically discover it, run the scrapers and parsers in the foreground, and present the final Markdown rundown safely in the chat window.
