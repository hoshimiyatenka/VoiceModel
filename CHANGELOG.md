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

## v0.3.0 (2026-11-04)

> 契约落地批次。本文件由首次提交手工播种一次，之后由 conventional-changelog 自动生成。

### Features

- **control**: 落地 VoiceSpec 正式契约 `configs/voicespec/voicespec.schema.json`（JSON Schema 2020-12，五层 $defs，全对象 additionalProperties:false）
- **control**: 建立两层校验体系（S 层 Schema + C 层 Control）与错误码表 `docs/voicespec/ERROR-CODES.md`
- **control**: 提供契约示例与本地/CI 校验脚本 `scripts/validate_voicespec.py`
- **docs**: 建立 ADR-0003（参数化控制层实现路径），正式确立 M1–M6 优先级修订
- **docs**: PAPERS.md 补录 6 篇至 58 篇（Qwen3-TTS `2601.15621` / 评测 `2610.23678`、Vocos `2306.00814`、ESD `2010.14794`+`2105.14762`、EmoV-DB `1806.09514`），纠正 `2111.01606`=PolyTrack 误关联，CASIA 语料论文标未找到
- **docs**: 13 篇论文 `journal_ref` 全空，会议归属降级为「arXiv comment 自述」（Lead + subagent 双路交叉印证）
- **license**: 回填 R-14 分项核验；发现 **R-18 代码许可 ≠ 权重许可**（F5-TTS / fishaudio / coqui），许可证矩阵拆两列并回填数据集商用范围；`[MISS]` 项降级为 R-14b 法务跟进
- **ci**: `eval-gate` 从纯占位升级为真实校验 VoiceSpec 契约与示例
- **ci**: 新增 `Spec:` footer 校验与 `configs/voicespec/**` 受保护路径
- **docs**: 全量同步 README / CONTRIBUTING / COMMIT_CONVENTION / CODEOWNERS / CHANGELOG 到 v0.3

### Notes

- 仍为 Phase 0：无任何训练产出与实测指标；`eval-gate` 的 VoiceSpec 契约校验真实生效，golden_set / Q1–Q10 门禁仍为骨架。
- D11 法务定稿仍是发布权重前阻塞项；本批次仅文档/代码层，不触碰权重发布。
- 新增 R-17（契约与实现漂移风险），Phase 3 靠错误码稳定 + 单测缓解。
