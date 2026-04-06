import os
import time

def monitor_logs(file_path):
    print(f"--- 🛡️ MLOps Sentinel: Monitoring {file_path} in real-time ---")
    print("--- (Press Ctrl+C to stop) ---")
    
    if not os.path.exists(file_path):
        print("❌ Error: Log file not found.")
        return

    # Open the file and move to the end so we only see NEW logs
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, os.SEEK_END) 
        
        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                
                line = line.strip() # Clean up the whitespace once

                # Single logic block for all alerts
                if "CRITICAL" in line:
                    print(f"\033[91m[!!] 🔥 CRITICAL ALERT: {line}\033[0m")
                elif "ERROR" in line:
                    print(f"\033[93m[!] 🛑 ERROR DETECTED: {line}\033[0m")
                elif "WARNING" in line:
                    print(f"\033[94m[*] ⚠️ WARNING: {line}\033[0m")
                    
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")

if __name__ == "__main__":
    monitor_logs("system.log")