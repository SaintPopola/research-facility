/* ============================================================================
   Research Facility — Interface
   Phase 1: branded shell + Lab section with 6 working macro knobs +
   Catalog placeholder grid + Studio FX rack visualization.
   See ~/Desktop/ResearchFacility/docs/07_ui_design_concept.md.
   ============================================================================ */

Content.makeFrontInterface(1024, 700);

// ============================================================================
// TOP BAR
// ============================================================================

const var TopBar = Content.addPanel("TopBar", 0, 0);
Content.setPropertiesFromJSON("TopBar", { "width": 1024, "height": 56 });
TopBar.setPaintRoutine(function(g)
{
    g.fillAll(0xFF0A0B0D);
    g.setColour(0xFF2A2E36);
    g.fillRect([0, 55, 1024, 1]);

    g.setColour(0xFF00D9A0);
    g.setFont("Oxygen Bold", 22);
    g.drawAlignedText("RF", [20, 14, 40, 28], "centred");

    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen Bold", 13);
    g.drawAlignedText("RESEARCH  FACILITY", [72, 16, 240, 20], "left");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("v0.1 · scaffold", [72, 34, 240, 14], "left");
});

const var SearchBar = Content.addPanel("SearchBar", 320, 12);
Content.setPropertiesFromJSON("SearchBar", { "width": 540, "height": 32, "allowCallbacks": "Clicks & Hover" });
SearchBar.setPaintRoutine(function(g)
{
    g.setColour(this.data.hover ? 0xFF1D2026 : 0xFF14161A);
    g.fillRoundedRectangle([0, 0, 540, 32], 6);
    g.setColour(0xFF2A2E36);
    g.drawRoundedRectangle([0.5, 0.5, 539, 31], 6, 1);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 13);
    g.drawAlignedText("What are you researching?", [16, 0, 500, 32], "left");
    g.setColour(0xFF00D9A0);
    g.setFont("Oxygen Bold", 14);
    g.drawAlignedText("Q", [510, 0, 20, 32], "centred");
});
SearchBar.setMouseCallback(function(event) { this.data.hover = event.hover; this.repaint(); });

const var AIBtn = Content.addPanel("AIBtn", 880, 12);
Content.setPropertiesFromJSON("AIBtn", { "width": 76, "height": 32, "allowCallbacks": "Clicks & Hover" });
AIBtn.setPaintRoutine(function(g)
{
    g.setColour(this.data.hover ? 0xFF1AEBB2 : 0xFF00D9A0);
    g.fillRoundedRectangle([0, 0, 76, 32], 6);
    g.setColour(0xFF0A0B0D);
    g.setFont("Oxygen Bold", 12);
    g.drawAlignedText("AI  ASK", [0, 0, 76, 32], "centred");
});
AIBtn.setMouseCallback(function(event) { this.data.hover = event.hover; this.repaint(); });

// ============================================================================
// LEFT RAIL
// ============================================================================

const var Rail = Content.addPanel("Rail", 0, 56);
Content.setPropertiesFromJSON("Rail", { "width": 140, "height": 584, "allowCallbacks": "Clicks & Hover" });

Rail.data.sections = ["CATALOG", "LAB", "FIELD", "STUDIO"];
Rail.data.activeIndex = 1; // Default to LAB so user immediately sees knobs
Rail.data.hoverIndex = -1;

Rail.setPaintRoutine(function(g)
{
    g.fillAll(0xFF0A0B0D);
    g.setColour(0xFF2A2E36);
    g.fillRect([139, 0, 1, 584]);

    for (i = 0; i < this.data.sections.length; i++)
    {
        var y = 28 + i * 44;
        if (i == this.data.activeIndex)
        {
            g.setColour(0xFF00D9A0);
            g.fillRect([0, y - 4, 3, 30]);
            g.setColour(0xFFE8EAED);
        }
        else if (i == this.data.hoverIndex)
        {
            g.setColour(0xFFE8EAED);
        }
        else
        {
            g.setColour(0xFF8B8F96);
        }
        g.setFont("Oxygen Bold", 12);
        g.drawAlignedText(this.data.sections[i], [24, y, 100, 22], "left");
    }

    g.setColour(0xFF2A2E36);
    g.fillRect([16, 224, 100, 1]);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Favorites", [24, 244, 100, 18], "left");
    g.drawAlignedText("Recent",    [24, 268, 100, 18], "left");
    g.drawAlignedText("History",   [24, 292, 100, 18], "left");

    g.setColour(0xFF2A2E36);
    g.fillRect([16, 520, 100, 1]);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("Phase 1",   [24, 532, 100, 14], "left");
    g.drawAlignedText("Playable",  [24, 548, 100, 14], "left");
});

// ============================================================================
// MAIN PANE — background that the section panels draw on top of
// ============================================================================

const var Main = Content.addPanel("Main", 140, 56);
Content.setPropertiesFromJSON("Main", { "width": 884, "height": 584 });
Main.setPaintRoutine(function(g)
{
    g.fillAll(0xFF14161A);

    var rail = Content.getComponent("Rail");
    var section = rail.data.activeIndex;
    var sectionName = rail.data.sections[section];

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("SECTION", [24, 16, 200, 14], "left");

    g.setColour(0xFF00D9A0);
    g.setFont("Oxygen Bold", 13);
    g.drawAlignedText(sectionName, [24, 32, 200, 18], "left");
});

// ============================================================================
// CATALOG SECTION — placeholder preset grid
// ============================================================================

const var CatalogPanel = Content.addPanel("CatalogPanel", 160, 116);
Content.setPropertiesFromJSON("CatalogPanel", { "width": 844, "height": 504 });

CatalogPanel.data.presets = [
    "Vellum|pad·dark|80 bpm",
    "Slow Dawn|pad·warm|76 bpm",
    "Vox Drift|texture·dark|82 bpm",
    "Choir Ghost|pad·vocal|85 bpm",
    "Owl Hymn|pad·warm|72 bpm",
    "Mist|texture·cold|78 bpm",
    "Old Tape|pad·vox|94 bpm",
    "Solar Drift|pad·bright|88 bpm",
    "Velvet|pad·warm|70 bpm"
];

CatalogPanel.setPaintRoutine(function(g)
{
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("TOP RESULTS",  [0, 0, 200, 14], "left");

    var cardW = 250;
    var cardH = 110;
    var gap = 18;
    var perRow = 3;

    for (i = 0; i < this.data.presets.length; i++)
    {
        var col = i % perRow;
        var row = Math.floor(i / perRow);
        var x = col * (cardW + gap);
        var y = 26 + row * (cardH + gap);

        var parts = this.data.presets[i].split("|");

        // Card background
        g.setColour(0xFF1D2026);
        g.fillRoundedRectangle([x, y, cardW, cardH], 6);
        g.setColour(0xFF2A2E36);
        g.drawRoundedRectangle([x + 0.5, y + 0.5, cardW - 1, cardH - 1], 6, 1);

        // Preset name
        g.setColour(0xFFE8EAED);
        g.setFont("Oxygen Bold", 16);
        g.drawAlignedText(parts[0], [x + 14, y + 14, cardW - 28, 22], "left");

        // Tags
        g.setColour(0xFF00D9A0);
        g.setFont("Oxygen", 10);
        g.drawAlignedText(parts[1], [x + 14, y + 38, cardW - 28, 14], "left");

        // BPM
        g.setColour(0xFF8B8F96);
        g.setFont("Oxygen", 10);
        g.drawAlignedText(parts[2], [x + 14, y + 54, cardW - 28, 14], "left");

        // Audition bar
        g.setColour(0xFF2A2E36);
        g.fillRect([x + 14, y + 80, cardW - 28, 1]);
        g.setColour(0xFF8B8F96);
        g.setFont("Oxygen", 10);
        g.drawAlignedText("hover to audition", [x + 14, y + 88, cardW - 28, 14], "left");
    }
});

// ============================================================================
// LAB SECTION — 6 working macro knobs bound to real DSP parameters
// ============================================================================

const var LabPanel = Content.addPanel("LabPanel", 160, 116);
Content.setPropertiesFromJSON("LabPanel", { "width": 844, "height": 504 });
LabPanel.setPaintRoutine(function(g)
{
    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen Bold", 18);
    g.drawAlignedText("Quick Tweak", [0, 0, 844, 24], "left");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Six macros control everything that matters. Toggle to Expert (bottom-right) for the full mod matrix.",
                      [0, 28, 844, 16], "left");

    // Section divider
    g.setColour(0xFF2A2E36);
    g.fillRect([0, 56, 844, 1]);

    // Engine info footer
    g.setColour(0xFF2A2E36);
    g.fillRect([0, 380, 844, 1]);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("SIGNAL FLOW", [0, 396, 844, 14], "left");
    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen", 12);
    g.drawAlignedText("Voice A (sine + saturation)  →  Master Filter  →  Chorus  →  Master Reverb  →  Out",
                      [0, 416, 844, 16], "left");
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("Phase 1 engine. Sampler module + multi-engine architecture lands in Phase 2.",
                      [0, 436, 844, 14], "left");
});

// Knob layout: 3 columns x 2 rows, centered in LabPanel
const var KNOB_Y1 = 200;     // absolute Y on main interface (LabPanel y=116 + offset 84)
const var KNOB_Y2 = 320;
const var KNOB_X = [240, 480, 720]; // 3 column centers

// Each knob is positioned absolutely on the interface

const var BrightnessKnob = Content.addKnob("BrightnessKnob", KNOB_X[0] - 40, KNOB_Y1 - 40);
Content.setPropertiesFromJSON("BrightnessKnob", {
    "text": "Brightness",
    "width": 80, "height": 80,
    "processorId": "Master Filter",
    "parameterId": "Frequency",
    "min": 80, "max": 20000,
    "mode": "Frequency",
    "defaultValue": 8000,
    "middlePosition": 1000,
    "stepSize": 1,
    "suffix": " Hz"
});

const var MovementKnob = Content.addKnob("MovementKnob", KNOB_X[1] - 40, KNOB_Y1 - 40);
Content.setPropertiesFromJSON("MovementKnob", {
    "text": "Movement",
    "width": 80, "height": 80,
    "processorId": "Chorus",
    "parameterId": "Rate",
    "min": 0.05, "max": 4.0,
    "defaultValue": 0.25,
    "stepSize": 0.01,
    "suffix": " Hz"
});

const var WarmthKnob = Content.addKnob("WarmthKnob", KNOB_X[2] - 40, KNOB_Y1 - 40);
Content.setPropertiesFromJSON("WarmthKnob", {
    "text": "Warmth",
    "width": 80, "height": 80,
    "processorId": "Master Filter",
    "parameterId": "Q",
    "min": 0.3, "max": 8.0,
    "defaultValue": 1.5,
    "stepSize": 0.01
});

const var WidthKnob = Content.addKnob("WidthKnob", KNOB_X[0] - 40, KNOB_Y2 - 40);
Content.setPropertiesFromJSON("WidthKnob", {
    "text": "Width",
    "width": 80, "height": 80,
    "processorId": "Chorus",
    "parameterId": "Width",
    "min": 0.0, "max": 1.0,
    "defaultValue": 0.5,
    "mode": "NormalizedPercentage",
    "stepSize": 0.01,
    "suffix": " %"
});

const var LengthKnob = Content.addKnob("LengthKnob", KNOB_X[1] - 40, KNOB_Y2 - 40);
Content.setPropertiesFromJSON("LengthKnob", {
    "text": "Length",
    "width": 80, "height": 80,
    "processorId": "Master Reverb",
    "parameterId": "WetLevel",
    "min": 0.0, "max": 1.0,
    "defaultValue": 0.25,
    "mode": "NormalizedPercentage",
    "stepSize": 0.01,
    "suffix": " %"
});

const var DriveKnob = Content.addKnob("DriveKnob", KNOB_X[2] - 40, KNOB_Y2 - 40);
Content.setPropertiesFromJSON("DriveKnob", {
    "text": "Drive",
    "width": 80, "height": 80,
    "processorId": "Voice A",
    "parameterId": "SaturationAmount",
    "min": 0.0, "max": 1.0,
    "defaultValue": 0.1,
    "mode": "NormalizedPercentage",
    "stepSize": 0.01,
    "suffix": " %"
});

// ============================================================================
// FIELD SECTION — sample import drop zone (visual stub)
// ============================================================================

const var FieldPanel = Content.addPanel("FieldPanel", 160, 116);
Content.setPropertiesFromJSON("FieldPanel", { "width": 844, "height": 504 });
FieldPanel.setPaintRoutine(function(g)
{
    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen Bold", 18);
    g.drawAlignedText("Field Recordings", [0, 0, 844, 24], "left");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Import your own samples. License-check happens on drop.",
                      [0, 28, 844, 16], "left");

    // Drop zone
    var dx = 122;
    var dy = 80;
    var dw = 600;
    var dh = 280;

    g.setColour(0xFF1D2026);
    g.fillRoundedRectangle([dx, dy, dw, dh], 12);

    // Dashed border (simulate with rect segments)
    g.setColour(0xFF2A2E36);
    for (i = 0; i < dw; i += 12)
    {
        g.fillRect([dx + i, dy, 6, 2]);
        g.fillRect([dx + i, dy + dh - 2, 6, 2]);
    }
    for (i = 0; i < dh; i += 12)
    {
        g.fillRect([dx, dy + i, 2, 6]);
        g.fillRect([dx + dw - 2, dy + i, 2, 6]);
    }

    g.setColour(0xFF00D9A0);
    g.setFont("Oxygen Bold", 28);
    g.drawAlignedText("Drop samples here", [dx, dy + 100, dw, 36], "centred");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 12);
    g.drawAlignedText("WAV  ·  AIF  ·  SFZ", [dx, dy + 144, dw, 18], "centred");
    g.drawAlignedText("(Phase 2 — currently visual only)", [dx, dy + 168, dw, 16], "centred");

    g.setColour(0xFF2A2E36);
    g.fillRect([0, 400, 844, 1]);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("LICENSE DISCIPLINE", [0, 416, 844, 14], "left");
    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Every sample carries a .meta.json sidecar (source URL + license + uploader). CI blocks merges without it.",
                      [0, 436, 844, 14], "left");
});

// ============================================================================
// STUDIO SECTION — FX rack visualization
// ============================================================================

const var StudioPanel = Content.addPanel("StudioPanel", 160, 116);
Content.setPropertiesFromJSON("StudioPanel", { "width": 844, "height": 504 });
StudioPanel.setPaintRoutine(function(g)
{
    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen Bold", 18);
    g.drawAlignedText("Studio", [0, 0, 844, 24], "left");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Global FX rack + output bus.",
                      [0, 28, 844, 16], "left");

    g.setColour(0xFF2A2E36);
    g.fillRect([0, 56, 844, 1]);

    // FX chain rack
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("FX CHAIN", [0, 76, 844, 14], "left");

    var fxList = ["FILTER", "CHORUS", "REVERB"];
    var fxColors = [0xFF1D2026, 0xFF1D2026, 0xFF1D2026];

    var slotW = 220;
    var slotH = 80;
    var gap = 18;

    for (i = 0; i < fxList.length; i++)
    {
        var x = i * (slotW + gap);
        var y = 100;

        g.setColour(fxColors[i]);
        g.fillRoundedRectangle([x, y, slotW, slotH], 6);
        g.setColour(0xFF2A2E36);
        g.drawRoundedRectangle([x + 0.5, y + 0.5, slotW - 1, slotH - 1], 6, 1);

        g.setColour(0xFFE8EAED);
        g.setFont("Oxygen Bold", 12);
        g.drawAlignedText(fxList[i], [x + 16, y + 14, slotW - 32, 16], "left");

        g.setColour(0xFF8B8F96);
        g.setFont("Oxygen", 10);
        g.drawAlignedText("ACTIVE", [x + 16, y + 34, slotW - 32, 14], "left");

        g.setColour(0xFF00D9A0);
        g.fillEllipse([x + slotW - 24, y + 16, 8, 8]);

        // Arrow to next
        if (i < fxList.length - 1)
        {
            g.setColour(0xFF8B8F96);
            var ax = x + slotW + 4;
            var ay = y + slotH / 2;
            g.setFont("Oxygen Bold", 14);
            g.drawAlignedText("→", [ax, ay - 8, 12, 16], "centred");
        }
    }

    // Add-effect slot
    var addX = 3 * (slotW + gap);
    g.setColour(0xFF14161A);
    g.fillRoundedRectangle([addX, 100, slotW, slotH], 6);
    g.setColour(0xFF2A2E36);
    g.drawRoundedRectangle([addX + 0.5, 100.5, slotW - 1, slotH - 1], 6, 1);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 12);
    g.drawAlignedText("+ add effect", [addX, 130, slotW, 16], "centred");

    // Output meter mockup
    g.setColour(0xFF2A2E36);
    g.fillRect([0, 220, 844, 1]);
    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("OUTPUT",  [0, 240, 200, 14], "left");

    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("L", [0, 270, 16, 16], "left");
    g.drawAlignedText("R", [0, 296, 16, 16], "left");

    // Meter bars (static visual)
    g.setColour(0xFF1D2026);
    g.fillRect([24, 270, 600, 14]);
    g.fillRect([24, 296, 600, 14]);
    g.setColour(0xFF00D9A0);
    g.fillRect([24, 270, 380, 14]);
    g.fillRect([24, 296, 360, 14]);

    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("-3.2 dB", [640, 270, 100, 16], "left");
    g.drawAlignedText("-4.1 dB", [640, 296, 100, 16], "left");

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("Headroom: 8.7 dB",  [0, 340, 844, 14], "left");
});

// ============================================================================
// BOTTOM BAR — Quick Tweak / Expert toggle
// ============================================================================

const var Bottom = Content.addPanel("Bottom", 0, 640);
Content.setPropertiesFromJSON("Bottom", { "width": 1024, "height": 60, "allowCallbacks": "Clicks & Hover" });

Bottom.data.expertMode = 0;

Bottom.setPaintRoutine(function(g)
{
    g.fillAll(0xFF0A0B0D);
    g.setColour(0xFF2A2E36);
    g.fillRect([0, 0, 1024, 1]);

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen", 10);
    g.drawAlignedText("Voice A active · 6-macro Quick Tweak · Phase 1",
                      [16, 22, 700, 16], "left");

    var quickColour = this.data.expertMode == 0 ? 0xFFE8EAED : 0xFF8B8F96;
    var exprColour  = this.data.expertMode == 1 ? 0xFFE8EAED : 0xFF8B8F96;

    g.setColour(quickColour);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("QUICK TWEAK", [820, 22, 100, 16], "right");

    g.setColour(0xFF1D2026);
    g.fillRoundedRectangle([930, 24, 36, 16], 8);
    g.setColour(0xFF00D9A0);
    var knobX = this.data.expertMode == 0 ? 932 : 950;
    g.fillEllipse([knobX, 26, 12, 12]);

    g.setColour(exprColour);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("EXPERT", [975, 22, 50, 16], "left");
});

Bottom.setMouseCallback(function(event)
{
    if (event.clicked && event.x >= 928 && event.x <= 970 && event.y >= 20 && event.y <= 44)
    {
        this.data.expertMode = this.data.expertMode == 0 ? 1 : 0;
        this.repaint();
    }
});

// ============================================================================
// SECTION VISIBILITY SWITCHING
// ============================================================================

inline function showSection(index)
{
    local catalog = Content.getComponent("CatalogPanel");
    local lab     = Content.getComponent("LabPanel");
    local field   = Content.getComponent("FieldPanel");
    local studio  = Content.getComponent("StudioPanel");

    catalog.set("visible", index == 0);
    lab.set("visible",     index == 1);
    field.set("visible",   index == 2);
    studio.set("visible",  index == 3);

    // Knobs only visible in Lab
    local knobs = ["BrightnessKnob", "MovementKnob", "WarmthKnob",
                   "WidthKnob", "LengthKnob", "DriveKnob"];
    for (i = 0; i < knobs.length; i++)
        Content.getComponent(knobs[i]).set("visible", index == 1);

    Content.getComponent("Main").repaint();
}

// Initialize visibility (active section = 1 = LAB)
showSection(1);

// Rail click handler updated to use showSection
Rail.setMouseCallback(function(event)
{
    var prevHover = this.data.hoverIndex;
    this.data.hoverIndex = -1;

    if (event.hover)
    {
        for (i = 0; i < this.data.sections.length; i++)
        {
            var y = 28 + i * 44;
            if (event.y >= y - 4 && event.y < y + 26)
            {
                this.data.hoverIndex = i;
                break;
            }
        }
    }

    if (event.clicked && this.data.hoverIndex >= 0)
    {
        this.data.activeIndex = this.data.hoverIndex;
        showSection(this.data.activeIndex);
        this.repaint();
    }

    if (prevHover != this.data.hoverIndex)
        this.repaint();
});

// ============================================================================
// HISE required callbacks
// ============================================================================

function onNoteOn() {}
function onNoteOff() {}
function onController() {}
function onTimer() {}
function onControl(number, value) {}
