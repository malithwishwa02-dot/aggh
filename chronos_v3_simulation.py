"""
CHRONOS v3: METHOD 4 SIMULATION ORCHESTRATOR
Objective: Test Kernel Shift & Forensic Sync WITHOUT MLX
Logic: Mock MLX Directory -> Shift Clock -> Inject Mock Data -> Verify
"""

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Ensure script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Import Core v3 Modules (Assumes directory structure is correct)
try:
    from core.genesis import shift_kernel_clock, restore_kernel_clock
    from core.isolation import TemporalIsolation
    from modules.behavior import poisson_delay
    from utils.forensics import audit_mft_alignment
except ImportError:
    print("[ERROR] Core modules not found. Ensure you are in the Aging-cookies-v3 root.")
    sys.exit(1)

# --- [1. SIMULATION SETTINGS] ---
MOCK_PROFILE_DIR = Path("./mock_mlx_profile/Default/Network")
MOCK_COOKIE_FILE = MOCK_PROFILE_DIR / "Cookies"
TEST_AGE_DAYS = 90

class ChronosSimulator:
    def __init__(self):
        self.isolation = TemporalIsolation()
        print("=== CHRONOS v3: METHOD 4 SIMULATION INITIATED ===")

    def setup_mock_environment(self):
        """Creates a fake MLX folder structure for testing."""
        if MOCK_PROFILE_DIR.exists():
            shutil.rmtree(MOCK_PROFILE_DIR.parent.parent)
        MOCK_PROFILE_DIR.mkdir(parents=True)
        # Create a dummy sqlite-like file
        with open(MOCK_COOKIE_FILE, "w") as f:
            f.write("MOCK_SQLITE_HEADER_DATA_V3")
        print(f"[SIM] Mock Profile Created at: {MOCK_PROFILE_DIR}")

    def run_simulation(self):
        try:
            # PHASE 1: Isolation
            print("[SIM] Engaging Temporal Isolation...")
            self.isolation.engage()
            
            # PHASE 2: Genesis (Shift Clock)
            print(f"[SIM] Shifting Kernel Clock back {TEST_AGE_DAYS} days...")
            if shift_kernel_clock(TEST_AGE_DAYS):
                shifted_time = datetime.utcnow()
                print(f"[VERIFY] Current OS Time (Shifted): {shifted_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print("[FAIL] Kernel Shift Failed. Run as Admin.")
                return

            # PHASE 3: Forensic Injection Simulation
            print("[SIM] Simulating Direct Injection & Metadata Polish...")
            # We touch a file while the clock is shifted
            MOCK_COOKIE_FILE.touch()
            past_ts = (datetime.now() - timedelta(days=TEST_AGE_DAYS)).timestamp()
            os.utime(MOCK_COOKIE_FILE, (past_ts, past_ts))
            
            # PHASE 4: Behavioral Simulation
            print("[SIM] Running 3 Poisson Delay Cycles (Human Emulation)...")
            for i in range(3):
                start = time.time()
                poisson_delay(lambda_val=2.5)
                end = time.time()
                print(f"  > Cycle {i+1}: Slept for {end-start:.2f}s")

            # PHASE 5: Forensic Audit
            print("[SIM] Auditing Forensic Alignment (MFT SI/FN)...")
            # In a real run, we'd check against the shifted clock
            is_aligned = audit_mft_alignment(MOCK_COOKIE_FILE)
            print(f"[RESULT] Forensic Alignment: {'PASSED' if is_aligned else 'FAILED'}")

        finally:
            # PHASE 6: Restore
            print("[SIM] Restoring System State...")
            restore_kernel_clock()
            self.isolation.disengage()
            print("=== SIMULATION COMPLETE ===")

if __name__ == "__main__":
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[CRITICAL] Simulation must be run as Administrator to shift Kernel clock.")
        sys.exit(1)
        
    sim = ChronosSimulator()
    sim.setup_mock_environment()
    sim.run_simulation()
