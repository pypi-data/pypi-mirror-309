# code_time_tracker/file_monitor.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class FileMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

def start_monitoring(path):
    observer = Observer()
    event_handler = FileMonitor()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

