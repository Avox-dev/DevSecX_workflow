```python
import subprocess
import json

def run_bandit_cli(file_path):
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        return json.loads(e.stdout)
    except json.JSONDecodeError:
        return {"error": "JSON decoding failed"}

if __name__ == "__main__":
    print(run_bandit_cli("../DevSecX/uploads/vulcode.py"))

```
