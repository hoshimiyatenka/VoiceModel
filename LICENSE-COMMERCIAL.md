# 商业授权（Commercial Licensing）

> 本文件说明「不得商业化」原则下的**例外通道**。它不是许可文本本身；
> 公众许可条款以仓库根目录 [`LICENSE`](LICENSE)（PolyForm Noncommercial 1.0.0 官方全文）为准。
> **本文件与 `LICENSE` / `NOTICE` 同属受保护路径，变更需法务 + maintainer 双人批准。**

## 1. 为什么需要这份文件

本项目采用 **开放权重 + 非商业许可**：源码与权重公开可得，但任何商业目的使用
默认不允许。版权持有人（项目方）保留向特定主体**单独授予商业许可**的权利
（双授权 / dual licensing）——这正是「保留一定权力」的落地机制。

PolyForm NC 1.0.0 的 `No Other Rights` 条款明确不阻止 licensor 向他人另行授权：
*"these terms do not ... prevent the licensor from granting licenses to anyone else"*。

## 2. 哪些用途必须申请授权

| 类别 | 典型场景 | 默认 | 需要 |
| --- | --- | --- | --- |
| 研究 / 个人 / 教育 / 公益 / 政府 | 毕设、个人 demo、高校实验室、非营利科普 | ✅ 允许（依 `LICENSE`） | — |
| 嵌入付费产品 | 收费 App、付费软件、游戏内角色语音、硬件内置 | ❌ 禁止 | ✅ 商业授权 |
| 对外提供语音生成服务 | API / SDK / 托管服务 / TTS 网站 / 语音克隆平台 | ❌ 禁止 | ✅ 商业授权 |
| 企业内部业务运营 | 客服机器人、内部播报、企业培训系统 | ❌ 禁止 | ✅ 商业授权 |
| 直接或间接产生收入 | 带广告内容、直播、有声书售卖、商业配音交付 | ❌ 禁止 | ✅ 商业授权 |
| 再分发衍生权重 | 把本项目微调权重打包进商业发行物 | ❌ 禁止 | ✅ 商业授权 |

> 边界 FAQ（待法务定稿，D11）：公益组织接受商业赞助、开源项目接受捐赠、
> 个人作品后续意外产生收益等情形，需在法务批准后补充到本节。

## 3. 授权范围（待法务填写具体条款）

一次商业授权至少需明确以下字段，缺一不可：

```
Licensee:          <主体全称>
Scope:             <内部使用 / 产品集成 / 托管服务 / 再分发>
Territory:         <地域>
Term:              <期限，是否可续约>
Models/Assets:     <授权覆盖的 checkpoint / preset / 音色 ID，按 commit 锁定>
Exclusivity:       <独占 / 非独占>
Sublicense:        <是否允许再许可>
Attribution:       <NOTICE 与 "AI 合成" 标识义务>
Watermark:         <是否允许关闭；默认不允许>
Fee / Royalty:     <占位，由商务确定>
Audit:             <使用量上报与审计方式>
Termination:       <违约/超范围时的终止与删除义务>
```

## 4. 申请流程（草案）

1. 提交申请：说明主体、用途、规模、覆盖的模型/音色、预计时长。
2. 合规预审：确认用途不涉及未授权声音克隆、冒充、去水印等禁止事项
   （见 `NOTICE` §4）。
3. 法务起草：按 §3 字段生成书面协议，**不得口头授权**。
4. 双方签署 → 发放授权凭证（`LICENSE-COMMERCIAL-<id>.md` 或签附件）。
5. 登记：写入商业授权台账（私有，不入库），并在被授权模型卡中标注
   `commercial_license: <id>`。

> **不入库原则**：协议正文、价格、被授权方信息属商业机密，仅存私有台账；
> 公开仓库只保留本说明与授权编号引用。发布前须过 `leak_guard`。

## 5. 与上游许可的关系（重要）

商业授权**仅覆盖本项目自有增量**（代码、控制层、preset、标注、LoRA
/adapter、微调权重、音色资产、文档）。上游基座权重依其自身许可
（多为 Apache-2.0）另行对待；项目方不对上游原作品主张限制或收费。

若被授权方使用的是带额外限制的上游组件（例如 IndexTTS2 的
bilibili 许可、Fish Audio Community License 的 Hosted Service 限制、
Spark-TTS 权重的 CC-BY-NC-SA-4.0），**还需自行取得该上游权利人的许可**。
详见 [`docs/licensing/UPSTREAM-LICENSE-MATRIX.md`](docs/licensing/UPSTREAM-LICENSE-MATRIX.md)。

## 6. 联系入口（占位，P0 填写）

```
Commercial licensing:  <待填写邮箱>
Legal / compliance:    <待填写邮箱>
Project:               https://github.com/hoshimiyatenka/VoiceModel
```

## 7. 状态

| 项 | 状态 |
| --- | --- |
| 许可选型（PolyForm NC 1.0.0） | ✅ 已核验官方原文并落地 |
| 商业化边界 FAQ | ⏳ 待法务定稿（D11，P0 阻塞项） |
| 书面协议模板 | ⏳ 待起草 |
| 定价与商务流程 | ⏳ 待确定 |
| 双授权台账 | ⏳ 待建立（私有） |

> **发布前门禁**：在 D11 法务书面批准之前，不得对外发布模型权重
> （文档与代码可先行公开）。原因：许可条款一经分发即对已分发副本生效，
> 事后收紧条款不溯及既往。
