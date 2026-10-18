/* =========================================================
   Der falsche Koffer – 공통 교재 스크립트
   - 연습 문제 채점 (data-answer 기반)
   - 독일어/한국어 음성 읽기 (Web Speech API)
   - 교사 모드, 활동 타이머, 사건 수첩 저장
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

  /* ---------- 교사 모드 ---------- */
  var teacherBtn = document.getElementById("teacher-toggle");
  function setTeacher(on) {
    document.body.classList.toggle("teacher-on", on);
    if (teacherBtn) teacherBtn.setAttribute("aria-pressed", on ? "true" : "false");
    store.setGlobal("teacher", on ? "1" : "0");
  }
  if (teacherBtn) {
    setTeacher(store.getGlobal("teacher") === "1");
    teacherBtn.addEventListener("click", function () {
      setTeacher(!document.body.classList.contains("teacher-on"));
    });
  }

  /* ---------- 테마 (자동 → 밝게 → 어둡게) ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var themes = ["auto", "light", "dark"];
  var themeLabels = { auto: ["🌓", "자동"], light: ["☀️", "밝게"], dark: ["🌙", "어둡게"] };
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
      score.textContent = right + " / " + total + (right === total ? " 🎉" : "");
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
    var faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
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
    var face = dice.querySelector(".dice-face");
    var result = dice.querySelector(".dice-result");
    var answer = dice.querySelector(".dice-answer");
    var current = null;
    dice.querySelector("[data-act=roll]").addEventListener("click", function () {
      var n = Math.floor(Math.random() * 6);
      var names = Object.keys(verbs);
      var v = names[Math.floor(Math.random() * names.length)];
      current = { n: n, v: v };
      face.textContent = faces[n];
      result.innerHTML = "<b lang=\"de\">" + subjects[n] + "</b> + <b lang=\"de\">" + v + "</b> → ?";
      answer.textContent = "";
    });
    dice.querySelector("[data-act=solve]").addEventListener("click", function () {
      if (!current) return;
      answer.textContent = subjects[current.n] + " " + verbs[current.v][current.n];
    });
  }

  /* ---------- 활동 타이머 (교사 모드에서 시간 배지를 누르면 시작) ---------- */
  var timer = document.createElement("div");
  timer.className = "timer";
  timer.setAttribute("role", "timer");
  timer.innerHTML = '<span class="t-label"></span><span class="t-time"></span><button type="button" aria-label="타이머 닫기">✕</button>';
  document.body.appendChild(timer);
  var tId = null;
  function stopTimer() { clearInterval(tId); tId = null; timer.className = "timer"; }
  timer.querySelector("button").addEventListener("click", stopTimer);
  document.querySelectorAll(".time[data-min]").forEach(function (badge) {
    badge.setAttribute("title", "교사 모드에서 누르면 타이머 시작");
    badge.addEventListener("click", function () {
      if (!document.body.classList.contains("teacher-on")) return;
      stopTimer();
      var left = parseInt(badge.getAttribute("data-min"), 10) * 60;
      var h = badge.closest(".activity");
      var title = h && h.querySelector("h3");
      timer.querySelector(".t-label").textContent = title ? title.firstChild.textContent.trim().slice(0, 24) : "";
      function tick() {
        var m = Math.floor(left / 60), s = left % 60;
        timer.querySelector(".t-time").textContent = m + ":" + (s < 10 ? "0" : "") + s;
        if (left <= 0) { clearInterval(tId); timer.classList.add("done"); }
        left--;
      }
      timer.className = "timer show";
      tick();
      tId = setInterval(tick, 1000);
    });
  });

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
