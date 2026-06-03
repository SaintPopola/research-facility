# Ship to GitHub — step-by-step

> **2026-06-03.** Concrete actions to get Research Facility from local repo to public GitHub with GitHub Pages marketing site.

Since the $0 path mandates D11 = public GitHub repo (GPL requires source available when distributing binaries), here's how to actually get there.

## Step 0 — One-time setup (5 min)

You need:
1. A GitHub account at [github.com](https://github.com/) (free)
2. The `gh` CLI installed (optional but easier) OR your SSH key uploaded to GitHub

### Install gh CLI

```bash
# Homebrew route (needs Homebrew installed; if not, skip and use SSH key instead)
brew install gh
gh auth login
# Choose: GitHub.com → HTTPS → Yes (use credentials) → Login with web browser
```

### Alternative: SSH key route (no Homebrew needed)

```bash
ls -la ~/.ssh/id_ed25519.pub 2>/dev/null
# If file doesn't exist:
ssh-keygen -t ed25519 -C "30rolo@gmail.com"
# Press enter for defaults

# Copy the public key:
cat ~/.ssh/id_ed25519.pub | pbcopy
# Paste it at https://github.com/settings/keys → "New SSH key"
```

## Step 1 — Create the repo on GitHub

### Via gh CLI

```bash
cd ~/Desktop/ResearchFacility
gh repo create research-facility --public \
  --description "A sonic research lab for musicians. Hybrid sampler/synth. GPL-3." \
  --source=. --remote=origin
gh repo edit --enable-issues --enable-discussions
```

### Or via the GitHub website

1. Go to https://github.com/new
2. Name: `research-facility` (or whatever you prefer)
3. Description: "A sonic research lab for musicians. Hybrid sampler/synth. GPL-3."
4. Public ✓
5. Skip the "Initialize repository" options (we already have a local repo)
6. Create

Then locally:
```bash
cd ~/Desktop/ResearchFacility
git remote add origin git@github.com:<your-username>/research-facility.git
# or HTTPS:
git remote add origin https://github.com/<your-username>/research-facility.git
```

## Step 2 — Push the existing commits

```bash
cd ~/Desktop/ResearchFacility
git push -u origin main
```

You should now see the project at `https://github.com/<your-username>/research-facility`.

## Step 3 — Enable GitHub Pages

This publishes the `site/` folder as your free marketing site.

### Via gh CLI

```bash
gh repo edit --enable-pages
# Then in the GitHub web UI under Settings → Pages, set:
#   Source: Deploy from a branch
#   Branch: main / /site
```

### Or via website

1. Go to your repo → Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: `main` · folder: `/site`
4. Save

After ~1-2 minutes your site is live at:
`https://<your-username>.github.io/research-facility/`

Optionally, configure a custom domain:
- Buy `researchfacility.audio` (~$15/yr) at any registrar (Namecheap, Cloudflare Registrar are cheap)
- In your DNS, add a CNAME record: `www → <your-username>.github.io`
- In GitHub Pages settings → Custom domain → enter `researchfacility.audio`

But this costs money. Skip until revenue exists.

## Step 4 — Adjust internal links

The `site/index.html` has links like `../docs/06_product_requirements.md`. These work locally but in GitHub Pages they need adjustment:

```bash
# Quick fix: update site/index.html links to point to GitHub-rendered markdown
cd ~/Desktop/ResearchFacility
# Replace '../docs/' with absolute github links
sed -i.bak 's|href="../docs/|href="https://github.com/<your-username>/research-facility/blob/main/docs/|g' site/index.html
rm site/index.html.bak
git add site/index.html
git commit -m "site: link docs to GitHub markdown views"
git push
```

(Replace `<your-username>` with your actual GitHub username before running.)

## Step 5 — First Release (when ready for v0.1)

When Phase 2 is complete and you have a buildable plugin:

```bash
# Tag the release
git tag -a v0.1.0 -m "v0.1.0 — pre-alpha public release"
git push origin v0.1.0

# Create the release with binaries (after building in HISE):
gh release create v0.1.0 \
  --title "v0.1.0 — pre-alpha public release" \
  --notes-file CHANGELOG.md \
  ResearchFacility-v0.1.0-macOS.zip \
  ResearchFacility-v0.1.0-Windows.zip
```

GitHub Releases hosts the binaries for free — no S3, no CloudFront, no bandwidth cost.

## Step 6 — Set up Discord (optional, free)

For community + support:
1. discord.com/register
2. Create a new server "Research Facility"
3. Create channels: #announcements, #general, #support, #bugs, #presets-share
4. Copy invite link
5. Add it to README.md and site/index.html

Cost: $0.

## Step 7 — Set up the donation / payment store (when v0.1 is real)

For the paid Studio tier:

### Easiest — Gumroad
1. Sign up at gumroad.com
2. New Product → "Digital Product"
3. Upload your .pkg/.exe installer + library .zip
4. Set price ($79)
5. Get the share URL → add to `site/index.html` Studio CTA
6. Cost: $0 monthly, 10% + Stripe 2.9% + 30¢ per sale

### Recommended — LemonSqueezy
Better for international sales (VAT handled), 5% per sale instead of 10%.
1. Sign up at lemonsqueezy.com
2. New store, new product → digital download
3. Same flow as Gumroad
4. Cost: $0 monthly, 5% + Stripe per sale

### Free donations — Ko-fi or Buy Me a Coffee
1. ko-fi.com/register (free tier)
2. Add donation button to README
3. Optional shop tier (5% fee) for paid products

## Step 8 — Ongoing maintenance

Once the repo is public:
- Tag every release: `git tag -a v0.X.Y -m "..."`
- Update CHANGELOG.md before each release
- Watch GitHub Issues for bug reports
- Update `site/index.html` status section as phases complete
- Sample submissions from contributors → check sidecar before merge: `python3 scripts/validate_library.py`

## Cost summary for going public

| Step | Cost |
|---|---|
| GitHub account | $0 |
| Public repo | $0 |
| GitHub Pages site | $0 |
| GitHub Releases for binaries | $0 |
| Discord server | $0 |
| Gumroad / LemonSqueezy account | $0 |
| Custom domain (optional) | $0 (skip) or ~$15/yr |
| **Total to ship** | **$0** |

This is the entire infrastructure to take Research Facility public, distribute it, and accept payments. Zero out of pocket. The payment processor only takes a cut when sales happen.

## Anti-pattern: don't do these

1. **Don't push commits to a public repo containing API tokens or `.env` files.** The `.gitignore` excludes these, but double-check `git ls-files | xargs grep -l "FREESOUND_TOKEN\|secret\|password"` before pushing.
2. **Don't push sample WAVs with unknown licenses.** Run `python3 scripts/validate_library.py` before each push; the validator rejects CC-BY-NC and unknown.
3. **Don't promise ship dates publicly.** Solo plugin projects' #1 failure mode is missed public deadlines. Internal milestones yes, public ones no.
4. **Don't enable GitHub Discussions on day 1 if you can't moderate them.** Start with Issues only; add Discussions when you have community.

## What to push first vs. defer

Push immediately after going public:
- README.md
- LICENSE
- docs/* (the public-facing ones)
- site/* (marketing)
- scripts/*
- hise_project/ResearchFacility/{Scripts,XmlPresetBackups,SampleMaps,*.xml}

Maybe defer (large or sensitive):
- docs/01_upstream_research.md (currently gitignored — it's a mirror; not yours to publish verbatim)
- Sample WAVs over 10 MB (use git-lfs or external storage if needed)
- Build artifacts in `Binaries/` (already in .gitignore)

Your current repo is clean — first push should be fine as-is.

## Final pre-push checklist

```bash
cd ~/Desktop/ResearchFacility
python3 scripts/validate_library.py     # sample licenses OK?
git status                                # working tree clean?
git log --oneline                         # commits look right?
git ls-files | grep -i "secret\|token\|password\|.env"   # any leaked secrets? (should print nothing)
```

If all green, you're ready to push.

## Reminder

Going public makes the code visible to competitors. That's fine. As covered in `FREE_PATH.md`, the moat is the library + brand + UX, not the engine. Indie plugin success is overwhelmingly social, not technical.

Vital ships publicly and makes meaningful money. So can this.
