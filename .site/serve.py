"""本地预览。

笔记在仓库根目录, 而 MkDocs 只监视它自己的 docs_dir (.site/docs/)。
所以这里套一层: 起动 mkdocs serve, 同时每秒检查一次根目录的笔记有没有改动,
有改动就同步进 .site/docs/, 剩下的重建和浏览器热刷新交给 MkDocs 自己完成。

用法:
    .venv/bin/python .site/serve.py
    .venv/bin/python .site/serve.py -a 127.0.0.1:8001
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

SITE = Path(__file__).resolve().parent
ROOT = SITE.parent

sys.path.insert(0, str(SITE / "hooks"))
from sync_docs import SKIP_DIRS, THEME, on_pre_build  # noqa: E402


def snapshot() -> dict[Path, int]:
    """记录所有笔记和站点资源的修改时间。"""
    stamps: dict[Path, int] = {}

    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        stamps[md] = md.stat().st_mtime_ns

    if THEME.is_dir():
        for path in THEME.rglob("*"):
            if path.is_file():
                stamps[path] = path.stat().st_mtime_ns

    return stamps


def main() -> int:
    # 先同步一次, 保证 mkdocs 起动时看到的是最新内容
    on_pre_build(None)

    server = subprocess.Popen(
        [sys.executable, "-m", "mkdocs", "serve", "-f", str(SITE / "mkdocs.yml"), *sys.argv[1:]]
    )

    state = snapshot()
    try:
        while server.poll() is None:
            time.sleep(1)
            current = snapshot()
            if current != state:
                on_pre_build(None)
                state = current
    except KeyboardInterrupt:
        pass
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    return server.returncode or 0


if __name__ == "__main__":
    raise SystemExit(main())
