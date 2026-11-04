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

## v0.4.0 (2026-11-04)

> 实施就绪批次（D16 / ADR-0004：**先规格、后实现**）。只落规格、模板、骨架与守卫，不写实现。

### Features

- **docs**: 建立技术栈方案 v0.4（实施就绪版，VM-TECH-001）——阶段门与 G0 硬前置、F1–F8/Q1–Q10 追溯矩阵、决策注册表 D1–D22、风险 R-01–R-24、版本收敛路线
- **docs**: 建立 ADR-0004（实施就绪路线），确立 Phase 0 不变量：`spec_version=="0.3.0"`、顶层 `additionalProperties===false`、错误码只追加、`calibration.status=="uncalibrated"`、`registry.production==null`、不称 OSI 开源
- **docs**: 建立九份实施规格（`docs/implement/`）：控制层 / API / preset 注册中心 / 数据流水线 / 数据集 manifest / 训练 / 评估门禁 / 部署 / 许可实施
- **configs**: 落地配置模板——`configs/base/base.template.yaml`（capability flags 全 `null` 待实测）、`configs/train/{sft,dpo,quantize}.template.yaml`、`configs/presets/registry.yaml`（`production: null`）、`configs/presets/examples/warm_companion.template.yaml`
- **control**: 落地代码骨架 `src/control/validator.py`（`CapabilityFlags` / `ControlContext` / `ValidationIssue` / `AuditPatch` / `ValidationResult` / `validate_control`）与 `src/serve/api.py`（5 端点），全部 `NotImplementedError`
- **ci**: 新增 `scripts/check_consistency.py` 五项检查（错误码分层比对 / 契约常量硬 FAIL / Markdown 断链 / v0.4 状态标记 / 阈值校准状态）并接入 `eval-gate`
- **test**: 新增 `tests/unit/test_spec_consistency.py` 与 `tests/unit/test_skeleton_contract.py`（13 个测试），把「只落占位」「字段名不可改」变成可执行断言
- **ci**: 新增 `Impl:` footer 校验与 `docs/implement/**` · `src/**` 受保护路径

### Notes

- 仍为 Phase 0：**无训练产出、无模型权重、无实测指标、无运行中的服务**；`eval-gate` 真实生效的仅契约校验、一致性检查与单测。
- 阈值仍为 `uncalibrated`，任何数值均为目标值，**不得当作实测结论**（R-22）。
- `registry.production` 为 `null`（D18），preset 尚未过生产准入（R-21）。
- 已知缺口（v0.5 回填）：`voice_blend`+`speaker_lock=false` 缺专用错误码、`W-PRESET-001` 未在错误码表登记；本版**不新增错误码**。
- D11 法务定稿、R-14b 九项、D1–D10 拍板仍为 G0 硬前置，阻塞权重发布与数据采集。
