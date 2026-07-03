# Signing & notarizing the installer (what YOU have to do)

The installer (`packaging/build_installer.sh`) already builds a working `.pkg`.
The one thing it can't do without you is **sign + notarize** it — that needs your
Apple identity and money. Until it's signed, macOS Gatekeeper warns buyers
("unidentified developer" / "damaged"). Signed + notarized = the plugin opens
instantly on any Mac with zero friction. This is the single hard blocker to a paid sale.

## One-time setup (your accounts, ~30 min + Apple's approval wait)

1. **Buy Apple Developer Program** — $99/yr at <https://developer.apple.com/programs>.
   (Needs your legal identity, or a D-U-N-S number for a company.)

2. **Create two certificates** (in Xcode → Settings → Accounts → Manage Certificates,
   or the developer portal). Both live in *your* keychain:
   - **Developer ID Application** — signs the `.vst3` and `.component`.
   - **Developer ID Installer** — signs the `.pkg`.
   Confirm they're installed: `security find-identity -v` should list both with your
   Team ID, e.g. `Developer ID Application: Your Name (AB12CD34EF)`.

3. **App-specific password for notarization** — at <https://appleid.apple.com> →
   Sign-In & Security → App-Specific Passwords. Note your **Team ID** too.

4. **Store notarization credentials once** (keychain profile named `rf-notary`):
   ```sh
   xcrun notarytool store-credentials rf-notary \
     --apple-id "you@email.com" --team-id "AB12CD34EF" --password "xxxx-xxxx-xxxx-xxxx"
   ```

## Build a signed, notarized, sellable installer

With the certs in your keychain and the profile stored, just run the same script —
it auto-detects the identities and signs + notarizes end to end:

```sh
cd ~/Desktop/ResearchFacility
RF_VST3=/path/to/ResearchFacility.vst3 \
RF_AU=/path/to/ResearchFacility.component \
RF_NOTARY_PROFILE=rf-notary \
bash packaging/build_installer.sh
```

Output: `dist/ResearchFacility-0.1.0.pkg`, signed + notarized + stapled — ready to sell.
(Get the two plugin bundles from the latest green CI run:
`gh run download <run-id> -R SaintPopola/research-facility -n ResearchFacility-macOS-VST3`
and `-n ResearchFacility-macOS-AU`.)

## Or sign automatically in CI

Add these GitHub repo secrets, then a release workflow can build + sign + notarize on
every tag with zero local steps:

| Secret | What |
|--------|------|
| `DEV_ID_APP_P12` / `DEV_ID_INSTALLER_P12` | base64 of each exported `.p12` |
| `P12_PASSWORD` | the export password you set |
| `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD` | for notarytool |

The runner imports the `.p12`s into a temporary keychain, then runs
`build_installer.sh` exactly as above. (Ask me to wire the workflow once the secrets exist.)

## Verify a finished pkg
```sh
pkgutil --check-signature dist/ResearchFacility-0.1.0.pkg     # should show "Notarized Developer ID"
spctl --assess -vv --type install dist/ResearchFacility-0.1.0.pkg   # should say "accepted"
```
