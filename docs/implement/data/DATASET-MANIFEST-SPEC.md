# 数据集 Manifest 字段规范 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | docs/AI智能体声音训练项目_技术栈方案_v0.4.md |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 本文件职责 | 定义 `datasets/manifests/*.yaml` 与 `datasets/golden_set/manifest.yaml` 的完整字段 schema、示例（占位）、golden_set 生成/冻结/校验流程 |

主方案相对链接：[`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md)；关联：[DATA-PIPELINE-SPEC.md](DATA-PIPELINE-SPEC.md)、[许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md)、[thresholds.yaml](../../../configs/eval/thresholds.yaml)、[.gitignore](../../../.gitignore)、[v0.1 §10 仓库结构](../../AI智能体声音训练项目_技术栈方案_v0.1.md)。

> 全项目仍 **Phase 0**：无训练产出、无权重、无实测指标。本文是**字段规范与流程模板**，不是已冻结数据记录。所有示例数值用 `<...>` 或 `0`，明确标注「非实测」。阈值引用写「见 thresholds.yaml」，不在本文硬编码，不写成结论。

## 1. 定位与硬约束

- manifest 是数据实体的**唯一入库形态**：音频实体走 DVC / 对象存储，仓库只留 manifest（含 hash、授权 ID、质检分），见 [.gitignore](../../../.gitignore) 与 [v0.1 §10](../../AI智能体声音训练项目_技术栈方案_v0.1.md)。
- `dataset_id` 命名沿用 v0.1 §10：`ds-YYYYMMDD-x`。
- 许可分层（**R-18 代码许可 ≠ 权重/语料许可**）：manifest 必须分别记录语料 `license_id` 与项目自有增量（PolyForm Noncommercial 1.0.0 禁商用 + 双授权）；上游 Apache-2.0 原权重第三方仍可按原条款商用，NC 不覆盖上游原作。对外称「开放权重 / 源码可得(source-available, open-weight)」，**不称 OSI 开源**。
- 数据集四层权利客体（语料 / 标注 / 代码 / 权重）分别登记，见 [DATA-PIPELINE-SPEC.md §4](DATA-PIPELINE-SPEC.md)。
- **ESD / CASIA 官方许可 `[MISS]`**，第三方镜像矛盾，列为 **R-14b** 法务跟进；官方确认前**不建 manifest**（连 manifest 都不建）。**EmoV-DB 仅非商用**，不得用于任何商业授权产物。
- 四套数据集职责分离：train / val / test / **golden_set（绝对冻结，PR 禁止修改，CI 校验 hash）**；`datasets/golden_set/manifest.yaml` 是唯一允许入库的 golden_set 文件。
- 需求编号 F1–F8 / Q1–Q10、决策 D1–D15（v0.4 新增 D16–D22 由 Lead 编号）、风险 R-01–R-18（新增 R-19–R-24 由 Lead 编号）均既定，本文不新增编号。

## 2. 字段 Schema（顶层）

| 字段 | 类型 | 必填 | 说明 | 校验规则 |
| --- | --- | --- | --- | --- |
| `dataset_id` | string | ✅ | 数据集唯一 ID | `^ds-[0-9]{8}-[a-z]$`（`ds-YYYYMMDD-x`）；全局唯一 |
| `version` | string | ✅ | manifest 语义版本 | `^[0-9]+\.[0-9]+\.[0-9]+$`；每次内容变更递增 |
| `spec_version` | string | ✅ | 本规范版本 | 常量 `0.4.0`；与校验器对齐 |
| `created_at` | string(date-time) | ✅ | 创建时间 | ISO 8601 |
| `created_by` | string | ✅ | 创建者标识 | 非空；写审计主体，不写凭据 |
| `approved_by` | string | ✅ | 批准者标识 | 非空；冻结前必须有人批准 |
| `license_id` | string | ✅ | 语料许可 ID（SPDX 或登记 ID） | 非空；禁止 `[MISS]` 数据集建 manifest；见 [许可证矩阵 §4](../../licensing/UPSTREAM-LICENSE-MATRIX.md) |
| `license_layers` | object | ✅ | 四层权利客体登记 | 见 §2.1；缺一层即阻断 |
| `source_uri` | string | ✅ | 语料来源 / 授权书引用 URI | `format: uri`；禁止内联二进制；指向受控存储，不入库 |
| `source_type` | string | ✅ | 来源类别 | 枚举 `self_recorded` / `purchased` / `customer` / `public` / `synthetic`（对应 D1 未拍板前的候选，不得假定） |
| `sha256` | string | ✅ | 冻结实体内容 hash | `^[a-f0-9]{64}$`；与 DVC / 对象存储实体一致，校验失败阻断冻结 |
| `speaker_count` | integer | ✅ | 说话人数 | `>= 1`；示例用 `0` 占位并标非实测 |
| `duration_hours` | number | ✅ | 有效时长（小时） | `>= 0`；示例用 `0` 占位并标非实测 |
| `sample_count` | integer | ✅ | 样本条数 | `>= 0`；示例用 `0` 占位并标非实测 |
| `quality_gate` | object | ✅ | 逐条质检汇总 | 见 §2.2；阈值见 thresholds.yaml（待校准），不在本文硬编码 |
| `split` | object | ✅ | 四套划分清单 | 见 §2.3；train/val/test/golden_set 两两交集为 0 |
| `golden_set` | object | 条件 | golden_set 冻结元信息 | 仅当本数据集含 golden_set 时必填；见 §2.4 |
| `toolchain` | array | ⬜ | 处理工具与版本 | 每项含 `name` / `version` / `code_license`；权重许可见 R-14b 跟进 |
| `notes` | string | ⬜ | 备注 | 可写「Phase 0 模板、非实测」 |

### 2.1 `license_layers`（四层权利客体，R-18）

| 字段 | 类型 | 必填 | 说明 | 校验规则 |
| --- | --- | --- | --- | --- |
| `corpus` | string | ✅ | 语料许可 | 与 `license_id` 一致；如 `apache-2.0` / `cc-by-4.0` / `noncommercial-only` / `[MISS]`（仅 R-14b 登记用，不得入 manifest 训练数据） |
| `annotation` | string | ✅ | 标注许可 | 项目自有增量 `PolyForm-Noncommercial-1.0.0` 或上游标注许可；须显式 |
| `code` | string | ✅ | 流水线代码许可 | 项目自有增量 `PolyForm-Noncommercial-1.0.0`（工具链代码许可另在 `toolchain` 记） |
| `weights` | string | ✅ | 权重/发行许可 | 语料集填 `not_applicable`；若数据集附带代理模型权重须填实际发行许可，未核验标 `pending-R-14b` |

### 2.2 `quality_gate` 子结构

| 字段 | 类型 | 必填 | 说明 | 校验规则 |
| --- | --- | --- | --- | --- |
| `status` | string | ✅ | 质检状态 | 枚举 `pending` / `passed` / `rejected`；Phase 0 模板用 `pending` |
| `thresholds_ref` | string | ✅ | 阈值单一真源引用 | 常量 `configs/eval/thresholds.yaml`；**禁止把数字写成结论、禁止硬编码** |
| `scorer_versions` | object | ✅ | 代理模型版本（反自证） | 键=指标名，值=模型版本；须锁定并写进模型卡（v0.1 §8.2） |
| `per_sample` | array | ⬜ | 逐条分数 | 每条含 `sample_id` / `scores` / `passed`；不通过不进训练集（[DATA-PIPELINE-SPEC.md §2 DP-03](DATA-PIPELINE-SPEC.md)） |
| `summary` | object | ⬜ | 汇总 | 仅统计，不替代逐条判定；示例标非实测 |

### 2.3 `split`（四套数据集）

| 字段 | 类型 | 必填 | 说明 | 校验规则 |
| --- | --- | --- | --- | --- |
| `train` | array[string] | ✅ | 训练样本 ID 列表 | 与 val/test/golden_set 无交 |
| `val` | array[string] | ✅ | 早停集（v0.1 §8.1，冻结） | 与其余三份无交 |
| `test` | array[string] | ✅ | 版本对比集（冻结） | 与其余三份无交 |
| `golden_set` | array[string] | ✅ | 上线门禁 / 回归 / 参数扫描（**绝对冻结**） | 与其余三份无交；hash 另记于 `golden_set` 节 |
| `dedup_key` | string | ✅ | 去重键 | 固定 `speaker_id + normalized_text`（[DATA-PIPELINE-SPEC.md §2 DP-08](DATA-PIPELINE-SPEC.md)） |
| `disjoint_verified` | boolean | ✅ | 两两不相交校验通过标记 | 必须为 `true` 才允许 ⑦ 冻结；示例用 `false` 占位并标非实测 |

### 2.4 `golden_set` 冻结元信息

| 字段 | 类型 | 必填 | 说明 | 校验规则 |
| --- | --- | --- | --- | --- |
| `frozen` | boolean | ✅ | 是否冻结 | 必须为 `true`；PR 禁止修改 |
| `frozen_hash` | string | ✅ | 冻结内容 hash | `^[a-f0-9]{64}$`；CI 校验，见 §4 |
| `manifest_path` | string | ✅ | 唯一入库文件 | 常量 `datasets/golden_set/manifest.yaml` |
| `coverage` | array[string] | ✅ | 覆盖维度 | 含 8 类情感 × 3 种语速 × 中英混 × 多音字 × 长数字/日期 × 专名 × 极短/极长句 × 疑问/感叹 × 停顿密集（v0.1 §8.1） |
| `hard_case_count` | integer | ✅ | 难例条数 | `>= 0`；示例用 `0` 占位并标非实测 |

## 3. 示例（占位 / 非实测）

> ⚠️ **以下为字段示例，数值全部用 `<...>` 或 `0`，明确「非实测」**。Phase 0 无真实数据集、无冻结实体、无 hash，禁止据此推断任何规模或指标。

```yaml
# 示例 / 占位 —— 非实测，Phase 0 模板
dataset_id: ds-20261104-a
version: 0.1.0
spec_version: 0.4.0
created_at: "2026-11-04T00:00:00+08:00"
created_by: "<creator-id>"
approved_by: "<approver-id>"
license_id: "<spdx-or-registered-id>"        # 如 apache-2.0；ESD/CASIA [MISS] 不得填
license_layers:
  corpus: "<spdx-or-registered-id>"
  annotation: "PolyForm-Noncommercial-1.0.0"  # 项目自有增量
  code: "PolyForm-Noncommercial-1.0.0"
  weights: "not_applicable"                  # 语料集不涉及权重
source_uri: "https://<controlled-storage>/<authorization-ref>"
source_type: "<self_recorded|purchased|customer|public|synthetic>"
sha256: "<64-hex-content-hash>"              # 占位，非实测
speaker_count: 0                             # 占位，非实测
duration_hours: 0                            # 占位，非实测
sample_count: 0                              # 占位，非实测
quality_gate:
  status: pending                            # Phase 0 模板，未质检
  thresholds_ref: configs/eval/thresholds.yaml
  scorer_versions: {}                        # 待锁定代理模型版本
  per_sample: []
  summary: {}                                # 非实测
split:
  train: []
  val: []
  test: []
  golden_set: []
  dedup_key: "speaker_id + normalized_text"
  disjoint_verified: false                   # 占位，非实测
golden_set:
  frozen: true
  frozen_hash: "<64-hex-frozen-hash>"        # 占位，非实测
  manifest_path: datasets/golden_set/manifest.yaml
  coverage: []
  hard_case_count: 0                          # 占位，非实测
toolchain: []
notes: "Phase 0 模板 / 字段示例 / 非实测"
```

## 4. `datasets/golden_set/manifest.yaml` 生成与冻结流程

```
DP-08 划分（按说话人 + 按文本双重去重，四份不相交）
   → 生成 golden_set 候选清单（含覆盖维度、难例）
   → 计算 frozen_hash = sha256(规范化清单 + 实体指针)
   → 写入 datasets/golden_set/manifest.yaml（唯一入库文件）
   → approved_by 签字 + golden_set.frozen=true
   → CODEOWNERS 保护 + CI 校验 hash
   → 冻结生效：此后任何 PR 修改该文件即失败
```

| 环节 | 规则 |
| --- | --- |
| 生成 | 由 ⑧ 划分产出；覆盖维度见 §2.4，规模目标见 v0.1 §8.1（待校准，不在本文写死） |
| 冻结 | `frozen=true` + `frozen_hash` 落盘；实体音频走 DVC / 对象存储，不入库 |
| CI 校验 | 见 §5：hash 不一致即失败 |
| 修改 | **绝对冻结，PR 禁止修改**；若确需变更，走新 `dataset_id` + 新 frozen_hash，旧版本留档，不得原地改 |

### 4.1 为何 PR 禁止修改 golden_set

- 它是**上线门禁 / 回归 / 参数扫描**的唯一基准（v0.1 §8.1、§8.4）：Q1–Q10 逐项比对、参数扫描 5 点单调性、1000 句回归都基于它。改一份样本，历史门禁报告与版本间对比即失去可比性，等于悄悄改了评分标准。
- 「保质量」要求**固定标准 + 每次变更都回归**；golden_set 可变则「回归」无意义，无法发现模型漂移。
- 防泄漏（R-02）：冻结后集合固定，避免为让某 checkpoint 过门禁而塞入/剔除样本（奖励作弊）。
- 配置即代码：CODEOWNERS + CI 校验 hash（v0.1 §10 第 5 条）把「不可改」变成机器可判定的硬约束，而非口头约定。

## 5. CI hash 校验（实施契约）

| 检查 | 行为 |
| --- | --- |
| 改动路径命中 `datasets/golden_set/`（含 `manifest.yaml`） | 与 `license-check.yml` 现有规则一致：**任何改动直接失败**（冻结集含新增/删除），见 [license-check.yml](../../../.github/workflows/license-check.yml) |
| 计算 manifest 内 `frozen_hash` 与实际规范化清单 + 实体指针 | 不一致即失败，阻断合并 |
| `split.disjoint_verified` | 非 `true` 阻断 ⑦ 冻结 |
| `quality_gate.thresholds_ref` | 必须指向 `configs/eval/thresholds.yaml`，阈值不在 manifest 硬编码 |
| `Dataset:` footer | manifest 变更须按 [COMMIT_CONVENTION.md](../../../COMMIT_CONVENTION.md) 附 `Dataset:` 声明 |

> 校验逻辑代码骨架由 code-skeleton 成员提供；本文只定义校验契约。阈值目标值见 thresholds.yaml，均 `calibration.status=uncalibrated`。

## 6. 交叉引用与未决项

| 引用 | 状态 |
| --- | --- |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.4.md`](../../AI智能体声音训练项目_技术栈方案_v0.4.md) | 本轮明确规划（Lead 编写） |
| [`DATA-PIPELINE-SPEC.md`](DATA-PIPELINE-SPEC.md) | 本轮产出 |
| [`docs/implement/train/TRAINING-SPEC.md`](../train/TRAINING-SPEC.md) | 本轮产出 |
| [`configs/eval/thresholds.yaml`](../../../configs/eval/thresholds.yaml) | 已存在，`calibration.status=uncalibrated` |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](../../licensing/UPSTREAM-LICENSE-MATRIX.md) | 已存在（v0.3） |
| [`.gitignore`](../../../.gitignore) / [`COMMIT_CONVENTION.md`](../../../COMMIT_CONVENTION.md) / [`license-check.yml`](../../../.github/workflows/license-check.yml) | 已存在 |
| [`configs/train/*.yaml`](../../../configs/train/) | 本轮由 code-skeleton 成员落盘的模板，本文仅引用路径 |

> 未决：D1 声音来源未拍板（阻塞 manifest 的 `source_type` / `license_id` 取值）；ESD / CASIA / 工具权重许可属 **R-14b** 法务跟进；所有阈值待 Phase 2 校准。
