import json
import time
import sys
import re
import os
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
            match = re.search(r"\*\*FindAPhD_URL:\*\*\s*(https?://[^\s]+)", content)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    print("Error: Could not find FindAPhD_URL in user_profile.md", file=sys.stderr)
    sys.exit(1)

def load_db():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

def main():
    db = load_db()
    page = 1
    
    base_url = get_target_url()
    
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
        
        while True:
            url = base_url if page == 1 else f"{base_url}&PG={page}"
            print(f"Scraping search page {page}...", file=sys.stderr)
            
            page_obj.goto(url, wait_until="domcontentloaded")
            page_obj.wait_for_timeout(3000)
            html = page_obj.content()
            
            soup = BeautifulSoup(html, "html.parser")
            
            # Find all project/program links on the search page
            results = soup.find_all("a", href=lambda x: x and ("/phds/project/" in x or "/phds/program" in x))
            
            if not results:
                print(f"No results found on page {page}. Stopping pagination.", file=sys.stderr)
                break
                
            found_new_on_page = False
            for link_elem in results:
                href = link_elem["href"]
                job_url = f"https://www.findaphd.com{href}" if href.startswith("/") else href
                
                # Title is usually the text of the link
                title = link_elem.text.replace("\n", "").strip()
                if not title:
                    continue
                    
                job_id = href.split("?")[-1] if "?" in href else href.strip("/")
                
                # Extract the snippet (often in the parent or a sibling div)
                # By going up a few levels to the card container, we can extract all the text
                card = link_elem.find_parent("div", class_=lambda x: x and "row" in x)
                snippet = card.text.strip().replace("\n", " ") if card else "No snippet available."
                
                if job_id not in db:
                    found_new_on_page = True
                    db[job_id] = {
                        "title": title,
                        "url": job_url,
                        "status": "unreviewed",
                        "description": snippet
                    }
                    
            if not found_new_on_page:
                 pass

            page += 1
            
        save_db(db)
            
        # --- PHASE 2: FETCH FULL DESCRIPTIONS ---
        import random
        
        for job_id, job_data in db.items():
            if job_data.get("status") == "unreviewed":
                # Only fetch if it's still just the snippet or empty
                print(f"Fetching full description for {job_data['url']}...", file=sys.stderr)
                try:
                    # Random delay between 5 and 12 seconds to avoid rate limiting
                    delay = random.uniform(5.0, 12.0)
                    print(f"Waiting {delay:.1f}s before next request...", file=sys.stderr)
                    time.sleep(delay)
                    
                    page_obj.goto(job_data['url'], wait_until="domcontentloaded")
                    
                    # Wait up to 15 seconds for the actual description block to appear (bypassing the "Just a moment" screen)
                    try:
                        page_obj.wait_for_selector(".phd-sections__description, .phd-project-description, .project-description", timeout=15000)
                    except:
                        pass # If it times out, we just proceed and try to grab what's there
                        
                    # Simulate human scrolling
                    page_obj.evaluate("window.scrollBy(0, 500)")
                    time.sleep(1)
                    page_obj.evaluate("window.scrollBy(0, 500)")
                    
                    content = page_obj.evaluate("""() => {
                        const desc = document.querySelector('.phd-sections__description') || 
                                     document.querySelector('.phd-project-description') ||
                                     document.querySelector('.project-description');
                        // Fallback to body only if the block string isn't there
                        if (desc) return desc.innerText;
                        if (!document.body.innerText.includes("Sorry, you have been blocked")) {
                            return document.body.innerText;
                        }
                        return "Cloudflare Blocked";
                    }""")
                    
                    if content and content != "Cloudflare Blocked":
                        job_data['description'] = content
                    save_db(db)
                except Exception as e:
                    print(f"Failed to fetch {job_data['url']}: {e}", file=sys.stderr)
                    
        browser.close()
        
    print("Database sync complete.", file=sys.stderr)

if __name__ == "__main__":
    main()
