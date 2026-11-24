/* ============================================================================
   Hook Lab (by Research Facility) - Interface v0.3
   Front end of the local Hook Lab server: type a hook, the server sings it, play the
   takes, drag them into the session (matched to the project tempo and key) or SAVE them
   to a folder you pick. The engine (about 9 GB) runs in the Hook Lab app, never here.

   Views: COMPACT (768 x 464, the whole job on one screen) and EXPANDED (1200 x 800:
   the same core plus the STACK / LEVELS / VOICE / MIX racks, PERFORMANCE / BED /
   OUTPUT and the TAKES / LINES / FIX desk). Content.setWidth / setHeight resize the
   editor at runtime (HISE 4.1.0, FrontendProcessorEditor.cpp:165).
   Look: docs/28 + 28b (black etched panel, wood cheeks, typed cards, collet knobs,
   K3 pointer selectors, lit keys, red push buttons).
   Server contract: Sweet Melody Vocal/docs/API.md (2026-11-19, Hook Lab Pro). Every
   long call is submit-then-poll (HISE server calls time out after 10 s).
   Rack knobs are sent only while that rack's MANUAL key is lit: a genre preset fills
   every value the request leaves out, so an untouched rack keeps the preset's sound.
   HiseScript: control callbacks are inline functions; `local` only inside inline
   functions; Graphics.drawLine is (x1, x2, y1, y2, thickness); Math.floor returns a
   double (wrap it in Math.round before building ids).
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
    "lampRed": 0xFFA11719, "lampRedGlow": 0xFFFF3B2A,
    "card": 0xFFE3D7BB, "cardHi": 0xFFE9DFC6, "paperEdge": 0xFFB9AC8E, "cardInk": 0xFF2A221A, "cardDim": 0xFF62553F, "cardRed": 0xFF9E2A1A,
    "lcdBg": 0xFF1C0606, "lcdBezel": 0xFF0D0303, "lcdText": 0xFFFF5A4E,
    "FONT": "VM Label", "SILK": "VM Silk", "SUB": "VM Bold", "TYPE": "VM Type", "TYPEB": "VM Type Bold", "DIGITS": "VM Digits", "ALPHA": "VM Alpha"
};

// Session state. jstate is the server's own word: "" | queued | running | done | error | cancelled
const var S = {
    "expanded": false, "online": false, "warm": false, "starting": false, "startAt": 0, "tick": 0,
    "job": "", "jstate": "", "kind": "", "lcd": "READY", "stage": "", "pct": 0, "msg": "", "preset": "",
    "takes": [], "lines": [], "ler": -1, "worst": -1, "E": -1, "timing": "",
    "orig": {}, "conf": {}, "takeFiles": {}, "folder": "", "exportOk": true, "disclosure": "AI-generated vocal", "outTier": "",
    "stemsFor": "", "stemJob": "", "playing": "", "hover": "", "qhover": "", "saveDir": "", "savePending": [],
    "syncLive": true, "intense": false, "match": true,
    "projSrc": "none", "projBpm": 0.0, "projKey": "", "projMode": "", "projKeySet": false, "posted": -1.0,
    "conformId": "", "confState": "", "confText": "", "confFor": "",
    "gateText": "", "memGb": -1, "genresFromServer": false, "scoreText": "",
    "act": "", "actBody": {}, "postBody": {}, "needStems": false, "needConform": false, "needGenres": false, "postedKey": ""
};
const var KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const var BARS = [4, 8, 12, 16];

// result tiles: [key, label, source keys in /stems/] (API.md section 7 tile table).
// Conformed copies are looked up by the source key's last segment (lead, lead_dry, dbl_L ...).
const var TILES = [["lead", "LEAD", ["files.lead"]], ["dry", "DRY", ["files.lead_dry"]],
                   ["bed", "BED", ["files.sketch_instrumental"]], ["dbl", "DOUBLES", ["stems.dbl_L", "stems.dbl_R"]],
                   ["harm", "HARMS", ["stems.harm_hi", "stems.harm_lo", "stems.oct_up", "stems.oct_lo"]],
                   ["adlib", "AD-LIBS", ["stems.adlibs"]], ["answer", "ANSWER", ["stems.answers"]],
                   ["bus", "ALL VOCALS", ["stems.vocal_bus"]]];
const var NOT_STEM_SAFE = ["lead", "bus"];     // tiles that carry lead.wav when stem_export_ok is false

// Genre families: fallback until GET /genres/ answers ([id, label, bpm_default]), in the
// server's order (API.md section 6, 63 presets). The server list replaces it.
reg GENRES = [
    {"id": "reggaeton", "label": "REGGAETON", "genres": [["reggaeton", "REGGAETON", 94], ["perreo", "PERREO", 98], ["old_school_perreo", "OLD SCHOOL PERREO", 96], ["reggaeton_romantico", "ROMANTICO", 90], ["dembow", "DEMBOW RD", 124], ["neoperreo", "NEOPERREO", 92], ["latin_trap", "LATIN TRAP", 140], ["moombahton", "MOOMBAHTON", 108]]},
    {"id": "caribbean_afro", "label": "CARIBBEAN / AFRO", "genres": [["dancehall", "DANCEHALL", 96], ["reggae", "REGGAE ONE DROP", 78], ["dub", "DUB", 74], ["lovers_rock", "LOVERS ROCK", 76], ["cumbia", "CUMBIA", 96], ["bachata", "BACHATA", 128], ["afrobeats", "AFROBEATS", 104], ["afro_swing", "AFROSWING", 104], ["amapiano", "AMAPIANO", 112]]},
    {"id": "hiphop_rap", "label": "HIP-HOP / RAP", "genres": [["boom_bap", "BOOM BAP", 90], ["lofi_hiphop", "LO-FI HIP-HOP", 80], ["trap_rap_halftime", "TRAP RAP HALF-TIME", 140], ["melodic_trap", "MELODIC TRAP", 140], ["rage", "RAGE", 160], ["plugg", "PLUGG", 140], ["pluggnb", "PLUGGNB", 130], ["uk_drill", "UK DRILL", 142], ["ny_drill", "NY DRILL", 144], ["cloud_rap", "CLOUD RAP", 140], ["emo_rap", "EMO RAP", 150], ["memphis_rap", "MEMPHIS RAP", 140], ["jazz_rap", "JAZZ RAP", 88]]},
    {"id": "brazil", "label": "BRAZIL", "genres": [["phonk_br", "BR PHONK", 130], ["baile_funk", "BAILE FUNK", 130], ["brega_funk", "BREGA FUNK", 90], ["mpb", "MPB", 88], ["bossa_nova", "BOSSA NOVA", 120], ["samba_pop", "SAMBA POP", 100], ["trap_br", "TRAP BR", 144], ["funk_melody", "FUNK MELODY", 130]]},
    {"id": "indie_electronic", "label": "INDIE / ELECTRONIC", "genres": [["indie_pop", "INDIE POP JANGLE", 118], ["bedroom_pop", "BEDROOM POP", 84], ["dream_pop", "DREAM POP", 80], ["shoegaze", "SHOEGAZE WALL", 92], ["indie_rock", "GARAGE INDIE ROCK", 128], ["surf_punk", "SURF PUNK", 168], ["post_punk", "POST-PUNK", 132], ["indie_folk", "INDIE FOLK STOMP", 96], ["synth_pop", "SYNTH-POP 80S", 124], ["disco_pop", "DISCO POP", 112], ["house_4x4", "HOUSE 4X4", 124], ["ukg_2step", "UK GARAGE 2-STEP", 132], ["electro", "ELECTRO 808", 124], ["chillwave", "CHILLWAVE HAZE", 96]]},
    {"id": "rnb_soul", "label": "R&B / SOUL", "genres": [["midnight_halftime", "MIDNIGHT HALF-TIME", 140], ["gospel_piano", "GOSPEL PIANO CONFESSIONAL", 64], ["afro_soul", "AFRO-SOUL SWAY", 100], ["night_sway", "NIGHT SWAY", 112], ["afro_house_soul", "AFTER-HOURS AFRO-HOUSE", 123], ["night_drive_80s", "80S NIGHT DRIVE", 100], ["soul_vamp", "TWO-CHORD SOUL VAMP", 85], ["stacked_heat", "STACKED HEAT", 140], ["alt_soul_lowlight", "ALT-SOUL LOW LIGHT", 90], ["night_call_answer", "NIGHT CALL AND ANSWER", 94], ["soul_night", "SOUL NIGHT", 70]]}
];

// K3 pointer selectors: id -> [labels, values sent]. "-" = leave the key out (preset / auto).
const var PTR = {
    // KEY / SCALE / BARS: position 0 PRESET leaves the key out, so the genre preset fills it (a 16-bar
    // MIDNIGHT HALF-TIME was crammed into 8 bars when 8 was always sent); the server's 10 scales
    "KeyKnob": [["PRESET", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], ["-", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]],
    "ScaleKnob": [["PRESET", "MAJ", "MIN", "HARM MIN", "DORIAN", "PHRYG", "PHR DOM", "MIXO", "MAJ PENT", "MIN PENT", "BLUES"],
                  ["-", "major", "minor", "harmonic_minor", "dorian", "phrygian", "phrygian_dominant", "mixolydian", "major_pentatonic", "minor_pentatonic", "blues"]],
    "BarsKnob": [["PRESET", "4", "8", "12", "16"], ["-", 4, 8, 12, 16]],
    "LangKnob": [["AUTO", "ES", "EN", "PT"], ["-", "es", "en", "pt"]], "VoiceKnob": [["PRESET", "MALE", "FEMALE"], ["-", "male", "female"]],
    "DblKnob": [["0", "2", "4"], [0, 2, 4]],
    "HarmKnob": [["OFF", "3RD", "5TH", "6TH", "OCT", "OCT LO", "3RD+OCT"], ["off", "3rd", "5th", "6th", "oct", "oct_lo", ["3rd", "oct"]]],
    "AdlibKnob": [["OFF", "LAST", "EVEN", "ALL"], [0, 1, 2, 3]],
    "ChainKnob": [["CLOSE", "DRENCHED", "FWD DARK", "TORCH", "RAW HARM", "HEAT", "SMOKE", "CLOSE+"], ["close", "drenched", "forward_dark", "torch", "raw_harmony", "stacked_heat", "smoke", "close_plus"]],
    "TuneModeKnob": [["NOTE", "HARD"], ["note", "hard"]],
    "AcapKnob": [["0", "2", "4"], [0, 2, 4]], "UnderKnob": [["0", "2", "4"], [0, 2, 4]], "SepKKnob": [["0", "1", "2", "3", "4"], [0, 1, 2, 3, 4]],
    "BedKnob": [["OFF", "GENTLE", "HEAVY"], ["off", "gentle", "heavy"]],
    "TierKnob": [["REF", "LOUD", "PRO STEM"], ["ref", "loud", "pro_stem"]], "TightenKnob": [["OFF", "10 MS", "15 MS"], [0, 10, 15]],
    "DcwKnob": [["DEFAULT", "OFF", "THINK"], ["-", "off", "think"]], "CaptionKnob": [["PRESET", "CLEAN", "RAW"], ["-", true, false]],
    "LangWordsKnob": [["AUTO", "ON", "OFF"], ["-", true, false]]
};
const var STEP_IDS = ["FamilyKnob", "GenreKnob", "SeedsKnob"];     // stepped, no printed option

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

// slim lit key with a lamp on the left (rack MANUAL keys, option switches)
inline function drawSlimLit(g, r, label, on, hot)
{
    g.setColour(0xFF0B0B0C);
    g.fillRoundedRectangle([r[0] - 1, r[1] - 1, r[2] + 2, r[3] + 2], 3.0);
    g.setGradientFill([hot ? T.cardHi : T.ivory, 0, r[1], on ? 0xFFC9C6BB : T.ivoryAged, 0, r[1] + r[3], false]);
    g.fillRoundedRectangle(r, 2.5);
    local d = Math.min(8, r[3] - 6);
    drawLamp(g, r[0] + 5, r[1] + (r[3] - d) / 2, d, on, T.lampAmber, T.lampAmberGlow);
    g.setColour(T.cardInk);
    g.setFontWithSpacing(T.FONT, 8, 0.08);
    g.drawAlignedText(label, [r[0] + 8 + d, r[1], r[2] - 10 - d, r[3]], "centred");
}

// small cream key (result rows: PLAY / STOP, drag handle, SAVE; desk actions)
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
    g.drawAlignedText(title, [r[0] + 16, r[1] + 2, r[2] - 32, 14], "left");
}

inline function hitIn(r, x, y)
{
    return x >= r[0] && x < r[0] + r[2] && y >= r[1] && y < r[1] + r[3];
}

// ============================================================================
// KNOBS: K2 collet (continuous), K3 pointer (stepped) per docs/28b; lit keys
// ============================================================================
const var knobLaf = Content.createLocalLookAndFeel();
knobLaf.loadImage("{PROJECT_FOLDER}vm_collet_s_2x.png", "clS");      // 80 px frames, 40 logical
knobLaf.loadImage("{PROJECT_FOLDER}vm_ptr_l_2x.png", "ptrL");        // 96 px frames, 61 angles -150..+150 at 5 deg
knobLaf.registerFunction("drawRotarySlider", function(g, obj)
{
    var w = obj.area[2];
    var cx = w / 2.0;
    var cy = 32.0;
    var R = 16.0;
    var v = obj.valueNormalized;
    var hot = obj.hover || obj.clicked;
    var opt = PTR[obj.id];
    var stepped = isDefined(opt) || STEP_IDS.indexOf(obj.id) >= 0;
    var ang = -2.618 + 5.236 * v;
    if (stepped)
    {
        var n = Math.round(obj.max - obj.min) + 1;
        var st = n <= 4 ? 40.0 : (n <= 9 ? 30.0 : 25.0);
        if ((n - 1) * st > 300.0) st = 300.0 / (n - 1);
        var deg = -0.5 * (n - 1) * st + Math.round(obj.value - obj.min) * st;
        var fr = Math.round((deg + 150.0) / 5.0);
        if (knobLaf.isImageLoaded("ptrL")) g.drawImage("ptrL", [Math.round(cx - 18), Math.round(cy - 18), 36, 36], 0, fr * 96);
        else
        {
            ang = deg / 57.29578;
            g.setColour(T.cap);
            g.fillEllipse([cx - R * 0.62, cy - R * 0.62, R * 1.24, R * 1.24]);
            g.setColour(T.txt);
            g.drawLine(cx, cx + Math.sin(ang) * R, cy, cy - Math.cos(ang) * R, 2.0);
        }
        if (isDefined(opt))
        {
            g.setColour(T.accentInk);
            g.setFontWithSpacing(T.FONT, 8, 0.06);
            g.drawAlignedText(opt[0][Math.round(obj.value - obj.min)], [0, 51, w, 10], "centred");
        }
    }
    else
    {
        var sx = Math.sin(ang);
        var sy = -Math.cos(ang);
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
        if (hot)
        {
            g.setColour(T.accentInk);
            g.setFontWithSpacing(T.FONT, 8, 0.06);
            g.drawAlignedText(obj.valueAsText, [0, 51, w, 10], "centred");
        }
    }
    if (hot)
    {
        g.setColour(Colours.withAlpha(T.accent, 0.35));
        g.drawEllipse([cx - R - 2, cy - R - 2, R * 2 + 4, R * 2 + 4], 1.2);
    }
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(obj.text.toUpperCase(), [0, 0, w, 12], "centred");
});
knobLaf.registerFunction("drawToggleButton", function(g, obj)
{
    drawSlimLit(g, [1, 1, obj.area[2] - 2, obj.area[3] - 2], obj.text, obj.value > 0.5, obj.over);
});

inline function addKnob(id, label, x, y, mn, mx, def, step, parent)
{
    local k = Content.addKnob(id, x, y);
    Content.setPropertiesFromJSON(id, {"width": 56, "height": 62, "text": label, "min": mn, "max": mx,
        "defaultValue": def, "stepSize": step, "saveInPreset": true, "isPluginParameter": false,
        "parentComponent": parent, "showValuePopup": "No"});
    if (isDefined(PTR[id]) || STEP_IDS.indexOf(id) >= 0)
    {
        k.set("dragDirection", "Vertical");
        k.set("mouseSensitivity", Math.max(1, mx - mn) * 36 / 250.0);
    }
    k.setValue(def);
    k.setLocalLookAndFeel(knobLaf);
    return k;
}

inline function addKey(id, label, x, y, w, h, parent)
{
    local b = Content.addButton(id, x, y);
    Content.setPropertiesFromJSON(id, {"width": w, "height": h, "text": label, "saveInPreset": true,
        "isPluginParameter": false, "parentComponent": parent});
    b.setLocalLookAndFeel(knobLaf);
    return b;
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
Content.setPropertiesFromJSON("Lyrics", {"parentComponent": "Core", "width": 304, "height": 154,
    "text": "", "editable": true, "multiline": true, "fontName": "VM Type", "fontSize": 13,
    "textColour": 0xFF2A221A, "bgColour": 0x00000000, "itemColour": 0x00000000, "itemColour2": 0x00000000,
    "alignment": "topLeft", "saveInPreset": true,
    "tooltip": "One sung line per row (8 at most). [Chorus] rows set the section, (words) become answers, one UPPERCASE word is the climax. Start a row with [en], [es] or [pt] to set its language."});
const var VoiceKnob = addKnob("VoiceKnob", "VOICE", 328, 120, 0, 2, 0, 1, "Core");
const var LangKnob = addKnob("LangKnob", "LANG", 328, 184, 0, 3, 0, 1, "Core");
const var KeyKnob = addKnob("KeyKnob", "KEY", 528, 50, 0, 12, 0, 1, "Core");        // 0 = PRESET
const var ScaleKnob = addKnob("ScaleKnob", "SCALE", 590, 50, 0, 10, 0, 1, "Core");
const var BarsKnob = addKnob("BarsKnob", "BARS", 652, 50, 0, 4, 0, 1, "Core");
const var FamilyKnob = addKnob("FamilyKnob", "FAMILY", 400, 140, 0, 5, 0, 1, "Core");      // REGGAETON first
const var GenreKnob = addKnob("GenreKnob", "GENRE", 462, 140, 0, 7, 0, 1, "Core");
const var SeedsKnob = addKnob("SeedsKnob", "TAKES", 676, 140, 1, 8, 4, 1, "Core");
FamilyKnob.set("saveInPreset", false);         // the choice is kept by id in GenreSel (lists can change order)
GenreKnob.set("saveInPreset", false);
const var GenreSel = Content.addLabel("GenreSel", 0, 0);
Content.setPropertiesFromJSON("GenreSel", {"saveInPreset": true, "visible": false, "width": 1, "height": 1, "editable": false, "text": "reggaeton|reggaeton"});

inline function famGenres()
{
    return GENRES[Math.min(GENRES.length - 1, Math.round(FamilyKnob.getValue()))].genres;
}

inline function curFamily()
{
    return GENRES[Math.min(GENRES.length - 1, Math.round(FamilyKnob.getValue()))];
}

inline function curGenre()
{
    local gl = famGenres();
    return gl[Math.min(gl.length - 1, Math.round(GenreKnob.getValue()))];
}

inline function selectGenreById(fid, gid)
{
    local i = 0;
    local j = 0;
    for (i = 0; i < GENRES.length; i++)
    {
        if (GENRES[i].id != fid) continue;
        FamilyKnob.setValue(i);
        GenreKnob.set("max", GENRES[i].genres.length - 1);
        GenreKnob.setValue(0);
        for (j = 0; j < GENRES[i].genres.length; j++)
            if (GENRES[i].genres[j][0] == gid) GenreKnob.setValue(j);
        rememberGenre();
        return true;
    }
    return false;
}

inline function rememberGenre()
{
    GenreSel.setValue(curFamily().id + "|" + curGenre()[0]);
}

inline function onFamily(component, value)
{
    local n = famGenres().length;
    GenreKnob.set("max", n - 1);
    if (GenreKnob.getValue() > n - 1) GenreKnob.setValue(0);
    rememberGenre();
    Core.repaint();
}
FamilyKnob.setControlCallback(onFamily);
inline function onGenre(component, value) { rememberGenre(); Core.repaint(); }
GenreKnob.setControlCallback(onGenre);
inline function onGenreSel(component, value)
{
    local p = ("" + value).split("|");
    if (p.length == 2) selectGenreById(p[0], p[1]);
    Core.repaint();
}
GenreSel.setControlCallback(onGenreSel);
inline function onCoreKnob(component, value) { Core.repaint(); }
KeyKnob.setControlCallback(onCoreKnob);
ScaleKnob.setControlCallback(onCoreKnob);
BarsKnob.setControlCallback(onCoreKnob);
SeedsKnob.setControlCallback(onCoreKnob);
LangKnob.setControlCallback(onCoreKnob);
VoiceKnob.setControlCallback(onCoreKnob);

inline function jobBusy()
{
    return S.job != "" && (S.jstate == "queued" || S.jstate == "running");
}

inline function tileRect(i)
{
    return [10 + (i % 2) * 364, 336 + Math.floor(i / 2) * 27, 358, 24];
}

inline function takeRect(i)
{
    return [10 + i * 182, 300, 176, 30];
}

inline function engineText()
{
    if (S.online)
    {
        if (S.stage == "memory" && jobBusy()) return "MEM WAIT";
        return S.warm ? "ENGINE WARM" : "ENGINE COLD";
    }
    return S.starting ? "STARTING" : "OFFLINE";
}

// the BPM the job sends: the DAW project (SYNC LIVE), else the host, else the genre's own
// the project's tempo when SYNC LIVE or MATCH DAW asks for it, else -1 (the preset's own BPM)
inline function syncedBpm()
{
    local hb = Engine.getHostBpm();
    if (!(S.syncLive || S.match)) return -1;
    if (S.projSrc != "none" && S.projBpm > 0) return S.projBpm;
    if (Engine.isPlugin() && hb > 0) return hb;
    return -1;
}

inline function jobBpm()
{
    local b = syncedBpm();
    return b > 0 ? b : curGenre()[2];
}

inline function keyText()
{
    local k = PTR.KeyKnob[0][Math.round(KeyKnob.getValue())];
    local sc = PTR.ScaleKnob[0][Math.round(ScaleKnob.getValue())];
    local b = PTR.BarsKnob[0][Math.round(BarsKnob.getValue())];
    return (k == "PRESET" ? "PRESET KEY" : k) + " " + (sc == "PRESET" ? "" : sc) + "  " + (b == "PRESET" ? "PRESET BARS" : b + " BARS");
}

inline function projText()
{
    if (S.projSrc == "live_bridge") return "LIVE KEY";
    if (S.projSrc == "post") return "HOST TEMPO";
    return "MANUAL";
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
    var memw = engineText() == "MEM WAIT";
    var blink = (S.starting || memw) && S.tick % 2 == 0;
    var lampOn = (S.online && !memw) || blink;
    drawLamp(g, 170, 15, 12, lampOn, S.warm && !memw ? T.lampGreen : T.lampAmber, S.warm && !memw ? T.lampGreenGlow : T.lampAmberGlow);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.1);
    g.drawAlignedText(engineText(), [188, 10, 120, 22], "left");
    if (!S.online)
    {
        drawPush(g, 300, 11, 22, hv == "start", false, !S.starting);
        g.drawAlignedText(S.starting ? "LAUNCHING (NO WINDOW)" : "START ENGINE", [328, 10, 170, 22], "left");
    }
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText(S.online && !S.warm ? "The engine loads on the first render (about a minute)." : "AI VOCAL. The engine runs in the Hook Lab app, not here.", [400, 28, 278, 10], "left");
    drawLit(g, [682, 8, 56, 30], S.expanded ? "COMPACT" : "EXPAND", S.expanded, hv == "view");

    // lyric sheet
    drawCard(g, [10, 50, 380, 196]);
    g.setColour(T.cardDim);
    g.setFont(T.TYPE, 10);
    var nl = 0;
    var rows = Lyrics.get("text").split("\n");
    for (k = 0; k < rows.length; k++) if (rows[k].trim() != "" && rows[k].trim().substring(0, 1) != "[") nl = nl + 1;
    g.setColour(nl > 8 ? T.cardRed : T.cardDim);
    g.drawAlignedText(nl + " / 8 SUNG LINES", [18, 220, 300, 12], "left");
    g.setColour(T.cardDim);
    g.drawAlignedText("[Chorus] rows   (answers)   one UPPERCASE word", [18, 232, 304, 12], "left");

    // groove strip
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText("BPM", [400, 42, 120, 10], "left");
    var gn = curGenre();
    drawLed(g, [400, 54, 120, 26], Engine.doubleToString(jobBpm(), 1), T.DIGITS, 14);
    drawLit(g, [400, 88, 56, 30], "SYNC LIVE", S.syncLive, hv == "sync");
    drawLamp(g, 466, 95, 12, S.projSrc == "live_bridge", T.lampAmber, T.lampAmberGlow);
    g.setColour(T.txt);
    g.drawAlignedText(projText(), [482, 93, 60, 16], "left");
    drawLed(g, [528, 116, 208, 22], keyText(), T.ALPHA, 10);

    // genre family -> genre, INTENSE, MATCH DAW
    drawLed(g, [400, 210, 336, 24], curFamily().label + " / " + gn[1], T.ALPHA, 9);
    drawLit(g, [530, 148, 64, 40], "INTENSE", S.intense, hv == "intense");
    drawLit(g, [604, 148, 64, 40], "MATCH DAW", S.match, hv == "match");
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText(S.genresFromServer ? "genres from the engine" : "built-in genre list", [400, 236, 200, 12], "left");

    // render row: RENDER (or CANCEL while busy), job LCD, progress, message line
    var busy = jobBusy();
    drawPush(g, 12, 254, 28, hv == "render", false, S.online);
    g.setColour(T.txt);
    g.setFontWithSpacing(T.FONT, 9, 0.08);
    g.drawAlignedText(busy ? "CANCEL" : "RENDER", [2, 284, 48, 10], "centred");
    drawLamp(g, 50, 264, 10, busy, T.lampAmber, T.lampAmberGlow);
    drawLed(g, [68, 254, 420, 30], S.lcd, T.ALPHA, 12);
    g.setColour(T.well);
    g.fillRect([500, 264, 236, 10]);
    g.setColour(T.accent);
    g.fillRect([500, 264, 236 * Math.range(S.pct / 100.0, 0.0, 1.0), 10]);
    g.setColour(S.jstate == "error" ? T.lampRedGlow : T.dim);
    g.setFont(T.FONT, 9);
    var line2 = S.msg;
    if (S.confText != "") line2 = S.confText + (line2 != "" ? "   " + line2 : "");
    g.drawAlignedText(line2, [68, 285, 668, 12], "left");

    // takes: kept take first; click plays its dry take, drag it into the DAW
    for (k = 0; k < 4; k++)
    {
        var r = takeRect(k);
        var has = k < S.takes.length;
        if (!has) g.setOpacity(0.4);
        drawCard(g, r);
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 11);
        g.drawAlignedText("TAKE " + "ABCD".substring(k, k + 1), [r[0] + 8, r[1], 70, r[3]], "left");
        if (has)
        {
            var tk = S.takes[k];
            g.setColour(tk.ler > 0.30 ? T.cardRed : T.cardDim);
            g.setFont(T.TYPE, 10);
            g.drawAlignedText(tk.ler >= 0 ? "LER " + Math.round(tk.ler * 100) + "%" : "--", [r[0] + 70, r[1], 70, r[3]], "left");
            drawLamp(g, r[0] + r[2] - 18, r[1] + 10, 10, tk.kept || S.playing == "take" + k, S.playing == "take" + k ? T.lampGreen : T.lampAmber, S.playing == "take" + k ? T.lampGreenGlow : T.lampAmberGlow);
        }
        g.setOpacity(1.0);
    }
    // stem tiles (PLAY / STOP, drag into the DAW, SAVE); NO STEM EXP when stem_export_ok is false
    for (k = 0; k < TILES.length; k++)
    {
        var sr = tileRect(k);
        var ok = tilePaths(TILES[k][0]).length > 0;
        if (!ok) g.setOpacity(0.4);
        drawCard(g, sr);
        g.setColour(T.cardInk);
        g.setFont(T.TYPEB, 11);
        g.drawAlignedText(TILES[k][1], [sr[0] + 8, sr[1], 96, sr[3]], "left");
        g.setOpacity(1.0);
        if (ok && !S.exportOk && NOT_STEM_SAFE.indexOf(TILES[k][0]) >= 0)
        {
            drawLamp(g, sr[0] + 60, sr[1] + 9, 6, true, T.lampRed, T.lampRedGlow);
            g.setColour(T.cardRed);
            g.setFont(T.FONT, 7);
            g.drawAlignedText("NOT FOR STEM EXPORT", [sr[0] + 68, sr[1], 44, sr[3]], "left");
        }
        drawKey(g, [sr[0] + 114, sr[1] + 3, 52, 18], S.playing == TILES[k][0] ? "STOP" : "PLAY", hv == "play" + k, ok);
        drawKey(g, [sr[0] + 172, sr[1] + 3, 96, 18], isMatched(TILES[k][0]) ? "DRAG (MATCHED)" : "DRAG TO DAW", hv == "drag" + k, ok);
        drawKey(g, [sr[0] + 274, sr[1] + 3, 76, 18], "SAVE", hv == "save" + k, ok);
    }
});

inline function hitCore(x, y)
{
    local k = 0;
    if (x >= 682 && x < 738 && y >= 8 && y < 38) return "view";
    if (!S.online && x >= 298 && x < 324 && y >= 9 && y < 35) return "start";
    if (x >= 400 && x < 456 && y >= 88 && y < 118) return "sync";
    if (x >= 530 && x < 594 && y >= 148 && y < 188) return "intense";
    if (x >= 604 && x < 668 && y >= 148 && y < 188) return "match";
    if (x >= 8 && x < 44 && y >= 250 && y < 286) return "render";
    for (k = 0; k < 4; k++)
        if (hitIn(takeRect(k), x, y)) return "take" + k;
    for (k = 0; k < TILES.length; k++)
    {
        local sr = tileRect(k);
        if (!hitIn(sr, x, y)) continue;
        if (x >= sr[0] + 114 && x < sr[0] + 166) return "play" + k;
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
        else if (h == "match") { S.match = !S.match; S.conf = {}; S.confText = ""; S.needConform = S.match; this.repaint(); }
        else if (h == "render" && S.online)
        {
            if (jobBusy()) cancelJob();
            else submitRender();
        }
        else if (h.indexOf("take") == 0) toggleTake(parseInt(h.substring(4, 5)));
        else if (h.indexOf("play") == 0) togglePlay(TILES[parseInt(h.substring(4, 5))][0]);
        else if (h.indexOf("save") == 0) saveTile(TILES[parseInt(h.substring(4, 5))][0]);
    }
    if (event.drag)
    {
        var dh = hitCore(event.mouseDownX, event.mouseDownY);
        if (dh.indexOf("drag") == 0)
        {
            var dp = tilePaths(TILES[parseInt(dh.substring(4, 5))][0]);
            if (dp.length > 0) this.startExternalFileDrag(dp, false, function() {});
        }
        else if (dh.indexOf("take") == 0)
        {
            var tp = takePath(parseInt(dh.substring(4, 5)));
            if (tp != "") this.startExternalFileDrag(tp, false, function() {});
        }
    }
    if (h != S.hover)
    {
        S.hover = h;
        this.repaint();
    }
});

// ============================================================================
// EXPANDED RACKS (docs/28b): right column STACK / LEVELS / VOICE / MIX,
// bottom PERFORMANCE / BED / OUTPUT, and the TAKES / LINES / FIX desk
// ============================================================================
const var Racks = Content.addPanel("Racks", CW + 8, 10);
Content.setPropertiesFromJSON("Racks", {"width": 404, "height": 444, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});
const var Lower = Content.addPanel("Lower", 20, CH + 8);
Content.setPropertiesFromJSON("Lower", {"width": 564, "height": 312, "allowCallbacks": "No Callbacks", "saveInPreset": false, "visible": false});

// [id, label, panel, x, y, min, max, default, step, request path, rack, multiplier]
// rack "out" is always sent; a pointer value "-" leaves the key out.
const var RK = [
    ["DblKnob", "DOUBLES", "Racks", 14, 20, 0, 2, 1, 1, "stack.dbl", "stack", 1],
    ["VarKnob", "VARIANCE", "Racks", 76, 20, 0.05, 0.25, 0.10, 0.01, "stack.retake_variance", "stack", 1],
    ["HarmKnob", "HARMONY", "Racks", 138, 20, 0, 6, 1, 1, "stack.harm", "stack", 1],
    ["AdlibKnob", "AD-LIBS", "Racks", 200, 20, 0, 3, 1, 1, "stack.adlib", "stack", 1],
    ["WidthKnob", "WIDTH", "Racks", 262, 20, 0.5, 1.0, 1.0, 0.01, "stack.width", "stack", 1],
    ["BusGrKnob", "BUS GLUE", "Racks", 324, 20, 0, 3, 1.5, 0.1, "stack.bus_gr", "stack", 1],
    ["GDblKnob", "DBL DB", "Racks", 14, 168, -30, 6, 0, 0.5, "stack.gain_db.dbl", "levels", 1],
    ["GHiKnob", "HARM HI", "Racks", 76, 168, -30, 6, 0, 0.5, "stack.gain_db.harm_hi", "levels", 1],
    ["GLoKnob", "HARM LO", "Racks", 138, 168, -30, 6, 0, 0.5, "stack.gain_db.harm_lo", "levels", 1],
    ["GAdKnob", "AD-LIB DB", "Racks", 200, 168, -30, 6, 0, 0.5, "stack.gain_db.adlib", "levels", 1],
    ["GAnsKnob", "ANSWER DB", "Racks", 262, 168, -30, 6, 0, 0.5, "stack.gain_db.answer", "levels", 1],
    ["SpaceKnob", "BV SPACE", "Racks", 324, 168, -30, 0, -10, 0.5, "stack.space_db", "levels", 1],
    ["ChainKnob", "CHAIN", "Racks", 14, 254, 0, 7, 0, 1, "chain", "voice", 1],
    ["TuneModeKnob", "TUNE MODE", "Racks", 76, 254, 0, 1, 0, 1, "expr.tune_mode", "voice", 1],
    ["TuneKnob", "TUNE", "Racks", 138, 254, 0, 100, 60, 1, "expr.tune", "voice", 0.01],
    ["RetuneKnob", "RETUNE MS", "Racks", 200, 254, 0, 120, 40, 1, "expr.retune_ms", "voice", 1],
    ["VibRateKnob", "VIB RATE", "Racks", 262, 254, 3.0, 8.0, 5.3, 0.1, "expr.vib_rate", "voice", 1],
    ["VibDepthKnob", "VIB DEPTH", "Racks", 324, 254, 0, 100, 30, 1, "expr.vib_depth_c", "voice", 1],
    ["AirKnob", "AIR", "Racks", 6, 340, 0, 4, 1.5, 0.1, "fx.air_db", "mix", 1],
    ["DeessKnob", "DE-ESS", "Racks", 62, 340, 0, 10, 4, 0.1, "fx.deess_db", "mix", 1],
    ["DriveKnob", "DRIVE", "Racks", 118, 340, 0, 25, 6, 1, "fx.sat_mix", "mix", 0.01],
    ["RoomKnob", "ROOM", "Racks", 174, 340, 0, 1, 0.4, 0.01, "fx.room", "mix", 1],
    ["PreDlyKnob", "PRE-DLY", "Racks", 230, 340, 0, 80, 20, 1, "fx.predelay_ms", "mix", 1],
    ["HallKnob", "HALL", "Racks", 286, 340, 0, 0.5, 0.2, 0.01, "hall_mix", "mix", 1],
    ["EchoKnob", "ECHO", "Racks", 342, 340, 0, 0.5, 0.16, 0.01, "echo_mix", "mix", 1],
    ["AcapKnob", "A CAPPELLA", "Lower", 14, 56, 0, 2, 0, 1, "acappella_beats", "perf", 1],
    ["UnderKnob", "UNDERWATER", "Lower", 76, 56, 0, 2, 0, 1, "underwater_bars", "perf", 1],
    ["SepKKnob", "SEP TOP-K", "Lower", 138, 56, 0, 4, 2, 1, "sep_top_k", "perf", 1],
    ["BedKnob", "BED", "Lower", 14, 210, 0, 2, 0, 1, "bed", "bed", 1],
    ["SubKnob", "SUB 60", "Lower", 76, 210, 0, 3, 1, 0.1, "bed_sub_db", "bed", 1],
    ["DuckKnob", "DUCK", "Lower", 138, 210, 0, 3, 1, 0.1, "bed_duck_db", "bed", 1],
    ["TrimKnob", "TRIM", "Lower", 200, 210, -3, 0, 0, 0.1, "bed_trim_db", "bed", 1],
    ["TierKnob", "OUT TIER", "Lower", 298, 26, 0, 2, 0, 1, "out_tier", "out", 1],
    ["TightenKnob", "TIGHTEN", "Lower", 298, 100, 0, 2, 0, 1, "tighten_ms", "out", 1],
    ["DcwKnob", "DCW", "Lower", 360, 100, 0, 2, 0, 1, "dcw", "out", 1],
    ["CaptionKnob", "CAPTION", "Lower", 422, 100, 0, 2, 0, 1, "caption_hygiene", "out", 1],
    ["LangWordsKnob", "LANG WORDS", "Lower", 484, 100, 0, 2, 0, 1, "lang_words", "out", 1]
];
// [id, label, panel, x, y, w, request path, rack, value off, value on]
const var RB = [
    ["DblSrcBtn", "RETAKE DOUBLES", "Racks", 14, 96, 118, "stack.dbl_src", "stack", "varispeed", "retake"],
    ["AnswerBtn", "COUNTER ANSWERS", "Racks", 140, 96, 118, "stack.answer_src", "stack", "derived", "counter"],
    ["SlapBtn", "SLAP", "Racks", 224, 323, 70, "fx.slap", "mix", false, true],
    ["ArcBtn", "ARC", "Lower", 14, 26, 70, "arc", "perf", false, true],
    ["CompBtn", "COMP X2", "Lower", 92, 26, 70, "comp_x2", "perf", false, true],
    ["OpenBtn", "OPEN ON HOOK", "Lower", 14, 180, 100, "bed_open_on_hook", "bed", false, true],
    ["MonitorBtn", "SMALL SPEAKER", "Lower", 360, 40, 110, "monitor", "out", "off", "small"]
];
// MANUAL key per rack: [id, rack, panel, x, y]
const var RM = [["ManStack", "stack", "Racks", 306, 1], ["ManLevels", "levels", "Racks", 306, 151], ["ManVoice", "voice", "Racks", 306, 237],
                ["ManMix", "mix", "Racks", 306, 323], ["ManPerf", "perf", "Lower", 196, 1], ["ManBed", "bed", "Lower", 196, 155]];
const var RKC = {};
const var RBC = {};
const var RMC = {};
var ri = 0;
for (ri = 0; ri < RK.length; ri++)
{
    var rk = RK[ri];
    RKC[rk[0]] = addKnob(rk[0], rk[1], rk[3], rk[4], rk[5], rk[6], rk[7], rk[8], rk[2]);
}
for (ri = 0; ri < RB.length; ri++)
{
    var rb = RB[ri];
    RBC[rb[0]] = addKey(rb[0], rb[1], rb[3], rb[4], rb[5], 20, rb[2]);
}
for (ri = 0; ri < RM.length; ri++)
{
    var rm = RM[ri];
    RMC[rm[1]] = addKey(rm[0], "MANUAL", rm[3], rm[4], 80, 15, rm[2]);
}
inline function onRackCtl(component, value)
{
    Racks.repaint();
    Lower.repaint();
}
for (ri = 0; ri < RK.length; ri++) RKC[RK[ri][0]].setControlCallback(onRackCtl);
for (ri = 0; ri < RB.length; ri++) RBC[RB[ri][0]].setControlCallback(onRackCtl);
for (ri = 0; ri < RM.length; ri++) RMC[RM[ri][1]].setControlCallback(onRackCtl);

inline function rackOn(rack)
{
    return rack == "out" || RMC[rack].getValue() > 0.5;
}

inline function rackReadout(g, rack, r, text)
{
    g.setColour(rackOn(rack) ? T.dim : T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText(rackOn(rack) ? text : "PRESET VALUES (light MANUAL to override)", r, "left");
}

Racks.setPaintRoutine(function(g)
{
    plate(g, [0, 0, 404, 146], "STACK");
    plate(g, [0, 150, 404, 82], "LEVELS");
    plate(g, [0, 236, 404, 82], "VOICE");
    plate(g, [0, 322, 404, 122], "MIX");
    rackReadout(g, "stack", [14, 124, 380, 12], "Doubles, harmony and ad-libs are built in post from the kept take.");
    rackReadout(g, "mix", [14, 408, 380, 12], "AIR / DE-ESS / DRIVE / ROOM move a CLOSE job onto the table-driven chain.");
    g.setColour(T.faint);
    g.setFont(T.FONT, 9);
    g.drawAlignedText("VIB RATE / DEPTH act only when the preset runs soulfx.", [14, 424, 380, 12], "left");
});

Lower.setPaintRoutine(function(g)
{
    plate(g, [0, 0, 280, 150], "PERFORMANCE");
    plate(g, [0, 154, 280, 156], "BED");
    plate(g, [284, 0, 280, 310], "OUTPUT / ENGINE");
    rackReadout(g, "perf", [14, 124, 260, 12], "ARC sings whisper then power (needs COMP X2).");
    rackReadout(g, "bed", [14, 280, 260, 12], "NIGHT BED: sub, duck keyed by the lead, trim.");
    g.setColour(T.dim);
    g.setFont(T.FONT, 9);
    var tier = Math.round(RKC.TierKnob.getValue());
    var tt = tier == 2 ? "PRO STEM: -18 LUFS, no limiter, dry stack parts" : (tier == 1 ? "LOUD: -14 LUFS, -1 dBTP" : "REF: lead -16 LUFS, -1 dBTP");
    g.drawAlignedText(tt, [298, 176, 260, 12], "left");
    g.drawAlignedText("TIGHTEN pulls onsets to the 1/16 grid.", [298, 192, 260, 12], "left");
    g.setColour(T.faint);
    g.drawFittedText(S.gateText, [298, 214, 256, 40], "topLeft", 3, 1.0);
    g.drawFittedText("Every stem folder carries provenance.json: " + S.disclosure + ".", [298, 262, 256, 30], "topLeft", 2, 1.0);
});

// TAKES / LINES / FIX desk
const var Qa = Content.addPanel("Qa", 588, CH + 8);
Content.setPropertiesFromJSON("Qa", {"width": 592, "height": 312, "allowCallbacks": "Clicks & Hover", "saveInPreset": false, "visible": false});
const var QA_ACT = [["lock", "LOCK", 12], ["counter", "COUNTER", 98], ["score", "SCORE", 184], ["release", "RELEASE ENGINE", 270], ["cancel", "CANCEL", 392]];

inline function fixRect(i)
{
    return [536, 41 + i * 18, 40, 15];
}

Qa.setPaintRoutine(function(g)
{
    var hv = S.qhover;
    var i = 0;
    plate(g, [0, 0, 592, 312], "TAKES / LINES / FIX");
    drawCard(g, [12, 22, 280, 172]);
    drawCard(g, [300, 22, 280, 172]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPEB, 10);
    g.drawAlignedText("TAKE  SEED      LER   E     SCORE", [20, 25, 266, 14], "left");
    g.drawAlignedText("LINE  HEARD                LER", [308, 25, 226, 14], "left");
    g.setFont(T.TYPE, 10);
    for (i = 0; i < Math.min(8, S.takes.length); i++)
    {
        var tk = S.takes[i];
        g.setColour(tk.ler > 0.30 ? T.cardRed : T.cardInk);
        var tline = "ABCDEFGH".substring(i, i + 1) + "     " + tk.name;
        g.drawAlignedText(tline, [20, 41 + i * 18, 120, 14], "left");
        g.drawAlignedText((tk.ler >= 0 ? Math.round(tk.ler * 100) + "%" : "--") + "   " + (tk.e >= 0 ? Engine.doubleToString(tk.e, 2) : "--") + "  " + (tk.score > -900 ? Engine.doubleToString(tk.score, 2) : "--") + (tk.kept ? "  KEPT" : ""), [130, 41 + i * 18, 160, 14], "left");
    }
    for (i = 0; i < Math.min(8, S.lines.length); i++)
    {
        var ln = S.lines[i];
        g.setColour(ln.fix ? T.cardRed : T.cardInk);
        g.drawAlignedText((i + 1) + "  " + ln.heard, [308, 41 + i * 18, 186, 14], "left");
        g.drawAlignedText(ln.ler >= 0 ? Math.round(ln.ler * 100) + "%" : "--", [494, 41 + i * 18, 40, 14], "left");
        drawKey(g, fixRect(i), "FIX", hv == "fix" + i, S.online && !jobBusy() && S.stemJob != "");
    }
    if (S.lines.length == 0)
    {
        g.setColour(T.cardDim);
        g.drawFittedText("Lines appear when a hook is done. Red = above the FIX trigger (30% of the words misheard). FIX repaints one line into a new folder; the source is never touched.", [308, 44, 264, 140], "topLeft", 8, 1.0);
    }
    var done = S.stemJob != "";
    for (i = 0; i < QA_ACT.length; i++)
    {
        var qa = QA_ACT[i];
        var en = qa[0] == "cancel" ? jobBusy() : (qa[0] == "release" ? S.online && !jobBusy() : S.online && done && !jobBusy());
        drawKey(g, [qa[2], 202, qa[0] == "release" ? 114 : 78, 20], qa[1], hv == qa[0], en);
    }
    drawCard(g, [12, 230, 568, 74]);
    g.setColour(T.cardInk);
    g.setFont(T.TYPE, 10);
    var info = "JOB " + (S.job == "" ? "-" : S.job + "  " + S.kind + "  " + S.preset) + "   " + S.lcd;
    info = info + "\nKEPT LER " + (S.ler >= 0 ? Math.round(S.ler * 100) + "%" : "--") + "   WORST LINE " + (S.worst >= 0 ? Math.round(S.worst * 100) + "%" : "--") + "   E " + (S.E >= 0 ? Engine.doubleToString(S.E, 2) : "--") + "   " + S.timing;
    info = info + "\n" + (S.folder == "" ? "FOLDER -" : S.folder);
    info = info + "\n" + (S.scoreText != "" ? S.scoreText : (S.exportOk ? "Stems OK for stem export." : "LEAD has Core Library breaths printed in: not for stem export."));
    g.drawFittedText(info, [20, 234, 552, 66], "topLeft", 4, 0.9);
});

inline function hitQa(x, y)
{
    local i = 0;
    for (i = 0; i < Math.min(8, S.lines.length); i++)
        if (hitIn(fixRect(i), x, y)) return "fix" + i;
    for (i = 0; i < QA_ACT.length; i++)
        if (hitIn([QA_ACT[i][2], 202, QA_ACT[i][0] == "release" ? 114 : 78, 20], x, y)) return QA_ACT[i][0];
    return "";
}

Qa.setMouseCallback(function(event)
{
    var h = hitQa(event.x, event.y);
    if (event.clicked)
    {
        var done = S.stemJob != "";
        if (h.indexOf("fix") == 0 && S.online && done && !jobBusy()) fixLine(parseInt(h.substring(3, 4)) + 1);
        else if (h == "lock" && S.online && done && !jobBusy()) lockJob(false);
        else if (h == "counter" && S.online && done && !jobBusy()) lockJob(true);
        else if (h == "score" && S.online && done && !jobBusy()) scoreJob();
        else if (h == "release" && S.online && !jobBusy()) releaseEngine();
        else if (h == "cancel" && jobBusy()) cancelJob();
    }
    if (h != S.qhover)
    {
        S.qhover = h;
        this.repaint();
    }
});

inline function setView(expand)
{
    S.expanded = expand;
    Racks.showControl(expand);
    Lower.showControl(expand);
    Qa.showControl(expand);
    Content.setWidth(expand ? FW : CW);
    Content.setHeight(expand ? FH : CH);
    Bg.repaint();
    Core.repaint();
}

// ============================================================================
// SERVER CLIENT (API.md section 12: submit then poll, every call under 10 s)
// ============================================================================
Server.setBaseURL(HOOKLAB_URL);
Server.setEnforceTrailingSlash(false);
Server.setHttpHeader("Content-Type: application/json");
const var Player = Synth.getAudioSampleProcessor("Hook Player");
const var HlTask = Engine.createBackgroundTask("Hook Lab start");
Globals.hlPlay = false;
Globals.hlPlayEpoch = 0;

inline function setPath(o, path, v)
{
    local parts = path.split(".");
    local cur = o;
    local i = 0;
    for (i = 0; i < parts.length - 1; i++)
    {
        if (!isDefined(cur[parts[i]])) cur[parts[i]] = {};
        cur = cur[parts[i]];
    }
    cur[parts[parts.length - 1]] = v;
}

inline function getPath(o, path)
{
    local parts = path.split(".");
    local cur = o;
    local i = 0;
    for (i = 0; i < parts.length; i++)
    {
        if (!isDefined(cur[parts[i]])) return "";
        cur = cur[parts[i]];
    }
    return cur;
}

inline function lyricLines()
{
    local out = [];
    local rows = Lyrics.get("text").split("\n");
    local i = 0;
    local def = PTR.LangKnob[1][Math.round(LangKnob.getValue())];
    for (i = 0; i < rows.length; i++)
    {
        local r = rows[i].trim();
        if (r == "") continue;
        local lang = def;
        local pre = r.substring(0, 4).toLowerCase();
        if (pre == "[en]" || pre == "[es]" || pre == "[pt]") { lang = pre.substring(1, 3); r = r.substring(4, r.length).trim(); }
        if (r == "") continue;
        if (lang == "-" || r.substring(0, 1) == "[") out.push(r);   // tag rows and auto-language lines go as text
        else out.push({"text": r, "lang": lang});
    }
    return out;
}

inline function rackValue(rk)
{
    local c = RKC[rk[0]];
    if (isDefined(PTR[rk[0]])) return PTR[rk[0]][1][Math.round(c.getValue() - rk[5])];
    return Math.round(c.getValue() * rk[11] * 1000.0) / 1000.0;
}

inline function buildJob()
{
    local gn = curGenre();
    local fam = curFamily();
    local seeds = Math.round(SeedsKnob.getValue());
    if (fam.id != "rnb_soul") seeds = Math.min(4, seeds);        // 1-8 only on the R&B / SOUL presets
    local job = {
        "lines": lyricLines(),
        "family": fam.id,
        "genre": gn[0],
        "n_seeds": seeds
    };
    // only what the user set (or the DAW sync) goes out: the genre preset fills the rest
    local kv = PTR.KeyKnob[1][Math.round(KeyKnob.getValue())];
    local sv = PTR.ScaleKnob[1][Math.round(ScaleKnob.getValue())];
    local bv = PTR.BarsKnob[1][Math.round(BarsKnob.getValue())];
    if (("" + kv) != "-") job.key = kv;
    if (("" + sv) != "-") job.scale = sv;
    if (("" + bv) != "-") job.bars = bv;
    if (syncedBpm() > 0) job.bpm = syncedBpm();
    local i = 0;
    local v = 0;
    local voice = PTR.VoiceKnob[1][Math.round(VoiceKnob.getValue())];
    if (voice != "-") job.voice = voice;
    if (S.intense) job.intense = true;
    for (i = 0; i < RK.length; i++)
    {
        if (!rackOn(RK[i][10])) continue;
        v = rackValue(RK[i]);
        if (("" + v) == "-") continue;
        setPath(job, RK[i][9], v);
    }
    for (i = 0; i < RB.length; i++)
    {
        if (!rackOn(RB[i][7])) continue;
        setPath(job, RB[i][6], RBC[RB[i][0]].getValue() > 0.5 ? RB[i][9] : RB[i][8]);
    }
    if (isDefined(job.arc) && job.arc == true) job.comp_x2 = true;     // ARC without COMP x2 is a 422
    return job;
}

inline function stopPlay()
{
    if (S.playing == "") return;
    S.playing = "";
    Globals.hlPlay = false;
    Globals.hlPlayEpoch = Globals.hlPlayEpoch + 1;
}

inline function clearResults()
{
    S.takes = [];
    S.lines = [];
    S.orig = {};
    S.conf = {};
    S.takeFiles = {};
    S.folder = "";
    S.exportOk = true;
    S.stemsFor = "";
    S.stemJob = "";
    S.confText = "";
    S.conformId = "";
    S.scoreText = "";
    S.ler = -1;
    S.worst = -1;
    S.E = -1;
    S.timing = "";
}

// a new job id from /render/, /fix_line/ or /lock/: polled the same way
inline function startedJob(status, response, kind)
{
    if (status == 200 && isDefined(response.id))
    {
        S.job = "" + response.id;
        S.jstate = isDefined(response.state) ? "" + response.state : "queued";
        S.lcd = isDefined(response.lcd) ? "" + response.lcd : "QUEUED";
        S.kind = kind;
        S.msg = isDefined(response.warnings) && response.warnings.length > 0 ? "" + response.warnings[0] : "";
    }
    else
    {
        S.jstate = "error";
        S.lcd = "REFUSED";
        S.msg = isDefined(response) && isDefined(response.error) ? "" + response.error : "the server refused the request (" + status + ")";
    }
    Core.repaint();
    Qa.repaint();
}

// ---- request gate (2026-11-24 Live crashes): HISE 4.1.0's server queue was unlocked, and this
// script piled 3-5 calls a second onto it, some started from inside callbacks. Now ONE request is
// on the queue at a time: fly() before every call, land() first thing in every callback (status 0
// on a timeout still calls back), a 15 s stale guard, polls on a 2 s cycle, user actions in a
// one-slot queue sent before any poll, and no call is ever started from inside a callback.
const var FLIGHT = {"tag": "", "at": 0};
inline function gateFree()
{
    return FLIGHT.tag == "" || S.tick - FLIGHT.at > 30;      // HISE gives up after 10 s
}
inline function fly(tag)
{
    FLIGHT.tag = tag;
    FLIGHT.at = S.tick;
}
inline function land()
{
    FLIGHT.tag = "";
}
Server.setTimeoutMessageString("{\"error\": \"no answer from Hook Lab (timeout)\"}");

inline function queueAct(a, body)
{
    S.act = a;
    S.actBody = body;
}

inline function submitRender()
{
    local job = buildJob();
    if (job.lines.length == 0) { S.lcd = "NO LYRICS"; S.msg = "Type at least one sung line."; Core.repaint(); return; }
    stopPlay();
    clearResults();
    S.job = "";
    S.jstate = "queued";
    S.lcd = "SENDING";
    S.msg = "";
    S.pct = 0;
    S.preset = curGenre()[0];
    queueAct("render", job);
    Core.repaint();
}

inline function fixLine(n)
{
    S.lcd = "SENDING";
    queueAct("fix", {"job": S.stemJob, "line": n, "passes": 2});
}

inline function lockJob(counter)
{
    S.lcd = "SENDING";
    queueAct("lock", {"job": S.stemJob, "counter": counter});
}

inline function cancelJob()
{
    if (S.job == "") return;
    queueAct("cancel", {});
}

inline function scoreJob()
{
    S.scoreText = "Writing the guide score ...";
    Qa.repaint();
    queueAct("score", {"job": S.stemJob});
}

inline function releaseEngine()
{
    queueAct("release", {});
}

// the queued user action, sent by the clock when the gate is free
inline function doAct()
{
    local a = S.act;
    S.act = "";
    fly(a);
    if (a == "render")
        Server.callWithPOST("/render/", JSON.stringify(S.actBody), function(status, response) { land(); startedJob(status, response, "render"); });
    else if (a == "fix")
        Server.callWithPOST("/fix_line/", JSON.stringify(S.actBody), function(status, response) { land(); startedJob(status, response, "fix"); });
    else if (a == "lock")
        Server.callWithPOST("/lock/", JSON.stringify(S.actBody), function(status, response) { land(); startedJob(status, response, "lock"); });
    else if (a == "cancel")
    {
        Server.callWithPOST("/cancel/" + S.job, "{}", function(status, response)
        {
            land();
            if (status == 200 && isDefined(response.message)) S.msg = "" + response.message;
            Core.repaint();
        });
    }
    else if (a == "score")
    {
        Server.callWithPOST("/score/", JSON.stringify(S.actBody), function(status, response)
        {
            land();
            if (status == 200 && isDefined(response.musicxml)) S.scoreText = "SCORE " + response.musicxml + " (+ .ustx)";
            else S.scoreText = "SCORE failed: " + (isDefined(response) && isDefined(response.error) ? response.error : status);
            Qa.repaint();
        });
    }
    else if (a == "release")
    {
        Server.callWithPOST("/engine/release", "{}", function(status, response)
        {
            land();
            S.msg = status == 200 ? "Engine released: its memory is back." : (isDefined(response) && isDefined(response.error) ? "" + response.error : "release refused (" + status + ")");
            Core.repaint();
        });
    }
    else land();
}

inline function applyQa(q)
{
    local i = 0;
    local kept = isDefined(q.best_seed) ? "" + q.best_seed : "";
    S.takes = [];
    S.lines = [];
    if (isDefined(q.seeds))
    {
        // kept take first, then the others in the server's order (Array.sort cannot order objects)
        for (i = 0; i < q.seeds.length; i++)
        {
            local sd = q.seeds[i];
            local t = {"seed": "" + sd.seed, "name": isDefined(sd.name) ? "" + sd.name : "seed" + sd.seed,
                       "ler": isDefined(sd.ler) ? sd.ler : -1, "e": isDefined(sd.E) ? sd.E : -1,
                       "score": isDefined(sd.score) ? sd.score : -999, "kept": ("" + sd.seed) == kept};
            if (t.kept) S.takes.insert(0, t);
            else S.takes.push(t);
        }
    }
    if (isDefined(q.lines))
    {
        for (i = 0; i < q.lines.length; i++)
        {
            local ln = q.lines[i];
            S.lines.push({"heard": isDefined(ln.heard) ? "" + ln.heard : (isDefined(ln.typed) ? "" + ln.typed : ""),
                          "ler": isDefined(ln.ler) ? ln.ler : -1, "fix": isDefined(ln.fix) && ln.fix == true});
        }
    }
    S.ler = isDefined(q.ler) ? q.ler : -1;
    S.worst = isDefined(q.worst_line_ler) ? q.worst_line_ler : -1;
    S.E = isDefined(q.E) ? q.E : -1;
    if (isDefined(q.stem_export_ok)) S.exportOk = q.stem_export_ok == true;
}

inline function applyStems(r)
{
    local i = 0;
    local j = 0;
    S.orig = {};
    for (i = 0; i < TILES.length; i++)
    {
        for (j = 0; j < TILES[i][2].length; j++)
        {
            local key = TILES[i][2][j];
            local p = getPath(r, key);
            if (("" + p) != "")
            {
                local parts = key.split(".");
                S.orig[parts[parts.length - 1]] = "" + p;
            }
        }
    }
    S.takeFiles = isDefined(r.takes) ? r.takes : {};
    S.folder = isDefined(r.folder) ? "" + r.folder : "";
    if (isDefined(r.stem_export_ok)) S.exportOk = r.stem_export_ok == true;
    if (isDefined(r.disclosure)) S.disclosure = "" + r.disclosure;
    S.outTier = isDefined(r.out_tier) ? "" + r.out_tier : "";
    S.stemsFor = S.job;
    S.stemJob = S.job;
    S.conf = {};
    S.confText = "";
}

// paths for a tile: the conformed copy when MATCH DAW has one, else the original
inline function tilePaths(key)
{
    local out = [];
    local i = 0;
    local j = 0;
    for (i = 0; i < TILES.length; i++)
    {
        if (TILES[i][0] != key) continue;
        for (j = 0; j < TILES[i][2].length; j++)
        {
            local parts = TILES[i][2][j].split(".");
            local nm = parts[parts.length - 1];
            if (isDefined(S.conf[nm])) out.push(S.conf[nm]);
            else if (isDefined(S.orig[nm])) out.push(S.orig[nm]);
        }
    }
    return out;
}

inline function isMatched(key)
{
    local i = 0;
    local j = 0;
    for (i = 0; i < TILES.length; i++)
    {
        if (TILES[i][0] != key) continue;
        for (j = 0; j < TILES[i][2].length; j++)
        {
            local parts = TILES[i][2][j].split(".");
            if (isDefined(S.conf[parts[parts.length - 1]])) return true;
        }
    }
    return false;
}

inline function takePath(i)
{
    if (i >= S.takes.length) return "";
    local p = S.takeFiles[S.takes[i].seed];
    return isDefined(p) ? "" + p : "";
}

inline function fetchStems()
{
    S.needStems = false;
    if (S.job == "") return;
    fly("stems");
    Server.callWithGET("/stems/" + S.job, {}, function(status, response)
    {
        land();
        if (status != 200) return;
        if (response.ready == true)
        {
            applyStems(response);
            S.needConform = S.match;
        }
        else if (isDefined(response.fix_accepted) && response.fix_accepted == false)
        {
            S.msg = isDefined(response.message) ? "" + response.message : "FIX kept nothing: the source take stays.";
            S.stemsFor = S.job;
        }
        Core.repaint();
        Qa.repaint();
    });
}

inline function playPath(tag, p)
{
    if (p == "") return;
    if (S.playing == tag) { stopPlay(); Core.repaint(); return; }
    Player.setFile(p);
    S.playing = tag;
    Globals.hlPlay = true;
    Globals.hlPlayEpoch = Globals.hlPlayEpoch + 1;      // the Trigger script starts the note
    Core.repaint();
}

inline function togglePlay(key)
{
    local ps = tilePaths(key);
    if (ps.length == 0) return;
    playPath(key, ps[0]);
}

inline function toggleTake(i)
{
    playPath("take" + i, takePath(i));
}

inline function saveTile(key)
{
    local ps = tilePaths(key);
    if (ps.length == 0) return;
    local src = FileSystem.fromAbsolutePath(ps[0]);
    local base = src.toString(1);                        // file name with extension
    local start = S.saveDir != "" ? FileSystem.fromAbsolutePath(S.saveDir + "/" + base) : FileSystem.getFolder(FileSystem.Desktop).getChildFile(base);
    S.savePending = ps;                                  // nested callbacks cannot see inline locals
    FileSystem.browse(start, true, "*.wav", function(target)
    {
        if (!isDefined(target)) return;
        var ok = FileSystem.fromAbsolutePath(S.savePending[0]).copy(target);
        var dir = target.getParentDirectory();
        var n = 1;
        for (n = 1; n < S.savePending.length; n++)
        {
            var extra = FileSystem.fromAbsolutePath(S.savePending[n]);
            ok = ok && extra.copy(dir.getChildFile(extra.toString(1)));
        }
        S.saveDir = dir.toString(0);
        S.msg = ok ? "SAVED to " + S.saveDir : "SAVE FAILED";
        Core.repaint();
    });
}

// START (API.md section 11): server with no window and no Dock icon; only while /health is silent
inline function startServer()
{
    if (S.starting || S.online) return;
    S.starting = true;
    S.startAt = S.tick;
    HlTask.runProcess("/usr/bin/open", ["-g", "-j", "-a", HOOKLAB_APP, "--args", "--background"], function(task, finished, data) {});
    Core.repaint();
}

// host tempo (and the plugin's key) to /project/ so conform has a target without the Live bridge:
// only when the tempo or the key really changed
inline function projectPostDue()
{
    local bpm = Engine.getHostBpm();
    if (!S.online || !Engine.isPlugin() || bpm <= 0 || S.projSrc == "live_bridge") return false;
    return Math.abs(bpm - S.posted) >= 0.01 || projectKeyText() != S.postedKey;
}

inline function projectKeyText()
{
    return PTR.KeyKnob[1][Math.round(KeyKnob.getValue())] + " " + PTR.ScaleKnob[1][Math.round(ScaleKnob.getValue())];
}

inline function postProject()
{
    local bpm = Engine.getHostBpm();
    S.posted = bpm;
    S.postedKey = projectKeyText();
    fly("post");
    S.postBody = {"bpm": bpm, "label": "hook lab plugin"};
    local pk = PTR.KeyKnob[1][Math.round(KeyKnob.getValue())];
    local pm = PTR.ScaleKnob[1][Math.round(ScaleKnob.getValue())];
    if (pk != "-" && (pm == "major" || pm == "minor")) { S.postBody.key = pk; S.postBody.mode = pm; }
    Server.callWithPOST("/project/", JSON.stringify(S.postBody), function(status, response) { land(); });
}

// MATCH DAW: stretch and transpose every stem to the project, never blocking (wait: false)
inline function conformAll()
{
    S.needConform = false;
    if (S.stemJob == "" || S.conformId != "") return;
    if (S.projSrc == "none" || S.projBpm <= 0) { S.confText = "MATCH DAW: no project tempo yet (Live bridge or host)"; Core.repaint(); return; }
    S.confText = "MATCHING TO " + Math.round(S.projBpm) + " BPM" + (S.projKeySet ? " " + S.projKey + " " + S.projMode : "") + " ...";
    S.confFor = S.stemJob;
    fly("conform");
    Server.callWithPOST("/conform/", JSON.stringify({"job": S.stemJob, "stem": "all", "target": "project", "wait": false}), function(status, response)
    {
        land();
        if (status == 200 && isDefined(response.id)) S.conformId = "" + response.id;
        else S.confText = "MATCH failed: " + (isDefined(response) && isDefined(response.error) ? response.error : status);
        Core.repaint();
    });
}

inline function applyConform(c)
{
    local i = 0;
    local j = 0;
    S.conf = {};
    for (i = 0; i < TILES.length; i++)
    {
        for (j = 0; j < TILES[i][2].length; j++)
        {
            local parts = TILES[i][2][j].split(".");
            local nm = parts[parts.length - 1];
            if (isDefined(c.paths) && isDefined(c.paths[nm])) S.conf[nm] = "" + c.paths[nm];
            else if (isDefined(c.stems) && isDefined(c.stems[nm]) && isDefined(c.stems[nm].path)) S.conf[nm] = "" + c.stems[nm].path;
        }
    }
    S.confText = "MATCHED " + Math.round(S.projBpm) + " BPM" + (S.projKeySet ? " " + S.projKey + " " + S.projMode : "") + ": drag gives the matched copy";
}

inline function applyStatus(s)
{
    S.jstate = "" + s.state;
    S.lcd = isDefined(s.lcd) ? "" + s.lcd : S.jstate.toUpperCase();
    S.stage = isDefined(s.stage) ? "" + s.stage : "";
    S.pct = isDefined(s.pct) ? s.pct : 0;
    S.kind = isDefined(s.kind) ? "" + s.kind : S.kind;
    if (isDefined(s.preset)) S.preset = "" + s.preset;
    if (isDefined(s.error)) S.msg = "" + s.error;
    else if (isDefined(s.message)) S.msg = "" + s.message;
    // a FIX LINE job that kept nothing reports qa {best_seed: null, fix_accepted: false}: keep the source take's table
    if (isDefined(s.qa) && !(isDefined(s.qa.fix_accepted) && s.qa.fix_accepted == false)) applyQa(s.qa);
    if (isDefined(s.timings) && isDefined(s.timings.engine_load_s)) S.timing = "ENGINE LOAD " + Math.round(s.timings.engine_load_s) + " S";
    if (isDefined(s.started) && isDefined(s.finished)) S.timing = S.timing + "  JOB " + Math.round(s.finished - s.started) + " S";
    if (S.jstate == "done" && S.stemsFor != S.job) S.needStems = true;     // fetched by the clock
}

inline function pollHealth()
{
    fly("health");
    Server.callWithGET("/health", {}, function(status, h)
    {
        land();
        var on = status == 200 && isDefined(h.ok) && h.ok == true;
        var warm = on && isDefined(h.engine) && isDefined(h.engine.warm) && h.engine.warm == true;
        if (on && isDefined(h.memory) && isDefined(h.gate))
            S.gateText = "MEMORY " + Engine.doubleToString(h.memory.available_gb, 1) + " GB free. The gate waits for " + h.gate.cold_gb + " GB to load the engine (" + h.gate.wait_s + " s at most); close heavy apps if a job sits in MEM WAIT.";
        if (on != S.online || warm != S.warm)
        {
            var first = on && !S.online;
            S.online = on;
            S.warm = warm;
            if (on) S.starting = false;
            if (!on && !jobBusy()) S.lcd = "OFFLINE";
            if (on && (S.lcd == "OFFLINE" || S.lcd == "READY")) S.lcd = "READY";
            if (first) S.needGenres = true;
            Core.repaint();
        }
    });
}

inline function pollProject()
{
    fly("project");
    Server.callWithGET("/project/", {}, function(status, p)
    {
        land();
        if (status != 200) return;
        var src = isDefined(p.source) ? "" + p.source : "none";
        var ks = isDefined(p.key_set) && p.key_set == true;
        var bpm = isDefined(p.bpm) ? p.bpm : 0;
        var chg = src != S.projSrc || bpm != S.projBpm || ks != S.projKeySet;
        S.projSrc = src;
        S.projBpm = bpm;
        S.projKeySet = ks;
        S.projKey = isDefined(p.key) ? "" + p.key : "";
        S.projMode = isDefined(p.mode) ? "" + p.mode : "";
        if (S.syncLive && ks)
        {
            var ki = KEYS.indexOf(S.projKey.toUpperCase());
            if (ki >= 0 && Math.round(KeyKnob.getValue()) != ki + 1) { KeyKnob.setValue(ki + 1); chg = true; }
            var mi = S.projMode == "minor" ? 2 : 1;
            if (Math.round(ScaleKnob.getValue()) != mi) { ScaleKnob.setValue(mi); chg = true; }
        }
        if (chg) Core.repaint();
    });
}

inline function pollStatus()
{
    fly("status");
    Server.callWithGET("/status/" + S.job, {}, function(status, s)
    {
        land();
        if (status != 200) return;
        applyStatus(s);
        Core.repaint();
        if (S.expanded) Qa.repaint();
    });
}

inline function pollConform()
{
    fly("conformpoll");
    Server.callWithGET("/conform/" + S.conformId, {}, function(status, c)
    {
        land();
        if (status == 200 && isDefined(c.state) && c.state == "running") return;
        S.conformId = "";
        if (status == 200 && isDefined(c.state) && c.state == "done" && S.confFor == S.stemJob) applyConform(c);
        else S.confText = "MATCH failed: " + (isDefined(c) && isDefined(c.error) ? c.error : status);
        Core.repaint();
    });
}

// one request per tick at most, and only when none is in flight. Order: the user's action, the
// follow-ups callbacks asked for, then a 2 s cycle: health, status, project (or a post), status
const var Clock = Engine.createTimerObject();
Clock.setTimerCallback(function()
{
    S.tick = S.tick + 1;
    if (S.starting || engineText() == "MEM WAIT") Core.repaint();     // blink the engine lamp
    if (S.starting && S.tick - S.startAt > 60) { S.starting = false; S.msg = "Hook Lab did not answer in 30 s. Is Hook Lab.app in Sweet Melody Vocal?"; Core.repaint(); }
    if (!gateFree()) return;
    var ph = S.tick % 4;
    if (S.act != "" && S.online) doAct();
    else if (S.needStems && S.online) fetchStems();
    else if (S.needConform && S.online) conformAll();
    else if (S.needGenres && S.online) loadGenres();
    else if (ph == 0) pollHealth();
    else if (!S.online) return;
    else if (ph == 2) { if (projectPostDue()) postProject(); else pollProject(); }
    else if (jobBusy()) pollStatus();
    else if (S.conformId != "") pollConform();
});
Clock.startTimer(500);

inline function loadGenres()
{
    S.needGenres = false;
    fly("genres");
    Server.callWithGET("/genres/", {}, function(status, response)
    {
        land();
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
            var keep = ("" + GenreSel.getValue()).split("|");
            GENRES = fams;
            S.genresFromServer = true;
            FamilyKnob.set("max", fams.length - 1);
            if (keep.length != 2 || !selectGenreById(keep[0], keep[1]))
            {
                var dft = response["default"];          // `default` is a keyword: no dot access
                selectGenreById(isDefined(dft) ? "" + dft.family : fams[0].id, isDefined(dft) ? "" + dft.genre : "");
            }
            Core.repaint();
        }
    });
}

// ============================================================================
// STARTUP + SELF-TEST
// ============================================================================
selectGenreById("reggaeton", "reggaeton");

inline function selfTest()
{
    local ok = true;
    local i = 0;
    Lyrics.set("text", "[Chorus]\nDime si tu me quieres (dime)\n[en] say it one more time");
    local j = buildJob();
    if (j.lines.length != 3 || j.lines[2].lang != "en" || j.lines[0] != "[Chorus]") { ok = false; Console.print("HL selftest lyric lines"); }
    if (isDefined(j.key) || isDefined(j.scale) || isDefined(j.bars) || isDefined(j.bpm) || isDefined(j.engine) || j.n_seeds != 4 || j.family != "reggaeton" || j.genre != "reggaeton") { ok = false; Console.print("HL selftest job defaults leave key / scale / bars / bpm to the preset"); }
    KeyKnob.setValue(10);
    ScaleKnob.setValue(3);
    BarsKnob.setValue(4);
    j = buildJob();
    if (j.key != "A" || j.scale != "harmonic_minor" || j.bars != 16) { ok = false; Console.print("HL selftest user key / scale / bars"); }
    KeyKnob.setValue(0);
    ScaleKnob.setValue(0);
    BarsKnob.setValue(0);
    j = buildJob();
    if (isDefined(j.stack) || isDefined(j.fx) || isDefined(j.chain) || isDefined(j.voice) || j.out_tier != "ref" || j.tighten_ms != 0 || isDefined(j.dcw)) { ok = false; Console.print("HL selftest presets keep their values"); }
    RMC.stack.setValue(1);
    RMC.mix.setValue(1);
    RMC.perf.setValue(1);
    RBC.ArcBtn.setValue(1);
    j = buildJob();
    if (j.stack.dbl != 2 || j.stack.harm != "3rd" || j.stack.dbl_src != "varispeed" || j.fx.sat_mix != 0.06 || j.hall_mix != 0.2 || j.arc != true || j.comp_x2 != true) { ok = false; Console.print("HL selftest MANUAL racks " + JSON.stringify(j)); }
    RMC.stack.setValue(0);
    RMC.mix.setValue(0);
    RMC.perf.setValue(0);
    RBC.ArcBtn.setValue(0);
    SeedsKnob.setValue(8);
    if (buildJob().n_seeds != 4) { ok = false; Console.print("HL selftest seed cap"); }
    selectGenreById("rnb_soul", "soul_night");
    if (curGenre()[0] != "soul_night" || buildJob().n_seeds != 8 || GenSelOk() != "rnb_soul|soul_night") { ok = false; Console.print("HL selftest R&B seeds / genre by id"); }
    SeedsKnob.setValue(4);
    selectGenreById("reggaeton", "reggaeton");
    // a done job: /status/ qa and /stems/ shapes from API.md sections 3 and 7
    applyQa({"best_seed": 203, "ler": 0.18, "worst_line_ler": 0.4, "E": 0.6, "stem_export_ok": false,
             "lines": [{"typed": "a", "heard": "a", "ler": 0.0, "fix": false}, {"typed": "b", "heard": "be", "ler": 0.4, "fix": true}],
             "seeds": [{"seed": 202, "name": "seed202", "ler": 0.3}, {"seed": 203, "name": "seed203", "ler": 0.18}]});
    S.job = "testjob";
    applyStems({"ready": true, "folder": "/tmp/x", "files": {"lead": "/tmp/x/lead.wav", "lead_dry": "/tmp/x/lead_dry.wav", "sketch_instrumental": "/tmp/x/bed.wav"},
                "stems": {"dbl_L": "/tmp/x/dbl_L.wav", "dbl_R": "/tmp/x/dbl_R.wav", "vocal_bus": "/tmp/x/vocal_bus.wav"},
                "takes": {"202": "/tmp/x/takes/seed202_dry.wav", "203": "/tmp/x/takes/seed203_dry.wav"}, "stem_export_ok": false});
    if (S.takes[0].seed != "203" || !S.takes[0].kept || !S.lines[1].fix || S.exportOk) { ok = false; Console.print("HL selftest qa"); }
    if (tilePaths("dbl").length != 2 || tilePaths("lead")[0] != "/tmp/x/lead.wav" || tilePaths("harm").length != 0 || takePath(0) != "/tmp/x/takes/seed203_dry.wav") { ok = false; Console.print("HL selftest tiles"); }
    applyConform({"paths": {"lead": "/tmp/x/lead_128bpm_Dm.wav"}});
    if (tilePaths("lead")[0] != "/tmp/x/lead_128bpm_Dm.wav" || !isMatched("lead") || isMatched("dbl")) { ok = false; Console.print("HL selftest conform paths"); }
    applyStatus({"state": "running", "stage": "memory", "pct": 1, "lcd": "MEM WAIT 1%", "message": "waiting for memory: close heavy apps"});
    S.online = true;
    if (S.lcd != "MEM WAIT 1%" || engineText() != "MEM WAIT" || S.msg.indexOf("heavy apps") < 0) { ok = false; Console.print("HL selftest MEM WAIT"); }
    // request gate: one call at a time, follow-ups queued, never sent from a callback
    S.job = "gatejob";
    S.stemsFor = "";
    applyStatus({"state": "done", "lcd": "DONE"});
    fly("status");
    if (gateFree() || !S.needStems) { ok = false; Console.print("HL selftest gate fly / needStems"); }
    land();
    if (!gateFree()) { ok = false; Console.print("HL selftest gate land"); }
    S.tick = S.tick + 100;
    fly("health");
    S.tick = S.tick + 31;
    if (!gateFree()) { ok = false; Console.print("HL selftest gate stale guard"); }
    land();
    S.needStems = false;
    S.online = false;
    clearResults();
    S.job = "";
    S.jstate = "";
    S.lcd = "OFFLINE";
    S.msg = "";
    if (hitCore(310, 20) != "start" || hitCore(620, 160) != "match" || hitQa(540, 62) != "" || hitQa(300, 210) != "release") { ok = false; Console.print("HL selftest hits"); }
    local allc = Content.getAllComponents(".*");
    for (i = 0; i < allc.length; i++)
    {
        local c = allc[i];
        local par = c.get("parentComponent");
        local pw = FW;
        local ph = FH;
        if (par == "Core") { pw = 744; ph = 450; }
        else if (par == "Racks") { pw = 404; ph = 444; }
        else if (par == "Lower") { pw = 564; ph = 312; }
        if (c.get("x") + c.get("width") > pw || c.get("y") + c.get("height") > ph) { ok = false; Console.print("HL selftest outside: " + c.getId()); }
    }
    if (Core.get("x") + Core.get("width") > CW || Core.get("y") + Core.get("height") > CH) { ok = false; Console.print("HL selftest core outside compact"); }
    if (!isDefined(Player)) ok = false;
    Lyrics.set("text", "");
    local ng = 0;
    for (i = 0; i < GENRES.length; i++) ng = ng + GENRES[i].genres.length;
    Console.print(ok ? "HL selftest PASS families=" + GENRES.length + " genres=" + ng : "HL selftest FAIL");
}

inline function GenSelOk()
{
    return "" + GenreSel.getValue();
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
