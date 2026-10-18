# Der falsche Koffer – 바뀐 여행가방
### CEFR 기반 통합형 독일어 교재 (A1 → B2) · 코지 미스터리

라이프치히 중앙역에서 한국인 유학생 **박민준**의 여행가방이 낯선 노신사의 가방과 바뀝니다.
가방 속 1989년 흑백 사진과 „Für E.“라고 적힌 편지 – 이 작은 사건이 **44개 챕터에 걸쳐** 같은 건물 사람들의 30년 넘은 비밀로 이어집니다.

- **두 주인공**: 🎓 민준(대학 유학 준비) · 👨‍👩‍👧‍👦 이수진(두 아이를 둔 이민 가정의 간호사) – 각자 다른 단서를 쥐고 있음
- **언어 현실성**: 한국인끼리는 한국어로 대화하고, 그 내용을 독일인에게 독일어로 전하는 **중개하기(Sprachmittlung)** 과제로 연결
- **추리 = 문법 진도**: 묻기(A1) → 주인 찾기 *Wem gehört …?*(A2) → 과거 재구성(B1) → 문서·증언 전하기 *Konjunktiv I*(B2)
- 대상: **대학 유학 준비생**과 **아이를 둔 이민 가정**의 성인 학습자

문법 · 말하기 · 쓰기 · 읽기 · 듣기를 매 챕터 안에서 함께 다룹니다.

**수업 형태**: 주 3회 × 100분(1교시 50분 + 2교시 50분) · 차시당 숙제 60분 · 전체 243차시, 약 18.7개월

| 폴더 / 파일 | 내용 |
|---|---|
| [`curriculum/00_교재_설계_개요.md`](curriculum/00_교재_설계_개요.md) | 콘셉트, 언어 현실성 원칙, 등장인물, 사건 전개(시즌별), 수업 회차, 챕터 구성 틀 |
| [`curriculum/01_A1_챕터구성.md`](curriculum/01_A1_챕터구성.md) | A1 · 1–8과 핵심 학습 내용 (2개월) |
| [`curriculum/02_A2_챕터구성.md`](curriculum/02_A2_챕터구성.md) | A2 · 9–20과 핵심 학습 내용 (약 4.4개월) |
| [`curriculum/03_B1_챕터구성.md`](curriculum/03_B1_챕터구성.md) | B1 · 21–32과 핵심 학습 내용 (약 5.5개월) |
| [`curriculum/04_B2_챕터구성.md`](curriculum/04_B2_챕터구성.md) | B2 · 33–44과 핵심 학습 내용 (약 6.7개월) |
| [`web/index.html`](web/index.html) | **HTML 교재 목차** (웹앱 원형) |
| [`web/cover-a1.html`](web/cover-a1.html) · [`web/dist/cover-a1.pdf`](web/dist/cover-a1.pdf) | **A1 표지 – 미니멀** (A4 인쇄용, SODA 로고 포함) |
| [`web/cover-a1-illustrated.html`](web/cover-a1-illustrated.html) · [`web/dist/cover-a1-illustrated.pdf`](web/dist/cover-a1-illustrated.pdf) | A1 표지 – 삽화형 (이전 안) |
| [`web/A1/kapitel-01.html`](web/A1/kapitel-01.html) | **1과 HTML 교재** – 자동 채점, 음성 듣기, 차시별 보기, 사건 수첩 저장 |
| [`A1/Kapitel_01_Hallo_ich_bin_Minjun.md`](A1/Kapitel_01_Hallo_ich_bin_Minjun.md) | **1과 시범 원고 (학생용)** |
| [`A1/Kapitel_01_Loesungen_Lehrerhandbuch.md`](A1/Kapitel_01_Loesungen_Lehrerhandbuch.md) | 1과 정답 · 수업 운영안 · 첨삭 가이드 (교사용) |

## 기존 방식과 무엇이 달라지나

| 기존 | 새 교재 |
|---|---|
| 문법만 2개월 → 이후 A2에서 4기능 | A1 첫 시간부터 문법 + 4기능 통합 |
| 문법 규칙 → 예문 → 연습 | 이야기 속 장면 → 문법 **발견** → 규칙 정리 → 말하기·쓰기에 바로 사용 |
| 과마다 따로 떨어진 주제 | 한 인물의 정착 과정이 이어짐 → 다음 과가 궁금해지는 구조 |
| 시험 대비는 마지막에 따로 | 레벨마다 마지막 과에서 Goethe 시험(Start Deutsch 1, A2, B1, B2) 형식 연습 |

## HTML 교재 구조 (웹앱 전환 대비)

> 1과는 **HTML이 원본**입니다. `A1/Kapitel_01_*.md`(원고·교사용 별책)는 초기 초안이며, 최신 내용(초보자용 재설계)은 HTML에 있습니다. 교사 모드는 삭제했으며, 교사용 운영안·첨삭 기준은 Markdown 교사용 별책(초안)을 참고하세요.

```
web/
├── index.html                 목차
├── assets/css/textbook.css    공통 스타일 (색은 :root 토큰, 다크 모드·인쇄 지원)
├── assets/js/textbook.js      공통 기능 (채점·음성·차시별 보기·ä ö ü ß 입력·저장)
└── A1/kapitel-01.html         챕터별 HTML
```

새 챕터는 `kapitel-01.html`을 복사해 내용만 바꾸면 됩니다. 기능은 모두 `data-` 속성으로 동작합니다.

| 속성 / 클래스 | 역할 |
|---|---|
| `.ex[data-check]` | 채점 가능한 연습 문제 (정답 확인 / 정답 보기 / 다시 하기 버튼 자동 생성) |
| `input.blank[data-answer="a\|b"]` | 빈칸 – `\|`로 여러 정답 허용, `data-ci` 대소문자 무시, `data-digits` 숫자만 비교 |
| `select[data-answer]`, `tr[data-answer="r"]` | 선택형 / richtig-falsch |
| `.dialog > .line > .who + .text[lang]` | 대화문 – 줄마다 ▶ 듣기 버튼 자동 생성 |
| `[data-play="대화 id"]` | 대화 전체 듣기 (원어민 녹음 전까지 브라우저 TTS 사용) |
| `[data-say]` | 단어·표현 듣기 버튼 |
| `.time[data-min]` | 활동 시간 표시 |
| `[data-persist]` | 학생 입력을 브라우저에 저장 (사건 수첩, 자기 점검) |
| `section[data-stunde]`, `[data-block="input\|output"]` | 차시·교시 구분 |
