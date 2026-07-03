/* Research Facility — live semantic preset search demo.
   Ports the exact ranking from scripts/rf_search.py so the storefront proves
   the plugin's headline feature: type a vibe, get the right sound, instantly,
   all in the browser (no server, no network). */
(function () {
  const WORD = /[a-z0-9\-]+/g;
  const tokens = (s) => (s.toLowerCase().match(WORD) || []);

  let INDEX = null;

  function search(query, index, k) {
    k = k || 8;
    const q = tokens(query);
    if (!q.length) return [];
    const concepts = index.concepts || {};
    const catWords = index.category_words || {};
    const expanded = new Set();
    let wantedCat = null;
    for (const t of q) {
      (concepts[t] || []).forEach((e) => expanded.add(e));
      if (!wantedCat && catWords[t]) wantedCat = catWords[t];
    }
    const qset = new Set(q);
    const scored = [];
    for (const p of index.presets) {
      const ptok = new Set(p.tokens || []);
      const tagmood = new Set([...(p.tags || []), ...(p.mood || [])]);
      const nameTok = new Set(tokens(p.name || ""));
      let score = 0;
      qset.forEach((t) => { if (tagmood.has(t)) score += 3.0; });
      qset.forEach((t) => { if (nameTok.has(t)) score += 2.0; });
      if (wantedCat && p.category === wantedCat) score += 2.5;
      expanded.forEach((t) => { if (ptok.has(t)) score += 1.5; });
      if (score > 0) scored.push([score / Math.sqrt(q.length), p]);
    }
    scored.sort((a, b) => b[0] - a[0]);
    return scored.slice(0, k).map(([s, p]) => ({
      id: p.id, name: p.name, category: p.category, tags: p.tags, score: s,
      spectrum: p.spectrum || [], similar: p.similar || [],
    }));
  }

  // favourites (persisted) + id → preset lookup (built when the index loads)
  let BY_ID = {};
  let TOP_MOODS = [];       // most common tags, for the shelf mood filter
  let MOODF = new Set();    // active mood filters
  let FAV = new Set();
  try { FAV = new Set(JSON.parse(localStorage.getItem("rf-fav") || "[]")); } catch (e) {}
  function toggleFav(id, btn) {
    if (FAV.has(id)) { FAV.delete(id); } else { FAV.add(id); }
    try { localStorage.setItem("rf-fav", JSON.stringify([...FAV])); } catch (e) {}
    if (btn) { const on = FAV.has(id); btn.textContent = on ? "♥" : "♡"; btn.classList.toggle("on", on); }
  }
  function surpriseMe() {
    const ps = (INDEX && INDEX.presets) || [];
    if (!ps.length) return;
    const p = ps[Math.floor(Math.random() * ps.length)];
    const rows = [p, ...(p.similar || []).map((sid) => BY_ID[sid]).filter(Boolean)].map(toRow);
    render(rows, "similar", "Surprise — " + p.name);
    unlocked = true; playFile(p.id);   // audition it immediately
  }
  function showFavorites() {
    const rows = [...FAV].map((id) => BY_ID[id]).filter(Boolean).map(toRow);
    render(rows.length ? rows : [], "similar", "Your favourites (" + FAV.size + ")");
    if (!rows.length) {
      document.getElementById("rf-results").innerHTML =
        '<div class="rf-simhead"><span>Your favourites</span><button class="rf-back">← back to search</button></div>' +
        '<div class="rf-empty">no favourites yet — tap the heart on any sound</div>';
    }
  }
  function toRow(p) {
    return { id: p.id, name: p.name, category: p.category, tags: p.tags || [],
             spectrum: p.spectrum || [], similar: p.similar || [] };
  }
  function showSimilar(id) {
    const p = BY_ID[id];
    if (!p) return;
    const rows = (p.similar || []).map((sid) => BY_ID[sid]).filter(Boolean).map(toRow);
    render(rows, "similar", "Sounds like " + p.name);
  }

  // --- audition: one shared <audio>. Click to play; once unlocked, hovering a
  //     row auditions it (the "plays-itself" discovery loop). ---
  const audio = new Audio();
  let playingId = null;
  let unlocked = false;          // set after first user click (browser autoplay gate)
  let hoverTimer = null;
  function playFile(id) {
    audio.src = "audio/" + id + ".wav";
    audio.currentTime = 0;
    audio.play().catch(() => {});
    playingId = id;
    markPlaying(id);
  }
  function play(id) {
    unlocked = true;
    if (playingId === id && !audio.paused) { audio.pause(); playingId = null; markPlaying(null); return; }
    playFile(id);
  }
  function hoverAudition(id) {
    if (!unlocked || playingId === id) return;
    clearTimeout(hoverTimer);
    hoverTimer = setTimeout(() => playFile(id), 250);   // brief dwell before it plays
  }
  function hoverCancel() { clearTimeout(hoverTimer); }
  audio.addEventListener("ended", () => { playingId = null; markPlaying(null); });
  function markPlaying(id) {
    document.querySelectorAll(".rf-hit").forEach((el) => {
      el.classList.toggle("is-playing", el.dataset.id === id);
    });
  }

  function spectrumSVG(spectrum, color) {
    if (!spectrum || !spectrum.length) return "";
    const W = 88, H = 26, n = spectrum.length, bw = W / n;
    let bars = "";
    for (let i = 0; i < n; i++) {
      const h = Math.max(1, spectrum[i] * (H - 2));
      bars += `<rect x="${(i * bw).toFixed(1)}" y="${(H - h).toFixed(1)}" width="${(bw - 0.6).toFixed(1)}" height="${h.toFixed(1)}" fill="${color}" opacity="0.85"/>`;
    }
    return `<svg class="rf-spec" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" preserveAspectRatio="none">${bars}</svg>`;
  }

  function catColor(cat) {
    const v = getComputedStyle(document.documentElement)
      .getPropertyValue("--cat-" + cat).trim();
    return v || getComputedStyle(document.documentElement).getPropertyValue("--accent").trim() || "#888";
  }

  function rowHTML(r) {
    const c = catColor(r.category);
    const lic = r.license ? `<span class="rf-hit__lic" title="${r.origin || ""} · cleared for commercial use">${r.license}</span>` : "";
    return `<div class="rf-hit" data-id="${r.id}" style="--c:${c}">
      <span class="rf-hit__play" aria-hidden="true" title="hear it"></span>
      <span class="rf-hit__name">${r.name}${lic}</span>
      <span class="rf-hit__cat">${r.category}</span>
      <span class="rf-hit__tags">${(r.tags || []).slice(0, 4).join(" · ")}</span>
      <span class="rf-hit__spec">${spectrumSVG(r.spectrum, c)}</span>
      <button class="rf-hit__fav${FAV.has(r.id) ? " on" : ""}" data-fav="${r.id}" title="favourite" aria-label="favourite">${FAV.has(r.id) ? "♥" : "♡"}</button>
      <button class="rf-hit__sim" data-sim="${r.id}" title="more like this" aria-label="more like this">≈</button>
    </div>`;
  }

  function render(results, mode, header) {
    const box = document.getElementById("rf-results");
    if (!box) return;
    const isSimilar = mode === "similar";
    if (!isSimilar && (!mode || !mode.trim())) { renderShelf(); return; }
    if (!results.length) {
      box.innerHTML = '<div class="rf-empty">no match — try "warm pad", "glassy pluck", "deep sub"</div>';
      return;
    }
    const head = (mode === "similar" && header)
      ? `<div class="rf-simhead"><span>${header}</span><button class="rf-back">← back to search</button></div>` : "";
    box.innerHTML = head + results.map(rowHTML).join("");
  }

  // Browse the whole shelf when there's no query — discovery without typing.
  const CAT_ORDER = ["pads", "plucks", "basses", "leads", "textures"];
  function renderShelf() {
    const box = document.getElementById("rf-results");
    if (!box || !INDEX) { if (box) box.innerHTML = ""; return; }
    const matchMood = (p) => [...MOODF].every((m) => (p.tags || []).includes(m));
    const all = (INDEX.presets || []).filter(matchMood);
    const groups = {};
    all.forEach((p) => { (groups[p.category] = groups[p.category] || []).push(p); });
    const cats = CAT_ORDER.filter((c) => groups[c]).concat(Object.keys(groups).filter((c) => !CAT_ORDER.includes(c)));
    const moodBar = `<div class="rf-moods">` + TOP_MOODS.map((m) =>
      `<button class="rf-mood${MOODF.has(m) ? " on" : ""}" data-mood="${m}">${m}</button>`).join("") + `</div>`;
    const label = MOODF.size ? `${all.length} specimens · ${[...MOODF].join(" + ")}`
                             : `The shelf — ${INDEX.count} curated specimens, all yours`;
    box.innerHTML = `<div class="rf-shelfhead">${label}</div>` + moodBar +
      (all.length ? cats.map((cat) => {
        const col = catColor(cat);
        return `<div class="rf-shelfcat" style="--c:${col}">${cat} · ${groups[cat].length}</div>` +
          groups[cat].map(rowHTML).join("");
      }).join("") : `<div class="rf-empty">no specimen matches those moods together — try fewer</div>`);
  }

  function wire() {
    const input = document.getElementById("rf-query");
    if (!input) return;
    const run = () => render(INDEX ? search(input.value, INDEX) : [], input.value);
    input.addEventListener("input", run);
    window.__rfRerender = run;   // palette switch repaints cards in new colors
    document.querySelectorAll(".rf-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        if (chip.dataset.fav === "1") { showFavorites(); return; }
        if (chip.dataset.surprise === "1") { surpriseMe(); return; }
        input.value = chip.textContent; run(); input.focus();
      });
    });
    const box = document.getElementById("rf-results");
    if (box) box.addEventListener("click", (e) => {
      const back = e.target.closest(".rf-back");
      if (back) { run(); return; }
      const mood = e.target.closest(".rf-mood");
      if (mood) { const m = mood.dataset.mood; if (MOODF.has(m)) MOODF.delete(m); else MOODF.add(m); renderShelf(); return; }
      const fav = e.target.closest(".rf-hit__fav");
      if (fav) { e.stopPropagation(); toggleFav(fav.dataset.fav, fav); return; }
      const sim = e.target.closest(".rf-hit__sim");
      if (sim) { e.stopPropagation(); showSimilar(sim.dataset.sim); return; }
      const row = e.target.closest(".rf-hit");
      if (row && row.dataset.id) play(row.dataset.id);
    });
    if (box) {
      box.addEventListener("mouseover", (e) => {
        const row = e.target.closest(".rf-hit");
        if (row && row.dataset.id) hoverAudition(row.dataset.id);
      });
      box.addEventListener("mouseout", (e) => {
        if (e.target.closest(".rf-hit")) hoverCancel();
      });
    }
    run();   // show the full shelf immediately (discovery without typing)
  }

  fetch("search_index.json", { cache: "no-cache" })
    .then((r) => r.json())
    .then((d) => { INDEX = d; (d.presets || []).forEach((p) => { BY_ID[p.id] = p; });
      const freq = {};
      (d.presets || []).forEach((p) => (p.tags || []).forEach((t) => { freq[t] = (freq[t] || 0) + 1; }));
      const skip = new Set(["pad", "pluck", "bass", "lead", "texture", "default", "harmonic"]);
      TOP_MOODS = Object.keys(freq).filter((t) => !skip.has(t))
        .sort((a, b) => freq[b] - freq[a]).slice(0, 10);
      wire();
      const c = document.getElementById("rf-count");
      if (c) c.textContent = d.count; })
    .catch(() => {
      const box = document.getElementById("rf-results");
      if (box) box.innerHTML = '<div class="rf-empty">index not built — run scripts/build_search_index.py</div>';
    });
})();
