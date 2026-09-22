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

**Displayed names keep "Aviva"** on every surface (screen, print, email), at the user's request (18 Sep 2026),
so Aviva funds read the same way as Zurich, New Ireland, Irish Life and Royal London funds beside them.
`short()` still drops the series suffix, "(Ireland)" and a trailing "Fund", but no longer the "Aviva "
prefix. The five Dimensional funds keep their own names, by the user's decision: they are in the Aviva
range (and under Aviva in the Provider filter) but "Aviva" is not part of their legal names.
**The share-class ending is never displayed** ("Series C", "Series 1", any "Series X", and a closing "G" as on
Stewardship Ethical Equity and four Zurich funds), at the user's request,
since every figure is gross of fees and the class adds nothing. `fullName()` strips it and is used wherever the
full name is shown (picker tooltip, holdings table, print, email, explorer titles); `short()` builds on it. The
data keeps the legal names, which remain the keys for selections and allocations.

The regulatory disclaimer is **Slate Labs** text covering provider status, trade marks and
attribution, intended audience, accuracy, and jurisdiction. It replaced the Aviva Investors
entity text (AIGSL, Aviva Investors Luxembourg S.A., Aviva Investors Schweiz GmbH), which was
Aviva's own regulatory statement and could not travel to a tool Aviva does not issue.

**Revised 20 Sep 2026** at the user's request, in every surface that carries each sentence: the source now reads
"the Aviva Ireland website and the Fund Focus service provided by Longboat Analytics / MoneyMate / CSS" and names
those three in the accuracy clause; the cost sentence now reads "Where a portfolio cost is shown... All performance
figures are gross: no fund, adviser or plan-level charges have been deducted", since the All Funds tabs show no cost
and the old "gross of charges; the portfolio cost... has not been deducted" said the same thing twice (the user
spotted the tautology).

**Print now carries the full text, from the screen block itself.** It used to hold three paragraphs where the
others held seven, omitting the simulated-performance, cost and volatility paragraphs. Fixed on the user's
instruction (20 Sep 2026): `buildPrintDoc()` reads `.disc`'s innerHTML, swaps the h3 for an h4 and scopes
`--ink` to #0D1B2A on the wrapper, because the first paragraph's inline `color:var(--ink)` would print
near-white from dark theme (the same trap `about.html` documents). There is now **one source** for screen,
print and About; only email keeps its own copy, since Outlook needs inline styles. Verified: all 11 items
(7 paragraphs, 4 warnings) match the screen word for word. Cost: the block is 85px taller, so a mixed
comparison such as 2 + 3 funds now runs to 3 pages; page 1 is unchanged in every case and single portfolios
still print on 2. The heading matches the screen's, both uppercase: reading it as sentence case came from
measuring `innerText` while `#printdoc` was hidden, where the browser reports untransformed text. Force
`display:block` before measuring the print document, or the reading is worthless.

It appears in **four** surfaces — screen warnings panel, print document, email copy, and the
About page, which reuses the screen block exactly. Treat it as fixed legal text: do not reword,
condense or split it, and if it changes, change it in all four places together. `about.html` scopes
`--ink` to white inside the block, because the block's first paragraph carries an inline
`color:var(--ink)` that would otherwise render dark navy on the dark panel and vanish.

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
- `data/allocation.json` — asset mix per fund, fetched separately and optional (see Asset mix).
- `data/inside.json` — per-fund breakdowns for the Fund explorer's "What's inside" cards, fetched
  separately by `fetch_inside.py` and optional (see Fund explorer).
- `data/others.json` — the other providers' funds (Zurich, New Ireland, Irish Life, Royal London),
  fetched separately by `fetch_others.py` and optional (see All Funds tabs).
- `refresh_dashboard.py` — builds the payload from the source workbook.
- `update_data.sh`, `check_data.py` — monthly refresh with a pre-publish review report.
- `about.html` — a plain About page: what the tool is, who provides it, data sources, privacy, contact
  (hello@portfoliobuilder.cloud), and the warnings block reproduced verbatim. Linked under the
  disclaimer on the dashboard (hidden in print).
- `robots.txt`, `sitemap.xml`, `.well-known/security.txt`, `.nojekyll` — crawler and legitimacy signals,
  added because Aviva's web filter isolates the site as uncategorised (see below).
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
- `fetch_inside.py` — "What's inside" breakdowns, staged to `work/inside.staged.json`. Runs after the
  asset mix in `refresh_daily.sh` and can never block prices; `promote.sh` shows a summary and copies it
  to `data/inside.json` with the month, or with `./promote.sh --allocation`.
- `watch_history.py` — the daily watch on already-published months. Runs on the days `month_ready.py` says
  there is no new month, re-derives the last 12 published months of both payloads from fresh prices and
  notifies if any figure moved. Reads only: it never stages, never edits, never publishes. Added 22 Sep 2026
  because a restatement was otherwise invisible until the next month end, up to four weeks later. Compares
  **rounded to 6 decimals**, as the payloads are written, or every figure differs in the 7th decimal.
  Tolerances differ by payload: `others.json` is derived from these same prices so it must reproduce exactly
  (1e-9), while the Aviva series came from the workbook's higher-precision prices (2e-4, the monthly overlap
  check's own tolerance). Verified: 1,152 figures reproduce with nothing flagged, and a deliberately altered
  month is caught and named.
- `fetch_others.py` — the other providers' funds, staged to `work/others.staged.json`. Runs after
  `fetch_inside.py` and can never block prices; `promote.sh` copies it to `data/others.json` only when its
  as-at equals the Aviva month, otherwise it is held back.

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

### The fetch sets its own date range, always

Both price fetches window the saved report before running it: **from 01/01/2001, monthly frequency
(`Frequency: 2`), to today**. `fetch_month.py` windows from a few months back, same anchor and frequency.
Never rely on the saved report's own range, and never hard-code an end date (`fetch_month.py` carried
`to = "2026-09-30"`, eight days from expiring when it was found).

The anchor day is what matters: a monthly range anchored on the 1st returns stamps on the 1st, and under
D+1 stamping those are month ends. On 22 Sep 2026 report 111322 came back anchored on the 5th (its saved
`FromDate` had become 05/01/2001), so every stamp was the 5th, `prices()` kept nothing and the run would
have stopped with "no month-end prices". Both fetches now also **stop on any stamp that is not the 1st**,
so a range change is reported rather than inferred. Verified: the monthly pull reproduces `others.json`
byte for byte, and all 4,996 live Aviva month-figures to within the 2e-4 tolerance (18 exceed it, all
Stewardship Ethical Equity before 2010, max 6e-4, old prices quoted to few decimals).

### Things that will bite

- **The spike check** (`fundfocus.month_end_spikes`, called by both price fetches before staging) pulls the
  daily prices around the month end and stops the run when a price moves more than 2% and hands back more
  than 2% the next business day. Tested: it names all five MyFolio Active funds on 01/09/2026 and flags
  nothing across four other month ends on both reports. Zurich Life Gold falling 2.9% that same day is not
  flagged, because it kept falling. It only examines the month being published, so it will not re-stop on
  August.
- **A bad month-end price is not hypothetical.** On 01/09/2026 the five Standard Life MyFolio Active funds
  printed about 5% below the 31/08 price and recovered the next day (Active I: 138.70, 131.60, 138.00). That
  stamp is August's month end, so the published August return for those five reads about -4.8% instead of
  about +0.3%, and their 5Y volatility about 0.4pp high. Found 22 Sep 2026 by checking a figure that looked
  wrong; it is the only such event in 15 months of daily prices across all 59 funds. A spike check (a
  month-end price that falls sharply and recovers the next business day) is not yet implemented. When the
  provider corrects the price, the "published months must not change" guard will stop the run: that
  correction is a deliberate override, not a reason to weaken the guard.
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

## All Funds tabs

Four tabs, in the user's order: **Aviva Portfolio Builder | Aviva Fund Explorer | All Funds Portfolio Builder |
All Funds Explorer** (the first two renamed from "Portfolio builder" and "Fund explorer" on 19 Sep 2026; the explorer
heading, toasts, notes and portfolio cards name the builder the same way). The All Funds pair is the same builder and the same explorer, not copies, over all 96 funds (37
Aviva range plus 59 from Zurich, New Ireland, Irish Life, Royal London and Standard Life; 15 Standard Life
funds were added to the reports by the user on 20 Sep 2026). The first two tabs read the Aviva
range only and are byte-identical to before the All Funds tabs existed (explorer table, note and count
verified against the published build). Built at the user's request; they will decide later whether it goes
public.

- **Data comes from two saved Fund Focus reports on the owner's account**: 111322 (daily prices) and 111323
  (AMC, "Risk Profile ESMA", Category). Adding a fund means adding it to **both** reports; nothing in the
  code lists funds. `fetch_others.py` stops if the two reports disagree, or if 111323's columns are not
  exactly Name, AMC, Risk Profile ESMA, Category.
- **Same conventions as `latest.json`**: month-end prices via `fundfocus.prices()` (D+1 stamping), grossed up
  geometrically by AMC, 6 decimals, no simulated history, `liveStart` the first priced month.
- **Royal London publishes 0.00% AMC.** By the user's decision their prices carry no AMC, so nothing is
  added back. Consequence to keep in mind: their portfolios show the lowest cost.
- **Providers are derived from the data, never listed in code** (`PROVS()`: Aviva first, then the distinct
  providers in `others.json`, alphabetical). Adding a provider to the Fund Focus reports gives it a chip and an
  entry in the explorer's filter with no code change. `fetch_others.py` still holds `PROVIDERS` as a **guard**:
  an unknown name prefix stops the run rather than inventing a provider (it fired on Standard Life, as intended).
- **Asset class, the user's rule, in this order:** "Gold" in the name → Alternative; name ending "Equities"
  → Equity (New Ireland PRIME Equities, iFunds Equities, both by the user's decision); category containing
  "Managed" or "Fund of Funds" → Multi-Asset; "Bond" → Fixed Income; "Equity" → Equity. An unplaced
  category stops the run. Standard Life's five **Global Index 20/40/60/80/100** sit in category "Specialist
  Funds", which no rule places; all five are **Multi-Asset** by the user's decision (`CLASS_SET_BY_OWNER`),
  including 100. The 10 MyFolio funds are placed by the "Managed" rule and carry published ESMA ratings.
- **ESMA:** published where Fund Focus has it. Otherwise, with 60 months, an indicative band from the
  fund's own 5-year volatility, `esmaSource: "calculated"`, shown with "≈" and a title (the four Royal
  London multi-asset funds). Two hand-set sources, both used only where Fund Focus publishes nothing, so a
  published rating always wins: **Irish Life Forum 3/4/5 take the band in their names** (`ESMA_FROM_NAME`,
  `esmaSource: "name"`, titled "Taken from the fund's name"), and the **PruFunds are set by the user**, Cautious 3
  and Growth 4 (`ESMA_SET_BY_OWNER`, `"owner"`, titled "Set by Slate Labs"), never calculated because smoothing
  makes their volatility meaningless. Neither shows "≈". Every one of the 81 funds now has a rating.
  **Overrides of published data**, at the user's request (19 Sep 2026): New Ireland Goodbody Dividend Income 6
  is **Equity** (`CLASS_SET_BY_OWNER`; Fund Focus says Managed Aggressive, so the rule made it Multi-Asset) and
  **ESMA 6** (`ESMA_OVERRIDE_BY_OWNER`, replacing a *published* 5). The published figure is kept as
  `esmaPublished` and named in the hover ("Set by Slate Labs; Fund Focus publishes 5"): an override of a
  provider's own rating is disclosed, never hidden.
- **Stops:** reports disagree, no prices, gaps, funds ending in different months, bad AMC, unknown provider,
  unplaced category, a fund disappearing, as-at going backwards, history start moving, a published month
  changing. All tested.
- **Client:** `MODE` "aviva" or "all", with separate `STATE_AVIVA` / `STATE_ALL`, so the two builders never
  share selections. `BF()` is the universe for the mode. Provider chips (`.pchip`, not `.tab`) appear only
  in the All Funds tabs. Cost there is each fund's **AMC** (`fundCost`), weighted, "not deducted"; the standard-fee
  control is hidden, since other providers have no standard fee. **No cost is shown in sections 1 and 2** of the
  All Funds builder (no picker tag, no Fund cost column, `holdCostTh` hidden and the total's colspan 4), and the
  **All Funds Explorer has no Fee vs standard column**, both at the user's request (19 Sep 2026). Section 3 follows:
  no Portfolio cost card (four cards, `.cards.four`) and no cost column in building blocks. Cost wording elsewhere is
  mode-aware: the section 2 heading drops "& cost" (`#secCost`), the growth legend reads "Gross of AMC", and the
  projection and performance-basis notes say no charges are deducted. **The disclaimer still carries the sentence
  "Portfolio cost figures are based on the standard portfolio cost entered by the user..."**, untrue on this tab;
  it is fixed legal text, so it waits for the user's disclaimer revision with the price-source sentence. The Aviva
  builder's markup is byte-identical to before apart from three ids.
- **Print and email work in the All Funds Portfolio Builder** (enabled 20 Sep 2026, once the disclaimer named Fund
  Focus as a source). They were disabled because both priced every fund as `stdFee + costAdj`, and a non-Aviva fund
  has no `costAdj`, so `1.00 + null` printed the standard fee as that fund's cost: a wrong figure, not a blank.
  Both are now cost-free in "all" mode, matching the screen: no cost column in the print composition and building
  blocks tables (and their colgroups), no Portfolio cost key figure (`.pd-kpis.four`), no standard cost in the
  print sub-header, no Cost p.a. column or cost stat cell in email (stat cells 25% wide instead of 20%), and the
  print methodology says no charges have been deducted. Verified: header and row cell counts match in every table,
  no cost figure survives anywhere, page 1 still fits and a 5 + 5 still runs to 3 pages, and the Aviva print and
  email output is byte-identical.
- **Asset mix and What's inside** cover only Aviva and Dimensional. A portfolio holding other funds says
  so; an other-provider fund's card shows AMC and ESMA and says no breakdown source is available.
- **`others.json` must end in the same month as `latest.json`**, or `mergeOthers()` drops it and the tab
  says why. A missing or malformed file leaves the Aviva range working (verified).
- **All Funds Explorer:** all 81 funds, plus a Provider filter (portfolios hidden when a provider is chosen;
  the filter is hidden in the Fund explorer). It has no Fee vs standard column, the standard fee being Aviva's
  alone. Its portfolio rows and Add to buttons are the All Funds Portfolio Builder's.
  Each explorer keeps its own state (`X_AVIVA` / `X_ALL`: filters, search, sort, ticks, compare view);
  `showTab()` sets `MODE`, `state` and `X` together for every tab.
- **Verified:** all 6,503 returns re-derived from the raw report; 484 explorer cells match Python; the
  Aviva builder (17 sections, three scenarios) and all 37 Aviva explorer rows byte-identical to before.
- **Before it goes public:** data licence scope with Longboat/CSS for non-Aviva funds, the disclaimer
  revision, and the outside interests question.

## Asset mix

The allocation-weighted asset mix of each portfolio, at **portfolio level only**: a doughnut of
the six asset classes with a two-column table beside it (asset class, % held). Screen sits after
building blocks, print after composition (static doughnut, A and B side by side), email is the
table only. Hovering, tapping or focusing a segment or table row names it in the ring's centre.

No per-fund breakdown is shown, by the user's decision. A richer view was explored (regions,
bond types, countries, sectors, look-through holdings) and rejected as not intuitive: the
underlying labels are inconsistent across providers, capped at ten lines, and for multi-asset
funds published for the whole fund rather than per asset class. Do not reintroduce it without asking. Data lives in
`data/allocation.json`, deliberately separate from `latest.json`: it has its own sources and
dates, and keeping it apart leaves the price payload, `check_data.py` and reconciliation untouched.

```
python3 fetch_allocation.py      # fetch, check, stage to work/allocation.staged.json
./promote.sh --allocation        # publish asset mix on its own, after review
```

`refresh_daily.sh` also runs the fetch when it stages a new price month, and `promote.sh`
publishes a staged asset mix alongside the month. An asset mix failure never blocks prices.

### Sources, both public and unauthenticated

- **Aviva (31 funds):** `GET aviva-fundcentre.longboatanalytics.com/api/FactsheetData/GetFactsheet?fundId=N`,
  the `Asset` block, FundIds from `fund_map.json`. Labels arrive HTML-escaped.
- **Dimensional (5 funds):** `POST etf.dimensional.com/public/v2/fundcenter/funddetail`, header
  `x-selected-country: FI`, body `{"portfolioNumber":N}`, lens slug
  `charsMixedAssetClassWithEquityRegionAllocation`, weights as fractions. Portfolio numbers,
  mapped by ISIN and checked against the rendered pages: 20/80 = 885, 40/60 = 746, 60/40 = 748,
  80/20 = 879, World Equity = 626. The web page asks for a professional-client declaration and
  cookie consent; the API needs neither, and neither has been accepted on the user's behalf.
- **Aviva Physical Gold** publishes no mix. It is classified as 100% gold (user's decision), the
  only hand-set record, shown as "Gold 100%" at fund level.

### Rules

- **Six classes:** Equities, Fixed Income, Cash, Property, Alternatives & Commodities, Other.
  **Displayed as "Alternatives"** everywhere (screen, print, email) via `AC_LABEL`, because the full
  name wrapped in print and made that row taller than the others. The data key in
  `allocation.json` and `AC_CLASSES` stays "Alternatives & Commodities", so no refetch was needed.
  Wherever a held fund has any, the asset mix note adds "Alternatives includes commodities and gold".
  The roll-up stops at asset class on purpose. Aviva's equity labels cannot be split into
  developed and emerging: "Pacific Basin Equities" is Taiwan/Korea/China in the EM index fund and
  developed Pacific elsewhere. Do not add a developed/emerging split without solving that.
- **Every label is mapped explicitly** in `CLASS_OF`. An unmapped label stops the run: a new
  Aviva category must never fall quietly into Other.
- **"Securities" is not an asset class.** Stewardship Ethical Equity publishes its whole mix as
  "Securities 99.3%". Generic labels resolve from the factsheet's declared `AssetClass`; an
  unrecognised one stops the run. Mapping it to Other was the original bug.
- **Per-fund check, then scale.** Each fund's published total must be 100 ± 1%, then it is scaled
  to exactly 100 (`scaledFrom` keeps the original). This replaced a portfolio-level 2% coverage
  rule at the user's request. Coverage of all dashboard funds is required; a missing fund stops
  the run. The dashboard's shape check rejects any fund not totalling 100.00.
- **Portfolio mix is a plain weighted average.** Every fund totals 100, so the portfolio does too.
- **Negative weights are kept, not clamped** (AIMS Target Return publishes Other -0.26%). The
  doughnut draws positive classes only; the table shows the signed figure.
- **Dates are labelled, never harmonised.** Providers publish on different month ends (Aviva
  30 Jun or 31 Jul, Dimensional 31 Aug at the time of writing). One date reads "Asset mix as at";
  several read "mixed month ends" and list them. Allocation dates are independent
  of the price as-at. A date going backwards stops the fetch.
- **It is a snapshot.** Say so wherever it appears: it does not describe how funds were invested
  over the performance window.
- **Non-fatal on the client.** `loadAlloc()` runs in parallel with the price fetch; any failure
  leaves `ALLOC` null and the section reads "Asset mix unavailable". No other figure depends on it.

### Colours

`--ac1`..`--ac6` (light and dark) on screen, `AC_FIXED` literal hex for print and email. A third
palette, separate from `--d1`..`--d5` (fund identity) and from `--signal`. `acDonutSVG()` draws
both the screen and print doughnut; print passes literal hex. It is SVG so it prints with
background graphics off. A single class at 100% is drawn as two half-arcs, since one arc with
coincident ends renders nothing. Email uses a filled swatch cell per row because Outlook cannot draw SVG.

## Fund explorer tab

A second view beside the builder: tabs **Portfolio builder | Fund explorer** under the header
(`.apptabs`, last tab remembered in `localStorage` as `apb-tab`). It researches the 37 funds rather
than building a portfolio, and reads the same `DATA`, so the monthly refresh needs nothing extra.
Agreed with the user in three stages: 1 the fund table (built), 2 a compare screen with line and
drawdown charts for up to 5 ticked funds, 3 optional extras they choose from (per-fund asset mix,
stress episodes, correlation table, rank in asset class, add to portfolio).

- **Table columns:** fund, add to, asset class, ESMA, fee vs standard, 1M, 3M, YTD, 1Y, 2Y/3Y/5Y/10Y p.a.,
  Vol 5Y, Max DD 5Y, plus an optional cumulative custom period column. Launched and since launch p.a. were
  removed and max drawdown moved from since launch to 5 years at the user's request (19 Sep 2026), so Vol and
  Max DD share one basis, the same 60 months, both flagged ◆ when those months include simulated history.
  Max DD 5Y matches the compare screen's own Max DD 5Y for all 37 funds and an independent Python check.
  Asset class filter, name search, sort by any heading (blanks always last), and an end month that
  recalculates every figure.
- **ESMA filter** is a dropdown straight after the asset class chips (user's placement). It lists only
  the ratings some row actually has, each with its row count ("4 (13)"), so no choice produces an empty
  table, and it combines with asset class and search. It filters on the figure shown in the ESMA
  column: a fund's published rating, or a portfolio row's own 5-year band.
- **Fee vs standard replaced the AMC column** at the user's request: the fund's charge above or below
  the standard fee (`costAdj`), rendered exactly as the builder's fund picker renders its `.costtag`
  (`+0.25%` in `--neg`, `−0.10%` in `--pos`), and **blank on the standard fee** so only the funds that
  differ draw the eye. 17 of 37 funds are standard. A portfolio row shows its allocation-weighted
  difference. Verified cell by cell against the picker's own tags.
- Period columns 1M to 10Y follow the builder's `fundPeriod` convention exactly,
  including its ◆ rule (`from < liveIdx`), so a fund's figures agree between the two tabs.
- **Portfolio A and B appear as rows**, because to this table a portfolio is exactly what a fund is: a
  monthly return series with a start month. `portfolioFund(k)` wraps `series(k, cs, END())` from the
  common start of its holdings in a fund-shaped object, and `xFunds()` is the combined list every
  explorer read goes through, so rows, tick pruning, the count and the compare screen all agree.
  Nothing is recomputed: the explorer's figures for a portfolio match the builder's own cards to full
  precision (verified), because both read the same `series()`.
  - Category Multi-Asset, badged "Portfolio", pinned to the top of the default sort but ranked among
    the funds as soon as a column heading is clicked, which is the point of having them there.
  - `liveIdx` is the **latest** live start among the holdings, so a month counts as simulated while any
    holding still is, which is what `series()` already flags.
  - **ESMA is the band for the portfolio's own volatility over the same 5 years as its Vol 5Y cell**, so
    the row is self-consistent; it is path-based like the builder's and indicative, since regulatory
    SRRI uses a fixed basis. **Fee vs standard is the allocation-weighted `costAdj`** of its holdings,
    which is what that column means, not `wCost()`.
  - Only a portfolio whose allocations total 100 has a series, so only a valid one appears. Emptying or
    unbalancing it in the builder removes the row and its tick on the next render, and compare falls
    back to the table when the last tick goes. A single-fund portfolio reproduces that fund's row
    exactly (verified).
- **Add to portfolio** is a non-sortable "Add to" column holding an **A** and a **B** button, placed
  immediately after the fund name (Stage 3, first extra; placement chosen by the user from a mockup).
  It never guesses a destination: both portfolios are always offered, since a fund landing in the wrong
  one is a silent, expensive mistake, and adding to B is also how B is started.
  - **The fund lands unweighted, at 0%**, by the user's decision: the code pushes the name and sets no
    allocation, exactly what the builder's own `toggleFund` does, so weights already set are never
    overwritten and no figure moves. Re-splitting equally was rejected: it discards the weights the
    user chose. A valid portfolio therefore stays valid and its explorer row does not change.
  - **It does not switch tabs**, at the user's request, since several funds are often added in one
    visit. An `.xtoast` confirms each add, names the portfolio, says the weight is 0%, and says when
    that portfolio has just become full.
  - **The same button takes the fund back out**, at the user's request, so a mistake is undone where it
    was made. Held reads ✓A and flips to ✕A on hover or focus, in the negative colour, so a removal is
    never a mystery click. Removing does what `toggleFund` does (drop the name, delete the allocation)
    and the toast offers **Undo**, which restores the fund at its original position with its original
    weight: removing a weighted fund loses that weight and drops the portfolio below 100%, and the
    toast says so, naming the new total. Adding offers Undo too.
  - Only "full at five" disables a button, and it carries the reason in `title`. A held button stays
    live even when its portfolio is full, since removing is how you make room. Portfolio rows carry no
    buttons at all.
  - **Ticks and holdings are separate**: the tick box means compare, and adding never ticks, nor the
    reverse. Verified, along with the builder, its picker, print and email staying byte-identical.
- **What's inside** closes the compare screen: one card per selection, built at the user's request after
  a coverage review of all 37 factsheets (country coverage was measured by how much each list *names*,
  since every list totals 100% only because of its "Other" row).
  - **The breakdown follows the asset class**, set by hand per fund in `KIND` in `fetch_inside.py` (a
    fund with no kind stops the run): equity = country, sector, top 10 (Aviva names 88% to 98% by
    country, Dimensional World Equity all of it); government bonds = issuer country, top 10, duration,
    yield; corporate bonds = bond type, issuer country, top 10, duration, yield; cash = duration and
    yield only; property = type, location, top 10 properties, properties, yield, lease, vacancy;
    multi-asset (including Concept K and the Dimensional allocation funds) = the existing asset mix from
    `allocation.json`, or `aggregateAssetMix` for a portfolio row; AIMS Target Return = no breakdown,
    with the reason (its split is 82% cash while its returns come from derivative positions); Physical
    Gold = 100%.
  - **Rejected, do not reintroduce without asking:** Aviva's region labels ("Pacific Basin" is 70% of both
    emerging markets funds and means Taiwan, Korea and China); country for multi-asset funds (Aviva names
    only 30% to 91%, the rest "European Union", "North America", "EUR", "Other"); holdings counts
    (Global Emerging Market Equity shows 2, being a fund of funds).
  - **Every card has the same frame**, at the user's request: header 38px, figures strip 50px, tabs 26px,
    ten row slots 200px, reconciliation line 16px, so a row of mixed funds lines up. A fund with several
    breakdowns switches between them with tabs (`.xin-t`, choice kept in `X_INTAB`) instead of stacking
    them. Verified: all 37 funds and both portfolios, in every tab, render at 392px with identical zones
    and nothing overflowing.
  - **Figures are never changed.** Rows are ordered largest first with Other/Cash/Unclassified last and
    grey; past ten rows the smallest are grouped as "Other (N more)" (only Dimensional World Equity,
    46 countries). The grey line under each list reconciles it ("8 countries 97.6% + Cash 0.7% + Other
    1.7% = 100.0%"). Only labels are tidied: sector names made consistent (explicit `SECTOR` map; an
    unknown label stops the run), Global Smaller Companies' ISO country codes shown as names (an
    unknown code stops the run), all-capitals holding names shown in normal case. In an asset-mix card
    "Other" is a real class and keeps its colour.
  - **Checks in the fetch:** each list totals 100% +/- 1% as published, top holdings are 1 to 10 valid
    weights, required figures (duration, yield, property facts) are present and numeric, and as-at dates
    never go backwards. All proven to stop the run. The dashboard re-checks shape and totals
    (`validInside`) and, on any failure, each card says "Breakdown unavailable" at the same size while
    multi-asset cards still draw from the asset mix.
  - **Verified** against the raw factsheets fetched independently: all 35 lists and every figure match
    exactly; every rendered row matches the file; portfolio cards match `aggregateAssetMix`. The builder,
    print, email, the explorer table and the rest of the compare screen are byte-identical.
- **Screen only**, by decision: no print or email version, and both are hidden in print.
- **One disclaimer:** the `.disc-wrap` node is moved into whichever tab is open, never duplicated,
  so the fixed legal text still has a single source.
- **Display names** strip Dimensional's "Fund EUR Acc" tail (`xName`) so every name fits one line
  and rows stay equal height; the full name is the cell's `title`. The builder's `short()` is unchanged.
- **Verified:** all 444 cells at Aug 2026 (with a custom period) and 407 at Dec 2025 match an
  independent Python calculation; the builder, its print and email are byte-identical to before.

**Stage 2, compare screen (built).** Tick up to `X_MAX` = 5 funds in the table, then Compare.
- **Every selected fund is measured over the same months.** The window ends at the table's
  "Performance to" month and starts no earlier than the latest first month among the selected funds.
  1Y/3Y/5Y/10Y clamp to that shared start and say so; Max is the shared start; Custom picks From/To.
- **Shows:** growth of €10,000 and drawdown charts (the builder's `growthChartSVG` / `drawdownChartSVG`,
  fund colours `SEG` in tick order), a performance table, and calendar years (10 full years plus
  YTD to the end month, ◆ hanging in the cell padding as in the builder).
- **Compare charts use their own style** (`XCHART`): no area fill, 8px axis and 8.5px semi-bold value
  labels (the print styling, at the user's request, since the full-width SVG scaled 10px text to about
  15px), 1.3px lines (`th.lw`, default 2) and an x axis line (`th.axisLine`). The drawdown axis also
  stops at zero (`th.noPosAxis`): nothing is ever plotted above it, so a positive tick wasted height.
  The builder's charts set none of these flags and are verified byte-identical.
- **Worst falls are on hover, never printed on the chart.** Each fund's lowest point carries a marker
  (`th.troughDots`): a 5.5px disc ringed 2px in `th.halo`, the chart's own ground, so it stays findable
  where several lines cross it, plus an invisible 11px disc as the hover target. `bindDDMarkers()`
  shows a positioned tooltip (fund, worst fall, month) on hover or keyboard focus, and grows the disc
  to 7px. Three earlier attempts were rejected by the user in turn: labels beside the troughs, then
  right-margin labels joined by leader lines, then a "Worst fall" legend line under the chart. The
  worst points cluster in the same months, so anything drawn on the chart overlaps. Do not reintroduce
  any of them. Position the tooltip from `getBoundingClientRect`: SVG elements have no `offsetLeft`,
  and the resulting `NaN` pins the tooltip to the corner. Each marker also has an SVG `<title>`.
- **The growth chart's €10,000 line is a plain grid line** on this screen (`th.plainStart`), not
  dashed and emphasised, at the user's request. The builder's growth chart and the projection chart
  keep their dashed reference lines.
- **The growth chart's amount is editable** (`#xAmt`, `xAmtVal()`, default €10,000, clamped to €1 to
  €1bn), following the euro-input rule: text input, commas on change, read through `numVal`. The
  subhead follows it. It is the compare screen's own amount and does not touch the builder's
  investment box.
- **Each end label carries the rate per year** beside the amount, separated by a dimmed `|` and set in
  a lighter `tspan`, with the right margin widened for it (`th.padR`, default 84, compare passes 134). A window under 12 months shows
  the amount alone, since annualising a part year misleads. The rate is `(end/amount)^(12/months)-1`,
  which reproduces the performance table's own p.a. figures exactly (verified at 1Y, 3Y, 5Y, 10Y).
- **End labels are stacked in value order** (`th.endStack`): each starts level with its own end point,
  is moved only far enough to clear its neighbour by 12px, and gets a short connector in its own colour
  only if it moved. The old rule stacked in tick order and pushed a label 13px down per collision, so
  two funds ending €5 apart (€15,276 and €15,271) sent the second label below a third fund's label,
  nowhere near its line. Sorting by value is what guarantees labels and lines share an order and cannot
  cross. The builder's chart does not set the flag and is verified byte-identical.
- **Screen order, top to bottom** (user's order): period and amount controls, fund legend, then
  **Performance** (bar chart and table), then growth, drawdown, calendar years. The period buttons stay
  at the top because they drive both the charts and the table's Vol/Max DD basis. The "Measured over
  <months>" note sits under the growth heading, not above the performance section: it describes the
  charts' shared window, while the performance section uses standard periods, and above it the note
  would have read as describing the wrong figures.
- **A performance bar chart sits above the performance table**, under the same heading, at the user's
  request: YTD, 1Y, 3Y p.a., 5Y p.a., 10Y p.a., one bar per selection in tick order (`xBarChartSVG`, the
  compare screen's own function; the builder's `barChartSVG` is untouched). Its figures are the table's
  own `xRow` values, verified label by label. A selection without a period reads "n/a"; a period no
  selection reaches is left out.
  - **Labels never overlap, including at five selections.** With five, each bar is about 21 units wide,
    narrower than a flat "-12.3%", so labels turn upright whenever a flat one would spill into the next
    bar. The width is measured with canvas `measureText`, plus 12% for the web font still loading: a
    character-count estimate misjudged "%". An upright label is only as wide as the type is tall, so it
    stays inside its own bar's slot. Verified across 69 fund combinations of two to five: no label
    overlaps another, sits on another fund's bar, crosses a category label or leaves the chart.
  - **The chart is sized to the selection** (`xBarSize`), at the user's request: one or two funds had
    looked like blocks stretched across the page, and a width cap (slim bars adrift in the full width)
    was previewed and rejected. The canvas is 360 to 760 units wide, chosen so each bar lands near 34
    units, and its container gets the matching share of the page, so type and bars render at exactly
    the size of the full chart (verified: period labels 17px on one fund and on five). Roughly: one fund
    47% of the width, two 64%, three 94%, four and five the full width and byte-identical to before.
    Fewer periods (no 10Y) narrow it further. The container never drops below 440px, or 100% of a
    smaller screen. One fund is also drawn 190 units tall rather than 250, at the user's request, and
    its bars take 60% of each period rather than 42%. Verified across 73 one-to-three-fund charts: no
    label overlaps, sits on another bar or leaves the chart.
  - Labels are 7.5 units (about 11.5px on screen), in the fund's colour, above positive bars and below
    negative ones. The axis starts at zero when nothing is negative; niceAxis otherwise adds an empty
    band below zero.
- **The performance table uses the main table's standard periods** (1M to 10Y), built with the same
  `xRow`, so a fund reads identically on both screens. It replaced a chart-period
  return/volatility/best/worst month table at the user's request. Since launch p.a. is deliberately
  absent here though the main table carries it: the user found it confusing beside the charts' fixed
  period. Columns are equal width from a `colgroup`, as in the calendar table; before that the long
  "Max DD since launch" heading widened its column and pushed it out of line.
- **Volatility and max drawdown on the compare screen are 5 years by default, 10 when 10Y is the
  selected period and the shared history reaches back that far** (the heading names the basis, e.g.
  "Vol 10Y" / "Max DD 10Y"), at the user's request. A clamped 10Y falls back to 5Y, and a fund whose
  own history is shorter reads "—" rather than a different period inside the same column. This is a
  third basis alongside the two in Locked methodology: the main explorer table is fixed at 5 years for both,
  and the builder keeps its own. Do not unify them.
- `growthChartSVG` takes an optional `th.amt`; the explorer passes 10000, and the builder still reads
  its investment box, verified byte-identical.
- **Class names are the explorer's own** (`.xwbtn`, `.xchip`, `.xpick`): the builder binds click
  handlers to `.wbtn` and `.tab` globally at load, so reusing those classes would wire explorer
  buttons to the builder's state.
- **Back** returns to the table with filters, sort and ticks intact.
- **Showing the builder tab re-runs `equaliseBBRows()`.** If the builder renders while the explorer
  is open (e.g. when data arrives), its hidden rows measure 0 tall and get no equal height.
- **Verified** against independent Python: every compare figure, the ◆ flags and the €10,000 end values
  at 5Y and at a clamped 10Y, plus all 44 calendar cells.

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

## Hosting and being recognised by web filters

**Aviva's network isolates the site as uncategorised** ("Web_Isolation_View_Only"), which makes it
view-only and so unusable, since the tool needs typing. Only Aviva IT can lift that, through the IT
Self Service Portal. Do not suggest workarounds (hotspot, VPN, another address): the github.io address
redirects to the custom domain anyway, and a workaround turns an allow-list request into a conduct
question. The author is an Aviva employee asking to use their own product on Aviva's network, so the
outside business interests policy is the other half of that request.

The site now carries the signals categorisers look for: a page description and canonical and Open Graph
tags, `robots.txt`, `sitemap.xml`, `/.well-known/security.txt` and an About page naming the operator,
the data sources and a contact. **`security.txt` has an `Expires` date and must be renewed yearly.**
`.nojekyll` is required or GitHub Pages will not serve the `.well-known` folder. **Search engines are registered** (17 Sep 2026): Google Search Console holds a *domain* property
(covers www and apex), verified by DNS, sitemap submitted and read successfully, both pages found;
Bing Webmaster Tools holds https://www.portfoliobuilder.cloud/, verified by DNS, sitemap submitted.

**DNS records that must not be deleted**, all in Hostinger (nameservers `*.dns-parking.com`, DNS
managed there, the site's A and www CNAME records point at GitHub Pages):
`google-site-verification=...` TXT at the root and the `d8d77...` CNAME to `verify.bing.com` keep
those verifications alive; the two `improvmx.com` MX records, the `v=spf1 include:spf.improvmx.com
~all` TXT and the `_dmarc` TXT run the mail side.

**hello@portfoliobuilder.cloud forwards to the owner's inbox** through ImprovMX's free tier (chosen
over Cloudflare Email Routing, which would have moved DNS off Hostinger, and over a paid Hostinger
mailbox). Hostinger itself offers no forwarding on a domain-only account. ImprovMX also created a
catch-all `*@` alias. Receiving only: replies come from the owner's own address, and DMARC `p=reject`
would block sending as the domain until that is set up properly.

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
  A "Diversification reduced volatility by…" banner under the summary cards was removed at the
  user's request. It compared actual volatility with the weighted average of the funds' own
  volatilities and called that "if the funds moved independently", which is wrong: a weighted
  average of volatilities is the perfectly correlated, lockstep case. Independent funds would sit
  *below* the actual figure. It was also small for typical portfolios (about 0.5pp) and cluttered
  comparison mode. The risk contribution table shows the effect better. Do not reintroduce it with
  that wording.
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

**Simulated history wording** (`SIM_METHOD`, one definition used by screen, print and email): the
pre-live months are "derived from the index, or blend of indices, that the fund is designed to
track over the same period". The blend clause is deliberate: of the 10 funds with simulated
history only 3 are single-index trackers (Emerging Markets Equity Index, European Equity ESG
Passive, Global Equity ESG Passive); the other 7 are multi-asset (Fixed ESG 20–80, Multi Asset ESG
Passive Plus 3–5), where a single underlying index would be wrong. The user confirmed on
12 Sep 2026 that the simulated series are index derived, which is what the wording rests on: it
cannot be verified from the payload, since a simulated month is just a return like any other.
This is methodology text; the regulatory disclaimer's own simulated-performance sentence is
separate fixed text and was not touched.

Stress episodes are GFC (Nov 2007 to Feb 2009), Q4 2018 selloff (Oct to Dec 2018), Covid crash
(Feb to Mar 2020) and the 2022 bond selloff (Jan to Oct 2022). Q4 2018 was added because GFC is n/a
for most portfolios: only 15 of 37 funds reach 2007, while 35 of 37 cover late 2018. Candidates that
vanish at month-end resolution (Brexit, Mar 2023 bank stress, Aug 2024 yen unwind) or duplicate an
existing episode (the 2022 gilt/LDI crisis, inside 2022) were rejected.

**Worst periods** are two extra rows *inside* the stress episode table (Episode / Period / Return),
at the user's request, with max drawdown and recovery shown as "—" because neither applies. They
show the lowest compounded return over any 3 and 12 consecutive months across the portfolio's full
common history, not the selected window. Their dates always sit in the Period column, so every row
is one line tall (dates under each return made those rows double height). In comparison mode
`worstPeriodCell()` shows one range when A and B share the same worst window, and otherwise both,
labelled A and B in their portfolio colours with a compact range ("A Apr–Jun 2022 · B Jan–Mar 2020").

**In comparison mode the stress table shows return only** (Episode / Period / A return / B return),
at the user's request: with Max DD and Recovery for both portfolios it ran to eight columns and
wrapped the episode names. Max drawdown and recovery are kept for a single portfolio, and the
comparison note says so. Same rule on screen and in print. A 3-year window was evaluated and dropped
at the user's request: for post-2016 portfolios the worst 3 years is usually a gain, which reads as
an error under "worst". Being data-driven it may date the 2025 tariff months; it names no event, so
the exclusion above still holds.

**Calendar year returns** cover the last 10 full years plus YTD (January to the data month). A year
the common history does not fully cover is n/a, never a part year shown as a calendar year.

## Conventions

- **The ◆ never takes horizontal space in a figure cell.** An inline `" ◆"` is about as wide as a
  digit, so a marked figure sat up to 11px left of the unmarked ones in its own column (measured in
  building blocks). Every numeric cell now appends a zero-width superscript span instead: `.simd` on
  screen, `.pd-dia` in print, which the print calendar already used. The two calendar tables keep
  their own rule pinning it to the cell's right edge, which suits their fixed layout. Alignment is
  verified by measuring the right edge of the digits alone, excluding the marker, across the calendar,
  stress, building blocks, explorer, compare and print tables. **Name cells keep the full-size
  `.simmark` ◆** (they are left-aligned, so nothing is knocked out of line), and email keeps the
  inline ◆ because Outlook's Word engine cannot position a span.
- European date formats, euro by default, en-IE locale.
- `niceAxis()` sizes its step from the span **including the anchor**, not just `mx-mn`. With a
  projection fully depleted by withdrawals every value collapses to zero, the spread is nil, the step
  falls back to 1% of the anchor and the axis draws ~100 labels on top of each other. It also refuses
  to return more than 14 ticks. The projection chart then floors its axis at zero, since a portfolio
  value cannot be negative. **The projection axis covers only what is drawn**: Portfolio A's
  5th–95th band and, in comparison mode, B's median line, each at its highest point across all 20
  years. It previously included B's 95th percentile, which is never plotted, so a volatile B pushed
  the axis to €2m while nothing on the chart passed €750k. Using the peak over all years rather
  than year 20 matters under withdrawals, where the band peaks early. Growth, drawdown and rolling volatility are unaffected: verified by
  identical chart output before and after, in both the 5Y and Max windows.
- Euro amount inputs (investment, monthly contribution, monthly withdrawal) are `type="text"` with
  `inputmode="numeric"` so they can display thousands separators ("100,000"), reformatted on change.
  Always read them through `numVal(id)` / `amtVal()`, which strip the commas. A bare
  `+el.value` on "100,000" is `NaN`, which silently falls back to the default amount.
- Fund picker category order is fixed: Multi-Asset, Equity, Alternative, Fixed Income.
- Print document is A4 portrait, sections wrapped in `.pd-sec` with `break-inside: avoid` so
  a section never splits across pages. Screen disclaimers are always visible and hidden in print.

## Print document — factsheet layout

Chosen by the user over a tidied flow and a cover-page report. **Page 1 is the whole story**:
key figures, composition, asset mix, growth and drawdown charts, performance by period. **Page 2**
is building blocks (A and B), stress episodes, notes and methodology, and the disclaimer. Normal
selections print on 2 pages; a 5 + 5 comparison runs the disclaimer onto a third.

- **`layoutPrintDoc()` measures, it does not estimate.** It renders the document off-screen at the
  printed width (703px = A4 less 12mm margins), levels the chart column with the left column, then
  moves optional content off page 1 in a fixed order until it fits (single: building blocks, then
  the ESMA scale; A and B: asset mix), then spends spare room on stress episodes, then the bar
  chart. Fund names wrap unpredictably, so every estimate-based version left gaps or overflowed.
  That is why the `.pd-*` styles sit **outside** `@media print`: they must apply on screen to be
  measured. Only `@page`, the canvas background and hiding the app stay inside it.
- **Charts take `W`/`H`** (`barChartSVG`, `growthChartSVG`, `drawdownChartSVG`) so print draws them
  at true column width and their type prints at the size written. Screen calls use the defaults.
- **Print charts use the `PRINT` theme** (`LIGHT` plus label sizes): 8px axis labels, 8.5px
  semi-bold value labels, no bold on the €100,000 / 0% reference labels, at the user's request, so
  chart type sits with the 8.5px table text. With `inside:true` the growth end value is drawn inside
  the plot, above-left of the end point, so growth and drawdown need no reserved right margin and
  share padding, which keeps their date axes aligned. Lines are drawn before labels. When A and B end
  close together the second label sits left of the first on the same baseline rather than dropping
  into the lines. The dashboard's charts keep `DARK` and are unaffected.
- **Footer is CSS page margin boxes** (`@bottom-left` / `@bottom-right`, page x of y). Defining them
  suppresses Chrome's own header and footer (date, title, localhost URL), verified with that option on.
- **Nothing relies on "Background graphics"**, which is off by default: swatches, the product tile
  and the ESMA scale are SVG, and table headers are rules, not filled bars.
- **Print forces a light canvas** (`html` background and `color-scheme`). In dark theme the page
  margins otherwise print dark navy whenever backgrounds print, which also makes right-aligned
  text look clipped.
- **The print button waits** for fonts (so measuring is right) and for the wordmark image to decode.
  Printing straight after `innerHTML` dropped the SLATE LABS wordmark from the page.
- The disclaimer block is lifted verbatim from the previous build; methodology changed one phrase,
  "portfolio summary cards" to "key figures".
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
