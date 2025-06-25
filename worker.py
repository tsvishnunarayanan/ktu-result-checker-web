import time
from bot import run_checker

if __name__ == "__main__":
    while True:
        try:
            print("\n🟢 Starting result check cycle...")
            run_checker()
            print("✅ Cycle complete. Waiting 5 minutes before next check...")
            time.sleep(300)  # 5 minutes
        except Exception as e:
            print(f"🔥 Error in worker loop: {e}\nRetrying in 2 minutes...")
            time.sleep(120)
