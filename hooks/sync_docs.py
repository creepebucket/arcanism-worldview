"""构建前把根目录的文档同步进 docs/。

这个目录由 Obsidian 直接管理, 笔记就放在根目录下; 而 MkDocs 要求所有文档
位于 docs_dir 之内。于是每次构建前重建 docs/:

    根目录 *.md  ->  docs/*.md
    theme/*      ->  docs/*       (样式表等静态资源)

docs/ 是纯粹的产物, 不出现在 git 里, 也永远不需要手动维护。
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
THEME = ROOT / "theme"

# 不参与建站的目录 / 文件
SKIP_DIRS = {
    ".git",
    ".github",
    ".obsidian",
    "docs",
    "hooks",
    "theme",
    "_site",
    "site",
    "__pycache__",
    ".venv",
}
# 给 AI 读的协作说明 / 仓库说明, 不属于世界观正文
SKIP_FILES = {"AGENTS.md", "README.md"}


def on_pre_build(config, **kwargs) -> None:  # noqa: ARG001
    # 只清空内容, 保留 docs/.gitkeep —— MkDocs 在读取配置时就要求 docs_dir 已存在
    DOCS.mkdir(parents=True, exist_ok=True)
    for item in DOCS.iterdir():
        if item.name == ".gitkeep":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or md.name in SKIP_FILES:
            continue
        target = DOCS / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md, target)

    if THEME.is_dir():
        shutil.copytree(THEME, DOCS, dirs_exist_ok=True)
