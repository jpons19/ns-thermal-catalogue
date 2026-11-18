"""Recalculate all formulas of an .xlsx with headless LibreOffice so that cached values exist
(the plotting/data scripts read the workbook with data_only=True).  Usage: python3 recalc_xlsx.py file.xlsx"""
import subprocess, sys, shutil, tempfile
from pathlib import Path
f = Path(sys.argv[1]).resolve()
soffice = shutil.which("soffice") or shutil.which("libreoffice")
if not soffice:
    sys.exit("LibreOffice (soffice) not found; open the workbook once in Excel/LibreOffice and save it instead.")
with tempfile.TemporaryDirectory() as d:
    subprocess.run([soffice, "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", d, str(f)], check=True, capture_output=True)
    shutil.copy(Path(d) / f.name, f)
from openpyxl import load_workbook
wb = load_workbook(f, data_only=True); bad = 0
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            if c.data_type == "e":
                bad += 1
                print("error cell", ws.title, c.coordinate, c.value)
print("recalculated", f.name, "- error cells:", bad)
if bad:
    sys.exit(1)
