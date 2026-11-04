# 数据流水线实施规格 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 本文件职责 | 把 v0.1 §6 的 ①–⑧ 数据流水线落成可实施规格：逐步 IO / 工具 / 门禁 / 失败处理 / 幂等键、许可分层、采集阻塞、目录约定 |

主方案相对链接：[`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md)；上游基线：[v0.1 §6 数据工程](../../AI智能体声音训练项目_技术栈方案_v0.1.md)、[许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md)、[thresholds.yaml](../../../configs/eval/thresholds.yaml)、[PAPERS.md](../../references/PAPERS.md)、[.gitignore](../../../.gitignore)。

> 全项目仍 **Phase 0**：无训练产出、无权重、无实测指标。本文所有数值均为**目标值 / 待校准**，引用写「见 thresholds.yaml」，不写成「已达 / 实测 / 已上线 / 已选定」。本文件是**实施规格模板**，不是运行记录；流水线代码骨架由 code-skeleton 成员提供，本文只定义行为契约。

## 1. 范围与硬约束

- 需求编号固定沿用 v0.1 的 **F1–F8 / Q1–Q10**，不新增不改义。
- 阈值单一真源 [`configs/eval/thresholds.yaml`](../../../configs/eval/thresholds.yaml)（`calibration.status=uncalibrated`）；逐条数据质检目标值见 v0.1 §6.2，**Phase 2 校准前不得写成结论**，不在代码里硬编码。
- 许可口径：对外称「**开放权重 / 源码可得(source-available, open-weight)**」，**不称 OSI 开源**；项目自有增量为 PolyForm Noncommercial 1.0.0（禁商用）+ 双授权；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游原作（见 [许可证矩阵 §5](../../licensing/UPSTREAM-LICENSE-MATRIX.md)）。
- **R-18（代码许可 ≠ 权重许可）** 对数据集同样成立：语料 / 标注 / 代码 / 权重是四种不同权利客体，逐条 manifest 分别登记（见 §4）。
- 数据不入库：音频实体走 DVC / 对象存储，仓库只留 manifest（含 hash、授权 ID、质检分）。`datasets/raw/`、`datasets/processed/` 已在 [.gitignore](../../../.gitignore) 忽略。
- 四套数据集职责分离：**train / val / test / golden_set（绝对冻结，PR 禁止修改，CI 校验 hash）**；`datasets/golden_set/manifest.yaml` 是唯一允许入库的 golden_set 文件。

## 2. 逐步规格（①–⑧）

流水线总序：`① 采集/授权 → ② 预处理 → ③ 质检门禁 → ④ 转写与对齐 → ⑤ 标注 → ⑥ 切片与打包 → ⑦ 版本冻结 → ⑧ 划分`。每步必须可由上一步输出单独重跑（幂等，见「幂等键」列）。

| 步骤ID | 输入 | 处理 | 输出 | 工具/库（代码许可，已核验） | 质检门禁 | 失败处理 | 幂等键 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ① 采集/授权 `DP-01` | 授权书、录音棚素材 / 客户自带素材 / 公开数据集申请凭证 | 校验授权书、登记 `license_id` 与授权书引用、按说话人分目录归档原始档（目标 ≥48kHz/24bit 存档） | `datasets/raw/<source>/<speaker>/原始 wav` + 授权登记行 | 无第三方模型；文件归档 + hash 工具（项目自有代码） | 授权书齐全且 `license_id` 非空；**D1 未拍板前禁止执行本步**（见 §5） | 缺授权即拒收、隔离不进流水线；记 R-02 | `sha256(原始字节) + DP-01` |
| ② 预处理 `DP-02` | ① 的原始 wav | VAD、降噪、去混响、人声分离、说话人日志(diarization)、响度归一；保留原始档不覆盖 | `datasets/processed/<ds>/clean/` 单说话人干净片段 | 项目自有处理链；可选 SpeechBrain（**Apache-2.0**，见 [许可证矩阵 §3](../../licensing/UPSTREAM-LICENSE-MATRIX.md)）做 diarization/VAD | 单说话人概率、有效时长、非静音占比等目标值见 v0.1 §6.2（待校准）；禁止过度降噪造成「电音」 | 不达标重跑一次；仍不达标丢弃并保留拒绝原因，不进训练集 | `sample_id + DP-02 + tool_version` |
| ③ 质检门禁 `DP-03` | ② 的干净片段 | 逐条打分：SNR、削波率、静音比、DNSMOS/PESQ、时长分布、ASR 置信度、说话人一致性 | 每条 `quality_gate` 分数 + 通过/拒绝标记（写入后续 manifest） | DNSMOS `2010.15258`、UTMOS `2204.02152` 类代理；版本须锁定并写模型卡（反自证原则，v0.1 §8.2） | **逐条打分，不通过不进训练集**；指标目标值见 v0.1 §6.2、门禁阈值见 thresholds.yaml（均待校准） | 削波/非静音异常重切；SNR/DNSMOS 不达标降噪重跑或丢弃 | `sample_id + DP-03 + scorer_version` |
| ④ 转写与对齐 `DP-04` | ③ 通过的片段 | ASR 转写 → 人工校验 → **强制对齐（MFA / WhisperX）** → G2P，产出 text + 音素 + **字级时间戳** | 对齐标注（text / phoneme / char-level timestamp） | Whisper `openai/whisper` **MIT**（`2212.04356`）；WhisperX `m-bain/whisperX` **BSD-2-Clause**（`2303.00747`）；MFA `MontrealCorpusTools/Montreal-Forced-Aligner` **MIT**；FunASR `modelscope/FunASR` **MIT**（`2305.11013` / Paraformer `2206.08317`）；WeNet `wenet-e2e/wenet` **Apache-2.0**（`2102.01547`） | 人工校验 CER 目标 = 0（禁止未校验转写入训）；字级对齐误差目标值见 v0.1 §6.2（待校准） | 对齐误差超限用另一工具重对齐；仍超限丢弃该条 | `sample_id + DP-04 + asr_version + aligner_version` |
| ⑤ 标注 `DP-05` | ④ 的对齐标注 | 标情感、场景、语速档、语气、重读、发音例外（多音字/专名/中英混/长数字） | 结构化 label（供 L-C / L-D 与 golden_set 难例） | 标注平台（项目自有）；发音词典落 [`dicts/`](../../../dicts/) | 双人标注 + 一致性检验（Cohen κ 目标值见 v0.1 §6.1，待校准）；R-11 发音例外零容忍 | κ 不达标第三人仲裁；发音例外漏标退回补标 | `sample_id + DP-05 + annotation_round` |
| ⑥ 切片与打包 `DP-06` | ⑤ 的完整标注样本 | 按句 / 按静音切（目标 3–15s，v0.1 §6.1 目标值）、去头尾静音、打包为训练样本 | `datasets/processed/<ds>/samples/` 训练样本 + 索引 | 项目自有切片器；强制对齐时间戳来自 ④ | 时长分布、去头尾静音目标值见 v0.1 §6.2（待校准）；避免过长导致显存与注意力退化 | 超长重切；过短丢弃 | `sample_id + DP-06 + slice_policy_version` |
| ⑦ 版本冻结 `DP-07` | ⑥ 的样本集 | 生成 / 更新 manifest（hash、来源、授权 ID、质检分），DVC 指针冻结；回归集单独冻结 | `datasets/manifests/ds-YYYYMMDD-x.yaml` + `.dvc` 指针 | DVC / 对象存储（项目自有配置）；字段规范见 [DATASET-MANIFEST-SPEC.md](DATASET-MANIFEST-SPEC.md) | manifest 必填项齐全、`sha256` 与实体一致、`license_id` 非空；golden_set hash 单独登记 | 校验失败阻断冻结，不产生新 `dataset_id` | `dataset_id + DP-07 + content_hash` |
| ⑧ 划分 `DP-08` | ⑦ 冻结的数据集 | **按说话人 + 按文本双重去重**后划分 train / val / test / golden_set，四份不相交 | 四份 split 清单（写回 manifest.split） | 项目自有划分器；去重键 = `speaker_id + normalized_text` | 四集合两两交集必须为 0；golden_set 覆盖 8 类情感 × 3 种语速 × 中英混 × 多音字 × 长数字/日期 × 专名 × 极短/极长句 × 疑问/感叹 × 停顿密集文本（v0.1 §8.1） | 任一交集非空即阻断，回到 ⑦ 重建 manifest；泄漏记 R-02 | `dataset_id + DP-08 + dedup_hash` |

> 「工具/库」列标注的是**代码许可**（已核验，见 [许可证矩阵 §3](../../licensing/UPSTREAM-LICENSE-MATRIX.md)）。各工具**权重 / 模型卡许可未全部核验**，见 §3。

## 3. 为什么强制对齐是 M2 与 F4 的前提

- **M2 声学特征编辑**（ADR-0003 已确立为连续量首选）要在 decoder 前改 F0 / energy / **duration contour**。没有字级时间戳，就不知道每个字/音节的起止边界，无法把 `pitch_contour`、`emphasis`、`pauses`、`duration_*` 映射到具体声学帧；只能退化为全局缩放，失去「细调」意义。
- **F4 精确时长**（`duration_mode=exact`，Q6）要求实测时长与目标误差受控。字级时间戳提供基准时长分布，是全局 duration 预算分配、`Σpauses` 冲突判定（`E-CONFLICT-002`）、流式跨 chunk 时长不漂移的基础；无对齐则 exact 模式无参照系，`E-CAPABILITY-001` 的能力探测也无法判定。
- 因此 ④ 的对齐产物是 ⑥ 参数化样本与后续参数扫描 Harness 的**必需输入**，不可跳过、不可用句级粗时间戳替代。对齐误差目标值见 v0.1 §6.2（待校准）。

## 4. 工具链与数据集的许可分层（R-18 / R-14b）

### 4.1 工具链

| 层 | 已核验 | 未核验 / 风险 |
| --- | --- | --- |
| 工具**代码**许可 | Whisper MIT、WhisperX BSD-2-Clause、MFA MIT、FunASR MIT、WeNet Apache-2.0、SpeechBrain Apache-2.0、AudioSeal MIT（[许可证矩阵 §3](../../licensing/UPSTREAM-LICENSE-MATRIX.md)） | — |
| 工具**权重 / 模型卡**许可 | — | **未全部核验**：ASR / VAD / diarization / DNSMOS / UTMOS 等代理模型的权重发行许可与商用范围未逐项确认，列为 **R-14b** 法务跟进；上线前须逐项回填模型卡 `base_license`，不得按代码许可推断 |

> 明确标注：本文只确认**工具链代码许可**已核验；**各工具权重 / 模型卡许可未全部核验，列为 R-14b**。代理模型版本须锁定并写进模型卡（v0.1 §8.2 反自证原则）。

### 4.2 数据集四层权利客体（数据表必须区分）

| 数据集 | 语料许可 | 标注许可 | 代码许可 | 权重/发行许可 | 商用 | 依据 |
| --- | --- | --- | --- | --- | --- | --- |
| AISHELL-3 | **Apache-2.0**（OpenSLR 93） | 随语料 / 项目自有增量另记 | 项目自有增量 PolyForm NC 1.0.0 | 不涉及（语料集） | ✅ 可商用 | [许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md) |
| WenetSpeech | GitHub LICENSE **Apache-2.0**；HF `gated=auto` 需申请 | 随语料 / 项目自有增量另记 | WeNet **Apache-2.0** | 衍生 WenetSpeech4TTS **`cc-by-4.0`** | ✅ 需申请；申请条款待确认 | [许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md) |
| EmoV-DB | **仅非商用**（商用须联系 Prof. Sarah Ostadabbas） | 项目自有增量 PolyForm NC 1.0.0 | — | — | ❌ | [许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md)；与本项目 NC 定位一致，但不得用于任何商业授权产物 |
| ESD | **[MISS]** 官方许可未确认 | 项目自有增量另记 | — | — | 未定 | 第三方镜像矛盾（apache-2.0 / mit / 无 tag）；**R-14b** 法务跟进，官方确认前不得进入训练数据（连 manifest 都不建） |
| CASIA 中文情感语料 | **[MISS]** 官方许可未确认 | 项目自有增量另记 | — | — | 未定 | 官方页超时 / SSL 失败，仅第三方镜像标 apache-2.0（非官方）；**R-14b** |
| LibriTTS / VCTK / Common Voice | 本轮未核验 | — | — | — | 待定 | [许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md) 保留待办 |

> **原则**：公开数据仅用于「流水线验证 / 评测对照 / 通用能力」；专属音色训练数据必须自有授权，二者物理隔离（不同目录 + 不同 manifest 字段）。ESD / CASIA 在官方许可确认前不得建 manifest。

## 5. 采集阻塞关系（D1 → DP-01）

```
D1（声音来源：自录授权 / 采购授权 / 客户自带 / 合成生成）待拍板
        │  未拍板 → DP-01..DP-08 全部不得开始（授权路径、成本、合规口径均未定）
        ▼
D1 拍板 → 按主方案 D17 默认建议确定采集与授权基线
        ▼
授权书先行（R-02）→ 允许执行 DP-01 → 后续步骤按幂等键逐个放行
```

- **D1 未拍板前不得开始采集**：声音来源决定数据成本、周期与合规路径（v0.1 §15.2），也决定 §4 的 `license_id` 取值；未定即采集会造成授权链断裂与返工。
- **D17 默认建议：按主方案 D17 默认建议**（编号由 Lead 统一分配，本文不展开、不发明新 D 号）。
- 硬件档 H-1/H-2/H-3 与 D6 的关系见 [TRAINING-SPEC.md](../train/TRAINING-SPEC.md)，默认建议同样见主方案 D17。
- 任一环节出现来源不明 / 授权书缺失样本，立即隔离，记 **R-02**，不进入下游。

## 6. 数据授权与物理隔离（R-02）

| 规则 | 落地 |
| --- | --- |
| 每条样本必须带 `license_id` | manifest 必填字段，见 [DATASET-MANIFEST-SPEC.md](DATASET-MANIFEST-SPEC.md)；缺字段即阻断 ⑦ 冻结 |
| 每条样本必须带授权书引用 | manifest `source_uri` / 授权书引用字段，指向授权凭证（不入库，走受控存储） |
| 自有数据与公开数据物理隔离 | 不同目录（`datasets/raw/<source>/`）+ 不同 manifest 字段 + 不同 `license_id` 命名空间；禁止混合打包 |
| 特殊数据 | EmoV-DB 仅非商用；ESD / CASIA `[MISS]` 在 R-14b 跟进前不建 manifest；WenetSpeech 的 HF `gated=auto` 申请条款与 PASSWORD 条件待确认 |

## 7. 输出目录约定

| 路径 | 内容 | 入库 |
| --- | --- | --- |
| `datasets/manifests/*.yaml` | 数据集 manifest（hash、授权 ID、质检分、split），字段规范见 [DATASET-MANIFEST-SPEC.md](DATASET-MANIFEST-SPEC.md) | ✅ 入库（受 `Dataset:` footer 约束） |
| `datasets/golden_set/manifest.yaml` | golden_set 冻结 hash 与元信息，**唯一允许入库的 golden_set 文件** | ✅ 入库（绝对冻结，PR 禁止修改） |
| `datasets/raw/` | 原始音频实体（① 产物） | ❌ [.gitignore](../../../.gitignore) 已忽略，走 DVC / 对象存储 |
| `datasets/processed/` | ②–⑥ 中间产物（clean / samples / 对齐标注） | ❌ [.gitignore](../../../.gitignore) 已忽略，走 DVC / 对象存储 |
| `datasets/golden_set/`（除 manifest） | 实体音频与难例 | ❌ 不入库，走 DVC / 对象存储 |

## 8. 交叉引用与未决项

| 引用 | 状态 |
| --- | --- |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md) | 本轮明确规划（Lead 编写），D16–D22 / R-19–R-24 / ADR-0004 由其统一编号 |
| [`docs/implement/data/DATASET-MANIFEST-SPEC.md`](DATASET-MANIFEST-SPEC.md) | 本轮产出 |
| [`docs/implement/train/TRAINING-SPEC.md`](../train/TRAINING-SPEC.md) | 本轮产出 |
| [`configs/eval/thresholds.yaml`](../../../configs/eval/thresholds.yaml) | 已存在，`calibration.status=uncalibrated` |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](../../licensing/UPSTREAM-LICENSE-MATRIX.md) | 已存在（v0.3） |
| [`docs/references/PAPERS.md`](../../references/PAPERS.md) | 已存在（v0.3，58 篇） |
| [`configs/train/*.yaml`](../../../configs/train/) | 本轮由 code-skeleton 成员落盘的模板，本文仅引用路径 |
| D1 / D6 / D17、R-14b / R-02 / R-11 / R-18 | 编号既定或由 Lead 分配，本文不新增 |

> 未决：D1 未拍板（阻塞 §5）；工具权重许可、ESD / CASIA 官方许可、Coqui CPML 全文等属 **R-14b** 法务跟进；所有阈值待 Phase 2 校准。
