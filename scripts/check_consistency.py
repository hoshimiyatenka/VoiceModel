#!/usr/bin/env python3
# v0.4 工具 / Phase 0 / 非实测 / 状态: helper
"""v0.4 一致性检查器（标准库，无第三方依赖）。

检查项：
  (a) ERROR-CODES.md 中登记的错误码 与 docs/implement/control/CONTROL-LAYER-SPEC.md
      中出现的错误码比对：§4 的 C 层码必须全部被规格引用（缺则 WARN），
      规格中不得出现未登记码（疑似自造，WARN）；§3 的 S 层码由 schema 落实，
      不参与比对以免常态误报；规格不存在时 SKIP 不算失败。
  (b) VoiceSpec schema 的 spec_version.const == "0.3.0" 且顶层
      additionalProperties is False；被改动即 FAIL。
  (c) 扫描全部 **/*.md 的相对 Markdown 链接，报告断链（WARN）。
  (d) 扫描 docs/implement/** 与 configs/**/*template*.yaml，检查 v0.4 状态标记（WARN）。
  (e) thresholds.yaml 的 calibration.status == "uncalibrated"（否则 WARN）。

用法：
    python scripts/check_consistency.py [--repo-root PATH]
默认 repo-root = 脚本父目录的父目录。
输出 [ OK ] / [WARN] / [FAIL]；退出码 0（无 FAIL）/ 1（有 FAIL）。
错误码唯一真源是 docs/voicespec/ERROR-CODES.md，本脚本用正则解析，不内置码表。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 反引号包裹的错误码，例如 `E-CONFLICT-001` / `W-CONFLICT-006`
CODE_RE = re.compile(r"`([EW]-[A-Z]+-\d{3})`")
# Markdown 链接/图片，捕获目标
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def codes_in(text: str) -> set:
    return set(CODE_RE.findall(text))


def codes_by_layer(text: str):
    """按 ERROR-CODES.md 章节区分「S 层」与「C 层」定义的码。

    §3 定义 S 层码（由 JSON Schema / validate_voicespec.py 落实），
    §4 定义 C 层码（由 CONTROL-LAYER-SPEC.md 落实），§5 为对照表（合法重复，不计入定义）。
    S 层码不应出现在控制层规格中，故不参与「规格未引用」比对，避免常态误报。
    """
    schema_layer: set = set()
    control_layer: set = set()
    bucket = None
    for line in text.splitlines():
        if line.startswith("## 3."):
            bucket = schema_layer
            continue
        if line.startswith("## 4."):
            bucket = control_layer
            continue
        if line.startswith("## 5."):
            bucket = None
            continue
        if bucket is not None:
            m = CODE_RE.search(line)
            if m and line.lstrip().startswith("|"):
                bucket.add(m.group(1))
    return schema_layer, control_layer


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def yaml_calibration_status(path: Path):
    """极简 YAML 读取：只取顶层 calibration: 段下的 status: 标量。"""
    if not path.exists():
        return None
    in_section = False
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and stripped == "calibration:":
            in_section = True
            continue
        if in_section:
            if indent == 0 and stripped.endswith(":"):
                break  # 离开 calibration 段
            if stripped.startswith("status:"):
                return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="v0.4 一致性检查器")
    ap.add_argument("--repo-root", default=None, help="仓库根目录（默认脚本父目录的父目录）")
    args = ap.parse_args(argv)

    root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parent.parent
    failed = False
    print("[INFO] repo-root = %s" % root)
    print("-" * 64)

    # ---- (a) 错误码集合比对 ----
    ec = root / "docs" / "voicespec" / "ERROR-CODES.md"
    spec = root / "docs" / "implement" / "control" / "CONTROL-LAYER-SPEC.md"
    if not ec.exists():
        print("[WARN] (a) ERROR-CODES.md 不存在，跳过错误码比对")
    elif not spec.exists():
        n = len(codes_in(read_text(ec)))
        print("[ OK ] (a) CONTROL-LAYER-SPEC.md 尚未写入，SKIP（不算失败）；ERROR-CODES.md 登记 %d 个码" % n)
    else:
        ec_text = read_text(ec)
        a = codes_in(ec_text)
        s_layer, c_layer = codes_by_layer(ec_text)
        b = codes_in(read_text(spec))
        missing = sorted(c_layer - b)   # C 层已登记但规格未引用（Phase 3 待实现，正常）
        extra = sorted(b - a)           # 规格中出现但未登记（疑似自造，须核对）
        if not missing and not extra:
            print("[ OK ] (a) 错误码一致：登记 %d 个（S 层 %d / C 层 %d），C 层全部在规格中引用"
                  % (len(a), len(s_layer), len(c_layer)))
        else:
            if missing:
                print("[WARN] (a) §4 中 %d 个 C 层码未在控制层规格引用（Phase 3 待实现，正常）: %s"
                      % (len(missing), ", ".join(missing)))
            if extra:
                print("[WARN] (a) 控制层规格出现 %d 个未登记码（疑似自造，须核对只追加规则）: %s"
                      % (len(extra), ", ".join(extra)))

    # ---- (b) 契约完整性（唯一硬 FAIL）----
    schema_path = root / "configs" / "voicespec" / "voicespec.schema.json"
    try:
        schema = json.loads(read_text(schema_path))
    except Exception as e:  # noqa: BLE001
        print("[FAIL] (b) 无法读取 schema: %s" % e)
        failed = True
    else:
        ver = schema.get("properties", {}).get("spec_version", {}).get("const")
        addp = schema.get("additionalProperties")
        if ver == "0.3.0" and addp is False:
            print("[ OK ] (b) spec_version.const='0.3.0' 且顶层 additionalProperties=false")
        else:
            print("[FAIL] (b) 契约被改动：spec_version.const=%r, additionalProperties=%r" % (ver, addp))
            failed = True

    # ---- (c) Markdown 相对链接断链 ----
    broken = []
    md_files = sorted(root.rglob("*.md"))
    link_count = 0
    for md in md_files:
        for m in LINK_RE.finditer(read_text(md)):
            target = m.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1].strip()
            # 去掉可选的链接标题 [x](path "title")
            target = target.split(' "')[0].split(" '")[0].strip()
            low = target.lower()
            if low.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if target.startswith("#"):
                continue
            target = target.split("#", 1)[0].rstrip()
            if not target:
                continue
            link_count += 1
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                broken.append((md.relative_to(root).as_posix(), target))
    if broken:
        print("[WARN] (c) 扫描 %d 个 md / %d 个相对链接，发现 %d 条断链:" % (len(md_files), link_count, len(broken)))
        for f, t in broken[:40]:
            print("         - %s -> %s" % (f, t))
        if len(broken) > 40:
            print("         ... 另有 %d 条" % (len(broken) - 40))
    else:
        print("[ OK ] (c) 扫描 %d 个 md / %d 个相对链接，无断链" % (len(md_files), link_count))

    # ---- (d) v0.4 状态标记 ----
    markers = ("| 版本 | v0.4 |", "# v0.4 模板")
    targets = []
    impl = root / "docs" / "implement"
    if impl.exists():
        targets += [p for p in impl.rglob("*") if p.is_file()]
    targets += [p for p in (root / "configs").rglob("*template*.yaml") if p.is_file()]
    targets = sorted(set(targets))
    no_marker = []
    for p in targets:
        if not any(mk in read_text(p) for mk in markers):
            no_marker.append(p.relative_to(root).as_posix())
    if not targets:
        print("[ OK ] (d) 暂无 docs/implement/** 或 configs/**/*template*.yaml，SKIP")
    elif no_marker:
        print("[WARN] (d) %d 个 v0.4 文件缺少版本/状态标记: %s" % (len(no_marker), ", ".join(no_marker)))
    else:
        print("[ OK ] (d) %d 个 v0.4 文件均带版本/状态标记" % len(targets))

    # ---- (e) 阈值校准状态 ----
    th = root / "configs" / "eval" / "thresholds.yaml"
    status = yaml_calibration_status(th)
    if status == "uncalibrated":
        print("[ OK ] (e) thresholds.yaml calibration.status=uncalibrated")
    else:
        print("[WARN] (e) thresholds.yaml calibration.status=%r（须确认是否误改）" % status)

    print("-" * 64)
    print("结果: %s" % ("FAIL（存在硬失败项）" if failed else "OK（无 FAIL；WARN/SKIP 不阻断）"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
