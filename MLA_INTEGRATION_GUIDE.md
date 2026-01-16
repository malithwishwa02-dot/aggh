# MultiLogin X (MLX) API Configuration Guide

## 1. Overview
Aging-Cookies v3 integrates with MultiLogin X (MLX) via its local and cloud APIs for profile lifecycle control and forensic-grade cookie injection. Correct API configuration is critical for Method 4 compliance.

## 2. MLX API Endpoints
- **Launcher (Cloud Auth):**
  - URL: `https://launcher.mlx.yt:45001/api/v1`
  - Used for authentication and token retrieval.
- **Agent (Local Control):**
  - URL: `http://127.0.0.1:35000/api/v2`
  - Used for starting/stopping profiles and direct file operations.

## 3. Authentication
- Obtain a Bearer Token from the Launcher endpoint using your MLX credentials.
- Example (Python):
  ```python
  import requests
  resp = requests.post('https://launcher.mlx.yt:45001/api/v1/auth/login', json={"username": "YOUR_USER", "password": "YOUR_PASS"}, verify=False)
  token = resp.json()["token"]
  headers = {"Authorization": f"Bearer {token}"}
  ```

## 4. Local Agent API Usage
- All profile operations (start, stop, health check) use the local agent endpoint.
- Example: Start a profile
  ```python
  import requests
  profile_id = "your-profile-id"
  resp = requests.post('http://127.0.0.1:35000/api/v2/profile/start', json={"profileId": profile_id})
  ```
- **Never use** `/profile/cookies/import` for Method 4. Always inject cookies via direct file overwrite.

## 5. Configuration File (app.properties)
- Ensure the following in your MLX `app.properties`:
  ```
  multilogin.port=35000
  multilogin.api.enabled=true
  multilogin.api.allowLocalhost=true
  multilogin.api.allowRemote=false
  ```
- Restart MLX after editing `app.properties`.

## 6. Troubleshooting
- If the agent API is unreachable, verify:
  - MLX is running and not blocked by firewall.
  - The port (35000) is open and matches your config.
  - `app.properties` is correctly set.
- Use the Gatekeeper script to probe API health before every mission.

## 7. References
- [MLX API Postman Documentation](https://documenter.getpostman.com/view/28533318/2s946h9Cv9)
- [Aging-Cookies v3 USER_GUIDE.md](../USER_GUIDE.md)

---
**For Method 4, always use physical file injection and never the MLX cookie import API.**
