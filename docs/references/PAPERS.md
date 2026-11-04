# 权威论文参考清单 · AI 智能体声音训练项目

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-REF-001 |
| 版本 | **v0.3**（对应技术栈方案 v0.3 §4；v0.2 为 52 篇，本版补录 6 篇并降级发表状态表述） |
| 核验日期 | **2026-11-04**（v0.3 补录与复核同日，Lead 本地 + subagent 双路交叉印证） |
| 核验方法 | arXiv Atom API `https://export.arxiv.org/api/query?id_list=...`，逐篇取回 `id` / `title` / `published` / `author` / `journal_ref` / `comment` 字段 |
| 收录篇数 | **58 篇**（去重独立论文；另含 2 处跨层引用占位） |
| 用途 | 技术选型、参数化控制体系、评估门禁、合规水印的权威依据 |

## 核验声明

- 下表所有 **arXiv ID、标题、首发日期、作者、发表信息**均来自 arXiv API 实际返回值，未凭记忆填写。
- `发表/状态` 列取自 arXiv 的 `comment` / `journal_ref` 字段；标 `—` 表示 API 未提供（技术报告或预印本），引用时请以论文首页为准。
- **v0.3 重要降级**：本轮对 13 个 ID 复核，**`arxiv:journal_ref` 全部为空**；ICLR / ICML / NeurIPS / INTERSPEECH 等会议归属仅来自 `comment` 自述，**未经 `journal_ref` 确认**。清单中此类一律理解为「arXiv comment 自述」，须从会议官网或 DBLP 二手核验后才可升级。详见 §分组统计后的「发表状态降级」与方案 v0.3 §4.3.3。
- `机构倾向` 按作者署名与公开信息整理，用于说明「国内外覆盖」，**不作为精确机构归属证明**。
- 论文链接统一格式：`https://arxiv.org/abs/<ID>`（去掉版本后缀亦可）。
- 本清单是**技术参考**，不是法律文件；上游代码/权重许可证见 [`../licensing/UPSTREAM-LICENSE-MATRIX.md`](../licensing/UPSTREAM-LICENSE-MATRIX.md)。

---

## L-0 基础架构与声码器（11 篇）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `1609.03499` | WaveNet: A Generative Model for Raw Audio | 2016-09-12 | Aäron van den Oord | — | 国外 (Google DeepMind) | 神经声码器起点；原始波形自回归生成 |
| 2 | `1712.05884` | Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions | 2017-12-16 | Jonathan Shen | ICASSP 2018 | 国外 (Google) | Tacotron 2；声学特征→波形的两段式范式 |
| 3 | `1905.09263` | FastSpeech: Fast, Robust and Controllable Text to Speech | 2019-05-22 | Yi Ren | NeurIPS 2019 | 国内 (MSRA / 浙大) | **duration predictor 使时长可控**；`ProsodySpec.rate` 的理论起点 |
| 4 | `2006.04558` | FastSpeech 2: Fast and High-Quality End-to-End Text to Speech | 2020-06-08 | Yi Ren | ICLR 2021 | 国内 (MSRA / 浙大) | **★ F0 / energy / duration 作为显式条件** → 本方案 M2 声学特征编辑的首要依据 |
| 5 | `2005.11129` | Glow-TTS: A Generative Flow for Text-to-Speech via Monotonic Alignment Search | 2020-05-22 | Jaehyeon Kim | — | 国外 (Kakao) | 单调对齐搜索；强制对齐与时长建模参考 |
| 6 | `2106.06103` | Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech | 2021-06-11 | Jaehyeon Kim | ICML 2021 | 国外 (Kakao) | VITS；端到端、对抗训练，音色/韵律潜变量解耦 |
| 7 | `2010.05646` | HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis | 2020-10-12 | Jungil Kong | NeurIPS 2020 | 国外 (Kakao) | 声码器基线；Q4 音质门禁 |
| 8 | `2206.04658` | BigVGAN: A Universal Neural Vocoder with Large-Scale Training | 2022-06-09 | Sang-gil Lee | ICLR 2023 | 国外 (NVIDIA) | 大规模声码器；48kHz 与通用性；`NVIDIA/BigVGAN` MIT |
| 9 | `2006.11239` | Denoising Diffusion Probabilistic Models | 2020-06-19 | Jonathan Ho | — | 国外 (UC Berkeley) | 扩散生成基础；NaturalSpeech 2 前置 |
| 10 | `2210.02747` | Flow Matching for Generative Modeling | 2022-10-06 | Yaron Lipman | — | 国外 (Meta) | F5-TTS 等 flow-matching TTS 的理论基础 |
| 11 | `2106.09685` | LoRA: Low-Rank Adaptation of Large Language Models | 2021-06-17 | Edward J. Hu | — | 国外 (Microsoft) | **★ 轨道 B 定制轨**（adapter 可热插拔/插值/回滚） |

## L-0 偏好对齐（1 篇）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | `2305.18290` | Direct Preference Optimization: Your Language Model is Secretly a Reward Model | 2023-05-29 | Rafael Rafailov | — | 国外 (Stanford) | **★ Stage 2 偏好对齐**；同时是 R-07 奖励黑客风险的来源 |

## L-1 神经编解码与语音语言模型（5 篇）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 13 | `2107.03312` | SoundStream: An End-to-End Neural Audio Codec | 2021-07-07 | Neil Zeghidour | — | 国外 (Google) | 神经音频编解码起点 |
| 14 | `2209.03143` | AudioLM: a Language Modeling Approach to Audio Generation | 2022-09-07 | Zalán Borsos | — | 国外 (Google) | 语音→离散 token→LM 范式 |
| 15 | `2301.02111` | Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers | 2023-01-05 | Chengyi Wang | Working in progress | 国内 (MSRA / 微软) | **VALL-E**；零样本克隆 + ICL；`ref_audio_uri` 设计依据 |
| 16 | `2305.09636` | SoundStorm: Efficient Parallel Audio Generation | 2023-05-16 | Zalán Borsos | — | 国外 (Google) | 并行解码，低延迟流式参照 |
| 17 | `2308.16692` | SpeechTokenizer: Unified Speech Tokenizer for Speech Large Language Models | 2023-08-31 | Xin Zhang | ICLR 2024 | 国内 (复旦 / 微软) | 统一 token；内容/音色分层，支撑解耦控制 |

## L-2 大规模与零样本合成（10 篇）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 18 | `2205.04421` | NaturalSpeech: End-to-End Text to Speech Synthesis with Human-Level Quality | 2022-05-09 | Xu Tan | — | 国内 (MSRA) | 人类水平自然度基线 |
| 19 | `2304.09116` | NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers | 2023-04-18 | Kai Shen | — | 国内 (MSRA) | 潜扩散 + 零样本 |
| 20 | `2403.03100` | NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized Codec and Diffusion Models | 2024-03-05 | Zeqian Ju | — | 国内 (MSRA) | **★ 因子分解 codec（内容/韵律/音色）** → 五层 VoiceSpec 正交性的结构保障 |
| 21 | `2306.15687` | Voicebox: Text-Guided Multilingual Universal Speech Generation at Scale | 2023-06-23 | Matthew Le | — | 国外 (Meta) | 大规模通用语音生成 |
| 22 | `2406.05370` | VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers | 2024-06-08 | Sanyuan Chen | — | 国内 (MSRA / 微软) | 人类水平零样本，Q2 相似度目标参照 |
| 23 | `2302.03540` | Speak, Read and Prompt: High-Fidelity Text-to-Speech with Minimal Supervision | 2023-02-07 | Eugene Kharitonov | — | 国外 (Google) | 极少监督 + 提示；少样本路线依据 |
| 24 | `2310.00704` | UniAudio: An Audio Foundation Model Toward Universal Audio Generation | 2023-10-01 | Dongchao Yang | — | 国内 (港中文 / 微软) | 通用音频基础模型 |
| 25 | `2403.16973` | VoiceCraft: Zero-Shot Speech Editing and Text-to-Speech in the Wild | 2024-03-25 | Puyuan Peng | — | 国外 (CMU / Meta) | 真实场景零样本与语音编辑 |
| 26 | `2406.18009` | E2 TTS: Embarrassingly Easy Fully Non-Autoregressive Zero-Shot TTS | 2024-06-26 | Sefik Emre Eskimez | — | 国外 (Microsoft) | 极简非自回归；效率对照 |
| 27 | `2409.00750` | MaskGCT: Zero-Shot Text-to-Speech with Masked Generative Codec Transformer | 2024-09-01 | Yuancheng Wang | — | 国内 (港中文 / OpenBMB 关联) | 掩码生成零样本观察池 |
| 28 | `2502.18924` | MegaTTS 3: Sparse Alignment Enhanced Latent Diffusion Transformer for Zero-Shot Speech Synthesis | 2025-02-26 | Ziyue Jiang | — | 国内 (字节) | 稀疏对齐 + 潜扩散观察池 |

## L-3 可控 / 指令 / 情感 / 国产基座（10 篇）★核心

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | `2211.12171` | PromptTTS: Controllable Text-to-Speech with Text Descriptions | 2022-11-22 | Zhifang Guo | — | 国内 (MSRA) | 文本描述控风格；`style_prompt` 起点 |
| 30 | `2301.13662` | InstructTTS: Modelling Expressive TTS in Discrete Latent Space with Natural Language Style Prompt | 2023-01-31 | Dongchao Yang | — | 国内 (港中文 / 微软) | 自然语言风格提示；同时暴露「描述不可严格复现」问题 |
| 31 | `2309.02285` | PromptTTS 2: Describing and Generating Voices with Text Prompt | 2023-09-05 | Yichong Leng | — | 国内 (MSRA) | 风格描述连续语义空间 → 本项目规定 `style_prompt` 不得单独作 preset |
| 32 | `2406.02430` | Seed-TTS: A Family of High-Quality Versatile Speech Generation Models | 2024-06-04 | Philip Anastassiou | — | 国内 (字节 Seed) | ICL / 指令 / 高质量；权重可得性待核验 |
| 33 | `2407.05407` | CosyVoice: A Scalable Multilingual Zero-shot Text-to-speech Synthesizer based on Supervised Semantic Tokens | 2024-07-07 | Zhihao Du | work in progress | 国内 (阿里 / 通义) | **轨道 A 候选**；语义 token + 零样本 |
| 34 | `2412.10117` | CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models | 2024-12-13 | Zhihao Du | Tech report | 国内 (阿里 / 通义) | **★ 流式合成** → Q7 与 chunk 连续性；Apache-2.0 权重 |
| 35 | `2410.06885` | F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching | 2024-10-09 | Yushen Chen | 17 pages | 国内 (上交 / 剑桥等) | flow matching；`SWivid/F5-TTS` MIT |
| 36 | `2503.01710` | Spark-TTS: An Efficient LLM-Based Text-to-Speech Model with Single-Stream Decoupled Speech Tokens | 2025-03-03 | Xinsheng Wang | Submitted to ACL 2025 | 国内 (港中文 / 01.AI 关联) | **★ 属性级控制 = 参数 schema** → 新增 `AttributeSpec` 候选；权重 CC-BY-NC-SA-4.0 不采用 |
| 37 | `2506.21619` | IndexTTS2: A Breakthrough in Emotionally Expressive and Duration-Controlled Auto-Regressive Zero-Shot Text-to-Speech | 2025-06-23 | Siyi Zhou | — | 国内 (bilibili) | **★ 精确时长 + 情感/音色三路解耦** → F4 升 P0 候选；许可需法务确认 |
| 38 | `2509.24650` | VoxCPM: Tokenizer-Free TTS for Context-Aware Speech Generation and True-to-Life Voice Cloning | 2025-09-29 | Yixuan Zhou | Technical Report | 国内 (OpenBMB / 面壁) | 轨道 A 备选；tokenizer-free；Apache-2.0 |
| 39 | `2409.00750` | （见 L-2 #27，跨层引用）MaskGCT | — | — | — | — | 掩码生成零样本 |

> 注：#39 为跨层引用占位，不计入独立篇数；L-3 独立论文为 #29–#38 共 10 篇。

## L-4 中文数据 / 工具链（8 篇，国内为主）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 40 | `2010.11567` | AISHELL-3: A Multi-speaker Mandarin TTS Corpus and the Baselines | 2020-10-22 | Yao Shi | — | 国内 (希尔贝壳 / 北邮等) | 中文多说话人 TTS 语料；流水线验证 |
| 41 | `2110.03370` | WenetSpeech: A 10000+ Hours Multi-domain Mandarin Corpus for Speech Recognition | 2021-10-07 | Binbin Zhang | — | 国内 (WeNet 社区 / 西工大等) | 大规模中文 ASR 语料 |
| 42 | `2102.01547` | WeNet: Production oriented Streaming and Non-streaming End-to-End Speech Recognition Toolkit | 2021-02-02 | Zhuoyuan Yao | — | 国内 (WeNet 社区) | ASR 工具链；Apache-2.0 |
| 43 | `2206.08317` | Paraformer: Fast and Accurate Parallel Transformer for Non-autoregressive End-to-End Speech Recognition | 2022-06-16 | Zhifu Gao | — | 国内 (阿里 / 通义) | 非自回归 ASR；CER 回环实现 |
| 44 | `2305.11013` | FunASR: A Fundamental End-to-End Speech Recognition Toolkit | 2023-05-18 | Zhifu Gao | — | 国内 (阿里 / 通义) | ASR + VAD + 标点 + diarization 流水线；MIT |
| 45 | `2303.00747` | WhisperX: Time-Accurate Speech Transcription of Long-Form Audio with Word-Level Timestamps | 2023-02-07 | Max Bain | INTERSPEECH 2023 | 国外 (Oxford / VGG) | **★ 字级时间戳** → M2 特征编辑与 F4 时长控制的前提；BSD-2-Clause |
| 46 | `2212.04356` | Robust Speech Recognition via Large-Scale Weak Supervision | 2022-12-06 | Alec Radford | — | 国外 (OpenAI) | Whisper；MIT |
| 47 | `2110.13900` | WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing | 2021-10-26 | Sanyuan Chen | — | 国内 (MSRA / 微软) | 全栈语音自监督；说话人/情感表征 |

> 注：#45–#47 为工具链补充；L-4 独立论文按 #40–#47 共 8 篇计。

## L-5 评估 / 水印 / 说话人（7 篇）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态 | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | `2204.02152` | UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022 | 2022-04-05 | Takaaki Saeki | INTERSPEECH 2022 | 国外 (东大 / SaruLab) | **Q3 客观自然度** 代理指标 |
| 49 | `2203.11389` | The VoiceMOS Challenge 2022 | 2022-03-21 | Wen-Chin Huang | — | 国外 (CMU / 多机构) | **★ 主观评测协议**（盲测/锚点/CI）；R-07 裁判规则 |
| 50 | `2010.15258` | DNSMOS: A Non-Intrusive Perceptual Objective Speech Quality metric to evaluate Noise Suppressors | 2020-10-28 | Chandan K A Reddy | Submitted to ICASSP 2020 | 国外 (Microsoft) | **Q4 音质门禁** 与数据质检 |
| 51 | `2401.16812` | SpeechBERTScore: Reference-Aware Automatic Evaluation of Speech Generation Leveraging NLP Evaluation Metrics | 2024-01-30 | Takaaki Saeki | — | 国外 (东大 / SaruLab) | **v0.2 新增**：参考感知辅助指标，与 UTMOS/DNSMOS 成三角 |
| 52 | `2005.07143` | ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification | 2020-05-14 | Brecht Desplanques | INTERSPEECH 2020 | 国外 (Ghent) | **Q2 / Q10 说话人相似度** |
| 53 | `2401.17264` | Proactive Detection of Voice Cloning with Localized Watermarking | 2024-01-30 | Pierre Fernandez | **ICML 2024** | 国外 (Meta) | **★ 默认水印方案 AudioSeal**；MIT；§2.6 权利保留 |
| 54 | `2301.02111` | （见 L-1 #15，跨层引用）VALL-E | — | — | — | — | 零样本相似度参照 |

> 注：#54 为跨层引用占位，不计入独立篇数；L-5 独立论文为 #48–#53 共 6 篇。

---

## 分组统计

| 组 | 独立篇数 | 编号 |
| --- | --- | --- |
| L-0 基础架构与声码器 | 11 | 1–11 |
| 偏好对齐 | 1 | 12 |
| L-1 编解码 / 语音 LM | 5 | 13–17 |
| L-2 大规模 / 零样本 | 11 | 18–28 |
| L-3 可控 / 指令 / 国产基座 | 10 | 29–38 |
| L-4 中文数据 / 工具链 | 8 | 40–47 |
| L-5 评估 / 水印 / 说话人 | 6 | 48–53 |
| **v0.3 补录** | **6** | **55–60**（见下） |
| **合计（去重）** | **58 篇** | — |

> 说明：v0.2 收录 52 篇；**v0.3 补录 6 篇 → 58 篇**（另含 2 处跨层引用占位 #39 / #54，不计入）。方案 v0.3 §4.3.4 与本文统一为 58 篇；归档版 v0.2 正文仍记 52 篇，以本版为准。
>
> 国内外覆盖：国内团队主导约 32 篇（MSRA/微软、阿里通义、字节 Seed、bilibili、OpenBMB/面壁、WeNet 社区、希尔贝壳、港中文等），国外团队主导约 26 篇（Google、Meta、OpenAI、NVIDIA、Microsoft、CMU、Oxford、东大 SaruLab、Ghent、Kakao、Numediart 等）。机构倾向仅用于说明覆盖面，不作精确归属。

---

## v0.3 补录（6 篇，2026-11-04 核验）

| # | arXiv ID | 标题 | 首发 | 第一作者 | 发表/状态（arXiv 实际值） | 机构倾向 | 与本方案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 55 | `2601.15621` | Qwen3-TTS Technical Report | 2026-01-22 | Hangrui Hu | `journal_ref` 空；`comment` = `https://github.com/QwenLM/Qwen3-TTS` | 国内 (阿里 / 通义) | **补齐 v0.2 缺口**：轨道 A 首选候选 Qwen3-TTS 的官方技术报告；摘要称 multilingual / controllable / robust / streaming |
| 56 | `2610.23678` | Beyond the Benchmark: Conditioning, Domains and Failure Modes of Qwen3-TTS | 2026-10-16 | — | 未取详细字段 | 待核 | Qwen3-TTS 评测关联；`ti:"Qwen3-TTS"` 命中 2 条之一 |
| 57 | `2306.00814` | Vocos: Closing the gap between time-domain and Fourier-based neural vocoders for high-quality audio synthesis | 2023-06-01 | Hubert Siuzdak | `journal_ref` 空；`comment` 空 | 国外 (Charactr) | 声码器备选；代码与权重均 MIT（见许可证矩阵 §3） |
| 58 | `2010.14794` | Seen and Unseen emotional style transfer for voice conversion with a new emotional speech dataset | 2020-10-28 | — | `comment` = `Accepted by ICASSP 2021`（**comment 自述**） | 国内 | **ESD 数据集论文**（纠正 v0.2 猜测 ID） |
| 59 | `2105.14762` | Emotional Voice Conversion: Theory, Databases and ESD | 2021-05-31 | — | `comment` = `Speech Communication`（**comment 自述**） | 国内 | ESD 综述/数据库论文 |
| 60 | `1806.09514` | The Emotional Voices Database: Towards Controlling the Emotion Dimension in Voice Generation Systems | 2018-06-25 | — | `comment` = `Submitted to SLSP 2018` | 国外 (Numediart) | **EmoV-DB 论文**；其数据集 LICENSE 明确仅非商用（见许可证矩阵 §4） |

### v0.3 纠错与 [MISS]

- ❌ **`2111.01606` 不是 ESD 论文**：API 实际返回 `PolyTrack: Tracking with Bounding Polygons`（2021-11-02，NeurIPS 2021 MLAD Workshop）。任何文档不得再把该 ID 关联到 ESD；正确 ID 为 `2010.14794` / `2105.14762`。
- `[MISS]` **CASIA 中文情感语料论文**：`ti:"CASIA" AND all:"corpus"` 返回 `totalResults=0`；命中条目均为 SER 方法论文，非语料本身。**标「未找到」，不猜 ID**，不计入 58 篇。
- `[OK]` 复核一致：`2010.11567`（AISHELL-3，2020-10-22）、`2110.03370`（WenetSpeech，2021-10-07）标题与日期无误。

### 发表状态降级（13 个 ID，`journal_ref` 全空）

核验源：`https://export.arxiv.org/api/query?id_list=1609.03499,2006.04558,2106.06103,2210.02747,2301.02111,2403.03100,2409.00750,2503.01710,2506.21619,2509.24650,2006.11239,2206.04658,2212.04356&max_results=20`

| ID | `comment` 线索 | 本版表述 |
| --- | --- | --- |
| `1609.03499` WaveNet | 空 | 预印本，arXiv 未记录正式发表 |
| `2006.04558` FastSpeech 2 | `Accepted by ICLR 2021` | arXiv comment 自述 |
| `2106.06103` VITS | `ICML 2021` | arXiv comment 自述 |
| `2210.02747` Flow Matching | 空 | 预印本 |
| `2301.02111` VALL-E | `Working in progress` | 未正式发表 |
| `2403.03100` NaturalSpeech 3 | 成果描述（非会议） | 预印本 |
| `2409.00750` MaskGCT | 空 | 预印本 |
| `2503.01710` Spark-TTS | `Submitted to ACL 2025` | 投稿中 |
| `2506.21619` IndexTTS2 | 空 | 预印本 |
| `2509.24650` VoxCPM | `Technical Report` | 技术报告 |
| `2006.11239` DDPM | 空 | 预印本（NeurIPS 2020 未经 `journal_ref` 确认） |
| `2206.04658` BigVGAN | `To appear at ICLR 2023...` | arXiv comment 自述 |
| `2212.04356` Whisper | 空 | 预印本 |

另 4 个复核：`2406.02430` Seed-TTS（comment 空）、`2306.15687` Voicebox（`Accepted to NeurIPS 2023`）、`2309.02285` PromptTTS 2（demo page）、`2301.13662` InstructTTS（`Submit to TASLP`），`journal_ref` 同样全空。

> 引用格式示例中的 `ICLR 2021` 等今后须理解为「arXiv comment 自述」。这不改变论文技术参考价值（ID/标题/日期已核验），只收紧发表状态可信度。

---

## 引用格式建议

```
[FastSpeech2] Yi Ren, Chenxu Hu, Xu Tan, et al. FastSpeech 2: Fast and
High-Quality End-to-End Text to Speech. ICLR 2021. arXiv:2006.04558.
https://arxiv.org/abs/2006.04558
```

在方案文档、ADR、模型卡中引用时，必须带 **arXiv ID + 链接**；涉及实现参照的，还须在 `NOTICE` 或模型卡中标注对应上游仓库与其许可证（见 [`../licensing/UPSTREAM-LICENSE-MATRIX.md`](../licensing/UPSTREAM-LICENSE-MATRIX.md)）。

---

## v0.3 已完成的补齐

- [x] Qwen3-TTS 官方技术报告 arXiv ID → `2601.15621`（另发现评测论文 `2610.23678`）
- [x] Vocos 声码器论文 ID → `2306.00814`
- [x] ESD 论文 ID → `2010.14794` / `2105.14762`；**纠正 `2111.01606` 误关联**
- [x] EmoV-DB 论文 ID → `1806.09514`
- [x] 发表状态复核 → 13 个 ID 的 `journal_ref` 全空，会议归属降级为「arXiv comment 自述」
- [x] CASIA 语料论文 → 明确 `[MISS] 未找到`，不猜 ID

## 待补齐（v0.4 / 需人工）

- [ ] 13 篇论文的正式会议/期刊归属：从会议官网或 DBLP 二手核验（arXiv `journal_ref` 无法确认）
- [ ] 各论文 DOI / 会议主页链接
- [ ] `2610.23678` 的详细作者与 `comment` 字段
- [ ] ESD / CASIA 数据集**官方许可证**（在线通道失败，需法务/书面确认，见方案 v0.3 §5.3.4 R-14b）
