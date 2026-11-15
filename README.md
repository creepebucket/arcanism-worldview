# 魔力工业世界观

一套魔法工业 mod 的世界观设定。正文是仓库根目录下的 Markdown, 由 Obsidian 编辑,
每次推送到 `main` 会自动构建成静态站点并发布到 GitHub Pages。

## 目录约定

根目录只放笔记本身, 站点相关的东西全部收在 `.site/` 里 (隐藏目录, Obsidian 不会显示它)。

| 路径 | 作用 |
|------|------|
| `*.md`、`生产/*.md` | 正文。用 Obsidian 正常编辑即可 |
| `index.md` | 站点首页, 也是普通笔记, 直接改就行 |
| `AGENTS.md` | 写给自己和 AI 的协作约定, 不上站 |
| `.site/mkdocs.yml` | 站点配置: 导航、主题色、Markdown 扩展 |
| `.site/theme/` | 4 套配色的 CSS 和色块切换脚本 |
| `.site/hooks/` | 构建前把根目录正文同步进 `docs/` |
| `.site/serve.py` | 本地预览入口 |
| `.site/docs/`、`.site/.build/` | 构建产物, 已在 `.gitignore` 里 |

新增一篇文档后, 记得在 `.site/mkdocs.yml` 的 `nav:` 里加一行, 否则构建会报错。

## 本地预览

首次需要装一次依赖:

```bash
python3 -m venv .venv
.venv/bin/pip install -r .site/requirements.txt
```

之后:

```bash
.venv/bin/mkdocs serve -f .site/mkdocs.yml
```

浏览器打开 http://127.0.0.1:8000 即可, 改动会自动刷新。

只构建不预览用 `.venv/bin/mkdocs build -f .site/mkdocs.yml`, 产物在 `.site/.build/`。

## 配色

站点默认深色。页头右侧有 4 个色块, 点击即在 4 套主题间切换, 选择记在浏览器 localStorage 里。

| 主题 | 主题色 (页头 / 表格 / 选中项) | 文本强调色 (链接 / 加粗 / 高亮) |
|------|------|------|
| 金黄 | `#e6da1f` | `#d8d45a` |
| 赤红 | `#f0332a` | `#e15d50` |
| 青蓝 | `#1fd0e0` | `#4ab8c4` |
| 翠绿 | `#2fd44a` | `#67cf67` |

改色只需要动 `.site/theme/stylesheets/theme.css` 顶部四个 `[data-md-color-primary=...]` 块。

## 首次部署

1. 在 GitHub 上建一个仓库, 把本地仓库推上去:
   ```bash
   git remote add origin git@github.com:<用户名>/<仓库名>.git
   git push -u origin main
   ```
2. 进入仓库的 **Settings → Pages**, 把 **Source** 设为 **GitHub Actions**。
3. 之后每次 push 到 `main`, `.github/workflows/pages.yml` 会自动构建并发布。

免费账号的 Pages 只对公开仓库开放; 私有仓库需要 GitHub Pro 及以上。
