"""Render two offline catalogues with numerical, colour-coded audit cells."""
from pathlib import Path
import csv,html,json,math,re
ROOT=Path(__file__).resolve().parents[1]
QUANTITIES=('age','distance','flux','temperature','field')
LABELS={'age':'Age (kyr)','distance':'Distance (kpc)','flux':'Thermal flux','temperature':'kT∞ (eV)','field':'Bdip (10¹² G)'}
HEADERS={'age':'Age · kyr','distance':'Distance · kpc','flux':'Fbol · 10⁻¹³ cgs','temperature':'kT∞ · eV','field':'Bdip · 10¹² G'}
def num(x):
 if x is None:return '—'
 return f'{x:.3g}'
def value(x):
 try:return float(x) if x!='' and x is not None else None
 except (ValueError,TypeError):return None
def interval(center,lo,hi,scale=1,upper=False):
 center,lo,hi=[value(x) for x in (center,lo,hi)]
 if upper:return '&lt; '+num((center if center is not None else hi)/scale) if center is not None or hi is not None else '—'
 if lo is not None and hi is not None:return num(lo/scale) if lo==hi else num(lo/scale)+'–'+num(hi/scale)
 return num(center/scale) if center is not None else '—'

def main():
 data=json.loads((ROOT/'data/quantity_assessments.json').read_text());assessments=data['sources'];status_labels=data['status_labels']
 decisions=json.loads((ROOT/'data/review_decisions.json').read_text())['sources'];fields=json.loads((ROOT/'data/magnetic_field_estimates.json').read_text())['sources']
 with (ROOT/'data/measurements.csv').open() as f:measurements=list(csv.DictReader(f))
 records={}
 for sid in assessments:
  rows=[r for r in measurements if r['source_id']==sid]
  records[sid]=next((r for ref in ('WEB','P20','V13') for r in rows if r['reference']==ref),rows[0])
 def numbers(sid):
  r=records[sid];d=decisions.get(sid,{});out={};extra={}
  age=[r[k] for k in ('age_yr','age_yr_lo','age_yr_hi')];abasis=r['reference']
  if 'age_yr_lo' in d:age=[d.get('display_marker_age_yr',age[0]),d['age_yr_lo'],d['age_yr_hi']];abasis='Adopted'
  elif 'display_age_yr_lo' in d:age=[d.get('display_marker_age_yr',d.get('display_age_yr',age[0])),d['display_age_yr_lo'],d['display_age_yr_hi']];abasis='Provisional'
  if value(age[0]) is None and value(age[1]) is None:
   # Some WEB rows lack ages supplied by an earlier compilation.
   older=next((x for x in measurements if x['source_id']==sid and value(x['age_yr']) is not None),None)
   if older:age=[older[k] for k in ('age_yr','age_yr_lo','age_yr_hi')];abasis=older['reference']
   elif value(r['tau_c_yr']) is not None:age=[r['tau_c_yr'],None,None];abasis='τc proxy'
  out['age']=(interval(*age,scale=1e3),abasis)
  dist=[r[k] for k in ('distance_kpc','distance_kpc_lo','distance_kpc_hi')];dbasis=r['reference']
  if 'distance_kpc_lo' in d:dist=[d.get('distance_kpc',(d['distance_kpc_lo']+d['distance_kpc_hi'])/2),d['distance_kpc_lo'],d['distance_kpc_hi']];dbasis='Adopted'
  out['distance']=(interval(*dist),dbasis)
  L=[r[k] for k in ('L_inf_erg_s','L_inf_erg_s_lo','L_inf_erg_s_hi')];ul=r['luminosity_upper_limit']=='True';lbasis=r['reference']
  if 'L_inf_erg_s_upper_limit' in d:L=[d['L_inf_erg_s_upper_limit'],None,None];ul=True;lbasis='Adopted limit'
  elif 'L_inf_erg_s_lo' in d:L=[d.get('fiducial_L_inf_erg_s',L[0]),d['L_inf_erg_s_lo'],d['L_inf_erg_s_hi']];lbasis='Adopted L∞' if sid!='33' else 'Provisional L∞'
  elif 'display_L_inf_erg_s_lo' in d:L=[d['display_L_inf_erg_s'],d['display_L_inf_erg_s_lo'],d['display_L_inf_erg_s_hi']];lbasis='Provisional L∞'
  # This diagnostic holds one distance fixed; never combine independent L/d
  # endpoints into an unsupported flux confidence interval.
  d0=value(d.get('luminosity_reference_distance_kpc',dist[0]));Ltext=interval(*L,scale=1e32,upper=ul)
  if d0 and d0>0:
   factor=4*math.pi*(d0*3.0856775814913673e21)**2*1e-13
   F=interval(*L,scale=factor,upper=ul);out['flux']=(F,f'L∞/10³²: {Ltext}')
   extra['flux']=f'{lbasis}; Fbol is calculated as L∞/(4πd₀²), holding d₀={d0:.3g} kpc fixed. These endpoints are a luminosity-envelope conversion, not an independently measured flux interval or a joint distance/flux confidence interval. Distance-dependent scenarios require their own spectral fits.'
  else:
   out['flux']=(Ltext,'L∞ / 10³² erg/s');extra['flux']='Flux unavailable without a usable reference distance; cell instead displays luminosity with its explicit unit.'
  temp=[r[k] for k in ('kT_inf_eV','kT_inf_eV_lo','kT_inf_eV_hi')]
  if 'temperature_upper_limit_eV' in d:
   out['temperature']=(interval(d['temperature_upper_limit_eV'],None,None,upper=True),'whole-surface limit')
  else:out['temperature']=(interval(*temp,upper=r['temperature_upper_limit']=='True'),r['reference']+' fit')
  extra['temperature']='No new temperature was adopted with the luminosity envelope. Display is the selected catalogue fit/component; it is not automatically a whole-surface effective temperature.'
  if 'temperature_upper_limit_eV' in d:extra['temperature']='Published whole-surface 3-sigma BB temperature ceiling 0.78 MK, converted using k_B; radius fixed at 12 km and reference distance 2 kpc. This replaces the hot-spot temperature in the overview only.'
  b=fields[sid];out['field']=(num(value(b['B_dip_G'])/1e12) if value(b['B_dip_G']) is not None else '—','dipole estimate' if b['B_dip_G'] else 'not measured');extra['field']=b['reference']
  return out,extra
 def render_page(path):
  doc=path.read_text()
  def source(match):
   sid=match[1];body=match[0];assessment=assessments[sid];values,extras=numbers(sid)
   body=re.sub(r' data-(?:age|distance|flux|temperature|field)-status="[^"]*"','',body)
   attrs=''.join(f' data-{k}-status="{assessment[k]["status"]}"' for k in QUANTITIES);body=body.replace(f'id="source-{sid}"',f'id="source-{sid}"'+attrs,1)
   spans=[]
   for k in QUANTITIES:
    status=assessment[k]['status'];reason=assessment[k]['reason']+' '+extras.get(k,'');v,basis=values[k]
    spans.append(f'<span class="quantity-cell" data-quantity="{k}" title="{html.escape(status_labels[status]+": "+reason,quote=True)}"><span class="quantity-label">{LABELS[k]}</span><span class="status {status}" aria-label="{html.escape(LABELS[k]+": "+html.unescape(v)+"; "+status_labels[status],quote=True)}">{v}</span><small class="value-basis">{basis}</small></span>')
   # Replace the complete middle of the source summary; nested numerical markup
   # cannot safely be removed by a shortest-span expression.
   a=body.index('<summary>');b=body.index('</summary>',a);summary=body[a:b]
   start=summary.index('<span class="quantity-cell"');end=summary.index('<span class="refset">',start)
   summary=summary[:start]+''.join(spans)+summary[end:];body=body[:a]+summary+body[b:]
   body=re.sub(r'<section class="quantity-notes"[\s\S]*?</section>\s*','',body)
   notes='<section class="quantity-notes" aria-label="Assessment by quantity"><h3>Values, provenance and assessment</h3><dl>'+''.join(f'<div><dt>{LABELS[k]} <span class="status {assessment[k]["status"]}">{status_labels[assessment[k]["status"]]}</span></dt><dd>{assessment[k]["reason"]} {html.escape(extras.get(k,""))}</dd></div>' for k in QUANTITIES)+'</dl></section>'
   body=body.replace('<h3>Reported measurements</h3>',notes+'\n<h3>Reported measurements</h3>',1)
   return body
  pattern=r'<details class="source" id="source-(\d+)"[\s\S]*?(?=<details class="source"|<p class="empty")';doc,n=re.subn(pattern,source,doc)
  head='<div class="row-head" aria-hidden="true"><span>Source</span><span>Type</span>'+''.join(f'<span>{HEADERS[k]}</span>' for k in QUANTITIES)+'<span>References</span><span>Cooling comparison</span></div>'
  doc=re.sub(r'<div class="row-head"[\s\S]*?</div>',lambda m:head,doc,count=1)
  doc=doc.replace('<details class="overview" open>','<details class="overview">')
  if path.name=='index.html' and 'class="plot-preview"' not in doc:
   doc=re.sub(r'(<a href="figures/ns_velajr_with_cooling.png"><img[\s\S]*?</a>)',r'<details class="plot-preview"><summary>Show luminosity–age plot</summary>\1</details>',doc,count=1)
  doc=doc.replace('How to read the four assessments','How to read the values and colours')
  doc=doc.replace('separate <b>age, distance, flux and temperature</b> assessments','separate <b>age, distance, flux, temperature and magnetic-field</b> assessments')
  doc=doc.replace('read all four explanations','read all five explanations')
  marker='<p class="numeric-conventions">'
  doc=re.sub(r'<p class="numeric-conventions">[\s\S]*?</p>\s*','',doc)
  explanation=marker+'<b>Numbers inside the coloured cells:</b> accepted review ranges take precedence; otherwise the named catalogue fit is shown. Age marked τc is a spin-down proxy. Flux is a <b>derived diagnostic</b> in 10⁻¹³ erg cm⁻² s⁻¹ at one stated reference distance; the accompanying L∞ range is in 10³² erg/s. It is not a new flux measurement or a common-confidence interval. Temperature remains fit/component dependent. Bdip is an equatorial canonical dipole estimate in 10¹² G; V13 polar estimates are divided by two. Missing fields remain blank (—). Hover or expand for status and provenance.</p>\n'
  doc=doc.replace('<section class="filter-panel"',explanation+'<section class="filter-panel"',1)
  doc=re.sub(r'<label>Quantity<select id="quantity">[\s\S]*?</select></label>','<label>Quantity<select id="quantity"><option value="">Any quantity</option>'+''.join(f'<option value="{k}">{LABELS[k]}</option>' for k in QUANTITIES)+'</select></label>',doc,count=1)
  doc=doc.replace('["age","distance","flux","temperature"]','["age","distance","flux","temperature","field"]')
  doc=re.sub(r'\n*/\* Per-quantity assessment layout;[\s\S]*?(?=</style>)','',doc)
  style='''
/* Per-quantity assessment layout; five numerical columns. */
main{max-width:1720px}.catalogue-nav{display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}.catalogue-nav a{padding:8px 13px;border:1px solid var(--line);border-radius:8px;background:#fff;font-weight:650}.numeric-conventions{padding:12px 18px;font-size:.83rem;color:var(--muted)}
.filters{grid-template-columns:minmax(180px,1.5fr) repeat(5,minmax(110px,1fr))}
.row-head,details.source>summary{grid-template-columns:minmax(205px,1.7fr) minmax(110px,.9fr) repeat(2,minmax(90px,.7fr)) minmax(132px,1fr) repeat(2,minmax(95px,.75fr)) minmax(95px,.8fr) minmax(105px,.85fr);gap:10px}
.quantity-cell{display:flex;flex-direction:column;align-items:flex-start;gap:4px;min-width:0}.quantity-label{display:none}.quantity-cell .status{font-size:.85rem;padding:4px 8px;font-variant-numeric:tabular-nums;white-space:normal}.value-basis{display:block;font-size:.65rem;color:var(--muted);line-height:1.35;overflow-wrap:anywhere}.quantity-notes{margin:14px 0;padding:12px 14px;background:#f5f8f7;border:1px solid var(--line);border-radius:8px}.quantity-notes dl{display:grid;grid-template-columns:1fr 1fr;gap:12px 20px;margin:0}.quantity-notes dt{font-weight:700}.quantity-notes dd{margin:5px 0 0;font-size:.85rem;color:var(--muted)}
@media(max-width:1300px){.filters{grid-template-columns:repeat(3,minmax(0,1fr))}.row-head{display:none}details.source>summary{grid-template-columns:repeat(5,minmax(0,1fr));gap:9px 12px}.name{grid-column:span 3;grid-row:auto}.type{grid-column:span 2}.quantity-label{display:block;font-size:.72rem;color:var(--muted);font-weight:650}.refset{grid-column:span 3}.sample{grid-column:span 2}}
@media(max-width:570px){.filters{grid-template-columns:1fr 1fr}details.source>summary{grid-template-columns:repeat(3,minmax(0,1fr));padding:12px 10px;gap:10px}.name,.type{grid-column:1/-1;padding-left:17px}.quantity-cell .status{font-size:.77rem;padding:4px 6px}.quantity-label{font-size:.68rem}.refset{grid-column:span 2}.sample{grid-column:span 1;font-size:.72rem}.quantity-notes dl{grid-template-columns:1fr}}
@media print{.status{print-color-adjust:exact;-webkit-print-color-adjust:exact}.row-head{display:none}details.source>summary{grid-template-columns:repeat(5,1fr)}.name{grid-column:span 3}.type{grid-column:span 2}.quantity-label{display:block}}
'''
  doc=doc.replace('</style>',style+'</style>',1);path.write_text(doc);print(f'Rendered {n} sources in {path.name}.');return set(re.findall(r'<details class="source" id="source-(\d+)"',doc))
 ids=set()
 for name in ['index.html','magnetar.html']:ids|=render_page(ROOT/'docs'/name)
 assert ids==set(assessments)
if __name__=='__main__':main()
