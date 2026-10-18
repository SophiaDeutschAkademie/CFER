# 1과 HTML 생성 (초보자용 재설계)
import re, html
OUT = "/home/user/CFER/web/A1/kapitel-01.html"
IMG = "../assets/img/k01/"
SPRITE = open("/home/user/CFER/web/assets/icons/icons.svg", encoding="utf-8").read()
keep_navy = {"i-123", "i-mediate", "i-abc"}
def _rc(m):
    sym = m.group(0); sid = re.search(r'id="([^"]+)"', sym).group(1)
    return sym if sid in keep_navy else sym.replace("#2E3A55", "currentColor")
SPRITE = re.sub(r"<symbol.*?</symbol>", _rc, SPRITE, flags=re.S)
SPRITE = re.sub(r"<!--.*?-->", "", SPRITE).replace('style="display:none">', 'style="display:none" aria-hidden="true">').strip()

def ic(n): return f'<svg class="ic" aria-hidden="true"><use href="#i-{n}"/></svg>'
def pic(n, alt="", cls="pic"): return f'<img class="{cls}" src="{IMG}{n}.webp" alt="{alt}" loading="lazy">'
def fig(n, alt, cap=""): return f'<figure class="scene"><img src="{IMG}{n}.webp" alt="{alt}" loading="lazy">' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def g(x, c): return f'<b class="g-{c}">{x}</b>'
AV = {"Minjun": "minjun", "민준": "minjun", "Jonas": "jonas", "Lena": "lena", "Frau Wagner": "wagner", "Carlos": "carlos",
      "Tomasz": "tomasz", "Priya": "priya", "수진": "sujin", "하은": "haeun", "Frau Schulze": "schulze"}

def line(who, de, ko="", lang="de"):
    av = f'<span class="avatar" style="background-image:url({IMG}person-{AV[who]}.webp)" aria-hidden="true"></span>' if who in AV else ""
    k = f'<span class="ko">{ko}</span>' if ko else ""
    la = f' lang="{lang}"' if lang else ""
    return f'      <div class="line"><span class="who">{av}{who}</span><span class="tx"><span class="text"{la}>{de}</span>{k}</span></div>'
def stage(t): return f'      <p class="stage">({t})</p>'
def dialog(id_, rows, cls="dialog", lang=None):
    la = f' lang="{lang}"' if lang else ""
    return f'    <div class="{cls}" id="{id_}"{la}>\n' + "\n".join(rows) + "\n    </div>"
def track(no, id_, text):
    return f'    <p><span class="track">{ic("listen")}Track {no} <button type="button" class="say-btn" data-play="{id_}" aria-label="대화 전체 듣기">▶</button></span> {text}</p>'
def tnote(t): return ''   # 교사 모드 삭제: 교사용 상자는 만들지 않음
ACT_NO = [0]
def act(id_, no, title, minutes, body, block="input"):
    # 활동 번호는 순서대로 다시 매기고, 본문 속 하위 번호(5a, 5c …)도 함께 바꾼다
    if no != "":
        ACT_NO[0] += 1
        new = ACT_NO[0]
        if isinstance(no, int) and no != new:
            body = re.sub(rf"\b{no}([a-h])\b", rf"{new}\1", body)
        no = new
    num = f"{no} · " if no else ""
    return f'''  <section class="activity card" id="{id_}" data-block="{block}">
    <h3>{num}{title} <span class="time" data-min="{minutes}">{ic("timer")}{minutes}분</span></h3>
{body}
  </section>
'''
def sel(ans, opts, label="고르기"):
    o = "".join(f"<option>{x}</option>" for x in opts)
    return f'<select data-answer="{ans}" aria-label="{label}"><option value=""></option>{o}</select>'
def blank(ans, label="빈칸", cls="", ci=False, digits=False):
    extra = (" data-ci" if ci else "") + (" data-digits" if digits else "")
    c = "blank" + (" " + cls if cls else "")
    return f'<input class="{c}"{extra} data-answer="{ans}" aria-label="{label}">'
def ex(id_, tag, head, body, check=True):
    c = " data-check" if check else ""
    return f'''    <div class="ex"{c} data-ex="{id_}">
      <div class="ex-head"><span class="tag">{tag}</span>{head}</div>
{body}
    </div>'''
def rf(name, rows, lang="de"):
    out = []
    for i, (de, ans, ko) in enumerate(rows, 1):
        k = f' <small>({ko})</small>' if ko else ""
        out.append(f'<tr data-answer="{ans}"><td>{i}</td><td><span lang="{lang}">{de}</span>{k}</td>'
                   f'<td class="c"><input type="radio" name="{name}-{i}" value="r" aria-label="richtig"></td>'
                   f'<td class="c"><input type="radio" name="{name}-{i}" value="f" aria-label="falsch"></td></tr>')
    return ('      <div class="table-wrap"><table class="rf"><thead><tr><th>#</th><th>문장</th><th class="c">r</th><th class="c">f</th></tr></thead><tbody>\n        '
            + "\n        ".join(out) + "\n      </tbody></table></div>")
def gram(title, body):
    return f'''    <aside class="gram">
      <p class="gram-title">{ic("book")}{title}</p>
{body}
    </aside>'''
def slots(*parts):
    out = []
    for p in parts:
        cls = "slot"
        for k, c in (("V:", " v"), ("S:", " subj"), ("0:", " zero")):
            if p.startswith(k): cls += c; p = p[2:]
        out.append(f'<span class="{cls}">{p}</span>')
    return '      <div class="slots" lang="de">' + "".join(out) + "</div>"
def today(items, title="오늘의 문장 틀", paired=False):
    cs = "".join(f'<div class="chunk"><b lang="de" data-say>{de}</b><span class="ko">{ko}</span></div>' for de, p, ko in items)
    return f'''    <div class="today">
      <p class="today-title">{ic("speak")}{title} – 먼저 듣고 세 번 따라 말하기</p>
      <div class="chunks chunks-v{' paired' if paired else ''}">{cs}</div>
    </div>'''
def homework(id_, title, rows, extra=""):
    r = "".join(f"<tr><td>{i}</td><td>{a}</td><td>{b}분</td></tr>" for i, (a, b) in enumerate(rows, 1))
    return f'''  <section class="box homework" id="{id_}">
    <p class="box-title">{ic("home")}{title}</p>
    <div class="table-wrap"><table><thead><tr><th>#</th><th>할 일</th><th>시간</th></tr></thead><tbody>{r}</tbody></table></div>
{extra}
  </section>
'''
def stunde(id_, no, title, plan, body):
    return f'''<section id="{id_}" class="stunde" data-stunde="{no}" data-panel="{id_}">
  <div class="stunde-head"><span class="stunde-no">{no}차시</span><h2 lang="de">{title}</h2></div>
{tnote('<p class="box-title">' + ic("teacher") + no + '차시 운영안</p>' + plan)}
{body}
</section>
'''
def block(t): return f'  <div class="block-head">▶ {t}</div>\n'

# =====================================================================
# 1차시 · Hallo! Ich bin Minjun.
# =====================================================================
greet = [("아침", "Guten Morgen!", "구텐 모르겐", "좋은 아침이에요"),
         ("낮", "Guten Tag!", "구텐 탁", "안녕하세요"),
         ("저녁", "Guten Abend!", "구텐 아벤트", "좋은 저녁이에요"),
         ("언제나 · 친구", "Hallo!", "할로", "안녕!"),
         ("헤어질 때 · 친구", "Tschüss!", "취스", "안녕! (작별)"),
         ("헤어질 때 · 어른", "Auf Wiedersehen!", "아우프 비더제엔", "안녕히 계세요/가세요"),
         ("고마울 때", "Danke!", "당케", "고마워요"),
         ("미안할 때", "Entschuldigung!", "엔트슐디궁", "죄송합니다 / 실례합니다")]
greetcards = "".join(f'<div class="card-word"><span class="when">{w}</span><b lang="de" data-say>{de}</b><span class="ko">{ko}</span></div>' for w, de, p, ko in greet)
gopts = ["Guten Morgen!", "Guten Tag!", "Guten Abend!", "Tschüss!", "Auf Wiedersehen!"]
vopts = ["bin", "bist", "heiße", "heißt"]
vopts2 = ["Bin", "Bist", "Heiße", "Heißt"]
gsit = ["아침 · 선생님과", "친구끼리 만남", "저녁 · 이웃과", "친구와 헤어짐", "선생님과 헤어짐"]
kopts = ["Noch einmal, bitte.", "Langsam, bitte.", "Ich verstehe das nicht.", "Was heißt „Mantel“?", "Wie schreibt man das?"]
iopts = ["들으세요.", "읽으세요.", "쓰세요.", "채우세요.", "표시하세요."]
aopts = ["Kein Problem.", "Gut, danke.", "Ja, ich bin Minjun.", "Danke!"]

s1 = block("1교시 · 50분 · Input")
s1 += act("s1-einstieg", 1, "Einstieg · 그림으로 시작해요", 5, f'''    {fig("story-1-bahnhof", "붐비는 라이프치히 중앙역에서 젊은 한국 남자와 회색 외투의 노신사가 부딪치고, 똑같은 검은 가방 두 개가 바닥에 놓여 있다", "라이프치히 중앙역. 캐리어를 든 젊은 남자는 <b>민준</b>, 한국에서 막 도착했어요.")}
    <p><b>1a</b> 그림을 보고 한국어로 이야기해 보세요. 가방 두 개가 똑같네요. <b>무슨 일이 생길까요?</b></p>
    <p><b>1b</b> 이번 과가 끝나면 이런 말을 할 수 있어요. 들어 보세요!</p>
    <p class="box" lang="de" data-say>Hallo! Ich heiße Minjun. Ich komme aus Südkorea. Ich wohne in Leipzig.</p>
    <p class="ko">안녕하세요! 제 이름은 민준이에요. 한국에서 왔어요. 라이프치히에 살아요.</p>
{tnote("독일어를 처음 듣는 시간입니다. 1b는 해석을 보여 주고 “3시간 뒤면 여러분도 이 말을 해요”라고 목표를 보여 주세요.")}''')

s1 += act("s1-hallo", 2, "Hallo! · 첫 독일어 인사", 10, f'''    <p>카드를 눌러 듣고, 소리 내어 <b>세 번씩</b> 따라 하세요.</p>
    <div class="cards cards-4">{greetcards}</div>
    <div class="box tip">{ic("tip")}▶를 눌러 <b>소리를 먼저</b> 듣고 따라 하세요. 글자보다 소리가 먼저예요!</div>
{gram("인사는 ‘언제’와 ‘누구에게’에 따라 달라요", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th>친구 · 가족 · 아이 <small>(du)</small></th><th>어른 · 처음 보는 사람 · 직원 <small>(Sie)</small></th></tr></thead>
        <tbody lang="de">
          <tr><th lang="ko">만날 때</th><td>Hallo! · Hi!</td><td>Guten Morgen! <small lang="ko">(~10시)</small> · Guten Tag! <small lang="ko">(낮)</small> · Guten Abend! <small lang="ko">(저녁)</small></td></tr>
          <tr><th lang="ko">헤어질 때</th><td>Tschüss! · Bis morgen!</td><td>Auf Wiedersehen!</td></tr>
        </tbody>
      </table></div>
      <p><b lang="de">Guten Tag!</b>는 낮 동안 언제나 쓸 수 있는 가장 무난한 인사예요. 헷갈리면 이것! <b lang="de">Gute Nacht!</b>(잘 자)는 자러 갈 때만 써요.</p>""")}
{ex("A0", "A1", "누구에게, 언제? 알맞은 인사를 고르세요.", f"""      <ol>
        <li>아침 8시, 어학원 선생님께 → {sel("Guten Morgen!", gopts)}</li>
        <li>오후 2시, 관청 직원에게 → {sel("Guten Tag!", gopts)}</li>
        <li>저녁 7시, 이웃 할머니께 → {sel("Guten Abend!", gopts)}</li>
        <li>친구와 헤어질 때 → {sel("Tschüss!", gopts)}</li>
        <li>선생님과 헤어질 때 → {sel("Auf Wiedersehen!", gopts)}</li>
        <li>밤 9시, 호텔 직원에게 처음 → {sel("Guten Abend!", gopts)}</li>
        <li>아침 7시, 빵집 주인에게 → {sel("Guten Morgen!", gopts)}</li>
        <li>점심때, 은행 직원에게 → {sel("Guten Tag!", gopts)}</li>
      </ol>""")}
{ex("A0b", "A1b", "이럴 때 뭐라고 할까요? 보기 없이 <b>직접 쓰세요</b>.", f"""      <ol>
        <li>누가 문을 잡아 줬어요. → <span lang="de">{blank("Danke!|Danke", "말")}</span></li>
        <li>지하철에서 다른 사람의 발을 밟았어요. → <span lang="de">{blank("Entschuldigung!|Entschuldigung", "말", "wide")}</span></li>
        <li>저녁 8시, 처음 보는 이웃을 만났어요. → <span lang="de">{blank("Guten Abend!|Guten Abend", "말", "wide")}</span></li>
        <li>면접이 끝나고 면접관에게 → <span lang="de">{blank("Auf Wiedersehen!|Auf Wiedersehen", "말", "wide")}</span></li>
        <li>누가 “Entschuldigung!” 하고 사과했어요. → <span lang="de">{blank("Kein Problem.|Kein Problem", "말", "wide")}</span></li>
      </ol>""")}''')

s1 += act("s1-gruss-hoeren", 3, "<span lang=\"de\">Hören</span> · 누가 누구에게 인사해요?", 10, f'''    <p>짧은 대화 다섯 개예요. 각 번호의 ▶를 눌러 듣고 문제를 푸세요. 대본은 다 푼 뒤에!</p>
{ex("GH1", "3a", "어떤 상황일까요? 고르세요.", f"""      <ol>
        <li><button type="button" class="say-btn" data-play="dlg-g1" aria-label="대화 1 듣기">▶</button> {sel("아침 · 선생님과", gsit)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-g2" aria-label="대화 2 듣기">▶</button> {sel("친구끼리 만남", gsit)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-g3" aria-label="대화 3 듣기">▶</button> {sel("저녁 · 이웃과", gsit)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-g4" aria-label="대화 4 듣기">▶</button> {sel("친구와 헤어짐", gsit)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-g5" aria-label="대화 5 듣기">▶</button> {sel("선생님과 헤어짐", gsit)}</li>
      </ol>""")}
{ex("GH2", "3b", "다시 듣고 빈칸을 쓰세요.", f"""      <ol lang="de">
        <li>Guten {blank("Morgen", "말")}, Frau Wagner!</li>
        <li>Hi, Jonas! Wie {blank("geht's|gehts", "말")}?</li>
        <li>Guten {blank("Abend", "말")}, Frau Schulze.</li>
        <li>Tschüss! Bis {blank("morgen", "말", ci=True)}!</li>
        <li>Auf {blank("Wiedersehen", "말")}, Frau Wagner!</li>
      </ol>""")}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-g1", [line("Minjun", "Guten Morgen, Frau Wagner!", "안녕하세요(아침), 바그너 선생님!"), line("Frau Wagner", "Guten Morgen, Minjun!", "좋은 아침이에요, 민준!")])}
{dialog("dlg-g2", [line("Jonas", "Hallo, Lena!", "안녕, 레나!"), line("Lena", "Hi, Jonas! Wie geht's?", "안녕, 요나스! 잘 지내?"), line("Jonas", "Gut, danke!", "좋아, 고마워!")])}
{dialog("dlg-g3", [line("Minjun", "Guten Abend, Frau Schulze.", "안녕하세요(저녁), 슐체 할머니."), line("Frau Schulze", "… Guten Abend.", "…안녕하세요.")])}
{dialog("dlg-g4", [line("Minjun", "Tschüss, Carlos!", "안녕, 카를로스!"), line("Carlos", "Tschüss! Bis morgen!", "안녕! 내일 봐!")])}
{dialog("dlg-g5", [line("Minjun", "Auf Wiedersehen, Frau Wagner!", "안녕히 계세요, 바그너 선생님!"), line("Frau Wagner", "Auf Wiedersehen!", "안녕히 가세요!")])}
    </details>
    <p class="muted">새 표현: <span lang="de">Bis morgen!</span> = 내일 봐! · <span lang="de">Hi!</span> = 안녕! (아주 친한 사이)</p>''')

s1 += act("s1-teil-a", 3, "Teil A · <span lang=\"de\">Am Bahnhof</span> · 역에서", 15, f'''{track("1-01", "dlg-1-01", "기차에서 내린 민준. 누군가 기다리고 있어요.")}
{dialog("dlg-1-01", [
    stage("쿵! 민준이 검은 가방을 든 노신사와 부딪친다."),
    line("Mann", "Oh! Entschuldigung!", "앗! 죄송합니다!"),
    line("Minjun", "Kein Problem.", "괜찮아요."),
    stage("두 사람이 서둘러 가방을 집어 든다."),
    line("Jonas", "Hallo! Bist du Minjun?", "안녕! 네가 민준이야?"),
    line("Minjun", "Ja, ich bin Minjun. Und du?", "응, 내가 민준이야. 너는?"),
    line("Jonas", "Ich bin Jonas. Willkommen in Leipzig!", "나는 요나스야. 라이프치히에 온 걸 환영해!"),
    line("Minjun", "Danke!", "고마워!"),
    line("Jonas", "Wie geht's?", "잘 지내? (어때?)"),
    line("Minjun", "Gut, danke. Ein bisschen müde.", "좋아, 고마워. 조금 피곤해.")])}
{ex("A1", "A2", "대화를 다시 듣고, 맞으면 <b>r</b>(richtig), 틀리면 <b>f</b>(falsch). 해석 없이 풀어 보세요!", rf("a1", [
    ("Der Mann sagt: „Danke!“", "f", ""),
    ("Minjun sagt zum Mann: „Kein Problem.“", "r", ""),
    ("Jonas fragt: „Wie heißt du?“", "f", ""),
    ("Jonas wartet am Bahnhof.", "r", "warten = 기다리다"),
    ("Minjun ist sehr gut.", "f", "sehr = 아주"),
    ("Minjun ist ein bisschen müde.", "r", "")]))}
{ex("A1c", "A3", "대화에 알맞은 대답을 고르세요.", f"""      <ol lang="de">
        <li>Entschuldigung! – {sel("Kein Problem.", aopts)}</li>
        <li>Wie geht's? – {sel("Gut, danke.", aopts)}</li>
        <li>Bist du Minjun? – {sel("Ja, ich bin Minjun.", aopts)}</li>
        <li>Willkommen in Leipzig! – {sel("Danke!", aopts)}</li>
      </ol>""")}
    <p><b>A4</b> 혼자 소리 내어 읽기 · ▶로 한 줄씩 듣고 <b>민준 역할</b>을 따라 하세요. 두 번째는 Minjun 대신 <b>내 이름</b>을 넣어서!</p>''')

s1 += act("s1-satz1", 4, "오늘의 문장 틀 ① · 나는 ○○이에요", 10, f'''{today([
    ("Ich bin Minjun.", "이히 빈 민준", "나는 민준이야."),
    ("Ich heiße Minjun.", "이히 하이세 민준", "내 이름은 민준이야."),
    ("Wie heißt du?", "비 하이스트 두", "너는 이름이 뭐야?"),
    ("Bist du Jonas?", "비스트 두 요나스", "네가 요나스야?")])}
{gram("나(ich)와 너(du) – 동사 모양이 달라요", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th lang="de">sein <small lang="ko">(~이다)</small></th><th lang="de">heißen <small lang="ko">(이름이 ~이다)</small></th></tr></thead>
        <tbody lang="de">
          <tr><th>ich <small lang="ko">나</small></th><td>Ich <b>bin</b> Minjun.</td><td>Ich <b>heiße</b> Minjun.</td></tr>
          <tr><th>du <small lang="ko">너</small></th><td><b>Bist</b> du Jonas?</td><td>Wie <b>heißt</b> du?</td></tr>
        </tbody>
      </table></div>
      <p><span lang="de">Ich bin Minjun.</span> = <span lang="de">Ich heiße Minjun.</span> 둘 중 <b>하나만</b> 쓰세요. <span lang="de"><s>Ich bin heiße Minjun.</s></span> ✗</p>
      <p>질문할 때 동사를 <b>맨 앞</b>에: <span lang="de"><b>Bist</b> du Jonas?</span> (네가 요나스야?)</p>""")}
{ex("G1", "G1", "알맞은 말을 고르세요. (<i lang=\"de\">oder?</i> = 그렇지?)", f"""      <ol lang="de">
        <li>Ich {sel("bin", vopts)} Minjun.</li>
        <li>{sel("Bist", vopts2)} du Jonas?</li>
        <li>Wie {sel("heißt", vopts)} du?</li>
        <li>Ich {sel("heiße", vopts)} Lena.</li>
        <li>{sel("Heißt", vopts2)} du Jonas?</li>
        <li>Du {sel("bist", vopts)} Lena, oder?</li>
      </ol>""")}
{ex("G1b", "G1b", "한국어를 보고 빈칸을 채우세요.", f"""      <ol>
        <li>나는 민준이야. → <span lang="de">Ich {blank("bin", "동사")} Minjun.</span></li>
        <li>네가 레나야? → <span lang="de">{blank("Bist", "동사")} du Lena?</span></li>
        <li>내 이름은 요나스야. → <span lang="de">Ich {blank("heiße", "동사")} Jonas.</span></li>
        <li>너는 이름이 뭐야? → <span lang="de">{blank("Wie", "의문사")} heißt du?</span></li>
        <li>나는 레나야. 너는? → <span lang="de">Ich bin Lena. {blank("Und", "말")} du?</span></li>
      </ol>""")}''')

alph1 = [("A", "a", "아"), ("B", "be", "베"), ("C", "tse", "체"), ("D", "de", "데"), ("E", "e", "에"), ("F", "ef", "에프"), ("G", "ge", "게"),
         ("H", "ha", "하"), ("I", "i", "이"), ("J", "jot", "요트"), ("K", "ka", "카"), ("L", "el", "엘"), ("M", "em", "엠")]
alph2 = [("N", "en", "엔"), ("O", "o", "오"), ("P", "pe", "페"), ("Q", "ku", "쿠"), ("R", "er", "에어"), ("S", "es", "에스"), ("T", "te", "테"),
         ("U", "u", "우"), ("V", "fau", "파우"), ("W", "we", "베"), ("X", "iks", "익스"), ("Y", "üpsilon", "윕실론"), ("Z", "tset", "체트")]
alph3 = [("Ä", "a Umlaut", "애"), ("Ö", "o Umlaut", "외"), ("Ü", "u Umlaut", "위"), ("ß", "eszett", "에스체트")]
eopts = ["ei", "ie", "eu"]
def acells(r): return "".join(f'<div class="say-cell" data-say="{n}"><b>{L}</b></div>' for L, n, p in r)
sounds = [("w", "[v]", "Wie, wohnen", "윗니로 아랫입술을 살짝 물고 ‘ㅂ’"), ("z", "[ts]", "zwei, zehn", "짧은 ‘츠’"), ("j", "[j]", "ja, Jonas", "‘야, 요’"),
          ("v", "[f]", "Vater, vier", "‘ㅍ’에 가까운 f 소리"), ("ei", "[ai]", "heißen, drei", "‘아이’"), ("ie", "[iː]", "Wie, vier", "길게 ‘이—’"),
          ("eu", "[ɔy]", "Leute, neun", "‘오이’"), ("sch", "[ʃ]", "Tschüss, Schulze", "‘슈’"), ("ä · ö · ü", "", "Mädchen, schön, müde", "‘애 · 외 · 위’ – 입술 모양 주의")]
srows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td lang="de" data-say>{c}</td><td>{d}</td></tr>' for a, b, c, d in sounds)

s1 += block("2교시 · 50분 · Output")
s1 += act("s1-alphabet", 5, "<span lang=\"de\">Das Alphabet</span> · 소리와 글자", 15, f'''    <p><b>5a</b> 글자를 눌러 들어 보세요. 독일어는 <b>글자대로 읽는</b> 언어예요. 이 소리들만 알면 처음 보는 단어도 읽을 수 있어요!</p>
    <div class="say-grid alphabet" lang="de">{acells(alph1 + alph2 + alph3)}</div>
    <p><b>5b</b> 한국어·영어와 <b>다르게</b> 읽는 글자 – 이것만 조심하세요!</p>
    <div class="table-wrap"><table><thead><tr><th>글자</th><th>소리</th><th>예</th><th>요령</th></tr></thead><tbody>{srows}</tbody></table></div>
{ex("5c", "5c", "ei 일까요, ie 일까요? 듣고 고르세요.", f"""      <p lang="de">dr{sel("ei", ["ei", "ie"])} · v{sel("ie", ["ei", "ie"])}r · h{sel("ei", ["ei", "ie"])}ßen · W{sel("ie", ["ei", "ie"])} · S{sel("ie", ["ei", "ie"])} · fr{sel("ei", ["ei", "ie"])}</p>""")}
{ex("5d", "5d", "ei · ie · eu 중 무엇일까요? ▶로 듣고 고르세요.", f"""      <ol lang="de">
        <li><span class="lis" data-say="sieben"></span> → s{sel("ie", eopts)}ben</li>
        <li><span class="lis" data-say="neun"></span> → n{sel("eu", eopts)}n</li>
        <li><span class="lis" data-say="zwei"></span> → zw{sel("ei", eopts)}</li>
        <li><span class="lis" data-say="Leute"></span> → L{sel("eu", eopts)}te</li>
        <li><span class="lis" data-say="Leipzig"></span> → L{sel("ei", eopts)}pzig</li>
        <li><span class="lis" data-say="wie"></span> → w{sel("ie", eopts)}</li>
      </ol>""")}
{ex("5e", "5e", "철자를 듣고 단어를 쓰세요. (▶를 누르세요)", f"""      <ol lang="de">
        <li><span class="lis" data-say="B, E, R, L, I, N."></span> {blank("Berlin", "단어 1", ci=True)}</li>
        <li><span class="lis" data-say="L, E, N, A."></span> {blank("Lena", "단어 2", ci=True)}</li>
        <li><span class="lis" data-say="K, O, F, F, E, R."></span> {blank("Koffer", "단어 3", ci=True)}</li>
        <li><span class="lis" data-say="P, A, R, K."></span> {blank("Park", "단어 4", ci=True)}</li>
        <li><span class="lis" data-say="J, O, N, A, S."></span> {blank("Jonas", "단어 5", ci=True)}</li>
        <li><span class="lis" data-say="W, A, G, N, E, R."></span> {blank("Wagner", "단어 6", ci=True)}</li>
      </ol>""")}
{tnote("5c 대본: drei, vier, heißen, Wie, Sie, frei – 천천히 두 번씩 읽어 주세요.")}''', "output")

s1 += act("s1-buchstabieren", 6, "<span lang=\"de\">Buchstabieren</span> · 이름 철자 말하기", 15, f'''{today([
    ("Wie bitte?", "비 비테", "뭐라고요?"),
    ("Wie schreibt man das?", "비 슈라입트 만 다스", "그건 어떻게 써요?")], "철자를 물을 때")}
{gram("이름을 말하는 세 가지 방법", f"""      <div class="slots-list" lang="de">
        <p><b>Ich heiße</b> Minjun. <span class="muted" lang="ko">– 가장 많이 써요</span></p>
        <p><b>Ich bin</b> Minjun. <span class="muted" lang="ko">– 짧고 편하게</span></p>
        <p><b>Mein Name ist</b> Minjun Park. <span class="muted" lang="ko">– 조금 격식 있게 (전화·창구)</span></p>
      </div>
      <p><span lang="de">Wie schreibt <b>man</b> das?</span>의 <b lang="de">man</b>은 ‘사람들이 (일반적으로)’라는 뜻이에요. „그건 어떻게 써요?“를 통째로 외우세요.</p>""")}
{ex("12a", "6a", f"{ic('listen')}Track 1-05 · 이름을 듣고 쓰세요.", f"""      <ol lang="de">
        <li>{blank("Wagner", "이름 1", "wide", ci=True)}</li>
        <li>{blank("Becker", "이름 2", "wide", ci=True)}</li>
        <li>{blank("Jeong", "이름 3", "wide", ci=True)}</li>
        <li>{blank("Schulze", "이름 4", "wide", ci=True)}</li>
      </ol>
      <details class="transcript"><summary>대본 보기 (듣기가 끝난 뒤에!)</summary>
{dialog("dlg-1-05", [
    '      <div class="line"><span class="who">1</span><span class="tx"><span class="text" lang="de" data-say="Wagner. W, A, G, N, E, R.">Wagner. W – A – G – N – E – R.</span></span></div>',
    '      <div class="line"><span class="who">2</span><span class="tx"><span class="text" lang="de" data-say="Becker. B, E, C, K, E, R.">Becker. B – E – C – K – E – R.</span></span></div>',
    '      <div class="line"><span class="who">3</span><span class="tx"><span class="text" lang="de" data-say="Jeong. J, E, O, N, G.">Jeong. J – E – O – N – G.</span></span></div>',
    '      <div class="line"><span class="who">4</span><span class="tx"><span class="text" lang="de" data-say="Schulze. S, C, H, U, L, Z, E.">Schulze. S – C – H – U – L – Z – E.</span></span></div>'])}
        <button type="button" class="btn ghost" data-play="dlg-1-05">▶ 전체 듣기</button>
      </details>""")}
    <p><b>6b</b> 아래 대화를 보고, B 자리에 <b>내 이름</b>을 넣어 혼자 소리 내어 말하세요. 철자는 한 글자씩 또박또박!</p>
{dialog("dlg-12b", [line("A", "Wie heißt du?", "이름이 뭐야?"), line("B", "Ich heiße Seoyeon Kim.", "내 이름은 김서연이야."),
                    line("A", "Wie bitte? Wie schreibt man das?", "뭐라고? 어떻게 써?"), line("B", "S – E – O – Y – E – O – N.", "")])}
{ex("6e", "6c", "명함과 이름표를 읽고 쓰세요. <b lang=\"de\">Vorname</b> = 이름 · <b lang=\"de\">Nachname</b> = 성", f"""      <div class="namecards">
        <figure>{pic("karte-wagner", "명함: Sprachschule Leipzig, Petra Wagner, Lehrerin · Deutsch, Tel. 0341 / 12 15 19, Raum 3 · Kurs A1", "card-img")}</figure>
        <figure>{pic("karte-becker", "명함: Jonas Becker, Student · Informatik, Kochstraße 12 · 04275 Leipzig, Mobil 0170 / 12 8 15", "card-img")}</figure>
        <figure>{pic("karte-park", "이름표: Hallo, ich bin Minjun Park, Südkorea · Kurs A1, Sprachschule Leipzig", "card-img")}</figure>
      </div>
      <ol>
        <li>바그너 선생님의 <span lang="de">Vorname</span> → <span lang="de">{blank("Petra", "Vorname")}</span></li>
        <li>요나스의 <span lang="de">Nachname</span> → <span lang="de">{blank("Becker", "Nachname")}</span></li>
        <li>민준의 <span lang="de">Nachname</span> → <span lang="de">{blank("Park", "Nachname")}</span></li>
        <li>요나스는 무엇을 공부해요? → <span lang="de">{blank("Informatik", "전공")}</span></li>
        <li>바그너 선생님의 수업은 어디에서? → <span lang="de">Raum {blank("3|drei", "번호")}</span></li>
        <li>요나스의 휴대폰 번호 → <span lang="de">{blank("0170 12 8 15", "번호", "wide", digits=True)}</span></li>
        <li>내 한국 이름(예: 김서연)을 독일식으로 쓰면? <span lang="de">Vorname</span> → <span lang="de">{blank("Seoyeon", "Vorname")}</span>, <span lang="de">Nachname</span> → <span lang="de">{blank("Kim", "Nachname")}</span></li>
      </ol>""")}
    <div class="box tip">{ic("tip")}한국 이름은 <b>성이 먼저</b>, 독일 이름은 <b>이름이 먼저</b>예요. 김서연 → <span lang="de">Seoyeon Kim</span>. 서류에는 <span lang="de">Nachname</span>과 <span lang="de">Vorname</span>을 따로 써요.</div>
    <div class="box warn">{ic("warn")}영어와 헷갈려요: <b>J</b> = <i lang="de">jot</i>, <b>V</b> = <i lang="de">fau</i>, <b>W</b> = <i lang="de">we</i>, <b>Z</b> = <i lang="de">tset</i>, <b>E</b> = <i lang="de">e</i>(에), <b>I</b> = <i lang="de">i</i>(이)</div>
{tnote("2번 Becker는 Jonas의 성, 4번 Schulze는 3차시에 등장하는 1층 이웃입니다. 아무 말도 하지 말고 이름만 들려주세요.")}''', "output")

s1 += act("s1-kurs", 7, "<span lang=\"de\">Im Kurs</span> · 수업 시간에 쓰는 독일어", 10, f'''{today([
    ("Noch einmal, bitte.", "", "한 번 더 말해 주세요."),
    ("Langsam, bitte.", "", "천천히 말해 주세요."),
    ("Ich verstehe das nicht.", "", "이해가 안 돼요."),
    ("Was heißt „Koffer“?", "", "„Koffer“가 무슨 뜻이에요?")], "수업 중에 꼭 쓰는 말")}
{ex("K1", "7a", "이럴 때 뭐라고 할까요?", f"""      <ol>
        <li>선생님 말이 너무 빨라요. → {sel("Langsam, bitte.", kopts)}</li>
        <li>못 들었어요. 다시 듣고 싶어요. → {sel("Noch einmal, bitte.", kopts)}</li>
        <li>„Mantel“이 무슨 뜻인지 몰라요. → {sel("Was heißt „Mantel“?", kopts)}</li>
        <li>설명을 들었지만 모르겠어요. → {sel("Ich verstehe das nicht.", kopts)}</li>
        <li>이름 철자를 알고 싶어요. → {sel("Wie schreibt man das?", kopts)}</li>
      </ol>""")}
    <p><b>7b</b> 교재와 시험에 나오는 지시문이에요. 듣고 따라 하세요.</p>
    <div class="vocab" lang="de">{"".join(f'<div><b data-say>{d}</b><span class="ko" lang="ko">{k}</span></div>' for d, k in [("Hören Sie.", "들으세요."), ("Lesen Sie.", "읽으세요."), ("Schreiben Sie.", "쓰세요."), ("Sprechen Sie.", "말하세요."), ("Ergänzen Sie.", "채우세요."), ("Kreuzen Sie an.", "표시하세요.")])}</div>
{gram("Hören Sie. – 지시하는 말은 동사가 맨 앞", f"""      <p lang="de">Sie hören. <span class="muted" lang="ko">당신은 들어요. (설명)</span></p>
      <p lang="de"><b>Hören</b> Sie? <span class="muted" lang="ko">들으세요? (질문)</span></p>
      <p lang="de"><b>Hören</b> Sie. / <b>Hören</b> Sie! <span class="muted" lang="ko">들으세요. (지시·부탁)</span></p>
      <p>존댓말 지시는 <b>동사 + Sie</b>. 모양은 질문과 같지만 끝에 <b>마침표나 느낌표</b>가 와요. 시험지 지시문이 모두 이 모양이에요.</p>""")}
{ex("K2", "7c", "지시문의 뜻을 고르세요.", f"""      <ol lang="de">
        <li>Schreiben Sie. → {sel("쓰세요.", iopts)}</li>
        <li>Hören Sie. → {sel("들으세요.", iopts)}</li>
        <li>Ergänzen Sie. → {sel("채우세요.", iopts)}</li>
        <li>Kreuzen Sie an. → {sel("표시하세요.", iopts)}</li>
        <li>Lesen Sie. → {sel("읽으세요.", iopts)}</li>
      </ol>""")}''', "output")

s1 += act("s1-sprechen", 7, "<span lang=\"de\">Sprechen</span> · 첫 만남 대화", 10, f'''{track("1-06", "dlg-7", "어학원 첫날, Lena가 복도에서 Priya를 만나요.")}
{dialog("dlg-7", [line("Lena", "Hallo! Ich bin Lena.", "안녕! 나는 레나야."), line("Priya", "Hallo! Ich heiße Priya.", "안녕! 내 이름은 프리야야."),
                  line("Lena", "Wie geht's?", "잘 지내?"), line("Priya", "Gut, danke! Und dir?", "좋아, 고마워! 너는?"),
                  line("Lena", "Auch gut. Tschüss!", "나도 좋아. 안녕!")])}
{ex("7a", "7a", "대화를 보지 말고 빈칸을 채우세요.", f"""      <div class="dialog" lang="de">
        <div class="line"><span class="who">A</span><span class="tx"><span>Hallo! Ich {blank("bin|heiße", "동사")} Lena.</span></span></div>
        <div class="line"><span class="who">B</span><span class="tx"><span>Hallo! Ich {blank("heiße|bin", "동사")} Priya.</span></span></div>
        <div class="line"><span class="who">A</span><span class="tx"><span>Wie {blank("geht's|gehts|geht es", "말")}?</span></span></div>
        <div class="line"><span class="who">B</span><span class="tx"><span>Gut, {blank("danke", "말")}! Und {blank("dir", "말")}?</span></span></div>
        <div class="line"><span class="who">A</span><span class="tx"><span>{blank("Auch", "말")} gut. {blank("Tschüss", "인사")}!</span></span></div>
      </div>""")}
    <p><b>7b</b> 혼자 말하기 · ▶로 A 줄만 듣고, 멈춘 뒤 B를 <b>내 이름</b>으로 소리 내어 대답하세요. 휴대폰으로 녹음해서 들어 보면 더 좋아요!</p>
{tnote("발표 중에는 오류를 메모만 하고, 끝난 뒤 한꺼번에 피드백하세요. <i lang='de'>Auch gut</i>(나도 좋아)는 덩어리로만 알려 주세요.")}''', "output")

s1 += homework("hw-1", "1차시 숙제 (60분)", [
    ("인사말 카드 8개 + Teil A 대화 듣고 따라 하기 – <b>소리 내어</b> 3번씩", 10),
    ("<b>H1</b> 인사와 문장 쓰기", 10),
    ("<b>H1c · H1d</b> 철자 받아쓰기, 대화 완성", 15),
    ("<b>H1e · H1f · H1g</b> 상황 판단, 질문 만들기, 틀린 문장 고치기", 15),
    (ic("mic") + "<b>녹음</b>: “Hallo! Ich heiße … Wie heißt du?” + 내 이름 철자를 녹음해서 제출", 10)],
    ex("H1", "H1", "알맞은 인사나 말을 쓰세요.", f"""      <ol>
        <li>친구에게 처음 인사: <span lang="de">{blank("Hallo!|Hallo|Hi!|Hi", "인사")}</span></li>
        <li>“내 이름은 민준이야.” → <span lang="de">Ich {blank("heiße", "동사")} Minjun.</span></li>
        <li>“네가 요나스야?” → <span lang="de">{blank("Bist", "동사")} du Jonas?</span></li>
        <li>“너는 이름이 뭐야?” → <span lang="de">Wie {blank("heißt", "동사")} du?</span></li>
        <li>선생님과 헤어질 때: <span lang="de">{blank("Auf Wiedersehen!|Auf Wiedersehen", "인사", "wide")}</span></li>
        <li>고마울 때: <span lang="de">{blank("Danke!|Danke", "말")}</span></li>
        <li>“괜찮아요.” → <span lang="de">Kein {blank("Problem", "말")}.</span></li>
      </ol>""") + "\n" + ex("H1c", "H1c", "▶로 철자를 듣고 단어를 쓰세요. 도시와 이름이에요!", f"""      <ol lang="de">
        <li><span class="lis" data-say="H, A, M, B, U, R, G."></span> {blank("Hamburg", "단어", ci=True)}</li>
        <li><span class="lis" data-say="D, R, E, S, D, E, N."></span> {blank("Dresden", "단어", ci=True)}</li>
        <li><span class="lis" data-say="K, Ö, L, N."></span> {blank("Köln", "단어", ci=True)}</li>
        <li><span class="lis" data-say="S, E, O, U, L."></span> {blank("Seoul", "단어", ci=True)}</li>
        <li><span class="lis" data-say="P, E, T, R, A."></span> {blank("Petra", "단어", ci=True)}</li>
        <li><span class="lis" data-say="S, C, H, U, L, Z, E."></span> {blank("Schulze", "단어", ci=True)}</li>
        <li><span class="lis" data-say="M, Ü, N, C, H, E, N."></span> {blank("München", "단어", ci=True)}</li>
      </ol>""") + "\n" + ex("H1d", "H1d", "대화를 완성하세요. 보기 없이!", f"""      <div class="dialog" lang="de">
        <div class="line"><span class="who">Carlos</span><span class="tx"><span>Hallo! Ich {blank("bin|heiße", "동사")} Carlos. {blank("Wie", "의문사")} heißt du?</span></span></div>
        <div class="line"><span class="who">Priya</span><span class="tx"><span>Ich {blank("heiße|bin", "동사")} Priya.</span></span></div>
        <div class="line"><span class="who">Carlos</span><span class="tx"><span>Wie bitte? Wie {blank("schreibt", "동사")} man das?</span></span></div>
        <div class="line"><span class="who">Priya</span><span class="tx"><span>P – R – I – Y – A.</span></span></div>
        <div class="line"><span class="who">Carlos</span><span class="tx"><span>{blank("Danke", "말")}! Wie geht's?</span></span></div>
        <div class="line"><span class="who">Priya</span><span class="tx"><span>Gut, danke. Und {blank("dir", "말")}?</span></span></div>
        <div class="line"><span class="who">Carlos</span><span class="tx"><span>Auch gut. {blank("Tschüss", "인사")}!</span></span></div>
      </div>""") + "\n" + ex("H1e", "H1e", "알맞은 말이면 <b>r</b>, 어색하면 <b>f</b>", rf("h1e", [
    ("밤 10시, 이웃에게 처음: „Guten Morgen!“", "f", ""),
    ("오후 3시, 우체국 직원에게: „Guten Tag!“", "r", ""),
    ("교수님과 헤어질 때: „Tschüss, Professor!“", "f", ""),
    ("친구가 „Danke!“라고 했어요. 대답: „Entschuldigung!“", "f", ""),
    ("다른 사람과 부딪쳤어요: „Entschuldigung!“", "r", ""),
    ("„Wie geht's?“에 대한 대답: „Gut, danke.“", "r", "")], lang="ko")) + "\n" + ex("H1f", "H1f", "문장을 du 질문으로 바꾸세요. (동사를 맨 앞에!)", f"""      <ol lang="de">
        <li>Du bist Lena. → {blank("Bist du Lena?", "질문", "full")}</li>
        <li>Du heißt Jonas. → {blank("Heißt du Jonas?", "질문", "full")}</li>
        <li>Du bist müde. → {blank("Bist du müde?", "질문", "full")}</li>
        <li>Du heißt Minjun Park. → {blank("Heißt du Minjun Park?", "질문", "full")}</li>
      </ol>""") + "\n" + ex("H1g", "H1g", "틀린 곳을 고쳐 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Ich heißt Lena. → {blank("Ich heiße Lena.", "고친 문장", "full")}</li>
        <li>Du bin Jonas? → {blank("Bist du Jonas?", "고친 문장", "full")}</li>
        <li>Wie heiße du? → {blank("Wie heißt du?", "고친 문장", "full")}</li>
        <li>Ich bin heiße Carlos. → {blank("Ich heiße Carlos.|Ich bin Carlos.", "고친 문장", "full")}</li>
        <li>guten abend! → {blank("Guten Abend!", "고친 문장", "full")}</li>
      </ol>"""))

# =====================================================================
# 2차시 · Woher kommst du?
# =====================================================================
langs = [("Südkorea", "Koreanisch", "쥐트코레아", "한국 – 한국어"), ("Deutschland", "Deutsch", "도이칠란트", "독일 – 독일어"),
         ("Spanien", "Spanisch", "슈파니엔", "스페인 – 스페인어"), ("Polen", "Polnisch", "폴렌", "폴란드 – 폴란드어"),
         ("Indien", "Hindi", "인디엔", "인도 – 힌디어"), ("England", "Englisch", "엥글란트", "영국 – 영어")]
lcards = "".join(f'<div class="card-word"><b lang="de" data-say>{a}</b><span class="ko">{ko}</span><b lang="de" data-say style="margin-top:.35rem">{b}</b></div>' for a, b, p, ko in langs)
lopts = ["Koreanisch", "Deutsch", "Spanisch", "Polnisch", "Hindi"]
wopts = ["Woher", "Wo", "Wie"]
wopts2 = ["Aus", "In"]
wopts3 = ["aus", "in"]
more_countries = [("Japan", "Japanisch", "일본 – 일본어"), ("China", "Chinesisch", "중국 – 중국어"), ("Vietnam", "Vietnamesisch", "베트남 – 베트남어"),
                  ("die Türkei", "Türkisch", "튀르키예 – 튀르키예어"), ("die Ukraine", "Ukrainisch", "우크라이나 – 우크라이나어"), ("Brasilien", "Portugiesisch", "브라질 – 포르투갈어")]
hk_people = [("Ahmet", "Türkei", "Leipzig", "Türkisch"), ("Mei", "China", "Halle", "Chinesisch"), ("Olena", "Ukraine", "Leipzig", "Ukrainisch"), ("Lucas", "Brasilien", "Dresden", "Portugiesisch")]
hk_land = ["Türkei", "China", "Ukraine", "Brasilien"]
hk_ort = ["Leipzig", "Halle", "Dresden"]
hk_spr = ["Türkisch", "Chinesisch", "Ukrainisch", "Portugiesisch"]
qopts = ["Aus Spanien.", "In Leipzig.", "Ja, ein bisschen.", "Ich heiße Lena."]

s2 = block("1교시 · 50분 · Input")
s2 += act("s2-wiederholung", "", "복습", 5, '    <p><b>인사 릴레이</b>: 원으로 서서 „<span lang="de">Hallo! Ich heiße … Wie heißt du?</span>“를 차례로 이어 가기.</p>')
s2 += act("s2-teil-b", 8, "Teil B · <span lang=\"de\">In der WG</span> · 공유 주택에서", 10, f'''{track("1-02", "dlg-1-02", "WG에 도착하자 룸메이트 Lena가 부엌에서 나와요.")}
{dialog("dlg-1-02", [
    line("Lena", "Moin! Ich bin Lena.", "안녕! 나는 레나야. (Moin = 북독일 인사)"),
    line("Minjun", "Hallo, Lena! Ich heiße Minjun.", "안녕, 레나! 내 이름은 민준이야."),
    line("Lena", "Freut mich! Woher kommst du?", "반가워! 어디에서 왔어?"),
    line("Minjun", "Ich komme aus Südkorea. Und du?", "한국에서 왔어. 너는?"),
    line("Lena", "Ich komme aus Hamburg. Aber ich wohne jetzt hier in Leipzig.", "나는 함부르크에서 왔어. 그런데 지금은 여기 라이프치히에 살아."),
    line("Lena", "Sprichst du Deutsch?", "너 독일어 해?"),
    line("Minjun", "Ein bisschen. Ich spreche Koreanisch und Englisch.", "조금. 나는 한국어랑 영어를 해."),
    stage("민준이 가방을 연다. …잠깐."),
    line("Minjun", "Hä? Das ist nicht mein Koffer!", "어? 이거 내 가방이 아니야!"),
    line("Jonas", "Oh nein! Der Mann am Bahnhof!", "이런! 역에서 그 남자!")])}
    {fig("story-2-wg", "WG 부엌에서 민준이 검은 가방을 열고 놀라고, Jonas와 Lena가 들여다본다", "<span lang=\"de\">Das ist nicht mein Koffer!</span> – 가방 속에는 낯선 물건들이…")}
{gram("nicht – ‘아니다’ · mein – ‘나의’", f"""      <p lang="de">Das ist <b>mein</b> Koffer. <span class="muted" lang="ko">이건 내 가방이에요.</span></p>
      <p lang="de">Das ist <b class="g-f">nicht</b> <b>mein</b> Koffer. <span class="muted" lang="ko">이건 내 가방이 아니에요.</span></p>
      <p><b lang="de">nicht</b>는 부정하고 싶은 말 <b>바로 앞</b>에 놓아요. <span lang="de">mein</span>(나의) · <span lang="de">dein</span>(너의)는 2과에서 자세히 배워요.</p>""")}
{ex("B1", "B1", "대화를 듣고 고르세요.", f"""      <ol lang="de">
        <li>Minjun kommt aus {sel("Südkorea", ["Südkorea", "Hamburg", "Leipzig"])}.</li>
        <li>Lena kommt aus {sel("Hamburg", ["Südkorea", "Hamburg", "Leipzig"])}.</li>
        <li>Lena wohnt jetzt in {sel("Leipzig", ["Südkorea", "Hamburg", "Leipzig"])}.</li>
        <li>Minjun spricht {sel("Koreanisch und Englisch", ["Koreanisch und Englisch", "Deutsch und Spanisch"])}.</li>
      </ol>""")}
{ex("B1b", "B1b", "맞으면 <b>r</b>, 틀리면 <b>f</b>. 해석 없이!", rf("b1b", [
    ("Lena kommt aus Leipzig.", "f", ""),
    ("Minjun spricht sehr gut Deutsch.", "f", ""),
    ("Minjun spricht zwei Sprachen: Koreanisch und Englisch.", "r", "Sprachen = 언어들"),
    ("Lena und Minjun wohnen jetzt in Leipzig.", "r", ""),
    ("Das ist Minjuns Koffer.", "f", ""),
    ("Jonas denkt an den Mann am Bahnhof.", "r", "denken an = ~을 떠올리다")]))}
    <div class="box mystery">
      <p class="box-title">{ic("search")}Im Koffer · 가방 속에는…</p>
      <div class="koffer-items">
        <figure class="kitem">{pic("ding-mantel", "낡은 회색 외투", "kitem-img")}<figcaption><span class="kword" lang="de" data-say="der Mantel">{g("der", "m")} Mantel</span><span class="ko">외투</span></figcaption></figure>
        <figure class="kitem">{pic("ding-foto", "촛불을 든 두 사람의 흑백 사진", "kitem-img")}<figcaption><span class="kword" lang="de" data-say="das Foto">{g("das", "n")} Foto</span><span class="ko">사진 · 촛불을 든 두 사람</span></figcaption></figure>
        <figure class="kitem">{pic("ding-brief", "봉투", "kitem-img")}<figcaption><span class="kword" lang="de" data-say="der Brief">{g("der", "m")} Brief</span><span class="ko">편지 · 봉투에 „Für E.“</span></figcaption></figure>
        <figure class="kitem">{pic("ding-tabletten", "약병", "kitem-img")}<figcaption><span class="kword" lang="de" data-say="die Tabletten">{g("die", "p")} Tabletten</span><span class="ko">약</span></figcaption></figure>
        <figure class="kitem">{pic("ding-anhaenger", "가방 이름표", "kitem-img")}<figcaption><span class="kword" lang="de" data-say="der Kofferanhänger">{g("der", "m")} Kofferanhänger</span><span class="ko">가방 이름표 · <b>T. S.</b></span></figcaption></figure>
      </div>
      <p class="muted koffer-note">단어 앞의 <b class="g-m">der</b> · <b class="g-n">das</b> · <b class="g-p">die</b>는 2과에서 배워요. 지금은 색깔만 봐 두세요!</p>
      <p class="koffer-q"><b>B2</b> 가방의 주인은 누구일까요? 한국어로 한 줄 추리!</p>
      <textarea data-persist="b3" rows="2" placeholder="나의 추리…" aria-label="B2 나의 추리"></textarea>
{tnote("정답 없음. 학생들의 추리를 교실 벽 ‘사건 게시판’에 붙여 두고 과마다 갱신하세요. <b>스포일러(교사만)</b>: T. S. = Thomas Schulze(함부르크), E. = Erika Schulze(1층 이웃, 여동생). 사라질 편지는 2과에서 도윤이 가져가고, A2 9과에서 하은이 밝힙니다.")}
    </div>''')

s2 += act("s2-laender", 9, "나라와 언어", 10, f'''    <p>카드를 눌러 듣고 따라 하세요. <b>나라 → 언어</b> 한 쌍으로!</p>
    <div class="cards cards-3">{lcards}</div>
    <div class="box tip">{ic("tip")}나라와 언어 이름은 항상 <b>대문자</b>로 시작해요: <span lang="de">Koreanisch</span> ✓ · <span lang="de"><s>koreanisch</s></span> ✗</div>
{gram("나라에서 왔어요, 언어를 해요", f"""      <div class="table-wrap"><table>
        <tbody lang="de">
          <tr><th lang="ko">출신</th><td>Ich komme <b>aus</b> Polen.</td><td lang="ko">aus + 나라</td></tr>
          <tr><th lang="ko">언어</th><td>Ich spreche Polni<b>sch</b>.</td><td lang="ko">관사 없이 · 언어는 대부분 <b>-isch</b>로 끝나요</td></tr>
          <tr><th lang="ko">예외</th><td>aus <b>der</b> Türkei · aus <b>der</b> Ukraine · aus <b>den</b> USA</td><td lang="ko">관사가 붙는 나라 – 통째로!</td></tr>
        </tbody>
      </table></div>
      <p>나라·언어 이름은 <b>대문자</b>로 시작해요. <span lang="de">Deutsch</span>(독일어)는 <span lang="de">-isch</span>가 아닌 특별한 모양이에요.</p>""")}
{ex("B3", "B3", "문장을 완성하세요. 나라나 언어를 쓰세요.", f"""      <ol lang="de">
        <li>Ich komme aus Polen. Ich spreche {blank("Polnisch", "언어")}.</li>
        <li>Ich komme aus {blank("Spanien", "나라")}. Ich spreche Spanisch.</li>
        <li>Ich komme aus Deutschland. Ich spreche {blank("Deutsch", "언어")}.</li>
        <li>Ich komme aus {blank("Südkorea|Korea", "나라")}. Ich spreche Koreanisch.</li>
        <li>Ich komme aus Indien. Ich spreche Hindi und {blank("Englisch", "언어")}.</li>
      </ol>""")}
{ex("B3b", "B3b", "나라와 언어를 쓰세요. 대문자로 시작!", f"""      <ol lang="de">
        <li>스페인 → {blank("Spanien", "나라")}</li>
        <li>한국 → {blank("Südkorea|Korea", "나라")}</li>
        <li>독일어 → {blank("Deutsch", "언어")}</li>
        <li>영어 → {blank("Englisch", "언어")}</li>
        <li>폴란드어 → {blank("Polnisch", "언어")}</li>
      </ol>""")}''')

s2 += act("s2-herkunft", 10, "<span lang=\"de\">Hören</span> · 어학원 친구들은 어디에서 왔을까?", 10, f'''    <p>어학원 다른 반 학생 네 명이 자기소개를 해요. ▶로 한 사람씩 듣고 알맞은 것을 고르세요.</p>
    <div class="vocab" lang="de">{"".join(f'<div><b data-say>{a}</b><span class="ko" lang="ko">{k}</span><b data-say style="margin-top:.3rem">{b}</b></div>' for a, b, k in more_countries)}</div>
    <div class="box tip">{ic("tip")}몇몇 나라는 앞에 <b lang="de">der</b>가 붙어요: <span lang="de">aus <b>der</b> Türkei</span>, <span lang="de">aus <b>der</b> Ukraine</span>. 그냥 덩어리로 외우세요!</div>
{ex("HK1", "10a", "누가 어디에서 왔고, 어디에 살고, 무슨 말을 할까요?", f"""      <ol class="hk-list" lang="de">
        {"".join(f'<li><p class="hk-who"><button type="button" class="say-btn" data-play="dlg-h{i}" aria-label="{n} 듣기">▶</button> <b>{n}</b></p><p><span>Land <small lang="ko">나라</small></span>{sel(l, hk_land)}</p><p><span>Wohnort <small lang="ko">사는 곳</small></span>{sel(w, hk_ort)}</p><p><span>Sprache <small lang="ko">모국어</small></span>{sel(sp, hk_spr)}</p></li>' for i, (n, l, w, sp) in enumerate(hk_people, 1))}
      </ol>""")}
{ex("HK2", "10b", "다시 듣고, 맞으면 <b>r</b>, 틀리면 <b>f</b>", rf("hk2", [
    ("Mei spricht Chinesisch und Englisch.", "r", ""),
    ("Lucas spricht zwei Sprachen.", "f", ""),
    ("Olena sagt: „Mein Name ist Olena.“", "r", "Mein Name ist … = 제 이름은 …예요"),
    ("Ahmet spricht sehr gut Deutsch.", "f", "")]))}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-h1", [line("Ahmet", "Hallo! Ich heiße Ahmet. Ich komme aus der Türkei, aus Izmir. Ich wohne in Leipzig. Ich spreche Türkisch und ein bisschen Deutsch.", "안녕하세요! 아흐메트예요. 튀르키예 이즈미르에서 왔어요. 라이프치히에 살아요. 튀르키예어를 하고 독일어를 조금 해요.")])}
{dialog("dlg-h2", [line("Mei", "Hi, ich bin Mei. Ich komme aus China. Ich wohne jetzt in Halle. Ich spreche Chinesisch und Englisch.", "안녕, 나는 메이야. 중국에서 왔어. 지금 할레에 살아. 중국어와 영어를 해.")])}
{dialog("dlg-h3", [line("Olena", "Guten Tag! Mein Name ist Olena. Ich komme aus der Ukraine, aus Kyjiw. Ich wohne in Leipzig. Ich spreche Ukrainisch und Russisch.", "안녕하세요! 제 이름은 올레나예요. 우크라이나 키이우에서 왔어요. 라이프치히에 살아요. 우크라이나어와 러시아어를 해요.")])}
{dialog("dlg-h4", [line("Lucas", "Hallo! Ich heiße Lucas. Ich komme aus Brasilien. Ich wohne in Dresden. Ich spreche Portugiesisch, Spanisch und Englisch.", "안녕하세요! 루카스예요. 브라질에서 왔어요. 드레스덴에 살아요. 포르투갈어, 스페인어, 영어를 해요.")])}
    </details>''')

s2 += act("s2-satz2", 10, "오늘의 문장 틀 ② · 어디에서? 어디에? 무슨 말?", 15, f'''{today([
    ("Woher kommst du?", "보헤어 콤스트 두", "너는 어디에서 왔어?"),
    ("Ich komme aus Südkorea.", "이히 코메 아우스 쥐트코레아", "나는 한국에서 왔어."),
    ("Wo wohnst du?", "보 본스트 두", "너는 어디에 살아?"),
    ("Ich wohne in Leipzig.", "이히 보네 인 라이프치히", "나는 라이프치히에 살아."),
    ("Sprichst du Deutsch?", "슈프리히스트 두 도이치", "너 독일어 해?"),
    ("Ich spreche Koreanisch.", "이히 슈프레헤 코레아니슈", "나는 한국어를 해.")], paired=True)}
{gram("ich는 -e, du는 -st", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th lang="de">kommen <small lang="ko">오다</small></th><th lang="de">wohnen <small lang="ko">살다</small></th><th lang="de">sprechen <small lang="ko">말하다</small></th></tr></thead>
        <tbody lang="de">
          <tr><th>ich</th><td>komm<b>e</b></td><td>wohn<b>e</b></td><td>sprech<b>e</b></td></tr>
          <tr><th>du</th><td>komm<b>st</b></td><td>wohn<b>st</b></td><td>spr<b>i</b>ch<b>st</b> {ic("warn")}</td></tr>
        </tbody>
      </table></div>
      <p>사전형 <span lang="de">komm<s>en</s></span>에서 <b>-en을 떼고</b> 어미를 붙여요. <span lang="de">sprechen</span>은 du에서 e가 <b>i</b>로 바뀌어요.</p>""")}
{gram("동사는 두 번째 자리!", f"""      <p>한국어는 동사가 <b>맨 끝</b>(“한국에서 <b>왔어요</b>”), 독일어는 <b>두 번째</b>예요.</p>
{slots("S:Ich", "V:komme", "aus Südkorea.")}
{slots("Woher", "V:kommst", "S:du?")}
      <p>예/아니요 질문은 동사가 <b>맨 앞</b>: </p>
{slots("V:Sprichst", "S:du", "Deutsch?")}
      <p><b lang="de">Woher?</b>(어디에서?) → <b lang="de">aus</b> · <b lang="de">Wo?</b>(어디에?) → <b lang="de">in</b> – 한 쌍으로 외우세요!</p>""")}
{ex("G2", "G2", "알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Ich {blank("komme", "kommen")} (kommen) aus Südkorea.</li>
        <li>Woher {blank("kommst", "kommen")} (kommen) du?</li>
        <li>Ich {blank("wohne", "wohnen")} (wohnen) in Leipzig.</li>
        <li>Wo {blank("wohnst", "wohnen")} (wohnen) du?</li>
        <li>Ich {blank("spreche", "sprechen")} (sprechen) Koreanisch.</li>
        <li>{blank("Sprichst", "sprechen")} (sprechen) du Deutsch?</li>
      </ol>""")}
{ex("G3", "G3", "woher · wo · wie, aus · in 중에서 고르세요. 한 문항에 빈칸이 두 개!", f"""      <ol lang="de">
        <li>{sel("Woher", wopts)} kommst du? – {sel("Aus", wopts2)} Hamburg.</li>
        <li>{sel("Wo", wopts)} wohnst du? – {sel("In", wopts2)} Leipzig.</li>
        <li>Ich komme {sel("aus", wopts3)} Südkorea, aber ich wohne {sel("in", wopts3)} Leipzig.</li>
        <li>{sel("Woher", wopts)} kommt Lena? Sie kommt {sel("aus", wopts3)} Hamburg.</li>
        <li>{sel("Wie", wopts)} heißt du? – Lena.</li>
      </ol>""")}
{ex("G3b", "G3b", "질문에 알맞은 대답을 고르세요.", f"""      <ol lang="de">
        <li>Woher kommst du? – {sel("Aus Spanien.", qopts)}</li>
        <li>Wo wohnst du? – {sel("In Leipzig.", qopts)}</li>
        <li>Sprichst du Deutsch? – {sel("Ja, ein bisschen.", qopts)}</li>
        <li>Wie heißt du? – {sel("Ich heiße Lena.", qopts)}</li>
      </ol>""")}
{ex("G3c", "G3c", "단어를 바른 순서로 써서 문장을 만드세요.", f"""      <ol lang="de">
        <li>aus / komme / ich / Südkorea → {blank("Ich komme aus Südkorea.", "문장", "full")}</li>
        <li>du / wohnst / wo → {blank("Wo wohnst du?", "문장", "full")}</li>
        <li>Deutsch / du / sprichst → {blank("Sprichst du Deutsch?", "문장", "full")}</li>
        <li>in / wohne / Leipzig / ich → {blank("Ich wohne in Leipzig.", "문장", "full")}</li>
      </ol>""")}
    <details class="more"><summary>더 알아보기 · 다른 말이 맨 앞에 오면? (선택)</summary>
{slots("Jetzt", "V:wohne", "S:ich", "in Leipzig.")}
      <p>„Jetzt“(지금) 같은 말이 맨 앞에 와도 <b>동사는 두 번째</b>, 주어는 동사 뒤로 가요. 4과에서 자세히 연습해요.</p>
    </details>
{tnote("표를 먼저 보여 주지 말고, 오늘의 문장 틀에서 동사에 형광펜 → “ich일 때 끝 글자는? du일 때는?”으로 학생이 규칙을 찾게 하세요. 문장 카드를 잘라 동사 카드(빨간색)를 두 번째 칸에 놓게 하면 어순이 눈에 들어옵니다.")}''')

s2 += block("2교시 · 50분 · Output")
s2 += act("s2-du-sie", 11, "Teil C · <span lang=\"de\">du oder Sie?</span> · 반말과 존댓말", 15, f'''{track("1-03", "dlg-1-03", "다음 날 아침, 어학원 첫 수업. 선생님이 말을 걸어요.")}
{dialog("dlg-1-03", [
    line("Frau Wagner", "Guten Morgen! Ich bin Petra Wagner. Wie heißen Sie?", "좋은 아침이에요! 저는 페트라 바그너예요. 성함이 어떻게 되세요?"),
    line("Minjun", "Ich heiße Minjun Park.", "박민준입니다."),
    line("Frau Wagner", "Wie schreibt man das?", "어떻게 쓰죠?"),
    '      <div class="line"><span class="who"><span class="avatar" style="background-image:url(' + IMG + 'person-minjun.webp)" aria-hidden="true"></span>Minjun</span><span class="tx"><span class="text" lang="de" data-say="P, A, R, K.">P – A – R – K.</span></span></div>',
    line("Frau Wagner", "Danke, Herr Park. Woher kommen Sie?", "고마워요, 박 선생님. 어디에서 오셨어요?"),
    line("Minjun", "Ich komme aus Südkorea.", "한국에서 왔습니다."),
    line("Frau Wagner", "Und wo wohnen Sie?", "그리고 어디에 사세요?"),
    line("Minjun", "Ich wohne in Leipzig, in einer WG.", "라이프치히의 WG(공유 주택)에 살아요.")])}
{gram("du는 친구에게, Sie는 어른에게", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th lang="de">du <small lang="ko">친구·가족·학생끼리</small></th><th lang="de">Sie <small lang="ko">처음 만난 어른·선생님·직원</small></th></tr></thead>
        <tbody lang="de">
          <tr><th lang="ko">이름</th><td>Wie heißt <b>du</b>?</td><td>Wie heißen <b>Sie</b>?</td></tr>
          <tr><th lang="ko">출신</th><td>Woher kommst <b>du</b>?</td><td>Woher kommen <b>Sie</b>?</td></tr>
          <tr><th lang="ko">사는 곳</th><td>Wo wohnst <b>du</b>?</td><td>Wo wohnen <b>Sie</b>?</td></tr>
        </tbody>
      </table></div>
      <p>좋은 소식! <b lang="de">Sie</b>의 동사는 <b>사전형과 똑같아요</b>: <span lang="de">kommen → Sie kommen</span>. (예외: <span lang="de">sein → Sie <b>sind</b></span>)</p>
      <p><b lang="de">Sie</b>는 항상 <b>대문자 S</b>. 부를 때는 <b lang="de">Herr / Frau + 성</b>: <span lang="de">Herr Park</span> ✓ · <span lang="de"><s>Herr Minjun</s></span> ✗</p>""")}
{ex("G4", "G4", "알맞은 질문을 고르세요.", f"""      <ol>
        <li>선생님께 → {sel("Woher kommen Sie?", ["Woher kommst du?", "Woher kommen Sie?"])}</li>
        <li>룸메이트에게 → {sel("Wie heißt du?", ["Wie heißt du?", "Wie heißen Sie?"])}</li>
        <li>분실물 센터 직원에게 → {sel("Wo wohnen Sie?", ["Wo wohnst du?", "Wo wohnen Sie?"])}</li>
        <li>반 친구에게 → {sel("Sprichst du Englisch?", ["Sprichst du Englisch?", "Sprechen Sie Englisch?"])}</li>
        <li>집주인 할머니께 → {sel("Wie heißen Sie?", ["Wie heißt du?", "Wie heißen Sie?"])}</li>
        <li>WG 친구 Jonas에게 → {sel("Woher kommst du?", ["Woher kommst du?", "Woher kommen Sie?"])}</li>
      </ol>""")}
{ex("G4b", "G4b", "du 질문을 Sie 질문으로 바꾸세요.", f"""      <ol lang="de">
        <li>Wie heißt du? → {blank("Wie heißen Sie?", "Sie 질문", "wide")}</li>
        <li>Woher kommst du? → {blank("Woher kommen Sie?", "Sie 질문", "wide")}</li>
        <li>Wo wohnst du? → {blank("Wo wohnen Sie?", "Sie 질문", "wide")}</li>
        <li>Sprichst du Deutsch? → {blank("Sprechen Sie Deutsch?", "Sie 질문", "wide")}</li>
      </ol>""")}
{ex("G4c", "G4c", "Herr일까요, Frau일까요?", f"""      <ol lang="de">
        <li>Petra Wagner → {sel("Frau", ["Herr", "Frau"])} Wagner</li>
        <li>Minjun Park → {sel("Herr", ["Herr", "Frau"])} Park</li>
        <li>Sujin Lee → {sel("Frau", ["Herr", "Frau"])} Lee</li>
        <li>Jonas Becker → {sel("Herr", ["Herr", "Frau"])} Becker</li>
      </ol>""")}''', "output")

s2 += act("s2-fundbuero", 12, "<span lang=\"de\">Im Fundbüro</span> · 분실물 센터에서 (Sie)", 15, f'''    <p>오후, 민준은 중앙역의 <b lang="de">Fundbüro</b>(분실물 센터)에 가요. 대화를 듣고 직원이 쓰는 분실 신고서를 완성하세요.</p>
{track("1-08", "dlg-fundbuero", "분실물 센터 창구에서.")}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-fundbuero", [
    line("Frau", "Guten Tag!", "안녕하세요!"),
    line("Minjun", "Guten Tag. Das ist nicht mein Koffer!", "안녕하세요. 이건 제 가방이 아니에요!"),
    line("Frau", "Oh. Wie heißen Sie?", "아. 성함이 어떻게 되세요?"),
    line("Minjun", "Ich heiße Park. Minjun Park.", "박이에요. 박민준."),
    line("Frau", "Wie schreibt man das?", "어떻게 쓰죠?"),
    '      <div class="line"><span class="who"><span class="avatar" style="background-image:url(' + IMG + 'person-minjun.webp)" aria-hidden="true"></span>Minjun</span><span class="tx"><span class="text" lang="de" data-say="P, A, R, K.">P – A – R – K.</span></span></div>',
    line("Frau", "Woher kommen Sie? Und wo wohnen Sie?", "어디에서 오셨어요? 그리고 어디에 사세요?"),
    line("Minjun", "Ich komme aus Südkorea. Ich wohne jetzt in Leipzig.", "한국에서 왔어요. 지금 라이프치히에 살아요."),
    line("Frau", "Und Ihr Koffer? Wie ist er?", "그럼 손님 가방은요? 어떻게 생겼어요?"),
    line("Minjun", "Er ist schwarz und groß.", "검은색이고 커요."),
    line("Frau", "Danke. Auf Wiedersehen!", "감사합니다. 안녕히 가세요!")])}
    </details>
    <p class="muted">새 단어: <span lang="de">schwarz</span> = 검은 · <span lang="de">groß</span> = 큰 · <span lang="de">Er ist …</span> = (가방은) …해요</p>
{gram("Er ist schwarz – er는 ‘그 남자’만이 아니에요", f"""      <p lang="de"><b class="g-m">der</b> Koffer → <b class="g-m">er</b> &nbsp;·&nbsp; <b class="g-f">die</b> Nummer → <b class="g-f">sie</b></p>
      <p>독일어는 <b>물건</b>도 er(남성)·sie(여성)로 가리켜요. <span lang="de">der Koffer</span>는 남성 명사라서 „<span lang="de">Wie ist <b>er</b>? – <b>Er</b> ist schwarz.</span>“ (그것은 검은색이에요)</p>
      <p><b lang="de">Ihr</b> Koffer = 손님의(당신의) 가방 – <span lang="de">Sie</span>로 말하는 상대에게 써요. 내 것은 <b lang="de">mein</b> Koffer.</p>""")}
{ex("F1", "12a", "분실 신고서 <span lang=\"de\">(Verlustmeldung)</span>를 채우세요.", f"""      <div class="form-grid" lang="de">{"".join(f'<label><span>{x} <small lang="ko">{k}</small></span>{blank(a, x)}</label>' for x, k, a in [("Nachname", "성", "Park"), ("Vorname", "이름", "Minjun"), ("Land", "나라", "Südkorea|Korea"), ("Wohnort", "사는 곳", "Leipzig"), ("Koffer", "가방", "schwarz und groß|groß und schwarz|schwarz, groß")])}</div>""")}
    <p><b>12b</b> 이번에는 <b>내가 손님</b>이에요. ▶로 직원 줄만 듣고, 멈춘 뒤 내 정보로 소리 내어 대답하세요.</p>''', "output")

s2 += act("s2-interview", 13, "<span lang=\"de\">Hören</span> · Jonas 인터뷰 (du)", 10, f'''{track("1-11", "dlg-13", "저녁, WG 부엌. 민준이 Jonas에게 이것저것 물어봐요.")}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-13", [line("Minjun", "Jonas, woher kommst du?", "요나스, 너는 어디에서 왔어?"),
                   line("Jonas", "Ich komme aus Leipzig. Ich wohne hier – in der WG mit dir!", "라이프치히 출신이야. 여기 살지 – 너랑 같은 WG에!"),
                   line("Minjun", "Sprichst du Englisch?", "영어 해?"),
                   line("Jonas", "Ja. Und ich spreche ein bisschen Spanisch.", "응. 그리고 스페인어도 조금 해."),
                   line("Minjun", "Wie ist deine Handynummer?", "네 휴대폰 번호는 뭐야?"),
                   line("Jonas", "Null – eins – sieben – null … zwölf, acht, fünfzehn.", "0170 … 12 8 15")])}
    </details>
{ex("13a", "13a", "Jonas의 프로필을 완성하세요.", f"""      <div class="form-grid" lang="de">{"".join(f'<label><span>{x} <small lang="ko">{k}</small></span>{blank(a, x, cls, digits=d)}</label>' for x, k, a, cls, d in [("Woher?", "출신", "Leipzig|aus Leipzig", "", False), ("Wo?", "사는 곳", "in der WG|WG|in einer WG|hier", "", False), ("Sprachen: Deutsch, Englisch und …", "언어", "Spanisch", "", False), ("Handy", "번호", "0170 12 8 15", "wide", True)])}</div>""")}
    <p><b>13b</b> 이제 나에 대해 써 보세요. 대답은 완전한 문장으로!</p>
    <div class="form-grid" lang="de">{"".join(f'<label><span>{q}</span><input class="blank" aria-label="{q}" placeholder="Ich …"></label>' for q in ["Wie heißt du?", "Woher kommst du?", "Wo wohnst du?", "Sprichst du Englisch?"])}</div>
{tnote("못 알아들었을 때 쓰는 <span lang='de'>Wie bitte?</span>를 꼭 쓰게 하세요. 3명이 끝난 학생은 Sie로 바꿔서 교사와 한 번 더.")}''', "output")

s2 += act("s2-formular", 14, "<span lang=\"de\">Lesen</span> · 어학원 등록 신청서", 10, f'''    <p>앞의 듣기 활동(<a href="#s2-herkunft">어학원 친구들</a>)에 나온 Ahmet가 어학원 <b lang="de">Anmeldung</b>(등록 신청서)를 냈어요. 그런데 <b>틀린 정보가 두 개</b> 있어요!</p>
    <div class="form-card" lang="de">
      <p class="form-card-title">Sprachschule Leipzig · Anmeldung</p>
      <dl>
        <dt>Nachname</dt><dd>Yılmaz</dd><dt>Vorname</dt><dd>Ahmet</dd><dt>Land</dt><dd>Türkei</dd>
        <dt>Wohnort</dt><dd>Dresden</dd><dt>Sprachen</dt><dd>Türkisch, Englisch</dd><dt>Kurs</dt><dd>A1</dd>
      </dl>
    </div>
{ex("AN1", "14a", "Ahmet의 자기소개를 다시 듣고, 틀린 정보를 바르게 고치세요.", f"""      <p><button type="button" class="say-btn" data-play="dlg-h1" aria-label="Ahmet 다시 듣기">▶</button> Ahmet 다시 듣기</p>
      <div class="form-grid" lang="de">
        <label><span>Wohnort <small lang="ko">사는 곳</small></span>{blank("Leipzig", "Wohnort")}</label>
        <label><span>Sprachen <small lang="ko">언어</small></span>{blank("Türkisch, Deutsch|Türkisch und Deutsch|Türkisch und ein bisschen Deutsch|Türkisch, ein bisschen Deutsch", "Sprachen")}</label>
      </div>""")}
    <p><b>14b</b> 이번에는 <b>내</b> 신청서를 써 보세요. 서류에서는 <b lang="de">Nachname</b>을 먼저 쓰는 경우가 많아요.</p>
    <div class="form-grid" lang="de">{"".join(f'<label><span>{x} <small lang="ko">{k}</small></span><input class="blank" aria-label="{x}"></label>' for x, k in [("Nachname", "성"), ("Vorname", "이름"), ("Land", "나라"), ("Wohnort", "사는 곳"), ("Sprachen", "언어"), ("Handynummer", "휴대폰")])}</div>''', "output")

s2 += homework("hw-2", "2차시 숙제 (60분)", [
    ("오늘의 문장 틀 ② 6문장 듣고 따라 하기 + 나라·언어 카드 복습", 10),
    ("<b>H2 · H2b · H2c</b> 질문 만들기(du / Sie), 동사 형태", 15),
    ("<b>H2d · H2e</b> 단어로 문장 만들기, 상황에 맞는 질문 쓰기", 15),
    ("<b>H2f · H2g</b> Lena의 메시지 읽기, 대문자 고치기", 10),
    (ic("mic") + "<b>녹음</b>: 내 이름 철자 + “Ich komme aus … Ich wohne in … Ich spreche …” 녹음해서 제출", 10)],
    ex("H2", "H2", "대답을 보고 질문을 쓰세요. (du)", f"""      <ol lang="de">
        <li>{blank("Wie heißt du?", "질문", "wide")} – Ich heiße Carlos.</li>
        <li>{blank("Woher kommst du?", "질문", "wide")} – Ich komme aus Spanien.</li>
        <li>{blank("Wo wohnst du?", "질문", "wide")} – Ich wohne in Leipzig.</li>
        <li>{blank("Sprichst du Englisch?", "질문", "wide")} – Ja, ich spreche Englisch.</li>
      </ol>""") + "\n" + ex("H2b", "H2b", "Sie로 대답을 보고 질문을 쓰세요.", f"""      <ol lang="de">
        <li>{blank("Wie heißen Sie?", "질문", "wide")} – Ich heiße Petra Wagner.</li>
        <li>{blank("Woher kommen Sie?", "질문", "wide")} – Ich komme aus Leipzig.</li>
        <li>{blank("Wo wohnen Sie?", "질문", "wide")} – Ich wohne in Leipzig.</li>
        <li>{blank("Sprechen Sie Englisch?", "질문", "wide")} – Ja, ich spreche Englisch.</li>
      </ol>""") + "\n" + ex("H2c", "H2c", "알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Woher {blank("kommst", "kommen")} du? (kommen)</li>
        <li>Ich {blank("spreche", "sprechen")} Koreanisch. (sprechen)</li>
        <li>{blank("Sprichst", "sprechen")} du Polnisch? (sprechen)</li>
        <li>Wo {blank("wohnen", "wohnen")} Sie? (wohnen)</li>
        <li>Wie {blank("heißen", "heißen")} Sie? (heißen)</li>
        <li>{blank("Sind", "sein")} Sie Frau Wagner? (sein)</li>
        <li>Ich {blank("wohne", "wohnen")} in Leipzig. (wohnen)</li>
        <li>{blank("Bist", "sein")} du Carlos? (sein)</li>
      </ol>""") + "\n" + ex("H2d", "H2d", "단어로 문장을 만드세요. 동사 형태도 바꾸세요!", f"""      <ol lang="de">
        <li>du / woher / kommen ? → {blank("Woher kommst du?", "문장", "full")}</li>
        <li>ich / in Leipzig / wohnen . → {blank("Ich wohne in Leipzig.", "문장", "full")}</li>
        <li>du / Deutsch / sprechen ? → {blank("Sprichst du Deutsch?", "문장", "full")}</li>
        <li>ich / aus Südkorea / kommen . → {blank("Ich komme aus Südkorea.", "문장", "full")}</li>
        <li>Sie / wo / wohnen ? → {blank("Wo wohnen Sie?", "문장", "full")}</li>
        <li>Sie / Englisch / sprechen ? → {blank("Sprechen Sie Englisch?", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H2e", "H2e", "이 상황에서 무엇을 물어볼까요? 독일어 질문을 쓰세요. (du일까요, Sie일까요?)", f"""      <ol>
        <li>시청 직원에게 이름을 물어요. → <span lang="de">{blank("Wie heißen Sie?", "질문", "full")}</span></li>
        <li>새 룸메이트에게 어디에서 왔는지 물어요. → <span lang="de">{blank("Woher kommst du?", "질문", "full")}</span></li>
        <li>병원에서 의사에게 영어를 하는지 물어요. → <span lang="de">{blank("Sprechen Sie Englisch?", "질문", "full")}</span></li>
        <li>놀이터에서 아이에게 이름을 물어요. → <span lang="de">{blank("Wie heißt du?", "질문", "full")}</span></li>
        <li>집주인에게 어디에 사는지 물어요. → <span lang="de">{blank("Wo wohnen Sie?", "질문", "full")}</span></li>
      </ol>""") + "\n" + ex("H2f", "H2f", "Lena가 보낸 메시지를 읽고, 맞으면 <b>r</b>, 틀리면 <b>f</b>", f"""      <div class="box" lang="de"><p>Hallo Minjun!<br>Ich bin's, Lena aus der WG. Ich komme aus Hamburg, aber ich wohne jetzt hier in Leipzig. Ich spreche Deutsch, Englisch und ein bisschen Koreanisch – „Annyeonghaseyo“! Jonas kommt aus Leipzig. Er spricht Deutsch und Englisch. Sprichst du auch Spanisch?<br>Bis später! Lena</p></div>
      <p class="muted">Ich bin's = 나야 · Bis später! = 이따 봐!</p>
""" + rf("h2f", [
    ("Lena wohnt in Hamburg.", "f", ""),
    ("Lena spricht drei Sprachen.", "r", ""),
    ("Lena spricht sehr gut Koreanisch.", "f", ""),
    ("Jonas kommt aus Leipzig.", "r", ""),
    ("Lena fragt: „Sprichst du Spanisch?“", "r", "")])) + "\n" + ex("H2g", "H2g", "대문자를 바르게 고쳐 다시 쓰세요.", f"""      <ol lang="de">
        <li>ich komme aus polen. → {blank("Ich komme aus Polen.", "고친 문장", "full")}</li>
        <li>sprichst du englisch? → {blank("Sprichst du Englisch?", "고친 문장", "full")}</li>
        <li>wo wohnen sie, frau wagner? → {blank("Wo wohnen Sie, Frau Wagner?", "고친 문장", "full")}</li>
      </ol>"""))

# =====================================================================
# 3차시 · Wer ist das?
# =====================================================================
wh_opts = ["Ahmet", "Mei", "Olena", "Lucas", "Jonas"]
copts = ["Carlos", "Tomasz", "Priya", "Frau Wagner"]
s3 = block("1교시 · 50분 · Input")
s3 += act("s3-wiederholung", "", "복습", 5, '    <p><b>질문 릴레이</b>: „<span lang="de">Woher kommst du?</span>“ → 대답한 사람이 다음 사람에게 „<span lang="de">Wo wohnst du?</span>“</p>')
s3 += act("s3-teil-d", 14, "Teil D · <span lang=\"de\">Wer ist das?</span> · 반 친구 소개", 10, f'''{track("1-04", "dlg-1-04", "쉬는 시간, 옆자리 Carlos가 친구들을 소개해요.")}
{dialog("dlg-1-04", [
    line("Carlos", "Hallo! Ich bin Carlos. Ich komme aus Spanien.", "안녕! 나는 카를로스야. 스페인에서 왔어."),
    line("Minjun", "Hallo, Carlos! Ich bin Minjun.", "안녕, 카를로스! 나는 민준이야."),
    line("Carlos", "Das ist Tomasz. Er kommt aus Polen.", "이쪽은 토마스야. 폴란드에서 왔어."),
    line("Tomasz", "Hallo! Freut mich.", "안녕! 반가워."),
    line("Carlos", "Und das ist Priya. Sie kommt aus Indien.", "그리고 이쪽은 프리야. 인도에서 왔어."),
    line("Priya", "Hi! Ich möchte hier studieren.", "안녕! 나는 여기서 대학에 다니고 싶어."),
    line("Minjun", "Ich auch!", "나도!")])}
    <div class="cast cast-big" aria-label="반 친구들">{"".join(f'<figure>{pic("person-" + k, n, "person")}<figcaption>{n}<br><small>{c}</small></figcaption></figure>' for k, n, c in [("carlos", "Carlos", "Spanien · Koch"), ("tomasz", "Tomasz", "Polen · Ingenieur"), ("priya", "Priya", "Indien · Informatikerin"), ("wagner", "Frau Wagner", "Lehrerin")])}</div>
{ex("C1", "C1", "누구일까요?", f"""      <ol lang="de">
        <li>Er kommt aus Polen. → {sel("Tomasz", copts)}</li>
        <li>Sie kommt aus Indien. → {sel("Priya", copts)}</li>
        <li>Er kommt aus Spanien. → {sel("Carlos", copts)}</li>
        <li>Er ist Ingenieur. → {sel("Tomasz", copts)}</li>
        <li>Sie ist Lehrerin. → {sel("Frau Wagner", copts)}</li>
        <li>Sie möchte hier studieren. → {sel("Priya", copts)}</li>
      </ol>""")}''')

s3 += act("s3-satz3", 15, "오늘의 문장 틀 ③ · 그는 / 그녀는", 10, f'''{today([
    ("Das ist Tomasz.", "다스 이스트 토마스", "이쪽은 토마스야."),
    ("Er kommt aus Polen.", "에어 콤트 아우스 폴렌", "그는 폴란드에서 왔어."),
    ("Das ist Priya.", "다스 이스트 프리야", "이쪽은 프리야야."),
    ("Sie wohnt in Leipzig.", "지 본트 인 라이프치히", "그녀는 라이프치히에 살아.")])}
{gram("er(그) · sie(그녀)는 -t", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th lang="de">kommen</th><th lang="de">wohnen</th><th lang="de">sprechen</th><th lang="de">heißen</th><th lang="de">sein</th></tr></thead>
        <tbody lang="de">
          <tr><th>ich <small lang="ko">나</small></th><td>komme</td><td>wohne</td><td>spreche</td><td>heiße</td><td>bin</td></tr>
          <tr><th>du <small lang="ko">너</small></th><td>kommst</td><td>wohnst</td><td>sprichst</td><td>heißt</td><td>bist</td></tr>
          <tr><th>er / sie <small lang="ko">그 / 그녀</small></th><td>komm<b>t</b></td><td>wohn<b>t</b></td><td>spr<b>i</b>ch<b>t</b></td><td>heiß<b>t</b></td><td><b>ist</b></td></tr>
          <tr><th>Sie <small lang="ko">당신</small></th><td>kommen</td><td>wohnen</td><td>sprechen</td><td>heißen</td><td>sind</td></tr>
        </tbody>
      </table></div>
      <p>남자는 <b lang="de">er</b>, 여자는 <b lang="de">sie</b>. 둘 다 동사 끝이 <b>-t</b>예요. 소개는 <span lang="de"><b>Das ist</b> + 이름</span>으로 시작!</p>
      <p class="muted">직업도 말해 볼까요? <span lang="de">Carlos ist Koch.</span> (요리사) · <span lang="de">Tomasz ist Ingenieur.</span> – 직업 앞에는 <span lang="de">ein</span>을 쓰지 않아요.</p>""")}
{ex("G5", "G5", "알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Tomasz {blank("kommt", "kommen")} (kommen) aus Polen.</li>
        <li>Priya {blank("wohnt", "wohnen")} (wohnen) in Leipzig.</li>
        <li>Lena {blank("spricht", "sprechen")} (sprechen) Englisch.</li>
        <li>Das {blank("ist", "sein")} (sein) Carlos.</li>
        <li>Er {blank("heißt", "heißen")} (heißen) Jonas.</li>
        <li>Das ist Priya. {sel("Sie", ["Er", "Sie"])} kommt aus Indien.</li>
        <li>Carlos {blank("spricht", "sprechen")} (sprechen) Spanisch.</li>
        <li>Frau Wagner {blank("wohnt", "wohnen")} (wohnen) in Leipzig.</li>
      </ol>""")}
{ex("G5b", "G5b", "er/sie와 동사를 <b>둘 다</b> 쓰세요. (괄호 = 사전형)", f"""      <ol lang="de">
        <li>Das ist Lena. {blank("Sie kommt", "er/sie + 동사", "wide")} aus Hamburg. (kommen)</li>
        <li>Das ist Jonas. {blank("Er wohnt", "er/sie + 동사", "wide")} in einer WG. (wohnen)</li>
        <li>Das ist Carlos. {blank("Er ist", "er/sie + 동사", "wide")} Koch. (sein)</li>
        <li>Das ist Haeun. {blank("Sie spricht", "er/sie + 동사", "wide")} Deutsch. (sprechen)</li>
        <li>Das ist Herr Park. {blank("Er heißt", "er/sie + 동사", "wide")} Minjun. (heißen)</li>
        <li>Das ist Frau Schulze. {blank("Sie wohnt", "er/sie + 동사", "wide")} unten. (wohnen)</li>
      </ol>""")}
{ex("G6", "G6", "동사 표를 채우세요.", f"""      <div class="table-wrap"><table lang="de" class="fixed"><thead><tr><th></th><th>wohnen</th><th>heißen</th><th>sein</th></tr></thead><tbody>
        <tr><th>ich</th><td>{blank("wohne", "ich wohnen")}</td><td>{blank("heiße", "ich heißen")}</td><td>{blank("bin", "ich sein")}</td></tr>
        <tr><th>du</th><td>{blank("wohnst", "du wohnen")}</td><td>{blank("heißt", "du heißen")}</td><td>{blank("bist", "du sein")}</td></tr>
        <tr><th>er / sie</th><td>{blank("wohnt", "er wohnen")}</td><td>{blank("heißt", "er heißen")}</td><td>{blank("ist", "er sein")}</td></tr>
        <tr><th>Sie</th><td>{blank("wohnen", "Sie wohnen")}</td><td>{blank("heißen", "Sie heißen")}</td><td>{blank("sind", "Sie sein")}</td></tr>
      </tbody></table></div>""")}
    <details class="more"><summary>더 알아보기 · 우리, 너희는? (2과에서 배워요)</summary>
      <p lang="de">wir komm<b>en</b> (우리) · ihr komm<b>t</b> (너희) · sie komm<b>en</b> (그들) – 2과에서 가족과 WG 이야기를 하면서 연습해요.</p>
    </details>''')


nums = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn", "zwanzig"]
ncells = "".join(f'<div class="say-cell" data-say="{n}"><b>{i}</b><span>{n}</span></div>' for i, n in enumerate(nums))
s3 += act("s3-wer", 16, "<span lang=\"de\">Hören</span> · 누구 이야기일까요?", 10, f'''    <p>Frau Wagner가 어학원 학생들을 소개해요. ▶로 듣고 누구인지 고르세요. (2차시에 들은 어학원 친구들도 나와요!)</p>
{ex("WH1", "16a", "누구일까요?", f"""      <ol>
        <li><button type="button" class="say-btn" data-play="dlg-w1" aria-label="1번 듣기">▶</button> {sel("Mei", wh_opts)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-w2" aria-label="2번 듣기">▶</button> {sel("Ahmet", wh_opts)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-w3" aria-label="3번 듣기">▶</button> {sel("Lucas", wh_opts)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-w4" aria-label="4번 듣기">▶</button> {sel("Olena", wh_opts)}</li>
        <li><button type="button" class="say-btn" data-play="dlg-w5" aria-label="5번 듣기">▶</button> {sel("Jonas", wh_opts)}</li>
      </ol>""")}
{ex("WH2", "16b", "다시 듣고 동사를 쓰세요.", f"""      <ol lang="de">
        <li>Sie {blank("kommt", "동사")} aus China.</li>
        <li>Er {blank("wohnt", "동사")} in Leipzig.</li>
        <li>Er {blank("spricht", "동사")} drei Sprachen.</li>
        <li>Sie {blank("ist", "동사")} Ärztin.</li>
        <li>Er {blank("heißt", "동사")} Jonas.</li>
      </ol>""")}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-w1", [line("Frau Wagner", "Sie kommt aus China. Sie wohnt in Halle. Sie spricht Chinesisch und Englisch.", "그녀는 중국에서 왔어요. 할레에 살아요. 중국어와 영어를 해요.")])}
{dialog("dlg-w2", [line("Frau Wagner", "Er kommt aus der Türkei. Er wohnt in Leipzig. Er spricht Türkisch.", "그는 튀르키예에서 왔어요. 라이프치히에 살아요. 튀르키예어를 해요.")])}
{dialog("dlg-w3", [line("Frau Wagner", "Er kommt aus Brasilien. Er wohnt in Dresden. Er spricht drei Sprachen.", "그는 브라질에서 왔어요. 드레스덴에 살아요. 3개 언어를 해요.")])}
{dialog("dlg-w4", [line("Frau Wagner", "Sie kommt aus der Ukraine. Sie ist Ärztin. Sie spricht Ukrainisch und Russisch.", "그녀는 우크라이나에서 왔어요. 의사예요. 우크라이나어와 러시아어를 해요.")])}
{dialog("dlg-w5", [line("Frau Wagner", "Er heißt Jonas. Er kommt aus Leipzig. Er wohnt in einer WG – mit Minjun!", "그의 이름은 요나스예요. 라이프치히 출신이에요. WG에 살아요 – 민준이랑!")])}
    </details>
    <p class="muted">새 단어: <span lang="de">Ärztin</span> = (여자) 의사</p>''')

s3 += act("s3-zahlen", 16, "<span lang=\"de\">Die Zahlen 0–20</span> · 숫자와 전화번호", 15, f'''    <p>숫자를 눌러 듣고 따라 하세요.</p>
    <div class="say-grid numbers" lang="de">{ncells}</div>
{ex("16x", "16a", "숫자를 독일어로 쓰세요.", f"""      <ol lang="de">
        <li>3 → {blank("drei", "3", ci=True)}</li>
        <li>7 → {blank("sieben", "7", ci=True)}</li>
        <li>11 → {blank("elf", "11", ci=True)}</li>
        <li>12 → {blank("zwölf", "12", ci=True)}</li>
        <li>16 → {blank("sechzehn", "16", ci=True)}</li>
        <li>20 → {blank("zwanzig", "20", ci=True)}</li>
      </ol>""")}
{ex("16y", "16b", "계산하고 답을 독일어로 쓰세요.", f"""      <ol lang="de">
        <li>zwei + drei = {blank("fünf", "답", ci=True)}</li>
        <li>vier + sechs = {blank("zehn", "답", ci=True)}</li>
        <li>acht + neun = {blank("siebzehn", "답", ci=True)}</li>
        <li>zwanzig – sieben = {blank("dreizehn", "답", ci=True)}</li>
        <li>elf + eins = {blank("zwölf", "답", ci=True)}</li>
        <li>neunzehn – fünf = {blank("vierzehn", "답", ci=True)}</li>
      </ol>""")}
{ex("16z", "16c", "▶로 듣고 숫자로 쓰세요.", f"""      <ol lang="de">
        <li><span class="lis" data-say="fünfzehn"></span> {blank("15", "숫자", digits=True)}</li>
        <li><span class="lis" data-say="acht"></span> {blank("8", "숫자", digits=True)}</li>
        <li><span class="lis" data-say="neunzehn"></span> {blank("19", "숫자", digits=True)}</li>
        <li><span class="lis" data-say="sechs"></span> {blank("6", "숫자", digits=True)}</li>
        <li><span class="lis" data-say="vierzehn"></span> {blank("14", "숫자", digits=True)}</li>
        <li><span class="lis" data-say="zwei"></span> {blank("2", "숫자", digits=True)}</li>
      </ol>""")}
    <div class="box tip">{ic("tip")}13–19는 <b>숫자 + zehn</b>: <span lang="de">drei + zehn = dreizehn</span>. 조심: <b lang="de">sech</b>zehn, <b lang="de">sieb</b>zehn</div>
{today([("Wie ist deine Handynummer?", "비 이스트 다이네 핸디누머", "네 휴대폰 번호가 뭐야?"),
        ("Null – eins – sieben – sechs …", "", "0 – 1 – 7 – 6 … (한 자리씩 말해도 OK)")], "전화번호 묻고 답하기")}
{gram("전화번호는 이렇게 읽어요", f"""      <p lang="de">0176 / 13 05 18 9</p>
      <p>① 앞자리(<span lang="de">Vorwahl</span>)는 <b>한 자리씩</b>: <span lang="de">null – eins – sieben – sechs</span></p>
      <p>② 뒷자리는 <b>두 자리씩</b> 읽는 사람이 많아요: <span lang="de">dreizehn – null fünf – achtzehn – neun</span></p>
      <p>묻기: <span lang="de">Wie ist <b>deine</b> Handynummer?</span> (du) · <span lang="de">Wie ist <b>Ihre</b> Handynummer?</span> (Sie)</p>""")}
{ex("14a", "16d", f"{ic('listen')}Track 1-07 · Frau Wagner가 전화번호를 확인해요. 듣고 쓰세요.", f"""      <div class="table-wrap"><table><thead><tr><th>이름</th><th lang="de">Handynummer</th></tr></thead><tbody lang="de">
        <tr><td>Minjun Park</td><td>0176 – {blank("13 05 18 9", "Minjun 번호", "wide", digits=True)}</td></tr>
        <tr><td>Carlos Ruiz</td><td>0157 – {blank("20 16 4 12", "Carlos 번호", "wide", digits=True)}</td></tr>
        <tr><td>Priya Sharma</td><td>0152 – {blank("17 11 19 3", "Priya 번호", "wide", digits=True)}</td></tr>
      </tbody></table></div>
      <details class="transcript"><summary>대본 보기 (듣기가 끝난 뒤에!)</summary>
{dialog("dlg-1-07", [
    line("Frau Wagner", "Herr Park, Ihre Nummer ist null, eins, sieben, sechs, dreizehn, null fünf, achtzehn, neun. Richtig?", "박 선생님, 번호가 0176 13 05 18 9 맞죠?"),
    line("Minjun", "Ja, richtig.", "네, 맞아요."),
    line("Carlos", "Meine Nummer: null, eins, fünf, sieben, zwanzig, sechzehn, vier, zwölf.", "제 번호는 0157 20 16 4 12예요."),
    line("Priya", "Null, eins, fünf, zwei, siebzehn, elf, neunzehn, drei.", "0152 17 11 19 3이에요.")])}
        <button type="button" class="btn ghost" data-play="dlg-1-07">▶ 전체 듣기</button>
      </details>""")}
    <div class="ex box mystery" data-check data-ex="14b">
      <div class="ex-head"><span class="tag">16e</span>{ic("search")}{ic("listen")}Track 1-09 · 저녁, WG. 가방 이름표의 지워진 번호! 들리는 숫자만 쓰세요.</div>
      <p lang="de">{pic("ding-anhaenger", "가방 이름표", "mini")}<b>T. S.</b> · Tel.: {blank("040", "앞자리", digits=True)} – {blank("17", "다음 숫자", digits=True)} ▓▓ {blank("3", "다음 숫자", digits=True)} ▓▓▓</p>
      <p>이 사람은 어느 도시에 살까요? → {blank("Hamburg|in Hamburg|aus Hamburg", "도시", "wide", ci=True)}</p>
      <details class="transcript"><summary>대본 보기 (듣기가 끝난 뒤에!)</summary>
{dialog("dlg-1-09", [
    line("Jonas", "Null, vier, null … siebzehn … hm, das kann ich nicht lesen.", "0, 4, 0 … 17 … 음, 이건 못 읽겠어."),
    line("Lena", "Null, vier, null? Das ist Hamburg! Ich komme aus Hamburg!", "040? 그거 함부르크야! 내가 함부르크 출신이잖아!"),
    line("Jonas", "Der Mann kommt aus Hamburg? Das ist ein Fall für uns!", "그 남자가 함부르크에서 왔다고? 이건 우리가 풀 사건이야!")])}
        <button type="button" class="btn ghost" data-play="dlg-1-09">▶ 전체 듣기</button>
      </details>
      <div class="box tip">{ic("tip")}독일 전화번호 앞자리(<b lang="de">Vorwahl</b>)는 도시를 알려 줘요. Leipzig = 0341, Hamburg = 040</div>
    </div>''')

prof = [("carlos", "Carlos Ruiz", "Hallo! Ich heiße Carlos. Ich komme aus Spanien. Ich wohne in Leipzig. Ich spreche Spanisch und Englisch.", "안녕! 내 이름은 카를로스야. 스페인에서 왔어. 라이프치히에 살아. 스페인어와 영어를 해."),
        ("tomasz", "Tomasz Nowak", "Hallo, ich bin Tomasz. Ich komme aus Polen. Ich bin Ingenieur. Ich spreche Polnisch, Englisch und Russisch.", "안녕, 나는 토마스야. 폴란드에서 왔어. 엔지니어야. 폴란드어, 영어, 러시아어를 해."),
        ("priya", "Priya Sharma", "Hi! Ich heiße Priya. Ich komme aus Indien. Ich spreche Hindi und Englisch. Ich möchte in Leipzig studieren.", "안녕! 내 이름은 프리야야. 인도에서 왔어. 힌디어와 영어를 해. 라이프치히에서 대학에 다니고 싶어."),
        ("minjun", "Minjun Park", "Hallo! Ich heiße Minjun. Ich komme aus Südkorea. Ich wohne in einer WG. Ich spreche Koreanisch und Englisch.", "안녕! 내 이름은 민준이야. 한국에서 왔어. WG에 살아. 한국어와 영어를 해.")]
pcards = "".join(f'<div class="profile">{pic("person-" + k, n, "person")}<b>{n}</b><span lang="de">{de}</span><span class="ko">{ko}</span></div>' for k, n, de, ko in prof)

s3 += block("2교시 · 50분 · Output")
s3 += act("s3-lesen", 17, "<span lang=\"de\">Lesen</span> · 우리 반 프로필", 10, f'''    <p>Frau Wagner가 교실 벽에 붙인 <b lang="de">Steckbrief</b>(프로필)예요. 먼저 <b>한국어 뜻을 손으로 가리고</b> 읽어 보세요!</p>
    <div class="profiles">{pcards}</div>
{gram("möchte + 동사원형 – 동사가 둘이면 하나는 맨 끝", f"""{slots("S:Ich", "V:möchte", "in Leipzig", "V:studieren.")}
      <p><b lang="de">möchte</b>(~하고 싶다)는 두 번째 자리, 진짜 할 일(<span lang="de">studieren</span>)은 <b>사전형으로 맨 끝</b>에 가요. 지금은 이 문장을 통째로 익히고, 4과에서 자세히 배워요.</p>""")}
{ex("L1", "L1", "네 프로필을 <b>모두</b> 보고 판단하세요. 맞으면 r, 틀리면 f", rf("l1", [
    ("Tomasz spricht drei Sprachen.", "r", "drei Sprachen = 3개 언어"),
    ("Alle vier sprechen Englisch.", "r", "alle vier = 네 명 모두"),
    ("Carlos kommt aus Spanien und wohnt jetzt in Leipzig.", "r", ""),
    ("Priya spricht Hindi und Spanisch.", "f", ""),
    ("Priya studiert schon in Leipzig.", "f", "studieren = 대학에 다니다 · schon = 이미"),
    ("Zwei Personen sprechen Spanisch.", "f", "zwei Personen = 두 사람"),
    ("Tomasz kommt aus Polen und ist Ingenieur.", "r", "")]))}
{ex("L2", "L2", "프로필을 보고 빈칸을 채우세요.", f"""      <ol lang="de">
        <li>Carlos kommt aus {blank("Spanien", "나라")}.</li>
        <li>Tomasz ist {blank("Ingenieur", "직업")}.</li>
        <li>Priya spricht Hindi und {blank("Englisch", "언어")}.</li>
        <li>Minjun wohnt in einer {blank("WG", "집")}.</li>
        <li>Tomasz spricht Polnisch, Englisch und {blank("Russisch", "언어")}.</li>
      </ol>""")}''', "output")

s3 += act("s3-sprachmittlung", 18, f"{ic('mediate')}<span lang=\"de\">Sprachmittlung</span> · 한국어로 듣고 독일어로 전하기", 10, f'''{track("1-10", "dlg-1-10", "저녁, Kochstraße 12. 계단에서 이삿짐을 옮기는 여자와 여자아이를 만난 민준이 상자 하나를 들어 줘요.")}
    {fig("story-3-treppenhaus", "계단에서 상자를 든 민준과 한국인 엄마와 딸이 마주치고, 1층 문 앞에서 나이 든 독일 여성이 무표정하게 바라본다")}
{dialog("dlg-1-10", [
    line("수진", "어머, 혹시 한국 분이세요?", "", lang=""),
    line("민준", "네! 저는 박민준이에요. 부산에서 왔어요. 이 건물 WG에 살아요.", "", lang=""),
    line("수진", "반가워요! 저는 이수진이에요. 서울에서 왔어요. 오늘 이 건물로 이사 왔어요. 얘는 딸 하은이에요.", "", lang=""),
    stage("1층 문이 열리고 할머니가 나온다."),
    line("하은", "Guten Tag, Frau Schulze!", "안녕하세요, 슐체 할머니!"),
    line("Frau Schulze", "… Guten Tag.", "…안녕하세요."),
    stage("웃지 않고 문을 닫는다.")], cls="dialog ko", lang="ko")}
    <p class="stage">(잠시 후, WG 부엌)</p>
{dialog("dlg-jonas", [line("Jonas", "Minjun, wer ist das?", "민준, 저 사람들 누구야?")])}
{ex("17a", "18a", "민준이 되어 Jonas에게 <b>독일어로</b> 전하세요. 필요한 정보만 골라요!", f"""      <p lang="de" class="template">Das ist {blank("Sujin|Sujin Lee", "이름", ci=True)}. Sie kommt aus {blank("Seoul|Südkorea|Korea", "출신", ci=True)}. Sie wohnt jetzt {blank("hier|in Leipzig", "사는 곳", ci=True)}. Das ist Haeun. Sie spricht schon {blank("Deutsch", "언어", ci=True)}!</p>""")}
    <div class="box tip">{ic("tip")}<b>중개하기</b>는 한 문장씩 번역하는 게 아니에요. <b>필요한 정보만 골라</b> 쉬운 독일어로 전하면 돼요. 오늘 배운 <span lang="de">Das ist … / Sie kommt aus …</span>가 딱 맞죠?</div>
{tnote("“독일에서 한국인 이웃을 만나면 당연히 한국어로 말하겠죠? 그런데 그 내용을 독일 친구에게 전해야 한다면?” – 활동의 이유를 이렇게 설명해 주세요. <i lang='de'>schon</i>(벌써)은 덩어리로만.")}''', "output")

s3 += act("s3-vorstellen", 19, "<span lang=\"de\">Sprechen</span> · 다른 사람 소개하기", 10, f'''    <p>프로필 카드를 보고 이 사람을 소개하세요. 먼저 <b>소리 내어 말하고</b>, 그다음 쓰세요.</p>
    <div class="namecards profile-cards">
      <figure>{pic("steckbrief-olena", "Steckbrief: Olena Kovalenko – Land: Ukraine, Wohnort: Leipzig, Sprachen: Ukrainisch, Russisch, Beruf: Ärztin", "card-img")}</figure>
      <figure>{pic("steckbrief-ahmet", "Steckbrief: Ahmet Yılmaz – Land: Türkei, Wohnort: Leipzig, Sprachen: Türkisch, Deutsch, Beruf: Koch", "card-img")}</figure>
    </div>
{ex("VS1", "19a", "Olena를 소개하는 문장을 완성하세요.", f"""      <ol lang="de">
        <li>Das {blank("ist", "동사")} Olena Kovalenko.</li>
        <li>Sie kommt aus {blank("der Ukraine", "나라", "wide")}.</li>
        <li>{blank("Sie wohnt in Leipzig.", "문장", "full")}</li>
        <li>{blank("Sie spricht Ukrainisch und Russisch.", "문장", "full")}</li>
        <li>{blank("Sie ist Ärztin.", "문장", "full")}</li>
      </ol>""")}
{ex("VS2", "19b", "Ahmet를 소개하는 글을 쓰세요. (5문장, 순서대로)", f"""      <ol lang="de">
        <li>{blank("Das ist Ahmet.|Das ist Ahmet Yılmaz.", "문장 1", "full")}</li>
        <li>{blank("Er kommt aus der Türkei.", "문장 2", "full")}</li>
        <li>{blank("Er wohnt in Leipzig.", "문장 3", "full")}</li>
        <li>{blank("Er spricht Türkisch und Deutsch.", "문장 4", "full")}</li>
        <li>{blank("Er ist Koch.", "문장 5", "full")}</li>
      </ol>""")}
    <p><b>19c</b> {ic("mic")} 혼자 녹음하기 · 두 사람을 보지 않고 소개해 보세요. 30초 안에!</p>''', "output")

s3 += act("s3-schreiben", 19, "<span lang=\"de\">Schreiben</span> · 나를 소개하는 글", 15, f'''    <p><b>19a</b> (7분) 틀에 맞춰 나를 소개하세요.</p>
    <p lang="de" class="template">Hallo! Ich heiße {blank("", "이름").replace(' data-answer=""', '')}. Ich komme aus {blank("", "나라").replace(' data-answer=""', '')}. Ich wohne in {blank("", "도시").replace(' data-answer=""', '')}. Ich spreche {blank("", "언어").replace(' data-answer=""', '')}.</p>
    <p><b>19b</b> (4분) 공책에 옮겨 쓰고, <b>한 문장 더</b> 붙여 보세요. 예: <span lang="de">Ich bin Student / Studentin.</span> · <span lang="de">Ich lerne Deutsch.</span></p>
    <textarea lang="de" data-persist="steckbrief" rows="5" placeholder="Hallo! Ich heiße …" aria-label="나의 자기소개"></textarea>
    <p><b>19c</b> (4분) 다 쓴 글을 소리 내어 읽고 <b>스스로</b> 아래 세 가지를 확인하세요.</p>
    <div class="table-wrap"><table><tbody>
      <tr><td>☐</td><td>동사가 <b>두 번째</b>에 있나요? (<span lang="de">Ich <b>komme</b> aus …</span>)</td></tr>
      <tr><td>☐</td><td>ich 다음 동사가 <b>-e</b>로 끝나나요? (<span lang="de">ich wohn<b>e</b></span>)</td></tr>
      <tr><td>☐</td><td>나라·언어·이름을 <b>대문자</b>로 시작했나요?</td></tr>
    </tbody></table></div>
    <div class="table-wrap"><table>
      <thead><tr><th>자주 하는 실수 ✗</th><th>이렇게 ✓</th></tr></thead>
      <tbody lang="de">
        <tr><td>Ich aus Korea komme.</td><td>Ich <b>komme</b> aus Korea.</td></tr>
        <tr><td>Ich bin heiße Minjun.</td><td>Ich heiße Minjun.</td></tr>
        <tr><td>Ich wohnen in Seoul.</td><td>Ich wohn<b>e</b> in Seoul.</td></tr>
        <tr><td>Ich spreche koreanisch.</td><td>Ich spreche <b>K</b>oreanisch.</td></tr>
      </tbody>
    </table></div>
{ex("W1", "19d", "틀린 곳을 고쳐 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Ich wohnen in Seoul. → {blank("Ich wohne in Seoul.", "고친 문장", "full")}</li>
        <li>Ich aus Spanien komme. → {blank("Ich komme aus Spanien.", "고친 문장", "full")}</li>
        <li>Wie heiße du? → {blank("Wie heißt du?", "고친 문장", "full")}</li>
        <li>Er kommen aus Polen. → {blank("Er kommt aus Polen.", "고친 문장", "full")}</li>
        <li>Ich spreche englisch. → {blank("Ich spreche Englisch.", "고친 문장", "full")}</li>
        <li>Ich bin heiße Carlos. → {blank("Ich heiße Carlos.|Ich bin Carlos.", "고친 문장", "full")}</li>
      </ol>""")}
{tnote("<p class='box-title'>첨삭 기호</p><p><b>V</b> 동사 위치 · <b>E</b> 어미 · <b>G</b> 대·소문자 · <b>W</b> 단어 · <b>^</b> 빠진 말 · <b>✓</b> 잘 쓴 표현</p><p>1과는 기호만 표시하고 학생이 스스로 고치게 하세요. 채점(10점): 과제 수행 4 (4문장 모두) · 의사소통 2 (인사로 시작) · 정확성 4 (오류 0–1: 4 / 2–3: 3 / 4–5: 2 / 6+: 1).</p>")}''', "output")

s3 += act("s3-abschluss", "", "마무리", 5, '    <p><a href="#drei-bilder">3컷으로 이야기 다시 보기</a> → <a href="#tagebuch">민준의 일기</a> → <a href="#selbstcheck">자기 점검</a></p>', "output")
s3 += homework("hw-3", "3차시 숙제 (60분)", [
    ("<b>자기소개 글 깨끗하게 다시 쓰기</b> (5–6문장) – 제출하면 2과 첫 시간에 첨삭본을 돌려받아요", 10),
    ("<b>H3 · H3b · H3c</b> 소개 글 완성, 동사 형태, 나 → 그/그녀 바꾸기", 15),
    ("<b>H3d · H3e</b> 숫자 쓰기, 전화번호 받아쓰기", 10),
    ("<b>H3f · H3g</b> 수진 가족 소개 읽기, 틀린 문장 고치기", 10),
    (ic("search") + "<a href=\"#fallakte\"><b>사건 수첩</b></a> 채우기 + " + ic("mic") + "<b>1분 자기소개 녹음</b> 제출", 15)],
    ex("H3", "H3", "Lena를 소개하는 글을 완성하세요.", f"""      <p lang="de" class="template">Das {blank("ist", "sein")} Lena. Sie {blank("kommt", "kommen")} aus Hamburg. Sie {blank("wohnt", "wohnen")} jetzt in Leipzig, in einer WG. Sie {blank("spricht", "sprechen")} Deutsch und Englisch. Ihre Handynummer ist null – eins – sieben – {blank("sechs", "6", ci=True)} (6) …</p>""") + "\n" + ex("H3b", "H3b", "알맞은 형태를 쓰세요. 주어를 잘 보세요!", f"""      <ol lang="de">
        <li>Carlos {blank("ist", "sein")} Koch. (sein)</li>
        <li>Sie (당신) {blank("sind", "sein")} Lehrerin, oder? (sein)</li>
        <li>Priya {blank("spricht", "sprechen")} Hindi. (sprechen)</li>
        <li>Du {blank("sprichst", "sprechen")} gut Deutsch! (sprechen)</li>
        <li>Wie {blank("heißt", "heißen")} er? (heißen)</li>
        <li>Woher {blank("kommt", "kommen")} Frau Wagner? (kommen)</li>
        <li>Ich {blank("bin", "sein")} Student. (sein)</li>
        <li>Wo {blank("wohnt", "wohnen")} Jonas? (wohnen)</li>
      </ol>""") + "\n" + ex("H3c", "H3c", "‘나’ 문장을 ‘그/그녀’ 문장으로 바꾸세요.", f"""      <ol lang="de">
        <li>Carlos: „Ich wohne in Leipzig.“ → {blank("Er wohnt in Leipzig.", "문장", "full")}</li>
        <li>Priya: „Ich spreche Hindi.“ → {blank("Sie spricht Hindi.", "문장", "full")}</li>
        <li>Tomasz: „Ich bin Ingenieur.“ → {blank("Er ist Ingenieur.", "문장", "full")}</li>
        <li>Lena: „Ich komme aus Hamburg.“ → {blank("Sie kommt aus Hamburg.", "문장", "full")}</li>
        <li>Jonas: „Ich heiße Jonas Becker.“ → {blank("Er heißt Jonas Becker.", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H3d", "H3d", "숫자를 독일어로 쓰세요.", f"""      <ol lang="de">
        <li>0 → {blank("null", "0", ci=True)}</li>
        <li>6 → {blank("sechs", "6", ci=True)}</li>
        <li>13 → {blank("dreizehn", "13", ci=True)}</li>
        <li>15 → {blank("fünfzehn", "15", ci=True)}</li>
        <li>17 → {blank("siebzehn", "17", ci=True)}</li>
        <li>18 → {blank("achtzehn", "18", ci=True)}</li>
        <li>19 → {blank("neunzehn", "19", ci=True)}</li>
      </ol>""") + "\n" + ex("H3e", "H3e", "▶로 전화번호를 듣고 숫자로 쓰세요.", f"""      <ol lang="de">
        <li><span class="lis" data-say="null, eins, sieben, sechs, zwölf, neunzehn, drei."></span> {blank("0176 12 19 3", "번호", "wide", digits=True)}</li>
        <li><span class="lis" data-say="null, drei, vier, eins, achtzehn, null, sieben."></span> {blank("0341 18 0 7", "번호", "wide", digits=True)}</li>
        <li><span class="lis" data-say="null, vier, null, sechzehn, elf, zwanzig."></span> {blank("040 16 11 20", "번호", "wide", digits=True)}</li>
      </ol>""") + "\n" + ex("H3f", "H3f", "글을 읽고 질문에 답하세요.", f"""      <div class="box" lang="de"><p>Das ist Sujin Lee. Sie kommt aus Seoul. Sie wohnt jetzt in Leipzig, in der Kochstraße 12. Sie ist Krankenschwester. Sie spricht Koreanisch, Englisch und ein bisschen Deutsch. Das ist Haeun. Sie ist sechs. Sie spricht schon gut Deutsch!</p></div>
      <p class="muted">Krankenschwester = 간호사 · sechs (Jahre alt) = 여섯 살</p>
      <ol lang="de">
        <li>Woher kommt Sujin? – Aus {blank("Seoul", "도시")}.</li>
        <li>Wo wohnt Sujin jetzt? – In {blank("Leipzig|der Kochstraße 12|der Kochstraße", "곳", "wide")}.</li>
        <li>Was ist Sujin? – Sie ist {blank("Krankenschwester", "직업", "wide")}.</li>
        <li>Wie alt ist Haeun? – Sie ist {blank("sechs|6", "나이")}.</li>
        <li>Wer spricht gut Deutsch? – {blank("Haeun", "이름")}.</li>
      </ol>""") + "\n" + ex("H3g", "H3g", "틀린 곳을 고쳐 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Priya kommen aus Indien. → {blank("Priya kommt aus Indien.", "고친 문장", "full")}</li>
        <li>Er sprecht Polnisch. → {blank("Er spricht Polnisch.", "고친 문장", "full")}</li>
        <li>Das sind Lena. → {blank("Das ist Lena.", "고친 문장", "full")}</li>
        <li>Sie wohnst in Leipzig. → {blank("Sie wohnt in Leipzig.|Sie wohnen in Leipzig.", "고친 문장", "full")}</li>
        <li>Tomasz ist ein Ingenieur. → {blank("Tomasz ist Ingenieur.", "고친 문장", "full")}</li>
      </ol>"""))

# =====================================================================
# 부록
# =====================================================================
keys = [("Hallo! / Guten Tag!", "안녕! / 안녕하세요!"), ("Ich heiße Minjun. / Ich bin Minjun.", "내 이름은 민준이야."),
        ("Wie heißt du? / Wie heißen Sie?", "이름이 뭐야? / 성함이 어떻게 되세요?"), ("Woher kommst du? – Ich komme aus Südkorea.", "어디에서 왔어? – 한국에서 왔어."),
        ("Wo wohnst du? – Ich wohne in Leipzig.", "어디에 살아? – 라이프치히에 살아."), ("Sprichst du Deutsch? – Ja, ein bisschen.", "독일어 해? – 응, 조금."),
        ("Das ist Priya. Sie kommt aus Indien.", "이쪽은 프리야야. 인도에서 왔어."), ("Wie bitte? / Wie schreibt man das?", "뭐라고요? / 어떻게 써요?"),
        ("Wie ist deine Handynummer?", "네 휴대폰 번호가 뭐야?"), ("Tschüss! / Auf Wiedersehen!", "안녕! / 안녕히 계세요!")]
krows = "".join(f'<tr><td lang="de" data-say>{a}</td><td>{b}</td></tr>' for a, b in keys)

def vt(rows): return '<div class="table-wrap"><table><tbody>' + "".join(f'<tr><td lang="de" data-say>{a}</td><td>{b}</td></tr>' for a, b in rows) + "</tbody></table></div>"

anh = f'''  <section class="card" id="saetze">
    <h3>{ic("speak")}이번 과의 핵심 문장 10 · 말하기 카드</h3>
    <p>▶를 눌러 듣고, 한국어 뜻만 보고 독일어로 말할 수 있는지 확인해 보세요.</p>
    <div class="table-wrap"><table><tbody>{krows}</tbody></table></div>
  </section>

  <section class="card" id="grammatik">
    <h3>{ic("book")}<span lang="de">Grammatik</span> · 1과 문법 한눈에</h3>
    <div class="sum-grid">
      <div class="sum">
        <p class="sum-title">① 주어에 따라 바뀌는 동사</p>
        <div class="table-wrap"><table lang="de"><tbody>
          <tr><td>ich</td><td>-e</td><td>komme</td><td><b>bin</b></td></tr>
          <tr><td>du</td><td>-st</td><td>kommst</td><td><b>bist</b></td></tr>
          <tr><td>er / sie</td><td>-t</td><td>kommt</td><td><b>ist</b></td></tr>
          <tr><td>Sie</td><td>-en</td><td>kommen</td><td><b>sind</b></td></tr>
        </tbody></table></div>
        <p class="muted">조심: du/er spr<b>i</b>chst, spr<b>i</b>cht · du hei<b>ßt</b></p>
      </div>
      <div class="sum">
        <p class="sum-title">② 동사는 두 번째!</p>
{slots("S:Ich", "V:komme", "aus Korea.")}
{slots("Woher", "V:kommst", "S:du?")}
{slots("V:Kommst", "S:du", "aus Korea?")}
        <p class="muted">예/아니요 질문만 동사가 맨 앞</p>
      </div>
      <div class="sum">
        <p class="sum-title">③ 의문사</p>
        <p lang="de">Wer? 누구 · Wie? 어떻게 · Woher? 어디에서 → aus · Wo? 어디에 → in · Was? 무엇</p>
        <p class="sum-title">④ du와 Sie</p>
        <p>친구·가족·학생끼리 <b lang="de">du</b> / 어른·선생님·직원에게 <b lang="de">Sie</b> (대문자, 동사는 사전형과 같음)</p>
      </div>
    </div>
  </section>

  <section class="card" id="landeskunde">
    <h3>{ic("flag")}<span lang="de">Landeskunde</span> · 독일 생활 팁</h3>
    <ul>
      <li><b>인사는 지역마다 달라요.</b> 북독일(함부르크) <span lang="de">Moin!</span> · 남독일·오스트리아 <span lang="de">Grüß Gott!</span> · 스위스 <span lang="de">Grüezi!</span> – 그래서 Lena가 „Moin!“이라고 했어요.</li>
      <li><b>du와 Sie</b>: 대학생·WG에서는 처음부터 du가 많아요. 상대가 „<span lang="de">Wir können uns duzen.</span>“(말 놓아요)이라고 하면 du로! 나이 많은 이웃에게는 Sie가 안전해요.</li>
      <li><b>물건을 잃어버렸다면</b>: 역·기차에서는 Deutsche Bahn 분실물 센터, 시내에서는 시청의 <span lang="de">Fundbüro</span>로. 이름·연락처·물건의 색깔과 크기를 말해요.</li>
      <li><b>라이프치히</b>: 작센주에서 가장 큰 도시(인구 약 60만 명). 1409년에 세워진 라이프치히 대학, 1989년 평화 혁명의 중심지 <b>니콜라이 교회</b>(→ 5과에서 민준이 찾아가요).</li>
    </ul>
  </section>

  <section class="card" id="wortschatz">
    <h3>{ic("write")}<span lang="de">Wortschatz</span> · 단어장</h3>
    <div class="wgrid">
    <div>
    <h4>인사</h4>
    {vt([("Hallo! / Guten Morgen! / Guten Tag! / Guten Abend!", "안녕! / 좋은 아침 / 안녕하세요 / 좋은 저녁"), ("Tschüss! / Auf Wiedersehen!", "안녕(작별) / 안녕히 계세요·가세요"), ("Danke! / Entschuldigung! / Kein Problem.", "고마워요 / 죄송합니다 / 괜찮아요"), ("Wie geht's? – Gut, danke.", "잘 지내? – 좋아, 고마워."), ("Freut mich.", "반가워요.")])}
    </div>
    <div>
    <h4>동사</h4>
    {vt([("sein – ich bin, du bist, er/sie ist, Sie sind", "~이다"), ("heißen", "이름이 ~이다"), ("kommen (aus)", "(~에서) 오다"), ("wohnen (in)", "(~에) 살다"), ("sprechen – du sprichst, er/sie spricht", "말하다")])}
    </div>
    <div>
    <h4>나라와 언어</h4>
    {vt([("Südkorea – Koreanisch", "한국 – 한국어"), ("Deutschland – Deutsch", "독일 – 독일어"), ("Spanien – Spanisch", "스페인 – 스페인어"), ("Polen – Polnisch", "폴란드 – 폴란드어"), ("Indien – Hindi", "인도 – 힌디어"), ("England – Englisch", "영국 – 영어")])}
    </div>
    <div>
    <h4>가방 사건</h4>
    {vt([("der Koffer", "여행가방"), ("der Mantel", "외투"), ("das Foto", "사진"), ("der Brief", "편지"), ("die Tabletten", "약"), ("das Fundbüro", "분실물 센터"), ("schwarz · groß", "검은 · 큰")])}
    </div>
    </div>
  </section>

  <section class="card" id="drei-bilder">
    <h3>{ic("book")}이번 과 이야기 · 3컷으로 다시 보기</h3>
    <div class="strip">
      <figure class="cut"><img src="{IMG}story-1-bahnhof.webp" alt="중앙역에서 가방이 바뀌는 장면" loading="lazy"><figcaption><b>1</b> <span lang="de">Am Bahnhof: zwei schwarze Koffer.</span><span class="ko">역에서: 검은 가방 두 개.</span></figcaption></figure>
      <figure class="cut"><img src="{IMG}story-2-wg.webp" alt="WG에서 가방을 열어 보는 장면" loading="lazy"><figcaption><b>2</b> <span lang="de">In der WG: Das ist nicht mein Koffer!</span><span class="ko">WG에서: 이건 내 가방이 아니야!</span></figcaption></figure>
      <figure class="cut"><img src="{IMG}story-3-treppenhaus.webp" alt="계단에서 새 이웃을 만나는 장면" loading="lazy"><figcaption><b>3</b> <span lang="de">Im Treppenhaus: neue Nachbarn.</span><span class="ko">계단에서: 새 이웃.</span></figcaption></figure>
    </div>
    <p><b>말해 보기</b> 그림을 보며 혼자 이야기를 독일어로 말하고 녹음해 보세요. <span lang="de">(Minjun kommt aus … · Das ist nicht … · Das ist Sujin. Sie …)</span></p>
  </section>

  <section class="card" id="tagebuch">
    <h3>{ic("diary")}<span lang="de">Minjuns Tagebuch</span> · 민준의 일기 <button type="button" class="say-btn" data-play="diary-1" aria-label="일기 듣기">▶</button></h3>
    <div class="diary" lang="de" id="diary-1">
      <p class="date">30. September</p>
''' + "\n".join(f'      <p data-say-seq>{de}<span class="ko" lang="ko">{ko}</span></p>' for de, ko in [
    ("Ich bin in Leipzig! Aber das ist nicht mein Koffer!", "나는 라이프치히에 있다! 그런데 이건 내 가방이 아니다!"),
    ("Im Koffer sind ein Mantel, ein Foto und ein Brief.", "가방 안에는 외투, 사진, 편지가 있다."),
    ("Jonas sagt: „Das ist ein Fall für uns!“", "요나스가 말한다: “이건 우리가 풀 사건이야!”"),
    ("Im Haus wohnt jetzt eine Familie aus Korea: Sujin und Haeun.", "이 건물에 이제 한국에서 온 가족이 산다: 수진 씨와 하은이."),
    ("Unten wohnt Frau Schulze. Sie lacht nicht.", "아래층에는 슐체 할머니가 산다. 할머니는 웃지 않는다."),
    ("<b>Wer ist T. S.? Und wer ist E.?</b>", "T. S.는 누구일까? 그리고 E.는 누구일까?")]) + f'''
    </div>
    <p class="next">→ 다음 과 · <span lang="de">Kapitel 2: Meine WG, meine Familie</span><br><span class="muted">가방 속 물건을 하나씩 살펴보는 민준과 친구들. 그리고 수진 가족의 새집에서는 작은 손 하나가 테이블 위의 종이를 집어 드는데…</span></p>
  </section>

  <section class="card box mystery" id="fallakte">
    <h3>{ic("search")}<span lang="de">Fallakte</span> · 사건 수첩 <small>(이 기기에 자동 저장)</small></h3>
    <p>아는 것만 쓰세요. 모르는 칸은 비워 두세요 – 이야기가 진행되면서 채워져요!</p>
    <div class="table-wrap"><table lang="de"><tbody>
''' + "\n".join(f'      <tr><th>{a}<br><small lang="ko">{k}</small></th><td><input class="blank full" data-persist="{p}" aria-label="{k}"></td></tr>' for a, k, p in [
    ("Im Koffer sind …", "가방 안에는", "fall-inhalt"), ("Der Brief ist für …", "편지는 누구에게?", "fall-brief"),
    ("T. S. – der Mann heißt …", "남자의 이름은?", "fall-name"), ("Tel. 040 → Er kommt aus …", "어느 도시에서?", "fall-stadt"),
    ("Wer ist E.?", "E.는 누구?", "fall-e")]) + f'''
    </tbody></table></div>
    <p><b>나의 추리</b> (한국어도 좋아요)</p>
    <textarea data-persist="fall-idee" rows="3" aria-label="나의 추리"></textarea>
  </section>

  <section class="card" id="selbstcheck">
    <h3>{ic("check")}<span lang="de">Das kann ich!</span> · 자기 점검</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>할 수 있어요</th><th class="c">{pic("stimmung-1-sehr-gut", "잘해요", "mood-s")}</th><th class="c">{pic("stimmung-2-gut", "괜찮아요", "mood-s")}</th><th class="c">{pic("stimmung-4-nicht-so-gut", "연습 필요", "mood-s")}</th></tr></thead>
      <tbody>
''' + "\n".join(f'        <tr><td>{t}</td>' + "".join(f'<td class="c"><input type="radio" name="sc{i}" value="{v}" data-persist="sc{i}" aria-label="{l}"></td>' for v, l in [("3", "잘해요"), ("2", "괜찮아요"), ("1", "연습 필요")]) + "</tr>" for i, t in enumerate([
    "때에 맞게 인사하고 작별 인사를 할 수 있다.", "이름을 말하고 상대 이름을 물을 수 있다.", "내 이름 철자를 말할 수 있다.",
    "어디에서 왔는지, 어디에 사는지, 무슨 말을 하는지 말하고 물을 수 있다.", "친구에게는 du, 어른에게는 Sie로 물을 수 있다.",
    "다른 사람을 소개할 수 있다. (Das ist … Er/Sie kommt aus …)", "0–20 숫자와 전화번호를 말할 수 있다.", "4–5문장으로 나를 소개하는 글을 쓸 수 있다."], 1)) + '''
      </tbody>
    </table></div>
  </section>
'''


COVER = f'''<section class="book-cover" id="cover" data-panel="cover" data-nav="off">
  <div class="cover-sheet">
    <svg class="cover-art" viewBox="0 0 210 297" aria-hidden="true">
      <line x1="18" y1="171" x2="192" y2="171" stroke="#D9D6CE" stroke-width=".35"/>
      <path d="M53 104 v-6 a3 3 0 0 1 3 -3 h14 a3 3 0 0 1 3 3 v6" fill="none" stroke="#1F2A44" stroke-width="2.2"/>
      <rect x="38" y="104" width="50" height="64" rx="4" fill="#1F2A44"/>
      <line x1="50" y1="106" x2="50" y2="166" stroke="#33405e" stroke-width="1.2"/><line x1="76" y1="106" x2="76" y2="166" stroke="#33405e" stroke-width="1.2"/>
      <rect x="44" y="168" width="4" height="3" rx="1" fill="#1F2A44"/><rect x="78" y="168" width="4" height="3" rx="1" fill="#1F2A44"/>
      <path d="M115 104 v-6 a3 3 0 0 1 3 -3 h14 a3 3 0 0 1 3 3 v6" fill="none" stroke="#1F2A44" stroke-width="2.2"/>
      <rect x="100" y="104" width="50" height="64" rx="4" fill="#1F2A44"/>
      <line x1="112" y1="106" x2="112" y2="166" stroke="#33405e" stroke-width="1.2"/><line x1="138" y1="106" x2="138" y2="166" stroke="#33405e" stroke-width="1.2"/>
      <rect x="106" y="168" width="4" height="3" rx="1" fill="#1F2A44"/><rect x="140" y="168" width="4" height="3" rx="1" fill="#1F2A44"/>
      <path d="M134 97 C 146 99, 152 106, 156 114" fill="none" stroke="#ED1C24" stroke-width=".7"/>
      <g transform="rotate(14 160 124)">
        <rect x="151" y="113" width="18" height="24" rx="2" fill="#F3C811"/>
        <circle cx="160" cy="117" r="1.3" fill="#F6F4EF"/>
        <text x="160" y="129.5" text-anchor="middle" font-family="Inter Tight, sans-serif" font-weight="700" font-size="5" fill="#1F2A44">T.S.</text>
      </g>
    </svg>
    <div class="cover-top">
      <span class="cover-brand"><img src="../assets/img/brand/soda-logo.svg" alt="SODA 로고"><b>SODA</b><span>Sophia Deutsch Akademie</span></span>
      <span class="cover-level">Deutsch<strong>A1</strong></span>
    </div>
    <div class="cover-title">
      <h1 lang="de">Der falsche<br><span>Koffer</span></h1>
      <p class="cover-sub">바뀐 여행가방<i>/</i>이야기로 배우는 독일어</p>
      <a class="cover-start" href="#contents" data-tab="contents">시작하기 <span aria-hidden="true">→</span></a>
    </div>
    <div class="cover-foot"><span>CEFR A1 · Kapitel 1–8</span><span>Lehrwerk für koreanische Lernende</span></div>
  </div>
</section>
'''

A1_TOC = [("Hallo, ich bin Minjun!", "인사 · 이름과 철자 · 출신과 사는 곳 · 숫자 0–20", "역에서 가방이 바뀌다"),
          ("Meine WG, meine Familie", "집과 물건 · 가족 · der/die/das · 숫자 21–100", "가방 속 물건과 사라질 편지"),
          ("Im Supermarkt", "장보기 · 가격 · 4격 · möchten", "외투 주머니 속 영수증"),
          ("Mein Tag und meine Freizeit", "시간과 하루 일과 · 분리동사 · 약속", "분실물 센터의 전화"),
          ("Wo ist die Nikolaikirche?", "길 찾기 · 교통 · 명령법", "사진 속 교회를 찾아서"),
          ("Termine und Gesundheit", "예약 · 병원 · müssen / dürfen / sollen", "가방 속 약의 비밀"),
          ("Was trägt der Mann?", "옷 · 색깔 · 날씨 · 사람 묘사", "‘찾습니다’ 전단"),
          ("Endlich!", "지난 일 말하기 · 현재완료 · A1 마무리", "가방의 주인이 나타나다")]
toc_items = ""
for i, (t, k, story) in enumerate(A1_TOC, 1):
    inner = f'<span class="toc-no">{i:02d}</span><span class="toc-main"><b lang="de">{t}</b><span>{k}</span><small>{ic("search")}{story}</small></span>'
    if i == 1:
        toc_items += f'<li><a class="toc-ch" href="#kapitel-1" data-tab="start">{inner}<span class="toc-go">시작 →</span></a></li>'
    elif i == 2:
        toc_items += f'<li><a class="toc-ch" href="kapitel-02.html">{inner}<span class="toc-go">시작 →</span></a></li>'
    else:
        toc_items += f'<li><div class="toc-ch soon">{inner}<span class="toc-go">준비 중</span></div></li>'
CONTENTS = f'''<section id="contents" class="contents" data-panel="contents">
  <p class="series">DER FALSCHE KOFFER · A1</p>
  <h2 class="contents-title">목차 <span lang="de">Inhalt</span></h2>
  <p class="muted">시즌 1 · 이 가방은 누구 것일까? – 한 과는 3차시(1주)예요.</p>
  <ol class="toc-list">{toc_items}<li><div class="toc-ch soon"><span class="toc-no">{ic("check")}</span><span class="toc-main"><b lang="de">Modelltest</b><span>Start Deutsch 1 모의시험</span></span><span class="toc-go">준비 중</span></div></li></ol>
  <div class="seasons">
    <div><b>A2</b> 시즌 2 · 편지 속 E.는 누구일까?</div>
    <div><b>B1</b> 시즌 3 · 1984년에 무슨 일이 있었을까?</div>
    <div><b>B2</b> 시즌 4 · 누가 밀고했을까?</div>
  </div>
</section>
'''

# =====================================================================
# 페이지 조립
# =====================================================================
cast = "".join(f'<figure>{pic("person-" + k, n, "person")}<figcaption>{n}</figcaption></figure>' for k, n in [
    ("minjun", "민준"), ("jonas", "Jonas"), ("lena", "Lena"), ("wagner", "Frau Wagner"), ("carlos", "Carlos"), ("tomasz", "Tomasz"), ("priya", "Priya"), ("sujin", "수진"), ("haeun", "하은"), ("schulze", "Frau Schulze")])
goals = [("speak", "때에 맞게 인사하고 작별 인사를 할 수 있어요.", "Hallo! · Guten Tag! · Tschüss!"),
         ("abc", "내 이름을 말하고 철자로 알려 줄 수 있어요.", "Ich heiße … · P – A – R – K"),
         ("speak", "어디에서 왔는지, 어디에 사는지 말하고 물을 수 있어요.", "Woher kommst du? · Wo wohnst du?"),
         ("speak", "다른 사람을 소개할 수 있어요.", "Das ist Priya. Sie kommt aus Indien."),
         ("123", "0–20 숫자와 전화번호를 말할 수 있어요.", "null – eins – sieben – sechs"),
         ("write", "4–5문장으로 나를 소개하는 글을 쓸 수 있어요.", "Ich heiße … Ich komme aus …")]
gcards = "".join(f'<div class="goal">{ic(i)}<div><p class="goal-ko">{k}</p><p class="goal-de" lang="de">{d}</p></div></div>' for i, k, d in goals)
plans = [("stunde-1", "1차시", "Hallo! Ich bin Minjun.", "인사 · 인사 듣기 · Teil A 역에서 · ich/du", "알파벳 · 이름 철자·명함 · 수업 독일어 · 첫 대화"),
         ("stunde-2", "2차시", "Woher kommst du?", "Teil B WG에서 · 나라와 언어 · 출신 듣기 · 동사 2번째", "Teil C du/Sie · 분실물 센터 · 인터뷰 · 등록 신청서"),
         ("stunde-3", "3차시", "Wer ist das?", "Teil D 반 친구 소개 · er/sie · 소개 듣기 · 숫자", "읽기 · 중개하기 · 다른 사람 소개 · 자기소개 쓰기")]
grams = [("인칭대명사", "ich · du · er / sie · Sie", "나 · 너 · 그/그녀 · 당신", "s1-satz1", "1차시"),
         ("sein 동사 (~이다)", "ich bin · du bist · er/sie ist · Sie sind", "모양이 불규칙 – 통째로 외우기", "s1-satz1", "1·3차시"),
         ("동사 현재형 어미", "ich komm<b>e</b> · du komm<b>st</b> · er komm<b>t</b> · Sie komm<b>en</b>", "kommen · wohnen · heißen", "s2-satz2", "2·3차시"),
         ("모음이 바뀌는 동사", "sprechen → du spr<b>i</b>chst · er spr<b>i</b>cht", "e → i", "s2-satz2", "2·3차시"),
         ("동사는 두 번째 자리", "Ich <b>komme</b> aus Südkorea. · Woher <b>kommst</b> du?", "평서문 · 의문사 질문", "s2-satz2", "2차시"),
         ("예/아니요 질문", "<b>Bist</b> du Jonas? · <b>Sprichst</b> du Deutsch?", "동사가 맨 앞", "s1-satz1", "1·2차시"),
         ("의문사와 전치사", "Wie? · Woher? → aus · Wo? → in", "어떻게 · 어디에서 · 어디에", "s2-satz2", "2차시"),
         ("du와 Sie", "Wie heißt du? · Wie heißen Sie? · Herr / Frau + 성", "반말과 존댓말", "s2-du-sie", "2차시"),
         ("대문자 쓰기", "Koreanisch · Deutschland · Sie", "나라·언어·명사·존댓말 Sie", "s2-laender", "2차시")]
grc = "".join(f'<a class="gram-row" href="#{a}"><span class="gram-no">{i}</span><b>{n}</b><span class="gram-ex" lang="de">{ex}</span><span class="gram-note">{note}</span><span class="gram-where">{w}</span></a>' for i, (n, ex, note, a, w) in enumerate(grams, 1))
pc = "".join(f'<a class="plan" href="#{i}"><span class="stunde-no">{n}</span><b lang="de">{t}</b><span><small>1교시</small> {x}</span><span><small>2교시</small> {y}</span></a>' for i, n, t, x, y in plans)

plan1 = "<p>1교시: 그림 5′ → 인사말 15′ → Teil A 15′ → 문장 틀 ① 15′ · 2교시: 알파벳·발음 20′ → 이름 철자 15′ → 첫 만남 대화 15′</p><p><b>원칙</b>: 소리 먼저. 1교시에는 쓰기보다 <b>듣고 따라 말하기</b>를 충분히. 한글 발음 도우미는 처음에만 켜고, 학생이 소리에 익숙해지면 끄게 하세요.</p>"
plan2 = "<p>1교시: 복습 5′ → Teil B 15′ → 나라와 언어 10′ → 문장 틀 ② 20′ · 2교시: Teil C du/Sie 15′ → 분실물 센터 20′ → 인터뷰 15′</p><p><b>준비물</b>: 문장 카드(동사 카드는 빨간색) · (선택) 검은 가방과 외투·흑백 사진·봉투·이름표 소품</p>"
plan3 = "<p>1교시: 복습 5′ → Teil D 10′ → 문장 틀 ③ 15′ → 숫자·전화번호 20′ · 2교시: 읽기 15′ → 중개하기 10′ → 쓰기 20′ → 마무리 5′</p><p><b>다음 과 첫 10분</b>: 첨삭한 자기소개 돌려주기 → 반 전체 공통 오류 3개 함께 고치기</p>"

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kapitel 1 · Hallo, ich bin Minjun!</title>
<meta name="description" content="Der falsche Koffer – 독일어를 처음 배우는 학생을 위한 CEFR A1 통합형 교재 1과">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/textbook.css">
</head>
<body data-chapter="A1-01" data-level="A1">
<!-- icons:start -->{SPRITE}<!-- icons:end -->
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="#cover" data-tab="cover">{ic("suitcase")} <span class="lbl">Der falsche Koffer</span></a>
    <nav aria-label="차시 이동">
      <a href="#contents" data-tab="contents">목차</a><a href="#kapitel-1" data-tab="start">목표</a><a href="#stunde-1" data-tab="stunde-1">1차시</a><a href="#stunde-2" data-tab="stunde-2">2차시</a><a href="#stunde-3" data-tab="stunde-3">3차시</a><a href="#anhang" data-tab="anhang">부록</a>
    </nav>
    <button type="button" class="toggle" id="theme-toggle" aria-label="화면 테마">◐ <span class="lbl">자동</span></button>
  </div>
</header>

{COVER}
<div class="page">
<main>

{CONTENTS}

<section class="hero" id="kapitel-1" data-panel="start">
  <div class="series">DER FALSCHE KOFFER · A1 · KAPITEL 1 · 독일어 첫걸음</div>
  <h1 lang="de">Hallo, ich bin Minjun!</h1>
  <div class="meta">
    <div><b>이야기</b> 9월 말, 한국인 유학생 민준이 독일 라이프치히에 도착해요. 그런데 역에서 가방이 바뀌는데…</div>
    <div><b>수업</b> 3차시(1주) · 1차시 = 1교시 50분 + 2교시 50분 · 차시마다 숙제 60분</div>
  </div>
  <div class="cast" aria-label="등장인물">{cast}</div>
{tnote('<p class="box-title">' + ic("teacher") + '교사 모드 안내</p><p>초록 상자는 운영 팁·대본·스포일러입니다. 활동 제목 옆 시간 배지를 누르면 타이머가 시작됩니다.</p><p><b>1과 설계 원칙</b>: ① 소리 먼저, 글자 나중 ② 주어를 하나씩 늘리기: ich/du(1차시) → Sie(2차시) → er/sie(3차시), wir/ihr는 2과 ③ 문장 덩어리 먼저, 규칙은 짧게 ④ 쉬운 연습부터: 고르기 → 빈칸 → 틀에 맞춰 쓰기</p>')}
</section>

<section id="ziele" class="card" data-panel="start">
  <h2>{ic("target")}이번 과가 끝나면</h2>
  <div class="goal-grid">{gcards}</div>
  <h3>{ic("book")}이번 과에서 배우는 문법</h3>
  <div class="gram-list">{grc}</div>
  <h3>이번 주 수업 · 3차시</h3>
  <div class="plan-grid">{pc}</div>
</section>

{stunde("stunde-1", "1", "Hallo! Ich bin Minjun.", plan1, s1)}
{stunde("stunde-2", "2", "Woher kommst du?", plan2, s2)}
{stunde("stunde-3", "3", "Wer ist das?", plan3, s3)}
<section id="anhang" class="stunde" data-panel="anhang">
  <div class="stunde-head"><span class="stunde-no">부록</span><h2>복습과 숙제용</h2></div>
{anh}
</section>

</main>
</div>

<footer>
  Der falsche Koffer · A1 Kapitel 1 · CEFR 기반 통합형 독일어 교재 · 등장인물과 병원·회사는 가상이며, 역사적 사실과 장소는 실제에 맞춰 서술합니다.
</footer>

<script src="../assets/js/textbook.js"></script>
</body>
</html>
'''
# ---- 녹음 파일 연결 (ElevenLabs eleven_v4로 만든 assets/audio/k01/*.mp3) ----
import os as _os
AUD = "../assets/audio/k01/"
_AUD_DIR = "/home/user/CFER/web/assets/audio/k01/"
def _attach_audio(h):
    def dlg(m):
        did, n = m.group(1), [0]
        def ln(mm):
            n[0] += 1
            fn = f"{did}-{n[0]}.mp3"
            return mm.group(0) + (f' data-audio="{AUD}{fn}"' if _os.path.exists(_AUD_DIR + fn) else "")
        return re.sub(r'<span class="text"', ln, m.group(0))
    h = re.sub(r'<div class="dialog[^"]*" id="([^"]+)".*?\n    </div>', dlg, h, flags=re.S)
    k = [0]
    def lis(m):
        k[0] += 1
        fn = f"lis-{k[0]}.mp3"
        return m.group(0)[:-1] + (f' data-audio="{AUD}{fn}"' if _os.path.exists(_AUD_DIR + fn) else "") + ">"
    h = re.sub(r'<span class="lis" data-say="[^"]+">', lis, h)
    # 민준이 직접 하는 문장(문장 틀·예문)은 민준 목소리 녹음으로
    for txt, fn in [("Hallo! Ich heiße Minjun. Ich komme aus Südkorea. Ich wohne in Leipzig.", "say-minjun-1.mp3"),
                    ("Ich bin Minjun.", "say-minjun-2.mp3"), ("Ich heiße Minjun.", "say-minjun-3.mp3"),
                    ("Ich heiße Minjun. / Ich bin Minjun.", "say-minjun-4.mp3")]:
        h = h.replace(f' data-say>{txt}<', f' data-say data-audio="{AUD}{fn}">{txt}<')
    return h
open(OUT, "w", encoding="utf-8").write(_attach_audio(page))
print("written", len(page))
