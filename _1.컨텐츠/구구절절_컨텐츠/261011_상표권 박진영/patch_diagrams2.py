# -*- coding: utf-8 -*-
"""KIPRIS 해외 탭(미국 11·일본 9) 확인분을 ②에 반영."""
import io
p = "make_diagrams.py"
s = io.open(p, encoding="utf-8").read()
NL = "\\" + "n"
rep = [
    ('"FANOMENON 11건' + NL + '2025.11.14 출원' + NL + '심사 보류(거절 아님)"',
     '"FANOMENON 11건' + NL + '2025.11.14 출원 · 심사 보류' + NL + '출원인: JYP 단독 (KIPRIS 확인)"'),
    ('("일본", "출원함' + NL + '(2026년 초)", LIGHT, INK)',
     '("일본", "FANOMENON 9건' + NL + '2026년 출원 (KIPRIS 확인)", LIGHT, INK)'),
    ('("멕시코", "출원함' + NL + '(2026년 초)", LIGHT, INK)',
     '("멕시코", "출원함 (보도)' + NL + 'KIPRIS 미수록 국가", LIGHT, INK)'),
    ('foot(d, "출처: KIPRIS 직접 조회(국내) · 딜사이트·Korea Times 보도(해외). 해외 출원인은 JYP 단독으로 보도됨.")',
     'foot(d, "출처: KIPRIS 직접 조회 — 국내 48건, 미국 11건(출원인 JYP ENTERTAINMENT CORPORATION), 일본 9건. 멕시코는 보도(Korea Times).")'),
]
for a, b in rep:
    if a not in s:
        print("MISS:", a[:50]); continue
    s = s.replace(a, b, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("patched2")
