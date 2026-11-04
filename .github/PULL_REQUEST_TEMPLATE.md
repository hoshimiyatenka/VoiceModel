## 变更概述

<!-- 一句话说明「为什么」，不是「改了什么」（diff 已有） -->

## 变更类型

- [ ] `feat` 新能力 / `fix` 缺陷
- [ ] `docs` 文档（方案 / 论文 / 模型卡）
- [ ] `model` / `voice` / `data` 模型、音色资产、数据
- [ ] `eval` / `train` / `perf` 评估、训练、性能
- [ ] `license` 许可与归因
- [ ] `ci` / `build` / `chore` / `refactor` / `test` / `revert`

## 影响勾选（必填）

- [ ] 是否影响 **门禁阈值** → 需 `Gate-Report:` + maintainer 批准
- [ ] 是否影响 **preset / 发音词典** → 需 `Gate-Report:` + `Preset:`
- [ ] 是否影响 **模型卡 / 权重** → 需 `Model:` + `License:`
- [ ] 是否影响 **许可 / NOTICE / 归因** → 需 `License-Review:`（法务 + 2 maintainer）
- [ ] 是否新增 / 更新 **第三方依赖、基座或数据集** → 已同步 `NOTICE` 与 `docs/licensing/UPSTREAM-LICENSE-MATRIX.md`
- [ ] 是否涉及 **golden_set** → ⚠️ 冻结路径，禁止修改；CI 会直接失败
- [ ] 是否包含 **音频实体 / checkpoint / 授权书扫描件 / 密钥 / 个人信息** → ⚠️ 禁止入库
- [ ] 是否为 **不兼容变更** → 需 `BREAKING CHANGE:`

## 关联

```
Refs: #
Gate-Report:
Preset:
Dataset:
Model:
License:
License-Review:
```

## 提交规范确认

- [ ] 提交信息符合 [`COMMIT_CONVENTION.md`](../COMMIT_CONVENTION.md)（type/scope 在枚举内、subject ≤72 字符、祈使句、无句号）
- [ ] body 写的是「为什么」，引用论文带 arXiv ID
- [ ] 强制 footer 已填齐

## 测试 / 验证

<!-- commitlint / license-check / eval-gate 状态；本地验证方式；如为文档变更说明核验来源与日期 -->

## 许可确认

提交即表示同意贡献依仓库 [`LICENSE`](../LICENSE)（PolyForm Noncommercial 1.0.0）对外提供，且有权提交该内容。本项目为**开放权重 / 源码可得**，非 OSI 认证开源。
