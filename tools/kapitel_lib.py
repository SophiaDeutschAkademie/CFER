# 교재 HTML 생성 공용 함수 (1과 gen_k01.py에서 나눔)
# 챕터 생성기에서: import kapitel_lib as K; K.IMG = "../assets/img/k02/"
import re, html
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "../assets/img/k01/"     # 챕터 그림 폴더 (챕터마다 바꿈)
PIMG = "../assets/img/"         # 인물 그림은 k01/person-*, k02/person-* 등 어디서든
SPRITE = open(ROOT + "/web/assets/icons/icons.svg", encoding="utf-8").read()
keep_navy = {"i-123", "i-mediate", "i-abc"}
def _rc(m):
    sym = m.group(0); sid = re.search(r'id="([^"]+)"', sym).group(1)
    return sym if sid in keep_navy else sym.replace("#2E3A55", "currentColor")
SPRITE = re.sub(r"<symbol.*?</symbol>", _rc, SPRITE, flags=re.S)
SPRITE = re.sub(r"<!--.*?-->", "", SPRITE).replace('style="display:none">', 'style="display:none" aria-hidden="true">').strip()

def ic(n): return f'<svg class="ic" aria-hidden="true"><use href="#i-{n}"/></svg>'
def src(n): return (PIMG + n if "/" in n else IMG + n) + ".webp"
def pic(n, alt="", cls="pic"): return f'<img class="{cls}" src="{src(n)}" alt="{alt}" loading="lazy">'
def fig(n, alt, cap=""): return f'<figure class="scene"><img src="{src(n)}" alt="{alt}" loading="lazy">' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def g(x, c): return f'<b class="g-{c}">{x}</b>'
AV = {"Minjun": "k01/person-minjun", "민준": "k01/person-minjun", "Jonas": "k01/person-jonas", "Lena": "k01/person-lena",
      "Frau Wagner": "k01/person-wagner", "Carlos": "k01/person-carlos", "Tomasz": "k01/person-tomasz", "Priya": "k01/person-priya",
      "수진": "k01/person-sujin", "Sujin": "k01/person-sujin", "하은": "k01/person-haeun", "Haeun": "k01/person-haeun", "Frau Schulze": "k01/person-schulze"}

def line(who, de, ko="", lang="de"):
    av = f'<span class="avatar" style="background-image:url({src(AV[who])})" aria-hidden="true"></span>' if who in AV else ""
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
