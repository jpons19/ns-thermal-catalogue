"""Rebuild current display data, figures and HTML entirely offline."""
from pathlib import Path
import shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 for script,args in [('export_plot_sample.py',[]),('plot_ns_sources.py',[]),('plot_ns_sources.py',['--original-catalogue'])]:
  subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)
 shutil.copyfile(ROOT/'README.md',ROOT/'docs/project_readme.md')
 shutil.copyfile(ROOT/'figures/ns_vela_revised_errors.png',ROOT/'docs/figures/ns_vela_revised_errors.png')
 subprocess.run([sys.executable,str(ROOT/'scripts/update_catalogue.py')],cwd=ROOT,check=True)
 print('Current outputs rebuilt; legacy files unchanged.')
if __name__=='__main__':main()
