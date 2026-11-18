"""Fill notes/template.tex with the tables computed in calc.json and write notes/ns_thermal_data_notes.tex."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # project root
import json, math
R=json.load(open(ROOT/'data'/'derived'/'calc.json'))
def sci(x,d=2):
    if x is None: return "--"
    e=int(math.floor(math.log10(abs(x)))); mt=x/10**e
    return f"${mt:.{d}f}\\times10^{{{e}}}$"
def f2(x,d=2): return "--" if x is None else f"{x:.{d}f}"
def tab(cols,rows,head,caption,label,fmt="l"*0,size="\\small"):
    s=f"\\begin{{table}}[htbp]\n\\centering{size}\n\\caption{{{caption}}}\\label{{{label}}}\n\\begin{{adjustbox}}{{max width=\\textwidth}}\\begin{{tabular}}{{{cols}}}\n\\toprule\n{head}\\\\\n\\midrule\n"
    s+="\n".join(" & ".join(r)+"\\\\" for r in rows)
    s+="\n\\bottomrule\n\\end{tabular}\\end{adjustbox}\n\\end{table}\n"
    return s
T={}
# redshift
rows=[[f"{M}",f"{Rk}",f2(rg,2),f2(z,3),f2(Rinf,1),f2(rat,3)] for M,Rk,rg,z,Rinf,rat in R['red']]
T['RED']=tab("cccccc",rows,"$M\\,(M_\\odot)$ & $R$ (km) & $r_g$ (km) & $1+z_g$ & $R^\\infty$ (km) & $1-r_g/R$",
 "Redshift factors for representative masses and radii. $T^\\infty=T_{\\rm eff}/(1+z_g)$, $L^\\infty=L\\,(1-r_g/R)$, $R^\\infty=R(1+z_g)$. Ho+26 fix $M=1.4\\,M_\\odot$, $R=12$ km ($1+z_g=1.235$); V13 use $M=1.4\\,M_\\odot$, $R=11.6$ km.","tab:red")
# bb L
rows=[[f"{kT}",sci(T_),sci(L,2)] for kT,T_,L in R['bb']]
T['BB']=tab("ccc",rows,"$kT^\\infty$ (eV) & $T^\\infty$ (K) & $L_{\\rm BB}$ (erg\\,s$^{-1}$)",
 "Luminosity of a blackbody covering the whole star, $L=4\\pi (R^\\infty)^2\\sigma_{\\rm SB}(T^\\infty)^4$ with $R^\\infty=14.8$ km ($M=1.4\\,M_\\odot$, $R=12$ km). Atmospheres differ at fixed $T_{\\rm eff}$ in colour but not in $L$; the point is the $T^4$ scaling and the magnitude of luminosity that can hide in the extreme-UV.","tab:bb")
# fraction
rows=[[f"{kT}"]+[sci(x,1) if x<0.01 else f"{x:.3f}" for x in fr] for kT,fr in R['frac']]
T['FRAC']=tab("cccc",rows,"$kT^\\infty$ (eV) & $N_{\\rm H}=2\\times10^{21}$ & $4.7\\times10^{21}$ & $7\\times10^{21}$ cm$^{-2}$",
 "Fraction of the \\emph{bolometric} blackbody flux that is detected in the 0.5--8 keV band after interstellar absorption (approximate cross-section $\\sigma=2.4\\times10^{-22}E_{\\rm keV}^{-8/3}$ cm$^2$, no absorption edges; accurate to a few tens of per cent in this range). For $kT\\lesssim 60$ eV the detected fraction is $\\lesssim 10^{-3}$: the luminosity of a cool whole-surface component is essentially unconstrained by the X-ray data.","tab:frac")
rows=[[f"{E}"]+[sci(x,1) for x in tr] for E,tr in R['trans']]
T['TRANS']=tab("cccc",rows,"$E$ (keV) & $N_{\\rm H}=2\\times10^{21}$ & $4.7\\times10^{21}$ & $7\\times10^{21}$ cm$^{-2}$",
 "Transmission $e^{-N_{\\rm H}\\sigma(E)}$ with the same approximate cross-section. Typical $N_{\\rm H}$: $4.9\\times10^{21}$ (J0205+6449), $2.0\\times10^{21}$ frozen (B2334+61), $(4.3$--$4.7)\\times10^{21}$ (Vela Jr).","tab:trans")
# dist
rows=[[n.replace('&','\\&'),f"{lo:g}",f"{hi:g}",f2(dl,2),f"{10**dl:.0f}"] for n,lo,hi,dl,c in R['dist'][:10]]
T['DIST']=tab("lcccc",rows,"Source & $d_{\\min}$ (kpc) & $d_{\\max}$ (kpc) & $\\Delta\\log L=2\\log(d_{\\max}/d_{\\min})$ & $L_{\\max}/L_{\\min}$",
 "Luminosity range implied by the distance range alone (P20 / web ranges), ten largest cases; $L\\propto d^2$. Ranges are those transcribed in the cross-match workbook (some bounds for `$\\sim$' entries are mine).","tab:dist")
rows=[[a,b.replace('$\\pm$','$\\pm$'),f"{lo:g}--{hi:g}",f2(dl,2),f"{10**dl:.0f}"] for a,b,lo,hi,dl in R['comp']]
T['COMP']=tab("llccc",rows,"Source & Competing distance estimates (kpc) & Range used & $\\Delta\\log L$ & Factor",
 "Competing distance determinations for the three cold sources of M24 and the implied luminosity spread.","tab:comp")
# agesens
rows=[[f"{dt*100:.0f}\\%",f2(a,3),f2(b,3)] for dt,a,b in R['agesens']]
T['AGES']=tab("ccc",rows,"Fractional age error & $\\delta\\log L$ (modified Urca, $L\\propto t^{-0.37}$) & $\\delta\\log L$ (direct Urca, $L\\propto t^{-0.55}$)",
 "Shift of a model curve in luminosity produced by an age error, from the analytic slopes derived in Section~\\ref{sec:ages}. Compare with the luminosity errors of $0.15$--$0.5$ dex in Table~\\ref{tab:conf} and distance spreads in Tables~\\ref{tab:dist}--\\ref{tab:comp}.","tab:agesens")
# birth
rows=[]
for nm,P,tc,tl,th,p0a,p0b,na,nb in R['birth']:
    age=f"{tl:g}" if tl==th else f"{tl:g}--{th:g}"
    if p0a is not None:
        a,b=sorted([p0a,p0b]); p0=f"{a:.3g}" if abs(a-b)<5e-4 else f"{a:.3g}--{b:.3g}"
        rows.append([nm,f"{P:g}",f"{tc:g}",age,f"{tc/((tl+th)/2):.1f}",p0,f"{(a+b)/2/P:.2f}","--"])
    else:
        rows.append([nm,f"{P:g}",f"{tc:g}",age,f"{tc/((tl+th)/2):.2f}","not possible with $n=3$","--",f"{na:.2f}--{nb:.2f}"])
T['BIRTH']=tab("lcccccccc".replace("cccccccc","ccccccc"),rows,"Pulsar & $P$ (s) & $\\tau_c$ (kyr) & $t_*$ (kyr) & $\\tau_c/t_*$ & implied $P_0$ (s), $n=3$ & $P_0/P$ & $n$ needed if $P_0\\ll P$",
 "Birth periods and braking indices implied by independent ages. For $n=3$: $t=\\tau_c[1-(P_0/P)^2]$; if $t_*>\\tau_c$, a braking index below 3 is required, $n=1+2\\tau_c/t_*$ for $P_0\\ll P$. $\\tau_c$ from the P20 table; $t_*$ from P20/web.","tab:birth")
# decay generic
rows=[[f"{x:g}",f2(v,2)] for x,v in R['gen']]
T['GEN']=tab("cc",rows,"$x=t/\\tau_d$ & $\\tau_c/t=(e^{2x}-1)/(2x)$",
 "Bias of the characteristic age for exponential field decay $B\\propto e^{-t/\\tau_d}$ with $P_0\\ll P$ (Equation~\\ref{eq:decay}).","tab:gen")
rows=[[n,f"{tc:g}",f"{ts:g}",f2(r,2),f2(x,2),f"{td:.0f}"] for n,tc,ts,r,x,td in R['decay']]
T['DEC']=tab("lccccc",rows,"X-ray isolated neutron star & $\\tau_c$ (kyr) & $t_*$ (kyr) & $\\tau_c/t_*$ & $x=t/\\tau_d$ & $\\tau_d$ (kyr)",
 "Decay time $\\tau_d$ required to reconcile $\\tau_c$ and $t_*$ if field decay were the only effect (equation~\\ref{eq:decay}); $P_0$ is irrelevant for $P\\sim10$ s. The V13 row uses its kinematic age $\\log\\tau_k=5.9$--$6.1$; P20 gives $550\\pm250$ kyr for the same source.","tab:dec")
rows=[]
for n,tc,tk,r,x in R['mag']:
    rows.append([n,f2(tc,2),f2(tk,2),f2(r,2),("%.2f"%x) if x else "$\\tau_k>\\tau_c$"])
T['MAG']=tab("lcccc",rows,"Magnetar (V13 values) & $\\tau_c$ (kyr) & $\\tau_k$ (kyr) & $\\tau_c/\\tau_k$ & $x$ (decay only)",
 "Characteristic vs kinematic ages for the magnetars of V13 with an SNR/proper-motion age ($\\tau_k$ is the midpoint of the quoted log range). The ratio scatters over two orders of magnitude and in both directions.","tab:mag")
# conf
rows=[[n,f2(L,2),f"+{u:.2f}/$-${d:.2f}",f"+{u1:.2f}/$-${d1:.2f}"] for n,L,u,d,u1,d1 in R['conf']]
T['CONF']=tab("llcc",rows,"Source & $L_{\\rm obs}$ ($10^{32}$) & M24 90\\% errors & Gaussian $1\\sigma$ equivalent",
 "M24 luminosity errors (90\\% confidence) and the equivalent Gaussian $1\\sigma$ values (divide by $1.645$). The other references quote $1\\sigma$ (P20, Ho+26), a statistical-plus-distance range (V13), or $3\\sigma$ for upper limits (P20).","tab:conf")
# polar cap
rows=[[n,f"{P:g}",sci(Ed,1),sci(L,1),f"{L/Ed:.1e}".replace("e-0","\\times10^{-").replace("e-","\\times10^{-")+"}" if False else sci(L/Ed,1),f2(rpc,2),f"{rb:g}",f"{rem:g}"] for n,P,Ed,L,rpc,rb,rem in R['pc']]
T['PC']=tab("lccccccc",rows,"Pulsar & $P$ (s) & $\\dot E$ (erg/s) & $L_{\\rm BB}$ (erg/s) & $L/\\dot E$ & $R_{\\rm pc}$ (km) & $R_{\\rm bb}$ (km) & $R_{\\rm em}$ NSMAXG-H (km)",
 "Hot-spot size vs the dipolar polar cap, $R_{\\rm pc}=R\\sqrt{2\\pi R/(cP)}$ with $R=12$ km. $R_{\\rm bb}$ and $N_{\\rm nsmaxg}=(R_{\\rm em}/R)^2$ are from M24 (Ext.\\ Data Tables 2, 4); $\\dot E$ from M24 Table~1.","tab:pc")


vrows=[
("Kargaltsev+02","ACIS-S","BB","$3.45\\pm0.15$","$404\\pm5$","$0.28\\pm0.01$","--"),
("Becker+06","MOS+pn 2001+03","BB","$3.22$","$391\\pm4$","$0.285$","--"),
("Becker+06","MOS+pn 2001+03","BB+BB","$3.82$","343 / 569","$0.36$ / $0.06$","--"),
("P20 (Shternin, priv.\\ comm.)","MOS+pn 2003--10","nsx carbon","$6.8\\pm0.1$","$133\\pm2$","$5.0\\pm0.4$","$2\\times10^{33}$ ($d=0.77$)"),
("Wu+21","pn 2010","BB+BB","$5.5$","317 / 482","$0.39$ / $0.12$","--"),
("Wu+21","pn 2010","H atm.+H atm.","$7.96$","256 / 71","$0.95$ / whole star","--"),
("Wu+21","pn 2010","carbon atm.","$7.0\\pm0.2$","$145\\pm3$","$4.3$","--"),
("Alford \\& Halpern 23","pn 2005, 2010","carbon atm.","$4.7$--$4.9$","$132$","$5.2$","--"),
("M24","ACIS-S (CC mode)","BB (+ hidden BB $<50$ eV, 11 km)","$4.7\\pm0.4$","$397\\pm9$","$0.24\\pm0.08$","$2.0\\times10^{32}$"),
("M24","ACIS-S","NSMAXG-H, $10^{12}$ G","--","$310\\pm10$","$0.50$","$F=27.0\\times10^{-13}$"),
("Ho+26","all XMM + Chandra","nsx+nsx (H): hot spot + whole star","--","$\\approx300$ / $57$--$76$ (cool)","hot spot $R^\\infty\\sim0.3$ km at 1 kpc","$5\\times10^{32}$ total; cool $1.3$--$4.0\\times10^{32}$"),
]
rows=[list(r) for r in vrows]
T['VELA']=tab("P{2.6cm}P{2.4cm}P{3.0cm}ccP{2.4cm}P{2.6cm}".replace("P{2.6cm}P{2.4cm}P{3.0cm}ccP{2.4cm}P{2.6cm}","P{2.2cm}P{2.3cm}P{2.8cm}P{1.3cm}P{2.0cm}P{2.4cm}P{2.8cm}"),rows,
 "Reference & Data & Model & $N_{\\rm H}$ ($10^{21}$) & $kT$ (eV) & $R/d$ (km/kpc) & $L$ (erg\\,s$^{-1}$)",
 "Published spectral analyses of Vela Jr, transcribed from Ho+26 Table~2 (errors $1\\sigma$ except P20 and M24 at 90\\%). The same data give $kT$ between 57 and 404 eV and $R/d$ between 0.24 and 5.2 km/kpc depending on the model; the luminosity follows the model class (hot-spot BB $\\sim2\\times10^{32}$, whole-surface carbon atmosphere $\\sim2\\times10^{33}$ at 0.77 kpc, hot spot plus cool surface $\\sim5\\times10^{32}$). Ho+26 tabulate M24's BB radius under $R/d$; whether M24's $R_{\\rm bb}=0.24$ km is already per kpc is not stated.","tab:vela",size="\\scriptsize")

tex=open(ROOT/'notes'/'template.tex').read()
for k,v in T.items(): tex=tex.replace('@@'+k+'@@',v)
open(ROOT/'notes'/'ns_thermal_data_notes.tex','w').write(tex)
print('wrote notes tex; unfilled placeholders:', [k for k in T if '@@'+k+'@@' in tex])
