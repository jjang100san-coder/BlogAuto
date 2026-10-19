# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from kiwipiepy import Kiwi
k = Kiwi(model_type="cong")
print("### 형태소로 본 「다른 낱말로 들릴 말」 — 분석기가 명사로 읽으면 TTS 도 그렇게 읽기 쉽다")
for s in ["직접 사서 재고 밟아 본 건", "직접 재고 직접 가 보는 데", "제품을 직접 사서, 저울에 달아 보고 밟아 보며 비교한 영상은",
          "창고에 재고가 많아", "유튜브에서 사고 재고 한 영상은", "2편에서 계속"]:
    toks = k.tokenize(s)
    flag = [t for t in toks if t.form in ("사고", "재고", "가고", "쓰고") and t.tag.startswith("NN")]
    print(f"  {s}\n   → {' '.join(f'{t.form}/{t.tag}' for t in toks)}" + ("   ⚠ 명사로 읽힘: " + ", ".join(t.form for t in flag) if flag else ""))
