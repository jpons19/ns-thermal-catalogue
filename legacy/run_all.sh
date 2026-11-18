#!/usr/bin/env bash
# Rebuild everything from the raw web page and the transcribed tables.
# Requirements: python3 (numpy, scipy, matplotlib, openpyxl), LibreOffice (soffice) for the recalc step,
#               pdflatex for the notes (optional; set SKIP_TEX=1 to skip).
set -euo pipefail
cd "$(dirname "$0")"
python3 src/parse_web.py                              # data/raw/Cooling_NS.html -> data/web_table.json
python3 src/build_workbook.py                         # transcribed tables + web -> data/NS_thermal_crossmatch.xlsx
python3 src/recalc_xlsx.py data/NS_thermal_crossmatch.xlsx
python3 src/gen_data_module.py                        # workbook -> data/ns_cooling_data.py
python3 src/plot_data_vs_age.py                       # figures/luminosity_vs_age.png, temperature_vs_age.png
python3 src/plot_old_stars_taud_scan.py --taud 1e5 3e5 1e6
python3 src/plot_taud_group.py --taud 3e5
python3 src/calc_estimates.py                         # data/derived/calc.json (estimates quoted in the notes)
python3 src/gen_notes_tex.py                          # notes/ns_thermal_data_notes.tex
if [ "${SKIP_TEX:-0}" != "1" ] && command -v pdflatex >/dev/null; then
  (cd notes && pdflatex -interaction=nonstopmode ns_thermal_data_notes.tex >/dev/null && pdflatex -interaction=nonstopmode ns_thermal_data_notes.tex >/dev/null \
   && rm -f *.aux *.log *.out *.toc)
fi
echo "done"
