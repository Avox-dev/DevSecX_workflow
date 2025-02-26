#!/usr/bin/env python3
import os
import requests
from Grok_api import Grok_req
from bandit_result import run_bandit_cli
import argparse

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
    for file in source_files_list:
        print(file)
    for file_path in source_files_list:
        try:
            # Bandit 스캔 실행 (run_bandit_cli 함수가 파일 경로를 인자로 받고 결과 문자열 반환)
            scan_result = run_bandit_cli(file_path)
            promft=scan_result+'''요약 json파일로 줘
            '''
            LLM_res=Grok_req(promft,args.api_key)
        except Exception as e:
            print(f"{file_path} 스캔 중 오류 발생: {e}")
        # 결과 파일 저장 경로 설정
        output_path = "response.json"
        with open(os.path.abspath(output_path), "a", encoding="utf-8") as outfile:
            outfile.write(LLM_res + "\n")

        # 기존 코드 개선
        with open(file_path, "r", encoding="utf-8") as code:
            prompt = code.read() + "\n취약점 대체코드만줘 코드블럭금지\n"

        LLM_code_res = Grok_req(prompt, args.api_key)

        # 수정된 코드 저장
        save_fixed_code(file_path, LLM_code_res)

    print(f"스캔결과 {os.path.abspath(output_path)}에 저장되었습니다.")
                
    

if __name__ == "__main__":
    main()
