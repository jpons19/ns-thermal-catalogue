"""Plot the independent-age literature cross-match and the one-record comparison."""
from pathlib import Path
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data"))
import ns_cooling_data as ns


def draw(quantity, *, comparison=False):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set(xscale="log", yscale="log")
    refs = ("COMPARISON",) if comparison else ("V13", "P20", "WEB", "M24", "HO26")
    ns.plot_observations(
        ax, quantity, refs=refs, xunit="kyr", include_magnetars=not comparison, legend=False,
    )
    if comparison:
        ax.set_title("Thermal luminosity and independent age")
        ax.set(xlim=(0.018, 1.1e4), ylim=(1e28, 1e36))
        offsets = {"PSR B2334+61": ("B2334+61", (8, -19)),
                   "CXOU J085201.4-461753": ("Vela Jr", (-27, -20))}
        for entry in ns.DATA["COMPARISON"]:
            if entry["name"] in offsets:
                name, offset = offsets[entry["name"]]
                ax.annotate(name, (entry["age"]/1000, entry["L"]), xytext=offset,
                            textcoords="offset points", fontsize=8, color="#1b6668")

        note = ("One luminosity per source. Arrows indicate upper limits. "
                "Vela Jr pairs the Ho et al. cool component with the Suherli et al. age. "
                "The disputed SN 1181 age for 3C 58 is omitted.")
        filename = "cooling_comparison.png"
    else:
        ax.set_title("Literature cross-match with independent ages")
        ax.set_xlim(0.018, 1.1e4)
        ax.set_ylim((1e28, 3e36) if quantity == "L" else (3, 1000))
        note = ("Open Viganò diamonds mark magnetars. An open Ho diamond marks the total luminosity. "
                "Marino measurements show the detected hot spots with 90% errors. "
                "The 3C 58 points use the disputed SN 1181 association.")
        if quantity == "T":
            note = ("Open Viganò diamonds mark magnetars. Marino temperatures are hot-spot blackbody fits. "
                    "Temperature ranges can span distinct spectral components.")
        filename = "luminosity_vs_age.png" if quantity == "L" else "temperature_vs_age.png"
    ax.grid(True, which="major", alpha=0.25)
    ax.legend(fontsize=9, loc="best")
    fig.text(0.12, 0.027, textwrap.fill(note, 120), fontsize=8, color="#444444")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(ROOT / "figures" / filename, dpi=170)
    plt.close(fig)


draw("L")
draw("T")
draw("L", comparison=True)
