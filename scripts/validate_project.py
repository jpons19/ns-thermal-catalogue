"""Validate release integrity, source ranges and internal static-site links."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import csv,json,shutil,subprocess,sys,tempfile
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.starts=Counter();self.ends=Counter()
 def handle_starttag(self,t,attrs):
  self.starts[t]+=1
  for k,v in attrs:
   if k=='id':self.ids.append(v)
   if k in ('href','src') and v:self.links.append(v)
 def handle_endtag(self,t):self.ends[t]+=1

def main():
 r=json.loads((ROOT/'data/review_decisions.json').read_text())['sources'];v=r['21'];b=r['33']
 assert v['age_yr_lo']==11000 and v['age_yr_hi']==40000
 assert v['L_inf_erg_s_lo']==2e32 and v['L_inf_erg_s_hi']==4.4e32
 m=r['20'];assert m['age_yr_lo']==70000 and m['age_yr_hi']==120000
 assert m['L_inf_erg_s_lo']==2.5e32 and m['L_inf_erg_s_hi']==9e32
 j=r['14'];assert (j['age_yr_lo'],j['age_yr_hi'],j['L_inf_erg_s_lo'],j['L_inf_erg_s_hi'])==(800,7000,8e31,3.4e32)
 assert (ROOT/'figures/ns_velajr_with_cooling.png').exists()
 curves=np.genfromtxt(ROOT/'data/cooling_five_eos.csv',delimiter=',',names=True,dtype=None,encoding='utf-8')
 models=np.array([name.removesuffix('_Lmin1e30') for name in curves['model']])
 assert set(models)=={'BSk22','BSk24','BSk25*','BSk26','DDFGOS(APR)*'}
 for model in ['BSk22','BSk24','BSk25*','BSk26','DDFGOS(APR)*']:
  c=curves[models==model];assert np.all(np.diff(c['time_years'])>0)
  assert np.all(np.isfinite(c['L_infinity_erg_s'])) and np.all(c['L_infinity_erg_s']>0)
  assert c['L_infinity_erg_s'][-1]<1e30
 assert b['distance_kpc']==3.1 and b['status']=='provisional_age_unresolved'
 with (ROOT/'data/current_plot_sample.csv').open() as f:sample=list(csv.DictReader(f))
 assert len(sample)==41 and len({x['source_id'] for x in sample})==41
 vv=next(x for x in sample if x['source_id']=='21');assert float(vv['L_inf_erg_s_lo'])==v['L_inf_erg_s_lo']
 assert all(x['source_class'] in ('RPP','XINS','UL','Hot-spot PSR') or x['source_id'] in ('3','13') for x in sample)
 c=next(x for x in sample if x['source_id']=='13');assert float(c['age_yr_lo'])==307 and float(c['age_yr_hi'])==345
 assert float(c['L_inf_erg_s_lo'])==5.6e33 and float(c['L_inf_erg_s_hi'])==9.3e33
 with (ROOT/'data/sources.csv').open() as f: active=list(csv.DictReader(f))
 assert len(active)==74 and not {'1','204','205'} & {x['source_id'] for x in active}
 assert not {'1','204','205'} & {x['source_id'] for x in sample}
 all_ids=set()
 for name,expected in [('index.html',57),('magnetar.html',17)]:
  path=ROOT/'docs'/name;p=Page();p.feed(path.read_text())
  assert len(p.ids)==len(set(p.ids))
  source_ids={i for i in p.ids if i.startswith('source-')};assert len(source_ids)==expected
  assert not all_ids & source_ids;all_ids|=source_ids
  assert not {'source-1','source-204','source-205'} & source_ids
  for t in ['details','table']:assert p.starts[t]==p.ends[t],t
  for link in p.links:
   if '://' in link or link.startswith(('mailto:','data:')):continue
   if link.startswith('#'):assert link[1:] in p.ids,link;continue
   target=path.parent/link.split('#')[0].split('?')[0];assert target.exists(),link
 assert len(all_ids)==74
 assert (ROOT/'data/raw/marino2024_sources.json').exists()
 # Re-run the deterministic data and HTML generators in an isolated copy, so
 # validation detects stale generated files without changing the working tree.
 with tempfile.TemporaryDirectory() as tmp:
  tmp_root=Path(tmp)
  for directory in ('scripts','data','docs'):
   shutil.copytree(ROOT/directory,tmp_root/directory)
  for script in ('export_plot_sample.py','update_catalogue.py'):
   subprocess.run([sys.executable,str(tmp_root/'scripts'/script)],cwd=tmp_root,check=True,stdout=subprocess.DEVNULL)
  for relative in ('data/current_plot_sample.csv','docs/index.html','docs/magnetar.html'):
   assert (ROOT/relative).read_bytes()==(tmp_root/relative).read_bytes(), f'Stale generated file: {relative}; run python scripts/rebuild.py'
  assert (ROOT/'README.md').read_bytes()==(ROOT/'docs/project_readme.md').read_bytes(), 'Stale docs/project_readme.md; run python scripts/rebuild.py'
 print('Validated 41 source records, generated data and HTML, and internal links.')
if __name__=='__main__':main()
