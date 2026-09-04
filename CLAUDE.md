# Aviva Investors | Internal Portfolio Builder

Static HTML dashboard for Irish financial brokers and advisers, plus a Python refresh
script. Models fund and portfolio performance from Aviva Ireland fund pricing data.
Built to be hosted: the app fetches its data at runtime rather than embedding it, so app
changes and data updates ship independently. Current version: v12.

Branded as **Aviva Investors | Internal Portfolio Builder** (renamed from "Aviva Ireland
Portfolio Builder").

The regulatory disclaimer is **Aviva Investors** entity text (AIGSL, Aviva Investors Luxembourg
S.A., Aviva Investors Schweiz GmbH), replacing the earlier Aviva Life & Pensions Ireland DAC
wording. It is supplied by the business and appears verbatim in all three surfaces — screen
warnings panel, print document, and email copy. Treat it as fixed legal text: do not reword,
condense or split it, and if it changes, change it in all three places together.

## Files

The app and its data are separate files, so the two ship independently: a data refresh
replaces one JSON file and never touches the app.

- `index.html` — the whole dashboard, with no data inside it. Fetches `data/latest.json` on
  load. No build step and no external dependencies except the Google Fonts stylesheet.
- `data/latest.json` — the payload the app fetches. `data/YYYY-MM.json` alongside it are dated
  archive copies.
- `refresh_dashboard.py` — builds the payload from the source workbook.
- `update_data.sh`, `check_data.py` — monthly refresh with a pre-publish review report.
- `publish.sh` — the only publishing route. Local helpers, all gitignored.
- `Portfolio builder files.xlsx` — monthly source workbook, project root, fixed name,
  gitignored. Four sheets:
  `ALPI fund centre details`, `Price history live`, `Simulated prices`, `Report`.

The previous self-contained `aviva_portfolio_builder_v12.html` was deleted once the split was
verified. Dated `*.bak.html` snapshots of it remain in the project root.

## Data refresh — the order is fixed

The source workbook lives at `Portfolio builder files.xlsx` in the project root, under that
exact fixed name. Each month the new workbook is saved over it, so the command never changes.
`*.xlsx` is gitignored, so the workbook stays local and is never published.

Do not select the workbook by "most recent file". Two workbooks have already existed with the
identical name `Portfolio builder files 31072026.xlsx`, one holding 37 funds and one holding 32
without the Dimensional range. Refreshing from the wrong one would have removed five funds from
the live site. `update_data.sh` therefore reads the fixed name only.

```
./update_data.sh          # rebuild and review, does not publish
./publish.sh "2026-08 data"
```

`update_data.sh` builds to a staging file, runs `check_data.py` against the currently published
`data/latest.json`, and installs into `data/latest.json` plus a dated `data/YYYY-MM.json` only
after the user approves. `refresh_dashboard.py` is still the engine and is unchanged; it
dispatches on output extension, and legacy three-file mode still works.

`check_data.py` reports and blocks on:

- **Funds disappearing.** A hard stop. Brokers lose them from the picker.
- **As-at going backwards.** A hard stop, it means the wrong workbook.
- **Already-published months changing value.** A hard stop. Adding a new month must never
  alter a past one; if it does, something is wrong upstream, not in the dashboard.
- As-at not advancing, or no fund gaining a month. Warnings, usually the same workbook twice.

The steps run in this order, every time:

1. Run `./update_data.sh` and read the review report out to the user in full.
2. If it reports a problem, stop. Do not install, do not publish, diagnose first.
3. **Wait for the user to confirm the report looks right.** They know which funds and periods
   to expect; Claude does not.
4. Install, then start the local preview and have the user check the as-at badge and a
   portfolio they recognise at `http://localhost:8000`.
5. Only once they approve, publish.

A data refresh is never published on a general go-ahead. It changes displayed figures, so it
always needs explicit sign-off, per the publishing protocol below.

## Loading and failure behaviour

`applyData()` is the single entry point for data arriving: it assigns `DATA`, derives
`startIdx`/`liveIdx`, prunes selections naming funds that no longer exist, refreshes the as-at
badge and re-renders. `loadData()` fetches, shape-checks, then calls it.

- **The fetch is cache-busted** (`?v=` + timestamp). Without this a user keeps seeing the
  previous period's figures from browser cache, which is the quietest way for this to go wrong.
  GitHub Pages does not allow custom `Cache-Control`, so the query param is the only lever.
- **Failures surface visibly.** A 404, a network error, malformed JSON or a failed shape check
  all render "Could not load fund data" plus the reason, and `DATA.funds` stays empty rather
  than half-applying. A blank dashboard that merely looks unpopulated is worse than an error.
- The client-side shape check guards against a truncated or half-written upload. It is not a
  substitute for upstream validation: `build_data()` already raises on any gap in a spliced
  series.

## Hosting

Static hosting only. `index.html` at the repo root, `data/` beside it. Because the data is
fetched, **the app cannot be opened from `file://`** any more, as browsers block those fetches.
Serve it over http even when testing locally.

## Publishing protocol — the order is fixed

The live site is https://www.portfoliobuilder.cloud, served from the `portfoliobuilder` GitHub
repo. The project root is a git clone of it, authenticated over SSH, so publishing is a push.
`publish.sh` is the only route: it stages an explicit allowlist (`index.html`, `data/*.json`,
`refresh_dashboard.py`, `.gitignore`), so the source workbook and the `*.bak.html` snapshots
cannot reach the repo even if staged by accident. `./publish.sh "msg"` prompts for
confirmation; `./publish.sh -y "msg"` skips the prompt and is the form Claude uses.

**Never publish before the user has seen the change running locally.** The steps run in this
order, every time, with no shortcuts:

1. Make the change and verify it yourself, including the browser console.
2. Start the local preview and give the user the URL:
   `python3 -m http.server 8000` from the project root, then `http://localhost:8000`.
   Start it in the background so the session stays usable, and say what specifically to look at.
   `file://` does not work: the app fetches its data, and browsers block that on local files.
3. **Wait for the user to confirm they have looked at it.** Do not ask "shall I publish?" in
   the same breath as announcing the change is ready. The review is the point of the gap.
4. Only once they approve, publish, and stop the preview server.

Rework loops back to step 1, and the user re-checks before it goes out. "Approved earlier"
never carries across to a changed build.

Two categories always need explicit user sign-off and are never published on a general
go-ahead: anything altering displayed figures or the regulatory disclaimer text, and any data
refresh. Look and feel, layout and bug fixes may be published as soon as the user approves the
local check.

To undo a publish: `git revert --no-edit HEAD && git push`, live again in about a minute.

## Locked methodology — do not change without asking

- **Month-end convention.** Live MoneyMate prices are stamped the first of the following
  month. Shift every live date back one day to the true month end. Simulated prices are
  already correctly dated at month end.
- **Grossing up.** Live prices are net of AMC. Gross up geometrically per fund:
  `(1 + r) * (1 + AMC)^(1/12) - 1`.
- **Simulated series are already gross.** Never gross them up again.
- **Splicing.** Live data wins from the first live price onwards; simulated returns are used
  only strictly before that date. Any gap in a spliced series is a hard error, not a warning.
- **Path-based portfolio statistics.** Volatility, maximum drawdown and the portfolio ESMA
  band are computed on the actual portfolio return series (allocation-weighted, monthly
  rebalanced), never as weighted averages of fund-level figures. This captures diversification
  and was a deliberate upgrade from earlier versions.
- **Gross display only.** All performance, growth and projection figures are gross of AMC.
  The weighted portfolio cost is shown separately and never deducted, because adviser and
  plan-level charges vary and are not known to the tool.
- **Portfolio ESMA** maps the window's annualised gross volatility to SRRI bands
  (1: <0.5%, 2: <2%, 3: <5%, 4: <10%, 5: <15%, 6: <25%, 7: above). Indicative only, since
  regulatory SRRI uses a fixed 5-year basis. Print document uses a fixed 5-year basis.
- **Comparison mode** measures Portfolio A and B over the common history of all selected
  funds across both, so the two are always like for like.

## Source data quirks

- `ESMA_OVERRIDES` in the refresh script patches Aviva Global Equity ESG Passive Series 1 to
  ESMA 6; the source cell contains a single space. Remove the override once fixed at source.
- Corporate Bond is absent from the Report sheet, so it cannot be reconciled.
- Reconciliation against the Report sheet is expected to tie within about 1bp on low-volatility
  funds. Larger gaps on volatile funds (Gold, emerging markets) are business-day price sampling
  where the 1st falls on a non-pricing day, not a methodology error. Do not "fix" these.

## Known limitations to keep disclosed

- Monthly pricing understates true maximum drawdown and intra-month stress losses.
- The gross-up assumes AMC is the only fund-level charge embedded in unit prices.
- Stochastic projections are GBM with a fixed seed, calibrated to the selected window.
  Withdrawals are fixed in euro, not indexed.

## Product boundaries

This is a portfolio modelling and illustration tool, not advice. It computes and displays;
it does not recommend. Features that imply a recommendation have been deliberately rejected:
risk profile target selectors, preset portfolios, baseline comparison against a reference
portfolio, share links. The Liberation Day / April 2025 tariff shock was explicitly excluded
as a stress episode. Do not reintroduce any of these without asking.

Stress episodes are GFC (Nov 2007 to Feb 2009), Covid crash (Feb to Mar 2020) and the 2022
bond selloff (Jan to Oct 2022).

## Conventions

- European date formats, euro by default, en-IE locale.
- Fund picker category order is fixed: Multi-Asset, Equity, Alternative, Fixed Income.
- Print document is A4 portrait, sections wrapped in `.pd-sec` with `break-inside: avoid` so
  a section never splits across pages. Screen disclaimers are always visible and hidden in print.
- Maximum 5 funds per portfolio. Single-fund portfolios are allowed.
- Allocations are free-form and never pre-populated; "Equal split" fills them on demand.

## Design system — "Slate & Signal"

Replaced the original navy `#0B1240` / Aviva yellow `#FFD900` brand. Typography is Nunito Sans
throughout; the Source Serif 4 headings were dropped (this reads as a software product, not an
editorial one).

**The one rule that matters: signal blue is for action, never decoration.** Buttons, active
tabs, focus rings, editable-input borders, and the logomark. Nothing else. Section labels,
category headings, the ◆ simulated marker and subheads are all muted grey — they are structure,
not actions. A mechanical find-and-replace of the old yellow will violate this, because yellow
*was* used decoratively; check every new `var(--signal)` against this rule.

**Data colours are a separate system from the accent.** Charts and fund identity use
`--d1`..`--d5` (steel blue, ochre, green, purple, grey). Portfolio A is `--d1`, Portfolio B is
`--d2` — blue vs ochre, the safest pairing for colour-blind readers, and they must stay
consistent between screen, print and email so a printed comparison matches the screen.

**Light and dark.** Screen supports both via `[data-theme="dark"]` on `<html>`, toggled in the
header and remembered in `localStorage` (wrapped in try/catch — storage is unavailable in some
`file://` contexts). Signal blue is re-tuned to `#5B8DEF` in dark mode: the light-mode
`#1A4FD6` computes to only 2.6:1 on the dark ground and fails contrast.

**Print and email are always light**, regardless of the screen toggle — print is ink, and email
gets forwarded and printed. They also render outside this document's CSS cascade, so they
**cannot use `var()`** and must use literal hex (`SEG_FIXED`, `CA_FIXED`, `CB_FIXED`). Screen
charts do use `var()`, which is what makes them follow the theme toggle; changing a theme
therefore requires a re-render, which `applyTheme()` handles.

**Email additionally cannot use inline SVG** — Outlook renders through the Word engine. No
icons travel to email; the brand device there is a solid-colour table cell instead.

## Working style

Confirm understanding and methodology before implementing, rather than presenting surprises
afterwards. Say when an approach is wrong instead of going along with it. Skip preamble.
No em dashes. Verify numeric changes against an independent calculation before declaring done.

## Data governance

Pricing data is licensed from MoneyMate / Longboat Analytics. Keep source workbooks local.
Flag any change that would put licensed or client data into a client-facing artefact or an
external system.
