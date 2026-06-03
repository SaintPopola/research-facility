# Claude takes control — you don't touch HISE

> **2026-06-03.** You said you don't want to work in HISE. Here's the path where I drive everything and you only do things no human can avoid (push to your own GitHub once, click "Open" on a security prompt once).

## The architecture

```
        YOU                              CLAUDE (me)                     CLOUD
   ─────────                         ─────────────                    ────────
                                                                    
   tell me what to                 edit code/patches/UI
   do in chat            ──→       in ~/Desktop/ResearchFacility
                                            │
                                            ▼
                                    git push ─────────────────────→  GitHub
                                                                          │
                                                                          ▼
                                                            ┌──────────────────┐
                                                            │ macos-14 runner  │
                                                            │ Xcode pre-installed│
                                                            │ HISE CLI export   │
                                                            └────────┬─────────┘
                                                                     │
                                                                     ▼ artifact
                                          ╔══════════════════════════════╗
                                          ║  ResearchFacility.vst3       ║
                                          ║  ResearchFacility.component  ║
                                          ╚══════════════════════════════╝
                                            │ (download via gh CLI)
                                            ▼
                                    install to ~/Library/Audio/Plug-Ins/
                                            │
                                            ▼
   open Ableton/Logic   ←──    DAW sees plugin, you play
```

GitHub Actions has free unlimited macOS minutes for public repos. Xcode is pre-installed on their runners. The cloud builds; you receive.

## What you do (one-time, ~20 min)

These three things ARE on you, but each is a single setup that you never repeat:

### 1. Create GitHub account (5 min)

If you don't have one already: [github.com/signup](https://github.com/signup). Pick any username. Free.

### 2. Install gh CLI (5 min)

Mac App Store doesn't have it. Three options:

**Option A — via Homebrew** (recommended; lets you install other tools easily later)
```bash
# Install Homebrew first (free, no signup):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Then:
brew install gh
```

**Option B — direct .pkg installer** (no Homebrew needed)
Download from [cli.github.com](https://cli.github.com/) → click the macOS download → run the installer.

**Option C — already have it**
Run `which gh` — if it prints a path, skip this step.

### 3. Authenticate gh CLI + create the repo (5 min)

```bash
gh auth login
# Choose: GitHub.com → HTTPS → "Login with a web browser" → paste the code → click "Authorize"

cd ~/Desktop/ResearchFacility
gh repo create research-facility --public \
  --description "A sonic research lab for musicians. Hybrid sampler/synth. GPL-3." \
  --source=. --remote=origin --push
```

Done. You should see your repo at `https://github.com/<your-username>/research-facility`.

## What I do from here on

After you complete the 3 steps above, every change goes through this loop:

### When I make code changes

I edit files locally. When I want to test, I run:

```bash
cd ~/Desktop/ResearchFacility
git add . && git commit -m "..." && git push
```

Pushing automatically triggers the GitHub Actions workflow `.github/workflows/build-plugin.yml`. The cloud:

1. Clones your repo
2. Clones HISE source (cached after first run)
3. Downloads pre-built HISE.app
4. Runs `HISE export_ci` against `ResearchFacility.xml`
5. Outputs `.vst3` and `.component` bundles
6. Uploads them as artifacts (kept for 90 days)

Build time: ~15-20 min the first time, ~5-8 min on subsequent builds (cache hit).

### When I want to install the latest build to your Mac

```bash
./scripts/download_build.sh --build --wait
```

This script:
1. Triggers the workflow
2. Waits for it to finish
3. Downloads the artifacts
4. Installs to `~/Library/Audio/Plug-Ins/VST3/` and `~/Library/Audio/Plug-Ins/Components/`
5. Strips macOS quarantine attribute
6. Reports status

Your DAW picks it up on next plugin scan.

## What you can't avoid (no human can)

These tasks involve your physical computer, your wallet, or your ears. I can't:

1. **Approve macOS security prompts** the first time a new unsigned plugin loads. You see "Research Facility can't be opened" once; right-click the .vst3 in Finder → Open → Open Anyway → done forever for that build. ~10 seconds.
2. **Decide if it sounds good.** Sound design has ears. You listen, give feedback, I adjust parameters/code.
3. **Push to YOUR GitHub account.** I can write commits, but the push uses your auth. You run `git push` (or I run it from your terminal with your gh auth).
4. **Buy a domain / set up storefront.** When the time comes to take payments, you connect your bank/Stripe/Gumroad. I can't be the merchant of record.

That's the entire list.

## Verification this works before you commit time

Test the no-HISE-needed path:

```bash
# After Step 3 above (repo exists on GitHub):
cd ~/Desktop/ResearchFacility
gh workflow run build-plugin.yml
gh run watch    # waits for completion; ~15-20 min
gh run download --name ResearchFacility-macOS-VST3 -D /tmp/rf-test
ls -R /tmp/rf-test
# Should show ResearchFacility.vst3 bundle
```

If you see a `.vst3` in that listing — the entire pipeline works. You never opened HISE.

If the build fails (the HISE CI on free macos-14 runners has known edge cases — see HISE forum), I read the failure log via `gh run view --log`, fix the workflow, push again. Iterate from chat. You don't have to think about it.

## Honest constraints I can't fix

1. **First plugin build takes 15-20 minutes** on the free macos-14 runner. You wait while CI runs. Subsequent builds are 5-8 min.
2. **macOS security prompts** on first load of each new build version. Unavoidable until we buy Apple Developer ($99/yr, deferred until revenue).
3. **If GitHub Actions changes pricing**, the free path could shrink. Currently macOS minutes are unlimited for public repos. Has been stable for years.
4. **HISE CLI sometimes fails on macos-14 in ways that don't fail in HISE GUI.** Forum reports exist. If we hit this, I fix the workflow (might involve a different runner image, or a self-hosted runner, or falling back to a Pamplejuce/JUCE rewrite).

## Fallback if the GitHub Actions path breaks

If HISE CLI build genuinely won't run on macos-latest runners (we'll find out on first try), the realistic alternatives in order of preference:

1. **Mac App Store install of Xcode** (free, 12 GB download you walk away from for 30 min; then I build locally via terminal). Zero ongoing user effort.
2. **Pamplejuce/JUCE rewrite** — pure C++ project that compiles via just CMake + CLT (which we already have). Throws away the Phase 1 HISE work. ~1-2 weeks redo.
3. **You do the HISE GUI export** the first time, then I copy that exported .vst3/.component to a known location for re-distribution. Defers the problem.

We try CI first. If it breaks, we adapt.

## What you do RIGHT NOW

Three commands. ~10 minutes of waiting:

```bash
# 1. Install gh CLI (Option A or B above)

# 2. Authenticate
gh auth login

# 3. Push the repo and trigger the first build
cd ~/Desktop/ResearchFacility
gh repo create research-facility --public --source=. --remote=origin --push
gh workflow run build-plugin.yml
gh run watch    # wait ~15-20 min for first build
```

Then paste the result in chat. From that point I drive everything.

## Mental model

Old workflow (with closed-source assumption):
> User opens HISE → loads patch → tweaks → exports → installs → tests → reports back

New workflow ($0 + don't-touch-HISE assumption):
> User talks to me in chat → I edit code → push to GitHub → CI builds → install script lands plugin in /Library/Audio/Plug-Ins → user opens DAW → reports back what they hear

HISE local copy still exists (`/Applications/HISE.app`) — you can use it for previewing if you ever want to. But it's no longer in the critical path. You only ever need: a browser, a terminal, your DAW, your ears.
