import os
import time
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
if platform.system().lower() == 'windows':
    try:
        import win32evtlog  # type: ignore # For Windows event log
    except ImportError:
        print("win32evtlog is not available on this system.")
from constants import monitoring_files

class LogMonitor:
    def __init__(self):
        self.host_machine = platform.system().lower()
        self.log_files = monitoring_files.get(self.host_machine, {})
        self.last_positions = {}
        self.machines_methods = {
            'linus': self.check_linus_logs,
            'windows': self.check_windows_logs
        }
        self.initialize_positions()

    def initialize_positions(self):
        for file in self.log_files:
            if os.path.exists(file):
                self.last_positions[file] = os.path.getsize(file)
        print(self.last_positions)

    def check_new_logs(self):
        for file in self.log_files:
            if os.path.exists(file):
                self.machines_methods.get(self.host_machine,self.check_linus_logs)(file)

    def check_linus_logs(self, file):
        with open(file, 'r') as f:
            f.seek(self.last_positions.get(file, 0))
            new_lines = f.readlines()
            self.last_positions[file] = f.tell()

        for line in new_lines:
            print(line,file)

    def check_windows_logs(self, file):
        hand = win32evtlog.OpenEventLog(None, "Application")
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)

        events = win32evtlog.ReadEventLog(hand, flags, 0)
        for event in events:
            # if event.EventID == 4625:
            #     print(f"New failed login attempt detected in Windows Event Log")
            print(event,file)
        
    def run(self):
        event_handler = LogFileHandler(self)
        observer = Observer()
        for file in self.log_files:
            if os.path.exists(file):
                observer.schedule(event_handler, path=os.path.dirname(file), recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1) # change time accordingly
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class LogFileHandler(FileSystemEventHandler):
    def __init__(self, log_monitor):
        self.log_monitor = log_monitor

    def on_modified(self, event):
        if not event.is_directory:
            self.log_monitor.machines_methods.get(self.log_monitor.host_machine,self.log_monitor.check_linus_logs)(event.src_path)

if __name__ == "__main__":
    monitor = LogMonitor()
    monitor.run()