#!/usr/bin/env python3
"""
Aviva Ireland Portfolio Builder - data refresh script (v2).

Accepts EITHER the consolidated monthly workbook OR the legacy three files:

  Single workbook (sheets: 'ALPI fund centre details', 'Price history live', 'Simulated prices'):
      python3 refresh_dashboard.py Portfolio_builder_files.xlsx dashboard.html

  Output path ending in .json writes the data payload for the hosted build instead:
      python3 refresh_dashboard.py Portfolio_builder_files.xlsx data/latest.json

  Legacy three files:
      python3 refresh_dashboard.py <live.xlsx> <simulated.xlsx> <fund_centre.xlsx> <dashboard.html>

Methodology (unchanged):
  - live price dates shifted back one day to true month end
  - live net returns grossed up geometrically: (1+r)*(1+AMC)^(1/12)-1
  - simulated returns (already gross) spliced strictly before the first live price
  - live data always wins on overlap

Injects the resulting JSON between the /*DATA_START*/ and /*DATA_END*/ markers
in the dashboard HTML.
"""
import sys, json, re
import pandas as pd

SIM_HEADER_FIX = {"Unnamed: 7": "Aviva Emerging Markets Equity Index Series 1"}

# Source-data overrides: applied where the Fund Centre extract is blank/wrong.
# Remove entries once corrected at source.
ESMA_OVERRIDES = {"Aviva Global Equity ESG Passive Series 1": 6}  # blank in July 2026 extract, confirmed 6

WB_SHEETS = {"static": "ALPI fund centre details", "live": "Price history live", "sim": "Simulated prices"}

def parse_cost_adj(text):
    m = re.search(r"([+-]\s*\d+\.?\d*)\s*%", str(text))
    return round(float(m.group(1).replace(" ", "")) / 100.0, 6) if m else 0.0

def build_data(live_src, sim_src, static_src):
    live = pd.read_excel(*live_src, header=2)
    live.columns = ["Fund", "Date", "Offer"]
    live["Date"] = pd.to_datetime(live["Date"], errors="coerce")
    live = live.dropna(subset=["Date"])
    live["Offer"] = pd.to_numeric(live["Offer"], errors="coerce")
    live = live.dropna(subset=["Offer"])
    live["P"] = (live["Date"] - pd.Timedelta(days=1)).dt.to_period("M")

    sim = pd.read_excel(*sim_src).rename(columns=SIM_HEADER_FIX)
    sim = sim.drop(columns=[c for c in sim.columns if str(c).startswith("Unnamed")])
    sim["Name"] = pd.to_datetime(sim["Name"])
    sim = sim.set_index(sim["Name"].dt.to_period("M")).drop(columns=["Name"])

    stat = pd.read_excel(*static_src, header=1)
    stat = stat.dropna(subset=["AMC"])
    stat = stat[stat["Fund name"] != "Name"].set_index("Fund name")

    funds = []
    for fund in stat.index:
        amc = float(stat.loc[fund, "AMC"])
        gm = (1.0 + amc) ** (1.0 / 12.0)
        lp = live[live["Fund"] == fund].set_index("P")["Offer"].sort_index()
        if lp.empty:
            print(f"WARNING: no live prices for {fund}; skipped"); continue
        live_ret = ((1.0 + lp.pct_change().dropna()) * gm - 1.0)
        first_live = lp.index.min()

        parts = []
        if fund in sim.columns:
            sr = sim[fund].dropna().pct_change().dropna()
            parts.append(sr[sr.index <= first_live])
        parts.append(live_ret)
        s = pd.concat(parts)
        s = s[~s.index.duplicated(keep="last")].sort_index()
        idx = s.index
        gaps = [i for i in range(len(idx) - 1) if (idx[i + 1] - idx[i]).n != 1]
        if gaps:
            raise ValueError(f"Gap in spliced series for {fund} at {idx[gaps[0]]}")

        cat = str(stat.loc[fund, "Category"]).strip()
        if cat.lower() == "alterantive": cat = "Alternative"
        esma_raw = str(stat.loc[fund, "ESMA Category"]).strip()
        funds.append({
            "name": fund,
            "category": cat,
            "esma": ESMA_OVERRIDES.get(fund, int(float(esma_raw)) if esma_raw not in ("", "nan", "None") else None),
            "costBasis": str(stat.loc[fund, "Cost"]).strip(),
            "costAdj": parse_cost_adj(stat.loc[fund, "Cost"]),
            "amc": round(amc, 6),
            "simulated": fund in sim.columns,
            "liveStart": str(first_live),
            "start": str(s.index.min()),
            "returns": [round(float(x), 6) for x in s.values],
        })

    as_of = str(max(pd.Period(f["start"], "M") + len(f["returns"]) - 1 for f in funds))
    return {"asOf": as_of, "funds": funds}

def write_json(json_path, data):
    """Write the payload for the hosted dashboard, which fetches it at runtime."""
    with open(json_path, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    print(f"Wrote {len(data['funds'])} funds, data to {data['asOf']}, to {json_path}")

def inject(html_path, data):
    with open(html_path) as fh: html = fh.read()
    blob = "/*DATA_START*/" + json.dumps(data, separators=(",", ":")) + "/*DATA_END*/"
    new = re.sub(r"/\*DATA_START\*/.*?/\*DATA_END\*/", lambda m: blob, html, count=1, flags=re.S)
    with open(html_path, "w") as fh: fh.write(new)
    print(f"Injected {len(data['funds'])} funds, data to {data['asOf']}, into {html_path}")

if __name__ == "__main__":
    if len(sys.argv) == 3:  # consolidated workbook mode
        wb, html = sys.argv[1], sys.argv[2]
        data = build_data((wb, WB_SHEETS["live"]), (wb, WB_SHEETS["sim"]), (wb, WB_SHEETS["static"]))
    elif len(sys.argv) == 5:  # legacy three-file mode
        data = build_data((sys.argv[1], "Report"), (sys.argv[2], "Sheet1"), (sys.argv[3], "Data"))
        html = sys.argv[4]
    else:
        print(__doc__); sys.exit(1)
    # .json writes the payload for the hosted build; anything else keeps the original
    # behaviour of injecting straight into a self-contained HTML file.
    if html.lower().endswith(".json"):
        write_json(html, data)
    else:
        inject(html, data)
