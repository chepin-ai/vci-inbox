# DRILL-0919 PATCH-READY — vci-qtlv/.github/workflows/tower.yml
# 毂预渲染三阶降级全文本;毂写403=物理边界非自限;请本线整件覆盖原档后推+操练+回执
# ---FILE-BEGIN---
name: QTLV-TOWER-03
on:
  push:
    paths: ["inbox/**", "relay/**"]
  repository_dispatch:
    types: ["qtlv-tower"]
  workflow_dispatch: {}
permissions:
  contents: write
concurrency:
  group: qtlv-tower03
  cancel-in-progress: false
jobs:
  tower:
    runs-on: ubuntu-latest
    timeout-minutes: 12
    steps:
      - uses: actions/checkout@v4
      - env:
          〈RED〉: ${{ secrets.GITHUB_TOKEN }}
          〈RED〉_QTL: ${{ secrets.〈RED〉_QTL }}
          QI_PAT: ${{ secrets.QI_PAT }}
          〈RED〉: ${{ secrets.〈RED〉 }}
          〈RED〉: ${{ secrets.LINE_PAT || secrets.〈RED〉 || github.token }}
          〈RED〉: ${{ secrets.〈RED〉 }}
        run: python3 ci/tower.py
