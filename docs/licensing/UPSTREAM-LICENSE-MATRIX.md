# 上游许可证核验矩阵 · VoiceModel

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-LIC-001 |
| 版本 | **v0.3**（对应技术栈方案 v0.3 §5；v0.2 为初版核验） |
| 核验日期 | **2026-11-04**（v0.3 补录同日；Lead 本地 + subagent 双路交叉印证） |
| 核验通道 | GitHub REST API `gh api repos/<owner>/<repo>` / `gh api repos/<owner>/<repo>/license`；Hugging Face `https://huggingface.co/api/models/<id>` / `/api/datasets/<id>`；官方 LICENSE 原文；OpenSLR；arXiv Atom API |
| 用途 | 「开放权重 + 非商业许可」的传导分析、基座选型一票否决依据、NOTICE 归因来源 |

> ⚠️ 本文是**工程核验记录，不是法律意见**。所有「商用结论」须经法务复核（D11）后方可作为立项依据。
> **v0.3 关键修订**：拆分「代码许可 / 权重许可」两列并回填核验值；发现多起**代码宽松、权重禁商用**（F5-TTS / fishaudio / coqui），按代码推断可商用会出错，登记为 **R-18**。HF API 对不存在/受限 ID 统一返回 HTTP 401（已用 `meta-llama/Llama-2-7b`=200、`coqui/XTTS-v2`=200 对照验证），所有 401 按「ID 不存在或不可公开访问」处理，不据此推断许可。

---

## 1. 为什么需要这张表

项目方只能对自己拥有版权的**增量**设定义务，**不能追溯撤销上游权利人已授予的权利**。
因此「本模型禁止商业化」的实际覆盖范围，取决于所选上游基座的权重许可。
本表逐项核验，并给出 ADR-0001 的选基座依据。

**核验发现的关键事实（v0.3 扩展）**：「代码开源 ≠ 权重可商用」不是个例，而是普遍现象——

- `SparkAudio/Spark-TTS`：代码 Apache-2.0，权重 **CC-BY-NC-SA-4.0**（v0.2 已发现）
- `SWivid/F5-TTS`：代码 **MIT**，权重 **`cc-by-nc-4.0`**（v0.3 新增）
- `fishaudio/fish-speech`：代码 Community License v1.0（有限商用），权重 **CC-BY-NC-SA-4.0** 或 **Fish Audio Research License（仅非商用）**（v0.3 新增）
- `coqui-ai/TTS`：代码 MPL-2.0，XTTS 权重 **CPML**（tos_required）、YourTTS 权重 **CC-BY-NC-ND 4.0**（v0.3 新增）

→ 因此本表**必须分别核验代码与权重**，模型卡强制填写 `base_license`（权重），`license-check` CI 校验。这正是 R-18 的缓解措施。

---

## 2. 基座 / TTS 候选

| 上游 | 仓库（核验时解析） | 代码许可 | 权重许可 | 商用 | 关键条款 / 风险 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| **CosyVoice / CosyVoice 2** | `QwenAudio/CosyVoice`（`FunAudioLLM/CosyVoice` 重定向至此），stars 24278 | **Apache-2.0**（LICENSE 原文核验） | **apache-2.0**（HF `FunAudioLLM/CosyVoice2-0.5B` license tag） | ✅ | 标准宽松许可；流式 + 指令控情感/方言/语速 | **轨道 A 首选候选** |
| **Qwen3-TTS** | `QwenLM/Qwen3-TTS`，stars 14207 | **Apache-2.0** | **apache-2.0**（HF `Qwen/Qwen3-TTS-12Hz-1.7B-Base`、`-CustomVoice`） | ✅ | 标准宽松；voice design + 克隆 + 流式 | **轨道 A 首选候选** |
| **VoxCPM / VoxCPM2** | `OpenBMB/VoxCPM`，stars 41016 | **Apache-2.0** | **apache-2.0**（HF `openbmb/VoxCPM2`） | ✅ | 标准宽松；tokenizer-free | **轨道 A 备选** |
| **IndexTTS2** | `index-tts/index-tts`，stars 24932 | `bilibili Model Use License Agreement`（GitHub SPDX = `NOASSERTION`） | **[OK] 确认无 license tag**：HF `IndexTeam/IndexTTS-2` 的 `tags` 无 `license:*`、`cardData.license` 空、`gated=false`、README 全文无许可条款 | 条件 | §2.2 MAU > 1 亿 或 上年营收 > RMB 10 亿须单独授权；§4.1(c) *"You may not Use ... to improve any AI model, except for ... non-commercial AI models"*；§5.1 违约可撤销并要求删除；中英文冲突以中文版为准。**同组织 `Index-TTS`/`IndexTTS-1.5`=apache-2.0、`IndexTTS-2.5`=license:other，许可不一致** | **方法首选 / 许可需法务书面确认**：HF 权重是否受 GitHub 自定义协议约束待定 |
| **Spark-TTS** | `SparkAudio/Spark-TTS`，stars 10993 | **Apache-2.0**（LICENSE 全文为 Apache-2.0） | **cc-by-nc-sa-4.0**（HF `SparkAudio/Spark-TTS-0.5B` 权重卡原文：*"The model can only be used for non-commercial purposes."*） | ❌ | **NC + SA 传染**：衍生作品须同许可发布，项目方无法改用 PolyForm NC 或自定义商业例外；代码/权重许可不一致 | **不采用其权重作发布基座**（ADR-0001）；仅参考属性级控制方法 |
| **Fish-Speech 家族** | `fishaudio/fish-speech`，stars 33570 | `Fish Audio Community License v1.0`（2026-10-13，SPDX `NOASSERTION`） | **[OK] 与代码不一致**：`fish-speech-1/1.2/1.2-sft/1.4/1.5`、`speech-lm-v1`、`s1-mini`、`fish-agent-v0.1-3b` = **`cc-by-nc-sa-4.0`**；`s2-pro`/`drama-3`/`drama-3-int4` = `license:other, license_name=fish-audio-research-license`（**仅研究/非商用**，`business@fish.audio` 另议） | ❌ | 代码 §III(a) 年营收 < USD 500,000 有限商用、§III(c) Hosted 须单独书面许可；但**权重**为 NC-SA 或 Research License，`s1-mini` 卡另有 "I agree to use this model for non-commercial use ONLY" 勾选；§IV(b) 禁止去水印、禁止用输出训练/蒸馏其他基础语音模型 | **依 ADR-0001 排除作发布基座**；`[MISS]` 精确 ID `fishaudio/fish-speech` / `OpenAudio-S1` 401/404，需确认 `s2-pro` 与 OpenAudio-S1 对应关系 |
| **F5-TTS** | `SWivid/F5-TTS`，stars 15509 | **MIT** | **[OK] `cc-by-nc-4.0`**（HF `SWivid/F5-TTS`：`tags=license:cc-by-nc-4.0`、`cardData.license=cc-by-nc-4.0`、`gated=false`） | ❌ | **v0.2「MIT，效率对照候选」须修正**：权重禁商用；与本项目 NC 定位一致，但不可声称可商用 | 仅作效率对照，不作可商用基座 |
| **GPT-SoVITS** | `RVC-Boss/GPT-SoVITS`，stars 64788 | **MIT** | **[MISS]** HF org 下 0 模型、精确 ID HTTP 401；镜像 `lj1995/GPT-SoVITS` = `license:mit` | 未定 | 官方权重许可是否独立于 MIT 代码**需人工确认** | **轨道 B 备选**（可控性弱），权重许可未定前不发布 |
| **Seed-TTS** | 论文 `arXiv:2406.02430` | 权重可得性待核验 | 待核验 | 待定 | 字节 Seed 技术报告 | 论文参考；权重不可得则一票否决 |
| **coqui-ai/TTS** | `coqui-ai/TTS`，stars 46175 | **MPL-2.0** | **[OK] 额外权重限制**：`TTS/.models.json` 中 `xtts_v2`/`xtts_v1.1` = `"license":"CPML", "tos_required":true`、`your_tts` = `CC BY-NC-ND 4.0`；HF `coqui/XTTS-v2` = `license:other, license_name=coqui-public-model-license` | 条件 | 代码弱互惠（修改过的 MPL 文件须继续 MPL）；**CPML 全文 `https://coqui.ai/cpml` 已 404（关站）**，仅间接证据，需法务从存档确认 | 工具链对照；权重不得按 MPL 推断可商用 |

## 3. 声码器 / 工具链（均宽松，不构成障碍）

| 组件 | 仓库 | 代码许可 | 权重/发行许可 | 论文 |
| --- | --- | --- | --- | --- |
| HiFi-GAN | `jik876/hifi-gan` | **[OK] MIT**（Copyright (c) 2020 Jungil Kong，`gh api repos/jik876/hifi-gan/license`） | **不统一**：`ntt123/hifigan_ljs_24k`=cc-by-nc-4.0、`hifigan_ljs_22k`=cc-by-nc-sa-4.0、两款 espnet=cc-by-4.0、`jaketae/hifigan-lj-v1` 无 tag；HF `jik876/hifi-gan` 精确 ID 401（非 HF 模型仓库） | `2010.05646`（发表状态见 PAPERS.md 降级说明） |
| **Vocos** | `gemelo-ai/vocos`（原 `charactr/vocos` 已迁） | **MIT**（Copyright (c) 2023 Charactr Inc.） | **[OK] MIT**：`charactr/vocos-mel-24khz` / `vocos-encodec-24khz` 权重卡 `license:mit` | **`2306.00814`**（v0.3 补录） |
| BigVGAN | `NVIDIA/BigVGAN` | **MIT** | — | `2206.04658` |
| Whisper | `openai/whisper` | **MIT** | — | `2212.04356` |
| WhisperX | `m-bain/whisperX` | **BSD-2-Clause** | — | `2303.00747` |
| MFA | `MontrealCorpusTools/Montreal-Forced-Aligner` | **MIT** | — | — |
| FunASR | `modelscope/FunASR` | **MIT** | — | `2305.11013` |
| Paraformer | （FunASR 内） | MIT | — | `2206.08317` |
| WeNet | `wenet-e2e/wenet` | **Apache-2.0** | — | `2102.01547` |
| SpeechBrain | `speechbrain/speechbrain` | **Apache-2.0** | — | ECAPA-TDNN `2005.07143` |
| AudioSeal | `facebookresearch/audioseal` | **MIT** | — | `2401.17264` |

## 4. 数据集（商用范围，v0.3 核验回填）

| 数据集 | 论文 / 来源 | 许可（核验值） | 商用 | 依据 |
| --- | --- | --- | --- | --- |
| **AISHELL-3** | `2010.11567` / OpenSLR 93 | **Apache-2.0**（HF `AISHELL/AISHELL-3` `license:apache-2.0`） | ✅ | `https://www.openslr.org/93/` "License: Apache License v.2.0" |
| **WenetSpeech** | `2110.03370` / `wenet-e2e/WenetSpeech` | GitHub LICENSE = **Apache-2.0**；HF `gated=auto` 且**无 license tag**；衍生 `WenetSpeech4TTS` = `cc-by-4.0`、gated=auto | ✅（需申请） | `https://raw.githubusercontent.com/wenet-e2e/WenetSpeech/master/LICENSE` 首行 "Apache License Version 2.0"；HF 需申请 PASSWORD |
| **EmoV-DB** | `1806.09514` / OpenSLR 115 | **★ 仅非商用**（Non-commercial Purposes） | ❌ | `LICENSE.md`：*"By downloading or using the EmoV-DB Dataset, you are agreeing to the 'Non-commercial Purposes' condition... If you wish to make use of the EmoV-DB Dataset for Commercial Purpose, please contact Prof. Sarah Ostadabbas"* |
| **ESD** | `2010.14794` / `2105.14762` | **[MISS]** 官方许可无法在线确认 | 未定 | 官方页 `hlj-group.github.io/ESD/` 404；3 个 GitHub 组织仓库全 404；HF 同名 ID 401；第三方镜像矛盾（`oxschaos/esd_dataset`=apache-2.0 / `DynamicSuperb/...`=mit / `duanyu027/ESD` 无 tag） |
| **CASIA 中文情感语料** | 无对应 arXiv 论文（v0.3 标「未找到」） | **[MISS]** 官方许可无法在线确认 | 未定 | `chineseldc.org` 超时、`casia.cn` SSL 信任失败；仅第三方 HF 镜像标 apache-2.0（非官方） |
| LibriTTS / VCTK | 公开 | 未在本轮核验 | 待定 | 保留待办 |
| Common Voice | Mozilla | 未在本轮核验 | 待定 | 保留待办 |

**原则（v0.3 收紧）**：公开数据仅用于「流水线验证 / 评测对照 / 通用能力」；专属音色训练数据必须自有授权，二者物理隔离（不同目录 + 不同 manifest 字段）。每条 manifest 强制 `license_id`。

- EmoV-DB 的 NC 属性与本项目 NC 定位**一致**（可作研究/评测数据），但**不得用于任何商业授权产物**。
- **ESD / CASIA 在官方许可确认前，不得进入训练数据**（连 manifest 都不建），仅列为 R-14b 法务跟进。
- AISHELL-3 / WenetSpeech 可商用，但 WenetSpeech 的 HF `gated=auto` 申请条款与 PASSWORD 条件需确认。

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

**v0.3 强化**：本轮核验发现 F5-TTS / fishaudio / coqui 同样存在「代码宽松、权重 NC 或受限」（见 §2），ADR-0001 的「选宽松许可权重」从单点发现变为**系统性规则**。轨道 A 三候选（CosyVoice 2 / Qwen3-TTS / VoxCPM2）经复核仍是代码与权重均 Apache-2.0 的干净选择，该决策不动摇。

## 7. 核验命令（可复核）

```bash
# 仓库许可证元数据
gh api repos/QwenAudio/CosyVoice --jq '[.full_name, .license.spdx_id, .stargazers_count] | @tsv'
gh api repos/index-tts/index-tts/license --jq '{name:.name, spdx:.spdx_id, size:.size}'

# LICENSE 原文（base64 → UTF-8）
gh api repos/SparkAudio/Spark-TTS/license --jq '.content' | base64 -d

# Hugging Face 权重卡 license（取 tags 与 cardData）
curl -s https://huggingface.co/api/models/SparkAudio/Spark-TTS-0.5B | jq '{tags:[.tags[]|select(startswith("license:"))], card:.cardData.license, gated:.gated}'
curl -s https://huggingface.co/api/models/SWivid/F5-TTS | jq '{tags:[.tags[]|select(startswith("license:"))], card:.cardData.license}'
curl -s https://huggingface.co/api/models/fishaudio/s2-pro | jq '{card:.cardData.license, name:.cardData.license_name}'
curl -s https://huggingface.co/api/models/IndexTeam/IndexTTS-2 | jq '{tags:[.tags[]|select(startswith("license:"))], card:.cardData.license}'

# coqui 权重限制（代码 MPL-2.0，权重另算）
curl -s https://raw.githubusercontent.com/coqui-ai/TTS/dev/TTS/.models.json | jq '{xtts_v2:.xtts_v2.license, your_tts:.your_tts.license}'

# 数据集许可原文
curl -s https://raw.githubusercontent.com/numediart/EmoV-DB/master/LICENSE.md | grep -i non-commercial
curl -s https://raw.githubusercontent.com/wenet-e2e/WenetSpeech/master/LICENSE | head -5
curl -s https://www.openslr.org/93/ | grep -i license

# PolyForm NC 官方纯文本
curl -s https://polyformproject.org/licenses/noncommercial/1.0.0.txt

# arXiv 发表状态（journal_ref 与 comment）
curl -s 'https://export.arxiv.org/api/query?id_list=2601.15621,2306.00814,2010.14794,2105.14762,1806.09514,2111.01606&max_results=20'
```

## 8. 待清零项（v0.3 状态）

### 8.1 已清零（v0.3 核验回填）

- [x] `SWivid/F5-TTS` 权重 → `cc-by-nc-4.0`
- [x] `IndexTeam/IndexTTS-2` 权重卡 → **确认无 license tag**（另补记 GitHub bilibili 自定义协议）
- [x] Fish Audio 权重 → `cc-by-nc-sa-4.0`（1.x）/ Fish Audio Research License（s2-pro）
- [x] HiFi-GAN 代码 → MIT；HF 权重许可不统一（已列明）
- [x] EmoV-DB → 仅非商用；AISHELL-3 → Apache-2.0；WenetSpeech → Apache-2.0（gated）
- [x] `coqui-ai/TTS` 权重 → CPML / CC-BY-NC-ND（代码 MPL-2.0 不代表权重）
- [x] Vocos → 代码与权重均 MIT；论文 `2306.00814`
- [x] Qwen3-TTS 技术报告 → `2601.15621`；ESD 论文 → `2010.14794` / `2105.14762`；EmoV-DB → `1806.09514`

### 8.2 R-14b：仍需人工 / 法务跟进（不阻塞文档与代码层工作）

1. **ESD 官方许可**：官方页 / GitHub / HF 全线 404/401，第三方镜像矛盾。
2. **CASIA 官方许可**：官方站点超时 / SSL 失败；arXiv 无对应语料论文。
3. **Coqui CPML 全文**：`coqui.ai/cpml` 404（关站），仅 `.models.json` 与 README 间接证据。
4. **fishaudio 精确权重 ID**：`fishaudio/fish-speech` / `OpenAudio-S1` 401/404，需确认 `s2-pro` 与 OpenAudio-S1 对应关系。
5. **RVC-Boss/GPT-SoVITS 官方权重卡**：org 下 0 模型、精确 ID 401。
6. **IndexTTS-2**：HF 无条款但 GitHub 有 bilibili 协议，需法务确认 HF 权重是否受约束。
7. **WenetSpeech**：HF `gated=auto` 申请条款与 PASSWORD 条件。
8. **13 篇论文**正式会议/期刊归属（arXiv `journal_ref` 全空，见 PAPERS.md）。
9. LibriTTS / VCTK / Common Voice 商用范围（本轮未核验）。

> **R-18 缓解**：每次升级或新增基座/依赖，**必须分别核验代码与权重许可**，同步更新本表与 `NOTICE`；模型卡强制 `base_license`（权重）字段；`license-check` CI 校验；提交信息填 `License:` footer（见 `COMMIT_CONVENTION.md`）。
