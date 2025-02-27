```python
import requests
import os
from google.auth.transport import requests as google_requests
from google.oauth2 import service_account

def gemini_generate_content(prompt: str, service_account_path: str) -> str:
    credentials = service_account.Credentials.from_service_account_file(service_account_path)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    request = google_requests.Request()
    authorized_request = scoped_credentials.authorize(request)

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = authorized_request.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "❌ 응답 없음")
    except requests.exceptions.RequestException as e:
        return f"❌ 요청 오류: {str(e)}"

if __name__ == "__main__":
    SERVICE_ACCOUNT_PATH = os.getenv("GEMINI_SERVICE_ACCOUNT_PATH")
    prompt = "Explain how AI works"

    if SERVICE_ACCOUNT_PATH:
        response = gemini_generate_content(prompt, SERVICE_ACCOUNT_PATH)
        print("Generated Response:", response)
    else:
        print("❌ GEMINI_SERVICE_ACCOUNT_PATH 환경 변수가 설정되지 않았습니다.")

```
