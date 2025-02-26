#!/usr/bin/env python3
import os,json
import requests
from Grok_api import Grok_req
from bandit_result import run_bandit_cli
import argparse
from aistudio_api import gemini_generate_content 

import os

def get_source_files(root_dir, extensions=(".py", ".js", ".java", ".cpp", ".c", ".h")):
    """
    주어진 루트 디렉토리 내에서 지정된 확장자를 가진 모든 소스 파일의 경로를 리스트로 반환합니다.
    단, 'devsecx_workflow' 폴더 및 그 하위 폴더들은 제외합니다.
    
    Parameters:
        root_dir (str): 소스 파일 검색을 시작할 루트 디렉토리 경로.
        extensions (tuple): 검색할 파일 확장자들의 튜플.
    
    Returns:
        list: 해당 확장자를 가진 파일들의 전체 경로 목록.
    """
    source_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # devsecx_workflow 폴더 및 모든 하위 폴더 제외
        if "devsecx_workflow" in dirpath:
            continue  # 탐색에서 제외
        if "new" in dirpath:
            continue  # 탐색에서 제외
        
        for filename in filenames:
            if filename.endswith(extensions):
                source_files.append(os.path.join(dirpath, filename))
    
    return source_files



def save_fixed_code(file_path, LLM_code_res):
    """
    LLM에서 생성한 코드 수정본을 원본 파일명에 'new'를 붙여 'new' 폴더 내에 저장하는 함수.
    
    Parameters:
        file_path (str): 원본 코드 파일 경로.
        LLM_code_res (str): LLM에서 반환된 코드 수정본.
    
    Returns:
        str: 새롭게 저장된 파일의 경로.
    """
    # 'new' 폴더 생성 (존재하지 않으면)
    new_folder = os.path.join(os.path.dirname(file_path), "new")
    os.makedirs(new_folder, exist_ok=True)

    # 새 파일명 설정 (기존 파일명에 'new' 추가)
    original_filename = os.path.basename(file_path)  # 예: main.py
    new_filename = f"new_{original_filename}"  # 예: new_main.py
    new_file_path = os.path.join(new_folder, new_filename)

    # 수정된 코드 저장
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        new_file.write(LLM_code_res)

    print(f"✅ Fixed code saved to: {new_file_path}")
    return new_file_path



def main():
    parser = argparse.ArgumentParser(description="LLM API 요청 스크립트")
    parser.add_argument("--api-key", required=True, help="LLM API 키")
    args = parser.parse_args()

    # 현재 GitHub Actions에서 실행 중인 리포지토리 경로 가져오기
    repo_path = os.getenv("GITHUB_WORKSPACE", os.getcwd())
    source_files_list=get_source_files(repo_path)
    print(f"🔍 Scanning source files in: {repo_path}")
    print("📂 탐색된 소스 파일 목록:")


        # 전체 결과를 저장할 리스트
    all_results = []

    for file_path in source_files_list:
        try:
            # Bandit 스캔 실행
            scan_result = run_bandit_cli(file_path)

            # LLM 요청 (Gemini 또는 Groq 사용 가능)
            prompt = scan_result + """
위 보안 스캔 결과를 바탕으로 다음 항목들을 포함하는 JSON 한글번역 요약 보고서를 작성해줘:
{
    "file": "<파일 경로>",
    "issues": [
        {
            "id": "<취약점 ID>",
            "description": "<취약점 설명>",
            "severity": "<심각도>",
            "reliability": "<신뢰도>",
            "recommendation": "<보안 권고사항>"
            "CWE": "<cwe>"
        },
        ...
    ]
}
"""
            LLM_res = gemini_generate_content(prompt, args.api_key)  # 또는 Grok_req(prompt, args.api_key)

            # 결과 저장 (리스트에 추가)
            all_results.append({
                "file": file_path,
                "llm_response": LLM_res
            })

        except Exception as e:
            print(f"{file_path} 스캔 중 오류 발생: {e}")

        # 기존 코드 개선 (취약점 대체 코드 요청)
        with open(file_path, "r", encoding="utf-8") as code:
            prompt = code.read() + prompt = code.read() + """
위 코드를 분석하여 보안 취약점을 개선한 수정 코드를 생성해줘.
- 주석은 포함하지 말고, 순수 코드만 제공해줘.
- 수정 전후의 차이점을 명확히 반영해줘.
"""
            LLM_code_res = gemini_generate_content(prompt, args.api_key)  # 또는 Grok_req(prompt, args.api_key)

        # 수정된 코드 저장
        save_fixed_code(file_path, LLM_code_res)

    # ✅ JSON 파일을 `for` 루프 종료 후 한 번만 저장
    output_path = "response.json"
    with open(os.path.abspath(output_path), "w", encoding="utf-8") as outfile:
        json.dump(all_results, outfile, ensure_ascii=False, indent=4)

    print(f"스캔결과 {os.path.abspath(output_path)}에 저장되었습니다.")
                
    

if __name__ == "__main__":
    main()
