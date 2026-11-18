/* ============================================================================
   Hook Lab (by Research Facility) - Interface v0.1
   Type a hook, the local Hook Lab server sings it, drag the stems into the session.
   Same vintage cabinet as Sweet Melody (docs/28 + 28b): black etched panel, wood
   cheeks, typed paper cards, collet knobs and pointer selectors, red push buttons.
   Server contract: docs/22 (submit then poll) and docs/29 section 3. Params marked
   NEW in docs/29 are sent but may be ignored by the server until it implements them.
   HiseScript rules: control callbacks are inline functions; `local` only inside
   inline functions; Graphics.drawLine is (x1, x2, y1, y2, thickness).
   ============================================================================ */

Content.makeFrontInterface(1200, 800);
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-500-Medium.ttf", "VM Silk");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-600-Semi.ttf", "VM Label");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/Jost-700-Bold.ttf", "VM Bold");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/CourierPrime-Regular.ttf", "VM Type");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/CourierPrime-Bold.ttf", "VM Type Bold");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/DSEG7Classic-Bold.ttf", "VM Digits");
Engine.loadFontAs("{PROJECT_FOLDER}fonts/DSEG14Classic-Bold.ttf", "VM Alpha");

const var HOOKLAB_URL = "http://127.0.0.1:7972";
const var HOOKLAB_APP = "/Users/noxvitae/Desktop/Sweet Melody Vocal/Hook Lab.app";

// ---- tokens (shared values with Sweet Melody docs/28)
const var T = {
    "bg": 0xFF1E1D1B, "bgHi": 0xFF292725, "well": 0xFF0E0D0C, "line": 0xFF5A564D,
    "txt": 0xFFE8E4D8, "dim": 0xFFB5AF9F, "faint": 0xFF8E887B, "mute": 0xFF55514A,
    "accent": 0xFFF2A93B, "accentInk": 0xFFFFBE4D,
    "cap": 0xFF0C0D0D, "capHi": 0xFF2A2B2E, "capRing": 0xFF7F8084,
    "woodDark": 0xFF83290D, "woodHi": 0xFFD7662B, "woodEdge": 0xFFB98A5A,
    "alu": 0xFFC9CCCF, "aluDark": 0xFF7F8084,
    "pushRed": 0xFFC8321C, "pushRedHi": 0xFFF2603E, "rockCream": 0xFFE2DCCB, "ivory": 0xFFE4E1D6, "ivoryAged": 0xFFD6D5CE,
    "lampOff": 0xFF5A0E0F, "lampRed": 0xFFA11719, "lampRedGlow": 0xFFFF3B2A,
    "lampAmber": 0xFFF2A93B, "lampAmberGlow": 0xFFFFD27A, "lampGreen": 0xFF3FA65A, "lampGreenGlow": 0xFF8CF2A0,
    "card": 0xFFE3D7BB, "cardHi": 0xFFE9DFC6, "paperEdge": 0xFFB9AC8E, "cardInk": 0xFF2A221A, "cardDim": 0xFF62553F, "cardRed": 0xFF9E2A1A,
    "felt": 0xFF101112, "glass": 0xFF13171C, "glassHi": 0xFF1C2228, "glassLine": 0xFF2A3139,
    "lcdBg": 0xFF1C0606, "lcdBezel": 0xFF0D0303, "lcdOff": 0xFF3B0F0E, "lcdText": 0xFFFF5A4E,
    "FONT": "VM Label", "SILK": "VM Silk", "SUB": "VM Bold", "TYPE": "VM Type", "TYPEB": "VM Type Bold", "DIGITS": "VM Digits", "ALPHA": "VM Alpha"
};

// ---- state
const var S = {
    "page": 0, "online": false, "lastHealth": -10.0, "job": "", "state": "OFFLINE", "stage": "", "pct": 0,
    "qa": [], "take": 0, "stems": {}, "live": false, "liveKey": "", "starting": false, "hostBpm": 0.0,
    "hover": "", "tick": 0
};
const var PAGES = ["HOOK", "STACK", "MIX", "QA"];
const var KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const var SCALES = ["MAJOR", "MINOR"];
const var BARS = [4, 8, 16];
const var STYLES = [["midnight_halftime", "MIDNIGHT HALF-TIME"], ["gospel_piano", "GOSPEL PIANO"], ["afro_soul", "AFRO-SOUL SWAY"],
                    ["night_sway", "NIGHT SWAY"], ["afro_house_soul", "AFTER-HOURS AFRO"], ["night_drive_80s", "80S NIGHT DRIVE"],
                    ["soul_vamp", "SOUL VAMP"], ["stacked_heat", "STACKED HEAT"], ["alt_soul_lowlight", "ALT-SOUL LOW LIGHT"],
                    ["night_call_answer", "CALL AND ANSWER"], ["dembow", "DEMBOW"], ["trap_halftime", "TRAP HALF-TIME"],
                    ["rnb", "R&B"], ["phonk", "PHONK"], ["pop", "POP"], ["indie", "INDIE"]];
const var CHAINS = ["FORWARD DARK", "TORCH", "RAW", "HEAT", "CLOSE", "DRENCHED"];
const var HARMS = ["3RD", "5TH", "6TH", "OCT"];
const var DBLS = [0, 2, 4];
const var STEMS = [["lead", "LEAD"], ["dry", "DRY"], ["dbl", "DOUBLES"], ["harm", "HARMS"], ["adlib", "ADLIBS"]];

// ============================================================================
// DRAW HELPERS (vector; the Blender strips replace fills behind isImageLoaded later)
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

inline function drawLed(g, r, text, font)
{
    g.setColour(T.lcdBg);
    g.fillRoundedRectangle(r, 2.0);
    g.setColour(T.lcdBezel);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 2.0, 1.0);
    g.setColour(T.lcdText);
    g.setFont(font, 13);
    g.drawAlignedText(text, [r[0] + 6, r[1], r[2] - 12, r[3]], "right");
}

inline function drawPush(g, x, y, d, hot, enabled)
{
    // sprite when the drawing panel loaded "push" (docs/28 vm_push_red_2x), else vector
    if (PushPanels.indexOf(PushCur) >= 0 && PushCur.isImageLoaded("push"))
    {
        if (!enabled) g.setOpacity(0.45);
        g.drawImage("push", [Math.round(x), Math.round(y), d, d], 0, 0);
        if (!enabled) g.setOpacity(1.0);
        if (hot && enabled)
        {
            g.setColour(Colours.withAlpha(T.accent, 0.35));
            g.drawEllipse([x - 2, y - 2, d + 4, d + 4], 1.2);
        }
        return;
    }
    if (!enabled) g.setOpacity(0.45);
    g.setColour(0x80000000);
    g.fillEllipse([x - 2, y - 1, d + 4, d + 4]);
    g.setGradientFill([T.alu, x, y - 2, T.aluDark, x, y + d + 2, false]);
    g.fillEllipse([x - 2, y - 2, d + 4, d + 4]);
    g.setGradientFill([hot ? T.pushRedHi : 0xFFE0482C, x + d * 0.35, y + d * 0.3, T.pushRed, x + d, y + d, true]);
    g.fillEllipse([x + 1, y + 1, d - 2, d - 2]);
    if (!enabled) g.setOpacity(1.0);
}

inline function drawCard(g, r)
{
    g.setGradientFill([T.cardHi, 0, r[1], T.card, 0, r[1] + r[3], false]);
    g.fillRect(r);
    g.setColour(T.paperEdge);
    g.drawRect(r, 1.0);
}

inline function rackPlate(g, r, title)
{
    // 19-inch style faceplate: recessed plate, ears with screws, engraved title
    g.setColour(0xFF161514);
    g.fillRoundedRectangle(r, 3.0);
    g.setColour(0x33FFFFFF);
    g.drawRoundedRectangle([r[0] + 0.5, r[1] + 0.5, r[2] - 1, r[3] - 1], 3.0, 1.0);
    screwHead(g, r[0] + 6, r[1] + 6, 8);
    screwHead(g, r[0] + r[2] - 14, r[1] + 6, 8);
    screwHead(g, r[0] + 6, r[1] + r[3] - 14, 8);
    screwHead(g, r[0] + r[2] - 14, r[1] + r[3] - 14, 8);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.SUB, 11, 0.12);
    g.drawAlignedText(title, [r[0] + 20, r[1] + 4, r[2] - 40, 16], "centred");
}

reg PushCur = 0;                              // the panel whose paint routine is running
const var PushPanels = [];

// ============================================================================
// KNOBS: K2 collet (continuous) and K3 pointer (stepped) per docs/28b
// ============================================================================
const var knobLaf = Content.createLocalLookAndFeel();
knobLaf.registerFunction("drawRotarySlider", function(g, obj)
{
    var w = obj.area[2];
    var cx = w / 2.0;
    var cy = 36.0;
    var R = w >= 70 ? 22.0 : 16.0;
    var v = obj.valueNormalized;
    var hot = obj.hover || obj.clicked;
    var ang = -2.618 + 5.236 * v;
    var stepped = obj.max - obj.min >= 1 && obj.max - obj.min <= 15 && obj.stepSize >= 1;
    if (stepped)
    {
        var n = Math.round(obj.max - obj.min) + 1;
        var st = n <= 4 ? 0.698 : 0.5236;                                // 40 or 30 deg detents
        ang = -0.5 * (n - 1) * st + Math.round(obj.value - obj.min) * st;
    }
    g.setColour(0x66000000);
    g.fillEllipse([cx - R + 1.0, cy - R + 2.0, R * 2.0, R * 2.0]);
    g.setGradientFill([T.capHi, cx - R * 0.6, cy - R * 0.8, T.cap, cx + R * 0.5, cy + R * 0.9, false]);
    g.fillEllipse([cx - R, cy - R, R * 2.0, R * 2.0]);
    var sx = Math.sin(ang);
    var sy = -Math.cos(ang);
    if (stepped)
    {
        // bar pointer: parallel sides, pointed tip, warm-white inlay
        g.setColour(0xFF050505);
        g.drawLine(cx - sx * R * 0.55, cx + sx * R * 1.05, cy - sy * R * 0.55, cy + sy * R * 1.05, 9.0);
        g.setColour(T.txt);
        g.drawLine(cx, cx + sx * R * 0.95, cy, cy + sy * R * 0.95, 1.8);
    }
    else
    {
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

inline function addKnob(id, label, x, y, w, mn, mx, def, step, parent)
{
    local k = Content.addKnob(id, x, y);
    Content.setPropertiesFromJSON(id, {"width": w, "height": 66, "text": label, "min": mn, "max": mx,
        "defaultValue": def, "stepSize": step, "saveInPreset": true, "isPluginParameter": false,
        "parentComponent": parent, "showValuePopup": "No"});
    k.setValue(def);
    k.setLocalLookAndFeel(knobLaf);
    return k;
}

// ============================================================================
// CHASSIS
// ============================================================================
const var Bg = Content.addPanel("Bg", 0, 0);
Content.setPropertiesFromJSON("Bg", {"width": 1200, "height": 800, "allowCallbacks": "No Callbacks", "saveInPreset": false});
Bg.setPaintRoutine(function(g)
{
    g.setColour(T.bg);
    g.fillRect([36, 16, 1128, 768]);
    g.setGradientFill([Colours.withAlpha(T.bgHi, 0.35), 0, 16, Colours.withAlpha(T.bgHi, 0.0), 0, 140, false]);
    g.fillRect([36, 16, 1128, 124]);
    g.setGradientFill([0x00000000, 0, 140, 0x40000000, 0, 784, false]);
    g.fillRect([36, 140, 1128, 644]);
    woodFill(g, [32, 0, 1136, 16], true);
    woodFill(g, [0, 0, 32, 800], false);
    woodFill(g, [1168, 0, 32, 800], false);
    woodFill(g, [32, 784, 1136, 16], true);
    g.setColour(Colours.withAlpha(T.woodEdge, 0.55));
    g.fillRect([32, 784, 1136, 1]);
    g.setGradientFill([T.alu, 32, 0, T.aluDark, 36, 0, false]);
    g.fillRect([32, 16, 4, 768]);
    g.setGradientFill([T.alu, 1164, 0, T.aluDark, 1168, 0, false]);
    g.fillRect([1164, 16, 4, 768]);
    screwHead(g, 114, 2, 12);
    screwHead(g, 594, 2, 12);
    screwHead(g, 1074, 2, 12);
    g.setColour(Colours.withAlpha(T.txt, 0.55));
    g.fillRect([36, 69, 1128, 1]);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.SILK, 14, 0.10);
    g.drawAlignedText(PAGES[S.page] == "HOOK" ? "LYRICS        GROOVE        RENDER" : PAGES[S.page], [36, 756, 1128, 20], "centred");
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("AI VOCAL: rendered by the local Hook Lab engine. No real singer's voice is used.", [48, 740, 600, 12], "left");
});

// ============================================================================
// HEADER: nameplate, job card, page keys, server lamp + START
// ============================================================================
const var Header = Content.addPanel("Header", 36, 16);
Content.setPropertiesFromJSON("Header", {"width": 1128, "height": 52, "allowCallbacks": "Clicks & Hover", "saveInPreset": false});
const var PK_X = [790, 848, 906, 964];
PushPanels.push(Header);
Header.loadImage("{PROJECT_FOLDER}vm_push_red_2x.png", "push");
Header.setPaintRoutine(function(g)
{
    PushCur = Header;
    var hv = S.hover;
    g.setGradientFill([0xFFDCDEE0, 20, 11, T.aluDark, 20, 41, false]);
    g.fillRoundedRectangle([20, 11, 200, 30], 3.0);
    g.setColour(0x80000000);
    g.drawRoundedRectangle([20.5, 11.5, 199, 29], 3.0, 1.0);
    g.setColour(T.cardInk);
    g.setFontWithSpacing(T.SUB, 14, 0.24);
    g.drawAlignedText("HOOK LAB", [34, 12, 176, 17], "left");
    g.setColour(0xFF3A342B);
    g.setFontWithSpacing(T.FONT, 9, 0.18);
    g.drawAlignedText("RESEARCH FACILITY", [34, 28, 176, 11], "left");
    screwHead(g, 23, 23, 6);
    screwHead(g, 211, 23, 6);

    // job card
    g.setColour(T.aluDark);
    g.drawRect([240, 8, 520, 36], 1.0);
    drawCard(g, [243, 11, 514, 30]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPEB, 14);
    var first = Lyrics.get("text").split("\n")[0];
    g.drawAlignedText(first == "" ? "Type a hook below" : first, [254, 11, 360, 30], "left");
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 11);
    g.drawAlignedText(STYLES[Math.round(StyleKnob.getValue())][1], [600, 11, 150, 30], "right");

    var i = 0;
    for (i = 0; i < 4; i++)
    {
        var on = S.page == i;
        var x = PK_X[i];
        g.setGradientFill([hv == "p" + i ? T.cardHi : T.ivory, 0, 8, on ? 0xFFC9C6BB : T.ivoryAged, 0, 44, false]);
        g.fillRoundedRectangle([x, on ? 9 : 8, 56, 36], 3.0);
        g.setColour(on ? T.lampAmber : T.lampOff);
        g.fillRoundedRectangle([x + 24, on ? 13 : 12, 8, 4], 1.5);
        g.setColour(T.cardInk);
        g.setFontWithSpacing(T.FONT, 9, 0.08);
        g.drawAlignedText(PAGES[i], [x, on ? 23 : 22, 56, 14], "centred");
    }
    // server: lamp + START when offline
    drawLamp(g, 1032, 12, 14, S.online, T.lampGreen, T.lampGreenGlow);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(S.online ? "SERVER" : (S.starting ? "STARTING" : "OFFLINE"), [1010, 28, 58, 12], "centred");
    if (!S.online)
    {
        drawPush(g, 1078, 12, 22, hv == "start", !S.starting);
        g.setColour(T.txt);
        g.drawAlignedText("START", [1066, 35, 46, 12], "centred");
    }
});
Header.setMouseCallback(function(event)
{
    var h = "";
    var i = 0;
    for (i = 0; i < 4; i++)
        if (event.x >= PK_X[i] && event.x < PK_X[i] + 56 && event.y >= 8 && event.y < 44) h = "p" + i;
    if (!S.online && event.x >= 1072 && event.x < 1106 && event.y >= 8 && event.y < 40) h = "start";
    if (event.clicked)
    {
        if (h.indexOf("p") == 0) setPage(parseInt(h.substring(1, 2)));
        else if (h == "start") startServer();
    }
    if (h != S.hover)
    {
        S.hover = h;
        this.repaint();
    }
});

// ============================================================================
// HOOK PAGE
// ============================================================================
const var HookPage = Content.addPanel("HookPage", 46, 78);
Content.setPropertiesFromJSON("HookPage", {"width": 1108, "height": 656, "allowCallbacks": "Clicks & Hover", "saveInPreset": false});

const var Lyrics = Content.addLabel("Lyrics", 26, 54);
Content.setPropertiesFromJSON("Lyrics", {"parentComponent": "HookPage", "width": 600, "height": 214,
    "text": "", "editable": true, "multiline": true, "fontName": "VM Type", "fontSize": 13,
    "textColour": 0xFF2A221A, "bgColour": 0x00000000, "itemColour": 0x00000000, "itemColour2": 0x00000000,
    "alignment": "topLeft", "saveInPreset": true, "tooltip": "One line per phrase. Start a line with [en] or [es] to set its language."});

const var LangKnob = addKnob("LangKnob", "LANG", 534, 278, 56, 0, 1, 0, 1, "HookPage");
const var KeyKnob = addKnob("KeyKnob", "KEY", 700, 54, 64, 0, 11, 9, 1, "HookPage");
const var ScaleKnob = addKnob("ScaleKnob", "SCALE", 780, 54, 56, 0, 1, 1, 1, "HookPage");
const var BarsKnob = addKnob("BarsKnob", "BARS", 852, 54, 56, 0, 2, 1, 1, "HookPage");
const var StyleKnob = addKnob("StyleKnob", "STYLE", 932, 54, 76, 0, STYLES.length - 1, 0, 1, "HookPage");
const var SeedsKnob = addKnob("SeedsKnob", "SEEDS", 700, 176, 56, 1, 4, 4, 1, "HookPage");
StyleKnob.set("stepSize", 1);

const var HOOK_TILES_Y = 498;
PushPanels.push(HookPage);
HookPage.loadImage("{PROJECT_FOLDER}vm_push_red_2x.png", "push");
HookPage.setPaintRoutine(function(g)
{
    PushCur = HookPage;
    rackPlate(g, [0, 0, 650, 330], "LYRICS");
    drawCard(g, [16, 44, 620, 230]);
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 10);
    g.drawAlignedText("LANG " + (LangKnob.getValue() > 0.5 ? "EN" : "ES") + "   per line: [en] / [es]", [26, 300, 400, 14], "left");
    var n = Lyrics.get("text").split("\n").length;
    g.drawAlignedText(n + " LINES", [26, 282, 200, 14], "left");

    rackPlate(g, [664, 0, 444, 330], "GROOVE");
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText("BPM", [690, 262, 72, 10], "centred");
    drawLed(g, [690, 274, 72, 28], S.hostBpm > 0 ? Engine.doubleToString(S.hostBpm, 1) : "---", T.DIGITS);
    g.drawAlignedText("KEY", [776, 262, 120, 10], "centred");
    drawLed(g, [776, 274, 120, 28], KEYS[Math.round(KeyKnob.getValue())] + " " + SCALES[Math.round(ScaleKnob.getValue())].substring(0, 3), T.ALPHA);
    drawLamp(g, 912, 280, 14, S.live, T.lampAmber, T.lampAmberGlow);
    g.drawAlignedText(S.live ? "LIVE KEY" : "MANUAL", [904, 296, 50, 12], "centred");
    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("BARS " + BARS[Math.round(BarsKnob.getValue())] + "   " + STYLES[Math.round(StyleKnob.getValue())][1], [776, 236, 300, 12], "left");

    rackPlate(g, [0, 344, 1108, 300], "RENDER");
    drawPush(g, 30, 384, 32, S.hover == "render", S.online && !jobBusy());
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText("RENDER", [18, 420, 56, 12], "centred");
    drawLamp(g, 80, 392, 10, jobBusy(), T.lampAmber, T.lampAmberGlow);
    drawLed(g, [110, 384, 360, 30], S.state + (S.stage != "" ? " " + S.stage : "") + (jobBusy() ? " " + Math.round(S.pct) : ""), T.ALPHA);
    g.setColour(T.well);
    g.fillRect([110, 422, 360, 6]);
    g.setColour(T.accent);
    g.fillRect([110, 422, 360 * Math.range(S.pct / 100.0, 0.0, 1.0), 6]);

    // takes A-D with lyric error rates (QA from the server)
    var t = 0;
    for (t = 0; t < 4; t++)
    {
        var tx = 500 + t * 120;
        var has = t < S.qa.length;
        g.setGradientFill([S.take == t ? 0xFFC9C6BB : T.ivory, 0, 384, T.ivoryAged, 0, 420, false]);
        if (!has) g.setOpacity(0.4);
        g.fillRoundedRectangle([tx, 384, 108, 36], 3.0);
        g.setColour(S.take == t ? T.lampAmber : T.lampOff);
        g.fillRoundedRectangle([tx + 8, 398, 8, 8], 2.0);
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 12);
        g.drawAlignedText("TAKE " + "ABCD".substring(t, t + 1), [tx + 20, 384, 84, 20], "left");
        g.setFont(T.TYPE, 10);
        g.drawAlignedText(has ? "LER " + Engine.doubleToString(S.qa[t], 2) : "--", [tx + 20, 402, 84, 16], "left");
        g.setOpacity(1.0);
    }

    // stem tiles: drag into the session
    var s = 0;
    for (s = 0; s < STEMS.length; s++)
    {
        var sx = 30 + s * 214;
        var ok = isDefined(S.stems[STEMS[s][0]]);
        drawCard(g, [sx, HOOK_TILES_Y, 196, 56]);
        if (!ok) { g.setColour(0x80161514); g.fillRect([sx, HOOK_TILES_Y, 196, 56]); }
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 13);
        g.drawAlignedText(STEMS[s][1], [sx + 12, HOOK_TILES_Y + 6, 170, 20], "left");
        g.setColour(T.cardDim);
        g.setFont(T.TYPE, 10);
        g.drawAlignedText(ok ? "DRAG INTO YOUR SESSION" : "RENDER FIRST", [sx + 12, HOOK_TILES_Y + 28, 170, 16], "left");
    }
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("Play C3 to audition the selected take. Stems are matched to the host tempo and the key above.", [30, 566, 800, 12], "left");
});

inline function jobBusy()
{
    return S.job != "" && S.state != "DONE" && S.state != "FAILED" && S.state != "OFFLINE" && S.state != "READY";
}

HookPage.setMouseCallback(function(event)
{
    var h = "";
    if (event.x >= 26 && event.x < 66 && event.y >= 380 && event.y < 420) h = "render";
    var t = 0;
    for (t = 0; t < 4; t++) if (event.x >= 500 + t * 120 && event.x < 608 + t * 120 && event.y >= 384 && event.y < 420) h = "take" + t;
    var s = 0;
    for (s = 0; s < STEMS.length; s++)
        if (event.x >= 30 + s * 214 && event.x < 226 + s * 214 && event.y >= HOOK_TILES_Y && event.y < HOOK_TILES_Y + 56) h = "stem" + s;
    if (event.clicked)
    {
        if (h == "render" && S.online && !jobBusy()) submitRender();
        else if (h.indexOf("take") == 0) pickTake(parseInt(h.substring(4, 5)));
    }
    if (event.drag && h.indexOf("stem") == 0)
    {
        var key = STEMS[parseInt(h.substring(4, 5))][0];
        if (isDefined(S.stems[key])) this.startExternalFileDrag(S.stems[key], false, function() {});
    }
    if (h != S.hover)
    {
        S.hover = h;
        this.repaint();
    }
});

// ============================================================================
// STACK / MIX / QA PAGES (rack units)
// ============================================================================
const var StackPage = Content.addPanel("StackPage", 46, 78);
Content.setPropertiesFromJSON("StackPage", {"width": 1108, "height": 656, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
const var DblKnob = addKnob("DblKnob", "DOUBLES", 40, 60, 64, 0, 2, 1, 1, "StackPage");
const var HarmKnob = addKnob("HarmKnob", "HARMONY", 130, 60, 64, 0, 3, 0, 1, "StackPage");
const var HarmOn = addKnob("HarmOnKnob", "HARM MIX", 220, 60, 64, 0, 1, 0.5, 0.01, "StackPage");
const var AdlibKnob = addKnob("AdlibKnob", "AD-LIBS", 310, 60, 64, 0, 3, 1, 1, "StackPage");
const var WidthKnob = addKnob("WidthKnob", "WIDTH", 400, 60, 64, 0.5, 1.0, 0.8, 0.01, "StackPage");
const var VarKnob = addKnob("VarKnob", "VARIANCE", 490, 60, 64, 0.05, 0.25, 0.12, 0.01, "StackPage");
StackPage.setPaintRoutine(function(g)
{
    rackPlate(g, [0, 0, 1108, 200], "STACK");
    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("DOUBLES " + DBLS[Math.round(DblKnob.getValue())] + "   HARMONY " + HARMS[Math.round(HarmKnob.getValue())] + "   AD-LIB DENSITY " + Math.round(AdlibKnob.getValue()), [40, 150, 600, 12], "left");
});

const var MixPage = Content.addPanel("MixPage", 46, 78);
Content.setPropertiesFromJSON("MixPage", {"width": 1108, "height": 656, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
const var ChainKnob = addKnob("ChainKnob", "CHAIN", 40, 60, 76, 0, CHAINS.length - 1, 4, 1, "MixPage");
const var TuneKnob = addKnob("TuneKnob", "TUNE", 150, 60, 64, 0, 100, 80, 1, "MixPage");
const var RetuneKnob = addKnob("RetuneKnob", "RETUNE MS", 240, 60, 64, 0, 120, 40, 1, "MixPage");
const var VibRateKnob = addKnob("VibRateKnob", "VIB RATE", 330, 60, 64, 3.0, 8.0, 5.5, 0.1, "MixPage");
const var VibDepthKnob = addKnob("VibDepthKnob", "VIB DEPTH", 420, 60, 64, 0, 100, 40, 1, "MixPage");
const var AirKnob = addKnob("AirKnob", "AIR DB", 510, 60, 64, 0, 4, 1.5, 0.1, "MixPage");
const var DeessKnob = addKnob("DeessKnob", "DE-ESS", 600, 60, 64, 0, 10, 4, 0.1, "MixPage");
const var DriveKnob = addKnob("DriveKnob", "DRIVE", 690, 60, 64, 0, 25, 6, 1, "MixPage");
const var RoomKnob = addKnob("RoomKnob", "ROOM", 780, 60, 64, 0, 1, 0.4, 0.01, "MixPage");
MixPage.setPaintRoutine(function(g)
{
    rackPlate(g, [0, 0, 1108, 200], "CHAIN");
    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("CHAIN " + CHAINS[Math.round(ChainKnob.getValue())] + "   (AIR, DE-ESS, DRIVE, ROOM, RETUNE: sent; used once the server supports them)", [40, 150, 900, 12], "left");
});

const var QaPage = Content.addPanel("QaPage", 46, 78);
Content.setPropertiesFromJSON("QaPage", {"width": 1108, "height": 656, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
QaPage.setPaintRoutine(function(g)
{
    rackPlate(g, [0, 0, 1108, 300], "TIMING / QA");
    drawCard(g, [30, 40, 520, 230]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPEB, 12);
    g.drawAlignedText("TAKE    LYRIC ERROR RATE", [44, 48, 480, 18], "left");
    g.setFont(T.TYPE, 12);
    var t = 0;
    for (t = 0; t < 4; t++)
    {
        var has = t < S.qa.length;
        g.setColour(has && S.qa[t] > 0.30 ? T.cardRed : T.cardInk);
        g.drawAlignedText("ABCD".substring(t, t + 1) + "       " + (has ? Engine.doubleToString(S.qa[t], 3) : "--"), [44, 76 + t * 22, 480, 18], "left");
    }
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 10);
    g.drawAlignedText("Red: more than 30% of the words misheard by the checker. Pick another take or re-render.", [44, 186, 480, 40], "topLeft");
});

const var PAGE_PANELS = [HookPage, StackPage, MixPage, QaPage];
inline function setPage(i)
{
    local k = 0;
    S.page = i;
    for (k = 0; k < 4; k++) PAGE_PANELS[k].showControl(k == i);
    Header.repaint();
    Bg.repaint();
}

// ============================================================================
// SERVER CLIENT (docs/22: submit then poll; defensive when the server is down)
// ============================================================================
Server.setBaseURL(HOOKLAB_URL);
Server.setEnforceTrailingSlash(false);
Server.setHttpHeader("Content-Type: application/json");
const var Player = Synth.getAudioSampleProcessor("Hook Player");
const var HlTask = Engine.createBackgroundTask("Hook Lab start");

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
    local bpm = S.hostBpm > 0 ? S.hostBpm : 94.0;
    return {
        "lines": lyricLines(),
        "key": KEYS[Math.round(KeyKnob.getValue())],
        "scale": Math.round(ScaleKnob.getValue()) == 1 ? "minor" : "major",
        "bpm": bpm,
        "bars": BARS[Math.round(BarsKnob.getValue())],
        "style": STYLES[Math.round(StyleKnob.getValue())][0],
        "n_seeds": Math.round(SeedsKnob.getValue()),
        "chain": CHAINS[Math.round(ChainKnob.getValue())].toLowerCase().replace(" ", "_"),
        "stack": {"dbl": DBLS[Math.round(DblKnob.getValue())], "harm": HARMS[Math.round(HarmKnob.getValue())].toLowerCase(),
                  "harm_mix": HarmOn.getValue(), "adlib": Math.round(AdlibKnob.getValue()), "width": WidthKnob.getValue(),
                  "retake_variance": VarKnob.getValue()},
        "expr": {"tune": TuneKnob.getValue() / 100.0, "retune_ms": RetuneKnob.getValue(), "vib_rate": VibRateKnob.getValue(),
                 "vib_depth_c": VibDepthKnob.getValue()},
        "fx": {"air_db": AirKnob.getValue(), "deess_db": DeessKnob.getValue(), "sat_mix": DriveKnob.getValue() / 100.0, "room": RoomKnob.getValue()}
    };
}

inline function submitRender()
{
    local job = buildJob();
    if (job.lines.length == 0) { S.state = "NO LYRICS"; HookPage.repaint(); return; }
    S.state = "QUEUED";
    S.stage = "";
    S.pct = 0;
    S.qa = [];
    S.stems = {};
    HookPage.repaint();
    Server.callWithPOST("/render/", JSON.stringify(job), function(status, response)
    {
        if (status == 200 && isDefined(response.id))
        {
            S.job = "" + response.id;
            S.state = "QUEUED";
        }
        else
        {
            S.job = "";
            S.state = "FAILED";
        }
        HookPage.repaint();
    });
}

inline function pickTake(t)
{
    if (t >= S.qa.length) return;
    S.take = t;
    fetchStems();
    HookPage.repaint();
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
        if (isDefined(S.stems.lead)) Player.setFile(S.stems.lead);
        HookPage.repaint();
    });
}

inline function startServer()
{
    if (S.starting) return;
    S.starting = true;
    HlTask.runProcess("/usr/bin/open", ["-a", HOOKLAB_APP], function(task, finished, data) {});
    Header.repaint();
}

const var Clock = Engine.createTimerObject();
Clock.setTimerCallback(function()
{
    S.tick = S.tick + 1;
    var hb = Engine.getHostBpm();
    if (hb != S.hostBpm) { S.hostBpm = hb; HookPage.repaint(); }
    if (S.tick % 2 == 0)
    {
        Server.callWithGET("/health", {}, function(status, response)
        {
            var on = status == 200;
            if (on != S.online)
            {
                S.online = on;
                if (on) S.starting = false;
                if (!on && S.state != "FAILED") S.state = "OFFLINE";
                if (on && S.state == "OFFLINE") S.state = "READY";
                Header.repaint();
                HookPage.repaint();
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
                if (fresh != S.live) { S.live = fresh; HookPage.repaint(); }
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
            HookPage.repaint();
        });
    }
});
Clock.startTimer(500);

// ============================================================================
// STARTUP + SELF-TEST
// ============================================================================
setPage(0);

inline function selfTest()
{
    local ok = true;
    Lyrics.set("text", "Dime si tu me quieres\n[en] say it one more time");
    local j = buildJob();
    if (j.lines.length != 2 || j.lines[1].lang != "en" || j.lines[0].lang != "es") { ok = false; Console.print("HL selftest lyric lines"); }
    if (j.key != "A" || j.scale != "minor" || j.bars != 8 || j.n_seeds != 4) { ok = false; Console.print("HL selftest job defaults"); }
    if (JSON.stringify(j).indexOf("\"lines\"") < 0) ok = false;
    local allc = Content.getAllComponents(".*");
    local i = 0;
    for (i = 0; i < allc.length; i++)
    {
        local c = allc[i];
        if (c.get("parentComponent") != "") continue;
        if (c.get("x") + c.get("width") > 1200 || c.get("y") + c.get("height") > 800) { ok = false; Console.print("HL selftest outside: " + c.getId()); }
    }
    if (!isDefined(Player)) ok = false;
    Lyrics.set("text", "");
    Console.print(ok ? "HL selftest PASS styles=" + STYLES.length : "HL selftest FAIL");
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
