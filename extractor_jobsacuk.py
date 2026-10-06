import json
import time
import sys
import re
import os
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(SCRIPT_DIR, "user_profile.md")
DB_PATH = os.path.join(SCRIPT_DIR, "jobs_database.json")

def get_target_url():
    try:
        with open(PROFILE_PATH, "r") as f:
            content = f.read()
            match = re.search(r"\*\*JobsAcUk_URL:\*\*\s*(https?://[^\s]+)", content)
            if match and "Coming Soon" not in match.group(1):
                return match.group(1).strip()
    except Exception:
        pass
    print("Warning: Could not find JobsAcUk_URL in user_profile.md, skipping jobs.ac.uk run.", file=sys.stderr)
    sys.exit(0)

def load_db():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

def main():
    base_url = get_target_url()
    if not base_url:
        return

    db = load_db()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page_obj = context.new_page()
        Stealth().apply_stealth_sync(page_obj)
        
        # --- PHASE 1: Collect Links ---
        start_index = 1
        new_jobs = {}
        
        while True:
            url = base_url if start_index == 1 else f"{base_url}&pageSize=25&startIndex={start_index}"
            print(f"Scraping jobs.ac.uk search page (startIndex {start_index})...", file=sys.stderr)
            
            page_obj.goto(url, wait_until="domcontentloaded")
            time.sleep(random.uniform(3, 6)) # Human delay
            
            links = page_obj.locator('a[href^="/job/"]').all()
            if not links:
                print(f"No results found on startIndex {start_index}. Stopping pagination.", file=sys.stderr)
                break
                
            page_found = False
            for link in links:
                href = link.get_attribute("href")
                title = link.inner_text().strip()
                if not href or not title:
                    continue
                
                full_url = f"https://www.jobs.ac.uk{href}"
                job_id = href.split('/')[2] if len(href.split('/')) > 2 else href
                
                # Check uniqueness (jobs.ac.uk can duplicate links on the same page)
                if job_id not in new_jobs and job_id not in db:
                    new_jobs[job_id] = {
                        "title": title,
                        "url": full_url,
                        "status": "unreviewed"
                    }
                    page_found = True
                    
            if not page_found:
                print(f"No new jobs on startIndex {start_index}. Stopping pagination.", file=sys.stderr)
                break
                
            start_index += 25

        # --- PHASE 2: Fetch Descriptions ---
        for job_id, job in new_jobs.items():
            print(f"Fetching full description for {job['url']}...", file=sys.stderr)
            
            try:
                page_obj.goto(job["url"], wait_until="domcontentloaded")
                
                # Human scroll behavior
                page_obj.evaluate("window.scrollBy(0, 500)")
                time.sleep(random.uniform(2, 4))
                page_obj.evaluate("window.scrollBy(0, 500)")
                
                # We extract the entire body text because jobs.ac.uk DOM varies heavily by university
                desc = page_obj.evaluate("document.body.innerText")
                if not desc:
                    desc = "Failed to extract description."
                    
                job["description"] = desc.strip()
                
            except Exception as e:
                print(f"Failed to fetch {job['url']}: {e}", file=sys.stderr)
                job["description"] = "Failed to fetch."

            db[job_id] = job
            save_db(db)
            
            delay = random.uniform(5, 10)
            print(f"Waiting {delay:.1f}s before next request...", file=sys.stderr)
            time.sleep(delay)

        browser.close()
        
    print("Jobs.ac.uk database sync complete.", file=sys.stderr)

if __name__ == "__main__":
    main()
