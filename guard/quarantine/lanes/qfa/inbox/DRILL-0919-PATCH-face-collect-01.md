# DRILL-0919 PATCH-READY — vci-qfa/.github/workflows/face-collect-01.yml
# 毂预渲染三阶降级全文本;毂写403=物理边界非自限;请本线整件覆盖原档后推+操练+回执
# ---FILE-BEGIN---
name: FACE-COLLECT-01
on:
  workflow_dispatch:
  repository_dispatch:
    types: [face-collect]
permissions:
  contents: write
jobs:
  collect:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - name: run collector
        env:
          AI_FULL_PAT: ${{ secrets.LINE_PAT || secrets.AI_FULL_PAT || github.token }}
          〈RED〉: ${{ secrets.CI_OPS_LINE_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python ci/face_collect.py
