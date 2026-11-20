"""Export display values plus provenance; no probabilistic interpretation implied."""
from pathlib import Path
import csv,json
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED=set(json.loads((ROOT/'data/excluded_sources.json').read_text())['sources'])

def main():
 with (ROOT/'data/measurements.csv').open() as f: rows=list(csv.DictReader(f))
 decisions=json.loads((ROOT/'data/review_decisions.json').read_text())['sources']
 groups=defaultdict(list)
 for r in rows:
  if (r['class'] in ('RPP','XINS','UL','Hot-spot PSR') or r['source_id'] in ('3','13')) and r['source_id'] not in EXCLUDED:groups[r['source_id']].append(r)
 result=[]
 for sid,options in groups.items():
  r=next(x for x in options if x['reference']=='WEB').copy();age_ref='WEB';basis='independent'
  if not r['age_yr']:
   other=[x for x in options if x['age_yr'] and x['reference'] in ('V13','P20')]
   if other:
    for k in ['age_yr','age_yr_lo','age_yr_hi']:r[k]=other[-1][k]
    age_ref=other[-1]['reference']
   else:r['age_yr']=r['tau_c_yr'];r['age_yr_lo']=r['age_yr_hi']='';basis='characteristic'
  status='not_yet_reviewed';notes='Original catalogue conventions; see measurement records.'
  if sid=='3':
   d=decisions[sid];r['age_yr']=d['display_age_yr'];r['age_yr_lo']=d['display_age_yr_lo'];r['age_yr_hi']=d['display_age_yr_hi']
   r['L_inf_erg_s']=d['display_L_inf_erg_s'];r['L_inf_erg_s_lo']=d['display_L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['display_L_inf_erg_s_hi']
   status=d['status'];notes=d['notes'];age_ref='REVIEW_ADOPTED'
  elif sid=='16':
   d=decisions[sid];r['age_yr']=d['display_marker_age_yr'];r['age_yr_lo']=d['age_yr_lo'];r['age_yr_hi']=d['age_yr_hi']
   r['L_inf_erg_s']=d['fiducial_L_inf_erg_s'];r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   status=d['status'];notes=d['notes'];age_ref='REVIEW_ADOPTED'
  elif sid=='13':
   d=decisions[sid];r['age_yr']=d['display_marker_age_yr'];r['age_yr_lo']=d['age_yr_lo'];r['age_yr_hi']=d['age_yr_hi']
   r['L_inf_erg_s']=d['fiducial_L_inf_erg_s'];r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   status=d['status'];notes=d['notes'];age_ref='REVIEW_ACCEPTED_CATALOGUE_EPOCH'
  elif sid in ('17','30','46','48'):
   d=decisions[sid];r['age_yr_lo']=d['age_yr_lo'];r['age_yr_hi']=d['age_yr_hi']
   if sid=='17':
    r['age_yr']=d['display_marker_age_yr'];r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   if sid=='30':
    r['L_inf_erg_s']=d['L_inf_erg_s_upper_limit'];r['L_inf_erg_s_lo']='';r['L_inf_erg_s_hi']='';r['luminosity_upper_limit']='True';r['class']='UL'
   status=d['status'];notes=d['notes'];age_ref='REVIEW'
  elif sid=='14':
   d=decisions[sid];r['age_yr_lo']=d['age_yr_lo'];r['age_yr_hi']=d['age_yr_hi']
   r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   status=d['status'];notes=d['notes'];age_ref='REVIEW_PROVISIONAL'
  elif sid in ('20','21'):
   d=decisions[sid];r['age_yr_lo']=d['age_yr_lo'];r['age_yr_hi']=d['age_yr_hi']
   r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   status=d['status'];notes=d['notes']+' Marker retained from WEB, not a new best estimate.';age_ref='REVIEW'
  elif sid=='33':
   d=decisions[sid];r['age_yr']=d['display_marker_age_yr'];r['age_yr_lo']=d['display_age_yr_lo'];r['age_yr_hi']=d['display_age_yr_hi']
   r['L_inf_erg_s']=d['fiducial_L_inf_erg_s'];r['L_inf_erg_s_lo']=d['L_inf_erg_s_lo'];r['L_inf_erg_s_hi']=d['L_inf_erg_s_hi']
   status=d['status'];notes=d['notes'];age_ref='DISPLAY_PLACEHOLDER'
  result.append(dict(source_id=sid,name=r['name'],source_class=r['class'],age_basis=basis,age_reference=age_ref,display_age_yr=r['age_yr'],age_yr_lo=r['age_yr_lo'],age_yr_hi=r['age_yr_hi'],L_inf_erg_s=r['L_inf_erg_s'],L_inf_erg_s_lo=r['L_inf_erg_s_lo'],L_inf_erg_s_hi=r['L_inf_erg_s_hi'],luminosity_upper_limit=r['luminosity_upper_limit'],review_status=status,notes=notes))
 assert len(result)==41 and len({r['source_id'] for r in result})==41
 out=ROOT/'data/current_plot_sample.csv'
 with out.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=result[0],lineterminator='\n');w.writeheader();w.writerows(result)
 print('Exported 41 display records:',out.name)
if __name__=='__main__':main()
