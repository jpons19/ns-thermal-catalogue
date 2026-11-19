"""Rebuild current display data, figures and HTML entirely offline."""
from pathlib import Path
import shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
 for script,args in [('export_plot_sample.py',[]),('plot_ns_sources.py',[]),('plot_ns_sources.py',['--cooling-curves']),('plot_ns_sources.py',['--original-catalogue','--cooling-curves'])]:
  subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,check=True)
 for name in ['ns_velajr_with_cooling.png','ns_original_with_cooling.png']:
  shutil.copyfile(ROOT/'figures'/name,ROOT/'docs/figures'/name)
 shutil.copyfile(ROOT/'README.md',ROOT/'docs/project_readme.md')
 shutil.copyfile(ROOT/'figures/ns_monogem_revised_errors.png',ROOT/'docs/figures/ns_monogem_revised_errors.png')
 subprocess.run([sys.executable,str(ROOT/'scripts/update_catalogue.py')],cwd=ROOT,check=True)
 print('Current outputs rebuilt; legacy files unchanged.')
if __name__=='__main__':main()
