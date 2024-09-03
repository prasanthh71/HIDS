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
        self.machinesMethods = {
            'linus': self.checkLinusLogs,
            'windows': self.checkWindowsLogs
        }
        self.initializePositions()

    def initializePositions(self):
        for file in self.log_files:
            if os.path.exists(file):
                self.last_positions[file] = os.path.getsize(file)
        print(self.last_positions)

    def checkNewLogs(self):
        for file in self.log_files:
            if os.path.exists(file):
                self.machinesMethods.get(self.host_machine,self.checkLinusLogs)(file)

    def checkLinusLogs(self, file):
        # with open(file, 'r') as f:
        #     f.seek(self.last_positions.get(file, 0))
        #     new_lines = f.readlines()
        #     self.last_positions[file] = f.tell()

        # for line in new_lines:
        #     if "Failed password" in line:
        #         print(f"New failed login attempt detected in {file}: {line.strip()}")
        print('linux log method is called')

    def checkWindowsLogs(self, file):
        # hand = win32evtlog.OpenEventLog(None, "Security")
        # flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        # total = win32evtlog.GetNumberOfEventLogRecords(hand)

        # events = win32evtlog.ReadEventLog(hand, flags, 0)
        # for event in events:
        #     if event.EventID == 4625:
        #         print(f"New failed login attempt detected in Windows Event Log")
        print('windows log method is called')
        
    def run(self):
        event_handler = LogFileHandler(self)
        observer = Observer()
        for file in self.log_files:
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
            print("File modified: ", event.src_path)
            self.log_monitor.checkNewLogs()

if __name__ == "__main__":
    monitor = LogMonitor()
    monitor.run()