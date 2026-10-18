/* =========================================================
   Der falsche Koffer – 공통 교재 스크립트
   - 연습 문제 채점 (data-answer 기반)
   - 독일어/한국어 음성 읽기 (Web Speech API)
   - 차시별 보기, 사건 수첩 저장
   모든 기능은 HTML의 data- 속성만 보고 동작하므로,
   웹앱으로 옮길 때 같은 마크업을 그대로 쓸 수 있다.
   ========================================================= */
(function () {
  "use strict";

  var chapterId = document.body.getAttribute("data-chapter") || "chapter";

  /* ---------- 저장소 (실패해도 페이지는 동작) ---------- */
  var store = {
    get: function (key) {
      try { return window.localStorage.getItem("dfk:" + chapterId + ":" + key); } catch (e) { return null; }
    },
    set: function (key, value) {
      try { window.localStorage.setItem("dfk:" + chapterId + ":" + key, value); } catch (e) { /* 무시 */ }
    },
    getGlobal: function (key) {
      try { return window.localStorage.getItem("dfk:" + key); } catch (e) { return null; }
    },
    setGlobal: function (key, value) {
      try { window.localStorage.setItem("dfk:" + key, value); } catch (e) { /* 무시 */ }
    }
  };


  /* ---------- 테마 (자동 → 밝게 → 어둡게) ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var themes = ["auto", "light", "dark"];
  var themeLabels = { auto: ["◐", "자동"], light: ["☼", "밝게"], dark: ["☾", "어둡게"] };
  function applyTheme(t) {
    if (t === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t);
    if (themeBtn) themeBtn.innerHTML = themeLabels[t][0] + ' <span class="lbl">' + themeLabels[t][1] + "</span>";
    store.setGlobal("theme", t);
  }
  if (themeBtn) {
    applyTheme(store.getGlobal("theme") || "auto");
    themeBtn.addEventListener("click", function () {
      var cur = store.getGlobal("theme") || "auto";
      applyTheme(themes[(themes.indexOf(cur) + 1) % themes.length]);
    });
  }

  /* ---------- 음성 읽기 ---------- */
  var synth = "speechSynthesis" in window ? window.speechSynthesis : null;
  var speakerPitch = {};
  function pitchFor(who) {
    if (!who) return 1;
    if (!(who in speakerPitch)) {
      var n = Object.keys(speakerPitch).length;
      speakerPitch[who] = [1, 0.8, 1.2, 0.9, 1.1, 0.7][n % 6];
    }
    return speakerPitch[who];
  }
  function utter(text, lang, who) {
    var u = new SpeechSynthesisUtterance(text);
    u.lang = lang === "ko" ? "ko-KR" : "de-DE";
    u.rate = lang === "ko" ? 1 : 0.85;
    u.pitch = pitchFor(who);
    return u;
  }
  function clearPlaying() {
    document.querySelectorAll(".say-btn.playing").forEach(function (b) { b.classList.remove("playing"); });
  }
  function speakQueue(items, btn) {
    if (!synth) return;
    synth.cancel();
    clearPlaying();
    if (btn) btn.classList.add("playing");
    items.forEach(function (it, i) {
      var u = utter(it.text, it.lang, it.who);
      if (i === items.length - 1) u.onend = u.onerror = clearPlaying;
      synth.speak(u);
    });
  }
  function textOf(el) {
    return (el.getAttribute("data-say") || el.textContent).replace(/\s+/g, " ").trim();
  }
  function langOf(el) {
    var l = el.closest("[lang]");
    return l && l.getAttribute("lang").indexOf("ko") === 0 ? "ko" : "de";
  }

  // 한 줄 읽기 버튼: .line 안의 [data-text] 또는 data-say 속성
  document.querySelectorAll(".line").forEach(function (line) {
    var textEl = line.querySelector(".text");
    if (!textEl || !synth) return;
    var b = document.createElement("button");
    b.className = "say-btn";
    b.type = "button";
    b.setAttribute("aria-label", "이 문장 듣기");
    b.textContent = "▶";
    b.addEventListener("click", function () {
      var who = line.querySelector(".who");
      speakQueue([{ text: textOf(textEl), lang: langOf(textEl), who: who && who.textContent }], b);
    });
    line.appendChild(b);
  });

  // 단어·표현 읽기: [data-say] 요소에 버튼 추가
  document.querySelectorAll("[data-say]:not(.line .text)").forEach(function (el) {
    if (!synth) return;
    var b = document.createElement("button");
    b.className = "say-btn";
    b.type = "button";
    b.setAttribute("aria-label", "듣기");
    b.textContent = "▶";
    b.style.marginLeft = ".3rem";
    b.style.width = b.style.height = "1.6rem";
    b.addEventListener("click", function () { speakQueue([{ text: textOf(el), lang: langOf(el) }], b); });
    // 표 칸·문단처럼 블록 요소면 안쪽 끝에, 인라인 요소면 바로 뒤에 붙인다
    if (/^(TD|TH|P|DIV|LI)$/.test(el.tagName)) el.appendChild(b);
    else el.insertAdjacentElement("afterend", b);
  });

  // 트랙 재생: [data-play="대화 id"] → 대화 전체를 순서대로 읽음
  document.querySelectorAll("[data-play]").forEach(function (btn) {
    if (!synth) { btn.disabled = true; btn.title = "이 브라우저는 음성 읽기를 지원하지 않습니다"; return; }
    btn.addEventListener("click", function () {
      var dlg = document.getElementById(btn.getAttribute("data-play"));
      if (!dlg) return;
      var items = [];
      dlg.querySelectorAll(".line, [data-say-seq]").forEach(function (line) {
        var t = line.querySelector(".text") || line;
        var who = line.querySelector(".who");
        items.push({ text: textOf(t), lang: langOf(t), who: who && who.textContent });
      });
      speakQueue(items, btn);
    });
  });

  /* ---------- 연습 문제 ---------- */
  function norm(s, el) {
    s = (s || "").replace(/[‘’]/g, "'").replace(/\s+/g, " ").trim();
    s = s.replace(/[.!?]+$/, "").trim();
    if (el && el.hasAttribute("data-digits")) s = s.replace(/\D/g, "");
    if (el && el.hasAttribute("data-ci")) s = s.toLowerCase();
    return s;
  }
  function accepts(el, value) {
    var v = norm(value, el);
    return el.getAttribute("data-answer").split("|").some(function (a) { return norm(a, el) === v; });
  }

  function checkEx(ex) {
    var total = 0, right = 0;
    ex.querySelectorAll("input.blank[data-answer], select[data-answer]").forEach(function (el) {
      total++;
      var ok = accepts(el, el.value);
      el.classList.toggle("ok", ok);
      el.classList.toggle("bad", !ok);
      if (ok) right++;
    });
    ex.querySelectorAll("tr[data-answer]").forEach(function (tr) {
      total++;
      var checked = tr.querySelector("input[type=radio]:checked");
      var ok = !!checked && checked.value === tr.getAttribute("data-answer");
      tr.classList.toggle("ok", ok);
      tr.classList.toggle("bad", !ok);
      if (ok) right++;
    });
    var score = ex.querySelector(".score");
    if (score) {
      score.textContent = right + " / " + total + (right === total ? " · 모두 정답!" : "");
      score.classList.toggle("all", right === total);
    }
  }
  function showEx(ex) {
    ex.querySelectorAll("input.blank[data-answer], select[data-answer]").forEach(function (el) {
      el.value = el.getAttribute("data-answer").split("|")[0];
    });
    ex.querySelectorAll("tr[data-answer]").forEach(function (tr) {
      var r = tr.querySelector('input[type=radio][value="' + tr.getAttribute("data-answer") + '"]');
      if (r) r.checked = true;
    });
    checkEx(ex);
  }
  function resetEx(ex) {
    ex.querySelectorAll("input.blank, select").forEach(function (el) { el.value = ""; el.classList.remove("ok", "bad"); });
    ex.querySelectorAll("tr[data-answer]").forEach(function (tr) {
      tr.classList.remove("ok", "bad");
      tr.querySelectorAll("input[type=radio]").forEach(function (r) { r.checked = false; });
    });
    var score = ex.querySelector(".score");
    if (score) { score.textContent = ""; score.classList.remove("all"); }
  }

  document.querySelectorAll(".ex[data-check]").forEach(function (ex) {
    // 빈칸 너비를 정답 길이에 맞춤
    ex.querySelectorAll("input.blank[data-answer]").forEach(function (el) {
      if (!el.classList.contains("wide") && !el.classList.contains("full")) {
        var len = Math.max.apply(null, el.getAttribute("data-answer").split("|").map(function (a) { return a.length; }));
        el.style.width = Math.max(5, len + 2) + "ch";
      }
      el.setAttribute("autocomplete", "off");
      el.setAttribute("autocapitalize", "off");
      el.setAttribute("spellcheck", "false");
      el.addEventListener("keydown", function (e) { if (e.key === "Enter") checkEx(ex); });
    });
    var bar = document.createElement("div");
    bar.className = "ex-actions";
    bar.innerHTML =
      '<button type="button" class="btn" data-act="check">정답 확인</button>' +
      '<button type="button" class="btn ghost" data-act="show">정답 보기</button>' +
      '<button type="button" class="btn ghost" data-act="reset">다시 하기</button>' +
      '<span class="score" aria-live="polite"></span>';
    bar.addEventListener("click", function (e) {
      var act = e.target.getAttribute && e.target.getAttribute("data-act");
      if (act === "check") checkEx(ex);
      if (act === "show") showEx(ex);
      if (act === "reset") resetEx(ex);
    });
    ex.appendChild(bar);
  });

  /* ---------- 동사 주사위 게임 ---------- */
  var dice = document.getElementById("verb-dice");
  if (dice) {
    function face(n) { return '<svg class="ic" aria-hidden="true"><use href="#i-die-' + n + '"/></svg>'; }
    var subjects = ["ich", "du", "er / sie", "wir", "ihr", "sie / Sie"];
    var verbs = {
      wohnen: ["wohne", "wohnst", "wohnt", "wohnen", "wohnt", "wohnen"],
      kommen: ["komme", "kommst", "kommt", "kommen", "kommt", "kommen"],
      lernen: ["lerne", "lernst", "lernt", "lernen", "lernt", "lernen"],
      machen: ["mache", "machst", "macht", "machen", "macht", "machen"],
      "heißen": ["heiße", "heißt", "heißt", "heißen", "heißt", "heißen"],
      arbeiten: ["arbeite", "arbeitest", "arbeitet", "arbeiten", "arbeitet", "arbeiten"],
      sprechen: ["spreche", "sprichst", "spricht", "sprechen", "sprecht", "sprechen"]
    };
    var faceEl = dice.querySelector(".dice-face");
    var result = dice.querySelector(".dice-result");
    var answer = dice.querySelector(".dice-answer");
    var current = null;
    dice.querySelector("[data-act=roll]").addEventListener("click", function () {
      var n = Math.floor(Math.random() * 6);
      var names = Object.keys(verbs);
      var v = names[Math.floor(Math.random() * names.length)];
      current = { n: n, v: v };
      faceEl.innerHTML = face(n + 1);
      result.innerHTML = "<b lang=\"de\">" + subjects[n] + "</b> + <b lang=\"de\">" + v + "</b> → ?";
      answer.textContent = "";
    });
    dice.querySelector("[data-act=solve]").addEventListener("click", function () {
      if (!current) return;
      answer.textContent = subjects[current.n] + " " + verbs[current.v][current.n];
    });
  }


  /* ---------- ä ö ü ß 입력 버튼 ---------- */
  var keypad = document.createElement("div");
  keypad.className = "keypad";
  keypad.setAttribute("aria-label", "독일어 특수 문자 입력");
  ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"].forEach(function (ch) {
    var k = document.createElement("button");
    k.type = "button"; k.textContent = ch;
    k.addEventListener("mousedown", function (e) { e.preventDefault(); });   // 입력 칸 포커스 유지
    k.addEventListener("click", function () {
      var el = keypad._target;
      if (!el) return;
      var a = el.selectionStart, z = el.selectionEnd;
      el.value = el.value.slice(0, a) + ch + el.value.slice(z);
      el.selectionStart = el.selectionEnd = a + 1;
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.focus();
    });
    keypad.appendChild(k);
  });
  document.body.appendChild(keypad);
  document.addEventListener("focusin", function (e) {
    var el = e.target;
    var de = el.closest && el.closest('[lang="de"]');
    if ((el.matches && el.matches("input.blank, textarea")) && (de || el.getAttribute("lang") === "de")) {
      keypad._target = el; keypad.classList.add("show");
    }
  });
  document.addEventListener("focusout", function () {
    setTimeout(function () {
      if (!document.activeElement || !document.activeElement.matches("input.blank, textarea")) keypad.classList.remove("show");
    }, 150);
  });


  /* ---------- 차시별로 나눠 보기 (상단 버튼 = 탭) ---------- */
  var panelEls = Array.prototype.slice.call(document.querySelectorAll("[data-panel]"));
  if (panelEls.length) {
    var names = [];
    panelEls.forEach(function (e) { var n = e.getAttribute("data-panel"); if (names.indexOf(n) < 0) names.push(n); });
    var tabLinks = document.querySelectorAll("[data-tab]");
    var tabLabel = function (n) {
      var t = document.querySelector('[data-tab="' + n + '"]');
      return t ? t.textContent.trim() : n;
    };
    var showPanel = function (name) {
      if (names.indexOf(name) < 0) name = names[0];
      panelEls.forEach(function (e) { e.classList.toggle("panel-off", e.getAttribute("data-panel") !== name); });
      tabLinks.forEach(function (a) {
        if (a.getAttribute("data-tab") === name) a.setAttribute("aria-current", "page");
        else a.removeAttribute("aria-current");
      });
      store.set("panel", name);
      var tab = document.querySelector('[data-tab="' + name + '"]');
      if (tab) { try { history.replaceState(null, "", tab.getAttribute("href")); } catch (err) { /* 무시 */ } }
    };
    var jump = function (fn) {   // 부분을 바꿀 때는 부드러운 스크롤 없이 바로 이동
      var root = document.documentElement, old = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto"; fn(); root.style.scrollBehavior = old;
    };
    var goTo = function (hash) {
      var id = (hash || "").replace(/^#/, "");
      var target = id ? document.getElementById(id) : null;
      if (!target) { showPanel(store.get("panel") || names[0]); return; }
      var owner = target.closest("[data-panel]");
      var name = owner ? owner.getAttribute("data-panel") : names[0];
      showPanel(name);
      var first = panelEls.filter(function (e) { return e.getAttribute("data-panel") === name; })[0];
      jump(function () {
        if (target === first) window.scrollTo(0, 0);
        else target.scrollIntoView();
      });
    };
    // 화면 안의 모든 #링크: 해당 부분을 열고 이동
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var h = a.getAttribute("href");
      if (h.length < 2 || !document.getElementById(h.slice(1))) return;
      e.preventDefault();
      if (a.hasAttribute("data-tab")) { showPanel(a.getAttribute("data-tab")); jump(function () { window.scrollTo(0, 0); }); }
      else { goTo(h); try { history.replaceState(null, "", h); } catch (err) { /* 무시 */ } }
    });
    // 각 부분 끝에 이전 / 다음 버튼
    names.forEach(function (n, i) {
      var own = panelEls.filter(function (e) { return e.getAttribute("data-panel") === n; });
      var last = own[own.length - 1];
      var nav = document.createElement("div");
      nav.className = "panel-nav";
      if (i > 0) nav.innerHTML += '<button type="button" class="btn ghost" data-go="' + names[i - 1] + '">← ' + tabLabel(names[i - 1]) + "</button>";
      if (i < names.length - 1) nav.innerHTML += '<button type="button" class="btn" data-go="' + names[i + 1] + '">' + tabLabel(names[i + 1]) + " →</button>";
      nav.setAttribute("data-panel", n);
      last.insertAdjacentElement("afterend", nav);
      panelEls.push(nav);
    });
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-go]");
      if (!b) return;
      showPanel(b.getAttribute("data-go"));
      jump(function () { window.scrollTo(0, 0); });
    });
    goTo(location.hash);
  }


  /* ---------- 저장되는 입력 (사건 수첩, 자기 점검, 추리 메모) ---------- */
  document.querySelectorAll("[data-persist]").forEach(function (el) {
    var key = "p:" + el.getAttribute("data-persist");
    if (el.type === "radio") {
      if (store.get(key) === el.value) el.checked = true;
      el.addEventListener("change", function () { if (el.checked) store.set(key, el.value); });
    } else {
      var saved = store.get(key);
      if (saved !== null) el.value = saved;
      el.addEventListener("input", function () { store.set(key, el.value); });
    }
  });
})();
