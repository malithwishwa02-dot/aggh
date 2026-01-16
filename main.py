import os
import ctypes
import sys

# Ensure script is run from its own directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from core.genesis import TemporalShift
from core.bridge import direct_injection
from core.isolation import disable_w32time, block_udp_123, restore_w32time
from modules.behavior import PoissonSleep, HumanMouse
from modules.trust import TrustPilot

import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        print("Admin rights required.")
        sys.exit(1)
    disable_w32time()
    block_udp_123()
    with TemporalShift(days=90):
        # DirectInjection Bridge (stub args)
        direct_injection('profile_id', 'chronos_db_path', 'profile_path')
        # BehavioralPilot
        pilot = TrustPilot()
        pilot.enforce_sequence()
        # Silence Window
        print("Silence window: 180s")
        time.sleep(180)
        input("Press Enter to terminate and restore system clock...")
    restore_w32time()
    print("System clock and NTP restored.")

if __name__ == "__main__":
    main()
