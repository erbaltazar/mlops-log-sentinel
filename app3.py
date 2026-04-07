import os
import time

def monitor_logs(file_path):
    # This dictionary keeps track of our "System Health" in memory
    stats = {"CRITICAL": 0, "ERROR": 0, "WARNING": 0}
    
    print(f"--- 🛡️ MLOps Sentinel: Monitoring {file_path} ---")
    print("--- (Press Ctrl+C to stop and see summary) ---")
    
    if not os.path.exists(file_path):
        print("❌ Error: Log file not found.")
        return

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, os.SEEK_END) 
        
        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                
                line = line.strip()

                # Logic to catch anomalies and increment our counters
                if "CRITICAL" in line:
                    stats["CRITICAL"] += 1
                    print(f"\033[91m[!!] 🔥 CRITICAL (Total: {stats['CRITICAL']}): {line}\033[0m")
                elif "ERROR" in line:
                    stats["ERROR"] += 1
                    print(f"\033[93m[!] 🛑 ERROR (Total: {stats['ERROR']}): {line}\033[0m")
                elif "WARNING" in line:
                    stats["WARNING"] += 1
                    print(f"\033[94m[*] ⚠️ WARNING (Total: {stats['WARNING']}): {line}\033[0m")
                    
        except KeyboardInterrupt:
            # This is the "Executive Summary" for your boss
            print("\n" + "="*30)
            print("📊 FINAL SYSTEM HEALTH SUMMARY")
            print("="*30)
            print(f"🔴 CRITICAL ERRORS: {stats['CRITICAL']}")
            print(f"🟠 STANDARD ERRORS: {stats['ERROR']}")
            print(f"🟡 SYSTEM WARNINGS: {stats['WARNING']}")
            print("="*30)
            print("🛑 Monitoring stopped.")

if __name__ == "__main__":
    monitor_logs("system.log")