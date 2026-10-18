# 2과 HTML 생성 · Meine WG, meine Familie
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kapitel_lib as K
from kapitel_lib import *
K.IMG = "../assets/img/k02/"
K.AV.update({"Amira": "k02/person-amira", "Oksana": "k02/person-oksana", "Herr Brandt": "k02/person-brandt",
             "태호": "k02/person-taeho", "Taeho": "k02/person-taeho", "도윤": "k02/person-doyun"})
OUT = "/home/user/CFER/web/A1/kapitel-02.html"

def art(a, w):   # 관사 색: der 파랑 · die 빨강 · das 초록 · 복수 die 갈색
    c = {"der": "m", "die": "f", "das": "n", "pl": "p"}[a]
    return f'{g("die" if a == "pl" else a, c)} {w}'

# =====================================================================
# 1차시 · Das ist mein Zimmer.
# =====================================================================
moebel = [("bett", "das", "Bett", "침대"), ("tisch", "der", "Tisch", "탁자, 책상"), ("stuhl", "der", "Stuhl", "의자"),
          ("schrank", "der", "Schrank", "옷장"), ("lampe", "die", "Lampe", "전등"), ("regal", "das", "Regal", "선반, 책장"),
          ("schreibtisch", "der", "Schreibtisch", "책상"), ("sofa", "das", "Sofa", "소파"), ("teppich", "der", "Teppich", "양탄자"),
          ("spiegel", "der", "Spiegel", "거울")]
mcards = "".join(f'<figure class="kitem">{pic("moebel-" + k, w, "kitem-img")}<figcaption><span class="kword" lang="de" data-say="{a} {w}">{art(a, w)}</span><span class="ko">{ko}</span></figcaption></figure>' for k, a, w, ko in moebel)
aopts = ["der", "die", "das"]

s1 = block("1교시 · 50분 · Input")
s1 += act("s1-einstieg", 1, "Einstieg · 민준의 새 방", 5, f'''    {fig("story-1-zimmer", "오래된 집의 거의 빈 방에서 요나스가 침대와 낡은 옷장을 가리키고, 민준이 놀란 얼굴로 둘러본다", "WG에 온 다음 날, 요나스가 민준에게 방을 보여 줘요.")}
    <p><b>1a</b> 그림을 보세요. 방에 무엇이 있어요? 무엇이 <b>없어요</b>? 한국어로 말해 보세요.</p>
    <p><b>1b</b> 이번 과가 끝나면 이런 말을 할 수 있어요. 들어 보세요!</p>
    <p class="box" lang="de" data-say>Mein Zimmer ist klein, aber hell. Ich habe ein Bett und einen Schrank. Das ist meine Familie: meine Mutter, mein Vater und meine Schwester.</p>
    <p class="ko">내 방은 작지만 밝아요. 침대 하나와 옷장 하나가 있어요. 이건 우리 가족이에요: 엄마, 아빠, 그리고 누나(언니)예요.</p>''')

s1 += act("s1-moebel", 2, "<span lang=\"de\">Im Zimmer</span> · 방 안의 물건", 10, f'''    <p>▶를 눌러 듣고 따라 하세요. 단어는 언제나 <b>관사와 함께</b> 외워요. 색깔을 보세요!</p>
    <div class="koffer-items">{mcards}</div>
{gram("der · die · das – 명사에는 성이 있어요", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th>남성</th><th>여성</th><th>중성</th><th>복수</th></tr></thead>
        <tbody lang="de"><tr><th lang="ko">정관사 (그)</th><td>{g("der", "m")} Tisch</td><td>{g("die", "f")} Lampe</td><td>{g("das", "n")} Bett</td><td>{g("die", "p")} Stühle</td></tr></tbody>
      </table></div>
      <p>사람은 대개 자연의 성을 따라요(<span lang="de">der Mann, die Frau</span>). 물건은 <b>규칙이 거의 없어서</b> 관사와 함께 통째로 외워요.</p>
      <p>작은 힌트: <b>-e</b>로 끝나면 대부분 <span lang="de">die</span>(<span lang="de">die Lampe, die Tasche</span>) · 복수는 언제나 <span lang="de">die</span>.</p>""")}
{ex("M1", "2a", "관사를 고르세요. 그림을 보지 말고!", f"""      <ol lang="de">
        <li>{sel("das", aopts)} Bett</li>
        <li>{sel("der", aopts)} Stuhl</li>
        <li>{sel("die", aopts)} Lampe</li>
        <li>{sel("der", aopts)} Schrank</li>
        <li>{sel("das", aopts)} Sofa</li>
        <li>{sel("der", aopts)} Spiegel</li>
        <li>{sel("das", aopts)} Regal</li>
        <li>{sel("der", aopts)} Teppich</li>
      </ol>""")}''')

s1 += act("s1-teil-a", 3, "Teil A · <span lang=\"de\">Das ist dein Zimmer!</span> · 방 구경", 15, f'''{track("2-01", "dlg-2-01", "WG에 온 다음 날 아침, 요나스가 민준의 방 문을 열어요.")}
{dialog("dlg-2-01", [
    line("Jonas", "So, Minjun, das ist dein Zimmer!", "자, 민준, 여기가 네 방이야!"),
    line("Minjun", "Oh, das Zimmer ist groß. Und hell!", "오, 방이 크다. 그리고 밝아!"),
    line("Jonas", "Ja. Hier ist das Bett, und das ist der Schrank.", "응. 여기 침대가 있고, 이건 옷장이야."),
    line("Minjun", "Der Schrank ist sehr alt.", "옷장이 아주 오래됐네."),
    line("Jonas", "Ja, aber er ist schön, oder?", "응, 그래도 예쁘지?"),
    line("Minjun", "Hm … Und wo ist der Tisch?", "음… 그런데 탁자는 어디 있어?"),
    line("Jonas", "Ein Tisch? Hier ist kein Tisch.", "탁자? 여기엔 탁자가 없어."),
    line("Minjun", "Und ein Stuhl?", "그럼 의자는?"),
    line("Jonas", "Auch kein Stuhl. Sorry! Aber die Lampe ist neu!", "의자도 없어. 미안! 그래도 전등은 새 거야!"),
    line("Minjun", "Super … Ein Zimmer ohne Tisch und ohne Stuhl!", "대단하다… 탁자도 의자도 없는 방이라니!")])}
{ex("A1", "3a", "대화를 듣고, 맞으면 <b>r</b>, 틀리면 <b>f</b>. 해석 없이!", rf("a1", [
    ("Das Zimmer ist klein und dunkel.", "f", ""),
    ("Im Zimmer ist ein Bett.", "r", ""),
    ("Der Schrank ist neu.", "f", ""),
    ("Jonas findet den Schrank schön.", "r", "finden = ~라고 생각하다"),
    ("Im Zimmer sind ein Tisch und ein Stuhl.", "f", ""),
    ("Die Lampe ist neu.", "r", "")]))}
{ex("A2", "3b", "다시 듣고 빈칸을 쓰세요.", f"""      <ol lang="de">
        <li>So, Minjun, das ist {blank("dein", "말")} Zimmer!</li>
        <li>Hier ist {blank("das", "관사")} Bett, und das ist {blank("der", "관사")} Schrank.</li>
        <li>Ja, aber {blank("er", "대명사")} ist schön, oder?</li>
        <li>Hier ist {blank("kein", "말")} Tisch.</li>
      </ol>""")}''')

s1 += act("s1-satz1", 4, "오늘의 문장 틀 ① · 이건 ○○예요 / ○○이 아니에요", 20, f'''{today([
    ("Das ist ein Tisch.", "", "이건 탁자예요."),
    ("Das ist eine Lampe.", "", "이건 전등이에요."),
    ("Das ist kein Stuhl.", "", "이건 의자가 아니에요."),
    ("Der Tisch ist neu.", "", "그 탁자는 새것이에요."),
    ("Wie heißt das auf Deutsch?", "", "이건 독일어로 뭐라고 해요?")])}
{gram("ein · eine – 처음 말할 때 / der · die · das – 이미 아는 것", f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th>남성</th><th>여성</th><th>중성</th><th>복수</th></tr></thead>
        <tbody lang="de">
          <tr><th lang="ko">정관사 (그)</th><td>{g("der", "m")}</td><td>{g("die", "f")}</td><td>{g("das", "n")}</td><td>{g("die", "p")}</td></tr>
          <tr><th lang="ko">부정관사 (하나의)</th><td>{g("ein", "m")}</td><td>{g("eine", "f")}</td><td>{g("ein", "n")}</td><td>–</td></tr>
          <tr><th lang="ko">부정 (없는)</th><td>{g("kein", "m")}</td><td>{g("keine", "f")}</td><td>{g("kein", "n")}</td><td>{g("keine", "p")}</td></tr>
        </tbody>
      </table></div>
      <p lang="de">Das ist <b>ein</b> Schrank. <b>Der</b> Schrank ist alt. <span class="muted" lang="ko">– 처음엔 ein, 다시 말할 땐 der</span></p>
      <p><b lang="de">kein</b>은 <span lang="de">ein</span> 앞에 k만 붙인 것! 명사를 부정할 땐 <b lang="de">kein</b>, 나머지는 <b lang="de">nicht</b>: <span lang="de">Das ist <b>kein</b> Stuhl.</span> · <span lang="de">Der Stuhl ist <b>nicht</b> neu.</span></p>""")}
{ex("G1", "4a", "ein일까요, eine일까요?", f"""      <ol lang="de">
        <li>Das ist {sel("ein", ["ein", "eine"])} Bett.</li>
        <li>Das ist {sel("eine", ["ein", "eine"])} Lampe.</li>
        <li>Das ist {sel("ein", ["ein", "eine"])} Spiegel.</li>
        <li>Das ist {sel("eine", ["ein", "eine"])} Tasche.</li>
        <li>Das ist {sel("ein", ["ein", "eine"])} Regal.</li>
      </ol>""")}
{ex("G2", "4b", "처음엔 ein/eine, 두 번째엔 der/die/das. 빈칸 두 개를 모두 쓰세요.", f"""      <ol lang="de">
        <li>Das ist {blank("ein", "관사")} Schrank. {blank("Der", "관사")} Schrank ist alt.</li>
        <li>Das ist {blank("eine", "관사")} Lampe. {blank("Die", "관사")} Lampe ist neu.</li>
        <li>Das ist {blank("ein", "관사")} Sofa. {blank("Das", "관사")} Sofa ist bequem.</li>
        <li>Das ist {blank("ein", "관사")} Teppich. {blank("Der", "관사")} Teppich ist schön.</li>
      </ol>
      <p class="muted">bequem = 편안한</p>""")}
{ex("G3", "4c", "아니에요! kein / keine로 바꿔 쓰세요.", f"""      <ol lang="de">
        <li>Ist das ein Stuhl? – Nein, das ist {blank("kein", "부정")} Stuhl.</li>
        <li>Ist das eine Lampe? – Nein, das ist {blank("keine", "부정")} Lampe.</li>
        <li>Ist das ein Bett? – Nein, das ist {blank("kein", "부정")} Bett. Das ist ein Sofa.</li>
        <li>Ist der Tisch neu? – Nein, der Tisch ist {blank("nicht", "부정")} neu.</li>
      </ol>""")}''')

adj = [("groß", "큰"), ("klein", "작은"), ("alt", "낡은, 오래된"), ("neu", "새로운"), ("hell", "밝은"), ("dunkel", "어두운"),
       ("schön", "예쁜"), ("hässlich", "못생긴"), ("teuer", "비싼"), ("billig", "싼"), ("bequem", "편안한"), ("modern", "현대적인")]
s1 += block("2교시 · 50분 · Output")
s1 += act("s1-adjektive", 5, "<span lang=\"de\">Wie ist das Zimmer?</span> · 방과 물건 설명하기", 15, f'''    <p>짝이 되는 말로 외워요. ▶를 눌러 들어 보세요.</p>
    <div class="vocab" lang="de">{"".join(f'<div><b data-say>{a}</b><span class="ko" lang="ko">{k}</span></div>' for a, k in adj)}</div>
{gram("명사 + ist + 형용사 – 형용사는 모양이 안 바뀌어요", f"""{slots("S:Der Tisch", "V:ist", "neu.")}
{slots("S:Die Lampe", "V:ist", "neu.")}
{slots("S:Die Stühle", "V:sind", "neu.")}
      <p><b lang="de">ist / sind</b> 뒤에 오는 형용사는 남성·여성·복수 모두 <b>같은 모양</b>이에요. 정도를 더하려면 <b lang="de">sehr</b>(아주) · <b lang="de">zu</b>(너무): <span lang="de">Das Zimmer ist <b>zu</b> klein.</span></p>
      <p>대명사로 받을 때: <span lang="de">der Tisch → <b>er</b> · die Lampe → <b>sie</b> · das Bett → <b>es</b> · die Stühle → <b>sie</b></span></p>""")}
{ex("D1", "5a", "반대말을 쓰세요.", f"""      <ol lang="de">
        <li>groß ↔ {blank("klein", "반대말")}</li>
        <li>alt ↔ {blank("neu", "반대말")}</li>
        <li>hell ↔ {blank("dunkel", "반대말")}</li>
        <li>teuer ↔ {blank("billig", "반대말")}</li>
        <li>schön ↔ {blank("hässlich", "반대말")}</li>
      </ol>""")}
{ex("D2", "5b", "알맞은 대명사(er · sie · es)를 고르세요.", f"""      <ol lang="de">
        <li>Der Schrank ist alt, aber {sel("er", ["er", "sie", "es"])} ist schön.</li>
        <li>Die Lampe ist neu. {sel("Sie", ["Er", "Sie", "Es"])} ist modern.</li>
        <li>Das Bett ist klein. {sel("Es", ["Er", "Sie", "Es"])} ist nicht bequem.</li>
        <li>Wie ist der Teppich? – {sel("Er", ["Er", "Sie", "Es"])} ist zu teuer!</li>
        <li>Wie sind die Stühle? – {sel("Sie", ["Er", "Sie", "Es"])} sind billig.</li>
      </ol>""")}''', "output")

s1 += act("s1-anzeige", 6, "<span lang=\"de\">Lesen</span> · WG-Zimmer 광고 읽기", 15, f'''    <p>Lena의 친구 Paul이 WG 방을 광고했어요. 읽고 문제를 푸세요.</p>
    <div class="form-card" lang="de">
      <p class="form-card-title">WG-Zimmer frei! · Leipzig-Südvorstadt</p>
      <p>Hallo! Das Zimmer ist 16 m² groß und sehr hell. Das Bett und der Schreibtisch sind neu. Ein Schrank ist auch da, aber er ist alt. Die Küche ist groß, das Bad ist klein. Wir sind drei Studenten: Paul, Mia und Ben. Wir sind nett und ruhig!</p>
      <p>Miete: 380 € · Tel. 0176 / 55 20 31</p>
    </div>
    <p class="muted">m² = Quadratmeter · die Küche = 부엌 · das Bad = 욕실 · nett = 친절한 · ruhig = 조용한 · die Miete = 월세</p>
{ex("L1", "6a", "맞으면 <b>r</b>, 틀리면 <b>f</b>", rf("l1", [
    ("Das Zimmer ist dunkel.", "f", ""),
    ("Der Schreibtisch ist neu.", "r", ""),
    ("Im Zimmer ist kein Schrank.", "f", ""),
    ("Das Bad ist groß.", "f", ""),
    ("In der WG wohnen drei Studenten.", "r", ""),
    ("Paul, Mia und Ben sind laut.", "f", "laut = 시끄러운")]))}
{ex("L2", "6b", "광고를 보고 답하세요.", f"""      <ol lang="de">
        <li>Wie ist das Zimmer? – Es ist {blank("hell|sehr hell", "형용사", "wide")}.</li>
        <li>Was ist alt? – Der {blank("Schrank", "명사")}.</li>
        <li>Wie ist die Küche? – Sie ist {blank("groß", "형용사")}.</li>
        <li>Wie heißen die Studenten? – Paul, Mia und {blank("Ben", "이름")}.</li>
      </ol>""")}''', "output")

s1 += act("s1-auf-deutsch", 7, "<span lang=\"de\">Wie heißt das auf Deutsch?</span> · 모르는 단어 묻기", 10, f'''{today([
    ("Wie heißt das auf Deutsch?", "", "이건 독일어로 뭐라고 해요?"),
    ("Das heißt „Spiegel“.", "", "그건 „Spiegel“이라고 해요."),
    ("Ist das der oder das Spiegel?", "", "Spiegel은 der예요, das예요?"),
    ("Was heißt „hell“ auf Koreanisch?", "", "„hell“이 한국어로 뭐예요?")], "단어를 물을 때")}
{ex("W1", "7a", "질문을 완성하세요.", f"""      <ol lang="de">
        <li>{blank("Wie", "의문사")} heißt das auf Deutsch? – Das heißt „Teppich“.</li>
        <li>Was {blank("heißt", "동사")} „Lampe“ auf Koreanisch? – 전등.</li>
        <li>Ist das {blank("der", "관사")} oder das Schrank? – Der Schrank.</li>
      </ol>""")}
    <p><b>7b</b> 혼자 말하기 · 지금 있는 방을 둘러보고 물건 3개를 독일어로 말해 보세요. 모르는 단어는 사전에서 찾아 <span lang="de">der/die/das</span>와 함께 공책에 쓰세요.</p>''', "output")

s1 += act("s1-sprechen", 8, "<span lang=\"de\">Sprechen</span> · 내 방 소개하기", 10, f'''    <p>휴대폰으로 내 방을 찍는다고 생각하고, 녹음하며 소개해 보세요. 아래 틀을 써도 좋아요.</p>
    <p lang="de" class="template">Das ist mein Zimmer. Es ist … und … . Hier ist ein/eine … . Der/Die/Das … ist … . Hier ist kein/keine … .</p>
{ex("S1", "8a", "민준의 방 메시지를 완성하세요.", f"""      <p lang="de" class="template">Hallo Mama! Das ist mein Zimmer. Es ist groß und {blank("hell", "형용사")}. Hier ist {blank("ein", "관사")} Bett. {blank("Der", "관사")} Schrank ist alt. Aber hier ist {blank("kein", "부정")} Tisch und {blank("kein", "부정")} Stuhl!</p>""")}''', "output")

s1 += homework("hw-1", "1차시 숙제 (60분)", [
    ("가구 카드 10개를 관사와 함께 듣고 따라 하기 + 공책에 색깔 펜으로 쓰기", 10),
    ("<b>H1 · H2</b> 관사 고르기, ein ↔ der 바꾸기", 15),
    ("<b>H3 · H4</b> kein/nicht, 형용사와 대명사", 15),
    ("<b>H5 · H6</b> 틀린 문장 고치기, 반대말", 10),
    ("<b>H7</b> 읽기 – 방 광고", 5),
    (ic("mic") + "<b>녹음</b>: 내 방을 5문장으로 소개해서 제출", 5)],
    ex("H1", "H1", "관사를 쓰세요. (der · die · das)", f"""      <ol lang="de">
        <li>{blank("der", "관사", ci=True)} Tisch</li>
        <li>{blank("die", "관사", ci=True)} Lampe</li>
        <li>{blank("das", "관사", ci=True)} Bett</li>
        <li>{blank("der", "관사", ci=True)} Spiegel</li>
        <li>{blank("das", "관사", ci=True)} Zimmer</li>
        <li>{blank("die", "관사", ci=True)} Küche</li>
        <li>{blank("das", "관사", ci=True)} Bad</li>
        <li>{blank("der", "관사", ci=True)} Koffer</li>
      </ol>""") + "\n" + ex("H2", "H2", "문장 두 개로 쓰세요. (ein → der)", f"""      <ol lang="de">
        <li>Lampe / neu → Das ist eine Lampe. {blank("Die Lampe ist neu.", "문장", "full")}</li>
        <li>Bett / klein → Das ist ein Bett. {blank("Das Bett ist klein.", "문장", "full")}</li>
        <li>Spiegel / alt → Das ist ein Spiegel. {blank("Der Spiegel ist alt.", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H3", "H3", "kein / keine / nicht 중에서 고르세요.", f"""      <ol lang="de">
        <li>Das ist {sel("kein", ["kein", "keine", "nicht"])} Sofa.</li>
        <li>Das Zimmer ist {sel("nicht", ["kein", "keine", "nicht"])} groß.</li>
        <li>Hier ist {sel("keine", ["kein", "keine", "nicht"])} Lampe.</li>
        <li>Der Schrank ist {sel("nicht", ["kein", "keine", "nicht"])} neu.</li>
        <li>Das ist {sel("kein", ["kein", "keine", "nicht"])} Teppich.</li>
      </ol>""") + "\n" + ex("H4", "H4", "대명사로 바꿔 쓰세요.", f"""      <ol lang="de">
        <li>Der Tisch ist neu. → {blank("Er ist neu.", "문장", "full")}</li>
        <li>Die Küche ist groß. → {blank("Sie ist groß.", "문장", "full")}</li>
        <li>Das Bad ist klein. → {blank("Es ist klein.", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H5", "H5", "틀린 곳을 고쳐 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Das ist eine Tisch. → {blank("Das ist ein Tisch.", "고친 문장", "full")}</li>
        <li>Das ist nicht Stuhl. → {blank("Das ist kein Stuhl.", "고친 문장", "full")}</li>
        <li>Der Lampe ist neu. → {blank("Die Lampe ist neu.", "고친 문장", "full")}</li>
        <li>Das Zimmer ist kein groß. → {blank("Das Zimmer ist nicht groß.", "고친 문장", "full")}</li>
      </ol>""") + "\n" + ex("H6", "H6", "반대말로 대답하세요.", f"""      <ol lang="de">
        <li>Ist das Zimmer groß? – Nein, es ist {blank("klein", "반대말")}.</li>
        <li>Ist der Schrank neu? – Nein, er ist {blank("alt", "반대말")}.</li>
        <li>Ist die Küche dunkel? – Nein, sie ist {blank("hell", "반대말")}.</li>
        <li>Ist das Sofa teuer? – Nein, es ist {blank("billig|günstig", "반대말")}.</li>
        <li>Ist die WG laut? – Nein, sie ist {blank("ruhig|leise", "반대말")}.</li>
      </ol>""") + "\n" + ex("H7", "H7", "광고를 읽고 질문에 답하세요.", f"""      <div class="box" lang="de"><p><b>Zimmer frei!</b> Das Zimmer ist 14 m² groß und hell. Hier sind ein Bett, ein Schrank und ein Schreibtisch. Ein Sofa ist nicht im Zimmer. Die Küche ist groß, das Bad ist klein. Die Miete ist 380 Euro. Wir sind zwei Studentinnen, Mia und Sara.</p></div>
      <p class="muted">die Miete = 월세 · die Studentin = 여학생(대학생)</p>
      <ol lang="de">
        <li>Wie ist das Zimmer? – Es ist {blank("hell", "형용사")}.</li>
        <li>Ist ein Sofa im Zimmer? – Nein, im Zimmer ist {blank("kein", "부정")} Sofa.</li>
        <li>Wie ist das Bad? – Es ist {blank("klein", "형용사")}.</li>
        <li>Wie viel ist die Miete? – {blank("380", "숫자", digits=True)} Euro.</li>
      </ol>"""))

# =====================================================================
# 2차시 · Im Koffer sind …
# =====================================================================
plural = [("der", "Tisch", "die Tische", "-e"), ("der", "Stuhl", "die Stühle", "¨-e"), ("die", "Lampe", "die Lampen", "-n"),
          ("das", "Bett", "die Betten", "-en"), ("das", "Buch", "die Bücher", "¨-er"), ("das", "Foto", "die Fotos", "-s"),
          ("der", "Spiegel", "die Spiegel", "–"), ("die", "Tablette", "die Tabletten", "-n")]
s2 = block("1교시 · 50분 · Input")
s2 += act("s2-wiederholung", "", "복습", 5, '    <p><b>혼자 말하기</b>: 방 안의 물건 5개를 보며 „<span lang="de">Das ist ein/eine … Der/Die/Das … ist …</span>“로 소리 내어 말하기.</p>')
s2 += act("s2-teil-b", 9, "Teil B · <span lang=\"de\">Was ist im Koffer?</span> · 가방 속 물건", 15, f'''{track("2-02", "dlg-2-02", "저녁, WG 부엌. 세 사람이 바뀐 가방을 열어 물건을 하나씩 꺼내요.")}
    {fig("story-2-abend", "WG 부엌 탁자에 둘러앉은 세 사람이 낡은 외투, 흑백 사진, 봉투, 약병을 살펴본다", "<span lang=de>Was ist im Koffer?</span> – 수상한 물건들")}
{dialog("dlg-2-02", [
    line("Lena", "Also, was ist im Koffer?", "자, 가방 안에 뭐가 있어?"),
    line("Jonas", "Das ist ein Mantel. Der Mantel ist alt und grau.", "이건 외투야. 외투는 낡았고 회색이야."),
    line("Minjun", "Und hier sind Tabletten. Zwei Packungen!", "그리고 여기 약이 있어. 두 통이야!"),
    line("Lena", "Und ein Foto! Wer sind die Leute?", "사진도 있어! 이 사람들은 누구지?"),
    line("Jonas", "Ein Mann und eine Frau. Sie sind jung.", "남자 한 명과 여자 한 명. 젊어."),
    line("Minjun", "Und hier ist der Brief. „Für E.“", "그리고 여기 편지. „E.에게“"),
    line("Lena", "Wer ist E.? Habt ihr eine Idee?", "E.가 누구지? 너희 생각 있어?"),
    line("Jonas", "Nein, wir haben keine Idee. Aber wir sind Detektive!", "아니, 우린 모르겠어. 그래도 우린 탐정이잖아!"),
    line("Lena", "Ihr seid verrückt!", "너희 진짜 못 말린다!"),
    line("Minjun", "Ich habe eine Idee: Sujin! Sie wohnt hier im Haus.", "좋은 생각이 있어: 수진 씨! 이 건물에 살아.")])}
{ex("B1", "9a", "맞으면 <b>r</b>, 틀리면 <b>f</b>. 해석 없이!", rf("b1", [
    ("Der Mantel ist neu und schwarz.", "f", ""),
    ("Im Koffer sind zwei Packungen Tabletten.", "r", ""),
    ("Auf dem Foto sind zwei Männer.", "f", "auf dem Foto = 사진에"),
    ("Die Leute auf dem Foto sind jung.", "r", ""),
    ("Jonas weiß: E. ist eine Frau.", "f", "wissen = 알다"),
    ("Sujin wohnt im Haus.", "r", "")]))}
{ex("B2", "9b", "누가 한 말일까요?", f"""      <ol lang="de">
        <li>„Ihr seid verrückt!“ → {sel("Lena", ["Lena", "Jonas", "Minjun"])}</li>
        <li>„Wir haben keine Idee.“ → {sel("Jonas", ["Lena", "Jonas", "Minjun"])}</li>
        <li>„Ich habe eine Idee: Sujin!“ → {sel("Minjun", ["Lena", "Jonas", "Minjun"])}</li>
        <li>„Habt ihr eine Idee?“ → {sel("Lena", ["Lena", "Jonas", "Minjun"])}</li>
      </ol>""")}''')

s2 += act("s2-plural", 10, "<span lang=\"de\">Ein Stuhl, zwei Stühle</span> · 복수형", 15, f'''    <div class="vocab" lang="de">{"".join(f'<div><b data-say="{a} {w}, {p}">{art(a, w)}</b><span>→ {art("pl", p.split(" ",1)[1])}</span><span class="ko" lang="ko">{e}</span></div>' for a, w, p, e in plural)}</div>
{gram("복수형 – 관사는 언제나 die, 끝 모양은 다섯 가지", f"""      <div class="table-wrap"><table>
        <thead><tr><th>끝에 붙는 것</th><th>예</th><th>자주 나오는 경우</th></tr></thead>
        <tbody>
          <tr><td lang="de">-e / ¨-e</td><td lang="de">Tisch → Tisch<b>e</b> · Stuhl → St<b>ü</b>hl<b>e</b></td><td>남성 명사</td></tr>
          <tr><td lang="de">-n / -en</td><td lang="de">Lampe → Lampe<b>n</b> · Bett → Bett<b>en</b></td><td>-e로 끝나는 여성 명사</td></tr>
          <tr><td lang="de">¨-er</td><td lang="de">Buch → B<b>ü</b>ch<b>er</b></td><td>짧은 중성 명사</td></tr>
          <tr><td lang="de">-s</td><td lang="de">Foto → Foto<b>s</b> · Sofa → Sofa<b>s</b></td><td>외래어, 모음으로 끝남</td></tr>
          <tr><td lang="de">–</td><td lang="de">Spiegel → Spiegel</td><td>-el · -er로 끝남</td></tr>
        </tbody>
      </table></div>
      <p>복수형도 단어와 함께 외워요. 사전에는 <span lang="de">Stuhl, der, <b>¨-e</b></span>처럼 적혀 있어요.</p>""")}
{ex("P1", "10a", "복수형을 쓰세요. 관사 die도 함께!", f"""      <ol lang="de">
        <li>der Tisch → {blank("die Tische", "복수형", "wide")}</li>
        <li>die Lampe → {blank("die Lampen", "복수형", "wide")}</li>
        <li>das Foto → {blank("die Fotos", "복수형", "wide")}</li>
        <li>der Stuhl → {blank("die Stühle", "복수형", "wide")}</li>
        <li>das Bett → {blank("die Betten", "복수형", "wide")}</li>
        <li>das Buch → {blank("die Bücher", "복수형", "wide")}</li>
      </ol>""")}
{ex("P2", "10b", "단수일까요, 복수일까요? ist / sind를 고르세요.", f"""      <ol lang="de">
        <li>Die Stühle {sel("sind", ["ist", "sind"])} neu.</li>
        <li>Der Spiegel {sel("ist", ["ist", "sind"])} alt.</li>
        <li>Die Spiegel {sel("sind", ["ist", "sind"])} alt.</li>
        <li>Die Lampe {sel("ist", ["ist", "sind"])} modern.</li>
        <li>Die Fotos {sel("sind", ["ist", "sind"])} schwarz-weiß.</li>
      </ol>""")}''')

pl_table = f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th lang="de">kommen</th><th lang="de">wohnen</th><th lang="de">sein</th><th lang="de">haben</th></tr></thead>
        <tbody lang="de">
          <tr><th>ich</th><td>komme</td><td>wohne</td><td>bin</td><td>habe</td></tr>
          <tr><th>du</th><td>kommst</td><td>wohnst</td><td>bist</td><td>ha<b>st</b></td></tr>
          <tr><th>er / sie / es</th><td>kommt</td><td>wohnt</td><td>ist</td><td>ha<b>t</b></td></tr>
          <tr class="hl"><th>wir <small lang="ko">우리</small></th><td>komm<b>en</b></td><td>wohn<b>en</b></td><td><b>sind</b></td><td>hab<b>en</b></td></tr>
          <tr class="hl"><th>ihr <small lang="ko">너희</small></th><td>komm<b>t</b></td><td>wohn<b>t</b></td><td><b>seid</b></td><td>hab<b>t</b></td></tr>
          <tr class="hl"><th>sie <small lang="ko">그들</small> / Sie</th><td>komm<b>en</b></td><td>wohn<b>en</b></td><td><b>sind</b></td><td>hab<b>en</b></td></tr>
        </tbody>
      </table></div>"""
s2 += act("s2-satz2", 11, "오늘의 문장 틀 ② · 우리 · 너희 · 그들", 15, f'''{today([
    ("Wir sind Detektive!", "", "우리는 탐정이야!"),
    ("Ihr seid verrückt!", "", "너희 정말 못 말려!"),
    ("Habt ihr eine Idee?", "", "너희 생각 있어?"),
    ("Wir haben keine Idee.", "", "우리는 모르겠어."),
    ("Sie sind jung.", "", "그들은 젊어.")])}
{gram("wir · ihr · sie – 주어가 여럿일 때", f"""{pl_table}
      <p><b lang="de">wir</b>와 <b lang="de">sie/Sie</b>는 언제나 <b>사전형과 같아요</b>(-en). <b lang="de">ihr</b>는 er와 같은 <b>-t</b>.</p>
      <p>조심! <b lang="de">sie</b>는 세 가지: <span lang="de">sie kommt</span>(그녀) · <span lang="de">sie kommen</span>(그들) · <span lang="de">Sie kommen</span>(당신, 대문자). <b>동사 끝</b>을 보면 구별돼요.</p>""")}
{ex("G4", "11a", "알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Wir {blank("wohnen", "wohnen")} in Leipzig. (wohnen)</li>
        <li>Woher {blank("kommt", "kommen")} ihr? (kommen)</li>
        <li>Jonas und Lena {blank("sind", "sein")} nett. (sein)</li>
        <li>{blank("Seid", "sein")} ihr Studenten? (sein)</li>
        <li>Wir {blank("sprechen", "sprechen")} Deutsch und Koreanisch. (sprechen)</li>
        <li>Was {blank("macht", "machen")} ihr? (machen)</li>
      </ol>""")}
{ex("G5", "11b", "sie는 누구일까요? 동사 끝을 보고 고르세요.", f"""      <ol lang="de">
        <li>Sie wohnt im Haus. → {sel("그녀", ["그녀", "그들", "당신"])}</li>
        <li>Sie sind jung. (Mann und Frau auf dem Foto) → {sel("그들", ["그녀", "그들", "당신"])}</li>
        <li>Woher kommen Sie, Herr Park? → {sel("당신", ["그녀", "그들", "당신"])}</li>
        <li>Lena? Sie kommt aus Hamburg. → {sel("그녀", ["그녀", "그들", "당신"])}</li>
      </ol>""")}''')

s2 += block("2교시 · 50분 · Output")
s2 += act("s2-haben", 12, "<span lang=\"de\">Ich habe …</span> · 가지고 있어요", 15, f'''{gram("haben – ‘가지고 있다’", f"""      <p lang="de">ich hab<b>e</b> · du ha<b>st</b> · er/sie ha<b>t</b> · wir hab<b>en</b> · ihr hab<b>t</b> · sie/Sie hab<b>en</b></p>
      <p>du와 er에서 <b>b가 빠져요</b>: <span lang="de"><s>habst</s> → hast · <s>habt</s>(er) → hat</span></p>
      <p lang="de">Ich habe <b>ein</b> Bett / <b>eine</b> Lampe / <b>einen</b> Schrank. · Ich habe <b>kein</b> Sofa.</p>
      <p class="muted">haben 뒤의 남성 명사는 <b lang="de">einen / keinen</b>가 돼요(<span lang="de">Ich habe einen Bruder.</span>). 지금은 덩어리로 외우고, 3과에서 자세히 배워요.</p>""")}
{ex("HB1", "12a", "haben의 알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Ich {blank("habe", "haben")} ein Zimmer in Leipzig.</li>
        <li>{blank("Hast", "haben")} du eine Lampe?</li>
        <li>Lena {blank("hat", "haben")} viele Bücher.</li>
        <li>Wir {blank("haben", "haben")} keine Idee.</li>
        <li>{blank("Habt", "haben")} ihr einen Spiegel?</li>
        <li>Minjun und Jonas {blank("haben", "haben")} einen Koffer – aber nicht ihren!</li>
      </ol>""")}
{ex("HB2", "12b", "sein일까요, haben일까요? 알맞은 형태를 고르세요.", f"""      <ol lang="de">
        <li>Das Zimmer {sel("ist", ["ist", "hat"])} hell.</li>
        <li>Das Zimmer {sel("hat", ["ist", "hat"])} ein Fenster.</li>
        <li>Wir {sel("sind", ["sind", "haben"])} Detektive.</li>
        <li>Wir {sel("haben", ["sind", "haben"])} einen Plan.</li>
        <li>{sel("Bist", ["Bist", "Hast"])} du müde?</li>
      </ol>
      <p class="muted">das Fenster = 창문 · der Plan = 계획</p>""")}''', "output")

s2 += act("s2-lenas-zimmer", 13, "<span lang=\"de\">Hören</span> · Lena의 방", 10, f'''    <p>Lena가 영상 통화로 함부르크의 친구에게 방을 보여 줘요. ▶로 듣고 문제를 푸세요. 대본은 다 푼 뒤에!</p>
    <p><button type="button" class="say-btn" data-play="dlg-2-03" aria-label="Lena 듣기">▶</button> Track 2-03</p>
{ex("LZ1", "13a", "Lena의 방에 있는 것에 <b>r</b>, 없는 것에 <b>f</b>", rf("lz1", [
    ("ein Bett", "r", ""), ("ein Sofa", "f", ""), ("ein Schreibtisch", "r", ""), ("zwei Lampen", "r", ""), ("ein Spiegel", "f", ""), ("viele Bücher", "r", "")]))}
{ex("LZ2", "13b", "다시 듣고 빈칸을 쓰세요.", f"""      <ol lang="de">
        <li>Mein Zimmer ist {blank("klein", "형용사")}, aber schön.</li>
        <li>Das Regal ist {blank("voll", "형용사")} – ich habe viele Bücher!</li>
        <li>Ich habe {blank("kein", "부정")} Sofa.</li>
      </ol>
      <p class="muted">voll = 가득 찬</p>""")}
    <details class="transcript"><summary>대본 보기 (문제를 다 푼 뒤에!)</summary>
{dialog("dlg-2-03", [
    line("Lena", "Schau mal, das ist mein Zimmer! Mein Zimmer ist klein, aber schön.", "봐, 이게 내 방이야! 내 방은 작지만 예뻐."),
    line("Lena", "Hier sind ein Bett, ein Schreibtisch und ein Regal. Das Regal ist voll – ich habe viele Bücher!", "여기 침대, 책상, 책장이 있어. 책장이 꽉 찼어 – 책이 많거든!"),
    line("Lena", "Ich habe kein Sofa und keinen Spiegel. Aber ich habe zwei Lampen. Sie sind gelb!", "소파도 거울도 없어. 그래도 전등이 두 개 있어. 노란색이야!")])}
    </details>''', "output")

s2 += act("s2-schreiben", 14, "<span lang=\"de\">Schreiben</span> · 가족에게 방 소개 메시지", 15, f'''    <p>민준이 한국의 누나에게 독일어로 메시지를 보내요(독일어 연습 중!). 먼저 민준의 메시지를 완성하고, 그다음 <b>내 방</b> 메시지를 쓰세요.</p>
{ex("SM1", "14a", "민준의 메시지를 완성하세요.", f"""      <div class="box" lang="de"><p>Hallo Jiyeon! Wie geht's? Ich {blank("bin", "sein")} jetzt in Leipzig. Ich {blank("habe", "haben")} ein Zimmer in einer WG. {blank("Das", "관사")} Zimmer ist groß und hell. Hier {blank("sind", "sein")} ein Bett und ein Schrank. Der Schrank ist alt, aber {blank("er", "대명사")} ist schön. Ich habe {blank("keinen", "부정")} Tisch und keinen Stuhl. Jonas und Lena {blank("sind", "sein")} nett. Wir {blank("haben", "haben")} ein Geheimnis … 😉</p></div>
      <p class="muted">das Geheimnis = 비밀</p>""")}
    <p><b>14b</b> 내 방 메시지 (5–6문장). <span lang="de">Mein Zimmer ist … Hier ist ein/eine … Der/Die/Das … ist … Ich habe kein/keine …</span></p>
    <textarea lang="de" data-persist="mein-zimmer" rows="5" placeholder="Hallo! Mein Zimmer ist …" aria-label="내 방 메시지"></textarea>
    <div class="table-wrap"><table><tbody>
      <tr><td>☐</td><td>명사는 <b>대문자</b>로 시작했나요? (<span lang="de">das Bett, die Lampe</span>)</td></tr>
      <tr><td>☐</td><td>남성 der · 여성 die · 중성 das를 맞게 썼나요?</td></tr>
      <tr><td>☐</td><td>복수 주어 뒤에는 <b lang="de">sind</b>를 썼나요?</td></tr>
    </tbody></table></div>''', "output")

s2 += act("s2-raetsel", 15, f"{ic('search')}<span lang=\"de\">Fallakte</span> · Jonas의 사건 메모", 10, f'''    <p>Jonas가 사건 메모를 썼어요. 그런데 Jonas는 문법이 조금 엉터리예요! 틀린 곳을 고쳐 주세요.</p>
    <div class="box mystery" lang="de"><p><b>Fall Nr. 1 – Der falsche Koffer</b><br>Im Koffer ist ein Mantel, ein Foto, ein Brief und zwei Packungen Tabletten. Der Mantel ist grau. Die Foto ist alt. Auf dem Foto sind ein Mann und eine Frau. Der Brief ist für E. Wir hat keine Idee.</p></div>
{ex("FA1", "15a", "Jonas의 메모에서 틀린 문장 세 개를 고쳐 쓰세요.", f"""      <ol lang="de">
        <li>Im Koffer ist ein Mantel, ein Foto … → Im Koffer {blank("sind", "동사")} ein Mantel, ein Foto …</li>
        <li>Die Foto ist alt. → {blank("Das Foto ist alt.", "고친 문장", "full")}</li>
        <li>Wir hat keine Idee. → {blank("Wir haben keine Idee.", "고친 문장", "full")}</li>
      </ol>
      <p class="muted">물건이 여러 개면 복수 → <span lang="de">sind</span></p>""")}''', "output")

s2 += homework("hw-2", "2차시 숙제 (60분)", [
    ("Teil B 대화 듣고 따라 읽기(Shadowing) 3번 + 복수형 카드 복습", 10),
    ("<b>H1 · H2</b> 복수형, wir/ihr/sie 동사 형태", 15),
    ("<b>H3 · H4</b> haben, sein과 haben", 15),
    ("<b>H5</b> 읽기 – Lena의 메시지", 5),
    ("<b>H6 · H7</b> 단수와 복수, 주어 바꿔 쓰기", 10),
    (ic("mic") + "<b>녹음</b>: „Wir sind … Wir wohnen … Wir haben …“로 나와 가족(또는 룸메이트)을 소개해서 제출", 5)],
    ex("H1", "H1", "단수 → 복수로 문장 전체를 바꾸세요.", f"""      <ol lang="de">
        <li>Das ist ein Stuhl. → Das sind zwei {blank("Stühle", "복수형")}.</li>
        <li>Die Lampe ist neu. → Die {blank("Lampen", "복수형")} {blank("sind", "동사")} neu.</li>
        <li>Das Foto ist alt. → {blank("Die Fotos sind alt.", "문장", "full")}</li>
        <li>Der Tisch ist groß. → {blank("Die Tische sind groß.", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H2", "H2", "알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Wir {blank("sind", "sein")} in Leipzig. (sein)</li>
        <li>Ihr {blank("seid", "sein")} nett! (sein)</li>
        <li>Woher {blank("kommen", "kommen")} Amira und Oksana? (kommen)</li>
        <li>{blank("Wohnt", "wohnen")} ihr in einer WG? (wohnen)</li>
        <li>Wir {blank("heißen", "heißen")} Lena und Jonas. (heißen)</li>
        <li>Ihr {blank("sprecht", "sprechen")} gut Deutsch! (sprechen)</li>
      </ol>""") + "\n" + ex("H3", "H3", "haben의 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Minjun {blank("hat", "haben")} ein Zimmer.</li>
        <li>Ich {blank("habe", "haben")} keine Lampe.</li>
        <li>{blank("Hast", "haben")} du ein Sofa?</li>
        <li>Wir {blank("haben", "haben")} zwei Stühle.</li>
        <li>{blank("Habt", "haben")} ihr Zeit?</li>
      </ol>
      <p class="muted">die Zeit = 시간</p>""") + "\n" + ex("H4", "H4", "sein과 haben 중 알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Das Bad {blank("ist", "동사")} klein.</li>
        <li>Die WG {blank("hat", "동사")} eine Küche.</li>
        <li>Jonas und Lena {blank("sind", "동사")} Studenten.</li>
        <li>Lena {blank("hat", "동사")} viele Bücher.</li>
        <li>{blank("Seid", "동사")} ihr müde?</li>
      </ol>""") + "\n" + ex("H5", "H5", "Lena의 메시지를 읽고 맞으면 <b>r</b>, 틀리면 <b>f</b>", f"""      <div class="box" lang="de"><p>Hi Anna! Wir haben jetzt einen Mitbewohner: Minjun aus Korea. Er ist nett und ruhig. Sein Zimmer ist groß, aber es hat keinen Tisch. Jonas und Minjun sind jetzt Detektive – sie haben einen falschen Koffer! Verrückt, oder? Liebe Grüße, Lena</p></div>
      <p class="muted">der Mitbewohner = 룸메이트 · sein Zimmer = 그의 방 · Liebe Grüße = 안부를 전하며</p>
""" + rf("h5", [("Minjun ist der neue Mitbewohner.", "r", ""), ("Minjun ist laut.", "f", ""), ("Minjuns Zimmer ist klein.", "f", ""), ("Im Zimmer ist kein Tisch.", "r", ""), ("Lena findet die Detektiv-Idee verrückt.", "r", "")])) + "\n" + ex("H6", "H6", "복수 문장을 단수로 바꾸세요. (ein/eine 사용)", f"""      <ol lang="de">
        <li>Das sind Lampen. → {blank("Das ist eine Lampe.", "문장", "full")}</li>
        <li>Das sind Betten. → {blank("Das ist ein Bett.", "문장", "full")}</li>
        <li>Das sind Stühle. → {blank("Das ist ein Stuhl.", "문장", "full")}</li>
        <li>Die Bücher sind alt. → {blank("Das Buch ist alt.", "문장", "full")}</li>
      </ol>""") + "\n" + ex("H7", "H7", "주어를 바꿔 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Ich habe eine Idee. (wir) → {blank("Wir haben eine Idee.", "문장", "full")}</li>
        <li>Du bist verrückt! (ihr) → {blank("Ihr seid verrückt!", "문장", "full")}</li>
        <li>Er wohnt in Leipzig. (sie, 그들) → {blank("Sie wohnen in Leipzig.", "문장", "full")}</li>
        <li>Hast du Zeit? (ihr) → {blank("Habt ihr Zeit?", "문장", "full")}</li>
      </ol>"""))

# =====================================================================
# 3차시 · Das ist meine Familie.
# =====================================================================
fam = [("der", "Vater", "아버지", "Papa"), ("die", "Mutter", "어머니", "Mama"), ("die", "Eltern", "부모", ""),
       ("der", "Sohn", "아들", ""), ("die", "Tochter", "딸", ""), ("die", "Kinder", "아이들", "das Kind"),
       ("der", "Bruder", "형제 (형·오빠·남동생)", ""), ("die", "Schwester", "자매 (누나·언니·여동생)", ""), ("die", "Geschwister", "형제자매", ""),
       ("der", "Mann", "남편 / 남자", ""), ("die", "Frau", "아내 / 여자", ""), ("die", "Oma", "할머니", "der Opa = 할아버지")]
def fart(a, w): return art("pl" if w in ("Eltern", "Kinder", "Geschwister") else a, w)
fcards = "".join(f'<div><b data-say="{"die" if w in ("Eltern", "Kinder", "Geschwister") else a} {w}">{fart(a, w)}</b><span class="ko" lang="ko">{ko}</span>{f"<small>{x}</small>" if x else ""}</div>' for a, w, ko, x in fam)
nums2 = [(21, "einundzwanzig"), (22, "zweiundzwanzig"), (25, "fünfundzwanzig"), (30, "dreißig"), (34, "vierunddreißig"), (38, "achtunddreißig"),
         (40, "vierzig"), (50, "fünfzig"), (60, "sechzig"), (67, "siebenundsechzig"), (70, "siebzig"), (80, "achtzig"),
         (90, "neunzig"), (99, "neunundneunzig"), (100, "hundert")]
ncells2 = "".join(f'<div class="say-cell" data-say="{n}"><b>{i}</b><span>{n}</span></div>' for i, n in nums2)
poss = f"""      <div class="table-wrap"><table>
        <thead><tr><th></th><th>{g("der", "m")} Vater · {g("das", "n")} Kind</th><th>{g("die", "f")} Mutter · {g("die", "p")} Eltern</th></tr></thead>
        <tbody lang="de">
          <tr><th>ich → <small lang="ko">나의</small></th><td>mein</td><td>mein<b>e</b></td></tr>
          <tr><th>du → <small lang="ko">너의</small></th><td>dein</td><td>dein<b>e</b></td></tr>
          <tr><th>er → <small lang="ko">그의</small></th><td>sein</td><td>sein<b>e</b></td></tr>
          <tr><th>sie → <small lang="ko">그녀의</small></th><td>ihr</td><td>ihr<b>e</b></td></tr>
          <tr><th>wir → <small lang="ko">우리의</small></th><td>unser</td><td>unser<b>e</b></td></tr>
          <tr><th>ihr → <small lang="ko">너희의</small></th><td>euer</td><td>eur<b>e</b></td></tr>
          <tr><th>sie → <small lang="ko">그들의</small> · Sie → <small lang="ko">당신의</small></th><td>ihr · Ihr</td><td>ihr<b>e</b> · Ihr<b>e</b></td></tr>
        </tbody>
      </table></div>"""

s3 = block("1교시 · 50분 · Input")
s3 += act("s3-wiederholung", "", "복습", 5, '    <p><b>혼자 말하기</b>: 가방 속 물건 4개를 복수형과 함께 말하기. „<span lang="de">Im Koffer sind … Die Tabletten sind …</span>“</p>')
s3 += act("s3-teil-c", 16, "Teil C · <span lang=\"de\">Der Integrationskurs</span> · 통합 과정 첫날", 15, f'''{track("2-04", "dlg-2-04", "같은 날 아침, 수진은 이민자 통합 과정(Integrationskurs) 첫 수업에 가요.")}
{dialog("dlg-2-04", [
    line("Herr Brandt", "Guten Morgen! Ich bin Michael Brandt, Ihr Lehrer. Bitte stellen Sie sich vor: Name, Land und Familie.", "안녕하세요! 저는 여러분의 선생님 미하엘 브란트입니다. 자기소개를 해 주세요: 이름, 나라, 가족."),
    line("Amira", "Ich heiße Amira. Ich komme aus Syrien. Ich bin verheiratet und habe zwei Kinder.", "저는 아미라예요. 시리아에서 왔어요. 결혼했고 아이가 둘 있어요."),
    line("Herr Brandt", "Wie alt sind Ihre Kinder?", "아이들은 몇 살이에요?"),
    line("Amira", "Mein Sohn ist acht und meine Tochter ist fünf.", "아들은 여덟 살, 딸은 다섯 살이에요."),
    line("Oksana", "Ich bin Oksana. Ich komme aus der Ukraine. Ich habe einen Sohn. Er heißt Maksym und ist fünfzehn.", "저는 옥사나예요. 우크라이나에서 왔어요. 아들이 하나 있어요. 이름은 막심이고 열다섯 살이에요."),
    line("Sujin", "Ich heiße Sujin Lee. Ich komme aus Südkorea. Ich habe 38.", "저는 이수진이에요. 한국에서 왔어요. 저는 38을 가지고 있어요(?)."),
    stage("반 전체가 웃는다."),
    line("Herr Brandt", "Sie <b>sind</b> 38! Auf Deutsch sagt man: Ich bin 38 Jahre alt.", "38살이시군요! 독일어로는 ‘Ich bin 38 Jahre alt.’라고 해요."),
    line("Sujin", "Ah, Entschuldigung! Ich bin 38 Jahre alt. Mein Mann heißt Taeho. Er ist Ingenieur. Unsere Kinder heißen Haeun und Doyun. Haeun ist sechs und Doyun ist drei.", "아, 죄송해요! 저는 38살이에요. 남편 이름은 태호예요. 엔지니어예요. 우리 아이들 이름은 하은이와 도윤이에요. 하은이는 여섯 살, 도윤이는 세 살이에요."),
    line("Herr Brandt", "Und was sind Sie von Beruf?", "그리고 직업이 뭐예요?"),
    line("Sujin", "Ich bin Krankenschwester.", "간호사예요."),
    line("Herr Brandt", "Sehr gut! Herzlich willkommen im Kurs!", "아주 좋아요! 수업에 오신 걸 환영합니다!")])}
    <div class="cast cast-big" aria-label="수업 친구들"><figure>{pic("k02/person-brandt", "Herr Brandt", "person")}<figcaption>Herr Brandt<small>Lehrer</small></figcaption></figure><figure>{pic("k02/person-amira", "Amira", "person")}<figcaption>Amira<small>Syrien</small></figcaption></figure><figure>{pic("k02/person-oksana", "Oksana", "person")}<figcaption>Oksana<small>Ukraine</small></figcaption></figure><figure>{pic("k01/person-sujin", "Sujin", "person")}<figcaption>Sujin<small>Südkorea</small></figcaption></figure></div>
{ex("C1", "16a", "맞으면 <b>r</b>, 틀리면 <b>f</b>", rf("c1", [
    ("Herr Brandt ist der Lehrer.", "r", ""),
    ("Amira hat drei Kinder.", "f", ""),
    ("Amiras Tochter ist fünf.", "r", ""),
    ("Oksanas Sohn ist fünfzig.", "f", ""),
    ("Sujins Mann ist Ingenieur.", "r", ""),
    ("Doyun ist sechs Jahre alt.", "f", "")]))}
{ex("C2", "16b", "누구일까요?", f"""      <ol lang="de">
        <li>Sie kommt aus der Ukraine. → {sel("Oksana", ["Amira", "Oksana", "Sujin"])}</li>
        <li>Sie ist Krankenschwester. → {sel("Sujin", ["Amira", "Oksana", "Sujin"])}</li>
        <li>Ihr Sohn ist acht. → {sel("Amira", ["Amira", "Oksana", "Sujin"])}</li>
        <li>Sie hat einen Sohn, Maksym. → {sel("Oksana", ["Amira", "Oksana", "Sujin"])}</li>
        <li>Sie sagt: „Ich habe 38.“ → {sel("Sujin", ["Amira", "Oksana", "Sujin"])}</li>
      </ol>""")}
    <div class="box tip">{ic("tip")}<b>왜 다들 웃었을까요?</b> 한국어로는 ‘서른여덟 살<b>이에요</b>’, 영어로도 ‘I <b>am</b> 38’. 그런데 수진은 ‘가지고 있다’(haben)를 썼어요. 나이는 언제나 <b lang="de">sein</b>! (프랑스어·스페인어는 ‘가지다’를 써서 이 반 친구들도 자주 틀려요.)</div>''')

s3 += act("s3-familie", 17, "<span lang=\"de\">Die Familie</span> · 가족", 15, f'''    <p>▶를 눌러 듣고 따라 하세요. 남자 가족은 der, 여자 가족은 die, 여럿이면 언제나 die!</p>
    <div class="vocab" lang="de">{fcards}</div>
{ex("F1", "17a", "수진의 가족이에요. 알맞은 말을 쓰세요.", f"""      <ol lang="de">
        <li>Taeho ist Sujins {blank("Mann", "가족")}.</li>
        <li>Haeun ist Sujins {blank("Tochter", "가족")}.</li>
        <li>Doyun ist Sujins {blank("Sohn", "가족")}.</li>
        <li>Doyun ist Haeuns {blank("Bruder", "가족")}.</li>
        <li>Haeun ist Doyuns {blank("Schwester", "가족")}.</li>
        <li>Sujin und Taeho sind die {blank("Eltern", "가족")} von Haeun und Doyun.</li>
        <li>Haeun und Doyun sind {blank("Geschwister", "가족")}.</li>
      </ol>
      <p class="muted">Sujin<b>s</b> Mann = 수진의 남편 (이름 + s, 아포스트로피 없음!)</p>""")}
{ex("F2", "17b", "der · die를 고르세요. 그리고 복수형인 것에는 die(복수)를!", f"""      <ol lang="de">
        <li>{sel("der", ["der", "die", "die (복수)"])} Bruder</li>
        <li>{sel("die", ["der", "die", "die (복수)"])} Tochter</li>
        <li>{sel("die (복수)", ["der", "die", "die (복수)"])} Eltern</li>
        <li>{sel("der", ["der", "die", "die (복수)"])} Sohn</li>
        <li>{sel("die (복수)", ["der", "die", "die (복수)"])} Kinder</li>
      </ol>""")}''')

s3 += act("s3-satz3", 18, "오늘의 문장 틀 ③ · 나의, 너의, 그의 …", 15, f'''{today([
    ("Das ist meine Familie.", "", "이건 우리 가족이에요."),
    ("Mein Mann heißt Taeho.", "", "제 남편 이름은 태호예요."),
    ("Unsere Kinder heißen Haeun und Doyun.", "", "우리 아이들 이름은 하은이와 도윤이에요."),
    ("Wie alt sind Ihre Kinder?", "", "아이들은 몇 살이에요?"),
    ("Ich bin 38 Jahre alt.", "", "저는 38살이에요."),
    ("Was sind Sie von Beruf? – Ich bin Krankenschwester.", "", "직업이 뭐예요? – 간호사예요.")])}
{gram("소유관사 – ‘나의’, ‘너의’ … 뒤 명사가 여성·복수면 -e", f"""{poss}
      <p>규칙은 ein / eine와 똑같아요: <span lang="de">ein Vater → <b>mein</b> Vater · eine Mutter → <b>meine</b> Mutter</span>. 복수는 <span lang="de">mein<b>e</b> Eltern</span>.</p>
      <p>조심! <b lang="de">sein</b> = 그의 / 이다 · <b lang="de">ihr</b> = 그녀의, 그들의 / 너희(주어). 문장 속 자리를 보고 구별해요. <span lang="de">euer</span>는 e가 빠져 <span lang="de">eure</span>.</p>""")}
{gram("나이와 직업 – 둘 다 sein", """      <p lang="de">Ich <b>bin</b> 38 (Jahre alt). · Wie alt <b>bist</b> du? · Ich <b>bin</b> Krankenschwester. · Er <b>ist</b> Ingenieur.</p>
      <p>직업 앞에는 <b>관사를 쓰지 않아요</b>: <span lang="de"><s>Ich bin eine Krankenschwester.</s></span> 여자는 대부분 <b>-in</b>을 붙여요: <span lang="de">der Lehrer → die Lehrer<b>in</b>, der Ingenieur → die Ingenieur<b>in</b></span>.</p>""")}
{ex("G6", "18a", "mein일까요, meine일까요?", f"""      <ol lang="de">
        <li>Das ist {sel("mein", ["mein", "meine"])} Bruder.</li>
        <li>Das ist {sel("meine", ["mein", "meine"])} Schwester.</li>
        <li>Das sind {sel("meine", ["mein", "meine"])} Eltern.</li>
        <li>Das ist {sel("mein", ["mein", "meine"])} Kind.</li>
        <li>Das ist {sel("meine", ["mein", "meine"])} Oma.</li>
      </ol>""")}
{ex("G7", "18b", "누구의 것일까요? 알맞은 소유관사를 쓰세요.", f"""      <ol lang="de">
        <li>Das ist Taeho. {blank("Seine", "소유관사")} Frau heißt Sujin. (er)</li>
        <li>Das ist Sujin. {blank("Ihr", "소유관사")} Mann heißt Taeho. (sie)</li>
        <li>Wir wohnen in Leipzig. {blank("Unsere", "소유관사")} Wohnung ist klein. (wir)</li>
        <li>Wie heißt {blank("dein", "소유관사")} Bruder? (du)</li>
        <li>Herr Brandt, wie alt sind {blank("Ihre", "소유관사")} Kinder? (Sie)</li>
        <li>Jonas und Lena, ist das {blank("euer", "소유관사")} Koffer? (ihr)</li>
      </ol>
      <p class="muted">die Wohnung = 집(아파트)</p>""")}
{ex("G8", "18c", "sein일까요, haben일까요? 알맞은 형태를 쓰세요.", f"""      <ol lang="de">
        <li>Ich {blank("bin", "동사")} 38 Jahre alt.</li>
        <li>Ich {blank("habe", "동사")} zwei Kinder.</li>
        <li>Oksanas Sohn {blank("ist", "동사")} fünfzehn.</li>
        <li>Amira {blank("hat", "동사")} einen Sohn und eine Tochter.</li>
        <li>Taeho {blank("ist", "동사")} Ingenieur.</li>
        <li>Wie alt {blank("bist", "동사")} du?</li>
      </ol>""")}''')

s3 += block("2교시 · 50분 · Output")
s3 += act("s3-zahlen", 19, "<span lang=\"de\">Die Zahlen 21–100</span> · 나이를 말하려면", 15, f'''    <p>숫자를 눌러 듣고 따라 하세요.</p>
    <div class="say-grid numbers" lang="de">{ncells2}</div>
{gram("21–99 – 뒤에서부터 읽어요", """      <p lang="de">21 = <b>ein</b>-und-<b>zwanzig</b> (1 그리고 20) · 38 = <b>acht</b>-und-<b>dreißig</b> (8 그리고 30)</p>
      <p>한 자리 수를 먼저, 그다음 <b lang="de">und</b>, 마지막에 십의 자리. 띄어 쓰지 않고 한 단어로 붙여 써요.</p>
      <p>조심! <span lang="de">dreißig</span>(ß) · <span lang="de">sechzig</span>(sechs의 s 빠짐) · <span lang="de">siebzig</span>(sieben의 en 빠짐) · <span lang="de">eins → <b>ein</b>undzwanzig</span></p>""")}
{ex("Z1", "19a", "숫자로 쓰세요.", f"""      <ol lang="de">
        <li>dreiundvierzig → {blank("43", "숫자", digits=True)}</li>
        <li>siebenundsechzig → {blank("67", "숫자", digits=True)}</li>
        <li>zweiundachtzig → {blank("82", "숫자", digits=True)}</li>
        <li>neunundfünfzig → {blank("59", "숫자", digits=True)}</li>
        <li>vierunddreißig → {blank("34", "숫자", digits=True)}</li>
        <li>sechsundneunzig → {blank("96", "숫자", digits=True)}</li>
      </ol>""")}
{ex("Z2", "19b", "독일어로 쓰세요.", f"""      <ol lang="de">
        <li>25 → {blank("fünfundzwanzig", "25", ci=True)}</li>
        <li>31 → {blank("einunddreißig", "31", ci=True)}</li>
        <li>60 → {blank("sechzig", "60", ci=True)}</li>
        <li>77 → {blank("siebenundsiebzig", "77", ci=True)}</li>
        <li>100 → {blank("hundert|einhundert", "100", ci=True)}</li>
      </ol>""")}
{ex("Z3", "19c", "▶로 듣고 숫자로 쓰세요. 몇 살일까요?", f"""      <ol lang="de">
        <li>Frau Schulze ist <span class="lis" data-say="vierundsiebzig"></span> {blank("74", "숫자", digits=True)} Jahre alt.</li>
        <li>Taeho ist <span class="lis" data-say="einundvierzig"></span> {blank("41", "숫자", digits=True)} Jahre alt.</li>
        <li>Herr Brandt ist <span class="lis" data-say="zweiundfünfzig"></span> {blank("52", "숫자", digits=True)} Jahre alt.</li>
        <li>Minjun ist <span class="lis" data-say="sechsundzwanzig"></span> {blank("26", "숫자", digits=True)} Jahre alt.</li>
        <li>Amira ist <span class="lis" data-say="vierunddreißig"></span> {blank("34", "숫자", digits=True)} Jahre alt.</li>
      </ol>""")}''', "output")

s3 += act("s3-lesen", 20, "<span lang=\"de\">Lesen</span> · Amira의 자기소개", 10, f'''    <p>통합 과정 숙제로 Amira가 쓴 글이에요. 먼저 끝까지 읽고 문제를 푸세요.</p>
    <div class="box" lang="de"><p>Ich heiße Amira Haddad. Ich bin 34 Jahre alt und komme aus Damaskus in Syrien. Meine Familie und ich wohnen jetzt in Leipzig. Mein Mann heißt Karim. Er ist 39 Jahre alt und Apotheker. Unser Sohn Omar ist acht, unsere Tochter Lina ist fünf. Meine Eltern wohnen noch in Syrien. Mein Bruder wohnt in Berlin. Er hat drei Kinder. Ich bin Lehrerin von Beruf, aber hier bin ich jetzt Schülerin!</p></div>
    <p class="muted">der Apotheker = 약사 · noch = 아직 · die Schülerin = 학생(여)</p>
{ex("LA1", "20a", "맞으면 <b>r</b>, 틀리면 <b>f</b>", rf("la1", [
    ("Amira ist 34 Jahre alt.", "r", ""),
    ("Karim ist Lehrer.", "f", ""),
    ("Ihre Kinder heißen Omar und Lina.", "r", ""),
    ("Amiras Eltern wohnen in Leipzig.", "f", ""),
    ("Amiras Bruder hat drei Kinder.", "r", ""),
    ("Amira ist Lehrerin von Beruf.", "r", "")]))}
{ex("LA2", "20b", "Amira에 대해 쓰세요. (ihr / ihre)", f"""      <ol lang="de">
        <li>{blank("Ihr", "소유관사")} Mann heißt Karim.</li>
        <li>{blank("Ihre", "소유관사")} Tochter ist fünf.</li>
        <li>{blank("Ihre", "소유관사")} Eltern wohnen in Syrien.</li>
        <li>{blank("Ihr", "소유관사")} Bruder wohnt in Berlin.</li>
      </ol>""")}''', "output")

s3 += act("s3-sprachmittlung", 21, f"{ic('mediate')}<span lang=\"de\">Sprachmittlung</span> · 하은이의 통역", 10, f'''{track("2-05", "dlg-2-05", "오후, 유치원(Kita). 선생님이 가족 사진을 가져오라고 했어요. 수진이 하은에게 한국어로 말해요.")}
{dialog("dlg-2-05", [
    line("수진", "하은아, 선생님께 우리 가족 사진 보여 드려. 이건 엄마, 이건 아빠야. 아빠는 엔지니어라고 말씀드려.", "", lang=""),
    line("수진", "이건 도윤이. 세 살이야. 그리고 이분은 할머니. 서울에 사셔.", "", lang="")], cls="dialog ko", lang="ko")}
{ex("SP1", "21a", "하은이가 되어 Kita 선생님께 <b>독일어로</b> 전하세요.", f"""      <p lang="de" class="template">Das ist meine {blank("Mama|Mutter", "가족", ci=True)}. Das ist {blank("mein", "소유관사", ci=True)} Papa. Er {blank("ist", "동사")} Ingenieur. Das ist mein {blank("Bruder", "가족", ci=True)} Doyun. Er ist {blank("drei|3", "나이", ci=True)} Jahre alt. Und das ist meine {blank("Oma", "가족", ci=True)}. Sie {blank("wohnt", "동사")} in Seoul.</p>""")}
    <div class="box tip">{ic("tip")}아이들은 <span lang="de">Mama, Papa, Oma, Opa</span>라고 말해요. 어른에게 공식적으로 말할 때는 <span lang="de">meine Mutter, mein Vater</span>.</div>''', "output")

s3 += act("s3-schreiben", 22, "<span lang=\"de\">Schreiben</span> · 가족 사진 설명", 10, f'''{ex("SF1", "22a", "민준이 Lena에게 가족 사진을 설명해요. 빈칸을 채우세요.", f"""      <div class="box" lang="de"><p>Das ist {blank("meine", "소유관사")} Familie. Das ist mein Vater. Er {blank("ist", "동사")} 58 Jahre alt. Er ist Taxifahrer. Das ist {blank("meine", "소유관사")} Mutter. Sie ist {blank("fünfundfünfzig", "55", ci=True)} (55). Das ist meine Schwester Jiyeon. {blank("Sie", "대명사")} wohnt in Seoul. {blank("Ihr", "소유관사")} Mann heißt Junho. Sie {blank("haben", "동사")} eine Tochter.</p></div>""")}
    <p><b>22b</b> 내 가족(또는 좋아하는 가족 사진) 소개 5–6문장. 나이와 직업도 넣어요.</p>
    <textarea lang="de" data-persist="meine-familie" rows="5" placeholder="Das ist meine Familie. Das ist mein …" aria-label="가족 사진 설명"></textarea>
    <div class="table-wrap"><table><tbody>
      <tr><td>☐</td><td>여성·복수 가족 앞에는 <b lang="de">meine</b>를 썼나요?</td></tr>
      <tr><td>☐</td><td>나이와 직업은 <b lang="de">sein</b>으로 썼나요? (<span lang="de">Er ist 58.</span>)</td></tr>
      <tr><td>☐</td><td>직업 앞에 관사를 빼고 썼나요?</td></tr>
    </tbody></table></div>''', "output")

s3 += act("s3-teil-d", 23, "Teil D · 수진의 집에서 · 이야기 마무리", 5, f'''{track("2-06", "dlg-2-06", "저녁, Kochstraße 12의 2층(한국식 3층). 민준이 가방 속 사진을 들고 수진의 집에 와요.")}
    {fig("story-3-familie", "수진의 거실 소파에서 어른들이 민준의 휴대폰 사진을 들여다보는 동안, 어린 도윤이 탁자 밑에서 봉투에 크레용으로 그림을 그린다", "아무도 보지 못했어요…")}
{dialog("dlg-2-06", [
    stage("민준이 가방 속 편지를 탁자 위에 올려놓고, 휴대폰으로 찍은 사진을 보여 준다."),
    line("민준", "누나, 이 사진 좀 보세요. 가방 안에 있었어요. 어딘지 아세요?", "", lang=""),
    line("수진", "음… 오래된 사진이네. 교회 같은데? 우리도 이사 온 지 얼마 안 돼서 잘 모르겠어.", "", lang=""),
    line("태호", "사진 속 사람들, 아주 젊네. 언제 사진일까?", "", lang=""),
    line("하은", "Mama, ich habe Hunger!", "엄마, 배고파요!"),
    line("수진", "하은아, 집에서는 한국말!", "", lang=""),
    stage("모두가 웃는 사이, 도윤이 탁자 위 봉투를 집어 들고 탁자 밑으로 기어 들어가 크레용을 꺼낸다."),
    line("도윤", "그림 그려야지~", "", lang=""),
    stage("밤늦게 민준은 편지를 까맣게 잊은 채 WG로 돌아간다.")], cls="dialog ko", lang="ko")}
{ex("TD1", "23a", "맞으면 <b>r</b>, 틀리면 <b>f</b>", rf("td1", [
    ("민준은 편지를 수진의 집에 가져갔다.", "r", ""),
    ("수진은 사진 속 장소를 잘 안다.", "f", ""),
    ("도윤이 봉투에 그림을 그린다.", "r", ""),
    ("도윤이 탁자 위의 종이를 가져갔다.", "r", ""),
    ("민준은 편지도 챙겨서 돌아갔다.", "f", "")], lang="ko"))}
    <p><a href="#drei-bilder">3컷으로 이야기 다시 보기</a> → <a href="#tagebuch">민준의 일기</a> → <a href="#selbstcheck">자기 점검</a></p>''', "output")

s3 += homework("hw-3", "3차시 숙제 (60분)", [
    ("가족 단어와 숫자 21–100을 듣고 따라 하기 + 오늘의 문장 틀 ③ 외우기", 10),
    ("<b>H1 · H2</b> 가족 단어, 소유관사", 15),
    ("<b>H3 · H4 · H5</b> sein/haben, 숫자", 15),
    ("<b>H6</b> 읽기 – Oksana의 메시지", 5),
    ("<b>H7</b> 틀린 문장 고치기", 5),
    (ic("write") + "<b>제출</b>: 22b 가족 사진 설명을 다듬어 사진과 함께 제출", 10)],
    ex("H1", "H1", "알맞은 가족 단어를 쓰세요.", f"""      <ol lang="de">
        <li>Mein Vater und meine Mutter sind meine {blank("Eltern", "가족")}.</li>
        <li>Mein Bruder und meine Schwester sind meine {blank("Geschwister", "가족")}.</li>
        <li>Ein Sohn und eine Tochter sind zwei {blank("Kinder", "가족")}.</li>
        <li>Die Mutter von meiner Mutter ist meine {blank("Oma", "가족")}.</li>
        <li>Haeun sagt „Papa“. Sujin sagt „mein {blank("Mann", "가족")}“.</li>
      </ol>""") + "\n" + ex("H2", "H2", "알맞은 소유관사를 쓰세요.", f"""      <ol lang="de">
        <li>Ich habe eine Schwester. {blank("Meine", "소유관사")} Schwester heißt Jiyeon.</li>
        <li>Oksana hat einen Sohn. {blank("Ihr", "소유관사")} Sohn heißt Maksym.</li>
        <li>Taeho hat zwei Kinder. {blank("Seine", "소유관사")} Kinder heißen Haeun und Doyun.</li>
        <li>Wir haben eine WG. {blank("Unsere", "소유관사")} WG ist in der Kochstraße.</li>
        <li>Minjun, wie alt ist {blank("deine", "소유관사")} Mutter?</li>
        <li>Frau Schulze, wo wohnt {blank("Ihr", "소유관사")} Bruder?</li>
      </ol>""") + "\n" + ex("H3", "H3", "sein일까요, haben일까요?", f"""      <ol lang="de">
        <li>Doyun {sel("ist", ["ist", "hat"])} drei.</li>
        <li>Haeun {sel("hat", ["ist", "hat"])} einen Bruder.</li>
        <li>{sel("Sind", ["Sind", "Haben"])} Sie verheiratet?</li>
        <li>Wir {sel("haben", ["sind", "haben"])} keine Kinder.</li>
        <li>Wie alt {sel("seid", ["seid", "habt"])} ihr?</li>
      </ol>""") + "\n" + ex("H4", "H4", "숫자를 독일어로 쓰세요.", f"""      <ol lang="de">
        <li>23 → {blank("dreiundzwanzig", "23", ci=True)}</li>
        <li>38 → {blank("achtunddreißig", "38", ci=True)}</li>
        <li>46 → {blank("sechsundvierzig", "46", ci=True)}</li>
        <li>70 → {blank("siebzig", "70", ci=True)}</li>
        <li>89 → {blank("neunundachtzig", "89", ci=True)}</li>
      </ol>""") + "\n" + ex("H5", "H5", "계산해서 숫자로 쓰세요.", f"""      <ol lang="de">
        <li>zwanzig + fünfzehn = {blank("35", "답", digits=True)}</li>
        <li>dreißig + zweiunddreißig = {blank("62", "답", digits=True)}</li>
        <li>hundert – einundzwanzig = {blank("79", "답", digits=True)}</li>
        <li>vierzig + siebenundvierzig = {blank("87", "답", digits=True)}</li>
      </ol>""") + "\n" + ex("H6", "H6", "Oksana가 수진에게 보낸 메시지예요. 맞으면 <b>r</b>, 틀리면 <b>f</b>", f"""      <div class="box" lang="de"><p>Hallo Sujin! Wie geht's? Morgen ist der Geburtstag von Maksym. Er ist dann sechzehn! Meine Mutter ist auch hier in Leipzig. Sie ist 67 und spricht kein Deutsch. Haben Haeun und Doyun Zeit? Wir machen eine Party. Liebe Grüße, Oksana</p></div>
      <p class="muted">morgen = 내일 · der Geburtstag = 생일 · dann = 그때</p>
""" + rf("h6", [("Maksym ist morgen sechzehn Jahre alt.", "r", ""), ("Oksanas Mutter wohnt in der Ukraine.", "f", ""), ("Oksanas Mutter ist 67 Jahre alt.", "r", ""), ("Sie spricht gut Deutsch.", "f", ""), ("Oksana fragt: Haben Haeun und Doyun Zeit?", "r", "")])) + "\n" + ex("H7", "H7", "틀린 곳을 고쳐 문장 전체를 다시 쓰세요.", f"""      <ol lang="de">
        <li>Ich habe 26 Jahre alt. → {blank("Ich bin 26 Jahre alt.", "고친 문장", "full")}</li>
        <li>Das ist mein Mutter. → {blank("Das ist meine Mutter.", "고친 문장", "full")}</li>
        <li>Er ist ein Ingenieur. → {blank("Er ist Ingenieur.", "고친 문장", "full")}</li>
        <li>Das sind mein Kinder. → {blank("Das sind meine Kinder.", "고친 문장", "full")}</li>
      </ol>"""))

# =====================================================================
# 부록
# =====================================================================
keys = [("Das ist ein Bett. Das Bett ist alt.", "이건 침대야. 침대는 낡았어."), ("Das ist kein Tisch. Das Zimmer ist nicht groß.", "이건 탁자가 아니야. 방은 크지 않아."),
        ("Wie heißt das auf Deutsch?", "이걸 독일어로 뭐라고 해요?"), ("Im Koffer sind zwei Packungen Tabletten.", "가방 안에 약 두 통이 있어."),
        ("Wir sind Detektive! – Ihr seid verrückt!", "우리는 탐정이야! – 너희 못 말려!"), ("Habt ihr eine Idee?", "너희 생각 있어?"),
        ("Ich habe einen Bruder und eine Schwester.", "나는 형(오빠)과 누나(언니)가 한 명씩 있어."), ("Das ist meine Familie. Mein Mann heißt Taeho.", "이건 우리 가족이에요. 제 남편 이름은 태호예요."),
        ("Wie alt sind Sie? – Ich bin 38 Jahre alt.", "몇 살이세요? – 38살이에요."), ("Was sind Sie von Beruf? – Ich bin Krankenschwester.", "직업이 뭐예요? – 간호사예요.")]
krows = "".join(f'<tr><td lang="de" data-say>{a}</td><td>{b}</td></tr>' for a, b in keys)
def vt(rows): return '<div class="table-wrap"><table><tbody>' + "".join(f'<tr><td lang="de" data-say>{a}</td><td>{b}</td></tr>' for a, b in rows) + "</tbody></table></div>"

anh = f'''  <section class="card" id="saetze">
    <h3>{ic("speak")}이번 과의 핵심 문장 10 · 말하기 카드</h3>
    <p>▶를 눌러 듣고, 한국어 뜻만 보고 독일어로 말할 수 있는지 확인해 보세요.</p>
    <div class="table-wrap"><table><tbody>{krows}</tbody></table></div>
  </section>

  <section class="card" id="grammatik">
    <h3>{ic("book")}<span lang="de">Grammatik</span> · 2과 문법 한눈에</h3>
    <div class="sum-grid">
      <div class="sum">
        <p class="sum-title">① 관사 (1격)</p>
        <div class="table-wrap"><table lang="de"><tbody>
          <tr><td></td><td>{g("m", "m")}</td><td>{g("f", "f")}</td><td>{g("n", "n")}</td><td>{g("pl", "p")}</td></tr>
          <tr><td lang="ko">그</td><td>der</td><td>die</td><td>das</td><td>die</td></tr>
          <tr><td lang="ko">하나의</td><td>ein</td><td>eine</td><td>ein</td><td>–</td></tr>
          <tr><td lang="ko">없는</td><td>kein</td><td>keine</td><td>kein</td><td>keine</td></tr>
          <tr><td lang="ko">나의</td><td>mein</td><td>meine</td><td>mein</td><td>meine</td></tr>
        </tbody></table></div>
        <p class="muted">명사 → <b>kein</b> · 형용사 → <b>nicht</b> · 대명사: der → er, die → sie, das → es</p>
      </div>
      <div class="sum">
        <p class="sum-title">② 동사 – 이제 모든 주어</p>
        <div class="table-wrap"><table lang="de"><tbody>
          <tr><td>ich</td><td>wohne</td><td>bin</td><td>habe</td></tr>
          <tr><td>du</td><td>wohnst</td><td>bist</td><td>hast</td></tr>
          <tr><td>er/sie/es</td><td>wohnt</td><td>ist</td><td>hat</td></tr>
          <tr><td>wir</td><td>wohnen</td><td>sind</td><td>haben</td></tr>
          <tr><td>ihr</td><td>wohnt</td><td>seid</td><td>habt</td></tr>
          <tr><td>sie/Sie</td><td>wohnen</td><td>sind</td><td>haben</td></tr>
        </tbody></table></div>
      </div>
      <div class="sum">
        <p class="sum-title">③ 복수형</p>
        <p lang="de">-e · ¨-e · -(e)n · ¨-er · -s · –</p>
        <p class="muted">관사는 언제나 die · 단어와 함께 외우기</p>
        <p class="sum-title">④ 나이·직업은 sein</p>
        <p lang="de">Ich <b>bin</b> 38. · Ich <b>bin</b> Krankenschwester.</p>
        <p class="sum-title">⑤ 숫자 21–99</p>
        <p lang="de">ein-und-zwanzig (1 + 20)</p>
      </div>
    </div>
  </section>

  <section class="card" id="landeskunde">
    <h3>{ic("flag")}<span lang="de">Landeskunde</span> · 독일 생활 팁</h3>
    <ul>
      <li><b lang="de">WG (Wohngemeinschaft)</b>: 여러 사람이 집 하나를 나눠 쓰는 것. 방은 각자, 부엌·욕실은 함께. 독일 대학생의 약 4분의 1이 WG에 살아요. 새 룸메이트를 뽑을 때는 <span lang="de">WG-Casting</span>(면접)을 하기도 해요.</li>
      <li><b>층 세는 법이 달라요!</b> 땅과 같은 높이의 층은 <span lang="de">das Erdgeschoss (EG)</span>, 그 위가 <span lang="de">der 1. Stock</span>. 그래서 수진이 사는 한국식 3층은 독일어로 <span lang="de">im 2. Stock</span>이에요.</li>
      <li><b lang="de">Integrationskurs</b>: 이민자를 위한 국가 지원 과정. 독일어 수업(보통 600시간)과 독일 사회·역사·법을 배우는 <span lang="de">Orientierungskurs</span>로 이루어져요. 마지막에 B1 시험(<span lang="de">DTZ</span>)을 봐요.</li>
      <li><b lang="de">Kita (Kindertagesstätte)</b>: 1–6세 아이가 다니는 어린이집·유치원. 만 1세부터 자리를 받을 법적 권리가 있지만, 대도시에서는 자리가 모자라 미리 신청해야 해요. 선생님은 <span lang="de">Erzieher/Erzieherin</span>이라고 불러요.</li>
    </ul>
  </section>

  <section class="card" id="wortschatz">
    <h3>{ic("write")}<span lang="de">Wortschatz</span> · 단어장</h3>
    <div class="wgrid">
    <div>
    <h4>집과 가구</h4>
    {vt([("das Zimmer, -", "방"), ("die Küche, -n · das Bad, ¨-er", "부엌 · 욕실"), ("das Bett, -en · der Tisch, -e · der Stuhl, ¨-e", "침대 · 탁자 · 의자"), ("der Schrank, ¨-e · das Regal, -e", "옷장 · 책장"), ("die Lampe, -n · der Spiegel, -", "전등 · 거울"), ("das Sofa, -s · der Teppich, -e", "소파 · 양탄자"), ("der Schreibtisch, -e", "책상")])}
    </div>
    <div>
    <h4>형용사</h4>
    {vt([("groß ↔ klein", "큰 ↔작은"), ("alt ↔ neu", "낡은 ↔ 새"), ("hell ↔ dunkel", "밝은 ↔ 어두운"), ("teuer ↔ billig", "비싼 ↔ 싼"), ("laut ↔ ruhig", "시끄러운 ↔ 조용한"), ("schön · modern · bequem", "예쁜 · 현대적인 · 편한"), ("verrückt · voll", "미친(못 말리는) · 가득 찬")])}
    </div>
    <div>
    <h4>가족</h4>
    {vt([("der Vater · die Mutter · die Eltern", "아버지 · 어머니 · 부모"), ("der Sohn · die Tochter · das Kind, -er", "아들 · 딸 · 아이"), ("der Bruder · die Schwester · die Geschwister", "형제 · 자매 · 형제자매"), ("der Mann · die Frau", "남편 · 아내"), ("der Opa · die Oma", "할아버지 · 할머니"), ("verheiratet", "결혼한")])}
    </div>
    <div>
    <h4>사람과 직업</h4>
    {vt([("der Lehrer / die Lehrerin", "선생님"), ("der Ingenieur / die Ingenieurin", "엔지니어"), ("die Krankenschwester", "간호사"), ("der Apotheker / die Apothekerin", "약사"), ("der Student / die Studentin", "대학생"), ("Was sind Sie von Beruf?", "직업이 뭐예요?")])}
    </div>
    </div>
  </section>

  <section class="card" id="drei-bilder">
    <h3>{ic("book")}이번 과 이야기 · 3컷으로 다시 보기</h3>
    <div class="strip">
      <figure class="cut"><img src="{K.IMG}story-1-zimmer.webp" alt="민준의 텅 빈 방" loading="lazy"><figcaption><b>1</b> <span lang="de">Das ist dein Zimmer! Aber kein Tisch …</span><span class="ko">여기가 네 방이야! 그런데 탁자가 없네…</span></figcaption></figure>
      <figure class="cut"><img src="{K.IMG}story-2-abend.webp" alt="부엌에서 가방 속 물건을 살펴보는 세 사람" loading="lazy"><figcaption><b>2</b> <span lang="de">Was ist im Koffer? Wir sind Detektive!</span><span class="ko">가방 안에 뭐가 있지? 우리는 탐정!</span></figcaption></figure>
      <figure class="cut"><img src="{K.IMG}story-3-familie.webp" alt="수진의 집에서 도윤이 봉투를 가져가는 장면" loading="lazy"><figcaption><b>3</b> <span lang="de">Bei Familie Lee: Wo ist der Brief?</span><span class="ko">수진 가족의 집: 편지는 어디에?</span></figcaption></figure>
    </div>
    <p><b>말해 보기</b> 그림을 보며 이야기를 독일어로 말하고 녹음해 보세요. <span lang="de">(Das ist Minjuns Zimmer. Es ist … · Im Koffer sind … · Das ist Sujins Familie …)</span></p>
  </section>

  <section class="card" id="tagebuch">
    <h3>{ic("diary")}<span lang="de">Minjuns Tagebuch</span> · 민준의 일기 <button type="button" class="say-btn" data-play="diary-2" aria-label="일기 듣기">▶</button></h3>
    <div class="diary" lang="de" id="diary-2">
      <p class="date">2. Oktober</p>
''' + "\n".join(f'      <p data-say-seq>{de}<span class="ko" lang="ko">{ko}</span></p>' for de, ko in [
    ("Mein Zimmer ist groß und hell. Aber ich habe keinen Tisch!", "내 방은 크고 밝다. 그런데 탁자가 없다!"),
    ("Jonas und Lena sind nett. Wir sind jetzt Detektive.", "요나스와 레나는 친절하다. 우리는 이제 탐정이다."),
    ("Heute Abend war ich bei Sujin. Ihre Familie ist sehr nett. Doyun ist drei und sehr süß.", "오늘 저녁 수진 누나 집에 갔다. 가족이 아주 친절하다. 도윤이는 세 살이고 아주 귀엽다."),
    ("Jetzt bin ich in meinem Zimmer. Das Foto ist hier.", "지금 내 방이다. 사진은 여기 있다."),
    ("<b>Aber der Brief? Der Brief ist weg!</b>", "그런데 편지는? 편지가 없어졌다!")]) + f'''
    </div>
    <p class="muted">war = ~에 있었다(sein의 과거) – 7과에서 배워요.</p>
    <p class="next">→ 다음 과 · <span lang="de">Kapitel 3: Im Supermarkt</span><br><span class="muted">민준과 Lena의 첫 장보기. 외투 주머니에서 나온 작은 영수증 한 장이 새로운 단서가 되는데…</span></p>
  </section>

  <section class="card box mystery" id="fallakte">
    <h3>{ic("search")}<span lang="de">Fallakte</span> · 사건 수첩 <small>(이 기기에 자동 저장)</small></h3>
    <p>1과에서 쓴 내용에 이어서 써요. 모르는 칸은 비워 두세요!</p>
    <div class="table-wrap"><table lang="de"><tbody>
''' + "\n".join(f'      <tr><th>{a}<br><small lang="ko">{k}</small></th><td><input class="blank full" data-persist="{p}" aria-label="{k}"></td></tr>' for a, k, p in [
    ("Der Mantel ist …", "외투는 어때요?", "fall2-mantel"), ("Auf dem Foto sind …", "사진 속에는?", "fall2-foto"),
    ("Die Tabletten – für wen?", "약은 누구의 것일까?", "fall2-tabletten"), ("Wo ist der Brief jetzt?", "편지는 지금 어디에?", "fall2-brief"),
    ("Wer hat eine Idee?", "누가 도와줄 수 있을까?", "fall2-hilfe")]) + f'''
    </tbody></table></div>
    <p><b>나의 추리</b> (한국어도 좋아요) – 편지는 어디로 갔을까요?</p>
    <textarea data-persist="fall2-idee" rows="3" aria-label="나의 추리"></textarea>
  </section>

  <section class="card" id="selbstcheck">
    <h3>{ic("check")}<span lang="de">Das kann ich!</span> · 자기 점검</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>할 수 있어요</th><th class="c">{pic("k01/stimmung-1-sehr-gut", "잘해요", "mood-s")}</th><th class="c">{pic("k01/stimmung-2-gut", "괜찮아요", "mood-s")}</th><th class="c">{pic("k01/stimmung-4-nicht-so-gut", "연습 필요", "mood-s")}</th></tr></thead>
      <tbody>
''' + "\n".join(f'        <tr><td>{t}</td>' + "".join(f'<td class="c"><input type="radio" name="sc{i}" value="{v}" data-persist="k2sc{i}" aria-label="{l}"></td>' for v, l in [("3", "잘해요"), ("2", "괜찮아요"), ("1", "연습 필요")]) + "</tr>" for i, t in enumerate([
    "방과 가구 이름을 관사(der/die/das)와 함께 말할 수 있다.", "방과 물건이 어떤지 형용사로 설명할 수 있다.", "kein과 nicht로 부정할 수 있다.",
    "모르는 단어를 독일어로 물어볼 수 있다. (Wie heißt das auf Deutsch?)", "복수형을 알아보고 wir/ihr/sie 동사를 쓸 수 있다.",
    "가족을 소개하고 나이와 직업을 말할 수 있다.", "소유관사(mein, dein, sein, ihr …)를 쓸 수 있다.", "21–100 숫자를 말하고 알아들을 수 있다.",
    "방 소개 메시지와 가족 사진 설명을 쓸 수 있다."], 1)) + '''
      </tbody>
    </table></div>
  </section>
'''

# =====================================================================
# 페이지 조립
# =====================================================================
cast = "".join(f'<figure>{pic(k, n, "person")}<figcaption>{n}</figcaption></figure>' for k, n in [
    ("k01/person-minjun", "민준"), ("k01/person-jonas", "Jonas"), ("k01/person-lena", "Lena"), ("k01/person-sujin", "수진"), ("k02/person-taeho", "태호"),
    ("k01/person-haeun", "하은"), ("k02/person-doyun", "도윤"), ("k02/person-brandt", "Herr Brandt"), ("k02/person-amira", "Amira"), ("k02/person-oksana", "Oksana")])
goals = [("speak", "방과 가구를 관사와 함께 말하고 설명할 수 있어요.", "Das ist ein Bett. Das Bett ist alt."),
         ("speak", "없는 것을 말하고, 모르는 단어를 물어볼 수 있어요.", "Ich habe keinen Tisch. · Wie heißt das auf Deutsch?"),
         ("listen", "여럿에 대해 말할 수 있어요.", "Im Koffer sind … · Wir sind … · Ihr seid …"),
         ("family", "가족을 소개하고 나이와 직업을 말할 수 있어요.", "Das ist meine Mutter. Sie ist 55. Sie ist Lehrerin."),
         ("123", "21–100 숫자를 말하고 알아들을 수 있어요.", "einundzwanzig · achtunddreißig · hundert"),
         ("write", "방 소개 메시지와 가족 사진 설명을 쓸 수 있어요.", "Mein Zimmer ist … · Das ist meine Familie.")]
gcards = "".join(f'<div class="goal">{ic(i)}<div><p class="goal-ko">{k}</p><p class="goal-de" lang="de">{d}</p></div></div>' for i, k, d in goals)
plans = [("stunde-1", "1차시", "Das ist mein Zimmer.", "그림 · 가구 · Teil A 방 구경 · der/die/das · ein/kein", "형용사 · WG 광고 읽기 · 모르는 단어 묻기 · 내 방 소개"),
         ("stunde-2", "2차시", "Im Koffer sind …", "Teil B 가방 속 물건 · 복수형 · wir/ihr/sie", "haben · Lena의 방 듣기 · 방 소개 메시지 · 사건 메모"),
         ("stunde-3", "3차시", "Das ist meine Familie.", "Teil C 통합 과정 · 가족 · 소유관사 · 나이와 직업", "숫자 21–100 · 읽기 · 하은이의 통역 · 가족 사진 · Teil D")]
grams = [("명사의 성과 정관사", "der Tisch · die Lampe · das Bett", "남성 · 여성 · 중성 – 관사와 함께 외우기", "s1-moebel", "1차시"),
         ("부정관사 ein / eine", "Das ist <b>ein</b> Bett. → <b>Das</b> Bett ist alt.", "처음 말할 때 ein, 다시 말할 때 der", "s1-satz1", "1차시"),
         ("부정 kein / nicht", "Das ist <b>kein</b> Tisch. · Es ist <b>nicht</b> groß.", "명사는 kein · 형용사는 nicht", "s1-satz1", "1차시"),
         ("형용사 서술 용법 · 대명사 er/sie/es", "Der Schrank ist alt. → <b>Er</b> ist alt.", "형용사는 모양이 안 바뀜", "s1-adjektive", "1차시"),
         ("명사의 복수형", "Tisch → Tisch<b>e</b> · Lampe → Lampe<b>n</b> · Buch → B<b>ü</b>ch<b>er</b>", "복수 관사는 언제나 die", "s2-plural", "2차시"),
         ("wir · ihr · sie 동사 변화", "wir komm<b>en</b> · ihr komm<b>t</b> · sie komm<b>en</b> · wir <b>sind</b> · ihr <b>seid</b>", "모든 주어 완성", "s2-satz2", "2차시"),
         ("haben 동사", "ich habe · du ha<b>st</b> · er ha<b>t</b> · wir haben · ihr habt", "du, er에서 b가 빠짐", "s2-haben", "2·3차시"),
         ("소유관사 (1격)", "mein · dein · sein · ihr · unser · euer · Ihr", "여성·복수 앞에서 -e", "s3-satz3", "3차시"),
         ("나이와 직업은 sein", "Ich <b>bin</b> 38. · Ich <b>bin</b> Krankenschwester.", "직업 앞에 관사 없음", "s3-satz3", "3차시"),
         ("숫자 21–100", "einundzwanzig · dreißig · hundert", "한 자리 + und + 십의 자리", "s3-zahlen", "3차시")]
grc = "".join(f'<a class="gram-row" href="#{a}"><span class="gram-no">{i}</span><b>{n}</b><span class="gram-ex" lang="de">{e}</span><span class="gram-note">{note}</span><span class="gram-where">{w}</span></a>' for i, (n, e, note, a, w) in enumerate(grams, 1))
pc = "".join(f'<a class="plan" href="#{i}"><span class="stunde-no">{n}</span><b lang="de">{t}</b><span><small>1교시</small> {x}</span><span><small>2교시</small> {y}</span></a>' for i, n, t, x, y in plans)

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kapitel 2 · Meine WG, meine Familie</title>
<meta name="description" content="Der falsche Koffer – 독일어를 처음 배우는 학생을 위한 CEFR A1 통합형 교재 2과">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@300;400;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/textbook.css">
</head>
<body data-chapter="A1-02" data-level="A1">
<!-- icons:start -->{SPRITE}<!-- icons:end -->
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="kapitel-01.html#cover">{ic("suitcase")} <span class="lbl">Der falsche Koffer</span></a>
    <nav aria-label="차시 이동">
      <a href="kapitel-01.html#contents">목차</a><a href="#kapitel-2" data-tab="start">목표</a><a href="#stunde-1" data-tab="stunde-1">1차시</a><a href="#stunde-2" data-tab="stunde-2">2차시</a><a href="#stunde-3" data-tab="stunde-3">3차시</a><a href="#anhang" data-tab="anhang">부록</a>
    </nav>
    <button type="button" class="toggle" id="theme-toggle" aria-label="화면 테마">◐ <span class="lbl">자동</span></button>
  </div>
</header>

<div class="page">
<main>

<section class="hero" id="kapitel-2" data-panel="start">
  <div class="series">DER FALSCHE KOFFER · A1 · KAPITEL 2 · 집과 가족</div>
  <h1 lang="de">Meine WG, meine Familie</h1>
  <div class="meta">
    <div><b>이야기</b> 민준의 WG 첫날. 방에는 탁자도 의자도 없어요. 저녁에는 Jonas·Lena와 가방 속 물건을 하나씩 살펴보고, 수진은 통합 과정 첫 수업에서 가족을 소개해요. 그런데 그날 밤, 편지가 사라지는데…</div>
    <div><b>수업</b> 3차시(1주) · 1차시 = 1교시 50분 + 2교시 50분 · 차시마다 숙제 60분</div>
  </div>
  <div class="cast" aria-label="등장인물">{cast}</div>
</section>

<section id="ziele" class="card" data-panel="start">
  <h2>{ic("target")}이번 과가 끝나면</h2>
  <div class="goal-grid">{gcards}</div>
  <h3>{ic("book")}이번 과에서 배우는 문법</h3>
  <div class="gram-list">{grc}</div>
  <h3>이번 주 수업 · 3차시</h3>
  <div class="plan-grid">{pc}</div>
</section>

{stunde("stunde-1", "1", "Das ist mein Zimmer.", "", s1)}
{stunde("stunde-2", "2", "Im Koffer sind …", "", s2)}
{stunde("stunde-3", "3", "Das ist meine Familie.", "", s3)}
<section id="anhang" class="stunde" data-panel="anhang">
  <div class="stunde-head"><span class="stunde-no">부록</span><h2>복습과 숙제용</h2></div>
{anh}
</section>

</main>
</div>

<footer>
  Der falsche Koffer · A1 Kapitel 2 · CEFR 기반 통합형 독일어 교재 · 등장인물과 병원·회사는 가상이며, 역사적 사실과 장소는 실제에 맞춰 서술합니다.
</footer>

<script src="../assets/js/textbook.js"></script>
</body>
</html>
'''
# 숙제 문제 번호가 차시마다 H1부터 시작하므로 data-ex는 차시별로 구분
def _hw_ids(h):
    def fix(m):
        no = m.group(1)
        return re.sub(r'data-ex="(H\d)"', rf'data-ex="hw{no}-\1"', m.group(0))
    return re.sub(r'<section class="box homework" id="hw-(\d)">.*?</section>', fix, h, flags=re.S)
page = _hw_ids(page)

# ---- 녹음 파일 연결 (assets/audio/k02/*.mp3가 있으면) ----
AUD = "../assets/audio/k02/"
_AUD_DIR = "/home/user/CFER/web/assets/audio/k02/"
def _attach_audio(h):
    def dlg(m):
        did, n = m.group(1), [0]
        def ln(mm):
            n[0] += 1
            fn = f"{did}-{n[0]}.mp3"
            return mm.group(0) + (f' data-audio="{AUD}{fn}"' if os.path.exists(_AUD_DIR + fn) else "")
        return re.sub(r'<span class="text"', ln, m.group(0))
    h = re.sub(r'<div class="dialog[^"]*" id="([^"]+)".*?\n    </div>', dlg, h, flags=re.S)
    k = [0]
    def lis(m):
        k[0] += 1
        fn = f"lis-{k[0]}.mp3"
        return m.group(0)[:-1] + (f' data-audio="{AUD}{fn}"' if os.path.exists(_AUD_DIR + fn) else "") + ">"
    h = re.sub(r'<span class="lis" data-say="[^"]+">', lis, h)
    return h
open(OUT, "w", encoding="utf-8").write(_attach_audio(page))
print("written", len(page))
