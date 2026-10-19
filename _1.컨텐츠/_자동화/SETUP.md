# 다른 컴퓨터에 설치하기

## 0. 미리 있어야 할 것

- **Python 3.10 이상** — https://www.python.org (설치 시 "Add python.exe to PATH" 체크)
- **Google Chrome** (일반 크롬. 스크립트가 `channel="chrome"`으로 실제 크롬을 쓴다)
- **Claude Code**

> ⚠️ **Claude for Chrome 확장은 필요 없다.** 네이버가 확장의 안전 차단 목록에 올라
> 있어서 `blog.naver.com` 접근이 아예 막힌다. 설치해도 소용없으니 하지 말 것.
> 이 자동화는 확장과 무관한 Playwright 경로를 쓴다.

## 1. 패키지 설치 (명령 두 줄)

```bash
pip install playwright pillow
python -m playwright install chromium
```

- `playwright` : 브라우저 자동 조작
- `pillow` : 사진 확인·대조용 (초안 작성 시 사진 배정 검토에 쓴다)
- `install chromium` : 예비 브라우저 내려받기(약 150MB). 평소 크롬은 안 건드린다

설치 확인:

```bash
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## 2. 스크립트 복사

`C:\Users\user\Desktop\Blog\네이버 블로그\_자동화\` 에서 **아래 5개만** 복사하면 된다.

```
editor_util.py     에디터 프레임 확보 + '작성 중인 글' 팝업 처리
md_parser.py       초안 md → 블록 파싱
naver_login.py     로그인 프로필 준비 (최초 1회)
fill_editor.py     본문 채우기 (본체)
SETUP.md           이 문서
```

`dbg_*.py`, `*.png`, `__pycache__` 는 개발 중 만든 것이라 **복사하지 않는다.**
단 `dbg_update_url.py` 와 `dbg_clear.py` 두 개는 수정 모드가 깨졌을 때 원인을 가르는 용도라
같이 복사해두면 편하다 (6장 참고).

> ⛔ **`chrome_profile\` 폴더는 절대 복사하지 말 것.**
> 로그인 세션이 들어 있다. 컴퓨터마다 새로 로그인하는 게 맞고, 안전하다.

## 3. 최초 1회 로그인

```bash
cd "<스크립트를 둔 폴더>"
python naver_login.py
```

- 크롬 창이 뜨면 **직접 네이버 로그인** (2단계 인증까지)
- 스크립트는 로그인 여부만 확인하고, 아이디·비밀번호는 다루지 않는다
- 성공하면 `chrome_profile\` 이 생기고 창이 닫힌다
- 이후로는 자동 로그인되므로 다시 할 필요 없다

## 4. 블로그 주소 확인

`fill_editor.py` 상단의 이 줄이 본인 블로그 ID여야 한다.

```python
BLOG_ID, IMG_SUB = "baiyan_novembre", "260906"
```

- `BLOG_ID` : blog.naver.com/**여기** 부분
- `IMG_SUB` : md 파일과 같은 폴더 안의 사진 하위폴더 이름 (글마다 다르면 수정).
  그런 폴더가 없으면 md가 있는 폴더에서 사진을 찾는다

## 5. 실행

```bash
python fill_editor.py "<초안 md 전체경로>"
```

- 크롬이 뜨고 제목 → 본문 → 사진 → 표 → 해시태그 순으로 채운다
- **발행도 임시저장도 하지 않는다.** 채우기만 하고 창을 열어둔 채 대기한다
- 검토 후 직접 발행 버튼을 누른다. 창을 닫으면 스크립트가 끝난다

## 6. 발행된 글 수정하기

이미 발행한 글을 고칠 때는 `--post` 에 글번호를 준다.

```bash
python fill_editor.py "<수정본 md 전체경로>" --post <글번호>
```

**글번호 찾는 법** — 글 주소 `blog.naver.com/baiyan_novembre/224419499878` 의 숫자다.
제목만 알면 RSS 로도 찾는다 (인증 불필요, 최근 50개):

```bash
python -c "import urllib.request,re; d=urllib.request.urlopen(urllib.request.Request('https://rss.blog.naver.com/baiyan_novembre.xml',headers={'User-Agent':'curl/8'})).read().decode('utf-8','replace'); [print(re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>',i,re.S).group(1)[:50],'|',re.search(r'/(\d+)\?',i).group(1)) for i in re.findall(r'<item>(.*?)</item>',d,re.S)[:10]]"
```

### 동작 방식 — 부분 수정이 아니라 전체 교체다

기존 제목과 본문을 **통째로 지우고** md 기준으로 처음부터 다시 채운다.
문단을 찾아 바꾸는 게 아니다. 그래서:

- **md 가 유일한 원본이다.** 에디터에서 직접 손본 내용은 md 에 없으면 사라진다
- **사진이 매번 새로 올라간다.** 3장에 약 3분. 그래서 **대표사진 지정이 풀린다** — 발행 팝업에서 다시 잡을 것
- **글 자체는 유지된다.** 수정이라서 URL·발행일시·댓글·공감 그대로
- **몇 번을 다시 돌려도 안전하다.** 비우기부터 다시 하므로 내용이 쌓이지 않는다

비우기가 덜 되면 **채우지 않고 멈춘다.** 그대로 채우면 발행된 글에 내용이 두 번 들어가기 때문이다.
로그의 `비우기 N회차 - 남은 본문 컴포넌트 N개` 가 **0 또는 1이면 정상**이다.

### 2026-09-22 에 확인한 것 — 추측으로 되돌리지 말 것

```
🚫 blog.naver.com/<id>/<logNo>?Redirect=Update  -> 글 보기 화면이다. 에디터가 아니다
🚫 PostWriteForm.naver?...&Redirect=Update      -> 빈 화면. redirect 가 대문자면 안 먹는다
⭕ PostWriteForm.naver?blogId=<id>&logNo=<logNo>&redirect=Update  -> 이것만 동작한다

🚫 수정 화면에는 iframe#mainFrame 이 없다. 새 글 화면과 구조가 다르다
⭕ 수정 화면은 최상위 프레임이 곧 에디터다. get_editor_frame 이 둘 다 받는다

🚫 se-documentTitle(제목 칸)도 se-component 라서 전체를 세면 비워도 2개가 남는다
⭕ 본문만 세려면 .se-component:not(.se-documentTitle)
```

확인에 쓴 진단 스크립트는 그대로 두었다. **둘 다 아무것도 고치지 않는다.**

- `dbg_update_url.py <글번호>` — 수정 주소 후보를 차례로 열어 프레임 구조와 스크린샷을 남긴다
- `dbg_clear.py <글번호>` — 비우기 전후로 어떤 컴포넌트가 남는지 찍는다

### 아직 없는 것

제목만 고치는 것 같은 **부분 수정 모드는 없다.** 작은 수정에도 사진을 전부 다시 올린다.
사진이 많은 글을 자주 고치게 되면, 사진 블록은 건드리지 않고 텍스트만 갈아끼우는 모드를 붙이는 쪽이
부분 수정보다 낫다 — 가정이 적어서 덜 깨진다.

## 알려진 제약

| 항목 | 내용 |
|---|---|
| 표 열 수 | 네이버 기본이 3열이지만 남는 빈 열을 자동으로 지운다. 실패하면 경고로 알린다 |
| 프로필 동시 사용 | 크롬 창이 열려 있으면 다른 스크립트가 같은 프로필을 못 쓴다. 먼저 닫을 것 |
| 카테고리 | 아직 자동 선택 안 함. 발행 팝업에서 직접 고른다 |
| 사진 배정 | md에 파일명이 정확히 적혀 있어야 한다 (초안작성_프롬프트.md 참고) |
| 사진 폴더 | `IMG_SUB` 하위폴더가 없으면 md와 같은 폴더에서 찾는다 |
| 링크 | `[[LINK:URL \| 표시할 글]]` 한 줄이 텍스트 링크가 된다(카드형 아님). 끝에 적용 개수를 검증한다 |

## 문제가 생기면

- **"작성 중인 글이 있습니다" 팝업** → 자동으로 [취소] 처리된다. 그래도 멈추면 수동으로 닫고 재실행
- **프로필 잠김 오류** → 열려 있는 자동화 크롬 창을 모두 닫고 다시 실행
- **로그인 풀림** → `python naver_login.py` 다시 실행
