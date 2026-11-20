"""Synchronize reviewed source discussions from the audit into the static HTML."""
from pathlib import Path
import re,html,json
ROOT=Path(__file__).resolve().parents[1]

def inline(t):
 t=html.escape(t)
 t=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<a href="\2">\1</a>',t)
 t=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',t)
 return t

def render(md):
 out=[];para=[];inlist=False
 def flush():
  if para:out.append('<p>'+inline(' '.join(para))+'</p>');para.clear()
 for line in md.splitlines():
  if not line.strip():flush();continue
  if line.startswith('#'):
   flush()
   if inlist:out.append('</ul>');inlist=False
   n=min(6,len(line)-len(line.lstrip('#'))+1);out.append(f'<h{n}>'+inline(line.lstrip('# ').strip())+f'</h{n}>')
  elif line.startswith('- '):
   flush()
   if not inlist:out.append('<ul>');inlist=True
   out.append('<li>'+inline(line[2:])+'</li>')
  else:
   if inlist:out.append('</ul>');inlist=False
   para.append(line)
 flush()
 if inlist:out.append('</ul>')
 return '\n'.join(out)

def main():
 audit=(ROOT/'docs/ns_thermal_literature_audit.md').read_text()
 path=ROOT/'docs/index.html';doc=path.read_text();r=json.loads((ROOT/'data/review_decisions.json').read_text());decisions=r['sources']
 for sid,heading,nextheading in [(30,'## B1951+32','## IC 443'),(17,'## IC 443','## B1727−47'),(48,'## B1727−47','## J0007+7303'),(46,'## J0007+7303','## Vela Jr'),(3,'## Vela Jr','## Cas A'),(13,'## Cas A','## 1. PSR J0205'),(14,'## 1. PSR J0205','## 2. PSR B2334'),(20,'## 4. Monogem','## 5. S147'),(21,'## 3. Vela pulsar','## 4. Monogem'),(33,'## 2. PSR B2334','## 3. Vela pulsar')]:
  a=audit.index(heading);b=audit.index(nextheading,a);discussion=render(audit[a:b]);d=decisions.get(str(sid),{})
  pat=rf'(<details class="source" id="source-{sid}"[\s\S]*?<div class="inside">)([\s\S]*?)(?=<h3>Reported measurements</h3>)'
  match=re.search(pat,doc)
  if not match:raise ValueError(f'Cannot locate source panel {sid}')
  if sid==30:
   chosen="<p class='chosen'><b>Age adopted · 18 November 2026</b><br>Age: <b>45–85 kyr</b>; distance: <b>1–2 kpc</b>. Adopt whole-surface <b>L∞ &lt; 3.8 × 10³² erg/s</b>, retaining the published 3σ fixed-radius BB ceiling at 2 kpc. Plot: upper-limit arrow with age error bar; hot-spot detection preserved separately in historical records.</p>"
  elif sid==17:
   chosen="<p class='chosen'><b>Adopted review envelope</b><br>Age: <b>3–20 kyr</b>; distance: <b>1.6–1.7 kpc</b>. Chevalier's old estimate excluded; cooling-model ages excluded to avoid circularity. Age marker is the geometric midpoint for display. Luminosity: <b>(1.0–3.5) × 10³² erg/s</b>. Previous luminosity marker retained for comparison; spectral model and distance-scaling caveats remain.</p>"
  elif sid==46:
   chosen=f"<p class='chosen'><b>Adopted · 20 November 2026</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>. Nominal ceiling <b>L∞ &lt; {d['L_inf_erg_s_upper_limit']:.0e} erg/s</b> (NSA, local temperature, 10 km); conservative ceiling about <b>{d['L_inf_erg_s_upper_limit_conservative']:.0e} erg/s</b> (blackbody, 10 km physical radius), shown dotted. A newer reanalysis or an independent refit is recommended.</p>"
  elif sid==48:
   chosen=f"<p class='chosen'><b>Age range adopted · 18 November 2026</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>. Published luminosity ceiling retained; spectral provenance and component caveats remain.</p>"
  elif sid==3:
   chosen="<p class='chosen'><b>Age and cool-surface luminosity adopted</b><br>Age 1.6–5.1 kyr; Ho2026 cool-surface luminosity (1.3–4.0) × 10³² erg/s. Error bars only; Ho range spans model medians, not a common confidence interval. Distance <b>1.41 (1.27–1.55) kpc</b> (Suherli2026), adopted 20 November 2026. Older wind age and spectral assumptions remain caveats.</p>"
  elif sid==13:
   chosen="<p class='chosen'><b>Accepted reference · 18 November 2026</b><br>Age: <b>307–345 yr (reference epoch 2007)</b>; L∞: <b>(5.6–9.3) × 10³³ erg/s</b>. Point with error bars only; no shaded box.</p>"
  elif sid==14:
   chosen=f"<p class='chosen'><b>Selected review envelope · {r['review_date']}</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>. Luminosity: <b>({d['L_inf_erg_s_lo']/1e32:g}–{d['L_inf_erg_s_hi']/1e32:g}) × 10³² erg/s</b>; small-area lower edge removed. Marker at about 819 yr retained as a display location; SN 1181 not assumed. Correct characteristic age approximately 5.4 kyr.</p>"
  elif sid==20:
   chosen=f"<p class='chosen'><b>Adopted review envelope · {r['review_date']}</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>; luminosity: <b>({d['L_inf_erg_s_lo']/1e32:g}–{d['L_inf_erg_s_hi']/1e32:g}) × 10³² erg/s</b>. Upper bound deliberately retains the unresolved P20 compilation value. No common confidence level.</p>"
  elif sid==21:
   chosen=f"<p class='chosen'><b>Adopted review envelope · {r['review_date']}</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>; luminosity: <b>({d['L_inf_erg_s_lo']/1e32:g}–{d['L_inf_erg_s_hi']/1e32:g}) × 10³² erg/s</b>. V13 excluded from the adopted range; historical records retained. No common statistical confidence level.</p>"
  else:
   chosen=f"<p class='chosen'><b>Working review selection · {r['review_date']}</b><br>Distance: <b>{d['distance_kpc']:g} kpc ({d['distance_kpc_lo']:g}–{d['distance_kpc_hi']:g})</b>; provisional luminosity envelope: <b>{d['L_inf_erg_s_lo']:.2g}–{d['L_inf_erg_s_hi']:.2g} erg/s</b>. Age unresolved at the adopted distance. Discussion closed for now.</p>"
  doc=doc[:match.start(2)]+chosen+'<details class="review-discussion" open><summary><b>Updated literature discussion and decisions</b></summary>'+discussion+'</details>\n'+doc[match.end(2):]
 banner='''<section id="review-deliverables" class="overview"><h2>Current review · 18 November 2026</h2><p><a href="ns_thermal_literature_audit.md">Full literature audit (Markdown)</a> · <a href="project_readme.md">Project README</a></p><p>Vela Jr: age 1.6–5.1 kyr adopted; thermal branches kept separate. Cas A: accepted reference with error bars only. J0205: adopted luminosity envelope with provisional age. Monogem and Vela: adopted review envelopes. B2334+61: provisional age at adopted distance. Other points retain their catalogue assumptions. Cooling curves: BSk22, BSk24, BSk25*, BSk26 and DDFGOS(APR)*, all at 1.4 M☉ with a Gudmundsson envelope, extended to L∞ &lt; 10³⁰ erg/s; asterisks indicate provisional EOS treatment; true age on both panels, with characteristic age used only as a proxy.</p><a href="figures/ns_velajr_with_cooling.png"><img src="figures/ns_velajr_with_cooling.png" alt="Luminosity-age catalogue with J0205 uncertainty box and five 1.4-solar-mass cooling tracks" style="max-width:100%;height:auto"></a><details><summary>Original catalogue values with the same cooling tracks</summary><img src="figures/ns_original_with_cooling.png" alt="Original catalogue with reference cooling curves" style="max-width:100%;height:auto"></details></section>'''
 if 'id="review-deliverables"' in doc:
  doc=re.sub(r'<section id="review-deliverables"[\s\S]*?</section>',lambda m:banner,doc,count=1)
 else:doc=doc.replace('</header>','</header>\n'+banner,1)
 doc=re.sub(r'(<details class="source" id="source-13"[\s\S]*?)(?=<details class="source" id="source-14")',lambda m:m[0].replace('data-status="open"','data-status="consistent"').replace('<span class="status open">Open discrepancy</span>','<span class="status consistent">Accepted reference</span>'),doc,count=1)
 path.write_text(doc)
 from update_quantity_assessments import main as update_quantities
 update_quantities()
 print('Synchronized Monogem, Vela and B2334 HTML discussions.')
if __name__=='__main__':main()
