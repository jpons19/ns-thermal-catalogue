# Observational catalogue for isolated neutron-star cooling

The catalogue brings together the supplied Viganò et al. (2013), Potekhin et al. (2020),
Potekhin web, Marino et al. (2024), and Ho et al. (2026) data. It includes the three sources
in the requested [Marino JSON](https://github.com/Blitzman/workshop_fisica/blob/main/observations/marino2024_sources.json).
The unmodified JSON is archived in `data/raw/`. Literature references and table locators accompany the data.

## Use the catalogue

| File | Contents |
|---|---|
| `data/NS_thermal_crossmatch.xlsx` | Searchable Sources, Measurements and Cooling_comparison sheets, with references and the original wide cross-match and consistency checks |
| `data/sources.csv` | One row per catalogue entry, including the historical disputed 1E 0102.2−7219 candidate and the SN 1987A remnant constraint |
| `data/measurements.csv` | Reference-specific ages, luminosities, temperatures and distances, including sources without independent ages |
| `data/cooling_comparison.csv` | One representative luminosity per source with an independent age, including upper limits |
| `data/vela_jr_ages.csv` | Both age ranges used for Vela Jr |
| `data/references.csv` | Bibliographic keys and links |
| `data/ns_cooling_data.py` | Standalone NumPy data and plotting helpers |
| `figures/` | Luminosity–age comparison, literature cross-match, and field-decay age diagnostics |
| `notes/ns_thermal_data_notes.pdf` | Interpretation notes and checks from the original project, updated for the catalogue changes |

For a cooling curve in years and photon luminosity at infinity in erg/s:

```python
import sys
sys.path.insert(0, "data")
import ns_cooling_data as ns

ax.set(xscale="log", yscale="log")
ns.plot_observations(ax, "L", refs=("COMPARISON",), xunit="yr")
```

Use `refs=("V13", "P20", "WEB", "M24", "HO26")` to inspect alternative determinations.
The full measurements table includes the conditional cool-surface limits from Viganò and Marino.
Temperature depends on the fitted model and emitting area. Use the luminosity table with its component and age metadata when comparing with a model. The comparison table is an exploratory plotting sample. Some included luminosities have heterogeneous spectral assumptions.

### The three Marino sources

| Source | Age (yr) | Detected hot-spot luminosity (10³² erg/s) | Conditional cool-surface limit (10³² erg/s) |
|---|---:|---:|---:|
| PSR J0205+6449 | 841 | 1.44 (−0.50, +0.60) | <0.0001 |
| PSR B2334+61 | 7700 | 0.78 (−0.10, +0.30) | <0.4 |
| CXOU J0852−4617 (Vela Jr) | 2500–5000 | 2.0 (−0.6, +0.6) | <1.3 |

Ages follow the main text and requested JSON. Luminosities and 90% errors are from
Supplementary Data Table 6. The paper adopted 10% age uncertainties for the first
two stars in its analysis. For PSR J0205+6449, the SN 1181 association is disputed.
The published age remains in the literature records, and the default comparison
omits this source. Ritter et al. identify Pa 30 with SN 1181, and Bietenholz's
radio expansion measurements indicate a much longer timescale for 3C 58.
Vela Jr also has distinct cool and total luminosities
from Ho et al., at 1.41 kpc. The comparison uses the Ho cool component and the
1.6–3.3 kyr age from Suherli et al. The Ho/Allen 2.4–5.1 kyr range stays in the
measurements. The full 70-object sample mentioned in Marino et al. was not available
as a verified data table for this update.

## Rebuild

```bash
python3 -m pip install -r requirements.txt
bash run_all.sh
```

The build uses the archived web snapshot dated 2026-08-03. It runs offline.
LibreOffice recalculates the audit workbook. Set `SKIP_TEX=1` to skip rebuilding
the PDF, or use `pdflatex` with the LaTeX packages listed in `notes/template.tex`.

Edit the original transcriptions in `src/build_workbook.py` and the supplementary
inputs in `data/raw/`. `src/catalogue.py` defines the normalized records and
selection rule. The scripts regenerate the CSVs, workbook, Python module, figures
and notes. See [the data dictionary](docs/DATA_DICTIONARY.md) for conventions and
remaining source-specific caveats.
