import subprocess

def run_bandit_cli(file_path):
    # Bandit CLI 명령어 실행 (예: --format json 옵션을 사용하여 JSON 형식으로 출력)
    # 필요한 옵션은 Bandit 문서에 따라 조정하세요.
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path, "--format", "txt"],
            capture_output=True,
            text=True,
            check=True
        )
        # 표준 출력 (stdout)에 결과가 저장됨
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout

if __name__ == "__main__":
    # 분석할 파일 또는 디렉토리 경로 지정 (여기서는 'uploads/vulcode.py' 파일)
    print(run_bandit_cli("../DevSecX/uploads/vulcode.py"))
