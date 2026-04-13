import os
import time

LOG_FILE = "system.log"
HEARTBEAT_THRESHOLD = 30  # Seconds of silence before we worry

last_heartbeat = time.time()
stats = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0}

print(f"📡 Monitoring {LOG_FILE}... (Press Ctrl+C to stop)")


def get_file_id(path):
    """Returns the unique Inode of a file."""
    if os.path.exists(path):
        return os.stat(path).st_ino
    return None


# Initial setup
current_ino = get_file_id(LOG_FILE)
f = open(LOG_FILE, "r")
f.seek(0, os.SEEK_END)

try:
    while True:
        # Check for rotation
        new_ino = get_file_id(LOG_FILE)

        # If the file ID changed OR the file size shrank (truncated)
        if new_ino != current_ino or os.path.getsize(LOG_FILE) < f.tell():
            print("\n🔄 [SYSTEM] Log rotation detected! Re-opening file...")
            f.close()
            time.sleep(1)  # Give the OS a second to finish the swap
            f = open(LOG_FILE, "r")
            current_ino = new_ino
            # Note: We do NOT seek to the end here; we want to read the new file from the start.

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
                print(f"\033[93m[!] 🛑 ERROR (Total: {stats['ERROR']}): {line}\033[0m")
            elif "WARNING" in line:
                stats["WARNING"] += 1
                print(
                    f"\033[94m[*] ⚠️ WARNING (Total: {stats['WARNING']}): {line}\033[0m"
                )

        else:
            # No new lines? Check if it's been silent for too long
            silence_duration = current_time - last_heartbeat

            if silence_duration > HEARTBEAT_THRESHOLD:
                print(f"⚠️  ALERT: System has been silent for {int(silence_duration)}s!")
                # In a real job, you'd send an email/Slack alert here

                # Reset slightly so we don't spam the alert every millisecond
                last_heartbeat = current_time

        time.sleep(0.5)

except KeyboardInterrupt:
    f.close()
    # This is the "Executive Summary" for your boss
    print("\n" + "=" * 30)
    print("📊 FINAL SYSTEM HEALTH SUMMARY")
    print("=" * 30)
    print(f"🔴 CRITICAL ERRORS: {stats['CRITICAL']}")
    print(f"🟠 STANDARD ERRORS: {stats['ERROR']}")
    print(f"🟡 SYSTEM WARNINGS: {stats['WARNING']}")
    print("=" * 30)
    print("🛑 Monitoring stopped.")
