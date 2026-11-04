# Changelog

> 本文件由 conventional-changelog 从符合 [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md) 的提交信息自动生成，**禁止手写**。
> 版本 tag 格式 `vX.Y.Z`。

## v0.2.0 (2026-11-04)

> 初始导入批次（本文件由首次提交手工播种一次，之后自动生成）。

### Features

- **docs**: 建立技术栈方案 v0.2（许可与权利保留策略、权威论文体系、仓库与提交规范、核验回填）
- **docs**: 建立权威论文清单 `docs/references/PAPERS.md`（52 篇，国内外，逐篇 arXiv ID + 发表信息 + 方案关联）
- **license**: 落地 PolyForm Noncommercial 1.0.0 官方原文、`NOTICE` 归因与权利保留声明、`LICENSE-COMMERCIAL.md` 商业授权入口
- **license**: 建立上游许可证核验矩阵（GitHub / Hugging Face / arXiv API 核验，2026-11-04）
- **docs**: 建立 ADR-0001（许可策略）与 ADR-0002（基座选型方法与评分卡）
- **ci**: 建立 commitlint / license-check / eval-gate 工作流与提交规范强制 footer 校验
- **eval**: 落地 `configs/eval/thresholds.yaml` 阈值单一真源
- **docs**: 归档技术栈方案 v0.1（五层参数化细调体系、数据/训练/评估/排期全文）

### Notes

- 采用「开放权重 / 源码可得」表述，非 OSI 认证开源；NC 条款覆盖项目自有增量。
- 当前阶段 Phase 0，尚未开始数据与训练，无任何实测指标；Q1–Q10 均为目标门禁，待 Phase 2 校准。
- D11（许可条款法务定稿）为发布权重前的阻塞项。
