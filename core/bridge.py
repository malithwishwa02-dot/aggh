import os
import shutil
import requests
import time

def direct_injection(profile_id, chronos_db_path, profile_path):
    # Start profile via MLX API
    requests.post('http://127.0.0.1:35000/api/v2/profile/start', json={"profileId": profile_id})
    # Kill MLX process (user must implement process kill logic)
    # shutil.copy Chronos DB to profile path
    shutil.copy2(chronos_db_path, profile_path)
    # Backdate file timestamps
    now = time.time() - 90*24*3600
    os.utime(profile_path, (now, now))
    # Start profile again
    requests.post('http://127.0.0.1:35000/api/v2/profile/start', json={"profileId": profile_id})
