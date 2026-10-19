# -*- coding: utf-8 -*-
"""초안 md → 블록 목록. 발행 스크립트와 검증기가 함께 쓴다."""
import io, os, re

RE_TITLE = re.compile(r"^\[\[TITLE:\s*(.+?)\s*\]\]\s*$")
RE_CAT   = re.compile(r"^\[\[CATEGORY:\s*(.+?)\s*\]\]\s*$")
RE_IMG   = re.compile(r"^\s*\[\[IMG:([^|\]]+?)\s*\|\s*([^\]]*?)\]\]\s*$")
RE_LINK  = re.compile(r"^\s*\[\[LINK:\s*(\S+?)\s*\|\s*([^\]]*?)\]\]\s*$")
# 시리즈 머리말(▶ 1편:)은 링크에서 뺀다. 두 번째 | 로 직접 지정할 수도 있다.
RE_HEAD  = re.compile(r"^\s*([▶▷►>]?)\s*(\d+)\s*편\s*[:：.]?\s+(.+)$")
RE_QUOTE = re.compile(r"^\s*>\s?(.*)$")          # '> 💡 팁' 인용구 줄
BEGIN, END = "===== ✂️ 여기부터 복사 =====", "===== ✂️ 여기까지 ====="

def split_link_label(label):
    """링크 문구 → (머리말, 링크 걸 부분). 마스터 2-3 — 머리말은 링크에서 뺀다.
    fill_editor([[LINK:]])와 add_link.py(발행글 링크 추가)가 이 함수 하나를 같이 쓴다(2026-10-16, 둘이 달라서 생긴 사고)."""
    label = label.strip()
    if "|" in label:                     # 「안 걸 부분 | 걸 부분」
        head, shown = label.split("|", 1)
        return (head.rstrip() + " " if head.strip() else ""), shown.strip()
    mh = RE_HEAD.match(label)
    if mh:                               # 「▶ 1편 : 」 꼴로 통일한다
        mark = (mh.group(1) + " ") if mh.group(1) else ""
        return "%s%s편 : " % (mark, mh.group(2)), mh.group(3)
    return "", label


def parse(md_path):
    lines = io.open(md_path, encoding="utf-8").read().split("\n")
    title = category = None
    for l in lines:
        m = RE_TITLE.match(l)
        if m: title = m.group(1)
        m = RE_CAT.match(l)
        if m: category = m.group(1)

    s = next(i for i, l in enumerate(lines) if l.startswith(BEGIN))
    e = next(i for i, l in enumerate(lines) if l.startswith(END))
    body = lines[s+1:e]

    blocks, i, blank = [], 0, 0
    while i < len(body):
        l = body[i]
        if not l.strip():
            blank += 1; i += 1
            continue
        if blank and blocks:
            blocks.append(("blank", None))       # 빈 줄은 최대 1개로 접음
        blank = 0

        m = RE_IMG.match(l)
        m2 = RE_LINK.match(l)
        if m:
            blocks.append(("img", (m.group(1).strip(), m.group(2).strip())))
        elif m2:
            url, label = m2.group(1).strip(), m2.group(2).strip()
            head, shown = split_link_label(label)
            blocks.append(("link", (url, head, shown)))
        elif RE_QUOTE.match(l) and not RE_HEAD.match(l.strip()):
            # 인용구 표식 '>' 는 본문에 들어가면 안 된다
            blocks.append(("quote", RE_QUOTE.match(l).group(1).rstrip()))
        elif l.strip() == "---":
            blocks.append(("hr", None))
        elif l.lstrip().startswith("|"):
            rows = []
            while i < len(body) and body[i].lstrip().startswith("|"):
                cells = [c.strip() for c in body[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows)); continue
        elif l.strip().startswith("#") and " #" in l:
            blocks.append(("tags", l.strip()))
        else:
            blocks.append(("text", l.rstrip()))
        i += 1

    return {"title": title, "category": category, "blocks": blocks,
            "img_dir": os.path.dirname(os.path.abspath(md_path))}

def split_bold(s):
    """'a **b** c' -> [('a ',False),('b',True),(' c',False)]"""
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", s):
        if m.start() > pos: out.append((s[pos:m.start()], False))
        out.append((m.group(1), True)); pos = m.end()
    if pos < len(s): out.append((s[pos:], False))
    return out or [(s, False)]
