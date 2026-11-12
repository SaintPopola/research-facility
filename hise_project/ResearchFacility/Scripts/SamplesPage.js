// ============================================================================
// SAMPLES (docs/21 Stage 1): a browser for an offline index of sounds on this
// Mac, matched to the host tempo and a chosen song key.
//
// The index (AppData/SampleBrowser/index.json, schema "sm.samples/1") is built
// by a private tool in AppData/tools (reindex.sh) and never ships with the
// plug-in. This code is source-agnostic: source names come from the index.
//
// Engine (verified at the HISE 4.1.0 tag, see docs/21):
// - "Sample Loops": TempoSynced stretch with a bar-exact SampleEnd per zone.
//   The stretcher learns the source BPM from NumQuarters at voice start. A
//   zone's own NumQuarters is cast to int at 4.1.0 (ModulatorSamplerSound::
//   updateInternalData), which cannot carry the sample-rate correction
//   (nq x device rate / file rate, as for Loop Lines), so zones leave it at 0
//   and the sampler's option value (a double) is set for each audition.
//   Root = slot - key shift moves pitch independently of speed.
// - "Sample Hits": classic resampling for one-shots.
// - "Sample Play": PLAY KEYS, the chosen sound across the keyboard.
// - Auditions go out on MIDI channel 15; SampleRouter.js starts them on the
//   next bar (loops) or beat (one-shots) while the host plays.
// - One sample map per page of 24 results: every load silences this instance
//   (KillStateHandler), so maps reload only on page, key, speed or feel changes.
// ============================================================================

const var SMP_DIR   = FileSystem.getFolder(FileSystem.AppData).getChildFile("SampleBrowser");
const var SMP_TOOLS = FileSystem.getFolder(FileSystem.AppData).getChildFile("tools");
const var SmpLoops = Synth.getSampler("Sample Loops");
const var SmpHits  = Synth.getSampler("Sample Hits");
const var SmpPlay  = Synth.getSampler("Sample Play");
const var SmpLoopsSynth = Synth.getChildSynth("Sample Loops");
const var SmpHitsSynth  = Synth.getChildSynth("Sample Hits");
const var SmpPlaySynth  = Synth.getChildSynth("Sample Play");
const var SmpTask = Engine.createBackgroundTask("Sample index");

const var SMP_CH = 15;
const var SMP_SLOT0 = 40;           // 24 slots, 40-63: Root stays in 0..127 for shifts -18..+17
const var SMP_PAGE = 24;            // results per sample map
const var SMP_ROWS = 12;            // rows visible in the RESULTS card
const var SMP_ROW_H = 26;
const var SMP_PACK = 8192;          // sort key = score * SMP_PACK + item index; scores stay < 200000 so keys fit int32
const var SMP_CAT = ["STARTER", "MELODY", "VOCAL", "808", "BASS", "DRUMS", "FX"];
const var SMP_CAT_INK = [0xFFB0205A, 0xFF2F5BC4, 0xFF8A3DB0, 0xFF4E3BA8, 0xFF00665A, 0xFFA23D1B, 0xFF59616B];
const var SMP_KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const var SMP_SORTS = ["BEST FIT", "FRESH", "RECENT", "RANDOM", "BPM", "KEY"];
const var SMP_SPEED_TXT = ["AUTO", "1/2x", "1x", "2x"];
const var SMP_SPEED_M = [0, 2, 1, 0.5];     // feel multiplier: NumQuarters x m (m = 2 plays half time)
const var SMP_FORM_TXT = ["LOOP", "ONE-SHOT", "ALL"];

const var SM = {
    "loaded": false, "missing": false, "busy": false, "built": "", "status": "",
    "items": [], "idx": {}, "srcIds": [], "srcLabels": [], "srcIx": {}, "srcOn": [],
    "genres": [], "topGenres": [], "genreOn": [], "packs": [],
    "cats": [1, 1, 1, 1, 0, 0, 0], "form": 2, "fitKey": true, "fitTempo": true,
    "favOnly": false, "unheard": false, "sort": 0, "query": "", "like": -1, "rnd": [],
    "songRoot": -1, "songMode": 1, "speed": 0, "semi": 0, "oct": 0, "level": 0,
    "res": [], "sel": -1, "top": 0,
    "page": -1, "gen": 0, "mk": -1, "mapDirty": false, "pageMul": [], "pageRate": 0,
    "want": -1, "wantSince": 0.0, "loopNq": -1.0, "playNq": -1.0, "playSlot": -1, "playIt": -1, "playLoop": false,
    "lastEvt": -1, "startAt": 0.0, "offAt": -1.0, "playedAt": 0.0,
    "fav": {}, "plays": {}, "hidden": {}, "over": {}, "hist": [], "saveAt": -1.0,
    "playKeys": -1, "playForm": -1, "playLo": -1, "playHi": -1, "pendingPlayId": "",
    "grid": "", "dragging": false, "hoverR": "", "hoverA": "", "hoverRow": -1, "tick": 0,
    "reindexDone": false, "reindexCode": 0
};

// ---------------------------------------------------------------- helpers
inline function smpRate()
{
    local sr = Engine.getSampleRate();
    if (sr <= 0) sr = 48000.0;
    return sr;
}

inline function smpHost()
{
    local b = Engine.getHostBpm();
    if (b < 40.0 || b > 300.0) b = 120.0;
    return b;
}

inline function smpKeyText(k, md)
{
    if (k < 0) return "";
    return SMP_KEYS[k] + (md == 1 ? "m" : "");
}

inline function smpFmtInt(n)
{
    local ni = Math.round(n);
    local s = "" + ni;
    if (ni >= 1000) s = Math.round(Math.floor(ni / 1000)) + "," + ("" + (1000 + ni % 1000)).substring(1, 4);
    return s;
}

// semitones that move an item into the song key (docs/21 KEY), plus PITCH and OCT
inline function smpShift(it)
{
    local us = SM.semi + SM.oct * 12;
    if (it.key < 0 || SM.songRoot < 0) return us;
    local tg = SM.songRoot;
    if (it.mode == 1 && SM.songMode == 0) tg = (SM.songRoot + 9) % 12;   // minor item, major song: relative minor
    if (it.mode == 0 && SM.songMode == 1) tg = (SM.songRoot + 3) % 12;   // major item, minor song: relative major
    local d = (tg - it.key + 12) % 12;
    if (d > 5) d = d - 12;
    return d + us;
}

// feel multiplier m: the stretch ratio host / (bpm * m) stays in 0.7 .. 1.45 (docs/21 TEMPO)
inline function smpFeel(it)
{
    if (it.f != 1 || it.bpm <= 0) return 1;
    if (SM.speed > 0) return SMP_SPEED_M[SM.speed];
    local r = smpHost() / it.bpm;
    local m = 1.0;
    local comp = smpRate() / it.sr;
    while (r / m > 1.45 && it.nq * m * 2 * comp <= 128) m = m * 2;
    while (r / m < 0.7 && it.nq * m / 2 >= 1) m = m / 2;
    return m;
}

inline function smpRatio(it)
{
    if (it.f != 1 || it.bpm <= 0) return 1.0;
    return smpHost() / (it.bpm * smpFeel(it));
}

inline function smpFeelText(m)
{
    if (m == 2) return "1/2x";
    if (m == 4) return "1/4x";
    if (m == 0.5) return "2x";
    if (m == 0.25) return "4x";
    return "";
}

inline function smpMatchText(it)
{
    local s = "";
    local sh = smpShift(it);
    if (it.f == 1) s = Math.round(smpHost()) + "";
    if (it.key >= 0 && SM.songRoot >= 0)
    {
        local tg = (it.key + sh - SM.semi - SM.oct * 12 + 24) % 12;
        s = s + (s == "" ? "" : " ") + smpKeyText(tg, it.mode);
    }
    if (sh != 0) s = s + (sh > 0 ? " +" : " ") + sh;
    if (it.f == 1)
    {
        local ft = smpFeelText(smpFeel(it));
        if (ft != "") s = s + " " + ft;
    }
    return s;
}

// ---------------------------------------------------------------- user data
inline function smpSaveSoon()
{
    SM.saveAt = Engine.getUptime() + 1.0;
}

inline function smpSaveUser()
{
    SM.saveAt = -1.0;
    if (!SMP_DIR.isDirectory()) return;
    local u = {"schema": "sm.samples.user/1", "fav": SM.fav, "plays": SM.plays, "hidden": SM.hidden,
               "over": SM.over, "hist": SM.hist,
               "view": {"cats": SM.cats, "form": SM.form, "fitKey": SM.fitKey, "fitTempo": SM.fitTempo, "sort": SM.sort}};
    SMP_DIR.getChildFile("user.json").writeObject(u);
}

inline function smpLoadUser()
{
    local f = SMP_DIR.getChildFile("user.json");
    if (!f.isFile()) return;
    local u = f.loadAsObject();
    if (!isDefined(u)) return;
    if (isDefined(u.fav)) SM.fav = u.fav;
    if (isDefined(u.plays)) SM.plays = u.plays;
    if (isDefined(u.hidden)) SM.hidden = u.hidden;
    if (isDefined(u.over)) SM.over = u.over;
    if (isDefined(u.hist)) SM.hist = u.hist;
    if (isDefined(u.view))
    {
        local vw = u.view;
        if (isDefined(vw.cats) && vw.cats.length == 7) SM.cats = vw.cats;
        if (isDefined(vw.form)) SM.form = vw.form;
        if (isDefined(vw.fitKey)) SM.fitKey = vw.fitKey;
        if (isDefined(vw.fitTempo)) SM.fitTempo = vw.fitTempo;
        if (isDefined(vw.sort)) SM.sort = Math.range(vw.sort, 0, SMP_SORTS.length - 1);
    }
}

inline function smpIsFav(ix)
{
    if (ix < 0) return false;
    return SM.fav[SM.items[ix].id] == 1;
}

inline function smpApplyOverride(ix)
{
    local it = SM.items[ix];
    local ov = SM.over[it.id];
    if (!isDefined(ov)) return;
    if (isDefined(ov.key)) { it.key = ov.key; it.kc = 3; }
    if (isDefined(ov.mode)) it.mode = ov.mode;
}

// ---------------------------------------------------------------- index
inline function smpLoadIndex()
{
    local f = SMP_DIR.getChildFile("index.json");
    local i = 0;
    SM.loaded = false;
    if (!f.isFile())
    {
        SM.missing = true;
        SM.status = "No sample index on this Mac yet.";
        return;
    }
    local d = f.loadAsObject();
    if (!isDefined(d) || !isDefined(d.items) || d.schema != "sm.samples/1")
    {
        SM.missing = true;
        SM.status = "The sample index could not be read: press RESCAN.";
        return;
    }
    SM.missing = false;
    SM.items = d.items;
    SM.built = d.built;
    SM.genres = d.genres;
    SM.packs = d.packs;
    SM.idx = {};
    SM.srcIds = d.source_ids;
    SM.srcLabels = [];
    SM.srcIx = {};
    SM.srcOn = [];
    for (i = 0; i < SM.srcIds.length; i++)
    {
        local sd = d.sources[SM.srcIds[i]];
        SM.srcLabels.push(sd.label);
        SM.srcIx[SM.srcIds[i]] = i;
        SM.srcOn.push(1);
    }
    smpLoadUser();
    local gc = [];
    for (i = 0; i < SM.genres.length; i++) gc.push(0);
    for (i = 0; i < SM.items.length; i++)
    {
        local it = SM.items[i];
        SM.idx[it.id] = i;
        smpApplyOverride(i);
        local gk = 0;
        for (gk = 0; gk < it.g.length; gk++) gc[it.g[gk]] = gc[it.g[gk]] + 1;
    }
    // GENRE chips: the 9 most common genres
    SM.topGenres = [];
    SM.genreOn = [];
    local pick = 0;
    for (pick = 0; pick < 9; pick++)
    {
        local best = -1;
        local bc = 0;
        for (i = 0; i < gc.length; i++)
        {
            if (gc[i] > bc && SM.topGenres.indexOf(i) < 0) { best = i; bc = gc[i]; }
        }
        if (best < 0) break;
        SM.topGenres.push(best);
        SM.genreOn.push(0);
    }
    SM.loaded = true;
    SM.page = -1;
    SM.status = "Indexed " + SM.built.replace("T", " ").substring(0, 16);
    smpRefilter(true);
    if (SM.pendingPlayId != "")
    {
        local pk = SM.idx[SM.pendingPlayId];
        SM.pendingPlayId = "";
        if (isDefined(pk)) smpSetPlayKeys(pk);
    }
}

inline function onSmpIndexLog(task, finished, data)
{
    // background thread: only hand the result over, the clock picks it up
    if (finished)
    {
        SM.reindexCode = data;
        SM.reindexDone = true;
    }
}

inline function smpRescan()
{
    local sh = SMP_TOOLS.getChildFile("reindex.sh");
    if (SM.busy) return;
    if (!sh.isFile())
    {
        SM.status = "No indexer installed in the plug-in's AppData/tools folder.";
        SmpRail.repaint();
        return;
    }
    SM.busy = true;
    SM.status = "Indexing your sounds (a minute or two) ...";
    SmpTask.runProcess("/bin/bash", [sh.toString(0)], onSmpIndexLog);
    SmpRail.repaint();
    SmpResults.repaint();
}

// ---------------------------------------------------------------- filter + sort
const var SMQ = {"terms": [], "neg": [], "bpm": 0, "key": -1, "mode": -1};

inline function smpParseQuery(q)
{
    local parts = q.toLowerCase().trim().split(" ");
    local i = 0;
    SMQ.terms = [];
    SMQ.neg = [];
    SMQ.bpm = 0;
    SMQ.key = -1;
    SMQ.mode = -1;
    for (i = 0; i < parts.length; i++)
    {
        local w = parts[i].trim();
        if (w == "") continue;
        if (w.charAt(0) == "-" && w.length > 1) { SMQ.neg.push(w.substring(1, w.length)); continue; }
        local nv = parseInt(w);
        if (("" + nv) == w && nv >= 55 && nv <= 200) { SMQ.bpm = nv; continue; }
        // key tokens: f, fm, f#min, bbmaj (one letter alone is too common to read as a key)
        local k0 = SMP_KEYS.indexOf(w.charAt(0).toUpperCase());
        if (k0 >= 0 && w.length >= 2)
        {
            local rest = w.substring(1, w.length);
            local kk = k0;
            if (rest.charAt(0) == "#") { kk = (k0 + 1) % 12; rest = rest.substring(1, rest.length); }
            else if (rest.charAt(0) == "b" && rest != "b") { kk = (k0 + 11) % 12; rest = rest.substring(1, rest.length); }
            local kmode = -2;
            if (rest == "") kmode = -1;
            if (rest == "m" || rest == "min" || rest == "minor") kmode = 1;
            if (rest == "maj" || rest == "major") kmode = 0;
            if (kmode > -2 && !(rest == "" && w.length < 2)) { SMQ.key = kk; SMQ.mode = kmode; continue; }
        }
        SMQ.terms.push(w);
    }
}

inline function smpPass(ix)
{
    local it = SM.items[ix];
    local j = 0;
    if (SM.hidden[it.id] == 1) return false;
    if (SM.srcOn[SM.srcIx[it.s]] != 1) return false;
    if (SM.cats.indexOf(1) >= 0 && SM.cats[it.c] != 1) return false;
    if (SM.form == 0 && it.f != 1) return false;
    if (SM.form == 1 && it.f != 0) return false;
    if (SM.favOnly && SM.fav[it.id] != 1) return false;
    if (SM.unheard && SM.plays[it.id] > 0) return false;
    if (SM.genreOn.indexOf(1) >= 0)
    {
        local hit = false;
        for (j = 0; j < SM.topGenres.length; j++)
            if (SM.genreOn[j] == 1 && it.g.indexOf(SM.topGenres[j]) >= 0) hit = true;
        if (!hit) return false;
    }
    if (SM.fitKey && SM.songRoot >= 0 && it.key >= 0 && Math.abs(smpShift(it) - SM.semi - SM.oct * 12) > 2) return false;
    if (SM.fitTempo && it.f == 1)
    {
        local rr = smpRatio(it);
        if (rr < 0.83 || rr > 1.2) return false;
    }
    for (j = 0; j < SMQ.terms.length; j++)
        if (it.q.indexOf(SMQ.terms[j]) < 0) return false;
    for (j = 0; j < SMQ.neg.length; j++)
        if (it.q.indexOf(SMQ.neg[j]) >= 0) return false;
    if (SMQ.bpm > 0)
    {
        if (it.bpm <= 0) return false;
        local bq = SMQ.bpm;
        local okb = Math.abs(it.bpm - bq) <= bq * 0.06 || Math.abs(it.bpm * 2 - bq) <= bq * 0.06 || Math.abs(it.bpm - bq * 2) <= bq * 0.12;
        if (!okb) return false;
    }
    if (SMQ.key >= 0)
    {
        if (it.key != SMQ.key) return false;
        if (SMQ.mode >= 0 && it.mode != SMQ.mode) return false;
    }
    return true;
}

inline function smpSortKey(ix)
{
    local it = SM.items[ix];
    local sh = Math.abs(smpShift(it) - SM.semi - SM.oct * 12);
    local fit = sh * 100;
    if (it.f == 1 && it.bpm > 0) fit = fit + Math.round(600 * Math.abs(Math.log(smpRatio(it)) / Math.log(2)));
    if (SM.sort == 0) return Math.min(fit, 199999);
    if (SM.sort == 1)
    {
        local pc = SM.plays[it.id];
        if (!isDefined(pc)) pc = 0;
        return Math.min(pc, 12) * 10000 + Math.min(fit, 9999);
    }
    if (SM.sort == 2) return Math.range(Math.round((2000000000 - it.add) / 3600), 0, 199999);   // hours before 2033
    if (SM.sort == 3) return SM.rnd[ix];
    if (SM.sort == 4) return it.bpm > 0 ? it.bpm * 10 : 9999;
    return (it.key < 0 ? 24 : it.key * 2 + Math.max(0, it.mode)) * 4000 + Math.min(fit, 3999);
}

inline function smpRefilter(keepSel)
{
    local keys = [];
    local i = 0;
    local selId = (SM.sel >= 0 && SM.sel < SM.res.length) ? SM.res[SM.sel] : -1;
    smpParseQuery(SM.query);
    if (SM.sort == 3 && SM.rnd.length != SM.items.length)
    {
        SM.rnd = [];
        for (i = 0; i < SM.items.length; i++) SM.rnd.push(Math.randInt(0, 199999));
    }
    if (SM.like >= 0)
    {
        // "more like this": the item, then its precomputed neighbours (filters still apply)
        local base = SM.items[SM.like];
        keys.push(SM.like);
        for (i = 0; i < base.sim.length; i++)
            if (smpPass(base.sim[i])) keys.push(base.sim[i]);
        SM.res = keys;
    }
    else
    {
        for (i = 0; i < SM.items.length; i++)
            if (smpPass(i)) keys.push(smpSortKey(i) * SMP_PACK + i);
        keys.sort();
        SM.res = [];
        for (i = 0; i < keys.length; i++) SM.res.push(keys[i] % SMP_PACK);
    }
    SM.sel = -1;
    if (keepSel && selId >= 0) SM.sel = SM.res.indexOf(selId);
    SM.top = SM.sel >= 0 ? Math.floor(SM.sel / SMP_ROWS) * SMP_ROWS : 0;
    SM.page = -1;               // the next audition loads the map for its page
    SmpRail.repaint();
    SmpResults.repaint();
    SmpAudition.repaint();
    Header.repaint();
}

// ---------------------------------------------------------------- sample maps
inline function smpZone(it, slot)
{
    local sh = smpShift(it);
    local z = {"FileName": it.p, "LoKey": slot, "HiKey": slot, "LoVel": 0, "HiVel": 127, "RRGroup": 1, "Root": slot - sh};
    local v = it.vol + SM.level;
    if (it.f == 1)
    {
        z.Volume = Math.min(18, Math.round(v + 6));                // the stretcher's output is x0.5
        z.SampleEnd = it.end;                                       // NumQuarters: see smpLoopNq
        z.LoopEnabled = 1;
        z.LoopStart = 0;
        z.LoopEnd = it.end;
        z.LoopXFade = 0;
    }
    else
    {
        z.Volume = Math.min(18, Math.round(v));
        z.Pitch = it.cents;
    }
    return z;
}

// quarters the stretcher must assume so the loop plays at host tempo: bars x 4 x feel,
// times device rate / file rate (4.1.0 plays the file at the device rate without
// resampling when it stretches, so the rate ratio only reaches the pitch)
inline function smpLoopNq(it)
{
    return Math.min(128.0, it.nq * smpFeel(it) * smpRate() / it.sr);
}

// set the option value for this loop; changing it kills the sampler's voices, so it
// only happens when the value moves, and the audition waits a moment before it starts
inline function smpSetNq(smp, nq)
{
    local o = smp.getTimestretchOptions();
    o.Mode = "TempoSynced";
    o.SkipLatency = true;
    o.Tonality = 0.17;
    o.NumQuarters = nq;
    smp.setTimestretchOptions(o);
}

inline function smpBuildPage(pg)
{
    local lz = [];
    local hz = [];
    local k = 0;
    local mf = "";
    SM.pageMul = [];
    for (k = 0; k < SMP_PAGE; k++)
    {
        local r = pg * SMP_PAGE + k;
        if (r >= SM.res.length) break;
        local it = SM.items[SM.res[r]];
        SM.pageMul.push(smpFeel(it));
        if (mf == "") mf = it.p;
        if (it.f == 1) lz.push(smpZone(it, SMP_SLOT0 + k));
        else hz.push(smpZone(it, SMP_SLOT0 + k));
    }
    // a marker zone on 100-115 tells the clock when THIS map (not the old one) is in
    SM.gen = (SM.gen + 1) % 16;
    SM.mk = -1;
    if (mf != "")
    {
        SM.mk = 100 + SM.gen;
        lz.push({"FileName": mf, "LoKey": SM.mk, "HiKey": SM.mk, "Root": SM.mk, "Volume": -100});
        hz.push({"FileName": mf, "LoKey": SM.mk, "HiKey": SM.mk, "Root": SM.mk, "Volume": -100});
    }
    SmpLoops.loadSampleMapFromJSON(lz);
    SmpHits.loadSampleMapFromJSON(hz);
    SM.page = pg;
    SM.pageRate = smpRate();
    SM.mapDirty = false;
}

inline function smpMapReady()
{
    if (SM.mk < 0) return true;
    return SmpLoops.isNoteNumberMapped(SM.mk) && SmpHits.isNoteNumberMapped(SM.mk);
}

// tempo, rate or key changes: does the loaded page still match?
inline function smpPageStale()
{
    local k = 0;
    if (SM.page < 0) return false;
    if (SM.pageRate != smpRate()) return true;
    for (k = 0; k < SM.pageMul.length; k++)
    {
        local r = SM.page * SMP_PAGE + k;
        if (r >= SM.res.length) return true;
        if (smpFeel(SM.items[SM.res[r]]) != SM.pageMul[k]) return true;
    }
    return false;
}

// ---------------------------------------------------------------- audition
inline function smpStopAudition()
{
    if (SM.playSlot >= 0) Synth.noteOffFromUI(SMP_CH, SM.playSlot);
    SM.playSlot = -1;
    SM.playIt = -1;
    SM.offAt = -1.0;
    SM.want = -1;
    SmpAudition.repaint();
    SmpResults.repaint();
}

inline function smpEnsureVisible()
{
    if (SM.sel < 0) return;
    if (SM.sel < SM.top || SM.sel >= SM.top + SMP_ROWS) SM.top = Math.floor(SM.sel / SMP_ROWS) * SMP_ROWS;
}

inline function smpNoteHistory(ix)
{
    local id = SM.items[ix].id;
    local pc = SM.plays[id];
    if (!isDefined(pc)) pc = 0;
    SM.plays[id] = pc + 1;
    if (SM.hist.length == 0 || SM.hist[SM.hist.length - 1] != id) SM.hist.push(id);
    if (SM.hist.length > 100) SM.hist.removeElement(0);
    smpSaveSoon();
}

inline function smpPlayRes(r)
{
    if (r < 0 || r >= SM.res.length) return;
    smpStopAudition();
    SM.sel = r;
    smpEnsureVisible();
    local pg = Math.floor(r / SMP_PAGE);
    if (pg != SM.page || SM.mapDirty) smpBuildPage(pg);
    local wit = SM.items[SM.res[r]];
    local wantNq = smpLoopNq(wit);
    if (wit.f == 1 && Math.abs(wantNq - SM.loopNq) > 0.0001)
    {
        smpSetNq(SmpLoops, wantNq);
        SM.loopNq = wantNq;
    }
    SM.want = r;
    SM.wantSince = Engine.getUptime();
    smpNoteHistory(SM.res[r]);
    SmpResults.repaint();
    SmpAudition.repaint();
    Header.repaint();
}

inline function smpStep(d)
{
    if (SM.res.length == 0) return;
    local r = SM.sel < 0 ? 0 : Math.range(SM.sel + d, 0, SM.res.length - 1);
    smpPlayRes(r);
}

inline function smpStartWanted()
{
    local r = SM.want;
    local it = SM.items[SM.res[r]];
    local slot = SMP_SLOT0 + r % SMP_PAGE;
    SM.want = -1;
    Globals.smpSnap = it.f == 1 ? 16 : 4;
    SM.lastEvt = Globals.smpEvt;
    Synth.playNoteFromUI(SMP_CH, slot, 100);
    SM.playSlot = slot;
    SM.playIt = SM.res[r];
    SM.playLoop = it.f == 1;
    SM.playedAt = Engine.getUptime();
    SM.startAt = SM.playedAt;
    SM.offAt = it.f == 1 ? -1.0 : SM.playedAt + 30.0;    // set from the real start once the router has run
}

// ---------------------------------------------------------------- PLAY KEYS
const var PlayItem = Content.addLabel("PlayItem", 0, 0);
Content.setPropertiesFromJSON("PlayItem", {"saveInPreset": true, "visible": false, "width": 1, "height": 1, "editable": false, "text": ""});

inline function smpSetPlayKeys(ix)
{
    local o = SmpPlay.getTimestretchOptions();
    if (ix < 0)
    {
        SmpPlay.loadSampleMapFromJSON([]);
        SM.playKeys = -1;
        SM.playLo = -1;
        SM.playHi = -1;
        PlayItem.setValue("");
        refreshKeyTints();
        SmpAudition.repaint();
        return;
    }
    local it = SM.items[ix];
    local z = {"FileName": it.p, "LoVel": 0, "HiVel": 127, "RRGroup": 1};
    if (it.f == 1)
    {
        local pnq = smpLoopNq(it);
        if (SM.playForm != 1 || Math.abs(pnq - SM.playNq) > 0.0001)
        {
            smpSetNq(SmpPlay, pnq);
            SM.playNq = pnq;
        }
        z.LoKey = 48;
        z.HiKey = 72;
        z.Root = 60 - smpShift(it);            // C3 plays the song key
        z.Volume = Math.min(18, Math.round(it.vol + SM.level + 6));
        z.SampleEnd = it.end;
        z.LoopEnabled = 1;
        z.LoopStart = 0;
        z.LoopEnd = it.end;
        z.LoopXFade = 0;
        SM.playLo = 48;
        SM.playHi = 72;
    }
    else
    {
        if (SM.playForm != 0)
        {
            o.Mode = "Disabled";
            SmpPlay.setTimestretchOptions(o);
            SM.playNq = -1.0;
        }
        local rt = it.root >= 0 ? it.root : 60;
        z.LoKey = Math.max(0, rt - 24);
        z.HiKey = Math.min(127, rt + 24);
        z.Root = rt;
        z.Volume = Math.min(18, Math.round(it.vol + SM.level));
        z.Pitch = it.cents;
        SM.playLo = z.LoKey;
        SM.playHi = z.HiKey;
    }
    SM.playForm = it.f;
    SmpPlay.loadSampleMapFromJSON([z]);
    SM.playKeys = ix;
    PlayItem.setValue(it.id);
    refreshKeyTints();
    SmpAudition.repaint();
}

inline function onPlayItem(component, value)
{
    local v = "" + value;
    if (v == "" || v == "0") return;
    if (SM.loaded && isDefined(SM.idx[v])) smpSetPlayKeys(SM.idx[v]);
    else SM.pendingPlayId = v;
}
PlayItem.setControlCallback(onPlayItem);

// ---------------------------------------------------------------- song key + speed (saved with the DAW set)
const var SongKey = Content.addLabel("SongKey", 0, 0);
Content.setPropertiesFromJSON("SongKey", {"saveInPreset": true, "visible": false, "width": 1, "height": 1, "editable": false, "text": ""});
const var SampleSpeed = Content.addLabel("SampleSpeed", 0, 0);
Content.setPropertiesFromJSON("SampleSpeed", {"saveInPreset": true, "visible": false, "width": 1, "height": 1, "editable": false, "text": "0"});

inline function smpKeysChanged()
{
    // key, speed, pitch or level moved: the loaded page and PLAY KEYS no longer match
    SM.mapDirty = true;
    if (SM.loaded) smpRefilter(true);
    if (SM.playKeys >= 0) smpSetPlayKeys(SM.playKeys);
    if (SM.playSlot >= 0 && SM.sel >= 0) smpPlayRes(SM.sel);
}

inline function smpSetSongKey(root, md)
{
    SM.songRoot = root;
    SM.songMode = md;
    SongKey.setValue(root < 0 ? "" : SMP_KEYS[root] + "|" + (md == 1 ? "min" : "maj"));
    smpKeysChanged();
}

inline function onSongKey(component, value)
{
    local v = "" + value;
    local parts = v.split("|");
    SM.songRoot = -1;
    if (v != "" && v != "0" && parts.length == 2)
    {
        SM.songRoot = SMP_KEYS.indexOf(parts[0]);
        SM.songMode = parts[1] == "maj" ? 0 : 1;
    }
    SM.mapDirty = true;
}
SongKey.setControlCallback(onSongKey);

inline function onSampleSpeed(component, value)
{
    SM.speed = Math.range(parseInt("" + value), 0, 3);
    SM.mapDirty = true;
}
SampleSpeed.setControlCallback(onSampleSpeed);

// ---------------------------------------------------------------- favourites, fix key, similar
inline function smpToggleFav(ix)
{
    if (ix < 0) return;
    local id = SM.items[ix].id;
    if (SM.fav[id] == 1) SM.fav[id] = 0;
    else SM.fav[id] = 1;
    smpSaveSoon();
    if (SM.favOnly) smpRefilter(true);
    SmpResults.repaint();
    SmpAudition.repaint();
    Header.repaint();
}

inline function smpSelItem()
{
    if (SM.sel < 0 || SM.sel >= SM.res.length) return -1;
    return SM.res[SM.sel];
}

inline function smpFixKey(ix, root, md)
{
    if (ix < 0) return;
    local it = SM.items[ix];
    SM.over[it.id] = {"key": root, "mode": root < 0 ? -1 : md};
    it.key = root;
    it.mode = root < 0 ? -1 : md;
    it.kc = 3;
    smpSaveSoon();
    smpKeysChanged();
}

inline function smpSimilar(ix)
{
    if (ix < 0) return;
    SM.like = ix;
    smpRefilter(false);
    if (SM.res.length > 0) smpPlayRes(0);
}

inline function smpHide(ix)
{
    if (ix < 0) return;
    SM.hidden[SM.items[ix].id] = 1;
    smpSaveSoon();
    smpStopAudition();
    local keep = SM.sel;
    smpRefilter(false);
    if (SM.res.length > 0) { SM.sel = Math.min(keep, SM.res.length - 1); smpEnsureVisible(); }
}

inline function smpBack()
{
    // Backspace: the sound heard before this one, when it is in the current results
    local i = SM.hist.length - 2;
    for (i = SM.hist.length - 2; i >= 0; i--)
    {
        local ix = SM.idx[SM.hist[i]];
        if (isDefined(ix))
        {
            local r = SM.res.indexOf(ix);
            if (r >= 0)
            {
                SM.hist.removeElement(SM.hist.length - 1);
                smpPlayRes(r);
                SM.hist.removeElement(SM.hist.length - 1);   // smpPlayRes logged it again
                return;
            }
        }
    }
}

// ---------------------------------------------------------------- drawing helpers
inline function smpTape(g, w, title, right)
{
    g.setColour(T.tape);
    g.fillRoundedRectangle([0, 0, w, 20], 6.0);
    g.fillRect([0, 10, w, 10]);
    g.setColour(T.onTape);
    g.setFontWithSpacing(T.BOLD, 9, 0.16);
    g.drawAlignedText(title, [12, 0, 300, 20], "left");
    g.setColour(T.onTapeDim);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(right, [w - 312, 0, 300, 20], "right");
}

inline function smpPill(g, r, text, on, hot)
{
    g.setColour(on ? Colours.withAlpha(T.accent, 0.14) : (hot ? T.s3 : T.s2));
    g.fillRoundedRectangle(r, r[3] / 2);
    g.setColour(on ? T.accent : (hot ? T.lineHi : T.line));
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], r[3] / 2, 1.0);
    g.setColour(on ? T.accentInk : T.dim);
    g.setFontWithSpacing(T.BOLD, 8, 0.1);
    g.drawAlignedText(text, r, "centred");
}

inline function smpLcd(g, r, text)
{
    g.setColour(T.lcdBg);
    g.fillRoundedRectangle(r, 4.0);
    g.setColour(T.lcdBezel);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 4.0, 1.0);
    g.setColour(T.lcdText);
    g.setFont(T.BOLD, 13);
    g.drawAlignedText(text, r, "centred");
}

inline function smpWave(g, r, w, col)
{
    local k = 0;
    local bw = r[2] / 64.0;
    g.setColour(col);
    for (k = 0; k < 64; k++)
    {
        local hh = Math.max(1, w[k] / 99.0 * (r[3] - 2));
        g.fillRect([r[0] + k * bw + 0.5, r[1] + (r[3] - hh) / 2, Math.max(1, bw - 1), hh]);
    }
}

// ---------------------------------------------------------------- FILTER RAIL (left, 256 x 520)
const var SR_CHIP = [[12, 94], [70, 94], [128, 94], [186, 94], [12, 118], [70, 118], [128, 118]];
const var SmpRail = Content.addPanel("SmpRail", 16, 60);
Content.setPropertiesFromJSON("SmpRail", {"width": 256, "height": 520, "allowCallbacks": "Clicks & Hover", "visible": false});

inline function smpRailHit(x, y)
{
    local k = 0;
    if (SM.grid != "")
    {
        if (x >= 12 && x < 244 && y >= 88 && y < 196)
        {
            local col = Math.floor((x - 12) / 58);
            local row = Math.floor((y - 88) / 27);
            return "g" + (row * 4 + col);       // g0 = NONE, g1..g12 = C..B
        }
        return "gclose";
    }
    if (SM.query != "" && x >= 218 && x < 244 && y >= 28 && y < 54) return "clearq";
    if (y >= 62 && y < 84)
    {
        if (x >= 92 && x < 192) return "key";
        if (x >= 200 && x < 244) return "mode";
    }
    for (k = 0; k < 7; k++)
        if (x >= SR_CHIP[k][0] && x < SR_CHIP[k][0] + 56 && y >= SR_CHIP[k][1] && y < SR_CHIP[k][1] + 20) return "c" + k;
    if (y >= 152 && y < 174 && x >= 12 && x < 244) return "f" + Math.floor((x - 12) / 77.4);
    if (y >= 180 && y < 202)
    {
        if (x >= 12 && x < 124) return "fitkey";
        if (x >= 132 && x < 244) return "fittempo";
    }
    if (y >= 208 && y < 286 && x >= 12 && x < 244)
    {
        local gi = Math.floor((y - 208) / 26) * 3 + Math.floor((x - 12) / 78);
        if (gi < SM.topGenres.length) return "ge" + gi;
    }
    if (y >= 304 && y < 326)
    {
        for (k = 0; k < SM.srcIds.length && k < 2; k++)
            if (x >= 12 + k * 120 && x < 124 + k * 120) return "s" + k;
    }
    if (y >= 332 && y < 354 && x >= 12 && x < 244) return "sort";
    if (y >= 360 && y < 382)
    {
        if (x >= 12 && x < 124) return "favonly";
        if (x >= 132 && x < 244) return "unheard";
    }
    if (y >= 488 && y < 512)
    {
        if (x >= 128 && x < 184) return "rescan";
        if (x >= 188 && x < 244) return "clear";
    }
    return "";
}

SmpRail.setPaintRoutine(function(g)
{
    var k = 0;
    var hv = SM.hoverR;
    g.setColour(T.s1);
    g.fillRoundedRectangle([0, 0, 256, 520], 8.0);
    g.setColour(T.line);
    g.drawRoundedRectangle([0.5, 0.5, 255, 519], 6.0, 1.0);
    smpTape(g, 256, "SAMPLES", SM.loaded ? smpFmtInt(SM.items.length) + " SOUNDS" : "");

    // search well (the SmpSearch label sits inside it)
    g.setColour(T.well);
    g.fillRoundedRectangle([12, 28, 232, 26], 5.0);
    g.setColour(T.bevelDark);
    g.fillRect([16, 28, 224, 1]);
    if (SM.query == "")
    {
        g.setColour(T.faint);
        g.setFont(T.FONT, 12);
        g.drawAlignedText("Search  name, tag, 140, Fm, -drums", [20, 28, 210, 26], "left");
    }
    else
    {
        g.setColour(hv == "clearq" ? T.txt : T.dim);
        g.setFont(T.BOLD, 12);
        g.drawAlignedText("x", [218, 28, 26, 26], "centred");
    }

    // SONG row: host BPM (read-only), key picker, MAJ/MIN
    g.setColour(T.faint);
    g.setFontWithSpacing(T.FONT, 8, 0.16);
    g.drawAlignedText("SONG", [12, 54, 80, 8], "left");
    smpLcd(g, [12, 62, 72, 22], Math.round(smpHost()) + "");
    smpPill(g, [92, 62, 100, 22], SM.songRoot < 0 ? "KEY  NONE" : "KEY  " + SMP_KEYS[SM.songRoot], SM.songRoot >= 0, hv == "key");
    smpPill(g, [200, 62, 44, 22], SM.songMode == 1 ? "MIN" : "MAJ", false, hv == "mode");

    if (SM.grid != "")
    {
        // 13-cell key grid (NONE + 12 notes) over the filters
        g.setColour(T.s1);
        g.fillRoundedRectangle([8, 86, 240, 114], 6.0);
        g.setColour(T.lineHi);
        g.drawRoundedRectangle([8.5, 86.5, 239, 113], 6.0, 1.0);
        var cur = SM.grid == "song" ? SM.songRoot : (smpSelItem() >= 0 ? SM.items[smpSelItem()].key : -1);
        for (k = 0; k < 13; k++)
        {
            var gx = 12 + (k % 4) * 58;
            var gy = 90 + Math.floor(k / 4) * 27;
            smpPill(g, [gx, gy, 54, 22], k == 0 ? "NONE" : SMP_KEYS[k - 1], cur == k - 1, hv == "g" + k);
        }
        g.setColour(T.faint);
        g.setFont(T.FONT, 9);
        g.drawAlignedText(SM.grid == "song" ? "Song key" : "Fix this sound's key", [70, 172, 170, 22], "centred");
        return;
    }

    g.setColour(T.faint);
    g.setFontWithSpacing(T.FONT, 8, 0.16);
    g.drawAlignedText("TYPE", [12, 86, 80, 8], "left");
    for (k = 0; k < 7; k++)
    {
        var on = SM.cats[k] == 1;
        var cr = [SR_CHIP[k][0], SR_CHIP[k][1], 56, 20];
        g.setColour(on ? Colours.withAlpha(SMP_CAT_INK[k], 0.12) : (hv == "c" + k ? T.s3 : T.s2));
        g.fillRoundedRectangle(cr, 10.0);
        g.setColour(on ? SMP_CAT_INK[k] : T.line);
        g.drawRoundedRectangle([cr[0] + 0.5, cr[1] + 0.5, 55, 19], 10.0, 1.0);
        g.setColour(SMP_CAT_INK[k]);
        g.fillEllipse([cr[0] + 6, cr[1] + 7, 6, 6]);
        g.setColour(on ? T.txt : T.dim);
        g.setFontWithSpacing(T.BOLD, 8, 0.06);
        g.drawAlignedText(SMP_CAT[k], [cr[0] + 12, cr[1], 44, 20], "centred");
    }

    for (k = 0; k < 3; k++)
        smpPill(g, [12 + k * 78, 152, 74, 22], SMP_FORM_TXT[k], SM.form == k, hv == "f" + k);
    smpPill(g, [12, 180, 112, 22], "IN KEY", SM.fitKey, hv == "fitkey");
    smpPill(g, [132, 180, 112, 22], "IN TEMPO", SM.fitTempo, hv == "fittempo");

    for (k = 0; k < SM.topGenres.length; k++)
    {
        var gname = SM.genres[SM.topGenres[k]].toUpperCase();
        if (gname.length > 11) gname = gname.substring(0, 10) + ".";
        smpPill(g, [12 + (k % 3) * 78, 208 + Math.floor(k / 3) * 26, 74, 22], gname, SM.genreOn[k] == 1, hv == "ge" + k);
    }

    g.setColour(T.faint);
    g.setFontWithSpacing(T.FONT, 8, 0.16);
    g.drawAlignedText("SOURCE", [12, 294, 80, 8], "left");
    for (k = 0; k < SM.srcIds.length && k < 2; k++)
    {
        var sl = SM.srcLabels[k].toUpperCase();
        if (sl.length > 16) sl = sl.substring(0, 15) + ".";
        smpPill(g, [12 + k * 120, 304, 112, 22], sl, SM.srcOn[k] == 1, hv == "s" + k);
    }
    smpPill(g, [12, 332, 232, 22], "SORT  " + SMP_SORTS[SM.sort], false, hv == "sort");
    smpPill(g, [12, 360, 112, 22], "HEARTS ONLY", SM.favOnly, hv == "favonly");
    smpPill(g, [132, 360, 112, 22], "UNHEARD", SM.unheard, hv == "unheard");

    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawMultiLineText("Up / Down  step and play\nReturn  play     Esc  stop\nB  heart     M  more like this\nBackspace  previous sound", [12, 400], 232, "left", 2.0);

    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    g.drawAlignedText(SM.status, [12, 462, 232, 22], "left");
    g.setColour(T.txt);
    g.setFont(T.BOLD, 10);
    g.drawAlignedText(SM.loaded ? smpFmtInt(SM.res.length) + " of " + smpFmtInt(SM.items.length) : "", [12, 488, 112, 24], "left");
    smpPill(g, [128, 490, 56, 20], SM.busy ? "..." : "RESCAN", false, hv == "rescan");
    smpPill(g, [188, 490, 56, 20], "CLEAR", false, hv == "clear");
});

SmpRail.setMouseCallback(function(event)
{
    var h = smpRailHit(event.x, event.y);
    if (event.mouseUp) refocusKeys();
    if (event.clicked)
    {
        if (SM.grid != "")
        {
            if (h.indexOf("g") == 0 && h != "gclose")
            {
                var gk = parseInt(h.substring(1, h.length)) - 1;
                if (gk <= 11)
                {
                    if (SM.grid == "song") smpSetSongKey(gk, SM.songMode);
                    else smpFixKey(smpSelItem(), gk, SM.songMode);
                }
            }
            SM.grid = "";
        }
        else if (h == "clearq") { SmpSearch.set("text", ""); SM.query = ""; SM.like = -1; smpRefilter(false); }
        else if (h == "key") SM.grid = "song";
        else if (h == "mode") smpSetSongKey(SM.songRoot, 1 - SM.songMode);
        else if (h.indexOf("c") == 0 && h != "clear" && h != "clearq")
        {
            var ck = parseInt(h.substring(1, h.length));
            if (event.shiftDown) { SM.cats = [0, 0, 0, 0, 0, 0, 0]; SM.cats[ck] = 1; }   // shift: only this type
            else SM.cats[ck] = 1 - SM.cats[ck];
            smpRefilter(false);
            smpSaveSoon();
        }
        else if (h.indexOf("f") == 0 && h.length == 2) { SM.form = parseInt(h.substring(1, 2)); smpRefilter(false); smpSaveSoon(); }
        else if (h == "fitkey") { SM.fitKey = !SM.fitKey; smpRefilter(false); smpSaveSoon(); }
        else if (h == "fittempo") { SM.fitTempo = !SM.fitTempo; smpRefilter(false); smpSaveSoon(); }
        else if (h.indexOf("ge") == 0)
        {
            var gn = parseInt(h.substring(2, h.length));
            SM.genreOn[gn] = 1 - SM.genreOn[gn];
            smpRefilter(false);
        }
        else if (h.indexOf("s") == 0 && h.length == 2)
        {
            var sk = parseInt(h.substring(1, 2));
            SM.srcOn[sk] = 1 - SM.srcOn[sk];
            smpRefilter(false);
        }
        else if (h == "sort") { SM.sort = (SM.sort + 1) % SMP_SORTS.length; if (SM.sort == 3) SM.rnd = []; smpRefilter(true); smpSaveSoon(); }
        else if (h == "favonly") { SM.favOnly = !SM.favOnly; smpRefilter(true); }
        else if (h == "unheard") { SM.unheard = !SM.unheard; smpRefilter(true); }
        else if (h == "rescan") smpRescan();
        else if (h == "clear")
        {
            SM.cats = [1, 1, 1, 1, 0, 0, 0];
            SM.form = 2;
            SM.like = -1;
            SM.favOnly = false;
            SM.unheard = false;
            SM.query = "";
            SmpSearch.set("text", "");
            var gz = 0;
            for (gz = 0; gz < SM.genreOn.length; gz++) SM.genreOn[gz] = 0;
            for (gz = 0; gz < SM.srcOn.length; gz++) SM.srcOn[gz] = 1;
            smpRefilter(false);
        }
        this.repaint();
    }
    if (h != SM.hoverR)
    {
        SM.hoverR = h;
        this.repaint();
    }
});

const var SmpSearch = Content.addLabel("SmpSearch", 16 + 18, 60 + 29);
Content.setPropertiesFromJSON("SmpSearch", {
    "width": 196, "height": 24, "text": "", "editable": true, "updateEachKey": true, "multiline": false,
    "saveInPreset": false, "fontName": "Oxygen", "fontSize": 13, "alignment": "left", "visible": false,
    "textColour": 0xFF1C2127, "bgColour": 0x00000000, "itemColour": 0x00000000, "itemColour2": 0x00000000,
    "tooltip": "AND search over name, pack and tags. 140 = BPM, Fm = key, -drums excludes"
});

inline function onSmpSearch(component, value)
{
    FocusClock.stopTimer();
    SM.query = value;
    SM.like = -1;
    if (SM.loaded) smpRefilter(false);
}
SmpSearch.setControlCallback(onSmpSearch);

// ---------------------------------------------------------------- RESULTS (720 x 372)
const var SmpResults = Content.addPanel("SmpResults", 288, 60);
Content.setPropertiesFromJSON("SmpResults", {"width": 720, "height": 372, "allowCallbacks": "Clicks, Hover & Dragging", "visible": false});

SmpResults.setPaintRoutine(function(g)
{
    var k = 0;
    g.setColour(T.s1);
    g.fillRoundedRectangle([0, 0, 720, 372], 8.0);
    g.setColour(T.line);
    g.drawRoundedRectangle([0.5, 0.5, 719, 371], 6.0, 1.0);
    var title = SM.like >= 0 ? "LIKE  " + SM.items[SM.like].n.toUpperCase() : "RESULTS";
    var rng = SM.res.length == 0 ? "" : (SM.top + 1) + "-" + Math.min(SM.res.length, SM.top + SMP_ROWS) + " of " + smpFmtInt(SM.res.length);
    smpTape(g, 720, title, rng + "      ");
    g.setColour(T.onTapeDim);
    g.fillPath(ARROW_L, [690, 5, 6, 10]);
    g.fillPath(ARROW_R, [704, 5, 6, 10]);

    if (!SM.loaded)
    {
        g.setColour(T.txt);
        g.setFont(T.BOLD, 14);
        g.drawAlignedText(SM.busy ? "Indexing your sounds ..." : (SM.missing ? "No sample index yet" : "Loading the index ..."), [0, 120, 720, 24], "centred");
        g.setColour(T.dim);
        g.setFont(T.FONT, 11);
        g.drawAlignedText(SM.status, [0, 148, 720, 20], "centred");
        if (SM.missing && !SM.busy) smpPill(g, [300, 180, 120, 28], "BUILD INDEX", true, SM.hoverA == "build");
        return;
    }

    g.setColour(T.faint);
    g.setFontWithSpacing(T.FONT, 8, 0.14);
    g.drawAlignedText("NAME", [128, 24, 200, 16], "left");
    g.drawAlignedText("TYPE", [368, 24, 60, 16], "left");
    g.drawAlignedText("ORIGINAL", [480, 24, 70, 16], "left");
    g.drawAlignedText("PLAYS AS", [556, 24, 90, 16], "left");

    var now = Engine.getUptime();
    for (k = 0; k < SMP_ROWS; k++)
    {
        var r = SM.top + k;
        if (r >= SM.res.length) break;
        var ix = SM.res[r];
        var it = SM.items[ix];
        var y = 44 + k * SMP_ROW_H;
        var sel = r == SM.sel;
        if (sel)
        {
            g.setColour(T.s2);
            g.fillRect([4, y, 712, SMP_ROW_H]);
            g.setColour(T.accent);
            g.fillRect([4, y, 3, SMP_ROW_H]);
        }
        else if (SM.hoverRow == r)
        {
            g.setColour(T.s3);
            g.fillRect([4, y, 712, SMP_ROW_H]);
        }
        // state LED: queued (warn) until the bar line, playing (glow)
        var led = T.frameHi;
        if (SM.playIt == ix) led = now < SM.startAt ? T.warn : T.glow;
        if (SM.want == r) led = T.warn;
        g.setColour(T.glass);
        g.fillEllipse([12, y + 8, 10, 10]);
        g.setColour(led);
        g.fillEllipse([14, y + 10, 6, 6]);
        g.setColour(T.glass);
        g.fillRoundedRectangle([32, y + 5, 88, 16], 3.0);
        smpWave(g, [34, y + 6, 84, 14], it.w, Colours.withAlpha(T.glow, 0.85));
        g.setColour(T.txt);
        g.setFont(sel ? T.BOLD : T.FONT, 12);
        g.drawAlignedText(it.n, [128, y, 236, SMP_ROW_H], "left");
        g.setColour(SMP_CAT_INK[it.c]);
        g.fillEllipse([368, y + 10, 6, 6]);
        g.setFontWithSpacing(T.BOLD, 8, 0.08);
        g.drawAlignedText(SMP_CAT[it.c], [378, y, 56, SMP_ROW_H], "left");
        g.setColour(T.dim);
        g.drawAlignedText(it.f == 1 ? "LOOP" : "HIT", [436, y, 40, SMP_ROW_H], "left");
        g.setFont(T.MONO, 11);
        var orig = (it.f == 1 && it.bpm > 0 ? it.bpm + " " : "") + smpKeyText(it.key, it.mode) + (it.kc == 1 ? "?" : "");
        g.drawAlignedText(orig, [480, y, 74, SMP_ROW_H], "left");
        var mt = smpMatchText(it);
        g.setColour(it.key < 0 && it.f == 0 ? T.faint : T.accentInk);
        g.drawAlignedText(it.key < 0 && SM.songRoot >= 0 ? (it.f == 1 ? "-> " + Math.round(smpHost()) + "  no key" : "no key") : (mt == "" ? "" : "-> " + mt), [556, y, 98, SMP_ROW_H], "left");
        g.setColour(SM.srcIx[it.s] == 0 ? T.lineHi : T.accent);
        g.fillEllipse([660, y + 10, 6, 6]);
        var fav = SM.fav[it.id] == 1;
        g.setColour(T.heart);
        if (fav) g.fillPath(HEART, [682, y + 7, 13, 12]);
        else if (SM.hoverRow == r) g.drawPath(HEART, [682, y + 7, 13, 12], 1.2);
    }
    if (SM.res.length == 0)
    {
        g.setColour(T.dim);
        g.setFont(T.FONT, 12);
        g.drawAlignedText("Nothing matches. Turn off IN KEY / IN TEMPO or clear the search.", [0, 160, 720, 24], "centred");
    }
});

SmpResults.setMouseCallback(function(event)
{
    var row = event.y >= 44 ? Math.floor((event.y - 44) / SMP_ROW_H) : -1;
    var r = (row >= 0 && row < SMP_ROWS) ? SM.top + row : -1;
    if (r >= SM.res.length) r = -1;
    if (event.mouseUp)
    {
        SM.dragging = false;
        refocusKeys();
    }
    if (!SM.loaded)
    {
        var hb = (event.x >= 300 && event.x < 420 && event.y >= 180 && event.y < 208) ? "build" : "";
        if (event.clicked && hb == "build") smpRescan();
        if (hb != SM.hoverA) { SM.hoverA = hb; this.repaint(); }
        return;
    }
    // DRAG: the original file into the host (the file is already on disk)
    if (event.drag && !SM.dragging)
    {
        var drow = event.mouseDownY >= 44 ? Math.floor((event.mouseDownY - 44) / SMP_ROW_H) : -1;
        var dr = SM.top + drow;
        if (drow >= 0 && drow < SMP_ROWS && dr < SM.res.length && (Math.abs(event.dragX) > 4 || Math.abs(event.dragY) > 4))
        {
            SM.dragging = true;
            this.startExternalFileDrag(SM.items[SM.res[dr]].p, false, function() { SM.dragging = false; });
        }
        return;
    }
    if (event.clicked && event.y < 20 && event.x >= 684)
    {
        SM.top = event.x < 700 ? Math.max(0, SM.top - SMP_ROWS) : (SM.top + SMP_ROWS < SM.res.length ? SM.top + SMP_ROWS : SM.top);
        this.repaint();
        return;
    }
    if (event.clicked && r >= 0)
    {
        if (event.x >= 676 && event.x < 700) smpToggleFav(SM.res[r]);
        else if (r == SM.sel && SM.playSlot >= 0) smpStopAudition();
        else smpPlayRes(r);
    }
    if (r != SM.hoverRow)
    {
        SM.hoverRow = r;
        this.repaint();
    }
});

// ---------------------------------------------------------------- AUDITION (720 x 148)
const var SmpAudition = Content.addPanel("SmpAudition", 288, 440);
Content.setPropertiesFromJSON("SmpAudition", {"width": 720, "height": 148, "allowCallbacks": "Clicks, Hover & Dragging", "visible": false});

inline function smpAudHit(x, y)
{
    if (y >= 92 && y < 114)
    {
        if (x >= 12 && x < 172) return "sp" + Math.floor((x - 12) / 40);
        if (x >= 180 && x < 228) return "pitch-";
        if (x >= 228 && x < 276) return "pitch+";
        if (x >= 284 && x < 316) return "oct-";
        if (x >= 316 && x < 348) return "oct+";
        if (x >= 444 && x < 484) return "lvl-";
        if (x >= 484 && x < 524) return "lvl+";
    }
    if (y >= 120 && y < 142)
    {
        if (x >= 12 && x < 108) return "playkeys";
        if (x >= 116 && x < 200) return "similar";
        if (x >= 208 && x < 292) return "fixkey";
    }
    if (x >= 444 && x < 708 && y >= 116 && y < 144) return "drag";
    return "";
}

SmpAudition.setPaintRoutine(function(g)
{
    var ix = smpSelItem();
    var it = ix >= 0 ? SM.items[ix] : 0;
    var hv = SM.hoverA;
    var now = Engine.getUptime();
    g.setColour(T.s1);
    g.fillRoundedRectangle([0, 0, 720, 148], 8.0);
    g.setColour(T.line);
    g.drawRoundedRectangle([0.5, 0.5, 719, 147], 6.0, 1.0);
    smpTape(g, 720, "NOW PLAYING", ix >= 0 ? it.n.toUpperCase() : "PICK A SOUND");
    var playing = SM.playIt >= 0 && SM.playIt == ix;
    g.setColour(playing ? (now < SM.startAt ? T.warn : T.glow) : T.frameHi);
    g.fillEllipse([104, 7, 6, 6]);

    g.setColour(T.glass);
    g.fillRoundedRectangle([12, 28, 420, 56], 5.0);
    if (ix < 0)
    {
        g.setColour(T.glassDim);
        g.setFont(T.FONT, 11);
        g.drawAlignedText("Click a sound, or press Up / Down", [12, 28, 420, 56], "centred");
        return;
    }
    smpWave(g, [16, 32, 412, 48], it.w, Colours.withAlpha(T.glow, 0.75));
    var b = 0;
    if (it.f == 1 && it.bars > 1)
    {
        g.setColour(T.glassLine);
        for (b = 1; b < it.bars; b++) g.fillRect([16 + 412 * b / it.bars, 30, 1, 52]);
    }
    if (playing && now >= SM.startAt)
    {
        var len = it.f == 1 ? it.nq * smpFeel(it) * 60.0 / smpHost() : it.dur;
        var ph = len > 0 ? ((now - SM.startAt) % len) / len : 0;
        if (it.f == 0) ph = Math.min(1.0, (now - SM.startAt) / Math.max(0.05, it.dur));
        g.setColour(T.glowCore);
        g.fillRect([16 + 412 * ph, 30, 2, 52]);
    }
    smpLcd(g, [444, 28, 128, 26], ((it.f == 1 && it.bpm > 0) ? it.bpm + "  " : "") + (it.key >= 0 ? smpKeyText(it.key, it.mode) : "NO KEY"));
    smpLcd(g, [580, 28, 128, 26], smpMatchText(it) == "" ? "AS IS" : smpMatchText(it));
    g.setColour(T.faint);
    g.setFontWithSpacing(T.FONT, 8, 0.14);
    g.drawAlignedText("SOURCE", [444, 56, 128, 12], "centred");
    g.drawAlignedText("PLAYS AS", [580, 56, 128, 12], "centred");
    g.drawAlignedText(SM.packs[it.pk].n.toUpperCase() + "   /   " + SM.srcLabels[SM.srcIx[it.s]].toUpperCase(), [444, 70, 264, 14], "centred");

    var sp = 0;
    for (sp = 0; sp < 4; sp++)
        smpPill(g, [12 + sp * 40, 92, 38, 22], SMP_SPEED_TXT[sp], SM.speed == sp, hv == "sp" + sp);
    drawStepper(g, [180, 92, 96, 22], "PITCH " + (SM.semi > 0 ? "+" : "") + SM.semi, hv == "pitch-" || hv == "pitch+");
    drawStepper(g, [284, 92, 64, 22], (SM.oct > 0 ? "+" : "") + SM.oct, hv == "oct-" || hv == "oct+");
    smpPill(g, [356, 92, 76, 22], "REPEAT", false, false);
    g.setColour(Colours.withAlpha(T.s1, 0.6));
    g.fillRoundedRectangle([356, 92, 76, 22], 11.0);
    drawStepper(g, [444, 92, 80, 22], (SM.level > 0 ? "+" : "") + SM.level + " dB", hv == "lvl-" || hv == "lvl+");

    smpPill(g, [12, 120, 96, 22], SM.playKeys == ix ? "ON KEYS" : "PLAY KEYS", SM.playKeys == ix, hv == "playkeys");
    smpPill(g, [116, 120, 84, 22], "SIMILAR", SM.like == ix, hv == "similar");
    smpPill(g, [208, 120, 84, 22], "FIX KEY", false, hv == "fixkey");
    smpPill(g, [300, 120, 84, 22], "+ STACK", false, false);
    g.setColour(Colours.withAlpha(T.s1, 0.6));
    g.fillRoundedRectangle([300, 120, 84, 22], 11.0);

    // DRAG chip: the original file; it says what the host must do to match
    g.setColour(hv == "drag" ? T.capHi : T.cap);
    g.fillRoundedRectangle([444, 116, 264, 28], 6.0);
    g.setColour(T.onTapeDim);
    var gd = 0;
    for (gd = 0; gd < 3; gd++)
    {
        g.fillEllipse([456, 122 + gd * 6, 3, 3]);
        g.fillEllipse([462, 122 + gd * 6, 3, 3]);
    }
    var sh = smpShift(it);
    var dtxt = "DRAG ORIGINAL";
    if (it.f == 1) dtxt = dtxt + "   warp on";
    if (sh != 0) dtxt = dtxt + "   transpose " + (sh > 0 ? "+" : "") + sh;
    g.setColour(T.onTape);
    g.setFontWithSpacing(T.BOLD, 9, 0.1);
    g.drawAlignedText(dtxt, [474, 116, 230, 28], "left");
});

SmpAudition.setMouseCallback(function(event)
{
    var h = smpAudHit(event.x, event.y);
    var ix = smpSelItem();
    if (event.mouseUp)
    {
        SM.dragging = false;
        refocusKeys();
    }
    if (event.drag && !SM.dragging && ix >= 0 && smpAudHit(event.mouseDownX, event.mouseDownY) == "drag")
    {
        SM.dragging = true;
        this.startExternalFileDrag(SM.items[ix].p, false, function() { SM.dragging = false; });
        return;
    }
    if (event.clicked && ix >= 0)
    {
        if (h.indexOf("sp") == 0)
        {
            SM.speed = parseInt(h.substring(2, 3));
            SampleSpeed.setValue("" + SM.speed);
            smpKeysChanged();
        }
        else if (h == "pitch-") { SM.semi = Math.max(-6, SM.semi - 1); smpKeysChanged(); }
        else if (h == "pitch+") { SM.semi = Math.min(6, SM.semi + 1); smpKeysChanged(); }
        else if (h == "oct-") { SM.oct = Math.max(-1, SM.oct - 1); smpKeysChanged(); }
        else if (h == "oct+") { SM.oct = Math.min(1, SM.oct + 1); smpKeysChanged(); }
        else if (h == "lvl-") { SM.level = Math.max(-24, SM.level - 1); smpKeysChanged(); }
        else if (h == "lvl+") { SM.level = Math.min(12, SM.level + 1); smpKeysChanged(); }
        else if (h == "playkeys") smpSetPlayKeys(SM.playKeys == ix ? -1 : ix);
        else if (h == "similar") smpSimilar(ix);
        else if (h == "fixkey") { SM.grid = "fix"; SmpRail.repaint(); }
        this.repaint();
    }
    if (h != SM.hoverA)
    {
        SM.hoverA = h;
        this.repaint();
    }
});

// ---------------------------------------------------------------- clock (only while SAMPLES is open)
const var SmpClock = Engine.createTimerObject();
SmpClock.setTimerCallback(function()
{
    var now = Engine.getUptime();
    SM.tick = SM.tick + 1;
    if (SM.reindexDone)
    {
        SM.reindexDone = false;
        SM.busy = false;
        if (SM.reindexCode == 0) smpLoadIndex();
        else SM.status = "The indexer stopped with code " + SM.reindexCode + ". See AppData/SampleBrowser/index_report.txt";
        SmpRail.repaint();
        SmpResults.repaint();
    }
    if (SM.want >= 0)
    {
        if (smpMapReady() && now - SM.wantSince > 0.08) smpStartWanted();   // let a map load or option kill finish
        else if (now - SM.wantSince > 4.0)
        {
            SM.want = -1;
            SM.status = "That sound did not load: its file may have moved. RESCAN.";
            SmpRail.repaint();
        }
    }
    if (SM.playSlot >= 0 && Globals.smpEvt != SM.lastEvt)
    {
        // the router has seen the note: it starts after Globals.smpDelay
        SM.lastEvt = Globals.smpEvt;
        SM.startAt = SM.playedAt + Globals.smpDelay;
        if (!SM.playLoop) SM.offAt = SM.startAt + SM.items[SM.playIt].dur + 0.05;
    }
    if (SM.offAt > 0 && now >= SM.offAt)
    {
        Synth.noteOffFromUI(SMP_CH, SM.playSlot);
        SM.playSlot = -1;
        SM.playIt = -1;
        SM.offAt = -1.0;
        SmpResults.repaint();
    }
    if (SM.playSlot >= 0 || SM.want >= 0)
    {
        SmpAudition.repaint();
        if (SM.tick % 4 == 0) SmpResults.repaint();     // the queued LED turns from warn to glow
    }
    if (SM.tick % 15 == 0 && SM.loaded)
    {
        // host tempo or device rate moved a feel threshold: reload once nothing plays
        if (SM.mapDirty == false && smpPageStale()) SM.mapDirty = true;
        if (SM.mapDirty && SM.playSlot < 0 && SM.want < 0 && SM.page >= 0) smpBuildPage(SM.page);
        if (SM.playKeys >= 0 && SM.playForm == 1 && Math.abs(smpLoopNq(SM.items[SM.playKeys]) - SM.playNq) > 0.0001) smpSetPlayKeys(SM.playKeys);
        SmpRail.repaint();
    }
    if (SM.saveAt > 0 && now >= SM.saveAt) smpSaveUser();
});

// ---------------------------------------------------------------- shortcuts (none of the 17 note keys)
inline function onSmpKeyDown(event) { if (S.mode == 2) smpStep(1); }
inline function onSmpKeyUp(event) { if (S.mode == 2) smpStep(-1); }
inline function onSmpKeyDown5(event) { if (S.mode == 2) smpStep(5); }
inline function onSmpKeyUp5(event) { if (S.mode == 2) smpStep(-5); }
inline function onSmpPageNext(event) { if (S.mode == 2) smpStep(SMP_ROWS); }
inline function onSmpPagePrev(event) { if (S.mode == 2) smpStep(-SMP_ROWS); }
inline function onSmpReturn(event) { if (S.mode == 2) smpPlayRes(SM.sel < 0 ? 0 : SM.sel); }
inline function onSmpEscape(event) { if (S.mode == 2) smpStopAudition(); }
inline function onSmpHeart(event) { if (S.mode == 2) smpToggleFav(smpSelItem()); }
inline function onSmpLike(event) { if (S.mode == 2) smpSimilar(smpSelItem()); }
inline function onSmpBack(event) { if (S.mode == 2) smpBack(); }
inline function onSmpBin(event) { if (S.mode == 2) smpHide(smpSelItem()); }
Content.setKeyPressCallback("cursor down", onSmpKeyDown);
Content.setKeyPressCallback("cursor up", onSmpKeyUp);
Content.setKeyPressCallback("shift + cursor down", onSmpKeyDown5);
Content.setKeyPressCallback("shift + cursor up", onSmpKeyUp5);
Content.setKeyPressCallback("cursor right", onSmpPageNext);
Content.setKeyPressCallback("cursor left", onSmpPagePrev);
Content.setKeyPressCallback("return", onSmpReturn);
Content.setKeyPressCallback("escape", onSmpEscape);
Content.setKeyPressCallback("b", onSmpHeart);
Content.setKeyPressCallback("m", onSmpLike);
Content.setKeyPressCallback("backspace", onSmpBack);
Content.setKeyPressCallback("shift + backspace", onSmpBin);

// ---------------------------------------------------------------- mode enter / leave (called by setMode)
inline function smpShow(on)
{
    SmpRail.showControl(on);
    SmpSearch.showControl(on);
    SmpResults.showControl(on);
    SmpAudition.showControl(on);
    Browser.showControl(!on);
}

inline function smpRawFx(raw)
{
    // RAW audition: the instrument's master FX would colour every sample
    FX_Filter.setBypassed(raw);
    FX_Drive.setBypassed(raw);
    FX_Chorus.setBypassed(raw);
    FX_Delay.setBypassed(raw);
    FX_Reverb.setBypassed(raw);
}

inline function smpEnter()
{
    SmpLoopsSynth.setBypassed(false);
    SmpHitsSynth.setBypassed(false);
    SmpPlaySynth.setBypassed(false);
    smpRawFx(true);
    smpShow(true);
    if (!SM.loaded) smpLoadIndex();
    else if (SM.playKeys >= 0) smpSetPlayKeys(SM.playKeys);
    SmpClock.startTimer(30);
}

inline function smpLeave()
{
    smpStopAudition();
    SmpClock.stopTimer();
    if (SM.saveAt > 0) smpSaveUser();
    SmpLoopsSynth.setBypassed(true);
    SmpHitsSynth.setBypassed(true);
    SmpPlaySynth.setBypassed(true);
    smpRawFx(false);
    smpShow(false);
}

// Sample Loops always stretches in TempoSynced mode; setting it at init costs no voices
inline function smpInitStretch()
{
    local o = SmpLoops.getTimestretchOptions();
    o.Mode = "TempoSynced";
    o.SkipLatency = true;
    o.Tonality = 0.17;
    o.NumQuarters = 0;
    SmpLoops.setTimestretchOptions(o);
}
smpInitStretch();
