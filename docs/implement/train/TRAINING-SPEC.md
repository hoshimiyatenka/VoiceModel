# 训练实施规格 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 本文件职责 | 三阶段训练（SFT → DPO → 量化/蒸馏）的可实施规格：阶段表、硬件档、偏好对齐与奖励黑客防线、可复现、准出与回滚 |

主方案相对链接：[`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md)；上游基线：[v0.1 §7 训练 / §8 评估 / §10 仓库结构](../../AI智能体声音训练项目_技术栈方案_v0.1.md)、[ADR-0003](../../decisions/ADR-0003.md)、[thresholds.yaml](../../../configs/eval/thresholds.yaml)、[许可证矩阵](../../licensing/UPSTREAM-LICENSE-MATRIX.md)、[PAPERS.md](../../references/PAPERS.md)、[DATA-PIPELINE-SPEC.md](../data/DATA-PIPELINE-SPEC.md)、[DATASET-MANIFEST-SPEC.md](../data/DATASET-MANIFEST-SPEC.md)。

> 全项目仍 **Phase 0**：**无训练代码运行、无训练产出、无权重、无实测指标**。本文件为**实施规格模板**，不是运行记录；训练入口骨架由 code-skeleton 成员提供。所有数值均为**目标值 / 待校准**，引用写「见 thresholds.yaml」，不写成「已达 / 实测 / 已上线 / 已选定」。

## 1. 范围与硬约束

- 需求编号固定沿用 v0.1 的 **F1–F8 / Q1–Q10**，不新增不改义。
- 阈值单一真源 [`configs/eval/thresholds.yaml`](../../../configs/eval/thresholds.yaml)（`calibration.status=uncalibrated`）；门禁阈值不在本文、不在代码硬编码。
- 轨道 A 基座候选 **CosyVoice 2 / Qwen3-TTS / VoxCPM2**（代码与权重均 Apache-2.0，已核验见 [许可证矩阵 §2](../../licensing/UPSTREAM-LICENSE-MATRIX.md)），**Phase 2 同台实测定型，不写「已选定」**。轨道 B 为 LoRA 定制轨（LoRA `arXiv:2106.09685`）。
- 许可口径：对外称「**开放权重 / 源码可得(source-available, open-weight)**」，**不称 OSI 开源**；项目自有增量为 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游原作。
- **R-18（代码许可 ≠ 权重许可）** 已确认：训练数据表必须分别登记「代码 / 标注 / 语料 / 权重」许可来源（见 [DATASET-MANIFEST-SPEC.md §2.1](../data/DATASET-MANIFEST-SPEC.md)；EmoV-DB 仅非商用、ESD / CASIA `[MISS]` 列为 R-14b 法务跟进，不得假定可商用）。
- 四套数据集职责分离：train / val / test / **golden_set（绝对冻结，PR 禁止修改，CI 校验 hash）**；`datasets/golden_set/manifest.yaml` 是唯一允许入库的 golden_set 文件。
- 决策 D1–D15 既定，v0.4 新增 **D16–D22 由 Lead 编号**（本文只引用「按主方案 D17 默认建议」，不发明新 D 号）；风险 R-01–R-18 既定，新增 **R-19–R-24 由 Lead 编号**（本文只引用 R-06 / R-07 / R-10 / R-11 / R-23 等既定或 Lead 分配的号）；ADR-0004 由 Lead 写，本文不新建 ADR。

## 2. 三阶段训练规格

训练链：`Stage 1 SFT/适配 → Stage 2 偏好对齐(DPO) → Stage 3 蒸馏/量化/部署化`。阶段间门禁见 §5，回滚点见 §6。

| 阶段 | 目标(对应 Q) | 数据 | 超参文件 | 产物命名 | 准入 | 准出(门禁) | 回滚点 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Stage 1 · SFT / 适配**（基座权重冻结或半冻结 → LoRA 注入 → 授权数据微调） | Q1 可懂度、Q2 说话人相似度（目标值见 thresholds.yaml，待校准） | train（自有授权，[DATA-PIPELINE-SPEC.md](../data/DATA-PIPELINE-SPEC.md) DP-01..08 产物）+ 通用语料 replay（比例目标值见 v0.1 §7.3，待校准）；val 早停 | [`configs/train/sft.yaml`](../../../configs/train/)（模板由 code-skeleton 落盘，本文仅引用路径） | `model-<base>-sft-<step>-<score>`（v0.1 §10） | D1 声音来源拍板 + 授权链齐全（R-02）；基座候选已锁定 commit 与依赖锁；golden_set 已冻结 | 首次**全量门禁报告**：Q1/Q2 硬指标、Q8 稳定、Q9 可复现、R-11 发音回归集零容忍；阈值见 thresholds.yaml（待校准） | 上一 production 基座 + 上一 `model-*-sft-*` |
| **Stage 2 · 偏好对齐 DPO / RLAIF**（`arXiv:2305.18290`） | Q3 自然度、F3/F4 参数遵循度（目标值见 thresholds.yaml，待校准） | 同一文本多采样 → 代理奖励打分 → 构造 `(chosen, rejected)` 偏好对（见 §3）；val 早停 | [`configs/train/dpo.yaml`](../../../configs/train/)（模板由 code-skeleton 落盘） | `model-<base>-dpo-<step>-<score>` | Stage 1 全量门禁通过；盲测协议就绪（§3） | 全量门禁重跑 + **主观盲测为最终裁判**（R-07）；代理奖励**不作上线依据** | Stage 1 最优 `model-*-sft-*` |
| **Stage 3 · 蒸馏 / 量化 / 部署化**（FP16/bf16 → INT8/INT4 若支持、流式 chunk 适配、热加载） | Q7 延迟与成本，且不越过 Q1–Q4 门禁（目标值见 thresholds.yaml，待校准） | 不新增训练语料；用 val / golden_set 做量化后重评 | [`configs/train/distill.yaml`](../../../configs/train/)（模板由 code-skeleton 落盘） | `model-<base>-distill-<step>-<score>` | Stage 2 门禁 + 盲测通过 | **量化/蒸馏后强制重跑全量门禁（R-10）**，任一 Q1–Q4 越界即回滚；流式专项（R-08 chunk 边界 F0 跳变） | Stage 2 最优 `model-*-dpo-*` |

### 2.1 checkpoint 工程规范（v0.1 §7.3）

- 命名：`model-<base>-<stage>-<step>-<score>`，按 **step + 门禁分数双命名**。
- 保留：只留 **Top-K（按 Q1–Q4 综合分）+ 最近 3 个**，其余归档到对象存储（不入库，见 [.gitignore](../../../.gitignore)）。
- 早停：以 val 集 UTMOS + 相似度为主，CER 为硬约束（CER 恶化即停）；阈值见 thresholds.yaml（待校准）。
- 每次运行必须关联 `dataset@version + code@commit + config@hash + 门禁报告`，否则结果不采纳；config hash 来自 `configs/train/*.yaml`。

## 3. DPO 阶段：偏好对、R-07 防线、盲测协议

### 3.1 偏好对构造

```
固定文本 + 固定 VoiceSpec（preset@version + seed）
   → 同一文本多采样 N 条候选（N 为待定超参，见 configs/train/dpo.yaml）
   → 代理奖励打分：reward = w1·UTMOS + w2·说话人相似度 + w3·(1-CER) + w4·情感/时长符合度
     （权重 w* 与指标版本须锁定并写进模型卡；版本清单见 thresholds.yaml metrics_sources）
   → 按 reward 排序取高/低构造 (chosen, rejected) 对
   → DPO 训练（arXiv:2305.18290）
```

- 采样必须用**固定 seed + 固定推理栈**，否则偏好对不可复现（违反 Q9）。
- 代理模型（UTMOS / ECAPA-TDNN / ASR / 情感分类器）版本锁定并写进模型卡，**不得用被评测模型自身组件做裁判**（v0.1 §8.2 反自证原则）。

### 3.2 R-07 奖励黑客防线

| 防线 | 规则 |
| --- | --- |
| 代理奖励不作上线依据 | reward 仅用于**构造偏好对**，绝不单独作为 Stage 2 准出条件 |
| 人评盲测为最终裁判 | 按 VoiceMOS Challenge `arXiv:2203.11389` 协议：评审 ≥ 20 人、样本 ≥ 40 条/轮、随机序、盲测、含隐藏锚点与重复项、报均值 + 95% CI、CMOS 差值 CI 不跨 0 才判胜出（v0.1 §8.3；配置见 thresholds.yaml `subjective`） |
| 方向一致性检查 | 若代理指标上升但盲测 CMOS 下降/持平，判定为奖励黑客，**回滚到 Stage 1**，并记录 R-07 |
| 频率 | Stage 1/2/3 各一轮、上线前一轮（v0.1 §8.3） |
| 记录 | 原始评分表归档，禁止只留平均分；代理分数与盲测分数并列留痕 |

> DPO 论文依据 `arXiv:2305.18290`（[PAPERS.md](../../references/PAPERS.md) L-0 偏好对齐）；盲测协议 `arXiv:2203.11389`。二者发表状态按 v0.3 降级规则理解（journal_ref 空时仅 comment 自述）。

## 4. 硬件档与 D6 / D17

| 档 | 配置 | 适用 | 约束 |
| --- | --- | --- | --- |
| H-1 起步 | 1× 24GB GPU（3090/4090/A10 级） | Phase 0–3，LoRA、推理、评测 | 无法做全量 SFT / 大 batch |
| H-2 推荐 | 1× 80GB（A100/H100）或 4–8× 24GB | 档 B 全流程，含偏好对齐 | 成本与排期平衡点 |
| H-3 规模化 | 8× 80GB + 高速互联 + 对象存储 | 档 C、全量 SFT、多音色矩阵 | 仅在有明确规模需求时上 |

- **D6（算力预算与硬件）未拍板**：三档是候选，不写「已选定」。
- **默认建议见主方案 D17 默认建议**（编号由 Lead 统一分配，本文不展开、不发明新 D 号）。D1（声音来源）同为训练准入前置，阻塞关系见 [DATA-PIPELINE-SPEC.md §5](../data/DATA-PIPELINE-SPEC.md)。
- 存储：原始音频 + 中间产物 + checkpoint，按 v0.1 §7.1 目标规模规划（待校准，随数据量与保留策略变化）。

## 5. 防退化与专项门禁（R-06 / R-11 / R-10）

| 风险 | 落地规则 |
| --- | --- |
| **R-06 灾难性遗忘**（口齿、中英混退化） | 冻结底层 / 低 LR；通用语料 replay（比例目标值见 v0.1 §7.3，待校准）；监控「静音/吞字/复读」专项集；每个 checkpoint 跑固定发音回归集 |
| **R-11 多音字 / 专名 / 长数字读错** | L-D 确定性规则（[ADR-0003](../../decisions/ADR-0003.md) 的 `LinguisticSpec`）+ 发音回归集，**零容忍**：回归集任一例失败即阻断准出；发音词典落 [`dicts/`](../../../dicts/) |
| **R-10 量化/蒸馏后质量越界** | Stage 3 后**强制重跑全量门禁**（Q1–Q4 硬指标 + Q8/Q9/Q10），任一越界即回滚到 Stage 2 最优产物（§2 回滚点） |
| R-08 流式 chunk 边界 F0 跳变 | Stage 3 流式专项听审，不通过不部署（v0.1 §9.2） |

## 6. Q9 byte-level 可复现（R-23）

固定「推理栈 + 依赖锁 + Docker + seed + 模型卡」五件套，缺一不可：

| 要素 | 落地 |
| --- | --- |
| 推理栈 | 锁 CUDA / cuDNN / torch 版本（版本写入 `locks/`，[.gitignore](../../../.gitignore) 保留 `.dvc/config` 与 `*.dvc`，依赖锁文件入库） |
| 依赖锁 | `locks/` 下推理/训练分离锁文件，禁止散落脚本（v0.1 §7.3、§10） |
| Docker | 训练镜像 Docker 化，镜像 digest 关联每次运行 |
| seed | 固定 seed；同 `(preset, 模型版本, seed, 文本)` → 波形 byte-level 一致（Q9） |
| 模型卡 | `docs/model-cards/` 每上线模型一份，含 `base_license`（权重许可）、代理模型版本、config hash、门禁报告 ID（R-18 缓解） |

> **R-23 由 Lead 编号**（可复现链路risk），本文只引用，不新增编号。复现目标值见 thresholds.yaml（`waveform_reproducible`，待校准）。

## 7. 实验跟踪与仓库边界

| 项 | 规则 |
| --- | --- |
| 跟踪系统 | MLflow 自托管（v0.1 §4.4） |
| 原始日志 | 进 MLflow / 对象存储，**不入库**（`experiments/runs/`、`mlruns/` 已在 [.gitignore](../../../.gitignore) 忽略） |
| 仓库留存 | `experiments/` 只留**摘要**（关联 `dataset@version + code@commit + config@hash + 门禁报告`） |
| 超参 | 全部写进 [`configs/train/*.yaml`](../../../configs/train/)（模板由 code-skeleton 成员落盘，本文仅引用路径），禁止散落在脚本 |
| 门禁报告 | `docs/eval/` 报告模板；生成流程见 v0.1 §8.4，阈值见 thresholds.yaml |

## 8. 准出与回滚总则

```
任意变更（数据 / 代码 / 超参 / checkpoint / preset / 依赖）
   → golden_set 全量合成（绝对冻结，CI 校验 hash）
   → 客观指标计算 → 与 Q1–Q10 逐项比对（阈值见 thresholds.yaml）
   → 参数扫描（连续参数 5 点，单调性 / 漂移目标值见 thresholds.yaml）
   → 生成门禁报告
   → 任一硬指标不通过 → 阻断，禁止进入人工评测
   → 硬指标通过 → 主观盲测（仅重大版本，arXiv:2203.11389 协议）
   → 通过 → 注册 candidate → 人工批准 → production
```

- 硬指标（阻断项）：Q1、Q2、Q4、Q8、Q9、Q10、F4 时长精度；软指标（需评审）：Q3、Q5、Q7（v0.1 §8.4）。
- 回滚：模型注册表保留上一 production 版本一键切回；preset 版本可单独回滚（v0.1 §9.3）。
- **Phase 0 声明**：以上流程当前**均未运行**，无门禁报告、无 candidate、无 production；本文件与 [`configs/train/*.yaml`](../../../configs/train/) 模板、训练入口骨架（code-skeleton 提供）共同构成「实施就绪」的规格层。

## 9. 交叉引用与未决项

| 引用 | 状态 |
| --- | --- |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md) | 本轮明确规划（Lead 编写），D16–D22 / R-19–R-24 / ADR-0004 由其统一编号 |
| [`docs/implement/data/DATA-PIPELINE-SPEC.md`](../data/DATA-PIPELINE-SPEC.md) · [`DATASET-MANIFEST-SPEC.md`](../data/DATASET-MANIFEST-SPEC.md) | 本轮产出 |
| [`configs/train/*.yaml`](../../../configs/train/) | 本轮由 code-skeleton 成员落盘的模板，本文仅引用路径 |
| [`configs/eval/thresholds.yaml`](../../../configs/eval/thresholds.yaml) | 已存在，`calibration.status=uncalibrated` |
| [`docs/decisions/ADR-0003.md`](../../decisions/ADR-0003.md) | 已存在（Accepted 契约层 / Phase 3 待实现） |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](../../licensing/UPSTREAM-LICENSE-MATRIX.md) · [`docs/references/PAPERS.md`](../../references/PAPERS.md) | 已存在（v0.3） |
| [`COMMIT_CONVENTION.md`](../../../COMMIT_CONVENTION.md) · [`.gitignore`](../../../.gitignore) | 已存在 |

> 未决：D1（声音来源）、D6（算力）未拍板；D17 默认建议见主方案；工具权重许可、ESD / CASIA 官方许可属 **R-14b** 法务跟进；轨道 A 三候选待 Phase 2 同台实测定型；所有阈值待校准。
