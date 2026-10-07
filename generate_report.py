import json

def main():
    try:
        with open('jobs_database.json', 'r') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print("Database not found.")
        return

    pending_jobs = []
    unreviewed_jobs = []
    
    for job_id, job in jobs.items():
        status = job.get('status')
        if status == 'pending':
            pending_jobs.append(job)
        elif status == 'unreviewed':
            unreviewed_jobs.append(job)

    with open('daily_rundown.md', 'w') as f:
        f.write("### 📊 Daily Rundown\n\n")
        
        if unreviewed_jobs:
            f.write(f"**{len(unreviewed_jobs)} New Unreviewed Jobs**\n\n")
            for i, job in enumerate(unreviewed_jobs, 1):
                f.write(f"{i}. [{job.get('title')}]({job.get('url')})\n")
                f.write(f"   * *Description Snippet:* {job.get('description', '')[:200]}...\n\n")
            f.write("---\n\n")

        f.write(f"**{len(pending_jobs)} Pending Jobs Found**\n\n")
        for i, job in enumerate(pending_jobs, 1):
            f.write(f"{i}. [{job.get('title')}]({job.get('url')})\n")
            f.write(f"   * *Fit:* {job.get('reason', 'Matches interests.')}\n")

if __name__ == "__main__":
    main()
