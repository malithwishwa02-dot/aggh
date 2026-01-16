import subprocess

def disable_w32time():
    subprocess.run(["sc", "stop", "w32time"])
    subprocess.run(["sc", "config", "w32time", "start= disabled"])

def block_udp_123():
    subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=Block NTP", "dir=out", "action=block", "protocol=UDP", "localport=123"])

def restore_w32time():
    subprocess.run(["sc", "config", "w32time", "start= auto"])
    subprocess.run(["sc", "start", "w32time"])
    subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=Block NTP"])
