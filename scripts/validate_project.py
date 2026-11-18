"""Validate release integrity, source ranges and internal static-site links."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import csv,json
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
 assert b['distance_kpc']==3.1 and b['status']=='provisional_age_unresolved'
 with (ROOT/'data/current_plot_sample.csv').open() as f:sample=list(csv.DictReader(f))
 assert len(sample)==40 and len({x['source_id'] for x in sample})==40
 vv=next(x for x in sample if x['source_id']=='21');assert float(vv['L_inf_erg_s_lo'])==v['L_inf_erg_s_lo']
 assert all(x['source_class'] in ('RPP','XINS','UL','Hot-spot PSR') for x in sample)
 path=ROOT/'docs/index.html';p=Page();p.feed(path.read_text())
 assert len(p.ids)==len(set(p.ids))
 for t in ['details','table']:assert p.starts[t]==p.ends[t],t
 for link in p.links:
  if '://' in link or link.startswith(('mailto:','data:')):continue
  if link.startswith('#'):assert link[1:] in p.ids,link;continue
  target=path.parent/link.split('#')[0].split('?')[0];assert target.exists(),link
 assert (ROOT/'data/raw/marino2024_sources.json').exists()
 print('Validated 40 source records, adopted decisions, HTML structure and internal links.')
if __name__=='__main__':main()
