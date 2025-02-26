#!/usr/bin/env python3
import os
import requests
from Grok_api import Grok_req
from bandit_result import run_bandit_cli
import argparse

def get_source_files(root_dir, extensions=(".py", ".js", ".java", ".cpp", ".c", ".h")):
    """
    주어진 루트 디렉토리 내에서 지정된 확장자를 가진 모든 소스 파일의 경로를 리스트로 반환합니다.
    
    Parameters:
        root_dir (str): 소스 파일 검색을 시작할 루트 디렉토리 경로.
        extensions (tuple): 검색할 파일 확장자들의 튜플. 기본값은 (".py", ".js", ".java", ".cpp", ".c", ".h") 입니다.
    
    Returns:
        list: 해당 확장자를 가진 파일들의 전체 경로 목록.
    """
    source_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extensions):
                source_files.append(os.path.join(dirpath, filename))
    return source_files



def main():
    parser = argparse.ArgumentParser(description="LLM API 요청 스크립트")
    parser.add_argument("--api-key", required=True, help="LLM API 키")
    args = parser.parse_args()

    source_files_list=get_source_files('../DevSecX')
    
    for file_path in source_files_list:
        try:
            # Bandit 스캔 실행 (run_bandit_cli 함수가 파일 경로를 인자로 받고 결과 문자열 반환)
            scan_result = run_bandit_cli(file_path)
            promft=scan_result+'''
            위 결과를 보고 밑에 조건대로 명심하고 응답하세요
            1.한국어로 답변할것
            2.아래 주어진 양식대로 작성할것
            [Example report form].

            1. Overview.  
            - Scan run date and time and target file information:  
            - Summary of the overall scan results (e.g., total number of issues detected, severity distribution, etc.):

            2. Detailed vulnerability analysis  
            - Vulnerability ID: Example) B307  
            - Vulnerability Description:  
            - Issues and security concerns related to the use of dangerous functions (e.g., eval).  
            - Severity and confidence level: e.g.) Medium, High  
            - Related CWE: CWE-78 (OS Instruction Injection)  
            - Found in: File path and code line number  
            - References: Links to related documentation

            3. Impact Analysis and Risk Assessment  
            - The impact of the vulnerability on the system or application:  
            - Security risk assessment and prioritization:

            4. Recommendations and remediation.  
            - Specific recommendations for improving the vulnerability (e.g., recommendation to use ast.literal_eval instead of eval)  
            - Suggestions for additional security best practices:

            5. Conclusion  
            - Summary of the report and recommendations for future remediation:
            '''
            LLM_res=Grok_req(promft,args.api_key)
            
        except Exception as e:
            print(f"{file_path} 스캔 중 오류 발생: {e}")
        # 결과 파일 저장 경로 설정
        output_path = "response.txt"

        # LLM_res 값이 비어 있는지 확인
        if not LLM_res:
            print("⚠️ LLM_res is empty! No data to write.")
        else:
            with open(output_path, "a", encoding="utf-8") as outfile:
                outfile.write(LLM_res + "\n")
            
            print(f"✅ Response saved to: {output_path}")

        # 최종적으로 response.txt가 존재하는지 확인
        if os.path.exists(output_path):
            print(f"📂 response.txt exists at: {os.path.abspath(output_path)}")
        else:
            print("❌ response.txt was not created.")

                
    print("스캔결과 response.txt에 저장되었습니다.")

if __name__ == "__main__":
    main()
