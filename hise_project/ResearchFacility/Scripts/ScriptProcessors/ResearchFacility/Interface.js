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
AIBtn.setMouseCallback(function(event)
{
    this.data.hover = event.hover;
    if (event.clicked)
    {
        // "Surprise me" — load a random preset from the full catalog
        if (catalog.length > 0)
        {
            var randIdx = Math.floor(Math.random() * catalog.length);
            var preset = catalog[randIdx];
            loadPresetById(preset.samplemap);
            // Switch catalog UI to that preset's category + clear filters
            var cp = Content.getComponent("CatalogPanel");
            for (k = 0; k < cp.data.categories.length; k++)
            {
                if (cp.data.categories[k] == preset.category)
                {
                    cp.data.activeCategory = k;
                    cp.data.activeMoods = [];
                    // Find the card index of the random preset in its category
                    var visibleList = getVisiblePresets(cp);
                    for (kk = 0; kk < visibleList.length; kk++)
                    {
                        if (visibleList[kk].samplemap == preset.samplemap)
                        {
                            cp.data.activeCardIndex = kk;
                            break;
                        }
                    }
                    break;
                }
            }
            cp.repaint();
        }
    }
    this.repaint();
});

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
// CATALOG SECTION — real preset browser wired to the sampler
// ============================================================================

// Reference to the sampler we'll swap maps on
const var VoiceA = Synth.getChildSynth("Voice A");

// Load the catalog JSON shipped with the plugin (Samples/_catalog.json)
const var catalogFile = FileSystem.getFolder(FileSystem.Samples).getChildFile("_catalog.json");
reg catalog;
if (catalogFile.isFile())
{
    catalog = catalogFile.loadAsObject();
}
else
{
    catalog = [];
}

// Card click handler — swap the sample on the Voice A sampler
inline function loadPresetById(presetId)
{
    if (VoiceA != undefined)
        VoiceA.asSampler().loadSampleMap(presetId);
}

const var CatalogPanel = Content.addPanel("CatalogPanel", 160, 116);
Content.setPropertiesFromJSON("CatalogPanel", {
    "width": 844, "height": 504,
    "allowCallbacks": "Clicks & Hover"
});

CatalogPanel.data.categories = ["pads", "plucks", "basses", "leads", "textures"];
CatalogPanel.data.moodChips = ["calm", "warm", "dark", "bright", "aggressive", "melancholy", "hopeful", "ethereal"];
CatalogPanel.data.activeCategory = 0;
CatalogPanel.data.activeMoods = [];  // selected moods (intersection filter)
CatalogPanel.data.hoverCategoryIndex = -1;
CatalogPanel.data.hoverMoodIndex = -1;
CatalogPanel.data.hoverCardIndex = -1;
CatalogPanel.data.activeCardIndex = 0;
CatalogPanel.data.cardW = 156;
CatalogPanel.data.cardH = 96;
CatalogPanel.data.cardGap = 16;
CatalogPanel.data.cardsPerRow = 5;
CatalogPanel.data.tabsY = 42;
CatalogPanel.data.moodChipsY = 70;
CatalogPanel.data.gridTopOffset = 110;

// Helper — get presets filtered by current category AND active moods
inline function getVisiblePresets(panel)
{
    local cat = panel.data.categories[panel.data.activeCategory];
    local moods = panel.data.activeMoods;
    local out = [];
    for (i = 0; i < catalog.length; i++)
    {
        local p = catalog[i];
        if (p.category != cat) continue;
        if (moods.length > 0)
        {
            // Must match ALL active moods (AND filter)
            local pmoods = p.mood;
            if (pmoods == undefined) continue;
            local allMatch = true;
            for (m = 0; m < moods.length; m++)
            {
                local found = false;
                for (k = 0; k < pmoods.length; k++)
                {
                    if (pmoods[k] == moods[m]) { found = true; break; }
                }
                if (!found) { allMatch = false; break; }
            }
            if (!allMatch) continue;
        }
        out.push(p);
    }
    return out;
}

// Helper — count how many presets in category have a given mood (for chip badges)
inline function countMoodInCategory(panel, mood)
{
    local cat = panel.data.categories[panel.data.activeCategory];
    local cnt = 0;
    for (i = 0; i < catalog.length; i++)
    {
        local p = catalog[i];
        if (p.category != cat) continue;
        if (p.mood == undefined) continue;
        for (k = 0; k < p.mood.length; k++)
        {
            if (p.mood[k] == mood) { cnt = cnt + 1; break; }
        }
    }
    return cnt;
}

// Helper — is a mood currently active?
inline function isMoodActive(panel, mood)
{
    for (i = 0; i < panel.data.activeMoods.length; i++)
    {
        if (panel.data.activeMoods[i] == mood) return true;
    }
    return false;
}

CatalogPanel.setPaintRoutine(function(g)
{
    var visiblePresets = getVisiblePresets(this);

    g.setColour(0xFF8B8F96);
    g.setFont("Oxygen Bold", 11);
    g.drawAlignedText("CATALOG", [0, 0, 200, 14], "left");

    g.setColour(0xFFE8EAED);
    g.setFont("Oxygen", 11);
    g.drawAlignedText("Showing " + visiblePresets.length + " of " + catalog.length + " sounds. Click a card to load.",
                      [0, 18, 600, 14], "left");

    // Category tabs
    var tabY = this.data.tabsY;
    var tabX = 0;
    for (i = 0; i < this.data.categories.length; i++)
    {
        var label = this.data.categories[i].toUpperCase();
        var tabW = 110;

        if (i == this.data.activeCategory)
        {
            g.setColour(0xFF00D9A0);
            g.fillRect([tabX, tabY + 18, tabW - 8, 2]);
            g.setColour(0xFFE8EAED);
        }
        else if (i == this.data.hoverCategoryIndex)
        {
            g.setColour(0xFFE8EAED);
        }
        else
        {
            g.setColour(0xFF8B8F96);
        }
        g.setFont("Oxygen Bold", 11);
        g.drawAlignedText(label, [tabX, tabY, tabW - 8, 16], "left");
        tabX += tabW;
    }

    // Mood filter chips (toggle-able)
    var chipY = this.data.moodChipsY;
    var chipX = 0;
    var chipPadX = 12;
    var chipH = 22;
    g.setFont("Oxygen", 10);
    for (i = 0; i < this.data.moodChips.length; i++)
    {
        var mood = this.data.moodChips[i];
        var cnt = countMoodInCategory(this, mood);
        if (cnt == 0) continue;  // skip moods with zero matches in current category
        var label = mood + " (" + cnt + ")";
        var chipW = label.length * 6 + chipPadX * 2;
        var active = isMoodActive(this, mood);
        var hover = (i == this.data.hoverMoodIndex);

        if (active)
        {
            g.setColour(0xFF00D9A0);
            g.fillRoundedRectangle([chipX, chipY, chipW, chipH], chipH / 2);
            g.setColour(0xFF0A0B0D);
        }
        else
        {
            g.setColour(hover ? 0xFF2A2E36 : 0xFF1D2026);
            g.fillRoundedRectangle([chipX, chipY, chipW, chipH], chipH / 2);
            g.setColour(0xFF2A2E36);
            g.drawRoundedRectangle([chipX + 0.5, chipY + 0.5, chipW - 1, chipH - 1], chipH / 2, 1);
            g.setColour(hover ? 0xFFE8EAED : 0xFF8B8F96);
        }
        g.drawAlignedText(label, [chipX + chipPadX, chipY + 2, chipW - chipPadX * 2, chipH - 4], "left");
        chipX += chipW + 8;
    }
    // Clear filters button if any active
    if (this.data.activeMoods.length > 0)
    {
        var clearLabel = "× clear";
        var clearW = clearLabel.length * 6 + chipPadX * 2;
        g.setColour(0xFF1D2026);
        g.fillRoundedRectangle([chipX, chipY, clearW, chipH], chipH / 2);
        g.setColour(0xFFFF8A4C);
        g.drawAlignedText(clearLabel, [chipX + chipPadX, chipY + 2, clearW - chipPadX * 2, chipH - 4], "left");
    }

    // Grid of preset cards
    var presets = getVisiblePresets(this);
    var cardW = this.data.cardW;
    var cardH = this.data.cardH;
    var gap = this.data.cardGap;
    var perRow = this.data.cardsPerRow;
    var topY = this.data.gridTopOffset;

    for (i = 0; i < presets.length; i++)
    {
        var col = i % perRow;
        var row = Math.floor(i / perRow);
        var x = col * (cardW + gap);
        var y = topY + row * (cardH + gap);
        var p = presets[i];

        var isHover = (i == this.data.hoverCardIndex);
        var isActive = (i == this.data.activeCardIndex);

        // Card background
        if (isActive)
            g.setColour(0xFF1D2026);
        else if (isHover)
            g.setColour(0xFF1A1D22);
        else
            g.setColour(0xFF14161A);
        g.fillRoundedRectangle([x, y, cardW, cardH], 6);

        // Card border (active = accent)
        if (isActive)
            g.setColour(0xFF00D9A0);
        else
            g.setColour(0xFF2A2E36);
        g.drawRoundedRectangle([x + 0.5, y + 0.5, cardW - 1, cardH - 1], 6, isActive ? 2 : 1);

        // Name
        g.setColour(0xFFE8EAED);
        g.setFont("Oxygen Bold", 13);
        g.drawAlignedText(p.name, [x + 12, y + 12, cardW - 24, 18], "left");

        // Tag chip (first 2 tags)
        var tagStr = "";
        if (p.tags != undefined && p.tags.length > 0)
        {
            tagStr = p.tags[0];
            if (p.tags.length > 1) tagStr = tagStr + " · " + p.tags[1];
        }
        g.setColour(0xFF00D9A0);
        g.setFont("Oxygen", 9);
        g.drawAlignedText(tagStr, [x + 12, y + 34, cardW - 24, 12], "left");

        // Category badge
        g.setColour(0xFF8B8F96);
        g.setFont("Oxygen", 9);
        g.drawAlignedText(p.category, [x + 12, y + cardH - 18, cardW - 24, 12], "left");

        // Active indicator dot
        if (isActive)
        {
            g.setColour(0xFF00D9A0);
            g.fillEllipse([x + cardW - 18, y + 12, 6, 6]);
        }
    }
});

// Compute mood chip hit-box (must match paint routine)
inline function moodChipAt(panel, x, y)
{
    if (y < panel.data.moodChipsY || y > panel.data.moodChipsY + 22) return -1;
    local cx = 0;
    local chipPadX = 12;
    for (i = 0; i < panel.data.moodChips.length; i++)
    {
        local mood = panel.data.moodChips[i];
        local cnt = countMoodInCategory(panel, mood);
        if (cnt == 0) continue;
        local label = mood + " (" + cnt + ")";
        local chipW = label.length * 6 + chipPadX * 2;
        if (x >= cx && x < cx + chipW) return i;
        cx = cx + chipW + 8;
    }
    // Clear-filters button area
    if (panel.data.activeMoods.length > 0)
    {
        local clearW = 60;
        if (x >= cx && x < cx + clearW) return -2;  // -2 = clear
    }
    return -1;
}

CatalogPanel.setMouseCallback(function(event)
{
    var prevHoverCat = this.data.hoverCategoryIndex;
    var prevHoverMood = this.data.hoverMoodIndex;
    var prevHoverCard = this.data.hoverCardIndex;
    this.data.hoverCategoryIndex = -1;
    this.data.hoverMoodIndex = -1;
    this.data.hoverCardIndex = -1;

    if (event.hover)
    {
        // Tab hover (Y 42-62)
        if (event.y >= this.data.tabsY && event.y < this.data.tabsY + 20)
        {
            var col = Math.floor(event.x / 110);
            if (col >= 0 && col < this.data.categories.length)
                this.data.hoverCategoryIndex = col;
        }
        // Mood chip hover
        else if (event.y >= this.data.moodChipsY && event.y < this.data.moodChipsY + 22)
        {
            var moodIdx = moodChipAt(this, event.x, event.y);
            if (moodIdx >= 0) this.data.hoverMoodIndex = moodIdx;
        }
        // Card hover
        else if (event.y >= this.data.gridTopOffset)
        {
            var cardW = this.data.cardW;
            var cardH = this.data.cardH;
            var gap = this.data.cardGap;
            var topY = this.data.gridTopOffset;
            var col2 = Math.floor(event.x / (cardW + gap));
            var row = Math.floor((event.y - topY) / (cardH + gap));
            if (col2 >= 0 && col2 < this.data.cardsPerRow && row >= 0)
            {
                var idx = row * this.data.cardsPerRow + col2;
                var presets = getVisiblePresets(this);
                if (idx < presets.length) this.data.hoverCardIndex = idx;
            }
        }
    }

    if (event.clicked)
    {
        // Category tab click
        if (this.data.hoverCategoryIndex >= 0)
        {
            this.data.activeCategory = this.data.hoverCategoryIndex;
            this.data.activeCardIndex = 0;
            this.data.activeMoods = [];  // clear mood filters when switching category
            this.repaint();
            return;
        }
        // Mood chip click → toggle
        if (event.y >= this.data.moodChipsY && event.y < this.data.moodChipsY + 22)
        {
            var moodIdx2 = moodChipAt(this, event.x, event.y);
            if (moodIdx2 == -2)
            {
                this.data.activeMoods = [];  // clear all
                this.repaint();
                return;
            }
            if (moodIdx2 >= 0)
            {
                var mood = this.data.moodChips[moodIdx2];
                var newMoods = [];
                var wasActive = false;
                for (m = 0; m < this.data.activeMoods.length; m++)
                {
                    if (this.data.activeMoods[m] == mood) { wasActive = true; }
                    else newMoods.push(this.data.activeMoods[m]);
                }
                if (!wasActive) newMoods.push(mood);
                this.data.activeMoods = newMoods;
                this.data.activeCardIndex = 0;
                this.repaint();
                return;
            }
        }
        // Card click → load
        if (this.data.hoverCardIndex >= 0)
        {
            this.data.activeCardIndex = this.data.hoverCardIndex;
            var presetsList = getVisiblePresets(this);
            var preset = presetsList[this.data.hoverCardIndex];
            if (preset != undefined)
                loadPresetById(preset.samplemap);
            this.repaint();
            return;
        }
    }

    if (prevHoverCat != this.data.hoverCategoryIndex ||
        prevHoverMood != this.data.hoverMoodIndex ||
        prevHoverCard != this.data.hoverCardIndex)
        this.repaint();
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
