# 贡献指南 · VoiceModel

欢迎参与。本项目是**开放权重 / 源码可得**的 AI 智能体声音训练项目，采用 PolyForm Noncommercial 1.0.0 许可。

## 0. 先读许可（重要）

- 公众许可：[`LICENSE`](LICENSE) — **PolyForm Noncommercial 1.0.0**，禁止任何商业目的使用。
- 归因与权利保留：[`NOTICE`](NOTICE)。
- 商业授权申请：[`LICENSE-COMMERCIAL.md`](LICENSE-COMMERCIAL.md)。

**提交贡献即表示你同意**：你的贡献依仓库 `LICENSE` 的条款对外提供，且你有权提交该内容；你不得在贡献中夹带你无权公开或带有不兼容许可的素材。若你的贡献涉及第三方代码/模型/数据，**必须在 PR 中声明其来源与许可证**，并同步更新 `NOTICE` 与 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](docs/licensing/UPSTREAM-LICENSE-MATRIX.md)。

> 本项目不是 OSI 认证开源（NC 条款与 OSD 第 6 条冲突），请勿在 PR 描述中把本项目称作 "Apache/MIT 开源"。对外统一用「开放权重 / 源码可得」。

## 1. 项目文档索引

| 文档 | 内容 |
| --- | --- |
| [`README.md`](README.md) | 项目入口、快速开始 |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.2.md`](docs/AI智能体声音训练项目_技术栈方案_v0.2.md) | **当前技术方案** |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.1.md`](docs/AI智能体声音训练项目_技术栈方案_v0.1.md) | 初版（归档；根目录亦保留一份） |
| [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md) | **★ 提交规范（必读）** |
| [`docs/references/PAPERS.md`](docs/references/PAPERS.md) | 权威论文清单（52 篇） |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](docs/licensing/UPSTREAM-LICENSE-MATRIX.md) | 上游许可证核验表 |
| [`docs/decisions/ADR-0001.md`](docs/decisions/ADR-0001.md) | 许可策略决策 |
| [`configs/eval/thresholds.yaml`](configs/eval/thresholds.yaml) | 评估阈值单一真源 |

## 2. 开发环境（骨架，P0 补全）

```bash
git clone https://github.com/hoshimiyatenka/VoiceModel.git
cd VoiceModel
# 依赖锁定见 locks/，环境用 conda/uv + Docker，禁止全局 pip install
```

当前处于 **Phase 0（立项 / 选型核验期）**：数据流水线、训练、推理服务尚未落地。欢迎贡献的优先方向：

- 文档与方案迭代（`docs`）
- 论文核验与补充（`docs(refs)`，须带 arXiv ID）
- 上游许可证核验（`license(notice)`，须附核验日期与来源）
- 提交规范与 CI（`ci`）
- 评估指标实现与 golden_set 设计（`eval`）

> **请勿提交**：音频实体、模型权重、checkpoint、有声授权书扫描件、含个人信息的原始录音、`.env` / 密钥 / token。大文件走 DVC / 对象存储，仓库只留 manifest（含 hash、授权 ID、质检分）。

## 3. 分支与提交

- 分支：`feat/<scope>-<slug>` / `fix/...` / `docs/...` / `model/...` / `voice/...` / `license/...`
- 提交信息：**必须**符合 [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md)，CI 用 commitlint 强校验。
- 一个 PR 一个逻辑变更；`main` 受保护，禁止直推；默认 squash merge。

## 4. Pull Request 流程

1. 从 `main` 建分支。
2. 提交（遵循提交规范，填齐强制 footer）。
3. 填 PR 模板：变更类型、是否影响门禁/许可/模型卡、Gate-Report、许可影响勾选、测试方式。
4. CI 全绿：`commitlint` / `license-check` / `eval-gate`（骨架）。
5. 受保护路径需对应 CODEOWNER 批准（见提交规范 §6）。
6. squash merge；`CHANGELOG.md` 由 conventional-changelog 自动生成。

## 5. 提交与发布前检查清单

```
[ ] 提交信息符合 COMMIT_CONVENTION.md（本地 commitlint 或 CI）
[ ] 未提交音频实体 / checkpoint / 授权书扫描件 / .env / 密钥 / 个人信息
[ ] 涉及 preset / 阈值 / 权重 / 数据集时填了对应 footer
[ ] 新增第三方依赖或基座已更新 UPSTREAM-LICENSE-MATRIX.md 与 NOTICE
[ ] 方案变更已同步 docs/ 对应文档与修订记录
[ ] 引用论文带 arXiv ID 且已加入 docs/references/PAPERS.md
[ ] git push 前跑过 leak_guard({action:"scan", path:"<仓库绝对路径>"}) 且 ok=true
```

> **发布前凭据审计**：`leak_guard` 不联网、不上传，只读本地路径；发现结果脱敏。`ok=false` 时先处理 critical/high 项再 push。

## 6. 受保护路径

| 路径 | 说明 |
| --- | --- |
| `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md` | 法务 + 2 maintainer 批准 |
| `datasets/golden_set/**` | CI 校验 hash，任何改动直接失败 |
| `configs/presets/**` | maintainer 批准 + Gate-Report |
| `configs/eval/thresholds.yaml` | maintainer 批准 + Gate-Report，校准只能收紧 |

## 7. 行为准则

- 禁止提交未授权声音克隆素材；禁止用于冒充、欺诈、骚扰。
- 禁止故意去除/规避水印与溯源信号。
- 对外交付音频与接口须标注「AI 合成」。
- 再分发时须以同等保护力条款约束下游（见 `NOTICE` §4）。

## 8. 联系

- 一般贡献：GitHub Issue / PR
- 商业授权：见 [`LICENSE-COMMERCIAL.md`](LICENSE-COMMERCIAL.md)
- 许可与合规：见 `NOTICE` §7
