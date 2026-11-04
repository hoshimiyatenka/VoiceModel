# 许可与合规实施清单 · 实施规格

| 项 | 内容 |
| --- | --- |
| 文档编号 | VM-IMPL-009 |
| 版本 | v0.4 |
| 日期 | 2026-11-04 |
| 关联主方案 | [docs/AI智能体声音训练项目_技术栈方案_v0.4.md](../../AI智能体声音训练项目_技术栈方案_v0.4.md) §12 / §3.3 G0-2 / §3.3 G0-3 |
| 状态 | 实施规格（Phase 0 模板，未实测） |
| 职责 | 把 D11 法务定稿、R-14b 跟进、模型卡许可字段、发布前检查变成可执行清单；本文件不替代法务意见 |

> **Phase 0 声明**：本文件是清单与流程，**不是法律意见，也不代表 D11 已签字**。[LICENSE](../../../LICENSE) 为 PolyForm Noncommercial 1.0.0 官方逐字原文，**禁止改写**；[NOTICE](../../../NOTICE) 与 [LICENSE-COMMERCIAL.md](../../../LICENSE-COMMERCIAL.md) 为待定稿文件。D11 未签字前**不发布任何模型权重**（G0-2，许可一经分发不溯及既往）。

## 1. 权利结构（不得改写，主方案 §12.1）

| 层 | 许可 | 边界 |
| --- | --- | --- |
| 项目自有增量 | **PolyForm Noncommercial 1.0.0** + 双授权 | 代码 / VoiceSpec 契约 / preset / 词典 / 标注 / golden_set / LoRA / adapter / 微调权重 / 模型卡 / 文档 / 音色资产；禁商用 |
| 上游 Apache-2.0 原权重 | 第三方仍可按原条款商用 | 依据 Apache-2.0 §4：可对修改与衍生作品整体附加不同条款，但须保留归因、不得剥夺第三方对上游原作权利；**NC 不覆盖上游** |
| 双授权依据 | `No Other Rights` 条款 | 原文 `these terms do not ... prevent the licensor from granting licenses to anyone else` → licensor 保留单独授予商业许可权 |
| 对外称谓 | 开放权重 / 源码可得（source-available, open-weight） | **不称 OSI 开源**：OSD 第 6 条 "No Discrimination Against Fields of Endeavor" 禁止按用途领域歧视 |

## 2. D11 法务定稿清单（P0 阻塞，L-1–L-6）

| # | 事项 | 交付物 | 落地路径 | 当前 |
| --- | --- | --- | --- | --- |
| L-1 | 商业化边界 FAQ | 「商业使用」定义、MAU / 营收口径、内部研究例外、Hosted Service 边界 | `docs/legal/COMMERCIAL-FAQ.md`（v0.5） | ❌ |
| L-2 | 商业授权书面协议模板 | 范围 / 期限 / 费率 / 归因 / 终止 / 管辖 | [LICENSE-COMMERCIAL.md](../../../LICENSE-COMMERCIAL.md) 定稿 | 草案 |
| L-3 | `NOTICE` 上游归因清单逐项签字 | 每个上游组件的版权人、许可、URL、修改声明 | [NOTICE](../../../NOTICE) | 草案 |
| L-4 | 双授权条款与 PolyForm NC 兼容性复核 | 法务意见书（尤其 NC 与商业例外并存） | `docs/legal/` | ❌ |
| L-5 | 模型卡许可字段模板 | `base_license` / `weight_license` / `delta_license` 三段 | `docs/model-cards/` 规范（§5） | ❌ |
| L-6 | 水印与「关闭需授权」合规说明 | `E-LICENSE-001` 的合规依据、授权凭证格式 | [法务规格](LICENSING-IMPLEMENTATION-SPEC.md) §6 + API-SPEC | 部分 |

> 改 `LICENSE` / `NOTICE` / `LICENSE-COMMERCIAL.md` 的提交必须带 `License-Review: <法务批准人>` footer 并受 CODEOWNERS 保护（[COMMIT_CONVENTION.md](../../../COMMIT_CONVENTION.md) §5/§6、`license-check.yml`）。

## 3. R-14b 法务跟进清单（九项，主方案 §12.3）

| # | 待跟进 | 现状 | 处理原则 | 阻塞级别 |
| --- | --- | --- | --- | --- |
| 1 | ESD 官方许可 | 官方页 404 / GitHub 404 / HF 401；第三方镜像矛盾（apache-2.0 / mit / 无 tag） | 书面询问官方或替换数据集；**不得假定可商用** | G0-3 |
| 2 | CASIA 中文情感语料官方许可 | chineseldc.org 超时 / casia.cn SSL 失败；仅第三方镜像 apache-2.0 | 书面询问或替换 | G0-3 |
| 3 | Coqui CPML 全文 | `https://coqui.ai/cpml` 404（关站）；仅 `.models.json` 间接证据 `CPML, tos_required=true` | **不用其权重** | 已规避 |
| 4 | fishaudio 精确权重 ID | `fish-speech` / `OpenAudio-S1` 401/404；s2-pro 为 Fish Audio Research License（仅研究） | 不进候选 | 已规避 |
| 5 | RVC-Boss/GPT-SoVITS HF 权重卡 | org 下 0 模型、精确 ID 401；代码 MIT | 权重许可独立确认前不用 | 已规避 |
| 6 | charactr/vocos | GitHub 404 / HF 401（已迁 `gemelo-ai/vocos`，代码与权重 MIT） | 用迁移后 ID 复核 | 低 |
| 7 | IndexTTS-2 HF 权重约束 | HF 无 license tag；GitHub bilibili Model Use License Agreement（1 亿 MAU / 10 亿 RMB 门槛、禁用于改进其他 AI 模型） | 法务确认 HF 权重是否受约束 | 已规避（非轨道 A） |
| 8 | WenetSpeech 申请条款 | GitHub Apache-2.0，HF `gated=auto` 需申请 PASSWORD | 记录申请条款与获批范围 | 中 |
| 9 | 论文会议归属 | 13 个 ID `journal_ref` 全空，仅 comment 自述 | 会议官网 / DBLP 二手核验；引用不写「已确认正式发表」 | 低 |

> 「已规避」= 该组件不在轨道 A 三候选与当前数据计划内，故不阻塞实施；但不等于已清零，仍登记在案。

## 4. R-18 防线（代码许可 ≠ 权重许可）

| 组件 | 代码许可 | 权重 / 发行许可 | 结论 |
| --- | --- | --- | --- |
| F5-TTS | MIT | `cc-by-nc-4.0`（禁商用） | 按代码推断可商用会出错 |
| fishaudio | Fish Audio Community License v1.0 | `cc-by-nc-sa-4.0`（1.x）/ Fish Audio Research License（s2-pro） | SA 传染 / 仅研究 |
| coqui-ai/TTS | MPL-2.0 | CPML（`tos_required=true`）/ `CC BY-NC-ND 4.0`（YourTTS） | 权重另有限制 |
| Spark-TTS | Apache-2.0 | `cc-by-nc-sa-4.0` | **不用其权重作发布基座**（ADR-0001，SA 传染阻断自定义商业例外） |
| CosyVoice 2 / Qwen3-TTS / VoxCPM2 | Apache-2.0 | Apache-2.0 | **轨道 A 三候选，干净**（D19） |

守卫：
- [许可证矩阵](../../licensing/UPSTREAM-LICENSE-MATRIX.md) 已拆「代码许可 / 权重发行许可」两列。
- 模型卡强制三段许可字段（§5）。
- `license-check.yml` 守住 `LICENSE` / `NOTICE` / 受保护路径与二进制文件类型。
- 任何新增第三方依赖 / 基座 / 数据集须在提交 footer 声明 `License: <spdx>`（[COMMIT_CONVENTION.md](../../../COMMIT_CONVENTION.md) §5）。

## 5. 模型卡许可字段模板（L-5）

| 字段 | 含义 | 必填 |
| --- | --- | --- |
| `model_id` | `model-<base>-<stage>-<step>-<score>` | ✅ |
| `base_model` | 定型基座 ID + commit + 来源 URL | ✅ |
| `base_license` | 上游基座**代码**许可 SPDX | ✅ |
| `weight_license` | 上游基座**权重**发行许可（R-18 关键，不得留空或照抄代码许可） | ✅ |
| `delta_license` | 项目自有增量许可 = `PolyForm-Noncommercial-1.0.0` | ✅ |
| `upstream_attribution` | 指向 `NOTICE` 对应条目 | ✅ |
| `commercial_license_ref` | 商业授权入口（[LICENSE-COMMERCIAL.md](../../../LICENSE-COMMERCIAL.md)） | ✅ |
| `watermark` | 默认 `true`；关闭需授权凭证 | ✅ |
| `dataset_manifests` | 训练数据来源 `ds-*` + 各自 `license_id` | ✅ |
| `gate_report` | 通过的 `gs-*` | ✅ |
| `capability_flags` | Phase 2 实测回填 | Phase 2 |

> `weight_license` 与 `base_license` 必须分别填写；二者相同也要各写一行，防止回退到「按代码推断」。

## 6. 水印与音色鉴权（E-LICENSE-001 / 002）

| 项 | 规则 | 落点 |
| --- | --- | --- |
| 水印默认 | `render.watermark=true`（schema 单一真源） | [voicespec.schema.json](../../../configs/voicespec/voicespec.schema.json) |
| 关闭水印 | 需商业授权凭证，否则 `E-LICENSE-001` 拒绝 | [API-SPEC](../control/API-SPEC.md) |
| 水印实现 | AudioSeal（`2401.17264`, ICML 2024, MIT） | [DEPLOYMENT-SPEC](../serve/DEPLOYMENT-SPEC.md) |
| 水印审计 | `audit.watermark_id` 全链路 | [CONTROL-LAYER-SPEC](../control/CONTROL-LAYER-SPEC.md) |
| 音色鉴权 | `ref_audio_uri` 必须指向已注册 / 已授权说话人，否则 `E-LICENSE-002` | 同上 |

## 7. 发布前检查单（G0-2 守门）

| # | 检查 | 通过条件 |
| --- | --- | --- |
| 1 | D11 法务签字 | L-1–L-6 全部有签字版 |
| 2 | `LICENSE` 完整性 | `license-check.yml` 全绿（PolyForm NC 1.0.0 官方原文、Required Notice、32 days） |
| 3 | `NOTICE` 归因 | 每个上游组件逐项列明且签字 |
| 4 | 模型卡 | 三段许可字段齐全、`weight_license` 已独立核验 |
| 5 | 数据集 | 每条 `license_id` + 授权书引用；R-02 物理隔离 |
| 6 | R-14b | 九项有书面结论（询问 / 替换 / 不采用） |
| 7 | 水印 | 覆盖率 100%（无授权场景） |
| 8 | `leak_guard` | 0 条 critical/high 发现 |
| 9 | 门禁报告 | `gs-*` 硬指标全过 |
| 10 | 提交规范 | `License-Review:` / `License:` footer 齐全 |

> **任一不过 → 不发布权重。** 本清单是流程闸门，不替代法务意见；L-4 兼容性复核须由法务出具书面结论。

## 8. Phase 0 边界与 v0.5 待办

- 本版：清单、字段模板、检查单落盘；**D11 未签字**，所有 LICENSE 相关文件保持 v0.2 状态不改。
- v0.5：L-1–L-6 定稿、`NOTICE` 签字、R-14b 九项处理结论、模型卡模板实例化。
- v1.0：G0-2 通过 → 允许进入权重发布流程。
