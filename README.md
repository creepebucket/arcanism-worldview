# 魔力工业世界观

一套魔法工业 mod 的世界观设定。正文是仓库根目录下的 Markdown, 由 Obsidian 编辑,
每次推送到 `main` 会自动构建成静态站点并发布到 GitHub Pages。

## 目录约定

| 路径 | 作用 |
|------|------|
| `*.md`、`生产/*.md` | 正文。用 Obsidian 正常编辑即可 |
| `index.md` | 站点首页 |
| `mkdocs.yml` | 站点配置: 导航、配色主题、Markdown 扩展 |
| `theme/stylesheets/theme.css` | 4 套主题色的定义与排版微调 |
| `theme/javascripts/palette.js` | 把 4 个色块摆成并排的切换按钮 |
| `hooks/sync_docs.py` | 构建前把正文复制进 `docs/`, 平时不用管 |
| `docs/` | 构建中间产物, 已在 `.gitignore` 里 |

新增一篇文档后, 记得在 `mkdocs.yml` 的 `nav:` 里加一行, 否则构建会报错。

## 本地预览

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

浏览器打开 http://127.0.0.1:8000 即可, 改动会自动刷新。

## 配色

页头右侧有 4 个色块, 点击即在 4 套主题间切换, 选择记在浏览器 localStorage 里。

| 主题 | 主题色 (页头 / 表格 / 选中项) | 文本强调色 (链接 / 加粗 / 高亮) |
|------|------|------|
| 金黄 | `#e6da1f` | `#d8d45a` |
| 赤红 | `#f0332a` | `#e15d50` |
| 青蓝 | `#1fd0e0` | `#4ab8c4` |
| 翠绿 | `#2fd44a` | `#67cf67` |

改色只需要动 `theme/stylesheets/theme.css` 顶部四个 `html[data-md-color-primary=...]` 块。

## 首次部署

1. 在 GitHub 上建一个仓库, 把本地仓库推上去:
   ```bash
   git remote add origin git@github.com:<用户名>/<仓库名>.git
   git push -u origin main
   ```
2. 进入仓库的 **Settings → Pages**, 把 **Source** 设为 **GitHub Actions**。
3. 之后每次 push 到 `main`, `.github/workflows/pages.yml` 会自动构建并发布。

免费账号的 Pages 只对公开仓库开放; 私有仓库需要 GitHub Pro 及以上。
