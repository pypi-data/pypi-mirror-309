# code_time_tracker/cli.py

import click
from code_time_tracker.time_tracker import TimeTracker
from code_time_tracker.data_storage import save_log
import time

tracker = TimeTracker()

@click.group()
def cli():
    pass

@click.command()
def start():
    tracker.start()

@click.command()
def stop():
    duration = tracker.stop()
    save_log("coding_logs.csv", [time.ctime(tracker.start_time), time.ctime(tracker.end_time), duration])
    print(f"Session duration: {duration:.2f} seconds")

cli.add_command(start)
cli.add_command(stop)

if __name__ == "__main__":
    cli()

