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
 for sid,heading,nextheading in [(21,'## 3. Vela pulsar','## 4. Monogem'),(33,'## 2. PSR B2334','## 3. Vela pulsar')]:
  a=audit.index(heading);b=audit.index(nextheading,a);discussion=render(audit[a:b]);d=decisions[str(sid)]
  pat=rf'(<details class="source" id="source-{sid}"[\s\S]*?<div class="inside">)([\s\S]*?)(?=<h3>Reported measurements</h3>)'
  match=re.search(pat,doc)
  if not match:raise ValueError(f'Cannot locate source panel {sid}')
  if sid==21:
   chosen=f"<p class='chosen'><b>Adopted review envelope · {r['review_date']}</b><br>Age: <b>{d['age_yr_lo']/1e3:g}–{d['age_yr_hi']/1e3:g} kyr</b>; luminosity: <b>({d['L_inf_erg_s_lo']/1e32:g}–{d['L_inf_erg_s_hi']/1e32:g}) × 10³² erg/s</b>. V13 excluded from the adopted range; historical records retained. No common statistical confidence level.</p>"
  else:
   chosen=f"<p class='chosen'><b>Working review selection · {r['review_date']}</b><br>Distance: <b>{d['distance_kpc']:g} kpc ({d['distance_kpc_lo']:g}–{d['distance_kpc_hi']:g})</b>; provisional luminosity envelope: <b>{d['L_inf_erg_s_lo']:.2g}–{d['L_inf_erg_s_hi']:.2g} erg/s</b>. Age unresolved at the adopted distance. Discussion closed for now.</p>"
  doc=doc[:match.start(2)]+chosen+'<details class="review-discussion" open><summary><b>Updated literature discussion and decisions</b></summary>'+discussion+'</details>\n'+doc[match.end(2):]
 banner='''<section id="review-deliverables" class="overview"><h2>Current review · 18 November 2026</h2><p><a href="ns_thermal_literature_audit.md">Full literature audit (Markdown)</a> · <a href="project_readme.md">Project README</a></p><p>Vela: adopted review envelope. B2334+61: provisional age at adopted distance. Other points retain their catalogue assumptions.</p><a href="figures/ns_vela_revised_errors.png"><img src="figures/ns_vela_revised_errors.png" alt="Luminosity-age catalogue with adopted Vela and provisional B2334 uncertainty boxes" style="max-width:100%;height:auto"></a></section>'''
 if 'id="review-deliverables"' not in doc:doc=doc.replace('</header>','</header>\n'+banner,1)
 path.write_text(doc)
 print('Synchronized Vela and B2334 HTML discussions.')
if __name__=='__main__':main()
