# 인수인계서 — claude-watch-kr 영상분석 스킬 + 브릿지(API) 이식

작성일: 2026-09-17 (같은 날 1차 개정 — 5·6·7항과 4-2b 추가)
대상: 이 스킬을 새 PC에서 다시 쓰려는 사람 (본인 포함)
요약: **현재 PC의 `~/.claude/skills/claude-watch-kr` 폴더가 유일한 원본이다.** 이 폴더를 통째로
옮기고, API 키 2개를 새 PC에서 **다시 입력**하면 끝난다. 브릿지 모드만 쓸 거면 설치할 프로그램은 없다.

---

## 0. 먼저 알아야 할 것 (중요)

| 항목 | 상태 |
|---|---|
| 스킬 본체 | `C:\Users\admin\.claude\skills\claude-watch-kr` (약 418KB) — **유일본** |
| 원본 GUI 폴더 `Transcript_Bridge_v1.5` | **이 PC에 더 이상 없음** (삭제됨) |
| 배포 폴더 `claude-watch-kr-배포` + `deploy.py` | **이 PC에 더 이상 없음** (삭제됨) |
| API 키 | `%APPDATA%\TranscriptBridge\settings.json` 에 **DPAPI 암호화** 저장 |

기존 스킬 문서(`references/other-pc.md`)는 "RUN.bat 으로 GUI 를 열어 키를 입력하라"고 되어 있는데,
**그 RUN.bat 은 이 PC에 이제 없다.** 대신 스킬 안의 `scripts\bridge_engine.py` 자체가
v1.5 GUI 를 통째로 품고 있으므로, **인자 없이 실행하면 같은 GUI 가 뜬다.** 아래 3단계가 그 방법이다.

### ⚠️ 이 PC를 정리하기 전에 반드시 할 일

API 키는 **Windows DPAPI**로 암호화돼 있다. DPAPI 는 **이 PC + 이 Windows 계정**에 묶여 있어서,
`settings.json` 파일을 복사해 가도 **새 PC에서는 절대 복호화되지 않는다.**

→ **이 PC가 살아 있는 동안 평문 키를 뽑아 두어야 한다.** (1단계)
→ 못 뽑고 PC를 잃으면, 두 서비스(Google AI Studio / YepAPI)에서 **키를 새로 발급**받아야 한다.

---

## 1. [구 PC에서] 평문 API 키 회수

PowerShell 에서 아래를 실행하면 화면에 키 2개가 그대로 찍힌다.
**화면에 뜬 값을 비밀번호 관리자나 안전한 메모에 옮겨 적는다. 이 파일에는 적지 않는다.**

```powershell
python -c "import sys; sys.path.insert(0, r'$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts'); import bridge_engine as b; s=b.load_settings(); print('GEMINI =', s.get('gemini_key')); print('YEP    =', s.get('yep_key'))"
```

- 정상이면 `GEMINI = AIza...`, `YEP = ...` 형태로 출력된다.
- 빈 값이거나 오류가 나면 이미 복호화가 불가능한 상태다 → **3-B (재발급)** 로 간다.
- 실행 후 콘솔 기록이 남지 않게 창을 닫는다. (`Clear-History` 도 같이)

> 키가 유효한지는 GUI 를 열지 않아도 3단계 마지막 검증으로 확인된다.

---

## 2. [구 PC → 새 PC] 파일 옮기기

옮길 것은 **폴더 하나**다.

```
C:\Users\admin\.claude\skills\claude-watch-kr\
```

새 PC의 같은 위치에 넣는다 (계정명은 다를 수 있다):

```
C:\Users\<새계정>\.claude\skills\claude-watch-kr\
```

복사할 때 **빼도 되는 것** (없어도 동작한다):
- `scripts\__pycache__\`, `scripts\watchlib\__pycache__\` — 파이썬 캐시
- `scripts\bridge_engine.py.bak`, `scripts\bridge_engine.py.bak-260917-pre-nogemini` — 백업본
  (다만 **뒤엣것은 2026-09-17 수정 직전 상태**라 되돌릴 일이 생기면 필요하다. 용량이 작으니 같이 가져가길 권한다)

**절대 빼면 안 되는 것:**
```
SKILL.md                     스킬 정의 (이 파일이 없으면 Claude가 스킬을 인식 못 한다)
config.json                  블로그 루트 / 기본 프레임 수
scripts\videoscan.py         진입점 (로컬 → 브릿지 자동 전환 담당)
scripts\bridge_engine.py     브릿지 본체 + GUI (v1.5 복사본 + 로컬 수정분, 아래 7항 참조)
scripts\watchlib\*.py        공용 모듈 4개 (timestamps.py 가 그리드 생성 담당)
references\*.md              설치·이식 참고 문서
```

`%APPDATA%\TranscriptBridge\settings.json` 은 **옮겨도 쓸모없다** (DPAPI). 옮기지 않아도 된다.

---

## 3. [새 PC에서] 설정

### 사전 조건

- **Python 3.10 이상** (권장 3.12~3.14). `python --version` 으로 확인.
- 외부 패키지 설치 **불필요**. `bridge_engine.py` 는 표준 라이브러리만 쓴다
  (tkinter 포함 — 파이썬 설치 시 tcl/tk 옵션이 켜져 있어야 GUI 가 뜬다).
- 브릿지 모드만 쓸 거면 **ffmpeg / yt-dlp / whisper 전부 필요 없다.** 프레임을 서버에서 받는다.
- 로컬 모드도 쓰려면 `references\setup-windows.md` 를 따른다.

### 3-A. API 키 입력 (회수한 키가 있을 때)

GUI 를 띄워 입력하는 방식이 표준이다. 인자 없이 실행하면 Transcript Bridge v1.5 GUI 가 뜬다.

```powershell
python "$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts\bridge_engine.py"
```

1. **Settings** 탭으로 이동
2. `Gemini API Key` 와 `YepAPI Key` 에 1단계에서 회수한 값을 붙여넣기
3. **"이 PC에서 API 키 기억하기 (Windows DPAPI 암호화)"** 체크박스를 **켠다**
4. 저장하고 GUI 를 닫는다

이러면 새 PC 계정 기준으로 다시 암호화되어 `%APPDATA%\TranscriptBridge\settings.json` 에 저장된다.
이후 스킬이 알아서 읽는다.

> **키를 명령줄 인자로 넘기지 않는다.** 프로세스 목록에 평문으로 남는다. 스크립트도 그 인자를 받지 않는다.

GUI 가 안 뜨는 환경(tkinter 없음 / 원격 세션)이면 **환경변수 대체**가 가능하다. 단 평문 저장이라 권장하지 않는다.

```powershell
[Environment]::SetEnvironmentVariable('GEMINI_API_KEY','<키>','User')
[Environment]::SetEnvironmentVariable('YEPAPI_KEY','<키>','User')
```
설정 후 **새 터미널**을 열어야 반영된다. 코드는 DPAPI 저장분을 먼저 보고, 없으면 환경변수를 쓴다.

### 3-B. 키를 회수 못 했을 때 — 재발급

| 키 | 발급처 | 용도 |
|---|---|---|
| `GEMINI_API_KEY` | Google AI Studio (aistudio.google.com) — API keys | 영상 이해 + 중요 장면 타임스탬프 선정 |
| `YEPAPI_KEY` | YepAPI (api.yepapi.com) 대시보드 | 유튜브 프레임 스크린샷 생성 + 프록시 수신 |

발급받은 뒤 3-A 와 동일하게 입력한다.

기본 모델은 `gemini-3.8-flash` 다. 이 모델이 사라졌거나 계정에서 안 되면 GUI Settings 의
모델 칸에서 바꾼다 (코드 상수는 `bridge_engine.py` 의 `DEFAULT_GEMINI_MODEL`).

### 3-C. blog_root 경로 수정

`claude-watch-kr\config.json` 이 현재 이렇게 되어 있다:

```json
{
  "blog_root": "D:/Base_JBS/개인/네이버 블로그",
  "bridge_source_version": "1.5",
  "default_max_frames": 24
}
```

`blog_root` 를 **새 PC의 실제 블로그 폴더 경로**로 고친다.
**슬래시(`/`)를 쓰는 게 안전하다.** 역슬래시를 쓰려면 반드시 두 번 (`D:\경로`) — 한 번이면 JSON 오류.

경로를 안 고치면:
```
[videoscan] 블로그 루트가 존재하지 않습니다: ...
  config.json 의 blog_root 를 고치세요.
```
JSON 을 잘못 고치면 "JSON 형식 오류" 가 뜬다 — 경로 문제가 아니라 형식 문제다.

한 번만 다른 곳에 쓰려면 파일을 고치지 말고 실행 시 `--blog-root "E:\다른경로"` 를 붙인다.

---

## 4. 검증 (비용 거의 0)

### 4-1. 스킬 인식 확인
새 PC에서 Claude Code 를 열고 스킬 목록에 `claude-watch-kr` 가 보이는지 확인한다.
안 보이면 폴더 위치(`~\.claude\skills\claude-watch-kr\SKILL.md`)를 다시 본다.

### 4-2. 브릿지 연결 확인 (Gemini 1회만 과금, YepAPI 0회)

```powershell
python "$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts\bridge_engine.py" `
  --capture "https://www.youtube.com/watch?v=tpoV4u_fd3s" `
  --out "$env:TEMP\check" --dry-run
```

- 마지막 줄이 `[bridge] DRYRUN <프레임수> <예상호출수>` 면 **정상**이다.
- `$env:TEMP\check\transcript.txt` 가 `[mm:ss] 문장` 형식으로 생겼는지도 같이 본다.
- `[bridge] Gemini API 키가 없습니다...` 가 뜨면 3-A 가 안 된 것이다.
- **중간에 이 줄이 뜨고도 `DRYRUN` 으로 끝났다면 그것도 정상이다** — Gemini 만 실패하고
  그리드 모드로 내려간 것이다. 자막·YepAPI 경로는 살아 있다는 뜻이다:
  ```
  [bridge] Gemini 호출 실패: HTTP 429 ...
  [bridge] Gemini 없이 균등 그리드로 진행합니다 (자료화면 선정 없음 - 프레임 간격이 일정해집니다).
  ```

### 4-2b. Gemini 없이만 검증하고 싶을 때 (호출 0회)

```powershell
python "$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts\bridge_engine.py" `
  --capture "https://www.youtube.com/watch?v=tpoV4u_fd3s" `
  --out "$env:TEMP\check2" --no-gemini --dry-run
```

Gemini 키가 아직 없어도 통과해야 한다. `DRYRUN 16 32` 가 나오면 정상이다.

### 4-3. 전체 경로 확인 (여기서부터 YepAPI 과금)

```powershell
python "$env:USERPROFILE\.claude\skills\claude-watch-kr\scripts\videoscan.py" "<유튜브 URL>" --max-frames 12
```

마지막 줄 `[videoscan] READY <경로>` 가 나오면 이식 완료다.
`--max-frames 12` 는 비용을 절반으로 줄인 확인용 값이다 (YepAPI 약 24회).

---

## 5. 비용 구조 (알고 있어야 할 것)

| 경로 | 비용 |
|---|---|
| 로컬 (yt-dlp 성공) | **0원** |
| 브릿지 — Gemini 모드 | Gemini 1회 + **YepAPI 프레임당 2회** |
| 브릿지 — 그리드 모드 (Gemini 실패 시 자동) | Gemini 0회 + **YepAPI 프레임당 2회** (프레임이 16장에서 고정) |

- Gemini 모드: 기본 24프레임 = YepAPI 약 48회. `--max-frames 12` 면 약 24회.
- **그리드 모드는 `--max-frames` 를 아무리 올려도 16장(훅 4 + 본문 12)에서 멈춘다** →
  YepAPI 약 32회로 고정이다. 더 촘촘히 보려면 `scripts\watchlib\timestamps.py` 의
  `BODY_POINTS`(기본 12)를 올려야 한다.
- 브릿지로 넘어가는 순간 콘솔에 사유와 예상 비용이 먼저 찍힌다:
  ```
  [videoscan] 로컬 실패 (HTTP 403) -> 브릿지 모드로 전환
  [videoscan] 예상 비용: Gemini 1회 + YepAPI 약 48회
  ```
- 유료 호출을 절대 막고 싶으면 `--no-fallback` 을 붙인다.
- 같은 영상을 다시 돌리면 **비용이 다시 발생한다.** 결과 폴더(`_raw\`)를 지우지 말고 재사용한다.

### ⚠️ Gemini 무료 티어는 하루 20회다

2026-09-17 실측. 영상 6편을 돌리다 소진돼 나온 에러 메시지다:

```
HTTP 429: You exceeded your current quota
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests,
  limit: 20, model: gemini-3.8-flash
```

**실패한 호출도 카운트에 들어간다.** 과부하(500)로 실패한 시도까지 합쳐 20회를 넘기면 그날은 끝이다.
쿼터는 태평양 시간 자정(= 한국시간 16~17시경)에 초기화된다.
하루에 영상을 여러 편 돌릴 계획이면 **유료 결제를 붙이거나, 아래 그리드 모드로 돌리는 것을 전제**로 해야 한다.

---

## 6. 알려진 제약

- **브릿지 폴백은 유튜브 전용.** 인스타·틱톡·Loom·로컬 mp4 는 로컬이 막히면 그냥 실패한다
  → 그때는 영상 파일을 직접 받아 로컬 경로로 돌린다 (ffmpeg/yt-dlp 필요).
- 로그인이 필요한 비공개 영상은 양쪽 다 실패한다. 브릿지는 자막 API 단계에서 멈추므로 **과금은 없다.**
- 브릿지 모드에는 **컷 검출 통계가 없다** (원본 파일이 없어서). 평균 숏 길이·분당 컷 수를 주장하면 안 된다.
- 30분 초과 영상은 로컬 모드에서 컷 검출을 자동으로 건너뛴다.
- **자막이 없는 영상은 그리드 모드로도 못 돌린다.** 영상 길이를 자막 마지막 구간에서 뽑기 때문이다.
  Gemini 까지 막힌 상태면 길이를 알 방법이 아예 없어 유료 호출 전에 중단된다.
- **YepAPI 가 못 찍는 영상이 있다.** 2026-09-17 실측: 라이브 아카이브 1편에서 `HTTP 502` 가
  연속 3회 떠 캡처가 중단됐다(21회 호출 소모). 서버측 문제이므로 시간을 두고 재시도하는 것 외에 방법이 없다.
- **네트워크 환경에 따라 유튜브 직접 접속이 통째로 막힐 수 있다.** 2026-09-17 이 PC 에서
  `youtube.com` 이 전부 연결 초기화(WinError 10054)됐고 `google.com` 은 정상이었다.
  이러면 yt-dlp 가 메타데이터 조회조차 못 해 **로컬 모드가 영구히 불가**하고 모든 영상이 브릿지로 간다
  = 전부 과금된다. 새 PC에서 비용이 이상하게 많이 나오면 이걸 먼저 의심한다:
  ```powershell
  python -c "import urllib.request; print(urllib.request.urlopen('https://www.youtube.com/',timeout=15).status)"
  ```

---

## 7. 유지보수 메모 (다음 사람에게)

- `scripts\bridge_engine.py` 는 원본 `transcript_bridge_v1_5.py` **v1.5 의 복사본에 CLI 를 덧붙인 것**이다.
  덧붙인 부분: `capture_cli`, `build_parser`, `main`, `bridge_frame_filename`,
  `build_bridge_manifest`, 상단 `watchlib` import.
  원본이 v1.6 등으로 올라가면 새 원본을 복사한 뒤 위 CLI 부분을 다시 이식해야 한다.
  현재 기준 버전은 `config.json` 의 `bridge_source_version` 에 적혀 있다 (= `1.5`).
- **2026-09-17 로컬 수정분이 있다.** v1.5 원본에는 없는 내용이므로, 원본을 새로 복사해 오면
  이것도 다시 옮겨 붙여야 한다. 수정 직전 상태는 `bridge_engine.py.bak-260917-pre-nogemini` 에 있다.
  수정한 곳은 전부 `capture_cli` 와 `build_parser` 안이다:

  | 변경 | 내용 |
  |---|---|
  | Gemini 실패 = 치명적 아님 | 기존엔 `return EXIT_API` 로 죽었다. 이제 경고만 찍고 **균등 그리드 모드로 내려간다** |
  | `--no-gemini` 플래그 추가 | 처음부터 Gemini 를 부르지 않는다 (쿼터 소진·키 없음 대비) |
  | Gemini 키 필수 조건 완화 | `--no-gemini` 일 때는 Gemini 키가 없어도 실행된다 |
  | 길이 추정 실패 시 중단 | 자막·Gemini 둘 다 없으면 그리드가 0~3초만 생긴다. **유료 호출 전에 멈춘다** |
  | `analysis.json` 조건부 저장 | 그리드 모드에서는 쓰지 않는다 |
  | `api_calls.gemini` | 그리드 모드면 `0` 으로 기록 |

  같은 날 `SKILL.md` 에도 그리드 모드 설명과 `degraded: ["gemini"]` 해석 규칙을 추가했다.
- **원본 v1.5 파일과 배포 폴더는 이 PC에서 이미 사라졌다.** 지금은 스킬 폴더 안의
  `bridge_engine.py` 가 사실상 원본이다. 새 PC에서는 이 파일을 직접 편집해도 된다
  (덮어쓸 `deploy.py` 가 없으므로). **다만 편집 전 백업을 뜬다.**
- 외부 의존 서비스 4곳:
  ```
  https://youtube-transcript.ai/transcript                        자막
  https://generativelanguage.googleapis.com/v1beta/interactions   Gemini
  https://api.yepapi.com/v1/youtube/screenshot                    프레임
  https://api.yepapi.com/v1/scrape/screenshot                     프레임(웹)
  ```
  이 중 하나라도 스펙이 바뀌면 브릿지가 깨진다. 깨졌을 때 먼저 볼 곳이다.

---

## 8. 체크리스트

**구 PC에서**
- [ ] 1단계 명령으로 평문 API 키 2개 회수 → 안전한 곳에 보관
- [ ] `~\.claude\skills\claude-watch-kr\` 폴더 통째로 백업 (USB / 클라우드)
- [ ] (선택) 블로그 결과 폴더 `_raw\` 들도 함께 백업 — 재추출하면 비용이 다시 든다

**새 PC에서**
- [ ] Python 3.10+ 설치 확인 (`python --version`)
- [ ] 스킬 폴더를 `C:\Users\<계정>\.claude\skills\claude-watch-kr\` 에 복원
- [ ] `config.json` 의 `blog_root` 수정
- [ ] `bridge_engine.py` GUI 실행 → Settings 에 키 2개 입력 → "키 기억하기" 체크 → 저장
- [ ] 4-2 `--dry-run` 검증 (`DRYRUN` 출력 확인)
- [ ] 4-2b `--no-gemini --dry-run` 검증 (그리드 폴백이 살아 있는지, 호출 0회)
- [ ] 유튜브 직통 확인 (6항 마지막 명령) — 막혀 있으면 **모든 영상이 유료 브릿지로 간다**
- [ ] 4-3 실제 1회 실행 (`READY` 출력 확인)
- [ ] Claude Code 에서 `/claude-watch-kr <유튜브 링크>` 동작 확인
