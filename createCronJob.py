import sys
import os
import subprocess
from datetime import datetime

def create_cron_job(course, day, min_time, max_time, players):
    # Parse the day parameter (expected format: YYYY-MM-DD)
    try:
        day_obj = datetime.strptime(day, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    # Extract the day, month, and year
    cron_day = day_obj.day
    cron_month = day_obj.month
    
    cron_year = day_obj.year
    cron_hour = 7  # Fixed to 7:00 AM
    cron_minute = 0  # Fixed to 0 minute

    # Build the cron job timing (0 7 <day> <month> *)
    cron_timing = f"{cron_minute} {cron_hour} {cron_day} {cron_month} *"

    # Build the cron command
    cron_command = f"python3 /path/to/bookTeeTimes.py {course} {day} {min_time} {max_time} {players}"

    # Full cron job entry
    cron_job = f"{cron_timing} {cron_command}"

    # Get the current user's crontab
    user = os.getlogin()
    crontab_file = f"/var/spool/cron/crontabs/{user}"

    # Check if the cron job already exists to avoid duplicates
    try:
        with open(crontab_file, 'r') as f:
            existing_cron_jobs = f.read()

        if cron_job in existing_cron_jobs:
            print("Cron job already exists!")
            return
    except Exception as e:
        print(f"Error reading crontab: {e}")

    # Append the new cron job to the crontab file
    try:
        with open(crontab_file, 'a') as f:
            f.write(f"\n{cron_job}\n")
        print(f"Cron job created successfully:\n{cron_job}")
    except Exception as e:
        print(f"Error writing to crontab: {e}")
        return

    # Optionally, reload crontab to apply changes
    try:
        subprocess.run(["crontab", crontab_file], check=True)
        print("Crontab updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update crontab: {e}")


def main():
    # Check if the required number of arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python createCronJob.py <course> <day> <minTime> <maxTime> <players>")
        sys.exit(1)

    # Get parameters from the command line
    course = sys.argv[1]
    day = sys.argv[2]
    min_time = sys.argv[3]
    max_time = sys.argv[4]
    players = sys.argv[5]

    # Create the cron job
    create_cron_job(course, day, min_time, max_time, players)


if __name__ == "__main__":
    main()
