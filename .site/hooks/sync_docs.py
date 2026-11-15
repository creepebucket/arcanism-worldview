"""构建前把仓库根目录的笔记同步进 .site/docs/。

这个仓库由 Obsidian 直接管理, 笔记就放在根目录下; 而 MkDocs 要求所有文档
位于 docs_dir 之内, 并且 docs_dir 不能是配置文件所在目录的父目录。
于是每次构建前同步一次 .site/docs/:

    仓库根 *.md      ->  .site/docs/*.md
    .site/pages/*.md ->  .site/docs/*.md   (站点自己的页面, 如首页)
    .site/theme/*    ->  .site/docs/*      (样式表和脚本)

同步是幂等的: 内容没变的文件不会被重写, 以免 mkdocs serve 反复重建。
.site/docs/ 是纯粹的产物, 不出现在 git 里, 也不需要手动维护。
"""

from __future__ import annotations

import filecmp
import shutil
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent  # .site/
ROOT = SITE.parent  # 仓库根目录
DOCS = SITE / "docs"
THEME = SITE / "theme"
PAGES = SITE / "pages"

# 不参与建站的目录
SKIP_DIRS = {".git", ".github", ".obsidian", ".site", "__pycache__", ".venv"}
# 仓库说明和 AI 协作说明, 不属于世界观正文
SKIP_FILES = {"AGENTS.md", "README.md"}


def on_pre_build(config, **kwargs) -> None:  # noqa: ARG001
    DOCS.mkdir(parents=True, exist_ok=True)
    wanted: dict[Path, Path] = {}

    # 1. 仓库根目录的笔记
    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or md.name in SKIP_FILES:
            continue
        wanted[DOCS / rel] = md

    # 2. 站点专属页面 (首页等)
    if PAGES.is_dir():
        for md in PAGES.rglob("*.md"):
            wanted[DOCS / md.relative_to(PAGES)] = md

    # 3. 样式与脚本
    if THEME.is_dir():
        for asset in THEME.rglob("*"):
            if asset.is_file():
                wanted[DOCS / asset.relative_to(THEME)] = asset

    for target, source in wanted.items():
        copy_if_changed(source, target)

    prune(DOCS, set(wanted))


def copy_if_changed(source: Path, target: Path) -> None:
    """只在内容确实不同的时候写入, 保留其它文件的 mtime。"""
    if target.is_file() and filecmp.cmp(source, target, shallow=False):
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def prune(docs: Path, keep: set[Path]) -> None:
    """删掉源文件已经不存在的旧产物, 并清理空目录。"""
    for item in sorted(docs.rglob("*")):
        if item.is_file() and item not in keep and item.name != ".gitkeep":
            item.unlink()
    for folder in sorted((p for p in docs.rglob("*") if p.is_dir()), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()
