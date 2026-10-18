# Der falsche Koffer · 작업 인계서

다른 채팅에서 이 교재를 이어 만들 때 **가장 먼저 읽는 문서**입니다.
기계가 읽기 좋은 같은 내용은 [`project-state.json`](project-state.json)에 있습니다.

> 새 채팅 첫 메시지 예시
> „sophiadeutschakademie/CFER 저장소의 `claude/cfer-german-textbook-qtcgcu` 브랜치에서 `handoff/HANDOFF.md`와 `handoff/project-state.json`을 읽고, 같은 형식으로 A1 3과를 만들어 줘.“

---

## 1. 무엇을 만들고 있나

- **교재**: CEFR A1→B2 통합형 독일어 교재 «Der falsche Koffer»(바뀐 여행가방). 한국인 학습자용, 코지 미스터리 이야기.
- **만드는 사람**: SODA(Sophia Deutsch Akademie) 독일어 학원 선생님. 학생에게 **최대한 쉽게** 설명하고 첨삭하는 것이 목표.
- **답변 언어**: 한국어(존댓말, 짧고 쉽게).
- **지금까지 완성**: 표지 → 목차 → **1과** → **2과**. 모두 `web/A1/kapitel-01.html` **한 파일** 안에 들어 있습니다.
- **배포용 파일**: `web/dist/kapitel-01.html`. CSS·JS·그림·녹음을 모두 넣은 단일 파일로, 약 7.8MB입니다.

## 2. 저장소와 브랜치

| 항목 | 값 |
|---|---|
| 저장소 | `sophiadeutschakademie/CFER` |
| 작업 브랜치 | `claude/cfer-german-textbook-qtcgcu` (여기에만 push, PR은 요청 있을 때만) |
| push | `git push -u origin claude/cfer-german-textbook-qtcgcu` |
| 커밋 메시지 | 한국어 요약 + 끝에 `Co-Authored-By` / `Claude-Session` 줄 (모델 이름은 넣지 않음) |

```
curriculum/            전체 설계(00 개요·인물, 01 A1 … 04 B2 챕터 구성)  ← 이야기·문법 계획의 원본
A1/*.md                1과 원고·해설(초기 문서)
tools/
  kapitel_lib.py       공용 HTML 생성 함수 (2과부터 사용)
  gen_k01.py           표지·목차·1과 생성 + 2과 조각을 이어 붙여 최종 파일을 씀
  gen_k02.py           2과 생성 → 조각(FRAG)과 상단 탭(NAV)만 만듦, id 앞에 k2-
  build-single.py      단일 파일 빌드: python3 tools/build-single.py A1/kapitel-01.html
  audio-k01-manifest.json  1과 녹음 목록(id, who, lang, text, voice)
  crop-sheet.py, draw-cards.py, draw-profile-cards.py  그림 자르기·글자 카드 그리기(Pillow)
web/
  A1/kapitel-01.html   ★ 최종 교재(표지+목차+1과+2과)
  dist/kapitel-01.html ★ 단일 파일 버전
  assets/css/textbook.css · js/textbook.js · icons/icons.svg
  assets/img/k01/ k02/ brand/   그림(webp)
  assets/audio/k01/             녹음(mp3, 127개) – 2과 녹음은 아직 없음
  index.html                    첫 화면(과 목록)
```

## 3. 다시 만드는 법 (생성 → 빌드 → 검사)

```bash
python3 tools/gen_k02.py                       # 2과를 만들고 gen_k01을 불러 최종 파일까지 다시 씀
# (1과만 고쳤으면 python3 tools/gen_k01.py 도 같음 – 내부에서 gen_k02를 import)
python3 tools/build-single.py A1/kapitel-01.html   # → web/dist/kapitel-01.html
```

**HTML을 손으로 고치지 말고 항상 생성기(`tools/gen_k0N.py`)를 고친 뒤 다시 생성합니다.**

검사는 Playwright로 합니다(Chromium 내장, `require('/opt/node22/lib/node_modules/playwright')`).
1. **채점 검사**: 모든 `.ex[data-check]`에서 `[data-act=show]`(정답 보기)를 누른 뒤 `.score`가 모두 '모두 정답'인지 봅니다. 지금은 129/129입니다.
2. **넘침 검사**: 폭 1440 · 1100 · 820 · 600 · 390 · 360에서 모든 탭(`contents, start, stunde-1..3, anhang, k2-start, k2-stunde-1..3, k2-anhang`)을 열고 확인합니다.
   - 상자 밖으로 나간 요소
   - 가로 스크롤이 생긴 `.table-wrap`
   - 텍스트 넘침
3. **나머지**: 스크립트 오류 0, 깨진 그림 0, 중복 id 0, 중복 라디오 name 0.
4. **눈으로 확인**: 스크린샷을 찍어 직접 봅니다.

## 4. 선생님이 정한 형식 규칙 (반드시 지킬 것)

**레이아웃**
- 지면을 넓게 씁니다(`--maxw:1240px`). 빈칸으로 구역을 분명히 나눕니다. 글씨는 크게(`html{font-size:19px}`), 문장 사이 간격은 넓게 합니다.
- **모두 세로 정렬**: 문제, 오늘의 문장 틀, 목표, 이번 주 수업(3차시), 가방 속 물건 카드, 문법 목록.
- 내용이 칸을 벗어나면 안 됩니다. 6가지 폭에서 모두 확인합니다.

**수업 구성**
- 한 과 = 3차시(1주). 한 차시 = **1교시 50분 Input + 2교시 50분 Output**. 활동 시간(분)의 합이 각각 정확히 50이어야 합니다.
- 차시마다 **숙제 60분, 문제 7개**(H1–H7). 행 시간의 합이 60입니다.
- **짝 활동·모둠 활동은 없습니다.** 말하기는 혼자 소리 내기나 녹음으로 합니다.
- 문제는 **너무 쉽지 않게, 많이** 냅니다. 고르기만 하지 말고 빈칸 쓰기, 문장 전체 쓰기, 틀린 문장 고치기를 섞습니다.

**내용**
- **문법이 쓰이는 곳마다 문법 상자**(`gram()`)를 넣습니다. 목표 페이지에는 '이번 과에서 배우는 문법' 목록을 둡니다.
- **한글 발음 표기(음차)는 쓰지 않습니다.**
- '이 교재 사용법', 교사 모드 상자는 없습니다(`tnote()`는 빈 문자열).
- 관사 색: der 파랑 `g-m`, die 빨강 `g-f`, das 초록 `g-n`, 복수 die 갈색 `g-p`.

**그림**
- ElevenLabs `recraft-v4.1-flash`로 **SODA 그림체**로 만듭니다(7절).
- 글자가 들어가는 그림(명함, 프로필 카드, 숫자, 가격표)은 **Pillow로 직접** 그립니다.

**녹음**
- ElevenLabs **eleven_v4**를 쓰고, 인물마다 **목소리를 고정**합니다(8절).
- **Minjun은 남자이고, 영어식 'Min-joon'으로 읽습니다.** 독일어 문장 안에서는 `/ˈmɪndʒuːn/`처럼 IPA로 적고, 브라우저 음성(TTS)은 `Mindschuun`으로 바꿔 읽습니다.

## 5. 페이지 구조 (한 파일에 여러 과)

- **`data-panel`**: 이 값이 같은 요소들이 한 화면(탭)입니다. 화면 순서는 다음과 같습니다.
  - `cover`: 표지(`data-nav="off"`)
  - `contents`: 목차
  - 1과: `start`(목표), `stunde-1`, `stunde-2`, `stunde-3`, `anhang`
  - 2과: `k2-start`, `k2-stunde-1`, `k2-stunde-2`, `k2-stunde-3`, `k2-anhang`
- **2과의 id 접두사**: 2과 안의 모든 `id`, `href="#…"`, `data-tab`, `data-panel`, `data-play`, `data-ex`, 라디오 `name` 앞에 `k2-`가 붙습니다(`gen_k02.py`의 `_prefix`). SVG 아이콘 `#i-…`는 예외입니다. **3과는 `k3-`** 로 합니다.
- **상단 탭**: `<span class="tabs" data-ch="1">`와 `data-ch="2"` 묶음이 있고, 지금 보는 과의 묶음만 보입니다(CSS `body[data-current^="k2-"]`). 각 탭의 `data-label="2과 1차시"`는 화면 끝 이전/다음 버튼의 이름이 됩니다.
- **목차**: 링크는 `href="#k2-kapitel-2" data-tab="k2-start"` 형식입니다.
- **1과 부록 끝**: '다음 과' 문구가 `#k2-kapitel-2`로 연결됩니다.
- **body 속성**: `data-chapter="A1-01"`, `data-level="A1"`.

## 6. 생성 함수 (tools/kapitel_lib.py)

| 함수 | 쓰임 |
|---|---|
| `act(id, no, title, minutes, body, block="input"|"output")` | 활동 카드. **번호는 자동으로 다시 매김**. 본문의 `9a, 9b`처럼 `{no}[a-h]`도 새 번호로 바뀜. no=""면 번호 없음(복습·마무리) |
| `block("1교시 · 50분 · Input")` | 교시 머리말 |
| `stunde(id, no, title, plan, body)` / `homework(id, title, rows[(할 일, 분)], extra)` | 차시 / 숙제 상자 |
| `ex(id, tag, head, body, check=True)` | 채점되는 문제 묶음 (`data-check`) |
| `blank(ans, label, cls="", ci=False, digits=False)` | 빈칸. 답 여러 개는 `"a|b"`. `cls="wide"`/`"full"` |
| `sel(ans, opts)` · `rf(name, rows[(문장, "r"/"f", 뜻)], lang)` | 고르기 · 맞다/틀리다 표 |
| `gram(title, body)` | 문법 상자 |
| `today(items[(de, "", ko)], title, paired)` | 오늘의 문장 틀 (세로, ▶ 듣기) |
| `dialog(id, rows, cls, lang)` · `line(who, de, ko, lang)` · `stage(t)` · `track(no, id, text)` | 대화. `who`가 `AV`에 있으면 얼굴 그림 표시 |
| `fig(name, alt, cap)` · `pic(name, alt, cls)` · `ic(icon)` · `g(word, "m/f/n/p")` | 장면 그림 · 작은 그림 · 아이콘 · 관사 색 |
| `K.IMG = "../assets/img/k03/"` | 과마다 그림 폴더. 이름에 `/`가 있으면 `assets/img/` 기준(예 `k01/person-minjun`) |

자주 쓰는 클래스는 다음과 같습니다.
- `.koffer-items` + `.kitem`: 그림 | 단어 ▶ | 뜻 세로 카드
- `.vocab`: 단어 격자
- `.say-grid.numbers`: 숫자 듣기 격자
- `.cast` / `.cast.cast-big`: 인물
- `.box.tip`, `.box.mystery`: 팁 상자, 사건 상자
- `.template`: 틀 문장
- `.muted`: 작은 설명
- `.table-wrap > table`, `tr.hl`(강조 줄)
- `details.transcript`: 대본 숨기기
- `textarea[data-persist]`: 이 기기에 자동 저장

`data-` 동작은 다음과 같습니다.
- `[data-say]`: 브라우저 음성
- `[data-audio]`: 녹음 파일
- `[data-play="dlg-id"]`: 대화 전체를 이어서 재생(다시 누르면 멈춤)
- `span.lis[data-say]`: 듣기 문제 ▶
- `[data-persist]`: 입력 저장

## 7. 그림 만들기 (SODA 그림체)

- **도구와 flow**: ElevenLabs `creative_generate_image`(모델 `recraft-v4.1-flash`, 1장 약 48.5크레딧). 이 교재는 flow **`UJBSwwDvHHFi9ZMS0yED`** 를 썼습니다.
- **프롬프트**: 영어 한 문장 + 고정 문장입니다.
  - 고정 문장: `Modern minimalist editorial illustration, calm and refined, simplified geometric forms, flat matte colors with a very fine subtle grain, restrained palette of deep navy, slate gray, warm sand and ivory with one muted ochre accent, natural muted skin tones, minimal facial features, soft subtle shadows. Plain white background, wordless.`
  - 장면 앞: `The whole scene sits fully inside the frame, centered, with even generous white margins on all four sides.`
  - 여러 개 한 장 앞: `Every item is complete, separated from the others by wide empty white space, and does not touch the edges of the image.`
- **결과 받기**: `creative_get_flow_run_status`로 `content_url`을 받아 curl로 내려받습니다. 결과가 너무 크면 파일로 저장되니 JSON을 읽어 처리합니다.
- **자르기**:
  - 장면: 잉크 영역에 여백 30px을 두고 자른 뒤 가로 1280 이하, webp q80.
  - 한 장에 5개: 위쪽 88% 높이에서 세로 열의 잉크 합으로 경계를 찾습니다. 붙어 있으면 잉크가 가장 적은 열에서 나눕니다.
  - 인물은 높이 560, 사물은 높이 300, webp.
  - 인물은 잉크 기준(밝기 200 미만)으로 위를 꼭 붙여 자릅니다. 위가 비면 대화 얼굴 그림(아바타)이 하얗게 보입니다.
- **파일 이름**: `story-1-…`, `person-이름`, `moebel-…`, `ding-…`, `karte-…`, `steckbrief-…`, `stimmung-1…5`. 언더바는 쓰지 않습니다.
- **검수**: 미리보기 시트로 직접 확인합니다(손가락, 겹침, 그림 속 글자). 이상하면 한 번만 다시 생성합니다.

## 8. 녹음 만들기 (eleven_v4)

- **도구**: `creative_generate_speech`(모델 eleven_v4, generations_count 1).
- **필요하면 태그**: `[slowly]`, `[coldly]` 등을 씁니다. 슐체 할머니는 차갑게 합니다.
- **정규화**: `ffmpeg -af loudnorm=I=-18:TP=-1.5:LRA=11 -ac 1 -b:a 64k`.
- **파일 이름**: `web/assets/audio/kNN/`에 저장합니다. 이름만 맞으면 생성기가 `data-audio`를 자동으로 연결합니다.
  - 대화: `{dialog-id}-{줄 번호}.mp3`. 대화 안 `<span class="text">` 순서이고, 무대 지시(stage)는 세지 않습니다.
  - 듣기 문제: `lis-{n}.mp3`. 그 과 안의 `span.lis` 순서입니다.
- **목록 관리**: `tools/audio-kNN-manifest.json`에 `{id, who, lang, text, voice}`로 적어 둡니다.
- **인물별 고정 목소리**(voice_id)는 `project-state.json`의 `voices`에 있습니다. 같은 인물은 언제나 같은 목소리입니다. 새 인물만 `creative_list_voices`에서 골라 추가합니다.

## 9. 새 과(예: 3과) 추가 순서

1. `curriculum/01_A1_챕터구성.md`의 해당 과(이야기·문법·말하기·쓰기·중개하기·문화)와 `00_교재_설계_개요.md`의 인물표를 읽습니다.
2. `tools/gen_k03.py`를 `gen_k02.py` 구조대로 만듭니다.
   - `K.IMG="../assets/img/k03/"`
   - `K.AV.update(...)`
   - 3차시 = 6교시
   - 부록: 핵심 문장 10, 문법 한눈에, Landeskunde, Wortschatz, 3컷, 민준의 일기, Fallakte(`data-persist="fall3-…"`), 자기 점검(라디오 `data-persist="k3sc…"`)
   - 끝에 `P="k3-"`인 `_prefix`, `FRAG`, `NAV`
3. `gen_k01.py`를 고칩니다.
   - `import gen_k03 as K3`
   - nav에 `{K3.NAV}` 추가
   - main에 `{K3.FRAG}` 추가
   - 목차 `toc_items`의 i==3을 `#k3-kapitel-3` / `data-tab="k3-start"`로
   - 2과 부록의 '다음 과'를 링크로
4. CSS에서 탭 숨김 규칙을 3과까지 넓힙니다.
   - `body[data-current^="k3-"] .tabs:not([data-ch="3"])` 숨김
   - `data-ch="3"`은 `k3-`일 때만 보이게
5. 그림과 녹음을 만들고, `index.html`·README의 과 목록을 고칩니다.
6. 생성 → 빌드 → 3절의 검사(채점·넘침·오류) → 커밋·push → 단일 파일 전달.

## 10. 이야기 진행 상황 (다음 과에서 이어 쓸 것)

- **1과**
  - 9월 말, 민준이 라이프치히 중앙역에서 가방이 바뀝니다.
  - 가방 안: 낡은 회색 외투, 흑백 사진(남녀 두 사람, 촛불), 편지 „Für E.“, 약, 이름표 **T. S.**, 전화 040(함부르크).
  - WG: Kochstraße 12, Jonas(라이프치히), Lena(함부르크, „Moin!“).
  - 어학원: Frau Wagner, Carlos, Tomasz, Priya.
  - 계단에서 수진과 하은을 만납니다. 1층 Frau Schulze는 웃지 않습니다.
- **2과**
  - 민준 방에는 탁자도 의자도 없습니다. 저녁에 Jonas·Lena와 가방을 살펴보고 „Wir sind Detektive!“라고 합니다.
  - 수진의 통합 과정 첫날: Herr Brandt, Amira(시리아), Oksana(우크라이나). „Ich habe 38“ 실수가 나옵니다.
  - 하은이 Kita에서 가족을 통역합니다.
  - 저녁에 수진 집(독일식 2. Stock)에서 **도윤(3세)이 편지 봉투를 탁자 밑으로 가져가 크레용으로 그림을 그립니다. 아무도 모릅니다.** 민준의 일기는 „Der Brief ist weg!“로 끝납니다.
  - 정답(편지의 행방)은 A2 9과에서 공개합니다.
- **3과 예고**(2과 일기에 이미 씀)
  - 민준과 Lena의 첫 장보기. 외투 주머니에서 나온 영수증이 새 단서가 됩니다.
  - 수진과 태호의 첫 대형 마트, 태호의 Gift(독) 착각도 들어갑니다.
  - 문법: 4격, möchten, 가격.

## 11. 남은 일

- [ ] 2과 녹음(eleven_v4)
  - 대화: dlg-2-01 … 2-06, 2-03 Lena 영상 통화
  - 듣기: 숫자 lis 5개
  - 일기: diary-2
  - 새 목소리: Herr Brandt, Amira, Oksana, 태호, 도윤
- [ ] 3과 «Im Supermarkt» (`k3-`)
- [ ] 다시 생성하면 좋은 그림: 2과 인물 5명은 발끝이 잘려 있음, `moebel-schreibtisch`는 모양이 단순함
