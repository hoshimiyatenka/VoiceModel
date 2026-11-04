# 上游许可证核验矩阵 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-LIC-001 |
| 版本 | v0.2 |
| 核验日期 | **2026-11-04** |
| 核验通道 | GitHub REST API `gh api repos/<owner>/<repo>` / `gh api repos/<owner>/<repo>/license`；Hugging Face `https://huggingface.co/api/models/<id>`；官方 LICENSE 原文 |
| 用途 | 「开放权重 + 非商业许可」的传导分析、基座选型一票否决依据、NOTICE 归因来源 |

> ⚠️ 本文是**工程核验记录，不是法律意见**。所有「商用结论」须经法务复核（D11）后方可作为立项依据。

---

## 1. 为什么需要这张表

项目方只能对自己拥有版权的**增量**设定义务，**不能追溯撤销上游权利人已授予的权利**。
因此「本模型禁止商业化」的实际覆盖范围，取决于所选上游基座的权重许可。
本表逐项核验，并给出 ADR-0001 的选基座依据。

**核验发现的关键事实**：`SparkAudio/Spark-TTS` 代码 Apache-2.0 但**权重 CC-BY-NC-SA-4.0**，
是「代码开源 ≠ 权重可商用」的典型案例。

---

## 2. 基座 / TTS 候选

| 上游 | 仓库（核验时解析） | 代码许可 | 权重许可 | 商用 | 关键条款 / 风险 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| **CosyVoice / CosyVoice 2** | `QwenAudio/CosyVoice`（`FunAudioLLM/CosyVoice` 重定向至此），stars 24278 | **Apache-2.0**（LICENSE 原文核验） | **apache-2.0**（HF `FunAudioLLM/CosyVoice2-0.5B` license tag） | ✅ | 标准宽松许可；流式 + 指令控情感/方言/语速 | **轨道 A 首选候选** |
| **Qwen3-TTS** | `QwenLM/Qwen3-TTS`，stars 14207 | **Apache-2.0** | **apache-2.0**（HF `Qwen/Qwen3-TTS-12Hz-1.7B-Base`、`-CustomVoice`） | ✅ | 标准宽松；voice design + 克隆 + 流式 | **轨道 A 首选候选** |
| **VoxCPM / VoxCPM2** | `OpenBMB/VoxCPM`，stars 41016 | **Apache-2.0** | **apache-2.0**（HF `openbmb/VoxCPM2`） | ✅ | 标准宽松；tokenizer-free | **轨道 A 备选** |
| **IndexTTS2** | `index-tts/index-tts`，stars 24932 | `bilibili Model Use License Agreement`（GitHub SPDX = `NOASSERTION`） | HF `IndexTeam/IndexTTS-2` **无 license tag**，待核验 | 条件 | §2.2 MAU > 1 亿 或 上年营收 > RMB 10 亿须单独授权；§4(c) **不得用于改进其他 AI 模型**（除自身衍生作品或**非商业** AI 模型）；§5.1 违约可撤销并要求删除；中英文冲突以中文版为准 | **方法首选 / 许可需法务书面确认**；其「非商业 AI 模型」例外与本项目 NC 定位一致 |
| **Spark-TTS** | `SparkAudio/Spark-TTS`，stars 10993 | **Apache-2.0**（LICENSE 全文为 Apache-2.0） | **cc-by-nc-sa-4.0**（HF `SparkAudio/Spark-TTS-0.5B` 权重卡原文：*"The model can only be used for non-commercial purposes."*） | ❌ | **NC + SA 传染**：衍生作品须同许可发布，项目方无法改用 PolyForm NC 或自定义商业例外；代码/权重许可不一致 | **不采用其权重作发布基座**（ADR-0001）；仅参考属性级控制方法 |
| **Fish-Speech / OpenAudio S1** | `fishaudio/fish-speech`，stars 33570 | `Fish Audio Community License v1.0`（2026-10-13，自定，SPDX `NOASSERTION`） | 待核验 | 有限 | §III(a) 年营收 < **USD 500,000** 才有限商用；§III(b) 达阈值 30 天内通知、90 天过渡期后须另签；§III(c) **Hosted Service 一律禁止**；§IV(b) 禁止未授权克隆、禁止去水印；§IV(b) **禁止用输出训练/蒸馏其他基础语音模型**；须保留 "Built with Fish Audio" | 备选，合规负担重 |
| **F5-TTS** | `SWivid/F5-TTS`，stars 15509 | **MIT** | 待核验 | 待定 | 代码宽松 | 效率对照候选 |
| **GPT-SoVITS** | `RVC-Boss/GPT-SoVITS`，stars 64788 | **MIT** | 待核验 | 待定 | 代码宽松；少样本音色定制 | **轨道 B 备选**（可控性弱） |
| **Seed-TTS** | 论文 `arXiv:2406.02430` | 权重可得性待核验 | 待核验 | 待定 | 字节 Seed 技术报告 | 论文参考；权重不可得则一票否决 |
| **coqui-ai/TTS** | `coqui-ai/TTS`，stars 46175 | **MPL-2.0** | — | ✅ | 弱互惠：修改过的 MPL 文件须继续以 MPL 提供，注意文件级 copyleft | 工具链对照 |

## 3. 声码器 / 工具链（均宽松，不构成障碍）

| 组件 | 仓库 | 许可 | 论文 |
| --- | --- | --- | --- |
| HiFi-GAN | `jik876/hifi-gan` | 待核验（论文注明代码地址） | `2010.05646` NeurIPS 2020 |
| BigVGAN | `NVIDIA/BigVGAN` | **MIT** | `2206.04658` ICLR 2023 |
| Whisper | `openai/whisper` | **MIT** | `2212.04356` |
| WhisperX | `m-bain/whisperX` | **BSD-2-Clause** | `2303.00747` INTERSPEECH 2023 |
| MFA | `MontrealCorpusTools/Montreal-Forced-Aligner` | **MIT** | — |
| FunASR | `modelscope/FunASR` | **MIT** | `2305.11013` |
| Paraformer | （FunASR 内） | MIT | `2206.08317` |
| WeNet | `wenet-e2e/wenet` | **Apache-2.0** | `2102.01547` |
| SpeechBrain | `speechbrain/speechbrain` | **Apache-2.0** | ECAPA-TDNN `2005.07143` |
| AudioSeal | `facebookresearch/audioseal` | **MIT** | `2401.17264` ICML 2024 |

## 4. 数据集（商用范围须逐项核验）

| 数据集 | 论文 / 来源 | 用途 | 状态 |
| --- | --- | --- | --- |
| AISHELL-3 | `2010.11567` | 中文多说话人 TTS 基线 | 许可证待核验 |
| WenetSpeech | `2110.03370` | 中文 ASR 语料 | 许可证待核验 |
| LibriTTS / VCTK | 公开 | 英文流水线验证 | 许可证待核验 |
| ESD / CASIA / EmoV-DB | 情感语音库 | 情感标注体系 | **多为研究用途，商用范围待核验** |
| Common Voice | Mozilla | 多语种储备 | 版本与许可待核验 |

**原则**：公开数据仅用于「流水线验证 / 评测对照 / 通用能力」；专属音色训练数据必须自有授权，二者物理隔离（不同目录 + 不同 manifest 字段）。每条 manifest 强制 `license_id`。

---

## 5. Apache-2.0 §4 传导分析（核心结论）

Apache-2.0 原文（已核验 `QwenAudio/CosyVoice`、`QwenLM/Qwen3-TTS`、`OpenBMB/VoxCPM`、`SparkAudio/Spark-TTS` 的 LICENSE 全文一致）：

> *"You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License."*

**结论**：基于 Apache-2.0 权重做 LoRA / 微调后，项目方可以对**自己的修改**乃至**衍生作品整体**附加 NC 条款，但必须：

1. 随附 Apache-2.0 许可副本；
2. 修改文件带显著变更声明；
3. 保留上游版权/专利/商标/归因声明（含 `NOTICE` 文件内容）；
4. **不能剥夺第三方对上游原作品本身依 Apache-2.0 享有的权利**（包括商用）。

因此本项目许可边界为：

```
上游基座权重（Apache-2.0）  → 第三方仍可按 Apache-2.0 使用「原样上游」，项目方不限制
本项目增量（PolyForm NC）   → 禁止商业化条款实际覆盖的部分：
    · 训练/推理/控制层代码
    · VoiceSpec 契约、preset、配置、发音词典
    · 数据集标注、质检流程、golden_set
    · LoRA / adapter / 微调后权重
    · 模型卡、文档、评测报告
    · 预设音色资产
```

**不可夸大的部分**：使用者若自行取用上游原始权重、绕过本项目增量，可按 Apache-2.0 商用。这是许可证无法阻止的，也应在 README 与 `LICENSE-COMMERCIAL.md` 中明示，避免权利范围表述失实。

## 6. 为什么不选 NC-SA 权重（ADR-0001 摘要）

| 代价 | 说明 |
| --- | --- |
| **SA 传染** | 衍生作品须以同一许可发布，项目方不能改用 PolyForm NC 1.0.0，也不能自定义商业例外条款 |
| **商业例外授权权不完整** | CC-BY-NC 的 NC 放宽需原权利人同意；项目方作为衍生方能否单独向第三方授予商用权存在不确定性，双授权变现路径受阻 |
| **代码/权重许可不一致** | 合规审计需拆分两套义务 |

→ **决策**：选宽松许可权重的基座（CosyVoice 2 / Qwen3-TTS / VoxCPM2 三选一，Phase 2 实测定型），项目自有增量用 PolyForm NC 1.0.0；不使用 Spark-TTS 权重作发布基座。

## 7. 核验命令（可复核）

```bash
# 仓库许可证元数据
gh api repos/QwenAudio/CosyVoice --jq '[.full_name, .license.spdx_id, .stargazers_count] | @tsv'
gh api repos/index-tts/index-tts/license --jq '{name:.name, spdx:.spdx_id, size:.size}'

# LICENSE 原文（base64 → UTF-8）
gh api repos/SparkAudio/Spark-TTS/license --jq '.content' | base64 -d

# Hugging Face 权重卡 license
curl -s https://huggingface.co/api/models/SparkAudio/Spark-TTS-0.5B | jq '.tags[] | select(startswith("license:"))'
curl -s https://huggingface.co/SparkAudio/Spark-TTS-0.5B/raw/main/README.md | grep -i -E 'license|non-commercial'

# PolyForm NC 官方纯文本
curl -s https://polyformproject.org/licenses/noncommercial/1.0.0.txt
```

## 8. 待清零项（R-14 / P0 阻塞）

- [ ] F5-TTS / GPT-SoVITS / HiFi-GAN 的**模型权重**许可证（当前仅核验代码）
- [ ] `IndexTeam/IndexTTS-2` 权重卡条款（HF 无 license tag）
- [ ] Fish Audio 模型权重许可证（与代码许可是否一致）
- [ ] ESD / CASIA / EmoV-DB / Common Voice 的商用范围
- [ ] Qwen3-TTS 官方技术报告 arXiv ID
- [ ] Vocos 声码器论文与许可

> 每次升级或新增基座/依赖，**必须同步更新本表与 `NOTICE`**，并在提交信息中填 `License:` footer（见 `COMMIT_CONVENTION.md`）。
