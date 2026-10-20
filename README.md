# 38 亿年 · 研究笔记

**网页：https://bluesky-rgb.github.io/38-billion-years-research/**

我们对"你从哪里来"的理解，按主题整理成一条完整的因果链：从星云收缩成太阳，到生命起源、细胞、动物的身体、登上陆地，再到人与社会。

这些理解来自视频系列[《38 亿年家谱》](https://github.com/4jt8jty9sk-cpu/38-billion-years)的制作过程：每一个"没看懂"，都先在这里弄懂，再写进视频。

## 内容

| 页面 | 内容 |
| --- | --- |
| [首页](https://bluesky-rgb.github.io/38-billion-years-research/) | 两条主线（合作与信息）、七个章节、社会的本质 |
| [章节](https://bluesky-rgb.github.io/38-billion-years-research/ch-earth.html) | 每章包括核心观点、因果链、关键事件、问与答、关键概念、尚无定论的地方、对应视频 |
| [大时间轴](https://bluesky-rgb.github.io/38-billion-years-research/timeline.html) | 46 亿年关键事件，对数刻度 |
| [问答](https://bluesky-rgb.github.io/38-billion-years-research/questions.html) | 制作中提出的全部问题与答案 |
| [概念词典](https://bluesky-rgb.github.io/38-billion-years-research/glossary.html) | 全部概念，按章节归类，可搜索 |
| [方法](https://bluesky-rgb.github.io/38-billion-years-research/method.html) | 正向流程：前提、形成、变化、概念、影响、引出 |

## 七个章节

1. **宇宙与地球**：舞台是怎么搭起来的（46–40 亿年前）
2. **生命的起源**：从化学到生物（约 40–38 亿年前）
3. **细胞与能量**：从细菌到复杂细胞（约 38–6 亿年前）
4. **会动的星球**：板块、气候与大灭绝（贯穿全程）
5. **动物的身体**：从一团细胞到长着下巴的鱼（约 6.4–4 亿年前）
6. **登上陆地**：植物先行，动物跟上（约 4.7–2.5 亿年前）
7. **人与社会**：系列的终点（约 700 万年前至今）

## 结构

```
data/        全部内容（章节、时间轴、问答、概念、方法）
build.py     由 data/ 生成网页
style.css    样式
*.html       生成的网页
```

更新内容：修改 `data/` 里的 JSON，运行 `python3 build.py`，提交即可。

## 许可

内容采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hans)。
