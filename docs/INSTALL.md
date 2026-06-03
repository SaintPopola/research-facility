# Installation Guide — Research Facility dev environment

> **2026-06-03.** macOS-first guide (you're on macOS 15.1 Sequoia). Windows steps added later.

## What you already have

Verified on your machine:

- ✅ **Xcode Command Line Tools** at `/Library/Developer/CommandLineTools`
- ✅ **macOS 15.1 (Sequoia)** — supported by HISE and JUCE 8
- ✅ **VSCode** — recommended via shell `code` command (install via VSCode → Cmd+Shift+P → "Shell Command: Install 'code' command in PATH")

## What you need to install

### 1. CMake (5 min, required)

CMake is missing. JUCE and HISE both want it. Install via Homebrew:

```bash
# Check if Homebrew is installed first
which brew

# If not, install Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install CMake + Ninja (faster build system)
brew install cmake ninja
```

### 2. HISE (15 min, primary toolchain)

Download from [hise.dev](https://hise.dev/):

1. Visit hise.dev → click the macOS download link
2. Open the downloaded `.dmg`, drag HISE to Applications
3. On first launch, macOS will warn it's from an unidentified developer — Right-click → Open → Open Anyway in System Settings if needed
4. HISE opens to a welcome screen

**No license purchase needed yet.** You can develop and build under HISE's free GPL path until you're ready to ship a closed-source commercial release (which is months away). When v0.1 launches commercially, buy the Starter Pack at store.hise.dev (€200 one-time).

### 3. (Optional) JUCE 8 (10 min, backup toolchain)

Only needed if we ever migrate to Path B (Pamplejuce). For now: skip.

If you want to install it anyway as future-proofing:

```bash
cd ~/Desktop/ResearchFacility/third_party
git clone --depth 1 https://github.com/juce-framework/JUCE.git
git clone --depth 1 https://github.com/sudara/pamplejuce.git
git clone --depth 1 https://github.com/free-audio/clap-juce-extensions.git
```

### 4. (Optional) Apple Developer Program (when you're ready to ship)

$99/year. Required for:
- Code signing your plugin for distribution outside the App Store
- Notarization (Apple's malware check, otherwise users see scary warnings)
- AU plugin format requires signed builds for some host validations

Wait to buy this until you have a v0.1 ready to give to outside testers. Sign up at [developer.apple.com](https://developer.apple.com/).

### 5. (Optional) Steinberg VST3 developer license (when you're ready to ship)

Free but requires registration. You provide a unique VST3 plug-in ID. Sign up at [developer.steinberg.help/display/VST/VST+3+Developer+Portal](https://developer.steinberg.help/display/VST/VST+3+Developer+Portal). Wait until v0.1.

### 6. (Optional) Avid AAX developer account (when shipping to Pro Tools users)

Free but requires registration + Pro Tools dev setup. Wait until later — Logic + Ableton + FL + Reaper user base (which uses VST3/AU) is much bigger.

## Quick-start verification

After CMake + HISE are installed, verify:

```bash
cmake --version    # should print 3.x
ninja --version    # should print 1.x
which HISE         # may not be in PATH; check /Applications/HISE.app exists
ls /Applications/ | grep -i hise
```

## What "Phase 0 done" looks like

You've followed this guide when:

- [ ] CMake installed: `cmake --version` works
- [ ] HISE installed: app opens, you see the empty project welcome screen
- [ ] You've followed HISE's "First Steps" tutorial: load a sample, play it back through a polyphonic sampler module, save the project
- [ ] You've exported a test plugin to `.vst3` and `.component` (AU) on macOS
- [ ] You've loaded those test plugin bundles into Ableton Live (or Logic) and made sound

When that checklist is green, the toolchain is proven and Phase 1 (engine + UI work) begins.

## Where the project files live

- HISE project files: I'll suggest creating them under `~/Desktop/ResearchFacility/hise_project/` when you're ready
- Built plug-in binaries during dev: typically auto-installed to `~/Library/Audio/Plug-Ins/VST3/` and `~/Library/Audio/Plug-Ins/Components/` (where DAWs scan for them)
- Source SFZ/WAV assets: `~/Desktop/ResearchFacility/assets/samples/` (with `.meta.json` sidecars)
- Preset files as you build them: `~/Desktop/ResearchFacility/assets/presets/`

## Common gotchas

1. **macOS quarantine.** Downloaded HISE may not open the first time. Right-click → Open → Open Anyway. Or `xattr -dr com.apple.quarantine /Applications/HISE.app`.
2. **DAW plugin scan.** First launch after building a new plugin: Ableton may not see it immediately. Force rescan: Preferences → Plug-ins → Rescan.
3. **AU validation.** Apple's `auval` tool is what Logic uses to validate AU plug-ins. If your plug-in fails auval, Logic won't show it. HISE handles this for you on export, but if you see "plugin not appearing in Logic," run `auval -a` and look for your plug-in's manufacturer code.
4. **CPU spikes from sample loading.** First voice trigger after loading a big sample can stutter while disk-streaming primes its buffer. HISE has settings for preload buffer size — increase if you see this.

## Next step

Once you've worked through this guide and have HISE running with a "hello world" sampler, ping me and we'll start Phase 1 — building the actual Research Facility engine in HISE Script.
