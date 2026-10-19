# 네이버 클립 PC 업로드(clipcreators.naver.com) 자동 입력 — [등록]·[임시저장]은 누르지 않는다
#
# 사용:  python fill_clip.py <clip_upload.json>            새 업로드부터
#        python fill_clip.py <clip_upload.json> --here     이미 영상을 넣은 화면에 나머지만 채움
#
# clip_upload.json 예:
# {
#   "video": "C:/.../clip/out/gamak_clip.mp4",
#   "description": "…(300자 이내)",
#   "cover_at": 3.0,                        # 영상의 이 시각(초) 장면을 뽑아 커버로 올림 — 이게 있으면 cover_index 무시
#   "cover_index": 0,                       # 자동 커버 후보 순서(0부터), 생략하면 기본값
#   "category": ["여행", "국내여행"],
#   "ai": true,                             # Higgsfield 움직임·AI 내레이션을 썼으면 true
#   "info_tag": {"type": "공연·축제·전시", "query": "감악산", "match": "감악산 꽃별"},
#   "blog": "감악산 꽃별여행 | 후기",         # 블로그 글 제목 일부 (콘텐츠 링크 → 블로그)
#   "schedule": "2026-10-08 19:00",         # 생략하면 즉시 등록용(예약 안 함)
#   "comments": true
# }
import sys, os, re, json, time, subprocess, urllib.request
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
PROFILE = os.path.join(BASE, "chrome_profile")
PORT = 9334
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
UPLOAD_URL = "https://clipcreators.naver.com/web/upload"
# 「오늘 클립 챌린지」 이달의 해시태그 — 매월 1일 조건 확인 후 바꾼다(지침 7-2, 2026-10 기준)
CHALLENGE_TAGS = ["#오늘클립챌린지"]
# 이달의 보너스 해시태그 — 설명에 이 낱말이 있으면(=글과 연관이 있으면) 반드시 붙인다(10/8 사용자: 보너스 금액이 있으니 연관 있으면 무조건)
BONUS_TAGS = {"#단풍": ["단풍", "은행나무", "억새", "가을 산", "가을산", "가을 코스", "가을 여행"]}


def log(s):
    print(s, flush=True)


def ensure_chrome():
    """블로그 자동화 프로필 크롬을 디버깅 포트로 띄워 둔다(이미 떠 있으면 그대로)."""
    try:
        urllib.request.urlopen("http://127.0.0.1:%d/json/version" % PORT, timeout=2)
        return
    except Exception:
        pass
    subprocess.Popen([CHROME, '--user-data-dir=%s' % PROFILE, '--remote-debugging-port=%d' % PORT,
                      '--no-first-run', '--window-size=1400,1000', UPLOAD_URL])
    for _ in range(30):
        time.sleep(1)
        try:
            urllib.request.urlopen("http://127.0.0.1:%d/json/version" % PORT, timeout=2)
            return
        except Exception:
            pass
    raise SystemExit("크롬 디버깅 포트가 안 열립니다")


def _pick_in_list(pg, match):
    btns = pg.locator("[class*=Modal] button[class*=selectBtn]")
    for i in range(btns.count()):
        b = btns.nth(i)
        # [선택] 버튼을 감싼 카드까지 올라가 제목을 읽는다
        text = b.evaluate("e => { let c = e.parentElement; while (c && c.innerText.trim() === '선택') c = c.parentElement; return c ? c.innerText : '' }")
        text = re.sub(r"<[^>]+>", "", text)  # 검색 결과 제목에 <em class="srch"> 가 글자로 섞여 나온다
        # 공백·「|」 무시하고 비교(10/9: blog 값 「거창 감악산 축제 셔틀 주차」 가 제목의 「축제 | 셔틀」 때문에 안 맞았다)
        if re.sub(r"[\s|]", "", match) in re.sub(r"[\s|]", "", text):
            b.click()
            pg.wait_for_timeout(800)
            return text.strip().split("\n")[0]
    return None


def modal_pick(pg, query, match):
    """정보태그·블로그 팝업: 지금 목록에서 먼저 찾고, 없으면 검색 → match 가 들어간 카드의 [선택]."""
    got = _pick_in_list(pg, match)
    if got:
        return got
    inp = pg.locator("[class*=Modal] input[class*=TagSearchBar_searchInput]")
    inp.fill(query)
    inp.press("Enter")
    pg.wait_for_timeout(2500)
    got = _pick_in_list(pg, match)
    if not got:
        pg.locator("[class*=Modal_closeBtn]").first.click()
    return got


def toggle(pg, label, want):
    row = pg.locator("text=%s" % label).first.locator("xpath=ancestor::*[.//button[@role='switch']][1]")
    sw = row.locator("button[role=switch]").first
    on = "toggleOn" in (sw.get_attribute("class") or "")
    if on != want:
        sw.click()
        pg.wait_for_timeout(400)


def main(cfg_path, here=False):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    warn = []
    ensure_chrome()
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:%d" % PORT)
        ctx = b.contexts[0]
        pages = [x for x in ctx.pages if "clipcreators.naver.com" in x.url]
        # 새 업로드는 항상 새 탭 — 아직 [등록] 안 누른 다른 클립 화면을 덮어쓰지 않게
        pg = (pages[0] if pages else ctx.new_page()) if here else ctx.new_page()
        pg.bring_to_front()

        if not here:
            pg.goto(UPLOAD_URL, wait_until="domcontentloaded")
            pg.wait_for_timeout(2000)
            if "nid.naver.com" in pg.url:
                raise SystemExit("네이버 로그인이 필요합니다. 크롬에서 로그인한 뒤 다시 실행하세요.")
            # Playwright 파일 전송은 50MB 제한(원격 취급) → CDP 로 경로만 넘긴다
            pg.locator("input[type=file]").first.wait_for(state="attached", timeout=30000)
            cdp = ctx.new_cdp_session(pg)
            obj = cdp.send("Runtime.evaluate", {"expression": "document.querySelector('input[type=file]')"})["result"]
            cdp.send("DOM.setFileInputFiles", {"objectId": obj["objectId"], "files": [os.path.abspath(cfg["video"])]})
            log("영상 넣음: %s" % os.path.basename(cfg["video"]))
        pg.locator("textarea[class*=ClipDetailForm_textarea]").wait_for(timeout=120000)

        # 설명
        desc = cfg["description"]
        # 이달의 챌린지 태그(지침 7-2) — 주제 해시태그 8개 뒤에 붙인다. 이미 있으면 그대로
        extras = list(cfg.get("challenge_tags", CHALLENGE_TAGS))
        for tag, words in BONUS_TAGS.items():
            if tag in cfg.get("bonus_tags", []) or any(w in desc for w in words):
                extras.append(tag)
        for extra in extras:
            if extra not in desc.split():
                desc = desc.rstrip() + " " + extra
                if extra != CHALLENGE_TAGS[0]:
                    log("보너스 태그 붙임: %s" % extra)
        if len(desc) > 300:
            warn.append("설명이 %d자라 300자로 잘랐습니다" % len(desc))
            desc = desc[:300]
        tags = [t for t in re.findall(r"#\S+", desc) if t not in CHALLENGE_TAGS and t not in BONUS_TAGS]
        if len(tags) != 8:
            warn.append("주제 해시태그가 %d개입니다 — 8개로 고정 (클립영상_지침 2-5, 챌린지 태그는 따로)" % len(tags))
        ta = pg.locator("textarea[class*=ClipDetailForm_textarea]")
        ta.fill(desc)
        log("설명 %d자" % len(desc))

        # 커버 — cover_at(초)이 있으면 영상의 그 장면을 뽑아 직접 올린다(자동 후보엔 원하는 장면이 없을 때가 많다, 10/7)
        if cfg.get("cover_at") is not None:
            img = os.path.splitext(cfg["video"])[0] + "_cover.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cfg["cover_at"]), "-i", cfg["video"],
                            "-frames:v", "1", "-q:v", "2", img], check=True)
            pg.locator("input[class*=coverUploadInput]").set_input_files(img)
            pg.wait_for_timeout(4000)
            first = pg.locator("button[class*=ClipDetailForm_coverItem]").first
            if "coverSelected" in (first.get_attribute("class") or ""):
                log("커버: 영상 %s초 장면을 올림" % cfg["cover_at"])
            else:
                warn.append("커버 이미지를 올렸지만 선택되지 않았습니다 — 화면에서 첫 칸을 눌러 주세요")
        elif "cover_index" in cfg:
            covers = pg.locator("button[class*=ClipDetailForm_coverItem]")
            pg.wait_for_timeout(1000)
            if covers.count() > cfg["cover_index"]:
                covers.nth(cfg["cover_index"]).click()
                log("커버 %d번째" % (cfg["cover_index"] + 1))
            else:
                warn.append("커버 후보가 %d개뿐이라 기본 커버 그대로" % covers.count())

        # 카테고리
        c1, c2 = cfg["category"]
        dd = pg.locator("button[class*=ClipDetailForm_dropdown]")
        dd.nth(0).click(); pg.wait_for_timeout(500)
        exact = lambda t: re.compile("^%s$" % r"\s*".join(map(re.escape, re.sub(r"\s+", "", t))))  # 10/8: 「문학, 인문, 교양」 은 공백·줄바꿈이 섞여 있어 글자만 비교
        opt1 = pg.locator("button[class*=dropdownOption]").filter(has_text=exact(c1))
        if not opt1.count():   # 10/8: 처음 쓰는 분야(책)는 1차 이름을 모른다 → 목록을 알려 주고 넘어감
            names = [t.strip() for t in pg.locator("button[class*=dropdownOption]").all_inner_texts()]
            pg.keyboard.press("Escape")
            warn.append("1차 카테고리 '%s' 가 없습니다. 고를 수 있는 것: %s" % (c1, ", ".join(names)))
            opt2 = None
        else:
            opt1.first.click(); pg.wait_for_timeout(700)
            dd.nth(1).click(); pg.wait_for_timeout(500)
            opt2 = pg.locator("button[class*=dropdownOption]").filter(has_text=exact(c2))
        if opt2 is None:
            pass
        elif opt2.count():
            opt2.first.click(); pg.wait_for_timeout(400)
            log("카테고리 %s > %s" % (c1, c2))
        else:
            names = [t.strip() for t in pg.locator("button[class*=dropdownOption]").all_inner_texts()]
            pg.keyboard.press("Escape")
            warn.append("2차 카테고리 '%s' 가 없습니다. 고를 수 있는 것: %s" % (c2, ", ".join(names)))

        # AI 활용 · 광고
        toggle(pg, "AI 활용 설정", bool(cfg.get("ai")))
        toggle(pg, "협찬 설정", bool(cfg.get("ad")))
        log("AI 활용 %s" % ("켬" if cfg.get("ai") else "끔"))

        # 정보 태그
        tag = cfg.get("info_tag")
        if tag:
            pg.locator("button[class*=tagBtn]", has_text=tag["type"]).first.click(); pg.wait_for_timeout(1500)
            got = modal_pick(pg, tag["query"], tag.get("match", tag["query"]))
            log("정보태그: %s" % got) if got else warn.append("정보태그 '%s' 를 못 찾았습니다" % tag["query"])

        # 콘텐츠 링크 → 블로그
        if cfg.get("blog"):
            pg.locator("button[class*=tagBtn]", has_text="블로그").first.click(); pg.wait_for_timeout(1500)
            # 목록엔 최근 30편만 뜬다. 그보다 오래된 글은 검색해야 하는데, 제목 단어로 검색하면
            # 연결 제목에 <em class="srch"> 가 글자로 박힌다 → blog_query 에 「본문에만 있는 단어」를 준다
            key = cfg.get("blog_query") or cfg["blog"].split("|")[0].strip()
            got = modal_pick(pg, key, cfg["blog"])
            log("블로그 연결: %s" % got) if got else warn.append("블로그 글 '%s' 를 못 찾았습니다" % cfg["blog"])
            sel = pg.locator("[class*=selectedLinkTitle]")
            if sel.count() and "srch" in sel.first.inner_text():
                warn.append("블로그 연결 제목에 <em class=\"srch\"> 가 들어갔습니다 — X 로 지우고 blog_query 에 본문 단어를 넣어 다시")

        # 공개 설정
        resv = pg.locator("label", has_text="등록 예약").locator("input[type=checkbox]")
        if cfg.get("schedule"):
            if not resv.is_checked():
                pg.locator("label", has_text="등록 예약").click(); pg.wait_for_timeout(600)
            warn.append("예약 시각 %s 은 아직 손으로 맞춰 주세요 (날짜·시·분 선택기는 미구현)" % cfg["schedule"])
        elif resv.is_checked():
            pg.locator("label", has_text="등록 예약").click()
        pg.locator("label").filter(has_text=re.compile("^%s$" % ("허용 안함" if cfg.get("comments") is False else "허용"))).first.click()

        ta.scroll_into_view_if_needed()
        log("")
        log("=" * 56)
        log("입력 완료 — [등록]은 화면을 확인한 뒤 직접 누르세요.")
        for w in warn:
            log("!! " + w)
        log("=" * 56)


if __name__ == "__main__":
    main(sys.argv[1], here="--here" in sys.argv)
