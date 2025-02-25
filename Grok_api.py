from groq import Groq
import os

def Grok_req(prompt: str) -> str:

    client = Groq(api_key=os.getenv("Groq_API_KEY"))
    completion = client.chat.completions.create(
        model="llama-3.3-70b-specdec",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    return result

# 사용 예시
if __name__ == "__main__":
    output = Grok_req("hello")
    print("Generated Response:", output)
