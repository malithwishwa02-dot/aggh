"""
CHRONOS v3: END-TO-END OPERATIONAL VERIFICATION (SHADOW MISSION)
Objective: Final proof of Method 4 functionality.
This script runs a complete mock mission to verify all core systems.
"""

import os
import sys
import time
import ctypes
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Ensure script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Mock directory for forensic verification
MOCK_MLX_PATH = Path("./shadow_mission_vault/data/profile_test/Default/Network")
MOCK_COOKIES = MOCK_MLX_PATH / "Cookies"

try:
    from core.genesis import shift_kernel_clock, restore_kernel_clock
    from core.isolation import TemporalIsolation
    from modules.behavior import poisson_delay
    from utils.forensics import audit_mft_alignment
except ImportError:
    print("[ERROR] Framework modules missing. Ensure directory structure is intact.")
    sys.exit(1)

class ShadowMission:
    def __init__(self):
        self.isolation = TemporalIsolation()
        self.age_days = 90

    def prepare(self):
        print("\n" + "="*60)
        print("INITIATING SHADOW MISSION: FINAL v3 VERIFICATION")
        print("="*60)
        if MOCK_MLX_PATH.exists():
            shutil.rmtree(MOCK_MLX_PATH.parent.parent.parent)
        MOCK_MLX_PATH.mkdir(parents=True)
        print(f"[1/6] Sandbox Environment Created: {MOCK_MLX_PATH}")

    def run(self):
        try:
            # Step 1: Isolation
            print("[2/6] Engaging Temporal Isolation (NTP Blockade)...")
            self.isolation.engage()

            # Step 2: Genesis
            print(f"[3/6] Executing Kernel Shift (T-{self.age_days} Days)...")
            if not shift_kernel_clock(self.age_days):
                raise RuntimeError("Kernel Shift Denied. Run as Admin.")
            
            shifted_now = datetime.utcnow()
            print(f"      Verified System Time: {shifted_now.strftime('%Y-%m-%d %H:%M:%S')}")

            # Step 3: Forensic Creation
            print("[4/6] Creating Mock Identity Data (Natively Timestamped)...")
            with open(MOCK_COOKIES, "w") as f:
                f.write("SQLITE_IDENTITY_SHADOW_DATA_v3")
            
            # Step 4: Behavioral Test
            print("[5/6] Testing Stochastic Pilot (Poisson Lambda 2.5)...")
            for i in range(2):
                start = time.time()
                poisson_delay()
                print(f"      Burst {i+1} duration: {time.time() - start:.2f}s")

            # Step 5: Audit
            print("[6/6] Running Final Forensic Audit...")
            passed = audit_mft_alignment(MOCK_COOKIES)
            if passed:
                print("\n" + "*"*60)
                print("SHADOW MISSION SUCCESS: SYSTEM IS 100% OPERATIONAL")
                print("METHOD 4 COMPLIANCE VERIFIED")
                print("*"*60)
            else:
                print("\n[!] FORENSIC MISMATCH DETECTED. Check Disk Formatting (NTFS Required).")

        except Exception as e:
            print(f"\n[CRITICAL FAILURE] {e}")
        finally:
            print("\n[CLEANUP] Restoring System Reality...")
            restore_kernel_clock()
            self.isolation.disengage()

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[!] FATAL: Administrator privileges required for Method 4 verification.")
        sys.exit(1)
        
    mission = ShadowMission()
    mission.prepare()
    mission.run()
