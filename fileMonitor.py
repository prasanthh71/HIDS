import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32evtlog  # For Windows event log
import re

class LogMonitor:
    def __init__(self):
        self.log_files = {
            'linux': ['/var/log/auth.log', '/var/log/secure'],
            'windows': ['C:\\Windows\\System32\\winevt\\Logs\\Security.evtx']
        }
        self.last_positions = {}
        self.initialize_positions()

    def initialize_positions(self):
        for os_type, files in self.log_files.items():
            for file in files:
                if os.path.exists(file):
                    self.last_positions[file] = os.path.getsize(file)

    def check_new_logs(self):
        for os_type, files in self.log_files.items():
            for file in files:
                if os.path.exists(file):
                    if os_type == 'linux':
                        self.check_linux_log(file)
                    elif os_type == 'windows':
                        self.check_windows_log(file)

    def check_linux_log(self, file):
        with open(file, 'r') as f:
            f.seek(self.last_positions.get(file, 0))
            new_lines = f.readlines()
            self.last_positions[file] = f.tell()

        for line in new_lines:
            if "Failed password" in line:
                print(f"New failed login attempt detected in {file}: {line.strip()}")

    def check_windows_log(self, file):
        hand = win32evtlog.OpenEventLog(None, "Security")
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)

        events = win32evtlog.ReadEventLog(hand, flags, 0)
        for event in events:
            if event.EventID == 4625:
                print(f"New failed login attempt detected in Windows Event Log")

    def run(self):
        event_handler = LogFileHandler(self)
        observer = Observer()
        for os_type, files in self.log_files.items():
            for file in files:
                if os.path.exists(file):
                    observer.schedule(event_handler, path=os.path.dirname(file), recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_monitor):
        self.log_monitor = log_monitor

    def on_modified(self, event):
        if not event.is_directory:
            self.log_monitor.check_new_logs()

if __name__ == "__main__":
    monitor = LogMonitor()
    monitor.run()