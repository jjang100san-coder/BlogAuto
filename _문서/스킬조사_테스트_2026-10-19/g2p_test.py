# -*- coding: utf-8 -*-
import sys, io, glob
from g2pkiwi import G2p
g = G2p()
sys.stdout.reconfigure(encoding='utf-8')
print("### 1) 지침에 적힌 「다른 낱말로 들린 말」 — 발음형으로 보면")
cases = ["직접 사서 재고 밟아 본 건", "제품을 직접 사서, 저울에 달아 보고 밟아 보며 비교한 영상은",
         "교통사고 현장 재고 조사", "2편에서 계속", "다음 편에서 계속", "영 대 이로 이겼어", "영대이로 이겼어",
         "온통 하얬어", "군 편은 어땠어", "신을 신고 얼른 동사무소에 가서 혼인 신고 해라"]
for s in cases:
    print(f"  {s}\n   → {g(s)}")
print("\n### 2) 실제 대본 (발행된 클립) — 원문 / 발음형")
base = "/home/user/BlogAuto/_1.컨텐츠"
for f in [base + "/정보(move)_컨텐츠/260929_등산스틱/clip2/narration/ST/script.txt",
          base + "/정보(move)_컨텐츠/261011_무봉산찾기/clip/narration/MB/script.txt"]:
    print("—", f.split("/")[-4])
    for line in io.open(f, encoding="utf-8"):
        line = line.strip()
        if not line: continue
        p = g(line)
        print(f"  {line}\n   → {p}")
