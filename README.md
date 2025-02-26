# DevSecX_workflow

```yml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  # DevSecX_workflow 프로젝트 생성 테스트
  scan-and-llm:
    runs-on: ubuntu-latest
    steps:
      - name: Run DevSecX Workflow
        uses: avox-dev/DevSecX_workflow@main
        env:
          MY_API_KEY: ${{ secrets.MY_API_KEY }}
```
