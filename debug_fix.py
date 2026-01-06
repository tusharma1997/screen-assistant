
import os
import ssl
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

print("Testing httpx with default settings...")
try:
    with httpx.Client() as client:
        resp = client.get("https://api.openai.com/v1/models")
        print(f"[OK] Default httpx success: {resp.status_code}")
except Exception as e:
    print(f"[FAIL] Default httpx failed: {e}")

print("\nTesting httpx with system SSL context...")
try:
    # Create an SSL context that uses the system's default certificates
    ssl_context = ssl.create_default_context()
    
    # This often loads the system store on Windows (depending on Python version)
    # If not, we might need to load specific locations, but let's try default first.
    
    with httpx.Client(verify=ssl_context) as client:
        resp = client.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"})
        print(f"[OK] System SSL context success: {resp.status_code}")
        
        # Try actual OpenAI client with this http_client
        if api_key:
            print("  Testing OpenAI Client with custom http_client...")
            ai_client = OpenAI(api_key=api_key, http_client=client)
            ai_client.chat.completions.create(
                model="gpt-4o", 
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=5
            )
            print("  [OK] OpenAI Client Integration Success!")

except Exception as e:
    print(f"[FAIL] System SSL context failed: {e}")
    # import traceback; traceback.print_exc()

print("\nTesting httpx with verify=False (Insecure fallback)...")
try:
    with httpx.Client(verify=False) as client:
        resp = client.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"})
        print(f"[OK] Insecure verify=False success: {resp.status_code}")
except Exception as e:
    print(f"[FAIL] Insecure verify=False failed: {e}")
