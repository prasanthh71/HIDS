rules_directory = './rules'
parsed_rules_file = './parsedRules.json'
test_directory = './tests'

monitoring_files = {
    'windows': [
        r"C:\Windows\System32\config\SAM",
        r"C:\Windows\System32\config\SYSTEM",
        # Hosts file for network configurations.
        r"C:\Windows\System32\drivers\etc\hosts",
        r"C:\Windows\System32\winevt\Logs\Security.evtx",
        r"C:\Windows\System32\winevt\Logs\Application.evtx",
        r"C:\Windows\System32\winevt\Logs\System.evtx",
        r"C:\Windows\explorer.exe",
        r"C:\Windows\System32\winlogon.exe",
        r"C:\Windows\System32\services.exe",
        r"C:\Windows\System32\svchost.exe",
        r"C:\Windows\System32\ntoskrnl.exe",
        r"C:\Windows\System32\kernel32.dll",
        r"C:\Windows\System32\user32.dll",
        r"C:\Windows\System32\firewall.cpl",
        r"C:\Program Files\Common Files\System\masadc"
    ],
    'linux': [
        # User account information and passwords.
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        # Local network configuration.
        "/etc/hosts",
        # Authentication logs, including SSH login attempts.
        "/var/log/auth.log",
        # General system logs for various activities.
        "/var/log/syslog",
        # Kernel logs, capturing low-level system operations.
        "/var/log/kern.log",
        "/etc/crontab",
        "/etc/ssh/sshd_config",
        # Common directories for system binaries.
        "/bin/bash",
        "/bin/sh",
        "/sbin/init",
        "/lib/systemd/systemd",
        "/etc/ld.so.conf"
    ]
}
