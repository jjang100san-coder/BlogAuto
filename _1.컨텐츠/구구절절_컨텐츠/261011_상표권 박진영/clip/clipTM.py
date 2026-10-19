# 패노메논 상표권 클립 (발행 10/11 14:48, logNo 224437965031)
# 실행: python clipTM.py stills / python clipTM.py → out\trademark.mp4
# 10/11 사용자: 「정보 전달이라 무거워질 수 있으니 사이사이 유머, 진정성은 가볍게」 — 휴 · 찜질팩이 나보다 빨랐어 · 상어도 예외 없어 · 찜질팩 나오면 알려 줘
# 화면은 발행글의 직접 그린 도해(img\) + AI 그네 그림(움직임 AI). 국감 방송 화면은 쓰지 않는다(방송사 저작물)
# 구구절절 상표 주인 실명은 가린다(img\08_masked.png). 숫자는 발행본 그대로
import os, sys
sys.path.insert(0, r'C:\Users\user\Desktop\Blog\_1.컨텐츠\_자동화\clipkit')
import shorts
from shorts import render, prep, YEL, WHITE
from tactics import build

BASE = os.path.dirname(os.path.abspath(__file__))
f = lambda n: os.path.join(BASE, 'fit_%s.jpg' % n)
shorts.HEAD = ('키프리스에 내 블로그 이름', '카테고리는 이미 남의 것')
D = dict(type='data', render=render, bg=(0, 0, 0), dur=3.0)
SWING = 'video:' + os.path.join(BASE, 'hf_swing.mp4')
DG = '직접 그린 도해'
W1 = dict(z0=1.0, z1=1.0, whole=True, label=DG)

SCENES = prep([
    dict(D, media=SWING, z0=1.0, z1=1.05, label='AI 생성 이미지',
         call=[(0.4, '내 블로그 이름, 상표 있을까?', WHITE)],
         cap='내 블로그 이름, 혹시 누가 상표로 냈을까? 키프리스에 쳐 봤어.'),
    dict(D, media=f('17_kipris_search'), **W1,
         call=[(0.5, '걷고읽고떠나고 0건', YEL)], sfx=[(0.5, 'ding')],
         cap='블로그 이름 걷고읽고떠나고는 0건. 휴, 아무도 안 냈더라.'),
    dict(D, media=f('08_masked'), **W1,
         cap='그런데 카테고리 이름 구구절절은, 상표가 넷이나 나왔어. 둘은 등록까지 끝났어. 책 가게, 그리고 찜질팩이 나보다 빨랐어.'),
    dict(D, media=f('01_fanomenon_overview'), **W1,
         cap='왜 남의 것이 됐는지 알려고, 요즘 국감에 나온 상표 사건을 들여다봤어. 이름은 패노메논.'),
    dict(D, media=f('02_name_not_event'), **W1,
         cap='나라가 여는 K팝 축제인데, 그 이름의 상표를 JYP 명의로 냈어. 그게 쟁점이었지.'),
    dict(D, media=f('03_swing_line'), **W1,
         cap='상표 규칙 하나. 그네는 오래 탄 아이가 아니라, 줄에 먼저 선 아이 차례야. 이름을 몇 년 썼어도, 특허청에 서류를 낸 순서대로 가져가.'),
    dict(D, media=f('04_bukangi_timeline'), **W1,
         cap='부산 상어 부캉이도 예외는 없었어. 이름은 시민들이 지었는데, 사흘 뒤 한 개인이 상표를 냈거든.'),
    # (10/11) 「규칙 둘 · 나라별 48·11·9」 장면은 90초를 넘겨서 뺐다 — 녹음 n07 은 남겨 둠
    dict(D, media=f('15_name_field_changes'), **W1, narr=8,
         cap='결국 쟁점은 법 위반이 아니라 이름 칸이었어. 국내는 문체부와 공동 명의로 바꿨고, 해외는 아직 JYP 단독이야.'),
    # 국감 결론 — 10/11 사용자: 「그래서 JYP는 어떤 방향으로 마무리하기로 했대?」 → 2번(국감 영상 자막 근거, 발행글엔 없음)
    #   base data±011_eOfPJsYab0k transcript [08:15] 「아, 그렇게 하면 안 되죠」 · [08:18] 전담법인 이양 입장 「예」 / 문체부 「계약서도 계획도 없다」(발행글)
    dict(D, media=os.path.join(BASE, 'ai_handover4.png'), z0=1.0, z1=1.1, label='AI 생성 이미지 · 국감 영상 기준', narr=11,
         call=[(0.4, '그래서 결론은?', WHITE), (3.6, '해외 권리 → 전담법인으로', YEL)], sfx=[(3.6, 'ding')],
         cap='그래서 결론은? 박진영 위원장은, 해외 권리까지 JYP가 갖는 건 안 된다고 했어. 전담법인으로 넘기겠다는 입장이야.'),
    dict(D, media=os.path.join(BASE, 'ai_blank_contract.png'), z0=1.0, z1=1.1, label='AI 생성 이미지', narr=12,
         call=[(0.5, '계약서 · 계획 없음', WHITE), (3.6, '방향 O · 날짜 X', YEL)],
         cap='다만 문체부는 그 계약서도, 계획도 없다고 답했어. 방향은 정해졌고, 날짜는 아직이야.'),
    dict(D, media=f('08_masked'), z0=1.0, z1=1.1, whole=True, focus=(0.5, 0.6), label=DG, narr=9,   # whole: 오른쪽 「나 · 괜찮음 / 못 씀」 칸이 잘리지 않게
         cap='그래서 내 카테고리는 괜찮아. 블로그 글 제목은 상표 칸에 안 들어가거든. 다만 그 이름으로 전자책을 팔면, 그건 안 돼.'),
    dict(D, media=SWING, z0=1.05, z1=1.0, label='AI 생성 이미지', narr=10,
         call=[(0.5, '키프리스 · 무료 · 3분', YEL)],
         cap='키프리스는 무료고, 로그인도 필요 없어. 너도 3분만 네 이름 쳐 봐. 찜질팩 나오면 꼭 알려 줘.'),
], BASE, 'TM')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        shorts.stills(SCENES, BASE)
    else:
        build(SCENES, BASE, 'TM', 'trademark.mp4')
