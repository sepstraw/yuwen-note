# yuwen-note

语文课文学习笔记：从「汉查查」抓取课堂笔记，按固定模板整理成 Markdown，网页端点开即读。

**在线阅读**：<https://sepstraw.github.io/yuwen-note/>

## 已收课文

共 **31 篇**，按部编版册次分组。

### 三年级上册（24 篇）

| # | 课文 | 笔记 |
| --- | --- | --- |
| 1 | 大青树下的小学 | [data/大青树下的小学.md](data/大青树下的小学.md) |
| 2 | 花的学校 | [data/花的学校.md](data/花的学校.md) |
| 3 | 不懂就要问 | [data/不懂就要问.md](data/不懂就要问.md) |
| 4 | 铺满金色巴掌的水泥道 | [data/铺满金色巴掌的水泥道.md](data/铺满金色巴掌的水泥道.md) |
| 5 | 秋天的雨 | [data/秋天的雨.md](data/秋天的雨.md) |
| 6 | 听听，秋的声音 | [data/听听，秋的声音.md](data/听听，秋的声音.md) |
| 7 | 卖火柴的小女孩 | [data/卖火柴的小女孩.md](data/卖火柴的小女孩.md) |
| 8 | 那一定会很好 | [data/那一定会很好.md](data/那一定会很好.md) |
| 9 | 在牛肚子里旅行 | [data/在牛肚子里旅行.md](data/在牛肚子里旅行.md) |
| 10 | 一块奶酪 | [data/一块奶酪.md](data/一块奶酪.md) |
| 11 | 总也倒不了的老屋 | [data/总也倒不了的老屋.md](data/总也倒不了的老屋.md) |
| 12 | 胡萝卜先生的长胡子 | [data/胡萝卜先生的长胡子.md](data/胡萝卜先生的长胡子.md) |
| 13 | 小狗学叫 | [data/小狗学叫.md](data/小狗学叫.md) |
| 14 | 搭船的鸟 | [data/搭船的鸟.md](data/搭船的鸟.md) |
| 15 | 金色的草地 | [data/金色的草地.md](data/金色的草地.md) |
| 16 | 富饶的西沙群岛 | [data/富饶的西沙群岛.md](data/富饶的西沙群岛.md) |
| 17 | 海滨小城 | [data/海滨小城.md](data/海滨小城.md) |
| 18 | 美丽的小兴安岭 | [data/美丽的小兴安岭.md](data/美丽的小兴安岭.md) |
| 19 | 大自然的声音 | [data/大自然的声音.md](data/大自然的声音.md) |
| 20 | 读不完的大书 | [data/读不完的大书.md](data/读不完的大书.md) |
| 21 | 父亲、树林和鸟 | [data/父亲、树林和鸟.md](data/父亲、树林和鸟.md) |
| 22 | 司马光 | [data/司马光.md](data/司马光.md) |
| 23 | 灰雀 | [data/灰雀.md](data/灰雀.md) |
| 24 | 手术台就是阵地 | [data/手术台就是阵地.md](data/手术台就是阵地.md) |

两套《古诗三首》源站未收录课堂笔记，暂缺。

### 三年级下册（7 篇）

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

每篇固定五节：课文一瞥（核心问题 / 主要内容 / 中心句）、文章结构（表格）、阅读与写作（写法分析 + 小技巧）、语言积累（词语库 + 句式库）、课后挑战（朗读 / 解说 / 写作）。

## 怎么加新课文

```bash
python crawler.py 肥皂泡 --volume sanxia   # 抓取并生成 data/肥皂泡.md
```

- 默认册次 `sanxia`（三下），可换 `sanshang` `sixia` 等；
- 配置 `DEEPSEEK_API_KEY` 后调用 AI 扩写成完整笔记，未配置则输出结构化骨架；
- 网页端也可触发：输入课名 → 调 GitHub Actions（需在仓库 Secrets 里配置 `DEEPSEEK_API_KEY`）；
- 新增后记得把课名加进 `index.html` 的 `GROUPS` 列表。

## 目录

- `crawler.py` — 抓取与生成
- `data/` — 生成的笔记
- `index.html` — 网页阅读器（GitHub Pages）
- `.github/workflows/crawl.yml` — 网页触发用的 Actions

## 说明

课堂笔记原文来自 <https://hanchacha.com>，仅供个人学习使用。
