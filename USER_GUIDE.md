# Aging-Cookies v3: Operational Hardening Guide

## 1. Pre-Mission Checklist
- **Run as Administrator:** Always launch all scripts with elevated privileges.
- **Verify Python Environment:** Use Python 3.11+ with all dependencies installed.
- **Run Gatekeeper:** Execute `chronos_v3_gatekeeper.py` before every session. Scrub mission if any check fails.
- **MLX Services:** Ensure MultiLogin X Launcher and Agent are running and reachable.
- **NTP Isolation:** Confirm Windows Time service is stopped and UDP 123 is blocked.

## 2. Secure Execution Protocols
- **Network Lock:** Use `core/network_lock.py` to instantly sever network if proxy drops.
- **Forensic Monitoring:** Enable `utils/forensics.py` to continuously audit NTFS MFT attributes during the session.
- **Session Logging:** Store logs in an encrypted volume. Use `utils/encryption.py` for at-rest protection.
- **Manual Handover:** Always pause automation at the target site for a 180s silence window before human interaction.

## 3. Post-Mission Cleanup
- **Clock Restore:** Use `core/cleanup.py` to restore system time and re-enable NTP.
- **Data Sanitization:** Securely wipe `isolation_state.json` and any temp files using DoD 3-pass overwrite.
- **Log Review:** Audit all logs for anomalies or unexpected events.

## 4. User Guide: Step-by-Step

### Initial Setup
1. Install Python 3.11+ and all dependencies: `pip install -r requirements.txt`
2. Configure MLX and trust sequence in `config/`.

### Running a Mission
1. Open terminal as Administrator.
2. Run: `python chronos_v3_gatekeeper.py` and confirm all [PASS].
3. Start MLX Launcher and Agent.
4. Run: `python main.py` to begin the synthetic identity aging pipeline.
5. Wait for the silence window at the target site, then take manual control.

### After the Mission
1. Run: `python core/cleanup.py` to restore system state.
2. Review logs and wipe sensitive data.

## 5. Best Practices
- Never skip the gatekeeper audit.
- Never run on a system with active NTP or time sync enabled.
- Always use encrypted storage for logs and temp data.
- Regularly update dependencies and review code for new detection vectors.

---

**For advanced OpSec, consider running inside a dedicated VM with snapshot/rollback capability.**
