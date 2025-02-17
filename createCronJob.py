import sys
import subprocess
from datetime import datetime, timedelta

def create_cron_job(course, day, min_time, max_time, players, numOfTeeTimes):
    try:
        day_obj = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    # Find the earliest valid cron day (7 days before, or the closest valid one)
    today = datetime.today()
    for days_prior in range(7, 0, -1):
        potential_run_day = day_obj - timedelta(days=days_prior)
        if potential_run_day >= today:
            cron_day = potential_run_day.day
            cron_month = potential_run_day.month
            break
    else:
        print("No valid prior day found for scheduling the cron job.")
        return

    cron_hour = 6  # Fixed to 6:59 AM
    cron_minute = 59  

    cron_timing = f"{cron_minute} {cron_hour} {cron_day} {cron_month} *"
    cron_command = f"python3 /home/teetimesuser/bookTeeTimes/bookTeeTimes.py '{course}' '{day}' '{min_time}' '{max_time}' '{players}' '{numOfTeeTimes}'"
    cron_job = f"{cron_timing} {cron_command}"

    try:
        result = subprocess.run(
            ["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        existing_cron_jobs = result.stdout.decode()
        if cron_job in existing_cron_jobs:
            print("Cron job already exists!")
            return
    except subprocess.CalledProcessError:
        existing_cron_jobs = ""

    temp_crontab_file = "/tmp/temp_crontab"
    with open(temp_crontab_file, "w") as f:
        f.write(existing_cron_jobs)
        f.write(f"{cron_job}\n")

    try:
        subprocess.run(["crontab", temp_crontab_file], check=True)
        print(f"Cron job created successfully:\n{cron_job}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating cron job: {e}")

def main():
    print("Arguments:", sys.argv)
    if len(sys.argv) != 7:
        print("Usage: python createCronJob.py <course> <day> <minTime> <maxTime> <players> <numOfTeeTimes>")
        sys.exit(1)

    course = sys.argv[1]
    day = sys.argv[2]
    min_time = sys.argv[3]
    max_time = sys.argv[4]
    players = sys.argv[5]
    numOfTeeTimes = sys.argv[6]

    create_cron_job(course, day, min_time, max_time, players, numOfTeeTimes)

if __name__ == "__main__":
    main()
