# Autonomous AI PhD Tracker

An automated pipeline that scrapes academic job boards (FindAPhD, jobs.ac.uk), bypasses bot-protections, and uses a scheduled AI agent to evaluate opportunities against a personal CV. 

The system runs completely autonomously in the background, waking up daily to fetch new roles, conduct AI research on the supervisors, and deliver a concise shortlist of perfect matches directly into your terminal or chat.

## How It Works
1. **The Scraper (`extractor.py`)**: A Python Playwright script that mimics human behavior (randomised delays, scrolling) to bypass Cloudflare. It scrapes job descriptions and saves them to a local JSON database.
2. **The AI Brain (`agent_instructions.md`)**: A detailed prompt that instructs a scheduled AI agent to read the database, evaluate new jobs against the user's constraints, research supervisors, and output a daily report.

## Files
*   `extractor.py` - The stealth Playwright scraper for FindAPhD.
*   `extractor_jobsacuk.py` - The stealth Playwright scraper for jobs.ac.uk.
*   `agent_instructions.md` - The execution workflow for the AI agent.
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

### 3. Schedule the AI Agent
To run this autonomously every day without fail, it is highly recommended to use your OS-level task scheduler (like macOS `launchd` or Linux `cron`) rather than an in-chat timer, as chat-timers can be lost if the server restarts.

**For Antigravity (using macOS LaunchAgent):**
Create a `.plist` file in `~/Library/LaunchAgents/` to trigger the AI automatically (e.g., at 8:30 AM). Replace the placeholders with your actual paths and conversation ID:
```xml
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin cd /path/to/phd-tracker && /path/to/agy --conversation YOUR_CHAT_ID --print "Please read and execute the workflow defined in agent_instructions.md"</string>
    </array>
```

**For Claude / ChatGPT Desktop:**
```
"Please read agent_instructions.md. I want you to create a local OS cron job / LaunchAgent on my machine that triggers you every day at 8:30 AM to execute this exact workflow and deliver the results in this chat."
```
