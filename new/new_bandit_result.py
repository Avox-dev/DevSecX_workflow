import subprocess

def run_bandit_cli(file_path):
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout

if __name__ == "__main__":
    print(run_bandit_cli("../DevSecX/uploads/vulcode.py"))