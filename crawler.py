# -*- coding: utf-8 -*-
"""按课文名生成学习笔记。

用法：
    python crawler.py 荷花                 # 默认按三年级下册检索
    python crawler.py 荷花 --volume sixia  # 指定册
    python crawler.py https://hanchacha.com/yuwen/xxx.html   # 直接给笔记页

流程：在「汉查查」的册索引里找到《X》课堂笔记 → 抓正文 → 有 DEEPSEEK_API_KEY 就调 AI 扩写
     → 没有则输出基于原文的结构化骨架 → 写入 data/X.md

日志一律写 stderr；stdout 只留笔记正文，这样 `python crawler.py X > data/X.md` 也不会写脏。
"""
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://hanchacha.com"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
MAX_PAGES = 8


def log(*args):
    print(*args, file=sys.stderr, flush=True)


def get(url):
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    r.encoding = "utf-8"          # 站点声明不准确，实际是 UTF-8
    return r.text


def lesson_index(volume="sanxia"):
    """抓一册的索引，返回 {课文名: 笔记页 URL}。"""
    found = {}
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE}/yuwen/{volume}/" if page == 1 else f"{BASE}/yuwen/{volume}/index_{page}.html"
        try:
            html = get(url)
        except Exception as exc:
            log(f"  索引第 {page} 页读取失败：{exc}")
            break
        soup = BeautifulSoup(html, "html.parser")
        before = len(found)
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            m = re.match(r"^《(.+?)》课堂笔记$", text)
            if m:
                found.setdefault(m.group(1), requests.compat.urljoin(url, a["href"]))
        if page > 1 and len(found) == before:
            break
    return found


def fetch_note_text(url):
    """取笔记页正文（去掉导航与文末「相关资料」）。"""
    soup = BeautifulSoup(get(url), "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    art = soup.find("article") or soup.find("div", class_="entry-content")
    text = (art or soup).get_text("\n", strip=True)
    text = text.split("相关资料")[0]
    text = re.sub(r"\n{2,}", "\n", text)
    lines = [ln.strip() for ln in text.split("\n") if ln.strip() and ln.strip() not in ("汉查查", "»")]
    # 去掉页头：标题、面包屑、日期之前的行都属于导航
    for i, ln in enumerate(lines):
        if re.match(r"^\d{4}-\d{2}-\d{2}", ln):
            lines = lines[i + 1:]
            break
    else:
        lines = lines[5:]
    return "\n".join(lines).strip()


def skeleton(lesson, raw):
    """无 API Key 时的兜底：把抓到的内容整理成固定骨架。"""
    return f"""# 📖 {lesson} · 学习笔记

> 由 crawler.py 抓取自汉查查课堂笔记；配置 DEEPSEEK_API_KEY 后可生成完整学霸笔记。

---

## 📚 一、课文一瞥

{raw[:600] if raw else f"《{lesson}》暂无抓取到资料。"}

---

## 🧱 二、文章结构

| 部分 | 自然段 | 内容 | 作用 |
|------|--------|------|------|
| 开头 | | | |
| 中间 | | | |
| 结尾 | | | |

---

## 📝 三、语言积累

| 类别 | 词语 |
|------|------|
| 必会字词 | |
| 近义词 | |
| 反义词 | |

---

*🕐 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}*
"""


def generate_with_ai(lesson, raw):
    if not DEEPSEEK_API_KEY:
        log("  🤖 未配置 DEEPSEEK_API_KEY，输出结构化骨架")
        return skeleton(lesson, raw)

    prompt = f"""你是小学语文特级教师。请为课文《{lesson}》写一份详细的学习笔记。

要求：
1. 严格按下面的结构输出，不要增加别的章节；
2. 表格每一格都要填具体内容，不能留空、不能写“请根据课文填写”；
3. 词语要给出真实的必会字词、近义词、反义词；
4. 只输笔记正文，不要解释。

# 🌊 探秘{lesson} · 学霸综合笔记 🐠

> 一份集**知识点、课堂笔记、教学思路**于一体的超实用手册

## 📚 一、课文一瞥：它讲了什么？
* **核心问题**：
* **主要内容**：
* **中心句**：

## 🧱 二、文章结构：总—分—总
| 部分 | 自然段 | 内容 | 作用 |
|------|--------|------|------|

## ✨ 三、阅读与写作：深挖课文“宝藏”
| 阅读要点 | 写法分析 | 写作小技巧 |
|----------|----------|------------|

## 📝 四、语言积累：词语库+句式库
| 类别 | 词语 |
|------|------|
| 必会字词 | |
| 近义词 | |
| 反义词 | |

### 仿写句式
> **句式名称** / 课文原句 / 仿写示例

## 🎯 五、课后挑战：小试牛刀
1. **朗读小能手**：
2. **小小解说员**：
3. **妙笔生花**：

【参考资料】
{raw[:3000]}
"""
    try:
        log("  🤖 正在调用 DeepSeek API...")
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "你是小学语文特级教师，擅长写详细、准确的课文笔记。"},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 4000,
            },
            timeout=90,
        )
        if resp.status_code == 200:
            note = resp.json()["choices"][0]["message"]["content"].strip()
            log(f"  ✅ AI 生成成功：{len(note)} 字")
            return note
        log(f"  ⚠️ AI 调用失败：HTTP {resp.status_code}")
    except Exception as exc:
        log(f"  ⚠️ AI 异常：{exc}")

    return skeleton(lesson, raw)


def main():
    argv = sys.argv[1:]
    if not argv:
        log("用法：python crawler.py 课文名 [--volume sanxia]")
        sys.exit(1)

    volume = "sanxia"
    if "--volume" in argv:
        idx = argv.index("--volume")
        volume = argv[idx + 1]
        del argv[idx:idx + 2]

    lesson = argv[0].strip()
    log(f"🕷️ 处理《{lesson}》")

    raw = ""
    if lesson.startswith("http"):
        raw = fetch_note_text(lesson)
        lesson = re.sub(r"[\\/:*?\"<>|]", "_", lesson)
    else:
        log(f"  🔍 在「{volume}」索引里查找...")
        index = lesson_index(volume)
        url = index.get(lesson)
        if not url:
            for name, link in index.items():
                if lesson in name:
                    url, lesson = link, name
                    break
        if url:
            log(f"  ✅ 命中：{url}")
            raw = fetch_note_text(url)
        else:
            log(f"  ⚠️ 索引里没有《{lesson}》，只生成骨架")

    note = generate_with_ai(lesson, raw)

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", f"{lesson}.md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(note)
    log(f"✅ 已保存：{path}")


if __name__ == "__main__":
    main()
