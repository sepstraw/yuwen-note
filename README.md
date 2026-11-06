# yuwen-note

语文课文学习笔记：从「汉查查」抓取课堂笔记，按固定模板整理成 Markdown，网页端点开即读。

**在线阅读**：<https://sepstraw.github.io/yuwen-note/>

## 已收课文（部编版三年级下册）

| # | 课文 | 笔记 |
| --- | --- | --- |
| 1 | 燕子 | [data/燕子.md](data/燕子.md) |
| 2 | 荷花 | [data/荷花.md](data/荷花.md) |
| 3 | 赵州桥 | [data/赵州桥.md](data/赵州桥.md) |
| 4 | 蜜蜂 | [data/蜜蜂.md](data/蜜蜂.md) |
| 5 | 我们奇妙的世界 | [data/我们奇妙的世界.md](data/我们奇妙的世界.md) |
| 6 | 火烧云 | [data/火烧云.md](data/火烧云.md) |
| 7 | 海底世界 | [data/海底世界.md](data/海底世界.md) |

## 笔记结构

每篇固定五节：课文一瞥（核心问题/主要内容/中心句）、文章结构（表格）、阅读与写作（写法分析）、语言积累（词语库+句式库）、课后挑战。

## 怎么加新课文

```bash
python crawler.py 肥皂泡 --volume sanxia   # 抓取并生成 data/肥皂泡.md
```

- 默认册次 `sanxia`（三下），可换 `sanshang` `sixia` 等；
- 配置 `DEEPSEEK_API_KEY` 后调用 AI 扩写成完整笔记，未配置则输出结构化骨架；
- 网页端也可触发：输入课名 → 调 GitHub Actions（需在仓库 Secrets 里配置 `DEEPSEEK_API_KEY`）。

## 目录

- `crawler.py` — 抓取与生成
- `data/` — 生成的笔记
- `index.html` — 网页阅读器（GitHub Pages）
- `.github/workflows/crawl.yml` — 网页触发用的 Actions

## 说明

课堂笔记原文来自 <https://hanchacha.com>，仅供个人学习使用。
