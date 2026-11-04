# 提交规范（Commit Convention）

> 本文件是 VoiceModel 仓库**提交信息的唯一权威定义**。
> 所有提交（含 PR 标题，squash 场景）由 `.commitlintrc.yml` + `.github/workflows/commitlint.yml` 强制校验，不合规直接失败。
> 贡献流程见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 1. 基本格式

基于 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)，项目定制如下：

```
<type>(<scope>): <subject>

<body>

<footer>
```

| 部分 | 规则 |
| --- | --- |
| `type` | 必填，**必须**属于 §2 表中小写枚举 |
| `scope` | 必填，**必须**属于 §3 表中小写枚举；跨多模块用最贴切的一个，确实无法归类用 `docs` 或省略括号写 `chore: ...` |
| `subject` | 必填，≤ **72 字符**；中文或英文均可；**祈使句**（「新增/修复/移除」，不是「新增了」）；**不加句号**；不重复 type 含义 |
| 空行 | subject 与 body 之间、body 与 footer 之间必须有空行 |
| `body` | 推荐。写**为什么**（动机、依据、取舍），不是「改了什么」；每行 ≤ 100 字符；可多段。引用论文必须带 arXiv ID |
| `footer` | 按 §5 强制项填写；多条每行一条；`BREAKING CHANGE:` 必须大写且带说明 |

**示例（合规）**

```
feat(control): 新增 duration_mode=exact 与 rate 互斥校验

IndexTTS2 (arXiv:2506.21619) 把时长作为独立条件，若与 rate 同时给出会
产生两个互相冲突的时长来源。按冲突消解矩阵 5.5 改为显式 400 而非
静默覆盖，避免 preset 复现时出现不可预期的时长漂移。

Refs: #42
Gate-Report: gs-2026-11-a
```

```
license(notice): 补充 Qwen3-TTS 权重 apache-2.0 归因条目

上游权重许可证核验（2026-11-04，GitHub/HF API）后补全 NOTICE，避免分发时
遗漏 Apache-2.0 §4 要求的归因声明。

License-Review: <法务批准人>
Refs: VM-TECH-001 v0.2 §2.4
```

**示例（不合规）**

```
update stuff                          # 无 type/scope，subject 无信息
feat(control): 更新了代码。             # 非祈使句、有句号、无意义
feat(unknown): xxx                    # scope 不在枚举内
feat(control): 把阈值从 3 调到 3.5     # 缺 Gate-Report footer
license: 改许可                        # scope 必填且受保护路径需 License-Review
```

## 2. `type` 枚举（CI 校验，不得自造）

| type | 用途 | 版本影响 | 附加要求 |
| --- | --- | --- | --- |
| `feat` | 新能力 | minor | — |
| `fix` | 缺陷修复 | patch | 关联 issue |
| `docs` | 文档（方案、论文清单、模型卡、README） | — | — |
| `model` | 模型结构 / checkpoint / adapter 变更 | minor | 必须更新 `docs/model-cards/`；`Model:` footer |
| `voice` | 音色资产 / preset / 发音词典变更 | patch | `Gate-Report:` + `Preset:` footer |
| `data` | 数据流水线 / manifest / 数据集 | patch | `Dataset:` footer；`golden_set` 受保护 |
| `eval` | 指标实现 / 阈值 / 评测报告 | patch | 改阈值需评审 + `Gate-Report:` |
| `train` | 训练脚本 / 超参 / 实验配置 | patch | 关联实验 ID |
| `perf` | 推理性能优化 | patch | 附前后 RTF/延迟数据 |
| `refactor` | 重构（无行为变化） | — | — |
| `test` | 测试 | — | — |
| `build` | 依赖 / 锁文件 / 镜像 | patch | `deps` scope |
| `ci` | CI 工作流 | — | — |
| `chore` | 杂项 | — | — |
| `license` | **许可 / NOTICE / 归因 / 合规** | — | **受保护路径；`License-Review:` footer；法务 + 2 人批准** |
| `revert` | 回滚 | — | `Reverts: <sha>` |

> `BREAKING CHANGE:` footer 触发 **major** 版本。典型：VoiceSpec schema 不兼容变更、API 契约变更、preset 格式升级。

## 3. `scope` 枚举（CI 校验）

| 分类 | scope |
| --- | --- |
| 控制层 | `control` `prosody` `style` `linguistic` `render` `preset` `speaker` |
| 前端 | `frontend` |
| 数据 | `dataset` `golden-set` |
| 模型/训练 | `train` `model` |
| 服务 | `serve` `api` `stream` |
| 评估 | `eval` `metrics` `gates` |
| 合规 | `license` `notice` |
| 工程 | `deps` `ci` `docs` `refs` `implement` |

> 新增 scope 需先改本文件 + `.commitlintrc.yml` + `.github/workflows/commitlint.yml`，用 `ci(ci)` 提交，不要临时自造。

## 4. Body 写作要求

- 写**动机与依据**：论文结论、门禁失败原因、用户反馈、许可证核验结果。
- 引用论文格式：`FastSpeech 2 (arXiv:2006.04558)`，链接可选。
- 引用方案章节：`v0.2 §5.5 冲突消解矩阵`。
- 涉及许可：`ADR-0001` / `docs/licensing/UPSTREAM-LICENSE-MATRIX.md`。
- 不写「改了哪些文件」（git diff 已经有了），不写空话（「优化代码」「修复问题」）。

## 5. Footer 强制项（CI 校验）

| Footer | 触发条件 | 格式 |
| --- | --- | --- |
| `Refs:` | 关联 issue / PR / 文档 | `Refs: #42` 或 `Refs: VM-TECH-001 v0.2 §3` |
| `Gate-Report:` | 改 `configs/eval/thresholds.yaml`、`configs/presets/**`、`dicts/**`、`docs/model-cards/**` | `Gate-Report: gs-2026-11-a` |
| `Spec:` | 改 `configs/voicespec/**`、`docs/voicespec/**`、`scripts/validate_voicespec.py` | `Spec: voicespec@0.3.0` |
| `Impl:` | 改 `docs/implement/**`、`src/**`、`configs/base/**`、`configs/train/**`、`scripts/check_consistency.py`、`tests/unit/**` | `Impl: implement-spec@0.4` |
| `Preset:` | 改 preset | `Preset: warm_companion@1.3.0` |
| `Dataset:` | 新增/更新数据集或 manifest | `Dataset: ds-20261104-a` |
| `Model:` | 新增/更新权重或 adapter | `Model: cv2-lora-20261104-s1200` |
| `License:` | 新增第三方依赖 / 基座 / 数据集 | `License: apache-2.0` |
| `License-Review:` | 改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md` | `License-Review: <法务批准人>` |
| `BREAKING CHANGE:` | 不兼容变更 | `BREAKING CHANGE: VoiceSpec 移除 rate 字段` |
| `Reverts:` | `revert` 类型 | `Reverts: <sha>` |

> **CI 规则**：`license-check` 工作流会扫描 PR 改动路径与 commit footer；缺 `License:` / `License-Review:` / `Gate-Report:` 直接失败；`commitlint` 工作流会校验 `Spec:`（v0.3 起）与 `Impl:`（v0.4 起）触发条件。

## 6. 受保护路径（CODEOWNERS）

| 路径 | 要求 |
| --- | --- |
| `LICENSE` | 禁止改写官方原文；仅允许整份替换为官方新版本，需法务 + 2 maintainer 批准 + `License-Review:` |
| `NOTICE` | 同上；上游归因变更需同步 `UPSTREAM-LICENSE-MATRIX.md` |
| `LICENSE-COMMERCIAL.md` | 法务 + 2 maintainer 批准 |
| `datasets/golden_set/**` | **CI 校验 hash，任何改动直接失败**；仅限 `data(golden-set)` 且需 maintainer 显式批准 |
| `configs/presets/**` | maintainer 批准 + `Gate-Report:` + `Preset:` |
| `configs/eval/thresholds.yaml` | maintainer 批准 + `Gate-Report:`；校准只能收紧 |
| `configs/voicespec/**` · `docs/voicespec/**` | maintainer 批准 + `Spec:` footer；契约变更须同步错误码表与 ADR-0003 |
| `docs/implement/**` · `src/**` | maintainer 批准 + `Impl:` footer；**Phase 0 期间 `src/**` 只允许签名占位**，出现实现代码须先改 ADR-0004 / D16 |
| `scripts/check_consistency.py` · `tests/unit/**` | maintainer 批准；单测须保持 `python -m unittest discover -s tests/unit` 全绿 |

## 7. 分支与 PR

| 项 | 规则 |
| --- | --- |
| 分支 | `feat/<scope>-<slug>` · `fix/<scope>-<slug>` · `docs/<slug>` · `model/<slug>` · `voice/<slug>` · `exp/<slug>` · `license/<slug>` |
| 默认分支 | `main`，受保护，**禁止直推** |
| PR 标题 | 必须符合本规范（squash 后成为提交信息） |
| PR 模板 | 必须填写：变更类型、是否影响门禁/许可/模型卡、关联 Gate-Report、许可影响勾选、测试方式 |
| 合并 | squash merge（默认）；一个 PR 一个逻辑变更；大改动拆 PR |
| 版本 | tag `vX.Y.Z`；`CHANGELOG.md` 由 conventional-changelog 从提交生成，**禁止手写** |

## 8. 本地校验

```bash
# 提交前（需 Node 环境 + commitlint）
npx commitlint --from HEAD~1 --to HEAD --edit

# 或依赖 CI：push 后 .github/workflows/commitlint.yml 自动校验 PR 内全部提交
```

提交前检查清单见 [`CONTRIBUTING.md`](CONTRIBUTING.md) §5；**`git push` 前必须跑 `leak_guard` 且 `ok=true`**。

## 9. 规范变更

修改本文件需用 `docs(refs)` 或 `ci(ci)` 提交，并同步更新 `.commitlintrc.yml` 与工作流中的枚举，避免规范与校验器不一致。
