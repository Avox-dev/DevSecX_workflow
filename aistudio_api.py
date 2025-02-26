import requests
import os

def gemini_generate_content(prompt: str, api_key: str) -> str:
    """
    Google Gemini API (Gemini-1.5-Flash)를 사용하여 AI 응답 생성.

    Parameters:
        prompt (str): AI에게 전달할 텍스트 프롬프트.
        api_key (str): Google Gemini API 키.

    Returns:
        str: 생성된 AI 응답.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # 응답에서 텍스트 추출
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "❌ 응답 없음")
    
    except requests.exceptions.RequestException as e:
        return f"❌ 요청 오류: {str(e)}"

# 사용 예시
if __name__ == "__main__":
    API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")  # 환경 변수에서 API 키 로드
    prompt = "Explain how AI works"

    response = gemini_generate_content(prompt, API_KEY)
    print("Generated Response:", response)
