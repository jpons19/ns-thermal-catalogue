"""Parse the saved Potekhin catalogue page (data/raw/Cooling_NS.html) into
data/web_table.json (one record per neutron star) and data/web_updates.json (the page's update log).

Units in the page: distance kpc, P s, Pdot s/s, Bdip G, tau_c and t* in yr, L in 1e33 erg/s, T in eV.
The build step converts to kyr / 1e32 erg/s.  Every table row has 16 numeric fields
(d min/mid/max, P, Pdot, Bdip, tau_c, t* min/mid/max, L min/mid/max, T min/mid/max);
'---' means not given.
"""
import re, html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
raw = (ROOT/"data"/"raw"/"Cooling_NS.html").read_bytes().decode("koi8-r", errors="replace")
t = re.sub(r"<script.*?</script>", "", raw, flags=re.S | re.I)
t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
t = re.sub(r"</(tr|p|h\d|li|pre)>", "\n", t, flags=re.I)
t = re.sub(r"</t[dh]>", " | ", t, flags=re.I)
t = html.unescape(re.sub(r"<[^>]+>", "", t))
t = re.sub(r"\n\s*\n+", "\n", t)
lines = t.split("\n")

sect = {"Weakly": "CCO/TINS", "Ordinary": "RPP", "High-B": "HB-PSR", "XINSs": "XINS", "Upper": "UL", "Small": "Hot-spot PSR"}
refre = re.compile(r"^\(?[DTAS](\[data\])?\)?$")
rows, cls = [], None
for ln in lines:
    st = ln.strip()
    for k, v in sect.items():
        if st.startswith(k) and st.endswith(":"):
            cls = v
    if not cls or not ln.startswith(" ") or st.startswith(("-", "=", "Name", "or", "min", "Weakly", "Ordinary", "High-B", "XINS", "Upper", "Small")):
        continue
    parts = re.split(r"\s{2,}", st)
    if len(parts) < 3:
        continue
    name, assoc = parts[0], parts[1]
    toks = " ".join(parts[2:]).split()
    date = toks.pop() if re.match(r"^\d\d\.\d\d\.\d{4}$", toks[-1]) else None
    while toks and refre.match(toks[-1]):
        toks.pop()
    if len(toks) != 16:
        print("skipped (unexpected field count):", name, len(toks)); continue
    v = [None if x == "---" else float(x) for x in toks]
    keys = ["dlo", "dmid", "dhi", "P", "Pd", "B", "tc", "tlo", "tmid", "thi", "Llo", "Lmid", "Lhi", "klo", "kmid", "khi"]
    rows.append(dict(name=name, assoc=assoc, cls=cls, date=date, **dict(zip(keys, v))))
(ROOT/"data"/"web_table.json").write_text(json.dumps(rows))
upd = t.split("Summary of updates:")[1].split("Alexander Potekhin,")[0].strip().split("\n")
(ROOT/"data"/"web_updates.json").write_text(json.dumps(upd))
print(f"parsed {len(rows)} rows and {len(upd)} update lines")
