# AI 智能体声音训练项目 · 技术栈方案（v0.4 · 实施就绪版）

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-TECH-001 v0.4 |
| 版本 | **v0.4**（实施就绪版 / 规格全量版） |
| 日期 | 2026-11-04 |
| 作者 | lead（VoiceModel 项目） |
| 定位 | **把 v0.1–v0.3 的方案、许可、论文、契约收敛为一套「可照着开工」的实施规格体系**：阶段门、追溯矩阵、编号注册表、配置模板、代码骨架、CI 校验、收敛排期全部落盘 |
| 上游 | [v0.1](AI智能体声音训练项目_技术栈方案_v0.1.md) · [v0.2](AI智能体声音训练项目_技术栈方案_v0.2.md) · [v0.3](AI智能体声音训练项目_技术栈方案_v0.3.md) |
| 仓库 | https://github.com/hoshimiyatenka/VoiceModel |
| 状态 | **待评审**。目标：再迭代 1–2 版（v0.5 回填评审 / v1.0 冻结）即可进入实施 |

---

## 0. 本版怎么读（先看这一节）

用户第四轮要求（原文）：「v0.4 尽量把文档写全一点 再迭代几个版本就可以落地实施了」。本版据此把「写全」定义为**四件可验证的事**，而不是把旧版重抄一遍：

1. **编号注册表闭合**：D1–D22、R-01–R-24、F1–F8、Q1–Q10、E-*/W-* 错误码全部有唯一归属与状态，任何文档不再出现「待定编号」或自造编号。见 §5、§13、§4。
2. **追溯矩阵闭合**：每条需求 → 设计落点 → VoiceSpec 字段 → 门禁 → 实施规格文件，一行贯通。见 §4。
3. **实施规格落盘**：`docs/implement/**` 九份规格 + `configs/**` 模板 + `src/**` 骨架 + `scripts/check_consistency.py` + `tests/unit/test_spec_consistency.py`，把「怎么做」从章节标题变成可照抄的函数签名、YAML 字段、端点、CI 检查项。见 §15、§16。
4. **收敛路线明确**：v0.4 → v0.5 → v1.0 → 实施，每版的准入/准出与「谁阻塞谁」写死，避免无限迭代。见 §14。

**诚实基线（不得在任何文档中改写）**：
- 技术路径仍为 **Phase 0（立项 / 选型核验期）**：**没有任何训练产出、没有模型权重、没有任何实测指标、没有运行中的服务**。
- `configs/eval/thresholds.yaml` 仍是 `calibration.status=uncalibrated`，所有 Q1–Q10 数字是**目标值**，不是实测结论。
- v0.4 新增的代码骨架一律 `raise NotImplementedError` / `status: template`，**不是实现**。`eval-gate` CI 里真实生效的只有：契约示例校验、阈值结构校验、一致性检查、单测；golden_set 合成与 Q1–Q10 门禁仍是 Phase 2 骨架。
- 许可：对外称「**开放权重 / 源码可得（source-available, open-weight）**」，**不称 OSI 开源**（OSD 第 6 条禁止按用途领域歧视，故「开源」与「禁止商业化」不可兼得，见 ADR-0001）。项目自有增量用 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；**上游 Apache-2.0 原权重，第三方仍可按原条款商用**，NC 不覆盖上游。
- **D11（许可条款法务定稿）仍是发布权重前的 P0 阻塞项**；本版所有工作都在文档 / 配置 / 代码骨架层，不触碰权重发布，故不受 D11 阻塞。

---

## 1. 摘要与一页结论

### 1.1 一句话

以「**机器可执行的 VoiceSpec 契约**」为控制面单一真源，以「**四套数据集 + 冻结 golden_set + 阈值单一真源**」为质量面，以「**开放权重 / 禁商用 + 双授权**」为权利面，用三档排期（基线档 B 16–20 周）把「所有声音可参数化细调」从文档约定做成可 CI 回归、可取证、可回滚的工程系统。

### 1.2 本版新增（相对 v0.3）

| # | 新增 | 落点 | 为什么现在做 |
| --- | --- | --- | --- |
| 1 | v0.4 主方案（本文件） | 本文件 | 把散在 v0.1–v0.3 的设计收敛为一套实施总纲 |
| 2 | [ADR-0004 实施就绪路线](decisions/ADR-0004.md) | `docs/decisions/` | 固化「先规格后实现」的阶段门，防止 Phase 0 写假实现 |
| 3 | 九份实施规格 | [docs/implement/](implement/README.md) | 控制层 / API / preset / 数据 / manifest / 训练 / 评估 / 部署 / 法务 |
| 4 | 配置模板 | `configs/presets/` · `configs/train/` · `configs/base/` | 让「配置即代码」有可照抄的字段与占位规范 |
| 5 | 代码骨架 | `src/**` | 模块边界与函数签名先冻结，Phase 2/3 填实现 |
| 6 | 一致性校验器 | [scripts/check_consistency.py](../scripts/check_consistency.py) | 自动挡住 R-19/R-20/R-22/R-24 四类漂移 |
| 7 | 单测 | [tests/unit/test_spec_consistency.py](../tests/unit/test_spec_consistency.py) | 契约常量、错误码唯一性、校准状态成为可跑断言 |
| 8 | 规范与 CI 同步 | `README` / `CONTRIBUTING` / `CHANGELOG` / `COMMIT_CONVENTION` / `CODEOWNERS` / `eval-gate.yml` | 新增路径纳入受保护与强制 footer |

### 1.3 一页结论（请评审时拍板）

| 结论 | 内容 | 依据 |
| --- | --- | --- |
| C1 | **本版不写训练/服务实现代码**，只落规格、模板、骨架、CI；实现从 Phase 2/3 开始 | D16；Phase 0 无算力 / 数据 / 授权，写实现 = 假进度 |
| C2 | **契约冻结**：VoiceSpec 保持 `spec_version="0.3.0"`，v0.4 **不改 schema、不升版本、无 BREAKING CHANGE** | §7.1；schema 是单一真源，改动成本最高 |
| C3 | **D1–D10 未拍板前用临时默认建议推进**（provisional，非承诺），拍板即覆盖 | D17；避免「等拍板 → 什么都不做」 |
| C4 | **preset 不得标 production**：registry `production: null`，未过 golden_set 门禁不得进业务 preset | D18 / R-21 |
| C5 | **收敛路线**：v0.4（规格全量）→ v0.5（评审回填 + D 拍板 + 法务清单）→ v1.0（冻结）→ 档 B 实施 | D22 / §14 |
| C6 | **「落地实施」的硬前置门 G0**：D1–D11 拍板 + D11 法务签字 + R-14b 清零 + 算力到位 | §3.3 / §14.2；G0 未过不进 P1 |
| C7 | **轨道 A 三候选仍不锁定**：CosyVoice 2 / Qwen3-TTS / VoxCPM2（均 Apache-2.0），Phase 2 同台实测定型 | D19 / ADR-0002；无实测分数不定型 |

---

## 2. 版本演进与文档体系

### 2.1 谱系

| 版本 | 日期 | 解决的问题 | 交付重心 | 归档状态 |
| --- | --- | --- | --- | --- |
| [v0.1](AI智能体声音训练项目_技术栈方案_v0.1.md) | 2026-11-04 | 「用什么训练 / 走到哪儿 / 多久 / 全参数细调」 | 需求 F1–F8 / Q1–Q10、五层架构、双轨路线、数据/训练/评估/服务/排期/风险 | 归档，细节仍有效 |
| [v0.2](AI智能体声音训练项目_技术栈方案_v0.2.md) | 2026-11-04 | 「开源但禁商业化 / 权威论文 / GitHub 仓库 + 提交规范」 | 许可策略、52 篇论文体系、ADR-0001/0002、仓库与 CI | 归档，历史数字保留 |
| [v0.3](AI智能体声音训练项目_技术栈方案_v0.3.md) | 2026-11-04 | 把参数化从文字变成机器可执行契约 | VoiceSpec JSON Schema、错误码表、ADR-0003、论文补录至 58 篇、R-18 发现 | 归档，契约仍生效 |
| **v0.4（本版）** | 2026-11-04 | 「写全，再迭代几版即可落地实施」 | 实施规格体系、编号闭合、配置模板、代码骨架、一致性校验、收敛排期 | **当前版** |

> 归档规则（D22）：历史版本**只增不改**；新版用「修订/取代」显式指向旧章节，不批量回改归档正文。例：v0.1 §5.4 的 M1–M6 优先级已由 [ADR-0003](decisions/ADR-0003.md) 取代，v0.1 正文保留原样。

### 2.2 单一真源清单（禁止复制数字 / 禁止第二份定义）

| 真源 | 管什么 | 被谁引用 | 变更代价 |
| --- | --- | --- | --- |
| [configs/voicespec/voicespec.schema.json](../configs/voicespec/voicespec.schema.json) | VoiceSpec 结构 / 类型 / 范围 / 枚举 / 静态依赖 | 校验脚本、控制层、API、preset、示例、文档 | 最高；major 升级须 golden_set 全量回归 |
| [docs/voicespec/ERROR-CODES.md](voicespec/ERROR-CODES.md) | 全部 E-*/W-* 错误码语义 | 控制层规格、实现、单测、响应信封 | 只追加，不改义 |
| [configs/eval/thresholds.yaml](../configs/eval/thresholds.yaml) | Q1–Q10 全部阈值 | 评估门禁、文档、CI、模板（`thresholds_ref`） | 需 `eval(gates)` + `Gate-Report:` |
| [LICENSE](../LICENSE) | PolyForm NC 1.0.0 官方逐字原文 | NOTICE、商业授权、模型卡 | **禁止改写**；改需 `License-Review:` |
| [docs/licensing/UPSTREAM-LICENSE-MATRIX.md](licensing/UPSTREAM-LICENSE-MATRIX.md) | 上游代码 / 权重 / 数据集许可核验值 | 法务规格、模型卡、基座选型 | v0.3 拆两列，R-18 后不得按代码推断权重 |
| [docs/references/PAPERS.md](references/PAPERS.md) | 58 篇论文的 ID / 日期 / 发表状态 | 设计依据、指标来源 | 发表状态降级为 arXiv comment 自述 |
| [COMMIT_CONVENTION.md](../COMMIT_CONVENTION.md) | 提交格式与强制 footer | `.commitlintrc.yml`、`commitlint.yml`、PR | 规范变更须同步 CI |

### 2.3 阅读路径（按角色）

| 角色 | 顺序 |
| --- | --- |
| 评审 / 决策者 | §0 → §1 → §3（阶段门）→ §5（决策）→ §13（风险）→ §14（排期与收敛） |
| 实施负责人 | §6（架构落地）→ §15/§16（文件索引）→ [实施规格总索引](implement/README.md) |
| 控制层开发 | §7 → [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) → [API-SPEC](implement/control/API-SPEC.md) → [PRESET-REGISTRY-SPEC](implement/control/PRESET-REGISTRY-SPEC.md) → [ERROR-CODES](voicespec/ERROR-CODES.md) |
| 数据 / 训练 | §8/§9 → [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) → [DATASET-MANIFEST-SPEC](implement/data/DATASET-MANIFEST-SPEC.md) → [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) |
| 评估 / 运维 | §10/§11 → [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) → [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) |
| 法务 / 合规 | §12 → [LICENSING-IMPLEMENTATION-SPEC](implement/legal/LICENSING-IMPLEMENTATION-SPEC.md) → [许可证矩阵](licensing/UPSTREAM-LICENSE-MATRIX.md) → [LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md) |

---

## 3. 实施就绪度总览

### 3.1 当前完成度（Phase 0 诚实盘点）

| 层 | 已落盘（可用） | 未落盘（明确缺口） |
| --- | --- | --- |
| 方案 / 决策 | v0.1–v0.4、ADR-0001–0004、D1–D22 注册表、R-01–R-24 全表 | D1–D11 拍板、D11 法务签字、R-14b 清零 |
| 契约 | VoiceSpec JSON Schema 2020-12、三示例、错误码表、校验脚本 | C 层 18 个错误码的**实现代码**（Phase 3） |
| 实施规格 | 九份 `docs/implement/**` | 规格评审回填（v0.5） |
| 配置 | thresholds.yaml、registry 骨架、train/base 模板 | Phase 2 实测后回填的真实超参与 capability_flags |
| 代码 | `src/**` 模块边界与签名占位、`check_consistency.py`、单测 | 真实训练 / 控制 / 服务实现 |
| 数据 | manifest 字段规范、golden_set 冻结流程 | 任何音频、标注、授权书、golden_set v1 实体 |
| 模型 / 指标 | 三候选许可核验、评分卡模板 | 任何权重、baseline 分数、校准后的阈值 |
| CI | commitlint / license-check / eval-gate（契约+一致性+单测真实生效） | golden_set 合成、Q1–Q10 自动门禁（Phase 2） |

### 3.2 阶段门（Phase 0 → Phase 4）

| 阶段 | 目标 | 准入（必须先有） | 准出（可交付） | 本版位置 |
| --- | --- | --- | --- | --- |
| **Phase 0** 立项 / 选型核验 | 文档、契约、规格、骨架、CI 自洽 | — | 本版 v0.4 + 三个 CI 全绿 + `check_consistency.py` 0 FAIL | **当前** |
| **Phase 1** 数据与授权 | 采集 + 质检 + golden_set v1 冻结 | **G0 通过**（§3.3） | `ds-*` manifest、质检报告、授权书、`golden_set/manifest.yaml` | [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) |
| **Phase 2** 基座复现与定型 | 三候选同台、能力探测、阈值校准 | Phase 1 数据集 | ADR-0002 回填、模型卡、capability_flags、`calibration.status=calibrated` | [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) · [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) |
| **Phase 3** 控制层与微调 | C 层 18 码、preset 注册、SFT→DPO、全量门禁 | Phase 2 定型基座 | 开放参数清单、preset production、全量门禁报告 | [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) |
| **Phase 4** 服务化与上线 | API / 流式 / 监控 / 降级 / 回滚 / 水印 | Phase 3 门禁通过 | 服务、模型卡、回滚手册、水印与审计 | [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) |

### 3.3 硬前置门 G0（「可以落地实施」的判定条件）

**G0 未过，不进 P1、不采购算力、不采集数据、不发布权重。**

| 门项 | 内容 | 责任 | 当前 |
| --- | --- | --- | --- |
| G0-1 | D1–D10 逐项拍板（或明确「暂缓 + 按 D17 默认建议」） | 评审人 | ❌ 未拍板 |
| G0-2 | **D11 许可条款法务定稿并签字** | 法务 | ❌ 阻塞 |
| G0-3 | R-14b 九项法务跟进清零或登记「替换方案」（§12.2） | 法务 + 选型 | ❌ 未清零 |
| G0-4 | D6 算力预算与硬件到位（H-1/H-2/H-3） | 资源方 | ❌ 未到位 |
| G0-5 | v1.0 方案冻结（v0.5 评审回填完成） | 评审人 | ❌ 未冻结 |

> 说明：D17 的临时默认建议**只用于写规格与模板**，不构成 G0 通过；任何「按默认建议先跑」都必须显式标注 provisional。

---

## 4. 需求冻结与追溯矩阵

### 4.1 编号冻结规则

- F1–F8（功能性需求）、Q1–Q10（非功能性 / 质量需求）沿用 v0.1 §2，**不得新增、不得改义**；新增诉求走 v0.5 变更评审并升文档版本。
- 所有编号在本版 §4.2/§4.3、§5、§13 出现且状态一致；[scripts/check_consistency.py](../scripts/check_consistency.py) 与单测负责守住契约常量与错误码，编号语义由本表守。

### 4.2 功能需求追溯（F1–F8）

| 需求 | 优先级 | 设计落点 | VoiceSpec 字段 | 门禁 | 实施规格 |
| --- | --- | --- | --- | --- | --- |
| F1 给定参考音频 / speaker_id 合成目标音色 | P0 | 轨道 A 基座 + 轨道 B 音色资产 | `identity.speaker_id` / `ref_audio_uri` / `ref_text` / `speaker_lock` | Q2（speaker_cosine_min） | [PRESET-REGISTRY-SPEC](implement/control/PRESET-REGISTRY-SPEC.md) · [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) |
| F2 中文、中英混、数字/日期/专名正确读法 | P0 | L-D 确定性规则层（TN + G2P + 词典覆写） | `linguistic.lang` / `text_normalize` / `pronunciation_dict` / `phoneme_overrides` / `code_switch_policy` | Q1 + R-11 发音回归集零容忍 | [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) |
| F3 情感/语速/音高/能量/停顿单独可调 | P0 | L-B 连续细调 + L-C 状态层；`M4>M2>M1>M5>M3>M6` | `prosody.*` / `style.emotion` / `emotion_strength` / `pauses[]` / `emphasis[]` | Q5 + Q10（单调性 / 正交） | [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) |
| F4 时长精确控制 | P0 候选（v0.2 升级） | 三路解耦，依赖基座 `exact_duration` 能力 | `prosody.duration_mode` / `duration_ms` / `duration_ratio` / `duration_range_ms` | Q6；`E-CAPABILITY-001` 不支持直接 400 | [API-SPEC](implement/control/API-SPEC.md) |
| F5 任意参数组合存 preset 一键复现 | P0 | preset 注册中心 + 默认值展开 + 审计 | `preset` / `preset_version` / `audit.preset_resolved` | Q9（byte-level 一致） | [PRESET-REGISTRY-SPEC](implement/control/PRESET-REGISTRY-SPEC.md) |
| F6 流式输出、实时首包延迟 | P1 | 服务端 SSE / chunk 调度 | `render.streaming` / `chunk_ms` / `seed` | Q7；R-08 跨 chunk 韵律连续 | [API-SPEC](implement/control/API-SPEC.md) · [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) |
| F7 多说话人 / 多音色矩阵 | P2 | 音色注册表 + 权限隔离 + 插值 | `identity.voice_blend[]`（`speaker_lock=true` 时禁，E-CONFLICT-004） | Q2 cross 上限 | [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) |
| F8 产物版本化、可回滚、可审计 | P0 | 命名规范 + 模型卡 + checkpoint manifest + 审计日志 | `audit.*`（服务端只读，E-AUDIT-001） | Q9 | [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) · [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) |

### 4.3 质量需求追溯（Q1–Q10）

| 需求 | 目标（**目标值 / 待校准**） | 真源 | 采集方式 | 规格 |
| --- | --- | --- | --- | --- |
| Q1 可懂度 | 中文 CER / 英文 WER | thresholds.yaml `hard.cer_zh_max` / `wer_en_max` | 固定 ASR 回环（ASR 模型版本锁定） | [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) |
| Q2 说话人相似度 | cosine 下限 + 跨说话人上限 | `hard.speaker_cosine_min` / `_cross_max` | ECAPA-TDNN embedding | 同上 |
| Q3 自然度 | MOS + UTMOS 双满足 | `soft.mos_min` / `utmos_min` | 盲测（VoiceMOS Challenge 协议）+ 代理 | 同上 |
| Q4 音质 | DNSMOS + 削波/爆音/底噪 | `hard.dnsmos_min` / `clipping_count_max` | 自动检测 + 听审 | 同上 |
| Q5 情感可控 | 分类准确率 + 连续强度 ρ | `soft.emotion_acc_min` / `emotion_monotonic_rho_min` | 固定情感分类器 + 人评抽样 | 同上 |
| Q6 时长精度 | exact 误差 | `hard.duration_exact_abs_ms` / `_ratio` | 实测音频时长 vs 目标 | 同上 |
| Q7 实时性 | 首包 P95 / RTF | `soft.first_packet_p95_ms` / `rtf_max` | 指定硬件下压测 | [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) |
| Q8 稳定性 | 1000 句回归 0 异常 | `hard.regression_*` | CI 全量合成 | [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) |
| Q9 可复现 | 同 (preset, model, seed, text) 波形 byte-level 一致 | `hard.waveform_reproducible` | 固定推理栈 + 依赖锁 + Docker + seed | [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) |
| Q10 参数正交 | 单参数扫描其他层漂移 | `hard.param_scan_*` + `soft.param_monotonic_rho_min` | 5 点扫描 + 说话人不漂移 | [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) |

> **R-22 防线**：上表「目标」列一律为**目标值 / 待校准**。`calibration.status=uncalibrated` 期间，任何文档、报告、提交信息不得把这些数字写成「实测 / 已达 / 已达标」。[scripts/check_consistency.py](../scripts/check_consistency.py) 检查项 (e) 会 WARN 状态被提前改成 calibrated。

---

## 5. 决策注册表（D1–D22）

> **D1–D10 与 D11 的可勾选拍板表**见 [`docs/decisions/DECISION-SHEET.md`](decisions/DECISION-SHEET.md)（逐项列选项、代价、建议与「不拍板的后果」）。

### 5.1 既有决策状态（D1–D15）

| ID | 决策点 | 状态 |
| --- | --- | --- |
| D1 | 声音来源：自录授权 / 采购 / 客户自带 / 合成生成 | **待拍板**（G0-1） |
| D2 | 首要场景：实时对话 vs 离线内容生产 | **待拍板**（G0-1） |
| D3 | 声音数量：1 主音色 vs 多音色矩阵 | **待拍板**（G0-1） |
| D4 | 是否需精确时长控制 | **待拍板**（G0-1）；F4 已升 P0 候选 |
| D5 | 是否允许云端商业 TTS 作对照 / 兜底 | **待拍板**（G0-1） |
| D6 | 算力预算与硬件 H-1/H-2/H-3 | **待拍板**（G0-4） |
| D7 | 商用许可要求 | **已由 v0.2 定**：接受禁商用 + 双授权（ADR-0001） |
| D8 | 语言范围 | **待拍板**（G0-1） |
| D9 | 情感粒度 | **待拍板**（G0-1） |
| D10 | 交付形态 | **待拍板**（G0-1） |
| **D11** | **许可条款法务定稿** | **P0 阻塞，待法务签字**（G0-2）；未签字不发布权重 |
| D12 | VoiceSpec 用 JSON Schema 2020-12 单一真源 + 全对象 `additionalProperties:false` | **已落地**（v0.3） |
| D13 | S 层 + C 层两层校验，错误码只追加 | **契约层已落地**；C 层 Phase 3 实现 |
| D14 | eval-gate 从占位升级为真实校验契约示例 | **已落地**（v0.3）；v0.4 再加一致性与单测 |
| D15 | 契约变更须 `Spec:` footer + CODEOWNERS 保护 | **已落地**（v0.3） |

### 5.2 v0.4 新增决策（D16–D22）

| ID | 决策 | 结论 | 理由（不可丢） | 状态 |
| --- | --- | --- | --- | --- |
| **D16** | 实施推进形态 | v0.4 **只落「规格 + 模板 + 骨架 + CI」**，训练 / 控制 / 服务实现代码留 Phase 2/3；`src/**` 一律签名占位 + `NotImplementedError` | Phase 0 无算力、无数据、无授权、无法务签字；此时写实现只能造假进度且会与未来实测结论冲突 | 已落地 |
| **D17** | D1–D10 未拍板前的推进方式 | 采用**临时默认建议（provisional）**写规格与模板，**非承诺、拍板即覆盖**；建议值见 §5.3 | 避免「等拍板 → 全部停摆」，同时不把猜测固化成承诺 | 已落地（建议待评审） |
| **D18** | preset 生产准入 | `registry.yaml` 的 `production` 指针必须带**非空 `gate_report`** + golden_set 通过 + 2 人批准；状态只能 `template → staging → production` 单向；**Phase 0 `production: null`** | 防「模板配置被当业务 preset 上线」（R-21）；门禁报告是唯一客观凭据 | 已落地 |
| **D19** | 基座定型流程 | Phase 2 三候选（CosyVoice 2 / Qwen3-TTS / VoxCPM2）**同台实测**：固定脚本 / 固定 seed / 固定数据切片 → 评分卡（ADR-0002，含「解耦表示」10% +「参数可枚举性」10%）→ 能力探测回填 `configs/base/` 的 `capability_flags` → 回填 ADR-0002 + 模型卡 | 无实测分数不定型；许可干净（均 Apache-2.0）只是准入，不是质量结论 | 已落地（流程） |
| **D20** | golden_set 与阈值校准 | train/val/test/golden_set 四份不相交；golden_set **绝对冻结**（CI 校验 hash，PR 禁改）；阈值**校准只能收紧**，放宽须书面评审；`calibration.status` 由 `uncalibrated → calibrated` 须附 `baseline_report` | 防「用调过阈值的回归集自证」（v0.1 §8.1 / R-22） | 已落地（流程） |
| **D21** | 交付 / 部署默认 | 默认**本地权重 + 私有 API（Docker）**，不入公有云托管；水印 `render.watermark` 默认 `true`；Q7 延迟预算依 D2 结果定 | 与禁商用许可一致；水印默认开是许可联动要求（E-LICENSE-001） | 已落地（默认建议） |
| **D22** | 版本收敛路线 | **v0.4 规格全量 → v0.5 评审回填 + D 拍板 + 法务清单 → v1.0 方案冻结 → 档 B 实施**；历史归档只增不改，新版显式「修订/取代」 | 给「再迭代几个版本就落地」一个可判定的终点，避免无限迭代 | 已落地 |

### 5.3 D17 临时默认建议表（provisional · 非承诺 · 拍板即覆盖）

| 原决策 | 临时默认建议 | 影响 |
| --- | --- | --- |
| D1 声音来源 | **自录授权优先**；采购 / 客户自带 / 合成生成留备选 | 合规路径最清晰；manifest 强制 `license_id` + 授权书引用 |
| D2 场景 | **实时对话优先**，离线内容生产共用同一套契约与 API | Q7 延迟暂按软指标；若改离线优先，流式优先级下调 |
| D3 音色数 | **1 个主音色起步**，架构保留 `voice_blend` 扩展 | 档 B 排期；多音色矩阵走档 C |
| D4 精确时长 | **保留 exact 能力但不锁基座**；`E-CAPABILITY-001` 不支持直接报错 | 三候选须在 Phase 2 能力探测中验 `exact_duration` |
| D5 云端对照 | **允许云端商业 TTS 仅作质量上限对照 / 兜底，不进交付物** | 不引入额外许可传导到发布权重 |
| D6 算力 | 按 **H-2（1×80GB 或 4–8×24GB）估算**，不采购、不承诺 | 成本模型；G0-4 到位才生效 |
| D8 语言 | **中文 + 中英混** | L-D `code_switch_policy` 与发音词典规模 |
| D9 情感粒度 | **离散 10 类（schema enum）+ 连续强度**，三者中自然语言指令仅作修饰 | 与 `style_prompt` 不得单独作 preset（E-CAPABILITY-004）一致 |
| D10 交付 | **本地权重 + 私有 API**（D21） | 与 D2/D6 联动 |

> 提醒：D7 已由 v0.2 定为「禁商用 + 双授权」，**不在 provisional 之列**；D11 法务签字不可用默认建议替代。

---

## 6. 架构落地分层

### 6.1 逻辑层 → 仓库目录映射（v0.1 §3 五层 + 本版落地）

| 逻辑层 | 职责 | 仓库落点 | 本版状态 |
| --- | --- | --- | --- |
| L6 服务 / 交付面 | API、流式、鉴权、水印、监控、回滚 | [src/serve/api.py](../src/serve/api.py) · `src/serve/` · [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) | 签名占位 |
| L5 控制面 | VoiceSpec 解析、S+C 校验、preset 合并、能力探测、降级、审计 | [src/control/validator.py](../src/control/validator.py) · `configs/voicespec/` · [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) | 契约已生效，C 层占位 |
| L4 模型面 | 基座封装、adapter、控制头、音色注册 | `src/models/` · [configs/base/base.template.yaml](../configs/base/base.template.yaml) | 模板占位 |
| L3 训练面 | SFT / DPO / 量化 / 蒸馏 | `src/train/` · `configs/train/` · [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) | 模板占位 |
| L2 数据面 | 清洗 / 质检 / 对齐 / 标注 / 打包 | `src/data/` · `datasets/manifests/` · [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) | 字段规范已定，无实体数据 |
| L1 评估面 | 指标、golden_set 运行器、参数扫描 Harness | `src/eval/` · `configs/eval/` · [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) | 阈值真源已定，门禁 Phase 2 |
| L0 前端面 | TN / G2P / 词典 / SSML-like 标记 | `src/frontend/` · `dicts/` | 目录占位 |

### 6.2 三条贯穿线

| 线 | 内容 | 守卫 |
| --- | --- | --- |
| **控制线** | 请求 → S 层 Schema → preset 合并 → C 层语义 → 能力探测 → 降级 → 审计 → 合成 | `additionalProperties:false` + 18 个 C 层错误码 + `audit.degraded` |
| **质量线** | 数据 manifest → 四套切分 → 训练 → golden_set 全量合成 → Q1–Q10 比对 → 门禁报告 → preset 准入 | thresholds.yaml 单一真源 + frozen golden_set hash |
| **权利线** | 上游许可核验 → 自有增量 NC → 商业授权另议 → 水印 / 归因 → 模型卡 → 发布前 D11 签字 | [许可证矩阵](licensing/UPSTREAM-LICENSE-MATRIX.md) + license-check CI + `E-LICENSE-001/002` |

### 6.3 双轨路线（沿用 v0.1 §4.3，本版不推翻）

- **轨道 A · 基座轨（控制面）**：CosyVoice 2 / Qwen3-TTS / VoxCPM2 三候选，均代码 + 权重 Apache-2.0；Phase 2 同台实测定型（D19）。**不用 Spark-TTS 权重**（`cc-by-nc-sa-4.0` SA 传染，ADR-0001）。
- **轨道 B · 定制轨（音色资产）**：LoRA / adapter + 音色注册；受 D1/D3 与 D11 约束。
- **L5 VoiceSpec 解耦**：两轨通过同一契约交汇，业务只写 VoiceSpec，不碰模型内部。

---

## 7. VoiceSpec 契约实现路径

### 7.1 冻结声明（本版最重要的不变量）

| 不变量 | 值 | 守卫 |
| --- | --- | --- |
| schema 方言 | JSON Schema draft 2020-12 | `$schema` |
| `spec_version` | `const: "0.3.0"` | 单测断言 + `check_consistency.py` (b) |
| 顶层 `additionalProperties` | `false`（全部对象同样） | 单测断言 + (b) |
| 五层 `$defs` | IdentitySpec / ProsodySpec / StyleSpec / LinguisticSpec / RenderSpec（+ AttributeSpec / AuditSpec / Unit01 / Uri / Span / F0Point / AdapterMix） | 单测断言 |
| 错误码 | [ERROR-CODES.md](voicespec/ERROR-CODES.md) 唯一真源，**只追加** | `check_consistency.py` (a) |
| **v0.4 动作** | **不改 schema、不升版本、无 BREAKING CHANGE** | 本表 |

> 版本演进规则见 [ERROR-CODES.md §7](voicespec/ERROR-CODES.md)：新增可选字段 → minor；新增必填 / 改枚举 / 收紧范围 → major + golden_set 全量回归；删除字段 → major + 一个 minor 兼容期。

### 7.2 两层校验与顺序

| 步 | 层 | 输入 → 输出 | 失败码 |
| --- | --- | --- | --- |
| 1 | **S 层 Schema** | 原始请求 → 结构合法对象 | `E-SCHEMA-001..006` / `E-DEPENDENCY-001..003` / `E-FORMAT-001/002` |
| 2 | preset 合并 | spec + registry → 展开默认值后的 spec | `E-PRESET-001/002` |
| 3 | **C 层语义** | 展开 spec → 冲突消解 / 跨字段算术 | `E-CONFLICT-001..005` / `E-RANGE-001` / `W-CONFLICT-006/007` |
| 4 | 能力探测 | spec + capability_flags → 支持/不支持 | `E-CAPABILITY-001..004` / `W-CAPABILITY-002/003` |
| 5 | 降级决策 | 不支持项 → 降级链 + `audit.degraded=true` | `W-RENDER-001` |
| 6 | 审计填充 | 服务端只读 `audit.*` | `E-AUDIT-001` / `E-LICENSE-001/002` |

完整函数签名、18 个 C 层错误码逐码判定逻辑、单测组织见 [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md)；响应信封与 HTTP 映射见 [API-SPEC](implement/control/API-SPEC.md)。

### 7.3 控制手段优先级（ADR-0003 已取代 v0.1 §5.4）

```
M4 > M2(连续声学特征编辑) > M1(离散标签) > M5 > M3 > M6(DSP，仅降级)
```

- 依据：FastSpeech 2（`arXiv:2006.04558`）证明 F0 / energy / duration 可显式条件注入，连续量走 M2 比自然语言更精确可复现。
- `pitch` / `rate` 主控制**禁用 M6**（金属音、损相似度）；仅降级路径允许，且必须 `audit.degraded=true` + `W-RENDER-001`。
- `style_prompt` 不得单独作 preset 唯一控制手段（PromptTTS 2 `2309.02285` 描述不可严格复现）→ `E-CAPABILITY-004`；`W-CONFLICT-006` 离散 `emotion` 优先。

### 7.4 preset 注册中心（D18）

- 结构见 [configs/presets/registry.yaml](../configs/presets/registry.yaml)：`schema_ref` / `production` / `presets[].versions[]`（`version` / `path` / `status` / `gate_report` / `created_by` / `approved_by`）。
- `preset_version` 省略 → 解析为 `production` 并写 `audit.preset_resolved`；**Phase 0 `production: null`，故省略版本必须报错**而非静默选模板。
- 默认值展开：`scenario` → 一组 L-B/L-C 默认值 → spec 显式字段覆盖（preset 是默认值集合，**不是强制值**，W-CONFLICT-007）。
- 变更走 PR，强制 `Gate-Report:` + `Preset:` footer（[COMMIT_CONVENTION.md §5](../COMMIT_CONVENTION.md)），CODEOWNERS 保护。
- 完整算法与联动见 [PRESET-REGISTRY-SPEC](implement/control/PRESET-REGISTRY-SPEC.md)。

---

## 8. 数据工程实施

| 主题 | 结论 | 规格 |
| --- | --- | --- |
| 流水线 ①–⑧ | 采集 → 清洗 → 转写 → **强制对齐（MFA/WhisperX 产字级时间戳）** → 质检 → 标注 → 打包 → 四套切分 | [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) |
| 时间戳为何是前提 | M2 连续声学特征编辑与 F4 精确时长都依赖字级 / 音素级对齐 | 同上 |
| 工具链许可 | 代码已核验（whisper MIT / whisperX BSD-2-Clause / MFA MIT / FunASR MIT / Wenet Apache-2.0）；**各工具权重 / 模型卡许可未全部核验 → R-14b** | [许可证矩阵 §3](licensing/UPSTREAM-LICENSE-MATRIX.md) |
| 数据集商用 | AISHELL-3 Apache-2.0 可商用；WenetSpeech Apache-2.0 但 HF `gated=auto` 需申请；**EmoV-DB 仅非商用**；**ESD / CASIA 官方许可 [MISS]** | [许可证矩阵 §4](licensing/UPSTREAM-LICENSE-MATRIX.md) |
| 防泄漏 | 按说话人 + 按文本去重；train/val/test/golden_set 四份不相交 | [DATASET-MANIFEST-SPEC](implement/data/DATASET-MANIFEST-SPEC.md) |
| 授权 | 每条样本强制 `license_id` + 授权书引用；自有数据与公开数据物理隔离（R-02） | 同上 |
| 实体不入库 | 音频走 DVC / 对象存储；仓库只留 `datasets/manifests/*.yaml` 与 `datasets/golden_set/manifest.yaml`（[.gitignore](../.gitignore) 已忽略 `datasets/raw/`、`datasets/processed/`） | 同上 |
| 阻塞 | **D1 未拍板前不得开始采集**；按 D17 默认建议只用于写规格 | §3.3 G0-1 |

---

## 9. 训练实施

| 阶段 | 目标 | 产物命名 | 准出 |
| --- | --- | --- | --- |
| Stage 1 SFT | Q1 / Q2 达标 | `model-<base>-sft-<step>-<score>` | 说话人相似度 + 可懂度门禁 |
| Stage 2 DPO（`arXiv:2305.18290`） | Q3 + F3/F4 遵循度 | `model-<base>-dpo-<step>-<score>` | 盲测为最终裁判；**代理奖励不作上线依据**（R-07） |
| Stage 3 量化 / 蒸馏 | Q7 延迟与成本 | `model-<base>-quant-<step>-<score>` | **强制重跑全量门禁**，越界即回滚（R-10） |

- 超参模板：[sft](../configs/train/sft.template.yaml) / [dpo](../configs/train/dpo.template.yaml) / [quantize](../configs/train/quantize.template.yaml)；均为 `status: template`、数值 `<...>` / 目标值待校准。
- checkpoint 按 `step + 门禁分数` 双命名，只留 Top-K（Q1–Q4 综合分）+ 最近 3 个。
- 防遗忘（R-06）：冻结底层、低 LR、通用语料 replay、发音回归集；CER 上升超阈值即回退。
- Q9 可复现：固定推理栈 + `locks/` 依赖锁 + Docker digest + seed + 模型卡；CI 做波形 hash 比对（R-23）。
- 实验跟踪 MLflow 自托管，**原始日志不进仓库**，只留摘要。
- 完整字段、准入/准出/回滚点见 [TRAINING-SPEC](implement/train/TRAINING-SPEC.md)。

---

## 10. 评估与门禁实施

| 主题 | 结论 |
| --- | --- |
| 四套数据集 | train / val / test / **golden_set（冻结，PR 禁改，CI 校验 hash）**；覆盖 8 类情感 × 3 语速 × 中英混 × 多音字 × 长数字/日期 × 专名 × 极短/极长句 × 疑问/感叹 × 停顿密集 |
| 客观指标 | CER/WER、ECAPA cosine、UTMOS / SpeechBERTScore、DNSMOS、F0 RMSE / duration MAE、情感 top-1、时长、延迟 / RTF / QPS |
| 主观评测 | 按 VoiceMOS Challenge（`arXiv:2203.11389`）：≥20 听者、隐藏锚点、重复项、95% 置信区间、CMOS CI 不跨零 |
| 门禁流程 | checkpoint → golden_set 全量合成 → 客观计算 → Q1–Q10 逐项比对 → 硬指标阻断 / 软指标评审 → 门禁报告 `gs-YYYY-MM-x` |
| 参数扫描 Harness | 每开放参数 5 点 × 20 条固定文本、固定 seed；ρ 单调性 + 说话人漂移 + UTMOS 下降 + CER 上升；**未过者不开放给业务**（F3 正式验收） |
| 阈值校准 | D20：只能收紧，放宽须书面评审；`calibration.status` 与 `baseline_report` 一起回填 |
| 水印 | AudioSeal（`2401.17264`, ICML 2024, MIT）默认开；`E-LICENSE-001` 关闭需商业授权 |
| Phase 0 边界 | 上述门禁**均未接入真实合成**；eval-gate 当前只跑契约示例、阈值结构、一致性、单测 |

完整流程与报告模板见 [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md)；阈值真源 [thresholds.yaml](../configs/eval/thresholds.yaml)。

---

## 11. 服务化与部署实施

| 主题 | 结论 |
| --- | --- |
| 端点 | `POST /v1/presets/validate`（422）· `POST /v1/synthesize`（400 / streaming）· `GET /v1/presets/{id}` · `GET /v1/capabilities` · `GET /v1/health` |
| 响应信封 | `valid / errors[] / warnings[]`（[ERROR-CODES.md §2](voicespec/ERROR-CODES.md)）；`audit.*` 服务端只读 |
| 流式 | SSE / chunk（`render.chunk_ms` 默认 200）；跨 chunk 韵律连续、exact 时长全局预算（R-08）；首包目标见 thresholds.yaml Q7 |
| 鉴权 | `E-LICENSE-002` 说话人注册鉴权；`E-LICENSE-001` 水印默认 true、关闭需商业授权 |
| 降级与监控 | 能力不支持报错不静默降级；`audit.degraded` 全链路；1000 句压测 0 异常 |
| 交付（D21） | 本地权重 + 私有 API（Docker），不入公有云托管；模型卡 + 回滚手册 |
| 回滚 | checkpoint 双命名 + Top-K + 门禁报告绑定；越界即回滚到上一 `gs-*` 通过的产物 |

接口冻结草案 [API-SPEC](implement/control/API-SPEC.md)；部署与回滚 [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md)；签名占位 [src/serve/api.py](../src/serve/api.py)。

---

## 12. 合规与许可实施

### 12.1 权利结构（不得改写）

| 层 | 许可 | 说明 |
| --- | --- | --- |
| 项目自有增量（代码 / VoiceSpec 契约 / preset / 词典 / 标注 / golden_set / LoRA / adapter / 微调权重 / 模型卡 / 文档 / 音色资产） | **PolyForm Noncommercial 1.0.0**（[LICENSE](../LICENSE) 官方逐字原文）+ 双授权（[LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md)） | 禁商用；licensor 保留单独授予商业许可权（依据 `No Other Rights` 条款） |
| 上游 Apache-2.0 原权重 | 第三方**仍可按原条款商用** | Apache-2.0 §4 允许对修改与衍生作品整体附加不同条款，但须保留归因、不得剥夺第三方对上游原作权利；**NC 不覆盖上游** |
| 对外称谓 | **开放权重 / 源码可得（source-available, open-weight）** | **不称 OSI 开源**；OSD 第 6 条禁止按用途领域歧视 |

### 12.2 D11 法务定稿清单（P0 阻塞）

| # | 事项 | 产出 |
| --- | --- | --- |
| L-1 | 商业化边界 FAQ（什么算「商业使用」、MAU / 营收口径、内部研究例外） | `docs/legal/` 文档 |
| L-2 | 商业授权书面协议模板（范围 / 期限 / 费率 / 归因 / 终止） | `LICENSE-COMMERCIAL.md` 定稿 |
| L-3 | `NOTICE` 上游归因清单逐项签字 | [NOTICE](../NOTICE) 更新 |
| L-4 | 双授权条款与 PolyForm NC 兼容性复核 | 法务意见书 |
| L-5 | 模型卡许可字段模板（`base_license` / `weight_license` / `delta_license`） | 模型卡规范 |
| L-6 | 水印与「关闭水印需授权」的合规说明 | `E-LICENSE-001` 落地 |

### 12.3 R-14b 法务跟进清单（v0.3 §5.3.4 九项）

| # | 待跟进 | 现状 | 处理原则 |
| --- | --- | --- | --- |
| 1 | ESD 官方许可 | 官方页 404 / GitHub 404 / HF 401；第三方镜像矛盾（apache-2.0 / mit / 无 tag） | 书面询问或替换数据集 |
| 2 | CASIA 中文情感语料官方许可 | chineseldc.org 超时 / casia.cn SSL 失败；仅第三方镜像 apache-2.0 | 书面询问或替换 |
| 3 | Coqui CPML 全文 | `https://coqui.ai/cpml` 404（关站）；仅 `.models.json` 间接证据 `CPML, tos_required=true` | 不用其权重 |
| 4 | fishaudio 精确权重 ID | `fish-speech` / `OpenAudio-S1` 401/404；s2-pro 为 Research License | 不进候选 |
| 5 | RVC-Boss/GPT-SoVITS HF 权重卡 | org 下 0 模型、精确 ID 401；代码 MIT | 权重许可独立确认前不用 |
| 6 | charactr/vocos | GitHub 404 / HF 401（已迁 `gemelo-ai/vocos`，代码与权重 MIT） | 用迁移后 ID 复核 |
| 7 | IndexTTS-2 HF 权重约束 | HF 无 license tag，但 GitHub 有 bilibili Model Use License Agreement（1 亿 MAU / 10 亿 RMB 门槛、禁用于改进其他 AI 模型） | 法务确认 HF 权重是否受约束 |
| 8 | WenetSpeech 申请条款 | GitHub Apache-2.0，HF `gated=auto` 需申请 PASSWORD | 记录申请条款 |
| 9 | 论文会议归属 | 13 个 ID `journal_ref` 全空，仅 comment 自述 | 会议官网 / DBLP 二手核验，引用不写「已确认正式发表」 |

### 12.4 R-18 防线（v0.3 核验发现，本版继续生效）

**代码许可 ≠ 权重许可**：F5-TTS（代码 MIT / 权重 `cc-by-nc-4.0`）、fishaudio（Community v1.0 / `cc-by-nc-sa-4.0` 或 Research）、coqui（MPL-2.0 / CPML 或 `CC BY-NC-ND 4.0`）。矩阵已拆「代码许可 / 权重发行许可」两列；模型卡强制 `base_license` + `weight_license`；`license-check` CI 守住受保护路径。**轨道 A 三候选因代码与权重均 Apache-2.0 而保持干净**（ADR-0001 被强化）。

完整落地清单见 [LICENSING-IMPLEMENTATION-SPEC](implement/legal/LICENSING-IMPLEMENTATION-SPEC.md)。

---

## 13. 风险登记全表（R-01–R-24）

### 13.1 既有（R-01–R-18，状态沿用 v0.3）

| ID | 风险 | 状态 / 缓解 |
| --- | --- | --- |
| R-01 | 联网检索不可用致选型基于未核验信息 | **已解除**（v0.2 在线核验；web_fetch/web_search 不可达，走 pwsh + gh 通道） |
| R-02 | 数据授权不清 / 来源不明 | 授权书先行、manifest 强制 `license_id`、自有与公开物理隔离；G0-1 阻塞 |
| R-03 | 许可证不允许商用 | 一票否决；逐项核验 LICENSE 原文；ADR-0001 |
| R-04 | 可控性与自然度互相牺牲 | 5 点单调性 / 正交门禁；M2 优先于 DSP；不通过的参数不开放 |
| R-05 | 情感 / 时长控制致说话人漂移 | `speaker_lock` + 相似度门禁 + 音色/情感参考解耦 |
| R-06 | 灾难性遗忘 | 冻结底层、低 LR、replay、发音回归集 |
| R-07 | DPO 奖励黑客 | 人评盲测终裁；代理奖励不作上线依据 |
| R-08 | 流式 chunk 边界跳变 | 全局 duration 预算 + 跨 chunk 韵律连续专项测试 |
| R-09 | 上游版本漂移 / 复现失败 | 锁定 commit + 依赖锁 + Docker + 模型卡 |
| R-10 | 量化 / 蒸馏后质量越界 | Stage 3 后强制重跑全量门禁，越界回滚 |
| R-11 | 多音字 / 专名 / 长数字读错 | L-D 确定性规则 + 发音回归集，零容忍 |
| R-12 | 音色被滥用 | 白名单、水印、审计日志、权限隔离 |
| R-13 | 范围蔓延（歌唱 / VC / 多语种） | v0.1 §2.3 排除项，新增需求走 v0.5 变更评审 |
| R-14 | 部分权重 / 数据集许可 | **分项核验、边界收窄但未清零**；`[OK]` 回填矩阵，`[MISS]` 降级 R-14b（§12.3） |
| R-15 / R-16 | 许可 / 合规相关 | 未改动；D11 仍是发布权重前阻塞项 |
| R-17 | 契约与实现漂移（C 层 18 码手写可能不一致） | 错误码只追加、单测覆盖每码、CI 对示例全量校验；v0.4 加 R-20 细化 |
| R-18 | **代码许可 ≠ 权重许可** | 矩阵拆两列 + 模型卡强制双许可字段 + license-check CI（§12.4） |

### 13.2 v0.4 新增（R-19–R-24）

| ID | 风险 | 触发信号 | 缓解（本版已落） |
| --- | --- | --- | --- |
| **R-19** | 规格文档与代码骨架**双份漂移**（文档说一套、`src/` 签名另一套） | 改规格未改签名 / 改签名未改文档 | [scripts/check_consistency.py](../scripts/check_consistency.py) 扫描链接与状态标记；[单测](../tests/unit/test_spec_consistency.py) 断言契约常量；规格与签名共用同一份字段表 |
| **R-20** | **错误码表 ↔ C 层实现漂移**（自造码 / 改义 / 漏实现） | 实现里出现表外 `E-*` / `W-*` | [ERROR-CODES.md](voicespec/ERROR-CODES.md) 为唯一真源；`check_consistency.py` (a) 比对规格与表的码集合；Phase 3 单测逐码覆盖；错误码只追加 |
| **R-21** | **preset 未过门禁被误标 production**（模板当业务配置上线） | `registry.production` 无 `gate_report` | D18：`production` 必须非空 `gate_report` + golden_set 通过 + 2 人批准；状态单向；Phase 0 `production: null`；`configs/presets/**` 走 PR + `Gate-Report:`/`Preset:` footer |
| **R-22** | **未校准阈值被当实测结论** | 文档 / 提交写「已达 / 实测 / 达标」 | 全库统一「目标值 / 待校准」；`calibration.status=uncalibrated`；`check_consistency.py` (e) 状态被提前改则 WARN；放宽须书面评审（D20） |
| **R-23** | **Q9 byte-level 可复现未落实** | 同 (preset, model, seed, text) 波形不一致 | 固定推理栈 + `locks/` 依赖锁 + Docker digest + seed + 模型卡；CI 波形 hash 比对（§9） |
| **R-24** | **模板占位值被误当真实配置**（`<...>` / `unselected` / `null` 被照抄上线） | template 文件无状态标记 | 所有 `*.template.yaml` 头部 `# 模板 / Phase 0 / 非实测 / 状态: template`；`check_consistency.py` (d) 扫描缺失并 WARN；registry `status` 字段区分三态 |

---

## 14. 里程碑、排期与收敛路线

### 14.1 三档排期（沿用 v0.1 §11.3，从 v1.0 冻结后起算）

| 档 | 周期 | 适用 | 本版立场 |
| --- | --- | --- | --- |
| A | 6–8 周 | 演示 / MVP | **不承诺**：全参数可控 + 高质量无法同时达标 |
| **B（基线）** | **16–20 周** | 高质量可用 | **推荐基线承诺** |
| C | 24–32 周 | 多音色矩阵 / 多语种 / 一体机 | 视 D3/D8/D10 结果升级 |

### 14.2 档 B 主线（P1–P6，前置门 G0）

| 阶段 | 周 | 交付物 | 准出 | 前置 |
| --- | --- | --- | --- | --- |
| **G0** | 冻结前 | D1–D11 拍板 + D11 法务签字 + R-14b 清零 + 算力到位 | v1.0 方案冻结 | §3.3 |
| P1 数据底座 | W2–W6 | 流水线、质检报告、精标数据、`ds-*` manifest、golden_set v1 | 全量过质检门禁；golden_set 冻结 | G0 |
| P2 基座复现 | W2–W6（并行） | 三候选 baseline、评分卡回填、capability_flags、阈值校准 | ADR-0002 回填；`calibration.status=calibrated` | G0 + Phase 1 切片 |
| P3 参数化控制层 v1 | W7–W11 | C 层 18 码实现、preset 注册、参数扫描器、开放参数清单 | F3/F5 通过；每开放参数过单调性 | P2 |
| P4 微调与偏好对齐 | W11–W17 | speaker adapter、DPO 产物、模型卡、全量门禁报告 | Q1/Q2/Q3 达标；Q9 可复现 | P1/P3 |
| P5 质量门禁与校准 | W14–W18 | golden_set 全量报告、`gs-*`、主观盲测报告 | 硬指标全过、软指标评审通过 | P4 |
| P6 服务化与流式 | W16–W20 | API、流式、监控、降级、回滚、水印 | Q7 达标；1000 句压测 0 异常 | P5 |

> P1 与 P2 并行是为了尽早拿到真实 baseline 分数——**没有基线分数的排期都是猜测**（v0.1 §11.2 原话，本版保留）。

### 14.3 版本收敛路线（D22 · 「再迭代几个版本就落地实施」的终点）

| 版本 | 准入 | 必做 | 准出（可判定） |
| --- | --- | --- | --- |
| **v0.4（本版）** | v0.3 已推送 + CI 全绿 | 规格全量、编号闭合、模板 / 骨架 / 校验器 / 单测、规范同步 | 三个 CI 全绿 + `check_consistency.py` 0 FAIL + 单测全过 |
| **v0.5** | v0.4 评审意见 | ① D1–D11 逐项拍板或标「暂缓 + D17」② D11 法务清单 L-1–L-6 回填 ③ R-14b 九项处理结论 ④ 规格评审回填 ⑤ 全库数字 / 引用交叉核对 | G0-1/2/3 有结论；无「待定编号」 |
| **v1.0（冻结）** | v0.5 无阻塞项 | ① 方案冻结声明 ② CHANGELOG 生成 ③ 受保护路径清单终版 ④ 实施准入单（算力 / 数据 / 法务 / 人力签字） | **G0 全过 → 可进入 P1** |
| **实施** | v1.0 冻结 | 按 §14.2 档 B 执行 | 每个 P 阶段按准出验收 |

> 收敛判据：v0.5 若仍有 D 未拍板但明确「暂缓 + D17」，不算阻塞；**只有 G0-2（D11 法务签字）、G0-3（R-14b 清零）、G0-4（算力到位）是硬阻塞**。

---

## 15. 实施规格文档索引

总索引与状态表见 [docs/implement/README.md](implement/README.md)。

| # | 文件 | 覆盖 | 对应章节 |
| --- | --- | --- | --- |
| 1 | [CONTROL-LAYER-SPEC](implement/control/CONTROL-LAYER-SPEC.md) | C 层函数签名、18 码逐码判定、能力探测、降级、单测组织 | §7 |
| 2 | [API-SPEC](implement/control/API-SPEC.md) | 5 端点、响应信封、HTTP 映射、流式、鉴权 / 水印 | §7 / §11 |
| 3 | [PRESET-REGISTRY-SPEC](implement/control/PRESET-REGISTRY-SPEC.md) | registry 结构、版本规则、默认值展开、生产准入 | §7.4 |
| 4 | [DATA-PIPELINE-SPEC](implement/data/DATA-PIPELINE-SPEC.md) | ①–⑧ 流水线、工具链许可、授权、防泄漏 | §8 |
| 5 | [DATASET-MANIFEST-SPEC](implement/data/DATASET-MANIFEST-SPEC.md) | manifest 字段 schema、golden_set 冻结与 CI hash | §8 |
| 6 | [TRAINING-SPEC](implement/train/TRAINING-SPEC.md) | 三阶段、命名、回滚、可复现、依赖锁 | §9 |
| 7 | [EVAL-GATE-SPEC](implement/eval/EVAL-GATE-SPEC.md) | 四套数据集、门禁流程、参数扫描 Harness、报告模板 | §10 |
| 8 | [DEPLOYMENT-SPEC](implement/serve/DEPLOYMENT-SPEC.md) | 部署形态、监控、降级、回滚、模型卡 | §11 |
| 9 | [LICENSING-IMPLEMENTATION-SPEC](implement/legal/LICENSING-IMPLEMENTATION-SPEC.md) | D11 清单、R-14b、模型卡许可字段、发布前检查 | §12 |

---

## 16. 配置 / 代码骨架索引

| 类别 | 文件 | 状态 |
| --- | --- | --- |
| 契约 | [voicespec.schema.json](../configs/voicespec/voicespec.schema.json) · [examples/minimal.json](../configs/voicespec/examples/minimal.json) · [examples/full_tuned.json](../configs/voicespec/examples/full_tuned.json) · [examples/duration_exact.json](../configs/voicespec/examples/duration_exact.json) | **已生效（v0.3，v0.4 不改）** |
| 阈值 | [thresholds.yaml](../configs/eval/thresholds.yaml) | `uncalibrated` |
| preset | [registry.yaml](../configs/presets/registry.yaml) · [warm_companion.template.yaml](../configs/presets/examples/warm_companion.template.yaml) | `template` |
| 训练 | [sft.template.yaml](../configs/train/sft.template.yaml) · [dpo.template.yaml](../configs/train/dpo.template.yaml) · [quantize.template.yaml](../configs/train/quantize.template.yaml) | `template` |
| 基座 | [base.template.yaml](../configs/base/base.template.yaml) | `template` / 三候选 `unselected` |
| 校验脚本 | [validate_voicespec.py](../scripts/validate_voicespec.py) · [check_consistency.py](../scripts/check_consistency.py) · [requirements.txt](../scripts/requirements.txt) | 前者生效；后者新增 |
| 单测 | [test_spec_consistency.py](../tests/unit/test_spec_consistency.py) · [test_skeleton_contract.py](../tests/unit/test_skeleton_contract.py) · [tests/unit/\_\_init\_\_.py](../tests/unit/__init__.py) | 新增，可跑（13 个测试全绿） |
| 代码骨架 | [src/control/validator.py](../src/control/validator.py) · [src/control/\_\_init\_\_.py](../src/control/__init__.py) · [src/serve/api.py](../src/serve/api.py) · [src/serve/\_\_init\_\_.py](../src/serve/__init__.py) · `src/{frontend,models,train,eval,data}/__init__.py` | 签名占位 / `NotImplementedError` |
| 规范 | [COMMIT_CONVENTION.md](../COMMIT_CONVENTION.md) · [CONTRIBUTING.md](../CONTRIBUTING.md) · [CODEOWNERS](../CODEOWNERS) · [.commitlintrc.yml](../.commitlintrc.yml) · [.gitignore](../.gitignore) | 同步更新 |
| CI | [eval-gate.yml](../.github/workflows/eval-gate.yml) · [commitlint.yml](../.github/workflows/commitlint.yml) · [license-check.yml](../.github/workflows/license-check.yml) | eval-gate 加一致性 + 单测 |

---

## 17. 变更规范与 CI 同步（v0.4）

| 变更 | 内容 |
| --- | --- |
| `COMMIT_CONVENTION.md` §5 | 新增 `Impl:` footer（改 `docs/implement/**`、`src/**`、`configs/base/**`、`configs/train/**`、`scripts/check_consistency.py`、`tests/unit/**` 时必填），格式 `Impl: implement-spec@0.4` |
| `CODEOWNERS` | 新增 `docs/implement/`、`configs/presets/`、`configs/train/`、`configs/base/`、`scripts/check_consistency.py`、`tests/unit/`、`src/**` 受保护 |
| `eval-gate.yml` | 新增两步：`python scripts/check_consistency.py --repo-root .` 与 `python -m unittest discover -s tests/unit -v`；触发路径补 `docs/implement/**`、`configs/**`、`src/**`、`tests/**`、`scripts/check_consistency.py` |
| `README` / `CONTRIBUTING` | 当前方案指向 v0.4；文档索引补九份实施规格、模板与骨架、本地校验命令 |
| `CHANGELOG` | 追加 `v0.4.0` 条目 |
| `commitlint.yml` | PR 的 required-footers 增加 `Impl:` 触发规则（push 分支不受影响） |
| `.commitlintrc.yml` | `scope-enum` 新增 `implement`（v0.4 规格与骨架批次的作用域） |

> 提交 footer 规则仍以 [COMMIT_CONVENTION.md](../COMMIT_CONVENTION.md) 为准；`license-check.yml` 本版**未改**（未动 LICENSE / NOTICE / LICENSE-COMMERCIAL.md）。

---

## 18. 术语表

| 术语 | 含义 |
| --- | --- |
| VoiceSpec | 参数化语音合成契约，五层解耦 + audit，机器可执行 |
| S 层 / C 层 | Schema 静态校验 / Control 语义校验 |
| preset | 默认值集合（不是强制值），版本化、需门禁报告才能进 production |
| golden_set | 冻结回归集，所有上线门禁基于它，PR 禁止修改 |
| M1–M6 | 控制手段编号；优先级 `M4>M2>M1>M5>M3>M6` |
| capability flag | 基座能力位（exact_duration / f0_contour / attribute_control / style_prompt / voice_blend），Phase 2 实测回填 |
| 开放权重 / source-available | 源码与权重可得但禁商用的对外称谓；**不是 OSI 开源** |
| R-18 | 代码许可 ≠ 权重许可（v0.3 核验发现） |
| G0 | 落地实施硬前置门（§3.3） |
| provisional | D17 临时默认建议，非承诺、拍板即覆盖 |
| `gs-YYYY-MM-x` | 门禁报告 ID 格式，preset production 准入凭据 |

---

## 19. 附录

### 19.1 文件索引（本版新增）

- 主方案：[v0.4（本文件）](AI智能体声音训练项目_技术栈方案_v0.4.md) · [v0.3](AI智能体声音训练项目_技术栈方案_v0.3.md) · [v0.2](AI智能体声音训练项目_技术栈方案_v0.2.md) · [v0.1](AI智能体声音训练项目_技术栈方案_v0.1.md)
- 决策：[ADR-0001](decisions/ADR-0001.md) · [ADR-0002](decisions/ADR-0002.md) · [ADR-0003](decisions/ADR-0003.md) · [ADR-0004](decisions/ADR-0004.md) · [决策表 D1–D11](decisions/DECISION-SHEET.md)
- 契约：[schema](../configs/voicespec/voicespec.schema.json) · [ERROR-CODES](voicespec/ERROR-CODES.md) · [README](voicespec/README.md)
- 许可：[LICENSE](../LICENSE) · [NOTICE](../NOTICE) · [LICENSE-COMMERCIAL](../LICENSE-COMMERCIAL.md) · [许可证矩阵](licensing/UPSTREAM-LICENSE-MATRIX.md)
- 论文：[PAPERS.md](references/PAPERS.md)
- 实施规格：[总索引](implement/README.md) + §15 九份
- 配置 / 骨架：§16

### 19.2 核验状态（2026-11-04）

| 项 | 状态 |
| --- | --- |
| web_fetch / web_search | **不可达**（`resolves to a non-public IP address`）；联网核验走 pwsh + `gh` / arXiv Atom API / HF API / OpenSLR 原文 |
| 论文清单 | v0.3 补录至 **58 篇**；13 个 ID `journal_ref` 全空 → 会议归属降级为 arXiv comment 自述 |
| 许可核验 | R-14 分项核验完成但**未清零**；`[MISS]` 降级 R-14b 九项（§12.3） |
| `leak_guard` | 发布前必跑；本版推送前再次扫描 |
| 远端 CI | `commitlint` / `license-check` / `eval-gate` 三个工作流每次 push 校验 |

### 19.3 v0.5 待办（不依赖本轮评审结论）

1. D1–D11 逐项拍板（或标「暂缓 + D17」），回填 §5.1 状态列。
2. D11 法务清单 L-1–L-6 定稿，`NOTICE` 归因清单签字。
3. R-14b 九项处理结论（书面询问 / 替换方案 / 不采用）。
4. 九份实施规格的评审回填（尤其 C 层 18 码判定逻辑、manifest 必填字段、门禁报告模板）。
5. 全库数字 / 引用 / 链接交叉核对（`check_consistency.py` 0 FAIL）。
6. v1.0 冻结声明与实施准入单。

---

**文档结束 · v0.4 · 待评审**
> 四轮评审重点：§3 阶段门与 G0 是否认可、§5 D16–D22 是否拍板、§13 R-19–R-24 缓解是否足够、§14 收敛路线是否可接受、D11 法务阻塞项。
