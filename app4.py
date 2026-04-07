import time
import os

# Configuration
LOG_FILE = "system.log"
HEARTBEAT_THRESHOLD = 30  # Seconds of silence before we worry

last_heartbeat = time.time()
stats = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0}

print(f"📡 Monitoring {LOG_FILE}... (Press Ctrl+C to stop)")

with open(LOG_FILE, "r") as f:
    f.seek(0, os.SEEK_END)  # Start at the end
    try:
        while True:
            line = f.readline()
            current_time = time.time()

            if line:
                # We found a log! Reset the heartbeat timer
                last_heartbeat = current_time
                print(f"✅ Activity detected: {line.strip()}")
                line = line.strip()

                # Logic to catch anomalies and increment our counters
                if "CRITICAL" in line:
                    stats["CRITICAL"] += 1
                    print(
                        f"\033[91m[!!] 🔥 CRITICAL (Total: {stats['CRITICAL']}): {line}\033[0m"
                    )
                elif "ERROR" in line:
                    stats["ERROR"] += 1
                    print(
                        f"\033[93m[!] 🛑 ERROR (Total: {stats['ERROR']}): {line}\033[0m"
                    )
                elif "WARNING" in line:
                    stats["WARNING"] += 1
                    print(
                        f"\033[94m[*] ⚠️ WARNING (Total: {stats['WARNING']}): {line}\033[0m"
                    )
                # (Your existing 'if ERROR in line' logic goes here)

            else:
                # No new lines? Check if it's been silent for too long
                silence_duration = current_time - last_heartbeat

                if silence_duration > HEARTBEAT_THRESHOLD:
                    print(
                        f"⚠️  ALERT: System has been silent for {int(silence_duration)}s!"
                    )
                    # In a real job, you'd send an email/Slack alert here

                    # Reset slightly so we don't spam the alert every millisecond
                    last_heartbeat = current_time

            time.sleep(1)  # Wait for 1 second before checking again
    except KeyboardInterrupt:
        # This is the "Executive Summary" for your boss
        print("\n" + "=" * 30)
        print("📊 FINAL SYSTEM HEALTH SUMMARY")
        print("=" * 30)
        print(f"🔴 CRITICAL ERRORS: {stats['CRITICAL']}")
        print(f"🟠 STANDARD ERRORS: {stats['ERROR']}")
        print(f"🟡 SYSTEM WARNINGS: {stats['WARNING']}")
        print("=" * 30)
        print("🛑 Monitoring stopped.")
