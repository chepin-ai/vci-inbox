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
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FINE_OWN_PAT_QTL: ${{ secrets.FINE_OWN_PAT_QTL }}
          QI_PAT: ${{ secrets.QI_PAT }}
          KIMI_API_KEY: ${{ secrets.KIMI_API_KEY }}
          AI_FULL_PAT: ${{ secrets.LINE_PAT || secrets.AI_FULL_PAT || github.token }}
          〈RED〉: ${{ secrets.CI_OPS_LINE_KEY }}
        run: python3 ci/tower.py
