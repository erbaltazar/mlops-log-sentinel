import os

def analyze_logs(file_path):
    # This line must be indented (4 spaces)
    print(f"--- 🛡️ Starting MLOps Log Analysis on {file_path} ---")
    
    if not os.path.exists(file_path):
        print("❌ Error: Log file not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    # Filtering for Critical and Error tags
    anomalies = [line.strip() for line in logs if "ERROR" in line or "CRITICAL" in line]
    
    if anomalies:
        print(f"🔥 Found {len(anomalies)} anomalies that require attention:")
        for a in anomalies:
            print(f"  >> {a}")
    else:
        print("✅ System Healthy: No critical errors found.")

# This part MUST be at the very edge (no spaces)
if __name__ == "__main__":
    analyze_logs("system.log")