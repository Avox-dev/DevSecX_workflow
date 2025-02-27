```python
from groq import Groq
import os

def Grok_req(prompt: str, api_key: str) -> str:
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key is None:
        print("Error: GROQ_API_KEY environment variable not set.")
    else:
        output = Grok_req("hello", api_key)
        print("Generated Response:", output)

```
