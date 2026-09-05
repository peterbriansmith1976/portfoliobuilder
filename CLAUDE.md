# Portfolio Builder | Slate Labs

Static HTML dashboard for Irish financial brokers and advisers, plus a Python refresh
script. Models fund and portfolio performance from Aviva Ireland fund pricing data.
Built to be hosted: the app fetches its data at runtime rather than embedding it, so app
changes and data updates ship independently. Current version: v12.

Branded as **Portfolio Builder**, provided by **Slate Labs** (renamed from "Aviva Investors |
Internal Portfolio Builder", itself renamed from "Aviva Ireland Portfolio Builder"). Slate Labs
is not authorised or regulated by the Central Bank of Ireland, and the tool is not an Aviva
publication. The word "Internal" was dropped deliberately: it is no longer accurate and was
doing real regulatory work while it was there.

The data is still overwhelmingly Aviva fund data (32 of 37 funds), so the product is
provider-neutral in name only. Fund names keep their "Aviva" prefix because those are the funds'
legal names; renaming them would misidentify regulated products.

The regulatory disclaimer is **Slate Labs** text covering provider status, trade marks and
attribution, intended audience, accuracy, and jurisdiction. It replaced the Aviva Investors
entity text (AIGSL, Aviva Investors Luxembourg S.A., Aviva Investors Schweiz GmbH), which was
Aviva's own regulatory statement and could not travel to a tool Aviva does not issue.

It appears verbatim in all three surfaces — screen warnings panel, print document, and email
copy. Treat it as fixed legal text: do not reword, condense or split it, and if it changes,
change it in all three places together.

A short lead line, "Not an Aviva publication…", sits at the top of each warnings block, above
the four Warning bullets. That placement is deliberate, not decorative: nominative fair use of
a third-party trade mark is judged partly on how prominent the disclaimer is, and Aviva fund
names appear on every screen. Do not demote it into the body of the long paragraph.

Never write that Slate Labs is "not affiliated with Aviva". The author is an Aviva employee, so
that statement would be false. The correct and equally protective framing is about the tool:
it is not issued, approved or endorsed by Aviva.

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

## Data refresh — automated from Fund Focus

Since September 2026 the data comes from the Longboat Fund Focus API, not a workbook. The
spreadsheet route still works and is the fallback, but it is no longer the normal path.
CSS have confirmed automated access is acceptable.

**Do not tell the user to download a workbook.** That was the old process. If they ask to
update the data, use the pipeline below.

```
./refresh_daily.sh        # what the scheduler runs: check, fetch, verify, stage
./publish.sh "2026-09 data"
```

A launchd agent (`cloud.portfoliobuilder.refresh`) runs `refresh_daily.sh` daily at 14:30.
On most days it exits in about a second having done nothing. It **never publishes**.

**The project lives at `~/portfoliobuilder`, deliberately not in `~/Documents`.** macOS blocks
background agents from Documents, Desktop and Downloads, so the scheduled job could not read its
own data there. Moving it was chosen over granting Full Disk Access to `/bin/bash`, which would
have given every shell script on the machine access to everything. Do not move it back.
Keychain access from launchd works fine; only the folder was the problem.

### The pieces

- `month_ready.py` — the readiness gate. Public Aviva API, no credentials.
- `fundfocus.py` — Fund Focus client. Credentials come from the macOS keychain, service
  `fundfocus`. Never logged, never passed as an argument, never in error text.
- `reconcile.py` — method check against Longboat's own published figures.
- `fetch_month.py` — fetch, overlap check, method check, append, stage to `work/staged.json`.
- `fund_map.json` — the fund mapping, self-verifying.

All are gitignored. `data/` holds only published payloads; anything transient goes in `work/`,
because `publish.sh` globs `data/*.json` and would otherwise ship working files.

### Readiness: do not gate on a month-end row existing

A month-end row appears carrying a **forward-filled** value before the real price is struck.
31 Aug 2026 returns 28 Aug's prices verbatim. Publishing that would write a wrong month, and
the "published months must not change" rule would then block the correction.

Gate on the **frontier**: the provider must have published prices at least two days beyond the
month end. `Price/GetLatestDate` answers this in 21 bytes with no login.

The "did the price move?" test cannot gate. It works when a month ends on a business day and
fails when it ends at a weekend, where the month-end price legitimately is Friday's carried
forward. Tested across seven months: correct on five, false negative on Feb (Sat) and May (Sun).
It is kept only as a warning.

### Reconciliation: use GetDaily, not GetMonthly

`PerformanceReport/GetMonthly` lags — it read `2026-07-31` while prices ran to `2026-09-04` —
and it was never established whether that reflected finality or a slow refresh. Do not gate or
reconcile on it.

`PerformanceReport/GetDaily` is current to the latest price date and reconciles **exactly**:
1M, 3M, YTD, 1Y, 3Y and 5Y all agree to about 5e-7, the price-rounding floor. Longboat compute
those figures in their own system; we derive ours from their raw prices. Agreement to seven
decimals is a regression detector, not a tolerance. Tolerance is 1e-5, and it has been verified
to fail when tightened below the floor.

Covers the 32 Aviva funds. The 5 Dimensional funds are not on the public feed and are covered
by the overlap check.

### Things that will bite

- **Longboat publishes net of AMC; the dashboard stores gross.** Comparing the wrong basis
  manufactures a ~4.6pp error that looks like a real fault.
- **Stamping is D+1.** A price stamped date D is the price for D-1, so the stamp on the 1st of
  month M+1 is the month end of M. Shifting by one day breaks the reconciliation immediately.
- **`(FundId, isMaster)` is the only unique key** across the Longboat universe: 189 records
  share 142 FundIds, base funds and series variants carrying different AMCs. Inside the saved
  report FundId alone is safe, since the 37 selections are explicit.
- The saved report is **"AA Price", id 111116**, 37 funds, 32 Aviva and 5 Dimensional.

### Order, every time

1. `refresh_daily.sh` runs the gate, fetch and all checks, and stages. Read its report out in full.
2. Any problem, stop. Do not install, do not publish, diagnose first.
3. **Wait for the user to confirm the report looks right.** They know what to expect; Claude does not.
4. Local preview at `http://localhost:8000`, check the as-at badge and a portfolio they recognise.
5. Only once they approve, publish.

A data refresh is never published on a general go-ahead. It changes displayed figures, so it
always needs explicit sign-off, per the publishing protocol below.

### Fallback: the workbook

Still works if the API is unavailable. The source workbook lives at
`Portfolio builder files.xlsx` in the project root under that exact name; `*.xlsx` is
gitignored. Do not select it by "most recent file" — two workbooks have existed with the
identical name, one holding 37 funds and one holding 32 without the Dimensional range.

```
./update_data.sh
```

`check_data.py` is shared by both routes and blocks on funds disappearing, the as-at going
backwards, and already-published months changing value.

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
- **Fund-level Vol and MDD differ by surface, deliberately.** On screen they follow the selected
  window, so the building blocks table agrees with the summary cards and the growth and drawdown
  charts. In the print document they stay on a fixed 5-year basis, taken from that portfolio's
  own `pdStats5` range so the fund table, the cards and the methodology paragraph all describe
  one period. Print clamps to the portfolio's common start, not each fund's own start: before
  this, a portfolio holding a 2003 fund and a 2023 fund measured the first over 60 months and
  the second over 38 inside a section captioned with a single basis, and the caption was false
  for the first. Both surfaces label the period in the column header. `fundRisk(f, from, to)` therefore takes an
  explicit range and has no default: each caller declares its own basis. Do not "unify" these.
  Before this split the table was always a fixed trailing 60 months while the cards followed the
  window, so at the Max window a portfolio could show a deeper drawdown than any of its holdings
  (-40.4% against fund figures of -20.2% and -11.5%), which is arithmetically impossible over a
  common period and was pure presentation. The screen table header names the window it covers,
  derived from the months actually rendered rather than the button pressed, so a clamped window
  is labelled honestly.
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

**Two marks, and they are not interchangeable.** The Slate Labs mark (a rounded square with a
notch cut from the top-right, inline SVG on a 41x33 viewBox) is the *company* mark: it sits in
the top brand band beside the SLATE LABS wordmark, and in the print band. The three-bar glyph on
its signal-blue tile is the *product* mark: it sits beside the "Portfolio Builder" H1 and in the
favicon. Both are inline SVG using `currentColor`, which is what lets one copy work on light and
dark without a second asset. Source artwork for the Slate Labs mark is a JPG the user supplied;
the path in the file was traced from it, so there is no image dependency to keep in sync. Email
gets neither mark, because Outlook renders through the Word engine and cannot draw SVG.

**The SLATE LABS wordmark is the user's own artwork, not type and not a redraw.** It is
monoline geometric caps with a crossbar-less A, which no Google Font reproduces; the faces that
do (Apex, Bool, Rati) are commercial. An attempt to redraw it as SVG paths was rejected as too
tall and too thin, and measurement confirmed it: the real wordmark is 10.35x its cap height,
the redraw was 7.47x.

It is now extracted straight from the supplied JPG (`~/Downloads/mQaBi.jpg`) and inlined as a
base64 PNG, about 6.7KB. The background was removed by deriving alpha from luminance, so paper
is transparent and edges stay anti-aliased. RGB carries the artwork's own charcoal, which lets
one file serve two purposes:

- **Screen** uses it as a CSS mask on `.bname` with `background-color:currentColor`, so the
  alpha channel supplies the shape and the theme supplies the colour. One asset, both themes.
- **Print** uses the same PNG as a plain `<img>`, relying on its charcoal directly. Deliberate:
  print is always light, and this avoids depending on mask support in the print renderer, where
  a failed mask would render nothing at all.
- **Email** keeps plain text, because Outlook renders through the Word engine.

`.bname` carries `role="img"` and `aria-label="Slate Labs"` since it is no longer real text. Do
not replace this with live text in Nunito Sans, and do not add a font dependency for it.

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
