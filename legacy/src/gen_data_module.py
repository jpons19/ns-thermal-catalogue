"""Generate the portable Python plotting module from the normalized catalogue."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
order = ["V13", "P20", "WEB", "M24", "HO26", "COMPARISON"]


def read_entries(filename, *, comparison=False):
    with (ROOT / "data" / filename).open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["source_id"] == "1" or not row["age_yr"]:
                continue
            if row["component"] == "cool_surface_upper_limit":
                continue  # The conditional limits remain in Measurements.
            ref = row["reference"]
            name = row["name"]
            if ref == "HO26" and not comparison:
                name += " (cool surface)" if row["component"] == "cool_surface" else " (total)"

            def number(key):
                return float(row[key]) if row[key] else None

            age = number("age_yr")
            T, Tlo, Thi = (number(key) for key in ("kT_inf_eV", "kT_inf_eV_lo", "kT_inf_eV_hi"))
            note = row["note"]
            if T is None and Tlo is not None and Thi is not None:
                if ref == "P20" and "/" in note:
                    T, Tlo, Thi = Tlo, None, None
                else:
                    T = (Tlo + Thi) / 2 if ref == "P20" else (Tlo * Thi)**0.5
                note = " ".join(filter(None, (note, "Temperature is a plotting representative; see Measurements.")))
            yield ("COMPARISON" if comparison else ref), dict(
                name=name, cls=row["class"], age=age,
                age_lo=number("age_yr_lo") or age, age_hi=number("age_yr_hi") or age,
                L=number("L_inf_erg_s"), L_lo=number("L_inf_erg_s_lo"), L_hi=number("L_inf_erg_s_hi"),
                L_ul=row["luminosity_upper_limit"] == "True", T=T, T_lo=Tlo, T_hi=Thi,
                T_ul=row["temperature_upper_limit"] == "True", note=note,
                component=row["component"], reference=ref, age_reference=row["age_reference"],
                age_ul=number("age_upper_limit_yr"), age_status=row["age_status"],
            )


E = [*read_entries("measurements.csv"),
     *read_entries("cooling_comparison.csv", comparison=True)]

def fmt(v):
    if v is None: return "None"
    if isinstance(v,bool): return "True" if v else "False"
    if isinstance(v,float): return repr(float(f"{v:.6g}"))
    return repr(v)
out=['''"""
ns_cooling_data.py - observed thermal luminosities, temperatures and ages of isolated neutron stars
==============================================================================================
Generated from the catalogue CSV tables. Intended to be imported and overplotted on
theoretical cooling curves.

References (keys of DATA)
  V13   Vigano et al. 2013, MNRAS 434, 123
  P20   Potekhin et al. 2020, MNRAS 496, 5052 (paper table; some values superseded by WEB)
  WEB   Potekhin catalogue page, last update 03.08.2026 (supersedes P20 for many sources)
  M24   Marino et al. 2024, arXiv:2404.05371 (three cold sources, hot-spot blackbody)
  HO26  Ho, Simkhayeva & Potekhin 2026, arXiv:2601.14388 (Vela Jr, cool surface and total)
  COMPARISON  One luminosity record per source with an independent age, see Cooling_comparison

Units (all quantities are as seen by a distant observer, i.e. redshifted)
  age  : years      (independent of spin-down timing)
  L    : erg/s      (thermal luminosity)
  T    : eV         (kT_inf; model dependent, NOT comparable across references - see notes)
Each entry: name, cls, age, age_lo, age_hi, L, L_lo, L_hi, L_ul, T, T_lo, T_hi, T_ul, note
  *_lo/_hi are the ends of the quoted range (not offsets); None = not available.
  L_ul / T_ul = True means the value is an upper limit.
  cls in {"CCO/TINS","RPP","HB-PSR","XINS","UL","Hot-spot PSR","MAG"}.
Caveats: V13 L is a range and its kT carries no error; V13 and M24 use hot-spot blackbody-type kT,
WEB/P20 often use atmosphere models. Known errors in the source tables are listed in the workbook (Findings).

Quick use
    import ns_cooling_data as ns
    ax.set_xscale("log"); ax.set_yscale("log")
    ns.plot_observations(ax, quantity="L", xunit="yr")            # all references
    ns.plot_observations(ax, "T", refs=("WEB","M24","HO26"), label_names=("PSR J0205+6449",))
    ns.plot_observations(ax, "L", refs=("COMPARISON",))
    a = ns.get("WEB", "L")   # dict of numpy arrays: name, x, xerr (2,N), y, yerr (2,N), ul, cls
"""
import numpy as np

STYLE = {
    "V13":  dict(color="#1f77b4", marker="o", ms=6,  label="Viganò+13"),
    "P20":  dict(color="#2ca02c", marker="s", ms=5,  label="Potekhin+20 paper", alpha=0.5),
    "WEB":  dict(color="#7b2d8e", marker="^", ms=6.5, label="Potekhin web (03.08.2026)"),
    "M24":  dict(color="#d62728", marker="*", ms=14, label="Marino+24"),
    "HO26": dict(color="#c97823", marker="D", ms=7, label="Ho+26 (Vela Jr)"),
    "COMPARISON": dict(color="#1b6668", marker="o", ms=6, label="Cooling comparison"),
}

DATA = {
''']
for ref in order:
    out.append(f'    "{ref}": [\n')
    for r,e in E:
        if r!=ref: continue
        items=", ".join(f"{k}={fmt(v)}" for k,v in e.items())
        out.append(f"        dict({items}),\n")
    out.append("    ],\n")
out.append("}\n")
out.append('''

def get(ref, quantity="L", include_magnetars=True, classes=None):
    """Return numpy arrays for one reference and quantity ('L' or 'T').
    x in years; xerr = [[x-age_lo],[age_hi-x]]; y and yerr likewise; ul = upper-limit flags."""
    q = quantity.upper()
    if q not in ("L", "T"):
        raise ValueError("quantity must be L or T")
    if ref == "COMPARISON" and q == "T":
        raise ValueError("COMPARISON is a luminosity sample; use a literature reference for temperature")
    names, x, xl, xh, y, yl, yh, ul, xul, cl = [], [], [], [], [], [], [], [], [], []
    for e in DATA[ref]:
        v = e[q]
        if v is None: continue
        if (not include_magnetars) and e["cls"] == "MAG": continue
        if classes is not None and e["cls"] not in classes: continue
        lo, hi = e[q + "_lo"], e[q + "_hi"]
        names.append(e["name"]); cl.append(e["cls"])
        xul.append(e["age_ul"] is not None)
        if xul[-1]:
            x.append(e["age_ul"]); xl.append(0.25 * e["age_ul"]); xh.append(0)
        else:
            x.append(e["age"]); xl.append(max(e["age"] - e["age_lo"], 0)); xh.append(max(e["age_hi"] - e["age"], 0))
        y.append(v)
        yl.append(0 if lo is None else max(v - lo, 0)); yh.append(0 if hi is None else max(hi - v, 0))
        ul.append(bool(e[q + "_ul"]))
    return dict(name=np.array(names), cls=np.array(cl), x=np.array(x, float),
                xerr=np.array([xl, xh], float), y=np.array(y, float), yerr=np.array([yl, yh], float),
                ul=np.array(ul, bool), xul=np.array(xul, bool))


def plot_observations(ax, quantity="L", refs=("V13", "P20", "WEB", "M24", "HO26"), xunit="yr",
                      include_magnetars=False, label_names=(), legend=True, zorder=5, **kw):
    """Overplot observations on an existing axes (e.g. next to theoretical cooling curves).
    xunit: 'yr' or 'kyr'. Extra keyword arguments (e.g. elinewidth, capsize) go to ax.errorbar.
    Magnetars (V13 only) are off by default. Returns the list of plotted references."""
    scale = {"yr": 1.0, "kyr": 1e-3}[xunit]
    done = []
    for ref in refs:
        d = get(ref, quantity, include_magnetars)
        if len(d["x"]) == 0: continue
        st = dict(STYLE[ref]); lab = st.pop("label"); ms = st.pop("ms"); mk = st.pop("marker"); col = st.pop("color")
        alpha = st.pop("alpha", 0.9)
        first = True
        for i in range(len(d["x"])):
            ul = d["ul"][i]
            ye = np.array([[0.0], [0.0]]) if ul else d["yerr"][:, i:i+1]
            style = {"mfc": "white"} if (ref == "HO26" and d["name"][i].endswith(" (total)")) else {}
            if ref == "V13" and d["cls"][i] == "MAG":
                style = {"mfc": "white", "fmt": "D"}
            else:
                style["fmt"] = mk
            ax.errorbar(d["x"][i]*scale, d["y"][i], xerr=d["xerr"][:, i:i+1]*scale, xuplims=bool(d["xul"][i]),
                        yerr=(np.array([[d["y"][i]*0.45], [0.0]]) if ul else ye), uplims=bool(ul),
                        ms=ms, color=col, ecolor=col,
                        **(dict(elinewidth=1.0, capsize=2, alpha=alpha, zorder=zorder,
                                label=lab if first else None) | style | kw))
            first = False
            if d["name"][i] in label_names:
                ax.annotate(d["name"][i], (d["x"][i]*scale, d["y"][i]), xytext=(6, 6),
                            textcoords="offset points", fontsize=8, color=col)
        done.append(ref)
    ax.set_xlabel(f"Age ({xunit})")
    ax.set_ylabel("Thermal luminosity (erg/s)" if quantity.upper() == "L" else "Temperature at infinity (eV)")
    if legend: ax.legend(fontsize=8)
    return done


if __name__ == "__main__":      # demo: observations with a dummy power-law curve
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    t = np.logspace(2, 6, 100)
    for ax, q, curve in ((axs[0], "L", 3e34*(t/1e3)**-0.35), (axs[1], "T", 160*(t/1e3)**-0.1)):
        ax.plot(t, curve, "k-", label="theory (dummy)")
        ax.set_xscale("log"); ax.set_yscale("log")
        plot_observations(ax, q, xunit="yr", label_names=("PSR J0205+6449", "PSR B2334+61"))
        ax.set_xlim(2e2, 3e6)
    fig.tight_layout(); fig.savefig("ns_cooling_data_demo.png", dpi=120)
    print({k: len(v) for k, v in DATA.items()})
''')
open(ROOT/'data'/'ns_cooling_data.py','w').write("".join(out))
print({r:sum(1 for x,_ in E if x==r) for r in order})
