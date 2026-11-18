/* ============================================================================
   Hook Lab (by Research Facility) - Interface v0.2
   Front end of the local Hook Lab server: type a hook, the server sings it, play the
   takes, drag them into the session or SAVE them to a folder you pick. The engine (about
   9 GB) runs in the Hook Lab server process, never in this plugin.

   Views: COMPACT (default, 768 x 464, everything on one screen) and EXPANDED (1200 x 800:
   the same core plus the STACK and MIX racks and the QA table). The window resizes at
   runtime through Content.setWidth / setHeight (HISE 4.1.0: the exported editor listens
   to the interface-size broadcaster, FrontendProcessorEditor.cpp:165).
   Look: docs/28 + 28b (black etched panel, wood cheeks, typed cards, collet knobs,
   pointer selectors, lit switches, red push buttons).
   Server contract: docs/22 (submit then poll) + docs/29. Params the server does not have
   yet are sent and ignored until it implements them; GET /genres/ falls back to the list
   below until the route exists.
   HiseScript: control callbacks are inline functions; `local` only inside inline
   functions; Graphics.drawLine is (x1, x2, y1, y2, thickness).
   ============================================================================ */

Content.makeFrontInterface(768, 464);
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-500-Medium.ttf", "VM Silk");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-600-Semi.ttf", "VM Label");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-700-Bold.ttf", "VM Bold");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/CourierPrime-Regular.ttf", "VM Type");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/CourierPrime-Bold.ttf", "VM Type Bold");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/DSEG7Classic-Bold.ttf", "VM Digits");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/DSEG14Classic-Bold.ttf", "VM Alpha");

const var HOOKLAB_URL = "http://127.0.0.1:7972";
const var HOOKLAB_APP = "/Users/noxvitae/Desktop/Sweet Melody Vocal/Hook Lab.app";
const var CW = 768;            // compact size
const var CH = 464;
const var FW = 1200;           // expanded size
const var FH = 800;

const var T = {
    "bg": 0xFF1E1D1B, "bgHi": 0xFF292725, "well": 0xFF0E0D0C, "line": 0xFF5A564D,
    "txt": 0xFFE8E4D8, "dim": 0xFFB5AF9F, "faint": 0xFF8E887B,
    "accent": 0xFFF2A93B, "accentInk": 0xFFFFBE4D,
    "cap": 0xFF0C0D0D, "capHi": 0xFF2A2B2E,
    "woodDark": 0xFF6E3418, "wood": 0xFFB8622E, "woodHi": 0xFFD08442, "woodEdge": 0xFFB98A5A,
    "alu": 0xFFC9CCCF, "aluDark": 0xFF7F8084,
    "pushRed": 0xFFC8321C, "pushRedHi": 0xFFF2603E, "ivory": 0xFFE4E1D6, "ivoryAged": 0xFFD6D5CE,
    "lampOff": 0xFF5A0E0F, "lampAmber": 0xFFF2A93B, "lampAmberGlow": 0xFFFFD27A, "lampGreen": 0xFF3FA65A, "lampGreenGlow": 0xFF8CF2A0,
    "card": 0xFFE3D7BB, "cardHi": 0xFFE9DFC6, "paperEdge": 0xFFB9AC8E, "cardInk": 0xFF2A221A, "cardDim": 0xFF62553F, "cardRed": 0xFF9E2A1A,
    "lcdBg": 0xFF1C0606, "lcdBezel": 0xFF0D0303, "lcdText": 0xFFFF5A4E,
    "FONT": "VM Label", "SILK": "VM Silk", "SUB": "VM Bold", "TYPE": "VM Type", "TYPEB": "VM Type Bold", "DIGITS": "VM Digits", "ALPHA": "VM Alpha"
};

const var S = {
    "expanded": false, "online": false, "ready": false, "starting": false, "state": "OFFLINE", "stage": "", "pct": 0,
    "job": "", "qa": [], "take": 0, "stems": {}, "live": false, "hostBpm": 0.0, "hover": "", "tick": 0,
    "playing": "", "saveDir": "", "genresFromServer": false, "intense": false, "syncLive": true
};
const var KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const var SCALES = ["MAJOR", "MINOR"];
const var BARS = [4, 8, 12, 16];
const var CHAINS = ["FORWARD DARK", "TORCH", "RAW", "HEAT", "CLOSE", "DRENCHED"];
const var HARMS = ["3RD", "5TH", "6TH", "OCT"];
const var DBLS = [0, 2, 4];
// result rows: takes A-D, then the stems (LEAD, DRY, BED, then the stack when it exists)
const var STEMS = [["lead", "LEAD"], ["dry", "DRY"], ["bed", "BED"], ["dbl", "DOUBLES"], ["harm", "HARMS"], ["adlib", "ADLIBS"], ["answer", "ANSWER"]];

// Genre families: fallback until GET /genres/ exists ([id, label, bpm_default]; the server's
// list replaces these, including its language and chain defaults)
reg GENRES = [
    {"id": "hiphop", "label": "HIP-HOP / RAP", "genres": [["boom_bap", "BOOM BAP", 90], ["lofi", "LO-FI", 82], ["halftime_trap", "HALF-TIME TRAP", 140], ["melodic_trap", "MELODIC TRAP", 145], ["rage", "RAGE", 155], ["plugg", "PLUGG", 150], ["drill", "DRILL", 142], ["cloud", "CLOUD", 130], ["emo_rap", "EMO RAP", 135]]},
    {"id": "latin", "label": "CARIBBEAN / LATIN / AFRO", "genres": [["dancehall", "DANCEHALL", 96], ["one_drop", "REGGAE ONE DROP", 76], ["roots", "ROOTS", 72], ["dub", "DUB", 70], ["reggaeton", "REGGAETON", 92], ["dembow", "DEMBOW", 120], ["perreo", "PERREO", 95], ["latin_trap", "LATIN TRAP", 140], ["cumbia", "CUMBIA", 96], ["bachata", "BACHATA", 128], ["afrobeats", "AFROBEATS", 106], ["amapiano", "AMAPIANO", 113]]},
    {"id": "brazil", "label": "BRAZIL", "genres": [["br_phonk", "BRAZILIAN PHONK", 130], ["baile_funk", "BAILE FUNK", 130], ["brega_funk", "BREGA FUNK", 160], ["mpb", "MPB", 96], ["bossa", "BOSSA", 120]]},
    {"id": "indie", "label": "INDIE / ELECTRONIC", "genres": [["indie_pop", "INDIE POP", 118], ["bedroom", "BEDROOM", 100], ["dream_pop", "DREAM POP", 104], ["shoegaze", "SHOEGAZE", 110], ["garage_rock", "GARAGE ROCK", 140], ["surf_punk", "SURF PUNK", 160], ["post_punk", "POST-PUNK", 140], ["folk", "FOLK", 96], ["synth_pop", "SYNTH-POP", 118], ["disco_pop", "DISCO-POP", 120], ["house", "HOUSE", 124], ["ukg", "UK GARAGE", 132], ["electro", "ELECTRO", 125]]},
    {"id": "rnb", "label": "R&B / SOUL", "genres": [["midnight_halftime", "MIDNIGHT HALF-TIME", 68], ["gospel_piano", "GOSPEL PIANO", 72], ["afro_soul", "AFRO-SOUL SWAY", 100], ["night_sway", "NIGHT SWAY", 88], ["afro_house_soul", "AFTER-HOURS AFRO", 120], ["night_drive_80s", "80S NIGHT DRIVE", 104], ["soul_vamp", "SOUL VAMP", 84], ["stacked_heat", "STACKED HEAT", 96], ["alt_soul_lowlight", "ALT-SOUL LOW LIGHT", 74], ["night_call_answer", "CALL AND ANSWER", 92]]}
];

// ============================================================================
// DRAW HELPERS
// ============================================================================
inline function woodFill(g, r, horiz)
{
    if (horiz) g.setGradientFill([T.woodHi, r[0], r[1], T.woodDark, r[0], r[1] + r[3], false]);
    else g.setGradientFill([T.woodHi, r[0], r[1], T.woodDark, r[0] + r[2], r[1], false]);
    g.fillRect(r);
}

inline function screwHead(g, x, y, d)
{
    g.setGradientFill([T.alu, x, y, T.aluDark, x + d, y + d, false]);
    g.fillEllipse([x, y, d, d]);
    g.setColour(0x99000000);
    g.drawLine(x + 2, x + d - 2, y + d / 2, y + d / 2, 1.2);
}

inline function drawLamp(g, x, y, d, on, col, glow)
{
    if (on)
    {
        g.setColour(Colours.withAlpha(glow, 0.25));
        g.fillEllipse([x - 3, y - 3, d + 6, d + 6]);
        g.setGradientFill([glow, x + d * 0.4, y + d * 0.35, col, x + d, y + d, true]);
        g.fillEllipse([x, y, d, d]);
    }
    else
    {
        g.setColour(T.lampOff);
        g.fillEllipse([x, y, d, d]);
    }
    g.setColour(0x80000000);
    g.drawEllipse([x, y, d, d], 1.0);
}

inline function drawLed(g, r, text, font, size)
{
    g.setColour(T.lcdBg);
    g.fillRoundedRectangle(r, 2.0);
    g.setColour(T.lcdBezel);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 2.0, 1.0);
    g.setColour(T.lcdText);
    g.setFont(font, size);
    g.drawAlignedText(text, [r[0] + 6, r[1], r[2] - 12, r[3]], "right");
}

inline function drawCard(g, r)
{
    g.setGradientFill([T.cardHi, 0, r[1], T.card, 0, r[1] + r[3], false]);
    g.fillRect(r);
    g.setColour(T.paperEdge);
    g.drawRect(r, 1.0);
}

reg PushCur = 0;
inline function drawPush(g, x, y, d, hot, down, enabled)
{
    if (!enabled) g.setOpacity(0.45);
    if (PushCur != 0 && PushCur.isImageLoaded("push"))
        g.drawImage("push", [Math.round(x), Math.round(y), d, d], 0, down ? 48 : 0);
    else
    {
        g.setColour(0x80000000);
        g.fillEllipse([x - 2, y - 1, d + 4, d + 4]);
        g.setGradientFill([T.alu, x, y - 2, T.aluDark, x, y + d + 2, false]);
        g.fillEllipse([x - 2, y - 2, d + 4, d + 4]);
        g.setGradientFill([hot ? T.pushRedHi : 0xFFE0482C, x + d * 0.35, y + d * 0.3, T.pushRed, x + d, y + d, true]);
        g.fillEllipse([x + 1, y + 1, d - 2, d - 2]);
    }
    if (!enabled) g.setOpacity(1.0);
    if (hot && enabled)
    {
        g.setColour(Colours.withAlpha(T.accent, 0.35));
        g.drawEllipse([x - 2, y - 2, d + 4, d + 4], 1.2);
    }
}

// latching lit switch (28b premium button): ivory cap with a lamp lens
inline function drawLit(g, r, label, on, hot)
{
    g.setColour(0xFF0B0B0C);
    g.fillRoundedRectangle([r[0] - 2, r[1] - 2, r[2] + 4, r[3] + 4], 4.0);
    g.setGradientFill([hot ? T.cardHi : T.ivory, 0, r[1], on ? 0xFFC9C6BB : T.ivoryAged, 0, r[1] + r[3], false]);
    g.fillRoundedRectangle([r[0], r[1] + (on ? 1 : 0), r[2], r[3]], 3.0);
    drawLamp(g, r[0] + r[2] / 2 - 4, r[1] + 4 + (on ? 1 : 0), 8, on, T.lampAmber, T.lampAmberGlow);
    g.setColour(T.cardInk);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(label, [r[0], r[1] + 13 + (on ? 1 : 0), r[2], r[3] - 13], "centred");
}

// small cream key (result rows: PLAY / STOP, drag handle, SAVE)
inline function drawKey(g, r, label, hot, enabled)
{
    if (!enabled) g.setOpacity(0.4);
    g.setGradientFill([hot ? T.cardHi : T.ivory, 0, r[1], T.ivoryAged, 0, r[1] + r[3], false]);
    g.fillRoundedRectangle(r, 2.5);
    g.setColour(0x66000000);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 2.5, 1.0);
    g.setColour(T.cardInk);
    g.setFontWithSpacing(T.FONT, 9, 0.06);
    g.drawAlignedText(label, r, "centred");
    if (!enabled) g.setOpacity(1.0);
}

inline function plate(g, r, title)
{
    g.setColour(0xFF161514);
    g.fillRoundedRectangle(r, 3.0);
    g.setColour(0x33FFFFFF);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 3.0, 1.0);
    screwHead(g, r[0] + 4, r[1] + 4, 7);
    screwHead(g, r[0] + r[2] - 11, r[1] + 4, 7);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.SUB, 10, 0.12);
    g.drawAlignedText(title, [r[0] + 14, r[1] + 2, r[2] - 28, 14], "centred");
}

// ============================================================================
// KNOBS: K2 collet (continuous), K3 pointer (stepped) per docs/28b
// ============================================================================
const var knobLaf = Content.createLocalLookAndFeel();
knobLaf.loadImage("{PROJECT_FOLDER}vm_collet_s_2x.png", "clS");      // 80 px frames, 40 logical
knobLaf.registerFunction("drawRotarySlider", function(g, obj)
{
    var w = obj.area[2];
    var cx = w / 2.0;
    var cy = 34.0;
    var R = 16.0;
    var v = obj.valueNormalized;
    var hot = obj.hover || obj.clicked;
    var stepped = obj.stepSize >= 1 && obj.max - obj.min <= 15;
    var ang = -2.618 + 5.236 * v;
    if (stepped)
    {
        var n = Math.round(obj.max - obj.min) + 1;
        var st = n <= 4 ? 0.698 : (n <= 9 ? 0.5236 : 0.4363);         // 40 / 30 / 25 deg detents
        ang = -0.5 * (n - 1) * st + Math.round(obj.value - obj.min) * st;
    }
    var sx = Math.sin(ang);
    var sy = -Math.cos(ang);
    if (stepped)
    {
        g.setColour(0x66000000);
        g.fillEllipse([cx - R * 0.62 + 1, cy - R * 0.62 + 2, R * 1.24, R * 1.24]);
        g.setGradientFill([T.capHi, cx - R * 0.5, cy - R * 0.6, T.cap, cx + R * 0.5, cy + R * 0.6, false]);
        g.fillEllipse([cx - R * 0.62, cy - R * 0.62, R * 1.24, R * 1.24]);
        g.setColour(0xFF050505);                                       // bar pointer
        g.drawLine(cx - sx * R * 0.6, cx + sx * R * 1.1, cy - sy * R * 0.6, cy + sy * R * 1.1, 8.0);
        g.setColour(T.txt);
        g.drawLine(cx, cx + sx * R * 1.0, cy, cy + sy * R * 1.0, 1.6);
    }
    else
    {
        if (knobLaf.isImageLoaded("clS"))
        {
            var fi = Math.round(Math.wrap(ang * 57.29578, 10.0) / 10.0 * 16.0) % 16;
            g.drawImage("clS", [Math.round(cx - 20), Math.round(cy - 20), 40, 40], 0, fi * 80);
        }
        else
        {
            g.setGradientFill([T.capHi, cx - R * 0.6, cy - R * 0.8, T.cap, cx + R * 0.5, cy + R * 0.9, false]);
            g.fillEllipse([cx - R, cy - R, R * 2.0, R * 2.0]);
        }
        var cr = R * 0.78;
        g.setGradientFill([0xFF8FA9C2, cx - cr * 0.5, cy - cr * 0.6, 0xFF3F7BAA, cx + cr, cy + cr, true]);
        g.fillEllipse([cx - cr, cy - cr, cr * 2.0, cr * 2.0]);
        g.setColour(0x59000000);
        g.drawLine(cx + sx * cr * 0.2 + 0.6, cx + sx * cr * 0.92 + 0.6, cy + sy * cr * 0.2 + 0.6, cy + sy * cr * 0.92 + 0.6, 2.0);
        g.setColour(T.txt);
        g.drawLine(cx + sx * cr * 0.2, cx + sx * cr * 0.92, cy + sy * cr * 0.2, cy + sy * cr * 0.92, 1.6);
    }
    if (hot)
    {
        g.setColour(Colours.withAlpha(T.accent, 0.35));
        g.drawEllipse([cx - R - 2, cy - R - 2, R * 2 + 4, R * 2 + 4], 1.2);
    }
    g.setColour(hot ? T.accentInk : T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(hot ? obj.valueAsText : obj.text.toUpperCase(), [0, 0, w, 12], "centred");
});

inline function addKnob(id, label, x, y, mn, mx, def, step, parent)
{
    local k = Content.addKnob(id, x, y);
    Content.setPropertiesFromJSON(id, {"width": 56, "height": 58, "text": label, "min": mn, "max": mx,
        "defaultValue": def, "stepSize": step, "saveInPreset": true, "isPluginParameter": false,
        "parentComponent": parent, "showValuePopup": "No"});
    k.setValue(def);
    k.setLocalLookAndFeel(knobLaf);
    return k;
}

// ============================================================================
// CHASSIS (paints for the current window size)
// ============================================================================
const var Bg = Content.addPanel("Bg", 0, 0);
Content.setPropertiesFromJSON("Bg", {"width": FW, "height": FH, "allowCallbacks": "No Callbacks", "saveInPreset": false});
Bg.setPaintRoutine(function(g)
{
    var W = S.expanded ? FW : CW;
    var H = S.expanded ? FH : CH;
    g.setColour(T.bg);
    g.fillRect([0, 0, W, H]);
    g.setGradientFill([Colours.withAlpha(T.bgHi, 0.35), 0, 0, Colours.withAlpha(T.bgHi, 0.0), 0, 120, false]);
    g.fillRect([0, 0, W, 120]);
    woodFill(g, [0, 0, 12, H], false);
    woodFill(g, [W - 12, 0, 12, H], false);
    woodFill(g, [12, 0, W - 24, 6], true);
    woodFill(g, [12, H - 8, W - 24, 8], true);
    g.setColour(Colours.withAlpha(T.woodEdge, 0.55));
    g.fillRect([12, H - 8, W - 24, 1]);
    if (S.expanded)
    {
        g.setColour(Colours.withAlpha(T.txt, 0.55));
        g.fillRect([CW, 10, 1, CH - 16]);
        g.fillRect([12, CH, W - 24, 1]);
    }
});

// ============================================================================
// CORE (the compact view; stays at the top-left when expanded)
// ============================================================================
const var Core = Content.addPanel("Core", 12, 6);
Content.setPropertiesFromJSON("Core", {"width": 744, "height": 450, "allowCallbacks": "Clicks, Hover & Dragging", "saveInPreset": false});
Core.loadImage("{PROJECT_FOLDER}vm_push_red_2x.png", "push");

const var Lyrics = Content.addLabel("Lyrics", 18, 58);
Content.setPropertiesFromJSON("Lyrics", {"parentComponent": "Core", "width": 364, "height": 154,
    "text": "", "editable": true, "multiline": true, "fontName": "VM Type", "fontSize": 13,
    "textColour": 0xFF2A221A, "bgColour": 0x00000000, "itemColour": 0x00000000, "itemColour2": 0x00000000,
    "alignment": "topLeft", "saveInPreset": true, "tooltip": "One line per phrase. Start a line with [en] or [es] to set its language."});
const var LangKnob = addKnob("LangKnob", "LANG", 330, 190, 0, 1, 0, 1, "Core");
const var KeyKnob = addKnob("KeyKnob", "KEY", 528, 54, 0, 11, 9, 1, "Core");
const var ScaleKnob = addKnob("ScaleKnob", "SCALE", 590, 54, 0, 1, 1, 1, "Core");
const var BarsKnob = addKnob("BarsKnob", "BARS", 652, 54, 0, 3, 1, 1, "Core");
const var FamilyKnob = addKnob("FamilyKnob", "FAMILY", 400, 144, 0, 4, 4, 1, "Core");
const var GenreKnob = addKnob("GenreKnob", "GENRE", 462, 144, 0, 9, 0, 1, "Core");
const var SeedsKnob = addKnob("SeedsKnob", "TAKES", 676, 144, 1, 4, 4, 1, "Core");

inline function famGenres()
{
    return GENRES[Math.round(FamilyKnob.getValue())].genres;
}

inline function curGenre()
{
    local gl = famGenres();
    return gl[Math.min(gl.length - 1, Math.round(GenreKnob.getValue()))];
}

inline function onFamily(component, value)
{
    local n = famGenres().length;
    GenreKnob.set("max", n - 1);
    if (GenreKnob.getValue() > n - 1) GenreKnob.setValue(0);
    Core.repaint();
}
FamilyKnob.setControlCallback(onFamily);
inline function onGenre(component, value) { Core.repaint(); }
GenreKnob.setControlCallback(onGenre);

inline function jobBusy()
{
    return S.job != "" && S.state != "DONE" && S.state != "FAILED" && S.state != "OFFLINE" && S.state != "READY" && S.state != "SAVED" && S.state != "SAVE FAILED";
}

inline function rowRect(i)
{
    // result rows: the 4 takes on one row, then the stems two per row
    if (i < 4) return [10 + i * 182, 300, 176, 30];
    local j = i - 4;
    return [10 + (j % 2) * 364, 336 + Math.floor(j / 2) * 27, 358, 24];
}

inline function serverText()
{
    if (S.online && S.ready) return "ENGINE READY";
    if (S.online || S.starting) return "ENGINE STARTING";
    return "OFFLINE";
}

Core.setPaintRoutine(function(g)
{
    PushCur = Core;
    var hv = S.hover;
    var k = 0;
    // header strip: nameplate, engine lamp + state, START, view key
    g.setColour(0xFF141414);
    g.fillRoundedRectangle([6, 8, 150, 28], 3.0);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.SUB, 12, 0.24);
    g.drawAlignedText("HOOK LAB", [14, 9, 140, 16], "left");
    g.setColour(T.dim);
    g.setFontWithSpacing(T.FONT, 7, 0.18);
    g.drawAlignedText("RESEARCH FACILITY", [14, 24, 140, 10], "left");
    var blink = (S.starting || (S.online && !S.ready)) && S.tick % 2 == 0;
    drawLamp(g, 170, 15, 12, (S.online && S.ready) || blink, S.ready ? T.lampGreen : T.lampAmber, S.ready ? T.lampGreenGlow : T.lampAmberGlow);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.1);
    g.drawAlignedText(serverText(), [188, 10, 140, 22], "left");
    if (!S.online)
    {
        drawPush(g, 330, 11, 22, hv == "start", false, !S.starting);
        g.drawAlignedText(S.starting ? "LAUNCHING IN BACKGROUND" : "START ENGINE", [358, 10, 170, 22], "left");
    }
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("AI VOCAL. The engine runs in the Hook Lab app, not in this plugin.", [400, 30, 270, 10], "left");
    drawLit(g, [682, 8, 56, 30], S.expanded ? "COMPACT" : "EXPAND", S.expanded, hv == "view");

    // lyric sheet
    drawCard(g, [10, 50, 380, 196]);
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 10);
    g.drawAlignedText(Lyrics.get("text").split("\n").length + " LINES   default LANG " + (LangKnob.getValue() > 0.5 ? "EN" : "ES"), [18, 220, 300, 12], "left");
    g.drawAlignedText("[en] / [es] at a line start", [18, 232, 300, 12], "left");

    // groove strip
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText("BPM", [400, 46, 120, 10], "left");
    var gn = curGenre();
    var bpm = (S.syncLive && S.hostBpm > 0) ? S.hostBpm : gn[2];
    drawLed(g, [400, 58, 120, 26], Engine.doubleToString(bpm, 1), T.DIGITS, 14);
    drawLit(g, [400, 92, 56, 30], "SYNC LIVE", S.syncLive, hv == "sync");
    drawLamp(g, 466, 99, 12, S.live, T.lampAmber, T.lampAmberGlow);
    g.setColour(T.txt);
    g.drawAlignedText(S.live ? "LIVE KEY" : "MANUAL", [482, 97, 50, 16], "left");
    drawLed(g, [528, 116, 208, 22], KEYS[Math.round(KeyKnob.getValue())] + " " + SCALES[Math.round(ScaleKnob.getValue())] + "  " + BARS[Math.round(BarsKnob.getValue())] + " BARS", T.ALPHA, 10);

    // genre family -> genre, INTENSE
    drawLed(g, [400, 210, 336, 24], GENRES[Math.round(FamilyKnob.getValue())].label + " / " + gn[1], T.ALPHA, 9);
    drawLit(g, [530, 152, 64, 40], "INTENSE", S.intense, hv == "intense");
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText(S.genresFromServer ? "genres from the engine" : "built-in genre list", [400, 236, 200, 12], "left");

    // render row
    var can = S.online && S.ready && !jobBusy();
    drawPush(g, 12, 254, 28, hv == "render", false, can);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText("RENDER", [2, 284, 48, 10], "centred");
    drawLamp(g, 50, 264, 10, jobBusy(), T.lampAmber, T.lampAmberGlow);
    drawLed(g, [68, 254, 420, 30], S.state + (S.stage != "" ? " " + S.stage : "") + (jobBusy() ? " " + Math.round(S.pct) : ""), T.ALPHA, 12);
    g.setColour(T.well);
    g.fillRect([500, 264, 236, 10]);
    g.setColour(T.accent);
    g.fillRect([500, 264, 236 * Math.range(S.pct / 100.0, 0.0, 1.0), 10]);

    // results: takes A-D (click to pick; LER badge)
    for (k = 0; k < 4; k++)
    {
        var r = rowRect(k);
        var has = k < S.qa.length;
        if (!has) g.setOpacity(0.4);
        drawCard(g, r);
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 11);
        g.drawAlignedText("TAKE " + "ABCD".substring(k, k + 1), [r[0] + 8, r[1], 70, r[3]], "left");
        g.setColour(has && S.qa[k] > 0.30 ? T.cardRed : T.cardDim);
        g.setFont(T.TYPE, 10);
        g.drawAlignedText(has ? "LER " + Engine.doubleToString(S.qa[k], 2) : "--", [r[0] + 70, r[1], 70, r[3]], "left");
        drawLamp(g, r[0] + r[2] - 18, r[1] + 10, 10, S.take == k && has, T.lampAmber, T.lampAmberGlow);
        g.setOpacity(1.0);
    }
    // results: stems (PLAY / STOP, drag into the DAW, SAVE)
    for (k = 0; k < STEMS.length; k++)
    {
        var sr = rowRect(4 + k);
        var ok = isDefined(S.stems[STEMS[k][0]]);
        if (!ok) g.setOpacity(0.4);
        drawCard(g, sr);
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 11);
        g.drawAlignedText(STEMS[k][1], [sr[0] + 8, sr[1], 90, sr[3]], "left");
        g.setOpacity(1.0);
        drawKey(g, [sr[0] + 110, sr[1] + 3, 56, 18], S.playing == STEMS[k][0] ? "STOP" : "PLAY", hv == "play" + k, ok);
        drawKey(g, [sr[0] + 172, sr[1] + 3, 96, 18], "DRAG TO DAW", hv == "drag" + k, ok);
        drawKey(g, [sr[0] + 274, sr[1] + 3, 76, 18], "SAVE", hv == "save" + k, ok);
    }
});

inline function hitCore(x, y)
{
    local k = 0;
    if (x >= 682 && x < 738 && y >= 8 && y < 38) return "view";
    if (!S.online && x >= 328 && x < 354 && y >= 9 && y < 35) return "start";
    if (x >= 400 && x < 456 && y >= 92 && y < 122) return "sync";
    if (x >= 530 && x < 594 && y >= 152 && y < 192) return "intense";
    if (x >= 8 && x < 44 && y >= 250 && y < 286) return "render";
    for (k = 0; k < 4; k++)
    {
        local r = rowRect(k);
        if (x >= r[0] && x < r[0] + r[2] && y >= r[1] && y < r[1] + r[3]) return "take" + k;
    }
    for (k = 0; k < STEMS.length; k++)
    {
        local sr = rowRect(4 + k);
        if (y < sr[1] || y >= sr[1] + sr[3] || x < sr[0] || x >= sr[0] + sr[2]) continue;
        if (x >= sr[0] + 110 && x < sr[0] + 166) return "play" + k;
        if (x >= sr[0] + 172 && x < sr[0] + 268) return "drag" + k;
        if (x >= sr[0] + 274 && x < sr[0] + 350) return "save" + k;
    }
    return "";
}

Core.setMouseCallback(function(event)
{
    var h = hitCore(event.x, event.y);
    if (event.clicked)
    {
        if (h == "view") setView(!S.expanded);
        else if (h == "start") startServer();
        else if (h == "sync") { S.syncLive = !S.syncLive; this.repaint(); }
        else if (h == "intense") { S.intense = !S.intense; this.repaint(); }
        else if (h == "render" && S.online && S.ready && !jobBusy()) submitRender();
        else if (h.indexOf("take") == 0) pickTake(parseInt(h.substring(4, 5)));
        else if (h.indexOf("play") == 0) togglePlay(STEMS[parseInt(h.substring(4, 5))][0]);
        else if (h.indexOf("save") == 0) saveStem(STEMS[parseInt(h.substring(4, 5))][0]);
    }
    if (event.drag)
    {
        var dh = hitCore(event.mouseDownX, event.mouseDownY);
        if (dh.indexOf("drag") == 0)
        {
            var key = STEMS[parseInt(dh.substring(4, 5))][0];
            if (isDefined(S.stems[key])) this.startExternalFileDrag(S.stems[key], false, function() {});
        }
    }
    if (h != S.hover)
    {
        S.hover = h;
        this.repaint();
    }
});

// ============================================================================
// EXPANDED RACKS: STACK and CHAIN (right column), QA (bottom)
// ============================================================================
const var Racks = Content.addPanel("Racks", CW + 8, 10);
Content.setPropertiesFromJSON("Racks", {"width": FW - CW - 28, "height": CH - 20, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
const var DblKnob = addKnob("DblKnob", "DOUBLES", 14, 24, 0, 2, 1, 1, "Racks");
const var HarmKnob = addKnob("HarmKnob", "HARMONY", 76, 24, 0, 3, 0, 1, "Racks");
const var HarmMix = addKnob("HarmMixKnob", "HARM MIX", 138, 24, 0, 1, 0.5, 0.01, "Racks");
const var AdlibKnob = addKnob("AdlibKnob", "AD-LIBS", 200, 24, 0, 3, 1, 1, "Racks");
const var WidthKnob = addKnob("WidthKnob", "WIDTH", 262, 24, 0.5, 1.0, 0.8, 0.01, "Racks");
const var VarKnob = addKnob("VarKnob", "VARIANCE", 324, 24, 0.05, 0.25, 0.12, 0.01, "Racks");
const var ChainKnob = addKnob("ChainKnob", "CHAIN", 14, 176, 0, 5, 4, 1, "Racks");
const var TuneKnob = addKnob("TuneKnob", "TUNE", 76, 176, 0, 100, 80, 1, "Racks");
const var RetuneKnob = addKnob("RetuneKnob", "RETUNE", 138, 176, 0, 120, 40, 1, "Racks");
const var VibRateKnob = addKnob("VibRateKnob", "VIB RATE", 200, 176, 3.0, 8.0, 5.5, 0.1, "Racks");
const var VibDepthKnob = addKnob("VibDepthKnob", "VIB DEPTH", 262, 176, 0, 100, 40, 1, "Racks");
const var AirKnob = addKnob("AirKnob", "AIR", 324, 176, 0, 4, 1.5, 0.1, "Racks");
const var DeessKnob = addKnob("DeessKnob", "DE-ESS", 76, 300, 0, 10, 4, 0.1, "Racks");
const var DriveKnob = addKnob("DriveKnob", "DRIVE", 138, 300, 0, 25, 6, 1, "Racks");
const var RoomKnob = addKnob("RoomKnob", "ROOM", 200, 300, 0, 1, 0.4, 0.01, "Racks");
Racks.setPaintRoutine(function(g)
{
    plate(g, [0, 0, 392, 140], "STACK");
    plate(g, [0, 152, 392, 280], "CHAIN");
    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("DBL " + DBLS[Math.round(DblKnob.getValue())] + "   HARM " + HARMS[Math.round(HarmKnob.getValue())] + "   AD-LIB " + Math.round(AdlibKnob.getValue()), [14, 100, 360, 12], "left");
    g.drawAlignedText("CHAIN " + CHAINS[Math.round(ChainKnob.getValue())], [14, 252, 360, 12], "left");
    g.setColour(T.faint);
    g.drawAlignedText("RETUNE, AIR, DE-ESS, DRIVE, ROOM: sent; used once the engine supports them", [14, 400, 370, 12], "left");
});

const var Qa = Content.addPanel("Qa", 20, CH + 8);
Content.setPropertiesFromJSON("Qa", {"width": FW - 40, "height": FH - CH - 20, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
Qa.setPaintRoutine(function(g)
{
    plate(g, [0, 0, FW - 40, FH - CH - 24], "TIMING / QA");
    drawCard(g, [16, 24, 520, 250]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPEB, 12);
    g.drawAlignedText("TAKE    LYRIC ERROR RATE", [30, 32, 480, 18], "left");
    g.setFont(T.TYPE, 12);
    var t = 0;
    for (t = 0; t < 4; t++)
    {
        var has = t < S.qa.length;
        g.setColour(has && S.qa[t] > 0.30 ? T.cardRed : T.cardInk);
        g.drawAlignedText("ABCD".substring(t, t + 1) + "       " + (has ? Engine.doubleToString(S.qa[t], 3) : "--"), [30, 60 + t * 22, 480, 18], "left");
    }
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 10);
    g.drawAlignedText("Red: more than 30% of the words misheard by the checker. Pick another take or render again.", [30, 160, 490, 40], "topLeft");
    drawCard(g, [556, 24, 568, 250]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPE, 11);
    g.drawAlignedText("JOB " + (S.job == "" ? "-" : S.job) + "\nSTATE " + S.state + (S.stage != "" ? " / " + S.stage : "") + "\nENGINE " + serverText() + "\nSAVE FOLDER " + (S.saveDir == "" ? "(chosen on the first SAVE)" : S.saveDir), [570, 34, 540, 120], "topLeft");
});

inline function setView(expand)
{
    S.expanded = expand;
    Racks.showControl(expand);
    Qa.showControl(expand);
    Content.setWidth(expand ? FW : CW);
    Content.setHeight(expand ? FH : CH);
    Bg.repaint();
    Core.repaint();
}

// ============================================================================
// SERVER CLIENT (submit then poll; honest OFFLINE / ENGINE STARTING states)
// ============================================================================
Server.setBaseURL(HOOKLAB_URL);
Server.setEnforceTrailingSlash(false);
Server.setHttpHeader("Content-Type: application/json");
const var Player = Synth.getAudioSampleProcessor("Hook Player");
const var HlTask = Engine.createBackgroundTask("Hook Lab start");
Globals.hlPlay = false;
Globals.hlPlayEpoch = 0;

inline function lyricLines()
{
    local out = [];
    local rows = Lyrics.get("text").split("\n");
    local i = 0;
    local def = LangKnob.getValue() > 0.5 ? "en" : "es";
    for (i = 0; i < rows.length; i++)
    {
        local r = rows[i].trim();
        if (r == "") continue;
        local lang = def;
        if (r.indexOf("[en]") == 0) { lang = "en"; r = r.substring(4, r.length).trim(); }
        else if (r.indexOf("[es]") == 0) { lang = "es"; r = r.substring(4, r.length).trim(); }
        out.push({"text": r, "lang": lang});
    }
    return out;
}

inline function buildJob()
{
    local gn = curGenre();
    local bpm = (S.syncLive && S.hostBpm > 0) ? S.hostBpm : gn[2];
    return {
        "lines": lyricLines(),
        "key": KEYS[Math.round(KeyKnob.getValue())],
        "scale": Math.round(ScaleKnob.getValue()) == 1 ? "minor" : "major",
        "bpm": bpm,
        "bars": BARS[Math.round(BarsKnob.getValue())],
        "family": GENRES[Math.round(FamilyKnob.getValue())].id,
        "genre": gn[0],
        "style": gn[0],
        "intense": S.intense,
        "n_seeds": Math.round(SeedsKnob.getValue()),
        "chain": CHAINS[Math.round(ChainKnob.getValue())].toLowerCase().replace(" ", "_"),
        "stack": {"dbl": DBLS[Math.round(DblKnob.getValue())], "harm": HARMS[Math.round(HarmKnob.getValue())].toLowerCase(),
                  "harm_mix": HarmMix.getValue(), "adlib": Math.round(AdlibKnob.getValue()), "width": WidthKnob.getValue(),
                  "retake_variance": VarKnob.getValue()},
        "expr": {"tune": TuneKnob.getValue() / 100.0, "retune_ms": RetuneKnob.getValue(), "vib_rate": VibRateKnob.getValue(),
                 "vib_depth_c": VibDepthKnob.getValue()},
        "fx": {"air_db": AirKnob.getValue(), "deess_db": DeessKnob.getValue(), "sat_mix": DriveKnob.getValue() / 100.0, "room": RoomKnob.getValue()}
    };
}

inline function stopPlay()
{
    if (S.playing == "") return;
    S.playing = "";
    Globals.hlPlay = false;
    Globals.hlPlayEpoch = Globals.hlPlayEpoch + 1;
}

inline function submitRender()
{
    local job = buildJob();
    if (job.lines.length == 0) { S.state = "NO LYRICS"; Core.repaint(); return; }
    stopPlay();
    S.state = "QUEUED";
    S.stage = "";
    S.pct = 0;
    S.qa = [];
    S.stems = {};
    Core.repaint();
    Server.callWithPOST("/render/", JSON.stringify(job), function(status, response)
    {
        if (status == 200 && isDefined(response.id))
            S.job = "" + response.id;
        else
        {
            S.job = "";
            S.state = "FAILED";
        }
        Core.repaint();
    });
}

inline function fetchStems()
{
    if (S.job == "") return;
    Server.callWithGET("/stems/" + S.job, {"take": S.take}, function(status, response)
    {
        if (status != 200) return;
        S.stems = {};
        var k = 0;
        for (k = 0; k < STEMS.length; k++)
            if (isDefined(response[STEMS[k][0]]) && response[STEMS[k][0]] != "") S.stems[STEMS[k][0]] = response[STEMS[k][0]];
        Core.repaint();
    });
}

inline function pickTake(t)
{
    if (t >= S.qa.length) return;
    S.take = t;
    stopPlay();
    fetchStems();
    Core.repaint();
}

inline function togglePlay(key)
{
    if (!isDefined(S.stems[key])) return;
    if (S.playing == key) { stopPlay(); Core.repaint(); return; }
    Player.setFile(S.stems[key]);
    S.playing = key;
    Globals.hlPlay = true;
    Globals.hlPlayEpoch = Globals.hlPlayEpoch + 1;      // the Trigger script starts the note
    Core.repaint();
}

inline function saveStem(key)
{
    if (!isDefined(S.stems[key])) return;
    local src = FileSystem.fromAbsolutePath(S.stems[key]);
    local base = src.toString(1);                        // file name with extension
    local start = S.saveDir != "" ? FileSystem.fromAbsolutePath(S.saveDir + "/" + base) : FileSystem.getFolder(FileSystem.Desktop).getChildFile(base);
    S.savePending = S.stems[key];                        // nested callbacks cannot see inline locals
    FileSystem.browse(start, true, "*.wav", function(target)
    {
        if (!isDefined(target)) return;
        var ok = FileSystem.fromAbsolutePath(S.savePending).copy(target);
        S.saveDir = target.getParentDirectory().toString(0);
        S.state = ok ? "SAVED" : "SAVE FAILED";
        Core.repaint();
    });
}

inline function startServer()
{
    if (S.starting) return;
    S.starting = true;
    // -g keeps the app behind the DAW; the windowless background mode replaces this when
    // Hook Lab.app ships it
    HlTask.runProcess("/usr/bin/open", ["-g", "-a", HOOKLAB_APP], function(task, finished, data) {});
    Core.repaint();
}

inline function loadGenres()
{
    Server.callWithGET("/genres/", {}, function(status, response)
    {
        if (status != 200 || !isDefined(response.families)) return;
        var fams = [];
        var i = 0;
        var j = 0;
        for (i = 0; i < response.families.length; i++)
        {
            var f = response.families[i];
            var gl = [];
            for (j = 0; j < f.genres.length; j++)
                gl.push([f.genres[j].id, ("" + f.genres[j].label).toUpperCase(), isDefined(f.genres[j].bpm_default) ? f.genres[j].bpm_default : 96]);
            if (gl.length > 0) fams.push({"id": f.id, "label": ("" + f.label).toUpperCase(), "genres": gl});
        }
        if (fams.length > 0)
        {
            GENRES = fams;
            S.genresFromServer = true;
            FamilyKnob.set("max", fams.length - 1);
            if (FamilyKnob.getValue() > fams.length - 1) FamilyKnob.setValue(0);
            onFamily(FamilyKnob, FamilyKnob.getValue());
        }
    });
}

const var Clock = Engine.createTimerObject();
Clock.setTimerCallback(function()
{
    S.tick = S.tick + 1;
    var hb = Engine.getHostBpm();
    if (hb != S.hostBpm) { S.hostBpm = hb; Core.repaint(); }
    if (S.starting || (S.online && !S.ready)) Core.repaint();          // blink the engine lamp
    if (S.tick % 2 == 0)
    {
        Server.callWithGET("/health", {}, function(status, response)
        {
            var on = status == 200;
            var rdy = on && (!isDefined(response.ready) || response.ready == true);
            if (on != S.online || rdy != S.ready)
            {
                var first = on && !S.online;
                S.online = on;
                S.ready = rdy;
                if (on) S.starting = false;
                if (!on && S.state != "FAILED") S.state = "OFFLINE";
                if (rdy && (S.state == "OFFLINE" || S.state == "ENGINE STARTING")) S.state = "READY";
                if (on && !rdy) S.state = "ENGINE STARTING";
                if (first) loadGenres();
                Core.repaint();
            }
        });
        if (S.online)
        {
            Server.callWithGET("/project/", {}, function(status, response)
            {
                var fresh = status == 200 && isDefined(response.key) && response.fresh == true;
                if (fresh)
                {
                    var ki = KEYS.indexOf(("" + response.key).toUpperCase());
                    if (ki >= 0 && Math.round(KeyKnob.getValue()) != ki) KeyKnob.setValue(ki);
                    if (isDefined(response.scale)) ScaleKnob.setValue(("" + response.scale).toLowerCase().indexOf("min") >= 0 ? 1 : 0);
                }
                if (fresh != S.live) { S.live = fresh; Core.repaint(); }
            });
        }
    }
    if (S.online && jobBusy())
    {
        Server.callWithGET("/status/" + S.job, {}, function(status, response)
        {
            if (status != 200) return;
            S.state = ("" + response.state).toUpperCase();
            S.stage = isDefined(response.stage) ? ("" + response.stage).toUpperCase() : "";
            S.pct = isDefined(response.pct) ? response.pct : 0;
            if (isDefined(response.qa) && isDefined(response.qa.ler)) S.qa = response.qa.ler;
            if (S.state == "DONE") fetchStems();
            Core.repaint();
            if (S.expanded) Qa.repaint();
        });
    }
});
Clock.startTimer(500);

// ============================================================================
// STARTUP + SELF-TEST
// ============================================================================
onFamily(FamilyKnob, FamilyKnob.getValue());

inline function selfTest()
{
    local ok = true;
    Lyrics.set("text", "Dime si tu me quieres\n[en] say it one more time");
    local j = buildJob();
    if (j.lines.length != 2 || j.lines[1].lang != "en" || j.lines[0].lang != "es") { ok = false; Console.print("HL selftest lyric lines"); }
    if (j.key != "A" || j.scale != "minor" || j.bars != 8 || j.n_seeds != 4 || j.family != "rnb") { ok = false; Console.print("HL selftest job defaults"); }
    if (JSON.stringify(j).indexOf("\"genre\"") < 0) ok = false;
    FamilyKnob.setValue(1);
    onFamily(FamilyKnob, 1);
    if (GenreKnob.get("max") != 11 || curGenre()[0] != "dancehall") { ok = false; Console.print("HL selftest genre family"); }
    FamilyKnob.setValue(4);
    onFamily(FamilyKnob, 4);
    local allc = Content.getAllComponents(".*");
    local i = 0;
    for (i = 0; i < allc.length; i++)
    {
        local c = allc[i];
        if (c.get("parentComponent") != "") continue;
        if (c.get("x") + c.get("width") > FW || c.get("y") + c.get("height") > FH) { ok = false; Console.print("HL selftest outside: " + c.getId()); }
    }
    if (Core.get("x") + Core.get("width") > CW || Core.get("y") + Core.get("height") > CH) { ok = false; Console.print("HL selftest core outside compact"); }
    if (!isDefined(Player)) ok = false;
    Lyrics.set("text", "");
    Console.print(ok ? "HL selftest PASS genres=" + GENRES.length : "HL selftest FAIL");
}
if (Engine.isHISE()) selfTest();
function onNoteOn()
{
}
function onNoteOff()
{
}
function onController()
{
}
function onTimer()
{
}
function onControl(number, value)
{
}
