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

**It waits for the network before it concludes anything.** launchd fires the job when the Mac wakes, which
at 14:30 is often before wifi has associated, and a DNS failure then is not news about the data. The script
tries the public price endpoint five times over two minutes first. A day on which nothing could be checked
increments `work/silent_days` and stays quiet; three consecutive such days notify, and so does every third
day after that, because the thing worth knowing is not one offline afternoon but a watch that has stopped
running. Any day that does check clears the counter.

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
- `correct_month.py` — the controlled way to accept a provider restatement of an already-published month,
  built 22 Sep 2026 so that taking one is as reviewed as a normal refresh. `python3 correct_month.py 2026-09`
  shows what would change and stages nothing; `--stage` writes `work/correction.*.json`, and
  `./promote.sh --correction` shows the differences again, asks, then copies to `data/`, refreshes the dated
  archive copy and publishes. It stops on: a month that is not the latest published one (the dated archives
  would disagree), a fund appearing or disappearing, a missing price, a stamp that is not the 1st, a
  **month-end price that still spikes** (a correction must never import another bad print, and `--force` does
  not override this), and any per-fund change above 5pp unless `--force` is given. Only the named month is
  ever touched. Verified against a simulated restatement of two Aviva funds: it found those two and nothing
  else, the review step cancelled cleanly, and both payloads restored to their original checksums.
- `watch_history.py` — the daily watch on already-published months. Runs on the days `month_ready.py` says
  there is no new month, re-derives the last 12 published months of both payloads from fresh prices and
  notifies if any figure moved. Reads only: it never stages, never edits, never publishes. Added 22 Sep 2026
  because a restatement was otherwise invisible until the next month end, up to four weeks later. Compares
  **rounded to 6 decimals**, as the payloads are written, or every figure differs in the 7th decimal.
  Tolerances differ by payload: `others.json` is derived from these same prices so it must reproduce exactly
  (1e-9), while the Aviva series came from the workbook's higher-precision prices (2e-4, the monthly overlap
  check's own tolerance). Verified: 1,152 figures reproduce with nothing flagged, and a deliberately altered
  month is caught and named.
  **Exit 0 nothing moved, 1 a figure moved, 2 the check could not be made**, and `refresh_daily.sh` keeps
  those apart. Before 6 Oct 2026 it caught only `FundFocusError`, `KeyError` and `ValueError`, so any
  connectivity failure died in a traceback and the caller read every non-zero exit as a restatement: seven
  runs between 24 Sep and 5 Oct announced that published history had moved when the Mac had simply been
  offline at 14:30. An alert that cries wolf is an alert nobody reads. `month_ready.py` exits 2 the same way.
  All four outcomes tested, including a real restatement (exit 1) and a real clean run (exit 0).
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
  wrong; it is the only such event in 15 months of daily prices across all 59 funds.
  **CSS restated it on or before 6 Oct 2026**, and everything downstream behaved as designed: the 01/09/2026
  stamp now reads 138.70 for Active I, with no dip and no recovery, `fetch_others.py` stopped on "1
  already-published month(s) changed value, first at 2026-08" and staged nothing, and the watch named the
  five funds and nothing else. Restated August runs +0.31% to +1.36% against the published -4.82% to -3.73%,
  which puts the five back in line with the unaffected MyFolio Market funds (+0.43% to +1.82%) and matches
  the +0.3% predicted for Active I on 22 Sep. September then reads -1.78% to -0.12% rather than the +3.52% to
  +5.16% a bad denominator gave. Taking it needs `correct_month.py 2026-08 --force`: the move is 5.09pp to
  5.13pp and the 5pp guard is doing its job, so **say why in the commit** rather than treating `--force` as
  routine. The guard is not the thing to weaken; the evidence is what clears it.
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

## Income sustainability tab

The last tab, built 23/24 Sep 2026 (fifth until My Fund Lists was put before it on 10 Oct at the user's request). It answers whether an income lasts, which
none of the other tabs do. Screen only, hidden in print, and it carries the warnings block like the others.

- **Selections are any fund and any valid portfolio from either builder**, up to three, labelled
  "Portfolio A · Aviva Portfolio Builder" and so on (user's decision: both builders, not just the one the
  tab sits beside). `iPortfolio()` points `MODE`/`state` at the right builder for one call and restores
  them, so a portfolio's series is the builder's own `series()`, never a second implementation. The tab
  therefore owns no mode, and `showTab()` deliberately leaves `MODE` alone for it.
- **Engine:** the projection chart's own maths, GBM fitted to each selection's whole history, 2,000 paths,
  monthly steps, fixed seed. The draws are generated once (`iDraws`) and reused by every run, which changes
  no figure and is what makes the sensitivity runs and the income solver affordable.
- **It deducts the charge entered**, alone in the tool. A sustainability figure computed gross would be
  wrong rather than conservative. The notes say so; the disclaimer stands unrevised at the user's decision,
  since the underlying fund performance data is still gross.
- **The card carries everything**, in the user's order (25 Sep 2026): sustainability with a bar, central
  forecast, the 90% range (5th to 95th, hidden when more than 5% of runs end empty, since every low
  percentile is then zero and an upper bound alone says nothing), what happens to the income in the worst
  5% of outcomes, the income that clears 90% (bisection on the same paths), sustainability at 1pp and 2pp
  lower returns, the stressed scenario when it is switched on, and the calibration in small print. The
  "Behind the figures" table that briefly held the last three was removed: the stress toggle appeared dead
  because its only effect was a column down there, and a control whose result is off screen reads as broken.
- **`.cards` is the builder's five-column summary row.** The income grid carried both `cards` and
  `inc-cards` and was silently overridden by it: one selection stretched across the page, three squeezed to
  230px. The container now uses `inc-cards` alone, `repeat(auto-fit,minmax(290px,330px))` with
  `justify-content:start`: left aligned, not centred, so the first card sits on the page's left edge like
  everything else and does not slide sideways when a second selection is added.
- **It opens with nothing selected** (user's request, 25 Sep 2026): three "None" selections and the line
  "Choose a fund or a portfolio to model an income". The chart, year table and notes cards are hidden until
  something is chosen, or they render as empty boxes with headings, and print and email no-op rather than
  producing a blank document.
- **`#income` needs its own page width.** `main.grid` and `#explorer` each carry
  `max-width:1240px;margin:0 auto`, and the income tab was missing it, so on a wide monitor the plan card
  ran the full width of the screen while every other tab sat in the 1240px column.
- **Print and email** (24 Sep 2026) build from one `iBundle()`, so the sheet and the pasted email cannot
  disagree. Print is one A4 page in every combination tested (one to three selections, stress on or off,
  40 years, inflation linked: 972 to 991px against the 1000px limit); the chart gives back 50px of height
  when the stress row appears, which was the only case that spilled. The chart passes literal hex for print,
  since print is always light, and email carries no chart at all. `PD_BAND(title, today)` is the shared
  brand band, extracted from `buildPrintDoc` and verified to leave its output byte-identical.
- **Percentiles are 5/95 throughout** (card, chart band and the runs-out figure), a true 90% range, chosen
  over 10/90 at the user's request for prudence and to match the builder's projection chart. Note that
  10/90 is the PRIIPs KID convention, so this tab is deliberately more conservative than a fund KID.
- **The sequencing stress restates the whole card** (25 Sep 2026). It first only added a footnote block while
  the headline stayed unstressed, and the user reported the switch as doing nothing: a control whose result
  does not move the figures reads as broken. Now `drop` is applied to the main run, both sensitivities, the
  solved income, the chart and the year table, and each card carries a badge: "Scenario, not a probability:
  the first 3 years lose X% evenly... Every figure below is the share of runs that start that way." The old
  "Survives a bad first 3 years" line was the same statistic as sustainability counted over stressed paths,
  under a second name, which is why it confused.
- **The stressed months are the band's total fall spread evenly over 36 months, not the period replayed.**
  Months 37 onwards are ordinary GBM draws. Say "spread evenly", never "the worst three years it has had",
  which implies a replay. Measured: replaying the ESMA 5 proxy's actual worst window gives 63% where the even
  decline gives 59%, because that window rose 4.3% in its first year before collapsing, so the even decline is
  the harsher and simpler assumption. `I_STRESS` proxies are Fixed ESG 20/60/80 and Global Equity ESG Passive,
  one family so the levels are measured alike, and their falls are index derived. Only ESMA 3 to 6 have a
  proxy; anything else runs unstressed and the badge says so.
- **Print carries its own condensed notes**, not the screen's methodology: reusing it pushed the stressed
  three-selection sheet to 1014px, over the one-page limit. With the shorter version every combination tested
  measures 896 to 965px (one and three selections, stress on and off, 40 years, inflation linked).
- **Verified:** the other four tabs byte-identical (both builders, both explorer tables and notes, print and
  email); the tab reproduces the reviewed prototype's figures exactly for the same inputs; a constant-return
  series matches closed-form arithmetic to the cent for fixed and inflation-linked income, and the depletion
  year is exact.
- A standalone `/income.html` existed for one day while this was agreed; it was removed when the tab landed.

## Copy for Word

A "Copy for Word" button beside "Copy for email" and "Print / save PDF" puts the whole results
document on the clipboard: tables arrive as real Word tables, charts as pictures, from one paste.
Built 6 Oct 2026 at the user's request, so sections can be lifted into their own client reports.
The clipboard carries `text/html` for Word and Excel and tab-separated `text/plain` for everything
else, and the destination picks.

- **The print document is the source.** `buildWordDoc()` runs `layoutPrintDoc()` then
  `buildPrintDoc(o)` and walks the composed result, so the pasted report and the printed PDF carry
  the same content in the same order and cannot disagree. It also inherits print's light-only,
  literal-hex composition, which is what keeps dark theme out of the paste, and the full warnings
  block travels with it, so pasted figures are never orphaned from the disclaimer.
- **Styles are read with `getComputedStyle`, not mapped by hand**, so a change to the `.pd-*` CSS
  reaches the Word output on its own. Only properties Word understands are carried.
- **An SVG loaded as an image ignores `@font-face`.** A chart rasterised whole comes out in a serif
  fallback, and no amount of waiting or `document.fonts.ready` fixes it: measured, "Growth of
  €100,000" sets 159px in Nunito Sans and 145px as the serif default. So `wdPNG()` rasterises the
  **shapes** from the SVG and paints the **text** onto the canvas, where this document's own font
  applies. Verified at 157px, the real face. Do not "simplify" this back to a single drawImage.
- **Type is mapped onto a ladder, not scaled.** The print document's sizes are px values for A4 at
  703px and cannot travel as they are: unscaled they read as fine print, and a flat 1.5x multiplier
  produced nine sizes running to 22.5pt, which the user rejected as a poster rather than a document.
  `WD_LADDER` maps print px onto **six** sizes: 6.5pt notes and tracking, 7pt table headers and
  labels, 8pt body and table text, 9pt section headings, 11pt a key figure, 14pt the title. A real
  document uses five or six sizes; keep it that way. Padding and letter-spacing stay true to the
  print page (px x 0.75). Key figures are bottom-aligned so values sit on one baseline where a label
  wraps, the asset mix doughnut sits beside its table as in print rather than stacked above dead
  space, and the ESMA scale's "Lower risk / Higher risk" spans the full width.
- **Word ignores `text-transform`.** The tracked uppercase labels arrived in sentence case ("Key
  figures · 5-year basis") where print shows them uppercase, because the uppercasing is CSS and Word
  imports the underlying text. The export uppercases the text itself and no longer emits the
  property. Found by unpacking a .docx the user saved; `word/document.xml` is the fastest way to see
  what Word actually made of a paste, including the real point sizes and image widths.
- **Word honours margins on `<p>` and throws them away on `<div>`.** A whole export came back with
  `spacing after="0"` on 174 of its 179 paragraphs, everything stacked on itself, because every block
  was a div; the only spacing that survived was on the chart paragraphs, which were already `<p>`.
  Anything holding inline content only is now a paragraph with explicit `margin-top`/`margin-bottom`,
  and a div survives only where it has to wrap a table or another block. Word also takes no margin on
  a table, so `WD_GAP`, a small empty paragraph, follows each one.
- **The brand band is one flat row of cells**: mark, SLATE LABS wordmark, caption. Sharing a
  paragraph ran the two images into each other in both bands, and separating them with a nested table
  inside a band cell is the fragile way to fix it. A table cell is the one horizontal gap Word will
  not collapse, so `.bm` is flattened into the band's own row rather than nested.
- **The ESMA scale is a 269x22 strip and must not be drawn at full width**, where its seven boxes
  dwarf the page. It carries no class of its own, so it is identified by the `.pd-esma-l` labels that
  follow it, with an aspect-ratio fallback, and drawn at 300px with its Lower/Higher labels
  constrained to the same width rather than spanning the page.
- **Word does not do flex or grid.** `.pd-kpis`, `.pd-ab`, `.pd-band`, `.pd-titlerow`,
  `.pd-ac`, `.pd-legend` and `.pd-esma-l` become one-row tables, so the product tile sits beside the
  title and the doughnut beside its table as print has them; everything else stacks. Charts are drawn at 640px, near Word's text width,
  and rasterised at 2x so they stay sharp when scaled. Marks, swatches and the doughnut keep their
  own size and stay inline; anything 250px or wider gets a paragraph of its own.
- **Cells are walked, not flattened.** `textContent` ran a fund name straight into its asset class
  ("Aviva Multi-Asset ESG Active 4Multi-Asset"), so cell contents go through the same walker and
  keep their sub-labels on their own line. The zero-width ◆ spans (`.pd-dia`, `.simd`) are dropped
  before they can wreck a number; name cells keep their full-size ◆ as on screen.
- **Cost stays out in All Funds mode**, because print already does: verified no cost figure reaches
  any table cell there. The disclaimer's own "Where a portfolio cost is shown" sentence remains, as
  fixed legal text.
- **Verified:** every one of the 202 table cells in the print document appears in the pasted
  document; `buildPrintDoc` and `buildEmailSummaryHTML` hash identically to the pre-change build for
  a single portfolio and for A and B, as do the layout options and the explorer; three scenarios
  (1 fund, 5 funds, 5 + 5) build with no SVG and no `var()` surviving, 235KB to 371KB and 180ms to
  886ms; and the user confirmed a real paste into Word keeps both the tables and the pictures.
- Clipboard writes need a user gesture and a focused document, so a scripted `.click()` fails with
  `NotAllowedError`. That is correct behaviour, and the button reports "Copy failed" rather than
  failing silently.
### The fund explorer's own export

Built the same day, at the user's request, covering the table and the whole compare screen.

- **The explorer has no print document**, being screen only by decision, so `buildExplorerPrintDoc()`
  composes one in the same `.pd-*` idiom and hands it to `wordFromHTML()`, the shared converter that
  the builder's export also goes through. That is what keeps the two outputs looking alike, and it
  sidesteps the two traps of exporting from the screen: the table's computed styles are the dark
  theme, and the compare charts resolve their colours through `var()`, which stops resolving the
  moment an SVG is detached. The composition is light by construction and the charts are re-drawn
  with `PRINT`.
- **Tables are read from the rendered DOM** (`xPdTable`), so the figures are the exact strings on
  screen and the filters, sort and end month are already applied: no second copy of that logic to
  drift. The tick box and the Add to column are controls, not data, and are dropped.
- **The compare charts are recomputed through the same pure helpers** `renderCompare` uses
  (`xWindow`, `xRets`, `xRow`, `xAmtVal`), so the figures cannot differ from the screen. Colours come
  from `SEG_FIXED` rather than `SEG`, which is `var()` based.
- **Everything on the compare screen travels**, at the user's request: legend, performance bar chart
  and table, growth, drawdown, calendar years, the notes and the What's inside cards, each card
  flattened to a small table taking whichever tab is open on screen.
- **Chart type is enlarged by shrinking the canvas, never by raising the font sizes.** A chart is read
  at about 6.3in whatever its canvas, so the export draws on 430 units and lets Word scale it up by
  1.4, landing the print theme's 8px axis labels near 8pt beside 8pt body text. Raising the sizes on
  a 703-unit canvas was tried first and clips: the charts' padding is set for the print sizes, so
  larger euro labels run off the left edge and the date axis is cut off.
- **The legend is drawn inside each chart's own image** (`xChartLegend`), at the user's request, so
  the whole graph is one object in Word. It wraps onto further lines rather than running off the
  edge, which three long fund names do. This is why `wdHarvest` had to become transform aware: the
  chart is nested under a `translate` once a legend band sits above it, and the harvester was reading
  raw x/y and ignoring ancestor transforms.
- **The bar chart turns its value labels upright with three or more selections**, and that is correct
  rather than a fault: across five periods at 6.3in a flat "-5.5%" is wider than its bar at any
  readable size. The chart decides this by measuring; do not force it flat.
- **Tables repeat their header row and rows do not split.** The header row goes in `<thead>`, which
  Word repeats at the top of each page a table runs onto, and every data row carries
  `page-break-inside:avoid`. Layout rows (the asset mix doughnut beside its table, the key figures
  strip) deliberately do not: forcing a layout row onto one page is not wanted.
- **The warnings block starts its own page**, and the break goes on one empty paragraph **before** the
  block, never on the block itself: Word hands a container's `page-break-before` to every paragraph
  inside it, so setting it on `.pd-disc` put each of the eight disclaimer paragraphs on its own page.
  Nine breaks in a document is the symptom; count them in `document.xml` (`w:pageBreakBefore`).
- **What's inside is two cards across as one flat table**, not two nested ones. Word dissolves a table
  nested inside a layout cell, and a pair came back as 5 rows by 3 columns with the nesting gone, so
  the pair is built as a single table of label, value, gap, label, value.
- **Chart value labels carry their halo as a stroke under the fill** (`paint-order="stroke"`), which is
  what keeps them readable where a label sits on its own line. The rasteriser strips text and repaints
  it, so it has to replay the stroke first or the halo is lost: without it the drawdown chart's lines
  ran straight through the digits. `wdPaint` strokes then fills, in that order.
- **Two per-table Excel buttons** sit beside it, on the explorer table and on calendar years, because
  a whole-document paste into Excel stacks everything down one sheet. Verified: 14 consistent
  columns, 38 rows, tab-separated plain text as the fallback.
- **Verified:** print, email, the builder's Word export, the explorer table and its note, and the
  compare screen's performance table, calendar and What's inside cards all hash identically to the
  build before the explorer export existed. Console clean.
- The income tab is excluded by the user's decision.

## Saved portfolios

Save the portfolio you have built under a name and open it back into A or B later, from a Saved
control in section 1 of either builder. Built 10 Oct 2026 at the user's request.

- **Only the funds and their allocations are saved**, by the user's decision: not the investment
  amount, the standard cost, the contributions or the window. A save is the composition, and the
  figures beside it are whatever today's data and today's inputs make them. Do not quietly start
  restoring the inputs too.
- **A single portfolio, never a pair**, so it can be opened into A or into B. Saving A and B together
  would lock them into the slots they happened to be in, and comparing a saved portfolio against a new
  one is the main reason to have this.
- **A save carries its mode**, and opening it switches to its own builder: an All Funds portfolio
  cannot open in the Aviva builder, where half its funds do not exist, so it takes you to that tab
  rather than silently dropping holdings.
- **Opening is where a save meets data that has moved.** A fund it names may have left the universe:
  it is dropped, named in the message, and the message says what the allocations now total, rather
  than quietly rebalancing. The list also marks a save with "n missing" before you open it.
- **These are the user's own portfolios**, which is what keeps them clear of the **preset portfolios**
  that were rejected as implying a recommendation. The distinction holds only while the tool ships
  none of its own: nothing pre-filled, nothing suggested, no starter set. Do not add one.
- **Stored under `apb-portfolios-v1`**, separate from the fund lists and with its own Save to file and
  Load from file, by the user's decision that each file should be one obvious thing. The About page's
  privacy section covers both and says plainly that neither is a record.
- **The panel lives in section 1, which is a narrow column**, so each row wraps: name on its own line,
  then the meta and the A / B / ✕ buttons. On one line the name was squeezed out of existence.
- **`pRender()` rebuilds the panel, so `pMsg()` must come after it**, or the confirmation is wiped by
  the re-render that follows. That bug was in the first cut of the save path.
- **Verified:** save, open into A and into B with the other left untouched, cross-mode open switching
  tabs, a save naming a fund that no longer exists (dropped, named, total reported), delete, file
  export and import round-tripping, and survival across a reload. Every other tab, print, email, the
  builder's Word export and the lists tab hash identically to the build before this existed.
- **Not built, and not to be added without asking:** a note or client reference on a save, and one
  combined file for portfolios and lists.

## My Fund Lists tab

A tab between All Funds Explorer and Income Sustainability, built 10 Oct 2026 at the user's request: four tables, ESMA 3 to 6, each holding the funds
**the user has chosen** for that band. It answers something no filter can, a hand-picked shortlist per
risk band, kept between visits and copied out as a document.

- **It sits next to a line the project does not cross.** Preset portfolios and risk profile target
  selectors were rejected because the tool computes and displays, it does not recommend, and a curated
  set of funds per band is in substance a preferred fund panel. What keeps this the right side of it is
  that **the tool chooses nothing**: the tab always opens empty, ships no starter list, and the heading
  and the copied output name it as the user's own selection, "not a recommendation and not a fund
  panel: the tool selects nothing". Raised with the user before building and confirmed by them. Do not
  pre-fill it, do not rank anything in it, and do not let it feed the builder's figures.
- **Membership is free, mismatches are flagged.** Any fund can go in any band, since an adviser may
  hold a 5 inside a band 4 plan. A fund whose published rating differs from its band is marked `!` in
  the row, listed in the warning line, and named in the Word copy. Flag, never silently correct, never
  block: a table headed ESMA 4 quietly holding a 6 would mislead the moment it reached a client.
- **Funds are added through a multi-select panel, not a dropdown.** At 96 funds, picking one at a
  time and waiting for a re-render between each is the wrong shape; the user asked for multiple. The
  panel has a search, a checkbox per fund showing its provider and published rating, a running count
  and one Add. **"Only funds rated N" defaults on**, since curating that band is the common case, and
  unticking it is how the band stays free to hold anything. Funds already in the band are not offered.
  The panel stays open after an add, with the selection cleared, so a list can be built in one sitting.
- **Universe is all 96 funds** (`ALLF`), regardless of `MODE`, with a Provider column and no Fee vs
  standard column, following the All Funds rule. Portfolios do not appear; these are fund lists. Like
  the income tab it **owns no mode**, so `showTab()` leaves `MODE` alone for it.
- **Figures come from `xRow(f, L.end)`**, the explorer's own row builder, so a fund reads identically on
  both tabs. Verified cell by cell: every figure for every listed fund matches the All Funds Explorer at
  the same end month, 0 differences.
- **Saved in `localStorage` under `apb-lists-v1`**, wrapped in try/catch, with Save to file and Load
  from file as JSON. The file is the real backup: browser storage is per machine, per browser, and goes
  when site data is cleared. Everything stays local, which keeps the data licence where it is. The
  About page's privacy section says all of this, and says plainly that the lists are not a record.
- **Order within a band is the user's: drag the row.** `lDragBind` uses pointer events rather than
  HTML5 drag and drop, which gives no touch support and an unusable drag image for a table row. Rows
  are moved in the DOM as the pointer passes their midpoints, which is its own feedback and needs no
  insertion marker, and the order is written back to `LISTS[b]` on release. **A drag that never travels
  4px is a click**, so the remove button still works.
  **A drag needs a mouse or a pen**: on a touch screen the same gesture is a scroll, and `pointerdown`
  returns early for `pointerType==="touch"`. So the up and down buttons (`lMove`) remain as the
  fallback, `visibility:hidden` until the row is hovered or holds focus and always visible under
  `@media (hover:none)`. That is what keeps the table clean while leaving keyboard and tablet users a
  way to reorder. Do not delete the arrows in favour of dragging alone.
  **Every row carries a grip** at its left, six dots in SVG, faint by default and signal blue on hover,
  with the title "Drag to reorder". A row you can pick up has to say so, and saying it only on hover
  means you must hover to learn that hovering does anything. The whole row stays draggable; the grip is
  a hint, not a handle you must hit.
  The grip takes first place in the row, so the `.proj` rules that keyed off `:first-child` move along
  one: `.ltbl` re-applies left alignment to the second cell and the Excel copy drops columns
  `[0, L_COLS.length+1]` rather than just the last. Forget either and the fund names right-align with
  the figures, or the grip column lands in the spreadsheet.
- **Every column heading sorts its own band, and sorting is a view, never a rewrite.** The order is
  the user's work; a stray click on a heading must not destroy it. `L.sort[b]` cycles ascending,
  descending, back to manual, blanks always last as in the explorer, and it is held **in memory only**
  so a reload returns to the arranged order. A sorted band hides its grips, disables the arrows and
  shows a "Sorted by X · Manual order" button to come back. `lOrdered(b)` is the one place display
  order is decided, and the screen table, the Word document and the Excel copy all go through it:
  the Word builder read `LISTS[b]` directly at first and ignored the sort, which is the mistake to
  watch for if another export is added.
- **A saved list names funds.** On load, a fund that has left the universe is dropped and named in the
  warning line rather than disappearing quietly, the same principle as `applyData()`'s pruning.
- **Copy for Word** builds the whole tab as one document through `buildListsPrintDoc()` and the shared
  `wordFromHTML()`, so it comes out under the same rules as the other two exports; empty bands are left
  out. **Copy table** per band reuses `xCopyTable` for Excel.
- **Verified:** all five existing tabs, print, email and the builder's Word export hash identically to
  the build before this tab existed. Console clean. Lists survive a reload, a removal persists, and a
  deliberate mismatch is caught and named in both the screen warning and the document.
- **Not built, and not to be added without asking:** several named list sets (the storage shape allows
  it without a migration), reordering within a band, and bands outside 3 to 6.

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
