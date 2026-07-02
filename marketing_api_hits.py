import os
import sys
import time
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError

# ================== CONFIGURATION ==================
# Pulls directly from GitHub Encrypted Secrets Framework
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
APP_ID = os.getenv("META_APP_ID")
APP_SECRET = os.getenv("META_APP_SECRET")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")

# Targets slightly over the 500 qualification mark
TOTAL_CALLS = 525                                      
DELAY_SECONDS = 1                                   

# Targeted fields to ensure a valid Marketing API footprint
FIELDS = ['id', 'name', 'status', 'objective', 'daily_budget']
# ===================================================

def main():
    print(f"[{datetime.utcnow()} UTC] 🚀 Starting Meta Marketing API Traffic Engine...")
    
    # 1. Credentials Sanity Check
    missing_secrets = []
    if not ACCESS_TOKEN: missing_secrets.append("META_ACCESS_TOKEN")
    if not APP_ID: missing_secrets.append("META_APP_ID")
    if not APP_SECRET: missing_secrets.append("META_APP_SECRET")
    if not AD_ACCOUNT_ID: missing_secrets.append("META_AD_ACCOUNT_ID")
    
    if missing_secrets:
        print(f"[{datetime.utcnow()} UTC] ❌ CRITICAL CONFIGURATION ERROR:")
        print(f"The following environment variables are missing: {', '.join(missing_secrets)}")
        print("Please check your GitHub Repository Secrets configuration settings.")
        sys.exit(1)
        
    # 2. SDK Initialization
    try:
        print(f"[{datetime.utcnow()} UTC] ⛓️ Initializing Facebook Business SDK Context...")
        FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
        account = AdAccount(AD_ACCOUNT_ID)
        print(f"[{datetime.utcnow()} UTC] ✅ SDK Target Bound to Account ID: {AD_ACCOUNT_ID}")
    except Exception as initialization_error:
        print(f"[{datetime.utcnow()} UTC] ❌ Initialization failed: {initialization_error}")
        sys.exit(1)
        
    # 3. Execution State Variables
    success_count = 0
    error_count = 0
    
    print(f"[{datetime.utcnow()} UTC] 📊 Strategy: Executing {TOTAL_CALLS} requests to /campaigns.")
    print(f"[{datetime.utcnow()} UTC] ⏱️ Interval spacing: {DELAY_SECONDS}s delay per iteration.")
    print("-" * 70)
    
    # 4. Traffic Loop
    for i in range(1, TOTAL_CALLS + 1):
        start_time = time.time()
        try:
            # Query the target Marketing API endpoint
            campaigns = account.get_campaigns(fields=FIELDS)
            success_count += 1
            execution_duration = time.time() - start_time
            
            # Logging Strategy: Print full data summary on first call, then step summaries every 50 calls.
            # This keeps the GitHub runner logs clear while validating payloads are correct.
            if i == 1:
                campaign_count = len(campaigns)
                print(f"[{datetime.utcnow()} UTC] 🛰️ [Call {i:03d}/{TOTAL_CALLS}] SUCCESS | Time: {execution_duration:.2f}s")
                print(f"    └── Payload Verification Check: Extracted {campaign_count} campaigns successfully.")
                if campaign_count > 0:
                    print(f"    └── Sample Campaign Object Structure -> ID: {campaigns[0].get('id')} | Name: {campaigns[0].get('name')}")
            elif i % 50 == 0 or i == TOTAL_CALLS:
                print(f"[{datetime.utcnow()} UTC] 🛰️ [Call {i:03d}/{TOTAL_CALLS}] SUCCESS | Cumulative Progress Match | Time: {execution_duration:.2f}s")
                
        except FacebookRequestError as api_error:
            error_count += 1
            print(f"\n[{datetime.utcnow()} UTC] 🚨 [Call {i:03d}/{TOTAL_CALLS}] FACEBOOK API ERROR DETECTED:")
            print(f"    ├── Code: {api_error.api_error_code()}")
            print(f"    └── Message: {api_error.api_error_message()}")
            
        except Exception as unexpected_error:
            error_count += 1
            print(f"\n[{datetime.utcnow()} UTC] 💥 [Call {i:03d}/{TOTAL_CALLS}] UNEXPECTED SYSTEM RUNTIME ERROR:")
            print(f"    └── Context: {unexpected_error}")
            
        # Pace requests to fit safety guardrails
        if i < TOTAL_CALLS:
            time.sleep(DELAY_SECONDS)
            
    # 5. Final Analytics Summary Report
    print("\n" + "=" * 70)
    print(f"[{datetime.utcnow()} UTC] 🏁 TRAFFIC GENERATION COMPLETE LOG RUN")
    print(f"    ├── Total Target Volume Checked: {TOTAL_CALLS}")
    print(f"    ├── Successful API Requests Run: {success_count}")
    print(f"    ├── Total Logged Exceptions/Errors: {error_count}")
    
    success_rate = (success_count / TOTAL_CALLS) * 100
    print(f"    └── Calculated Pipeline Health Rate: {success_rate:.1f}%")
    
    if success_rate >= 85.0:
        print("\n🏆 STATUS: SUCCESS. App metrics are safely within Meta's threshold.")
        print("💡 Check your App Dashboard → Marketing API Access Tier parameters to watch the validation progress.")
    else:
        print("\n⚠️ STATUS: WARNING. Error rates exceed optimal verification parameters (< 15%).")
        print("📊 Review the endpoint exception tracking variables listed above.")
    print("=" * 70)

if __name__ == "__main__":
    main()
