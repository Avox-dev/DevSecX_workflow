#!/usr/bin/env python3
import os
import requests

def scan_source_code():
    """현재 디렉토리 이하의 모든 .py 파일을 읽어 하나의 문자열로 결합."""
    code_snippets = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        code_snippets.append(f"File: {file_path}\n{content}\n")
                except Exception as e:
                    print(f"파일 {file_path} 읽기 실패: {e}")
    return "\n".join(code_snippets)

def main():

    # 소스코드 스캔
    payload = scan_source_code()
    
    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(payload)
    print("소스코드가가 response.txt에 저장되었습니다.")

if __name__ == "__main__":
    main()
