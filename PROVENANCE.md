# Provenance and review state

Prepared 18 November 2026 from the supplied NS thermal catalogue project and the source-by-source review in this discussion.

## Imported inputs

- Complete original `ns_thermal_project.zip`, latest supplied revision, is preserved unpacked in `legacy/`. It contains the original workbook, CSVs, raw inputs, scripts, exploratory figures and LaTeX/PDF notes. These files have not been regenerated with the new source decisions.
- The current `data/measurements.csv` is byte-identical to the table in both the original project and the later plotting package. Original measurements remain historical records.
- The Potekhin website snapshot is dated **3 August 2026** in the supplied project. This packaging task did not refresh the external catalogue or perform another full literature audit.
- `data/raw/marino2024_sources.json` is the original requested three-source JSON from https://github.com/Blitzman/workshop_fisica/blob/main/observations/marino2024_sources.json.
- `docs/ns_thermal_literature_audit.md` includes all decisions through Monogem's accepted 70–120 kyr and (2.5–9.0) × 10³² erg/s envelope, including the unreconciled P20 value.
- `docs/index.html` is the updated source catalogue, retaining the reported-measurement tables and the revised Monogem/Vela/B2334 discussions.

## Main literature keys

| Key | Reference |
|---|---|
| V13 | Viganò et al. 2013, https://doi.org/10.1093/mnras/stt1008 |
| P20 | Potekhin et al. 2020, https://doi.org/10.1093/mnras/staa1871 |
| WEB | https://www.ioffe.ru/astro/NSG/thermal/cooldat.html (archived snapshot) |
| M24 | Marino et al. 2024, https://doi.org/10.1038/s41550-024-02291-y |

Primary references and table/section locators for individual sources appear in the audit and in `data/references.csv`. Literature PDFs collected while researching the audit are not redistributed in this repository; the original project's generated notes PDF is retained in `legacy/notes/`.

## Current versus historical calculations

`data/review_decisions.json` and the current audit define the review selections. The two initial B2334 comparison images in `figures/history/` are historical diagnostics; the earliest box includes alternatives later excluded. The default figure uses the accepted Monogem and Vela boxes and the provisional B2334 selection. Other plotted sources are unreviewed catalogue values.

The legacy workbook, data module and `cooling_comparison.csv` remain exploratory imported products. Their older selections, field-decay age diagnostics, source exclusions and figure conventions may differ from the present review. Do not treat them as synchronized current results. Running `legacy/run_all.sh` is a separate workflow with its original dependencies and tools, including optional LaTeX/LibreOffice steps.

The review envelope is a documented selection across interpretations, not an independent statistical confidence region. P20 and WEB often inherit the same underlying fits and must not be counted as independent observations. Characteristic ages, remnant ages and display-only age spans retain their distinct meanings.
