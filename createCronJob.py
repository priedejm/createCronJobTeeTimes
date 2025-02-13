import sys
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
    cron_hour = 7  # Fixed to 7:00 AM
    cron_minute = 0  # Fixed to 0 minute

    # Build the cron job timing (0 7 <day> <month> *)
    cron_timing = f"{cron_minute} {cron_hour} {cron_day} {cron_month} *"

    # Ensure course, day, min_time, max_time, and players are wrapped in quotes
    cron_command = f"python3 /home/teetimesuser/bookTeeTimes/bookTeeTimes.py \"{course}\" \"{day}\" \"{min_time}\" \"{max_time}\" \"{players}\""

    # Full cron job entry
    cron_job = f"{cron_timing} {cron_command}"

    # Check if the cron job already exists by listing current cron jobs
    try:
        result = subprocess.run(
            ["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
        existing_cron_jobs = result.stdout.decode()
        if cron_job in existing_cron_jobs:
            print("Cron job already exists!")
            return
    except subprocess.CalledProcessError:
        # If there are no existing cron jobs (crontab -l fails), we simply continue
        existing_cron_jobs = ""

    # Add the new cron job to the crontab using echo and crontab
    try:
        # Append the cron job to the current list of cron jobs and update crontab
        subprocess.run(
            f"(echo '{existing_cron_jobs}' ; echo '{cron_job}') | crontab -",
            shell=True,
            check=True
        )
        print(f"Cron job created successfully:\n{cron_job}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating cron job: {e}")

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
