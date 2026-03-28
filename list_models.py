from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("GEMINI_API_KEY が設定されていません")
    exit(1)

client = genai.Client(api_key=api_key)
for m in client.models.list():
    if "generateContent" in (m.supported_actions or []):
        print(m.name)
