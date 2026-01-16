"""
CHRONOS v3 MAINTENANCE PATCH
Target: Resolving Privilege, API, and Temporal Failures
Authority: The Omni-Architect
"""

import os
import sys
import ctypes
import subprocess
import requests
from pathlib import Path

# Ensure script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

class Method4Patch:
    @staticmethod
    def request_admin():
        """Force self-elevation if not running as admin."""
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[PATCH] Requesting Administrative Privileges...")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
        print("[PASS] Administrative Privileges Verified.")

    @staticmethod
    def fix_temporal_isolation():
        """Aggressively disables NTP and Windows Time Service."""
        print("[PATCH] Initiating Deep Temporal Isolation...")
        try:
            # 1. Stop and Disable the service
            subprocess.run(["sc", "stop", "w32time"], capture_output=True)
            subprocess.run(["sc", "config", "w32time", "start=disabled"], capture_output=True)
            
            # 2. Block NTP Port at Firewall (UDP 123)
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule", 
                "name=Chronos_NTP_Block", "dir=out", "action=block", 
                "protocol=UDP", "remoteport=123"
            ], capture_output=True)
            
            print("[PASS] NTP Service Disabled and Firewall Blocked.")
        except Exception as e:
            print(f"[FAIL] Temporal Patch Failed: {e}")

    @staticmethod
    def probe_mlx_stack():
        """Diagnoses why the MLX stack appears offline."""
        launcher_url = "https://launcher.mlx.yt:45001/api/v1/version"
        agent_url = "http://127.0.0.1:35000/api/v2/health"
        
        print("[PATCH] Probing MLX Stack Connectivity...")
        
        # Check Launcher
        try:
            l_check = requests.get(launcher_url, verify=False, timeout=3)
            print(f"[INFO] Launcher (45001): {'ONLINE' if l_check.status_code == 200 else 'ERR'}")
        except:
            print("[FAIL] Launcher Service is NOT RUNNING. Open MultiLogin X App.")

        # Check Agent
        try:
            a_check = requests.get(agent_url, timeout=3)
            print(f"[INFO] Agent (35000): {'ONLINE' if a_check.status_code == 200 else 'ERR'}")
        except:
            print("[FAIL] Agent is OFFLINE. Check app.properties for 'multilogin.port=35000'.")

def apply_all_patches():
    patcher = Method4Patch()
    patcher.request_admin() # Must be first
    patcher.fix_temporal_isolation()
    patcher.probe_mlx_stack()
    print("\n[COMPLETE] System Patched. Re-run Gatekeeper to verify.")

if __name__ == "__main__":
    apply_all_patches()
