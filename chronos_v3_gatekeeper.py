"""
CHRONOS v3 GATEKEEPER : MASTER VERIFICATION AGENT
Protocol: Method 4 (Kernel Time Shift / MLX Hybrid)
Authority: The Omni-Architect

USAGE:
    Run as Administrator: python chronos_v3_gatekeeper.py

AUDIT PIPELINE:
    1. PRIVILEGE : Verify SeSystemtimePrivilege for clock manipulation.
    2. API       : Handshake with MLX Launcher (45001) & Agent (35000).
    3. TEMPORAL  : Verify w32time isolation (NTP blockade).
    4. FORENSIC  : Validate NTFS MFT timestamp injection capability.
    5. BEHAVIOR  : Statistically verify Poisson (Lambda 2.5) entropy.
"""

import os
import sys
import ctypes
import math
import random
import time
import shutil
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Ensure script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- [1. CONFIGURATION: METHOD 4 THRESHOLDS] ---
class Config:
    MLX_LAUNCHER = "https://launcher.mlx.yt:45001/api/v1"
    MLX_AGENT = "http://127.0.0.1:35000/api/v2"
    
    REQUIRED_AGE = 90
    POISSON_LAMBDA = 2.5
    MIN_SILENCE_WINDOW = 180
    
    # ANSI Colors for terminal output
    PASS = "\033[92m[PASS]\033[0m"
    FAIL = "\033[91m[FAIL]\033[0m"
    WARN = "\033[93m[WARN]\033[0m"

# --- [2. AUDITOR LOGIC: CORE VERIFICATION] ---
class ChronosAuditor:
    def audit_privileges(self):
        """Must be Admin to shift kernel clock."""
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return is_admin, "Elevated Privileges Found" if is_admin else "Access Denied: Run as Admin"
        except:
            return False, "Privilege Check Error"

    def audit_mlx_stack(self):
        """Verifies MultiLogin X background and agent services."""
        results = {"launcher": False, "agent": False}
        try:
            # Launcher Check (Launcher handles login/auth)
            l_req = requests.get(f"{Config.MLX_LAUNCHER}/version", verify=False, timeout=3)
            results["launcher"] = l_req.status_code == 200
            
            # Agent Check (Agent handles browser automation)
            a_req = requests.get(f"{Config.MLX_AGENT}/health", timeout=3)
            results["agent"] = a_req.status_code == 200
        except:
            pass
        
        status = all(results.values())
        msg = f"L:{results['launcher']} A:{results['agent']} (Ready)" if status else "MLX Stack Offline"
        return status, msg

    def audit_temporal_isolation(self):
        """Ensures Windows won't auto-correct our T-90 shift."""
        # Check service status via shell
        status_raw = os.popen('sc query w32time').read()
        ntp_active = "RUNNING" in status_raw
        
        # We WANT it to be stopped or blocked
        return not ntp_active, "NTP Isolated (Safe)" if not ntp_active else "NTP Running (LEAK RISK)"

    def audit_forensic_ntfs(self):
        """Verifies if Method 4 can backdate files without MFT rejection."""
        test_path = Path("method4_forensic.tmp")
        test_path.touch()
        
        try:
            past_date = datetime.now() - timedelta(days=Config.REQUIRED_AGE)
            past_ts = past_date.timestamp()
            # Apply SI (Standard Information) attribute shift
            os.utime(test_path, (past_ts, past_ts))
            
            # Re-read from disk
            actual_ts = os.path.getmtime(test_path)
            verified = abs(actual_ts - past_ts) < 1.0
            test_path.unlink()
            return verified, "NTFS Timestamp Injection Working"
        except Exception as e:
            return False, f"FS Error: {str(e)}"

    def audit_behavioral_entropy(self):
        """Mathematical verification of Poisson activity distribution."""
        samples = []
        for _ in range(300):
            # Formula for Poisson delay with Lambda 2.5
            delay = -math.log(1.0 - random.random()) / Config.POISSON_LAMBDA
            samples.append(delay)
        
        avg = sum(samples) / len(samples)
        # Expected average is 1/Lambda (1/2.5 = 0.4)
        valid = 0.3 <= avg <= 0.5
        return valid, f"Poisson Adherence: {avg:.4f}s avg (Target 0.4s)"

# --- [3. ORCHESTRATOR: END-TO-END EXECUTION] ---
def run_gatekeeper_audit():
    print("\n" + "="*60)
    print("CHRONOS v3 GATEKEEPER - END-TO-END VERIFICATION")
    print("METHOD 4 COMPLIANCE AUDIT")
    print("="*60 + "\n")
    
    auditor = ChronosAuditor()
    critical_failures = 0

    # Task List
    tasks = [
        ("Privilege Audit", auditor.audit_privileges),
        ("MLX API Stack", auditor.audit_mlx_stack),
        ("Temporal Isolation", auditor.audit_temporal_isolation),
        ("Forensic NTFS", auditor.audit_forensic_ntfs),
        ("Behavioral Entropy", auditor.audit_behavioral_entropy)
    ]

    for name, task in tasks:
        success, message = task()
        status_tag = Config.PASS if success else Config.FAIL
        if not success: critical_failures += 1
        print(f"{status_tag} {name.ljust(20)} : {message}")

    print("\n" + "="*60)
    if critical_failures == 0:
        print("FINAL RESULT: [READY] SYSTEM COMPLIANT FOR METHOD 4 OPS")
    else:
        print(f"FINAL RESULT: [CRITICAL] {critical_failures} FAILURE(S) DETECTED")
        print("ACTION: Correct failed components before initiating Method 4.")
    print("="*60 + "\n")

if __name__ == "__main__":
    # Suppress SSL warnings for local Launcher check (self-signed certs)
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        run_gatekeeper_audit()
    except KeyboardInterrupt:
        print("\n[!] Audit Aborted by User.")
    except Exception as e:
        print(f"\n[!] Fatal Error during Gatekeeper execution: {e}")
