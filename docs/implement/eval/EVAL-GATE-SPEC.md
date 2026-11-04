# 评估门禁与参数扫描 Harness · 实施规格

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-IMPL-007 |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | [docs/AI智能体声音训练项目_技术栈方案_v0.4.md](../../AI智能体声音训练项目_技术栈方案_v0.4.md) §10 / §4.3 |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 定义四套数据集职责、Q1–Q10 门禁流程、参数扫描 Harness、阈值校准协议与门禁报告模板 |

> **Phase 0 声明**：本文件是规格，**不是实现**。`src/eval/` 当前为 `__init__.py` 占位；CI 里真实生效的只有阈值结构校验、契约示例校验、一致性检查与单测。golden_set 全量合成与 Q1–Q10 自动门禁从 Phase 2 接入。所有数值均为**目标值 / 待校准**，真源为 [configs/eval/thresholds.yaml](../../../configs/eval/thresholds.yaml)（`calibration.status=uncalibrated`）。

## 1. 职责与真源

| 真源 | 管什么 | 本规格如何引用 |
| --- | --- | --- |
| [thresholds.yaml](../../../configs/eval/thresholds.yaml) | Q1–Q10 全部阈值、参数扫描点配置、主观评测协议、指标来源 | 一律写「见 thresholds.yaml」，**本文件不复制任何阈值数字** |
| [ERROR-CODES.md](../../voicespec/ERROR-CODES.md) | 请求侧校验错误码 | 门禁不复用其码；门禁失败用 `gs-*` 报告 + Q 编号 |
| [PAPERS.md](../../references/PAPERS.md) | 指标论文依据 | 按 ID 引用，不写「已确认正式发表」 |
| [voicespec.schema.json](../../../configs/voicespec/voicespec.schema.json) | 合成输入契约 | 门禁调用合成时传合法 VoiceSpec（固定 seed） |

## 2. 四套数据集职责分离（v0.1 §8.1 / D20）

| 集 | 用途 | 可否改动 | 入库内容 |
| --- | --- | --- | --- |
| `train` | SFT / DPO 训练 | 可增，须重跑质检 | manifest（实体走 DVC） |
| `val` | 超参选择、早停 | 可增 | manifest |
| `test` | 阶段末独立评估（不用于调参） | 冻结到阶段末 | manifest |
| **golden_set** | **上线门禁 / 回归 / 参数扫描** | **绝对冻结，PR 禁止修改，CI 校验 hash** | 仅 `datasets/golden_set/manifest.yaml` |

### 2.1 golden_set 覆盖矩阵（构造规范，非实测）

| 维度 | 取值 |
| --- | --- |
| 情感 | 8 类（对应 `style.emotion` enum 子集）× 3 种语速 |
| 语言 | 中文 / 中英混 / 英文专名 |
| 发音难点 | 多音字 / 长数字 / 日期 / 专名（R-11 零容忍） |
| 句长 | 极短句 / 普通句 / 极长句 |
| 句式 | 陈述 / 疑问 / 感叹 |
| 韵律 | 停顿密集文本 / `pauses[]` 边界 / `duration_mode=exact` 用例 |
| 难例 | 100 条难例（历史失败样本回流，须记录来源报告 ID） |

### 2.2 防泄漏

- 按**说话人**去重 + 按**文本**去重；四份互不相交，切分脚本输出 hash 清单写进 manifest。
- 任何样本缺 `license_id` / 授权书引用 → 拒收（[DATASET-MANIFEST-SPEC](../data/DATASET-MANIFEST-SPEC.md)）。

## 3. 门禁流程（v0.1 §8.4 可实施化）

| 步 | 输入 | 处理 | 输出 | 失败 |
| --- | --- | --- | --- | --- |
| G-1 | checkpoint + `model_commit` + 依赖锁 + Docker digest | 拉起固定推理栈，`seed` 固定 | 可复现运行环境 | 环境 hash 不一致 → 阻断（Q9 / R-23） |
| G-2 | golden_set manifest（校验 hash） | **冻结集 hash 比对** | 通过 / 失败 | hash 不符 → 阻断并报警（D20） |
| G-3 | 全量 golden_set 文本 + 固定 VoiceSpec | 全量合成（每例固定 seed） | 音频实体（不入库，走对象存储） | 任一 crash / 空音频 / 乱码 → 阻断（Q8） |
| G-4 | 音频 + 固定评测模型版本 | 客观指标计算（§4） | 逐例 + 聚合指标 | 评测模型版本漂移 → 阻断（Q1 固定 ASR） |
| G-5 | 聚合指标 + thresholds.yaml | Q1–Q10 **逐项比对** | 门禁结果表 | 硬指标任一不过 → 阻断 |
| G-6 | 软指标不达标 / 新 preset | 人工盲测（§5） | MOS / CMOS 报告 | CMOS CI 跨零 → 退回 |
| G-7 | 全部通过 | 生成门禁报告 `gs-YYYY-MM-x` | `gate_report` ID | 报告缺字段 → 阻断 |
| G-8 | `gs-*` + 2 人批准 | 允许 preset 进 `production`（D18） | registry 更新 | 缺报告 → `E-PRESET-*` 类阻断 |

### 3.1 硬 / 软指标划分

| 类 | 指标 | 行为 |
| --- | --- | --- |
| **硬（自动阻断）** | Q1、Q2、Q4、Q6（启用 F4 时）、Q8、Q9、Q10 + 削波 / 空音频 | 任一不过立即失败，不进人工评测 |
| **软（需评审）** | Q3、Q5、Q7 | 不自动阻断；F3 验收后部分转硬（规则写 thresholds.yaml） |

> 分类本身以 thresholds.yaml 的 `hard` / `soft` 分组为真源；本表只描述行为，不复制数值。

## 4. 客观指标实现（Q1–Q10）

| 需求 | 指标 | 实现要点 | 论文依据 |
| --- | --- | --- | --- |
| Q1 | 中文 CER / 英文 WER | **固定 ASR 模型版本**回环，禁止用自家模型自证 | Whisper `2212.04356` / Paraformer `2206.08317` / FunASR `2305.11013` |
| Q2 | ECAPA-TDNN embedding cosine | 同参考下限 + 跨说话人上限双判 | `2005.07143`（INTERSPEECH 2020，comment 自述） |
| Q3 | UTMOS / SpeechBERTScore（代理）+ MOS（主观） | 代理仅辅助，主观为最终裁判 | UTMOS `2204.02152`、SpeechBERTScore `2401.16812` |
| Q4 | DNSMOS + 削波 / 爆音 / 拖尾 / 底噪检测 | 自动检测 + 听审双通道 | DNSMOS `2010.15258` |
| Q5 | 固定情感分类器 top-1 + 连续强度 Spearman ρ | 人评抽样校验分类器 | — |
| Q6 | 实测音频时长 vs `duration_ms` 目标 | 取绝对 / 相对误差较大者判定 | IndexTTS2 `2506.21619` |
| Q7 | 首包 P95 / RTF / 显存峰值 / 并发 QPS | 指定硬件下测量，硬件型号写进报告 | — |
| Q8 | 1000 句回归 | crash / 空音频 / 乱码 / 非静音异常计数 | — |
| Q9 | 波形 byte-level 一致 | 同 (preset, model, seed, text) 两次合成比对 hash | R-23 |
| Q10 | 单参数扫描漂移 | 见 §6 | v0.1 §5.6 |

## 5. 主观评测协议（VoiceMOS Challenge，`arXiv:2203.11389`）

| 项 | 要求（见 thresholds.yaml `subjective`） |
| --- | --- |
| 听者数 | ≥ 20 |
| 每轮样本 | ≥ 40 |
| 隐藏锚点 | 必须 |
| 重复项 | 必须（测听者一致性） |
| 报告置信区间 | 95% |
| CMOS | **CI 不得跨零**；与 UTMOS 方向不一致时以人评为终裁（R-07） |

> 盲测问卷、评分界面、随机化与反作弊细节在 `docs/eval/` 目录下后续补；本版只冻结协议参数与终裁规则。

## 6. 参数扫描 Harness（F3 正式验收方法，v0.1 §5.6）

### 6.1 扫描配置（真源 thresholds.yaml `param_scan`）

| 项 | 内容 |
| --- | --- |
| 点数 | 5 点（含默认值） |
| 每点文本 | 20 条固定文本（golden_set 子集，固定 seed） |
| 固定 seed | 见 `param_scan.fixed_seed` |
| 相邻档位「风格跳变」听审 | 3 人 |

### 6.2 判定逻辑（每个开放参数逐项）

| 检查 | 判定 | 不过的处置 |
| --- | --- | --- |
| 感知单调性 | 目标感知量与参数值 Spearman ρ ≥ 阈值 | **不开放给业务**，降级为内部实验参数或改离散档位 |
| 说话人不漂移 | ECAPA cosine 相对参考变化 ≤ 阈值（Q10） | 同上 |
| 音质不塌陷 | UTMOS 下降 ≤ 阈值 | 同上 |
| 可懂度不退化 | CER 上升 ≤ 阈值（百分点） | 同上 |
| 无风格跳变 | 3 人听审相邻档位无突兀跳变 | 收窄参数范围或改离散档位 |

### 6.3 Harness 输出

| 字段 | 说明 |
| --- | --- |
| `param_path` | 如 `prosody.rate`、`prosody.pitch_semitones` |
| `points[]` | 每点的实测 / 目标值、5 项检查的通过位 |
| `rho` / `cosine_drift` / `utmos_drop` / `cer_rise_pp` | 聚合结果 |
| `open_to_business` | bool；仅全过时 true |
| `report_id` | 关联 `gs-*` |

> **不得把未过扫描的参数写进 production preset**（联动 [PRESET-REGISTRY-SPEC](../control/PRESET-REGISTRY-SPEC.md) 与 `W-CAPABILITY-003`）。

## 7. 阈值校准协议（D20）

| 规则 | 内容 |
| --- | --- |
| 初始态 | `calibration.status = uncalibrated`；所有数字为**目标值** |
| 校准时机 | Phase 2 用 golden_set v1 拿到真实 baseline 后 |
| 方向 | **只能收紧**；放宽须书面说明理由并经评审 |
| 回填 | `calibration.status: calibrated` + `calibrated_at` + `baseline_report` 三者同时写 |
| 守卫 | [scripts/check_consistency.py](../../../scripts/check_consistency.py) 检查项 (e) 状态被提前改则 WARN；本版禁止改为 calibrated |
| 变更提交 | `eval(gates)` + `Gate-Report:` footer（[COMMIT_CONVENTION.md](../../../COMMIT_CONVENTION.md) §5） |

## 8. 门禁报告模板（`gs-YYYY-MM-x`）

| 字段 | 说明 |
| --- | --- |
| `report_id` | `^gs-[0-9]{4}-[0-9]{2}-[a-z]$`（与 `audit.golden_set_passed` 同格式） |
| `model_commit` / `checkpoint` | 产物标识 |
| `env` | 依赖锁 hash / Docker digest / 硬件型号 / 评测模型版本 |
| `golden_set_hash` | 冻结集 hash |
| `q_results` | Q1–Q10 逐项：目标值（引用 thresholds.yaml）、观测值、通过位、硬/软 |
| `hard_blocking` | 任一硬指标失败即 `false` |
| `subjective` | MOS / CMOS 报告 ID（若有） |
| `param_scan` | 开放参数清单 + 各报告 ID |
| `approved_by` | 2 人（D18） |
| `created_at` | 时间戳 |

> Phase 0 不出任何 `gs-*` 报告；`configs/presets/registry.yaml` 的 `gate_report` 全为 `null`（R-21 / D18）。

## 9. CI 接入现状（eval-gate.yml）

| 检查 | 本版状态 |
| --- | --- |
| thresholds.yaml 结构 | ✅ 真实生效 |
| VoiceSpec 三示例校验 | ✅ 真实生效（v0.3 起） |
| `check_consistency.py` | ✅ v0.4 新增 |
| `unittest discover -s tests/unit` | ✅ v0.4 新增 |
| golden_set 全量合成 / Q1–Q10 自动门禁 | ⏳ Phase 2 骨架，未接入 |

## 10. Phase 2/3 待办

1. 实现 `src/eval/` 指标适配器（固定评测模型版本 + hash 锁）。
2. golden_set v1 实体构造与冻结（[DATA-PIPELINE-SPEC](../data/DATA-PIPELINE-SPEC.md)）。
3. 参数扫描 Harness 可跑代码 + 报告生成器。
4. 门禁报告接入 preset registry 的 `gate_report` 校验。
5. 阈值校准回填（须附 `baseline_report`）。
