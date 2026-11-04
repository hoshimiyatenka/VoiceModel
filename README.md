# VoiceModel · AI 智能体声音训练项目

> 可控、可复现、可评测的 AI 智能体语音合成能力。
> 以开源基座 + 授权数据微调得到专属音色，把「声音」抽象为**版本化、可单独调节、互不干扰的参数**。

| 项 | 内容 |
| --- | --- |
| 仓库 | `https://github.com/hoshimiyatenka/VoiceModel` |
| 当前阶段 | **Phase 0 — 立项 / 选型核验期**（尚未开始数据与训练，无实测指标） |
| 当前方案 | [`docs/AI智能体声音训练项目_技术栈方案_v0.3.md`](docs/AI智能体声音训练项目_技术栈方案_v0.3.md) |
| 许可 | **PolyForm Noncommercial License 1.0.0**（开放权重 / 源码可得，**禁止商业化**） |

---

## ⚠️ 许可摘要（请先读）

本项目**公开全部源代码与模型权重**，但**不是 OSI 认证的 Open Source**：

- ✅ **允许**：研究、个人学习/实验/测试、非商业组织（公益/教育/公共研究/政府，无论资金来源）、法律赋予的合理使用。
- ❌ **禁止（除非取得单独书面授权）**：任何商业目的使用 —— 嵌入付费产品、提供语音生成 API / 托管服务、企业内部业务运营、直接或间接产生收入的用途。
- 🔑 **权利保留**：版权持有人保留向特定主体单独授予**商业许可**的权利（双授权）。申请见 [`LICENSE-COMMERCIAL.md`](LICENSE-COMMERCIAL.md)。

完整条款以 [`LICENSE`](LICENSE) 为准；归因、覆盖边界与使用限制见 [`NOTICE`](NOTICE)。

**术语说明**：OSI 开源定义第 6 条禁止「按用途领域歧视」，因此「允许商用」的 Apache/MIT 与「禁止商业化」不可兼得。本项目对外称 **「开放权重 / 源码可得（source-available, open-weight）」**，不称「开源」。详见 [`docs/decisions/ADR-0001.md`](docs/decisions/ADR-0001.md)。

**许可覆盖边界**：NC 条款覆盖**本项目自有增量**（代码、VoiceSpec 契约、preset、词典、标注、golden_set、LoRA/adapter、微调权重、模型卡、文档、音色资产）；上游基座权重依其自身许可（如 Apache-2.0），第三方仍可按原条款使用原样上游，项目方不主张限制。详见 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](docs/licensing/UPSTREAM-LICENSE-MATRIX.md)。

---

## 项目核心：参数化细调

同一音色，稳定地产出任意情绪、语速、语调、时长与场景的声音。五层 `VoiceSpec`：

| 层 | 职责 | 代表参数 |
| --- | --- | --- |
| `IdentitySpec` | 是谁在说 | `speaker_id` `ref_audio_uri` `speaker_lock` `voice_blend` |
| `ProsodySpec` | 怎么说 | `pitch_semitones` `pitch_range` `energy_db` `rate` `duration_mode` `duration_ms` `pauses` |
| `StyleSpec` | 什么状态说 | `emotion` `emotion_strength` `emotion_ref_uri` `scenario` `formality` |
| `LinguisticSpec` | 把字念对（零容忍） | `lang` `pronunciation_dict` `phoneme_overrides` `emphasis` |
| `RenderSpec` | 最后怎么送出去 | `sample_rate` `loudness_lufs` `seed` `streaming` `watermark` |

每个连续参数须过 5 点扫描门禁（单调 ρ ≥ 0.90、UTMOS 下降 ≤ 0.30、说话人 cosine 漂移 ≤ 0.03）。完整定义见方案 v0.1 §5 / v0.2 §5。

**v0.3 起契约已机器可读**：[`configs/voicespec/voicespec.schema.json`](configs/voicespec/voicespec.schema.json)（JSON Schema 2020-12）、[`docs/voicespec/README.md`](docs/voicespec/README.md)、[`docs/voicespec/ERROR-CODES.md`](docs/voicespec/ERROR-CODES.md)、[`docs/decisions/ADR-0003.md`](docs/decisions/ADR-0003.md)。本地校验：

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_voicespec.py configs/voicespec/examples/*.json
```

最小请求（[`minimal.json`](configs/voicespec/examples/minimal.json)）：

```json
{
  "spec_version": "0.3.0",
  "text": "你好，我是你的智能助手。",
  "identity": { "speaker_id": "agent_main" },
  "prosody": { "rate": 0.92, "pitch_semitones": -0.5, "pause_profile": "gentle" },
  "style": { "emotion": "tender", "emotion_strength": 0.6, "scenario": "陪伴" },
  "render": { "streaming": true, "loudness_lufs": -16, "watermark": true }
}
```

---

## 技术路径（当前位置）

```
P0 立项与核验  ← 你在这里（选型/许可/论文的在线核验已完成，法务待批）
P1 数据底座 → P2 基线复现与定型 → P3 参数化控制层 → P4 微调与偏好对齐
   → P5 评估体系与 CI（贯穿）→ P6 服务化与流式 → P7 灰度
```

- 双轨路线：轨道 A 可控基座（CosyVoice 2 / Qwen3-TTS / VoxCPM2 三选一）+ 轨道 B LoRA 定制，L5 参数契约解耦。
- 保质量：train / val / test / **golden_set（冻结）** 四套分离；客观 + 主观双轨门禁；阈值单一真源 [`configs/eval/thresholds.yaml`](configs/eval/thresholds.yaml)。
- 排期：档 A 6–8 周演示 / **档 B 16–20 周（基线承诺，灰度至 24 周）** / 档 C 24–32 周。

---

## 文档索引

| 文档 | 内容 |
| --- | --- |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.3.md`](docs/AI智能体声音训练项目_技术栈方案_v0.3.md) | **当前方案**：契约落地、R-14 核验回填、v0.3 迭代 |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.2.md`](docs/AI智能体声音训练项目_技术栈方案_v0.2.md) | 上一版（归档）：许可策略、论文体系、核验回填、提交规范 |
| [`docs/AI智能体声音训练项目_技术栈方案_v0.1.md`](docs/AI智能体声音训练项目_技术栈方案_v0.1.md) | 初版（归档）：五层参数体系、数据/训练/评估/排期全文（根目录亦保留一份 `AI智能体声音训练项目_技术栈方案_v0.1.md`） |
| [`docs/references/PAPERS.md`](docs/references/PAPERS.md) | **权威论文清单**（58 篇，国内外，逐篇 arXiv ID + 发表信息 + 方案关联；v0.3 补录 6 篇并降级发表状态表述） |
| [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](docs/licensing/UPSTREAM-LICENSE-MATRIX.md) | 上游许可证核验矩阵与传导分析（核验 2026-11-04） |
| [`configs/voicespec/voicespec.schema.json`](configs/voicespec/voicespec.schema.json) | **★ VoiceSpec 机器可读契约**（JSON Schema 2020-12） |
| [`docs/voicespec/README.md`](docs/voicespec/README.md) | VoiceSpec 使用说明 |
| [`docs/voicespec/ERROR-CODES.md`](docs/voicespec/ERROR-CODES.md) | 校验错误码表 |
| [`docs/decisions/ADR-0001.md`](docs/decisions/ADR-0001.md) | 许可策略决策 |
| [`docs/decisions/ADR-0002.md`](docs/decisions/ADR-0002.md) | 基座选型方法与评分卡 |
| [`docs/decisions/ADR-0003.md`](docs/decisions/ADR-0003.md) | 参数化控制层实现路径 |
| [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md) | **★ 提交规范**（Conventional Commits 定制 + CI 强制） |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 贡献流程与检查清单 |
| [`LICENSE-COMMERCIAL.md`](LICENSE-COMMERCIAL.md) | 商业授权入口 |

## 目录结构（骨架）

```
configs/      阈值 / 训练 / preset（单一真源）
datasets/     manifest 与 golden_set（音频实体走 DVC/对象存储，不入库）
dicts/        发音词典（多音字 / 专名）
docs/         方案 / 论文 / 许可 / ADR / 模型卡 / 评测规范
src/          frontend / control / models / train / eval / serve / data
tests/        unit / integration / regression（挂 CI）
.github/      commitlint / license-check / eval-gate / PR 与 Issue 模板
```

---

## 核验声明

v0.1 编写时联网检索通道不可用（HTTP 401），所有第三方信息标注待核验。v0.2 于 **2026-11-04** 改用 arXiv Atom API、GitHub REST API（`gh api`）、Hugging Face Model API 与官方 LICENSE 原文逐项核验，已解除主要 ⚠️ 项；剩余待核验项（部分权重与数据集许可）登记为 R-14，P0 清零前不得定型发布。所有结论附来源 URL 与核验日期，可复核。

---

## 贡献

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。提交信息必须符合 [`COMMIT_CONVENTION.md`](COMMIT_CONVENTION.md)，`git push` 前须过 `leak_guard` 凭据审计。

## 伦理与合规

禁止未授权声音克隆、冒充、欺诈、去除水印；对外交付须标注「AI 合成」；再分发须以同等保护力条款约束下游。详见 [`NOTICE`](NOTICE) §4。

---

*本项目由 DeepSeek Harness 辅助构建。*
