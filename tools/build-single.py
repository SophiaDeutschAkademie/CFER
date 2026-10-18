# 챕터 HTML 하나에 CSS·JS·그림을 모두 넣어 web/dist/ 에 단일 파일로 저장
# 사용: python3 tools/build-single.py A1/kapitel-01.html
import re, base64, os, sys
WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
rel = sys.argv[1] if len(sys.argv) > 1 else "A1/kapitel-01.html"
base = os.path.dirname(os.path.join(WEB, rel))
s = open(os.path.join(WEB, rel), encoding="utf-8").read()
css = open(os.path.join(WEB, "assets/css/textbook.css"), encoding="utf-8").read()
js = open(os.path.join(WEB, "assets/js/textbook.js"), encoding="utf-8").read()

def uri(p):
    path = os.path.normpath(os.path.join(base, p))
    return "data:image/webp;base64," + base64.b64encode(open(path, "rb").read()).decode()

# 대화 아바타: 인물마다 한 번만 넣고 CSS 클래스로 재사용
pat = r'class="avatar" style="background-image:url\(\.\./assets/img/([^/]+)/person-([a-z]+)\.webp\)"'
people = sorted(set(re.findall(pat, s)))
s = re.sub(pat, r'class="avatar av-\2"', s)
extra = ":root{" + "".join(f"--p-{n}:url({uri(f'../assets/img/{d}/person-{n}.webp')});" for d, n in people) + "}"
extra += "".join(f".av-{n}{{background-image:var(--p-{n})}}" for _, n in people)

s = s.replace('<link rel="stylesheet" href="../assets/css/textbook.css">', "<style>\n" + css + "\n" + extra + "\n</style>")
s = s.replace('<script src="../assets/js/textbook.js"></script>', "<script>\n" + js + "\n</script>")
s = re.sub(r'src="(\.\./assets/img/[^"]+)"', lambda m: 'src="' + uri(m.group(1)) + '"', s)
s = s.replace('href="../index.html"', 'href="#"')
assert "../assets" not in s, "외부 파일 참조가 남아 있습니다"
out = os.path.join(WEB, "dist", os.path.basename(rel))
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w", encoding="utf-8").write(s)
print(out, round(len(s.encode()) / 1024), "KB")
