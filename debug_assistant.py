
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

print("Starting diagnostics...")

# 1. Test .env loading
try:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment.")
    else:
        # Mask the key for security in logs, show first/last few chars
        masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        print(f"[OK] Found API Key: {masked_key}")
        
        # Check for whitespace issues
        if api_key.strip() != api_key:
             print("[WARNING] API Key has leading/trailing whitespace!")
except Exception as e:
    print(f"[ERROR] Error loading .env: {e}")

# 2. Test OpenAI API connection
if api_key:
    try:
        print("Testing OpenAI API connection...")
        client = OpenAI(api_key=api_key.strip())
        
        # Simple test model call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Hello, is this working?"}
            ],
            max_tokens=10
        )
        print("[OK] API Call Successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"[ERROR] API Call Failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

print("\n3. Testing Basic Connectivity...")
import urllib.request
try:
    urllib.request.urlopen("https://www.google.com", timeout=5)
    print("[OK] Google is reachable.")
except Exception as e:
    print(f"[ERROR] Google is NOT reachable: {e}")

print("\n4. Proxy Environment Variables:")
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    print(f"  {key}: {os.environ.get(key, 'Not Set')}")
    
print("\nDiagnostics complete.")
