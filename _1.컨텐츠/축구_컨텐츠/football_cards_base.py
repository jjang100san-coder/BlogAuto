# 축구 네임카드·전술판 공통 모듈 (걷고읽고떠나고, 2026.10.7 기준)
# 사용: from football_cards_base import *  → set_palette(...) 후 카드별 코드 작성
from PIL import Image, ImageDraw, ImageFont
import math

# ---------- 폰트 (Noto Sans CJK, .ttc 의 index=1 이 KR) ----------
BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
BOLD  = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG   = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
# 윈도우(이 PC)에는 CJK .ttc 가 없다 → 같은 계열 Noto Sans KR 가변 글꼴의 굵기 축으로 대신한다 (2026.10.7)
import os
WIN_VF = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
WEIGHT = {BLACK: 900, BOLD: 700, REG: 400}
def f(path, size):
    if os.path.exists(path): return ImageFont.truetype(path, size, index=1)
    fo = ImageFont.truetype(WIN_VF, size); fo.set_variation_by_axes([WEIGHT.get(path, 400)])
    return fo

# ---------- 고정 규격 ----------
W = 1080          # 폭 고정. 높이는 카드마다 계산
MARGIN = 70       # 좌우 여백
BAND = 8          # 상단 띠 두께

# ---------- 색 (글마다 바꾸는 것: BG/PANEL/PANEL2/MUTED/ACCENT) ----------
P = dict(
    BG=(24,30,40), PANEL=(36,44,58), PANEL2=(50,60,78),
    CREAM=(244,240,232), MUTED=(166,176,192), ACCENT=(240,140,130),
    PITCH=(30,52,58), LINE=(92,120,128),
)
# 고정 의미색 (글이 바뀌어도 의미는 유지)
KOR   = (208,119,63)    # 한국(우리 팀) — 주황
OPP   = (46,156,192)    # 상대 기본 — 청록 (상대 색이 겹치면 (74,139,203) 등 청 계열로)
GREEN = (120,200,140)   # 맞음 / 좋아진 것
AMBER = (236,190,100)   # 반반
RED   = (232,108,100)   # 빗나감 / 대가·위험
def set_palette(**kw): P.update(kw)

# ---------- 텍스트 ----------
def center(d, xy, t, fo, fill):
    x, y = xy; b = d.textbbox((0,0), t, font=fo)
    d.text((x-(b[2]-b[0])/2-b[0], y-(b[3]-b[1])/2-b[1]), t, font=fo, fill=fill)
def left(d, xy, t, fo, fill):
    x, y = xy; b = d.textbbox((0,0), t, font=fo)
    d.text((x, y-(b[3]-b[1])/2-b[1]), t, font=fo, fill=fill)
def right(d, xy, t, fo, fill):
    x, y = xy; b = d.textbbox((0,0), t, font=fo)
    d.text((x-(b[2]-b[0]), y-(b[3]-b[1])/2-b[1]), t, font=fo, fill=fill)
def wrap(d, s, fo, maxw):
    lines, cur = [], ""
    for w_ in s.split(" "):
        t = (cur+" "+w_).strip()
        if d.textlength(t, font=fo) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    return lines

# ---------- 뼈대 ----------
def base(H, title=None, sub=None, band=None):
    """배경 + 상단 띠 + 제목(y74) + 부제(y130)"""
    im = Image.new("RGB", (W, H), P["BG"]); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,BAND], fill=band or P["ACCENT"])
    if title: center(d, (W/2,74), title, f(BLACK,50), P["CREAM"])
    if sub:   center(d, (W/2,130), sub, f(REG,26), P["MUTED"])
    return im, d
def bar(d, y, text, size=30, col=None):
    """하단 결론 바 — 높이 82. 보통 y = H-122"""
    d.rounded_rectangle([MARGIN,y,W-MARGIN,y+82], radius=14, fill=P["PANEL2"])
    center(d, (W/2,y+41), text, f(BLACK,size), col or P["ACCENT"])
def src(d, y, t):
    """출처 줄 — 항상 '직접 만든 이미지'로 끝낸다"""
    center(d, (W/2,y), t, f(REG,20), P["MUTED"])
def chip(d, xy, text, col):
    """판정 칩(맞음/반반/빗나감/보류) — 오른쪽 끝 x 기준"""
    x, y = xy; fo = f(BLACK,22); b = d.textbbox((0,0), text, font=fo); w_ = b[2]-b[0]+30
    d.rounded_rectangle([x-w_,y-20,x,y+20], radius=20, fill=col); center(d, (x-w_/2,y), text, fo, P["BG"])
def legend(d, y, items):
    """범례: [(색, 이름), ...] 가운데 정렬"""
    fo = f(BOLD,24); widths = [26+12+d.textlength(n,font=fo) for _,n in items]; gap = 60
    x = (W - (sum(widths)+gap*(len(items)-1)))/2
    for (col,n),wd in zip(items,widths):
        d.ellipse([x,y-13,x+26,y+13], fill=col, outline=P["CREAM"], width=2)
        left(d, (x+38,y), n, fo, P["CREAM"]); x += wd+gap

# ---------- 네임카드(인물) ----------
def namecard(path, kicker, name, sub, rows, foot, source, col=None):
    """rows=[(라벨,값),...] 6~8줄. 첫 줄은 '현재/이번 대회' 같은 핵심을 둔다"""
    col = col or P["ACCENT"]; top=330; rh=86; gap=12
    H = top+len(rows)*(rh+gap)+30+82+80
    im, d = base(H, band=col)
    center(d, (W/2,70), kicker, f(BOLD,28), P["MUTED"])
    center(d, (W/2,160), name, f(BLACK,104), P["CREAM"])
    center(d, (W/2,250), sub, f(BOLD,28), P["CREAM"])
    d.rounded_rectangle([W/2-60,280,W/2+60,286], radius=3, fill=col)
    y = top
    for i,(k,v) in enumerate(rows):
        d.rounded_rectangle([MARGIN,y,W-MARGIN,y+rh], radius=14, fill=P["PANEL2"] if i==0 else P["PANEL"])
        d.rectangle([MARGIN,y+14,MARGIN+8,y+rh-14], fill=P["ACCENT"] if i==0 else col)
        left(d, (104,y+rh/2), k, f(BOLD,26), P["ACCENT"] if i==0 else P["MUTED"])
        left(d, (300,y+rh/2), v, f(BOLD,29), P["CREAM"])
        y += rh+gap
    y += 18; bar(d, y, foot, size=31); src(d, y+82+40, source)
    im.save(path)

# ---------- 전술판 ----------
PW, PH = 430, 700                      # 미니 피치 크기 (세로)
PA, PB = (75,230), (575,230)           # 두 장 나란히: 왼쪽 A, 오른쪽 B
def pt(o, fx, fy): return (o[0]+PW*fx, o[1]+PH*fy)   # 피치 비율 좌표 → 픽셀
def pitch(d, x0, y0, x1, y1, lw=2):
    w_, h_ = x1-x0, y1-y0; L = P["LINE"]
    d.rectangle([x0,y0,x1,y1], fill=P["PITCH"], outline=L, width=lw)
    d.line([x0,y0+h_/2,x1,y0+h_/2], fill=L, width=lw)
    r = w_*0.13; d.ellipse([x0+w_/2-r,y0+h_/2-r,x0+w_/2+r,y0+h_/2+r], outline=L, width=lw)
    bw, bh = w_*0.6, h_*0.13
    d.rectangle([x0+(w_-bw)/2,y0,x0+(w_+bw)/2,y0+bh], outline=L, width=lw)
    d.rectangle([x0+(w_-bw)/2,y1-bh,x0+(w_+bw)/2,y1], outline=L, width=lw)
def two_pitches(d, left_title, right_title, lcol=GREEN, rcol=RED):
    for o in (PA,PB): pitch(d, o[0], o[1], o[0]+PW, o[1]+PH)
    center(d, (PA[0]+PW/2,200), left_title, f(BLACK,26), lcol)
    center(d, (PB[0]+PW/2,200), right_title, f(BLACK,26), rcol)
def tag(d, x, y, text, size=18, fill=None, bg=(12,16,24)):
    """선수·구역 라벨 — 어두운 바탕 위 글자. 원 바로 아래(+r+17) 또는 위"""
    fo = f(BOLD,size); b = d.textbbox((0,0), text, font=fo); tw, th = b[2]-b[0], b[3]-b[1]
    d.rounded_rectangle([x-tw/2-8,y-th/2-6,x+tw/2+8,y+th/2+8], radius=8, fill=bg)
    center(d, (x,y), text, fo, fill or P["CREAM"])
def player(d, x, y, col, label=None, r=16, below=True, size=17):
    """선수 원: 크림 테두리 3px. 이름 있는 선수 r=16, 배경 선수 r=12~14"""
    d.ellipse([x-r,y-r,x+r,y+r], fill=col, outline=P["CREAM"], width=3)
    if label: tag(d, x, y+(r+17 if below else -(r+17)), label, size)
def arrow(d, p1, p2, col, w=4, dashed=False, head=14):
    """실선 = 공(패스), 점선 = 사람의 움직임"""
    x1,y1 = p1; x2,y2 = p2; ang = math.atan2(y2-y1,x2-x1); L = math.hypot(x2-x1,y2-y1)
    if dashed:
        t = 0
        while t < L-head:
            a = t; b = min(t+14, L-head*0.8)
            d.line([x1+math.cos(ang)*a,y1+math.sin(ang)*a,x1+math.cos(ang)*b,y1+math.sin(ang)*b], fill=col, width=w); t += 24
    else:
        d.line([x1,y1,x2-math.cos(ang)*head*0.8,y2-math.sin(ang)*head*0.8], fill=col, width=w)
    d.polygon([(x2,y2),(x2-math.cos(ang-0.42)*head,y2-math.sin(ang-0.42)*head),
               (x2-math.cos(ang+0.42)*head,y2-math.sin(ang+0.42)*head)], fill=col)
def zone(im, box, col, alpha=55):
    """반투명 구역(빈 공간·과부하). 호출 뒤 d = ImageDraw.Draw(im) 다시 잡을 것"""
    ov = Image.new("RGBA", im.size, (0,0,0,0)); ImageDraw.Draw(ov).rounded_rectangle(box, radius=18, fill=col+(alpha,))
    im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"))
def numbered_notes(d, y, notes):
    """전술판 아래 번호 설명 (최대 3줄)"""
    for i,t in enumerate(notes):
        d.ellipse([90,y-17,124,y+17], fill=P["ACCENT"]); center(d, (107,y), str(i+1), f(BLACK,20), P["BG"])
        left(d, (140,y), t, f(BOLD,24), P["CREAM"]); y += 50
    return y


# =====================================================================================
# B 양식 (2026-10-17 본인 결정) — 「Claude 로 만든 카드」처럼 흔한 꼴(둥근 상자·가운데 정렬·둥근 결론 바)을 벗어나기
#   · 팀 색을 화면에 크게(면으로) 쓴다 — 점으로 흩어 쓰면 촌스러워진다(밝은 종이·형광펜 시안은 탈락)
#   · 왼쪽 정렬, 각진 모서리, 아주 큰 숫자, 노란 강조(YEL), 결론은 화면 폭 전체 노란 띠
#   · 블로그에는 정지 PNG, 움직이는 버전은 클립용(양식집 _카드양식_시안_2026-10-17/네임카드_모션_양식집.html)
#   · 옛 함수(base·namecard·two_pitches …)는 그대로 둔다 — 지난 글 다시 그릴 때용
# =====================================================================================
from PIL import ImageFilter

YEL   = (245,211,74)
NIGHT = (14,16,22)
INKB  = (240,238,232)
MUTB  = (150,156,168)
# 팀 색 — 실제 팀 색 계열(엠블럼·로고·유니폼 재현은 금지, 색만). 두 팀 색이 비슷하면 옛 의미색(KOR/OPP)으로 돌아간다.
TEAM = {
    "수원삼성": (42,94,224), "수원삼성_적": (208,38,59),
    "화성FC": (238,122,44),
    "안산": (196,202,212),
}
def FB(size, w=900):
    """B 양식 글꼴 — Noto Sans KR 가변 굵기(400·500·700·900)."""
    return f({900: BLACK, 700: BOLD}.get(w, REG), size) if w in (400, 700, 900) else _fw(size, w)
def _fw(size, w):
    fo = ImageFont.truetype(WIN_VF, size); fo.set_variation_by_axes([w]); return fo


class TacticsBoard:
    """B 양식 전술판 — 꼴은 그대로(세로 피치 두 장·위쪽이 상대 골문·점선=사람·실선=공), 디자인만 새로.
    잔디 줄무늬 · 실제 팀 색 · 그림자 원 · 빛나는 공 화살표 · 각진 이름표 · 노란 빗금 빈 공간 · 노란 결론 띠.
    사용:
        tb = TacticsBoard("끌어내서 생긴 틈", "화성 1차전 동점골과 안산전 첫 골 · 위쪽이 상대 골문")
        A, B = tb.A, tb.B
        tb.pitch(A, "화성 1차전 동점골", "68분"); tb.hatch(A, .83,.01,.995,.40)
        tb.player(A, .5,.17, TEAM["수원삼성"]); tb.run(A, (.47,.31),(.50,.20), TEAM["수원삼성"]); tb.ball(A, [(.84,.065),(.53,.16)])
        tb.name(A, .37,.165, "강현묵", TEAM["수원삼성"]); tb.callout(A, .80,.60, "오른쪽이 비었다")
        tb.finish(path, legend=[(색,"수원삼성"),...], notes=[...], foot="결론 한 줄", source="장면: … · 개념도 · 직접 만든 이미지")
    좌표는 피치 비율(0~1). 그리는 순서: pitch → hatch → 배경 선수 → run → ball → 주인공 선수 → name/callout (글씨가 맨 위)."""
    PW, PH = 440, 720

    def __init__(self, title, sub, kicker="전술 도해 · 개념도", H=1440, band=None):
        self.H = H; self.im = Image.new("RGBA", (W, H), NIGHT + (255,))
        self.A, self.B = (60, 270), (580, 270)
        b1, b2 = band or (TEAM["수원삼성"], TEAM["수원삼성_적"])
        l = self._layer(); d = ImageDraw.Draw(l)
        d.polygon([(0,0),(420,0),(400,12),(0,12)], fill=b1 + (255,)); d.polygon([(420,0),(450,0),(430,12),(400,12)], fill=b2 + (255,))
        self._paste(l); d = ImageDraw.Draw(self.im)
        d.text((60,52), kicker, font=FB(22,700), fill=YEL)
        d.text((60,86), title, font=FB(56,900), fill=INKB)
        d.text((60,166), sub, font=FB(24,400), fill=MUTB)

    # --- 내부 ---
    def _layer(self): return Image.new("RGBA", (W, self.H), (0,0,0,0))
    def _paste(self, l): self.im = Image.alpha_composite(self.im, l)
    def pt(self, o, fx, fy): return (o[0] + self.PW*fx, o[1] + self.PH*fy)

    def pitch(self, o, title=None, sub=""):
        x0, y0 = o; x1, y1 = x0 + self.PW, y0 + self.PH; PW, PH = self.PW, self.PH
        b = self._layer(); bd = ImageDraw.Draw(b)
        for i in range(12):                                   # 잔디 깎은 줄무늬
            bd.rectangle([x0, y0 + PH*i/12, x1, y0 + PH*(i+1)/12], fill=((24,62,46,255) if i % 2 == 0 else (28,70,52,255)))
        self._paste(b)
        ln = self._layer(); l = ImageDraw.Draw(ln); C = (255,255,255,150); w = 2
        l.rectangle([x0,y0,x1,y1], outline=C, width=w); l.line([x0,y0+PH/2,x1,y0+PH/2], fill=C, width=w)
        r = PW*0.13; l.ellipse([x0+PW/2-r,y0+PH/2-r,x0+PW/2+r,y0+PH/2+r], outline=C, width=w)
        l.ellipse([x0+PW/2-3,y0+PH/2-3,x0+PW/2+3,y0+PH/2+3], fill=C)
        for top in (True, False):
            yb = y0 if top else y1; s = 1 if top else -1
            for bw, bh in ((PW*0.6, PH*0.13), (PW*0.3, PH*0.05)):
                l.rectangle([x0+(PW-bw)/2, min(yb, yb+s*bh), x0+(PW+bw)/2, max(yb, yb+s*bh)], outline=C, width=w)
            gw = PW*0.16; l.rectangle([x0+(PW-gw)/2, yb-(8 if top else 0), x0+(PW+gw)/2, yb+(0 if top else 8)], fill=(255,255,255,200))
        self._paste(ln)
        if title:
            d = ImageDraw.Draw(self.im); x, y = x0, y0 - 62
            d.rectangle([x, y+6, x+8, y+34], fill=YEL)            # 번호 대신 노란 날 — 아래 설명 번호와 헷갈리지 않게
            d.text((x+20, y), title, font=FB(26,900), fill=INKB)
            if sub: d.text((x+20+d.textlength(title, font=FB(26,900))+12, y+6), sub, font=FB(20,500), fill=MUTB)

    def hatch(self, o, fx0, fy0, fx1, fy1):
        """빈 공간 = 노란 빗금 칸."""
        (x0,y0), (x1,y1) = self.pt(o,fx0,fy0), self.pt(o,fx1,fy1)
        hl = self._layer(); h = ImageDraw.Draw(hl)
        h.rectangle([x0,y0,x1,y1], fill=YEL + (28,))
        for k in range(-int(y1-y0), int(x1-x0), 14): h.line([x0+k, y1, x0+k+(y1-y0), y0], fill=YEL + (90,), width=2)
        mask = Image.new("L", (W, self.H), 0); ImageDraw.Draw(mask).rectangle([x0,y0,x1,y1], fill=255)
        c = self._layer(); c.paste(hl, (0,0), mask); ImageDraw.Draw(c).rectangle([x0,y0,x1,y1], outline=YEL + (220,), width=2)
        self._paste(c)

    def player(self, o, fx, fy, col, r=13):
        x, y = self.pt(o, fx, fy)
        s = self._layer(); ImageDraw.Draw(s).ellipse([x-r+2, y-r+4, x+r+2, y+r+4], fill=(0,0,0,120))
        self._paste(s.filter(ImageFilter.GaussianBlur(3)))
        ImageDraw.Draw(self.im).ellipse([x-r, y-r, x+r, y+r], fill=col, outline=(255,255,255), width=3)

    def name(self, o, fx, fy, text, col, size=16):
        x, y = self.pt(o, fx, fy); fo = FB(size, 700); tw = ImageDraw.Draw(self.im).textlength(text, font=fo)
        bx, by = x - tw/2 - 10, y - size/2 - 7
        b = self._layer(); ImageDraw.Draw(b).rectangle([bx, by, bx+tw+20, by+size+14], fill=(8,10,14,215)); self._paste(b)
        d = ImageDraw.Draw(self.im); d.rectangle([bx, by, bx+4, by+size+14], fill=col); d.text((bx+12, by+3), text, font=fo, fill=INKB)

    def callout(self, o, fx, fy, text, size=17):
        x, y = self.pt(o, fx, fy); d = ImageDraw.Draw(self.im); fo = FB(size, 900); tw = d.textlength(text, font=fo)
        d.rectangle([x-tw/2-10, y-size/2-7, x+tw/2+10, y+size/2+9], fill=YEL); d.text((x-tw/2, y-size/2-4), text, font=fo, fill=NIGHT)

    @staticmethod
    def _head(d, x1, y1, ang, col, head):
        d.polygon([(x1,y1),(x1-math.cos(ang-0.42)*head, y1-math.sin(ang-0.42)*head),(x1-math.cos(ang+0.42)*head, y1-math.sin(ang+0.42)*head)], fill=col)

    def run(self, o, a, b, col, w=4, head=13):
        """사람의 움직임 = 팀 색 점선."""
        (x0,y0), (x1,y1) = self.pt(o,*a), self.pt(o,*b); d = ImageDraw.Draw(self.im)
        ang = math.atan2(y1-y0, x1-x0); L = math.hypot(x1-x0, y1-y0); t = 0
        while t < L - head:
            e = min(t+13, L-head*0.8)
            d.line([x0+math.cos(ang)*t, y0+math.sin(ang)*t, x0+math.cos(ang)*e, y0+math.sin(ang)*e], fill=col, width=w); t += 22
        self._head(d, x1, y1, ang, col, head)

    def ball(self, o, pts, w=4, head=14):
        """공 = 흰 실선 + 은은한 빛. 점 2개면 직선, 3개면 휘어 가는 공(가운데가 조절점)."""
        P = [self.pt(o, *p) for p in pts]
        if len(P) == 2:
            P = [(P[0][0]+(P[1][0]-P[0][0])*i/30, P[0][1]+(P[1][1]-P[0][1])*i/30) for i in range(31)]
        elif len(P) == 3:
            P = [((1-t)**2*P[0][0]+2*(1-t)*t*P[1][0]+t*t*P[2][0], (1-t)**2*P[0][1]+2*(1-t)*t*P[1][1]+t*t*P[2][1]) for t in [i/40 for i in range(41)]]
        g = self._layer(); ImageDraw.Draw(g).line(P[:-1], fill=(255,255,255,90), width=w+8, joint="curve")
        self._paste(g.filter(ImageFilter.GaussianBlur(4)))
        d = ImageDraw.Draw(self.im); d.line(P[:-1], fill=(255,255,255), width=w, joint="curve")
        self._head(d, P[-1][0], P[-1][1], math.atan2(P[-1][1]-P[-3][1], P[-1][0]-P[-3][0]), (255,255,255), head)

    def finish(self, path, legend, notes, foot, source):
        d = ImageDraw.Draw(self.im); y = 1032; x = 60; fo = FB(22,700)
        for col, t in legend:
            d.rectangle([x, y-9, x+18, y+9], fill=col); d.text((x+28, y-15), t, font=fo, fill=INKB); x += 28 + d.textlength(t, font=fo) + 40
        d.line([x, y, x+40, y], fill=(255,255,255), width=4); d.text((x+50, y-15), "공", font=fo, fill=INKB); x += 110
        for k in range(3): d.line([x+k*16, y, x+k*16+9, y], fill=legend[0][0], width=4)
        d.text((x+56, y-15), "사람", font=fo, fill=INKB); x += 140
        d.rectangle([x, y-10, x+22, y+10], outline=YEL, width=2); d.text((x+32, y-15), "빈 공간", font=fo, fill=INKB)
        y = 1086
        for i, t in enumerate(notes[:3]):
            d.rectangle([60, y, 92, y+32], fill=YEL); d.text((70, y-1), str(i+1), font=FB(22,900), fill=NIGHT)
            d.text((106, y-1), t, font=FB(24,500), fill=INKB); y += 50
        d.rectangle([0, self.H-170, W, self.H-82], fill=YEL); d.text((60, self.H-157), foot, font=FB(40,900), fill=NIGHT)
        d.text((60, self.H-56), source, font=FB(18,400), fill=MUTB)
        self.im.convert("RGB").save(path)


def vs_card(path, kicker, title, left_, right_, rows, question, source, H=1180):
    """B 양식 맞대결 카드(썸네일·비교) — 두 팀 색 면을 대각으로 반씩, 아주 큰 숫자 두 개.
    left_/right_ = (팀색, 숫자, 단위, 설명)  rows = [(라벨, 왼쪽 값, 오른쪽 값), …] 최대 4줄."""
    cL, nL, uL, tL = left_; cR, nR, uR, tR = right_
    im = Image.new("RGB", (W, H), NIGHT); d = ImageDraw.Draw(im)
    d.polygon([(0,0),(W*0.56,0),(W*0.44,H),(0,H)], fill=cL); d.polygon([(W*0.56,0),(W,0),(W,H),(W*0.44,H)], fill=cR)
    ov = Image.new("RGBA", (W,H), (0,0,0,0)); od = ImageDraw.Draw(ov)
    od.rectangle([0,0,W,190], fill=(0,0,0,150)); od.rectangle([0,H-230,W,H], fill=(0,0,0,170))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
    d.text((60,52), kicker, font=FB(30,900), fill=(255,255,255)); d.text((60,104), title, font=FB(44,900), fill=YEL)
    def big(x, num, unit, label, right):
        fn, fu = FB(230,900), FB(70,900); wn = d.textlength(num, font=fn); wu = d.textlength(unit, font=fu)
        x0 = x - (wn + wu + 8) if right else x
        d.text((x0,250), num, font=fn, fill=(255,255,255)); d.text((x0+wn+8,390), unit, font=fu, fill=(255,255,255))
        lw = d.textlength(label, font=FB(34,900)); d.text((x-lw if right else x0, 540), label, font=FB(34,900), fill=(255,255,255))
    big(70, nL, uL, tL, False); big(W-70, nR, uR, tR, True)
    y = 640
    for k, a, b in rows[:4]:
        d.text((70,y), a, font=FB(40,900), fill=(255,255,255))
        kw = d.textlength(k, font=FB(26,700)); d.text(((W-kw)/2, y+10), k, font=FB(26,700), fill=(255,255,255))
        bw = d.textlength(b, font=FB(40,900)); d.text((W-70-bw, y), b, font=FB(40,900), fill=(255,255,255))
        d.line([70,y+62,W-70,y+62], fill=(255,255,255), width=1); y += 80
    d.text((60,H-190), question, font=FB(50,900), fill=YEL)
    d.text((60,H-58), source, font=FB(20,400), fill=(220,220,220))
    im.save(path)


def namecard_b(path, col, edge, kicker, num, unit, name, role, rows, yellow, source):
    """B 양식 네임카드(대각 슬래시, 1080×1080) — 팀 색 대각 면 + 큰 숫자 + 이름 + 기록 줄 2개 + 노란 띠.
    양식집의 「대각 슬래시」 마지막 장면과 같다. rows = [(라벨, 값), (라벨, 값)]."""
    S = 1080; im = Image.new("RGB", (S, S), NIGHT); d = ImageDraw.Draw(im)
    d.polygon([(0,0),(S*0.64,0),(S*0.46,S),(0,S)], fill=col); d.polygon([(S*0.64,0),(S*0.67,0),(S*0.49,S),(S*0.46,S)], fill=edge)
    c = lambda v: v*S/100
    d.text((c(6),c(5)), kicker, font=FB(int(c(3.2)),700), fill=(255,255,255))
    fn = FB(int(c(46)),900); bb = d.textbbox((0,0), num, font=fn)          # 숫자 아래끝을 57% 선에 맞춘다(기록 줄과 안 겹치게)
    d.text((c(5)-bb[0], c(57)-bb[3]), num, font=fn, fill=(255,255,255))
    fu = FB(int(c(9)),900); ub = d.textbbox((0,0), unit, font=fu)
    d.text((c(5)+bb[2]-bb[0]+c(1.5)-ub[0], c(57)-ub[3]), unit, font=fu, fill=(255,255,255))
    fnm = FB(int(c(15)),900); nw = d.textlength(name, font=fnm); d.text((S-c(6)-nw, c(14)), name, font=fnm, fill=(255,255,255))
    fr = FB(int(c(3.4)),700); rw = d.textlength(role, font=fr); d.text((S-c(6)-rw, c(33)), role, font=fr, fill=(255,255,255))
    for i, (k, v) in enumerate(rows[:2]):
        y = c(63) + i*c(10)
        d.text((c(6), y+c(1.6)), k, font=FB(int(c(3)),500), fill=(255,255,255))
        fv = FB(int(c(6)),900); vw = d.textlength(v, font=fv); d.text((S-c(6)-vw, y), v, font=fv, fill=(255,255,255))
        d.line([c(6), y+c(8), S-c(6), y+c(8)], fill=(255,255,255), width=1)
    fy = FB(int(c(5.2)),900); yw = d.textlength(yellow, font=fy)
    d.rectangle([c(5), c(84), c(5)+yw+c(6), c(84)+c(8.4)], fill=YEL); d.text((c(8), c(85.2)), yellow, font=fy, fill=NIGHT)
    d.text((c(5), S-c(4.6)), source, font=FB(int(c(2.1)),400), fill=(220,220,220))
    im.save(path)
