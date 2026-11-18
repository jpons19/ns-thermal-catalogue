"""Stars with tau_c > 1e5 yr at standard and field-decay-corrected age for several decay times (--taud ...)."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # project root
import re, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from openpyxl import load_workbook
import sys; sys.path.insert(0,str(ROOT/'data')); import ns_cooling_data as ns
import argparse
def fmt_td(td):
    e=int(np.floor(np.log10(td))); mt=td/10**e
    return f"10^{{{e}}}" if abs(mt-1)<1e-9 else f"{mt:g}\\times10^{{{e}}}"
ap=argparse.ArgumentParser(description="Old-star luminosity/temperature vs age with field-decay-corrected ages")
ap.add_argument("--taud",type=float,nargs="+",default=[1e5,3e5,1e6],help="field decay times in yr")
ap.add_argument("--xlsx",default=str(ROOT/'data'/'NS_thermal_crossmatch.xlsx'))
ap.add_argument("--out",default=str(ROOT/'figures'))
ap_args=ap.parse_args()
TAUDS=ap_args.taud
corr=lambda tc,td:(td/2)*np.log(1+2*tc/td)
wb=load_workbook(ap_args.xlsx,data_only=True); m=wb['Master']
nz=lambda x: None if x in (None,"") else float(x)
def parseT(s):
    s=str(s).strip()
    if s.startswith("<"): return float(s[1:]),None,None,True
    if "/" in s: return float(s.split("/")[0]),None,None,False
    mm=re.match(r"^([\d.]+)-([\d.]+)$",s)
    if mm: a,b=float(mm[1]),float(mm[2]); return (a+b)/2,a,b,False
    return float(s),None,None,False
S=[]
for r in range(5,m.max_row+1):
    g=lambda c:nz(m.cell(r,c).value)
    cls=m.cell(r,4).value; name=m.cell(r,2).value
    tc=g(66) or g(24)
    tc=tc*1e3 if tc else (10**g(11) if g(11) else None)
    if not tc or tc<1e5 or cls in ("UL","CCO/TINS"): continue
    # luminosity
    L=Llo=Lhi=None;Lul=False
    if g(70) is not None and g(72) is not None:
        Llo,Lhi=g(70)*1e32,g(72)*1e32; L=(g(71) or np.sqrt(g(70)*g(72)))*1e32
    elif g(27) is not None and g(28) is not None:
        L,Llo,Lhi=g(27)*1e32,g(28)*1e32,g(29)*1e32
    elif g(41) is not None:
        Llo,Lhi=g(41)*1e32,g(42)*1e32; L=np.sqrt(Llo*Lhi)
    if L is None: continue
    if cls=="Hot-spot PSR": Lul=True
    # temperature
    T=Tlo=Thi=None
    if g(75) is not None and g(73) is not None: Tlo,Thi=g(73),g(75); T=g(74) or np.sqrt(Tlo*Thi)
    elif m.cell(r,30).value not in (None,""): T,Tlo,Thi,_=parseT(m.cell(r,30).value)
    elif g(17) is not None: T=g(17)
    S.append(dict(name=name,cls=cls,tc=tc,tcor={td:corr(tc,td) for td in TAUDS},L=L,Llo=Llo,Lhi=Lhi,Lul=Lul,T=T,Tlo=Tlo,Thi=Thi))
print(len(S),"sources")
CA="#e07b00"; CASE_COL=["#0a8f7a","#2a5db0","#8e3b9e","#b5473a"]
def draw(q):
    fig,ax=plt.subplots(figsize=(11,6.8))
    for ref in ("V13","P20","WEB"):
        d=ns.get(ref,q,include_magnetars=True)
        ax.errorbar(d["x"],d["y"],fmt=".",ms=5,color="#b0b0b0",alpha=.7,zorder=1)
    key="L" if q=="L" else "T"
    items=[s for s in S if s[key] is not None]
    ys=np.array([s[key] for s in items]); pad=1.25
    cases=[("standard",CA,[s["tc"] for s in items],"standard $\\tau_c$")]
    for td,col in zip(TAUDS,CASE_COL):
        cases.append((td,col,[s["tcor"][td] for s in items],f"corrected, $\\tau_d={td:.0e}$ yr".replace("e+0","\\times10^{").replace("e+","\\times10^{")+"}" if False else f"corrected, $\\tau_d={fmt_td(td)}$ yr"))
    for name,col,xs,lab in cases:
        xs=np.array(xs)
        ax.add_patch(Rectangle((xs.min()/1.15,ys.min()/pad),xs.max()*1.15-xs.min()/1.15,ys.max()*pad-ys.min()/pad,facecolor=col,alpha=.09,edgecolor=col,lw=1.4,zorder=0))
        print(q,name,"age range %.2e - %.2e, median %.2e"%(xs.min(),xs.max(),np.median(xs)))
    for s in items:
        y=s[key]; lo,hi=(s["Llo"],s["Lhi"]) if q=="L" else (s["Tlo"],s["Thi"]); mag=s["cls"]=="MAG"
        for name,col,xs,lab in cases:
            x=s["tc"] if name=="standard" else s["tcor"][name]
            full=(name=="standard")
            yerr=None
            if full and lo is not None and hi is not None and not (q=="L" and s["Lul"]): yerr=[[max(y-lo,0)],[max(hi-y,0)]]
            if q=="L" and s["Lul"] and full:
                ax.errorbar(x,y,yerr=[[y*0.5],[0]],uplims=True,fmt="none",ecolor=col,elinewidth=1,capsize=2,zorder=3)
            ax.errorbar(x,y,yerr=yerr,fmt="D" if mag else ("o" if full else "s"),ms=6.5 if full else 4.8,mfc="white" if mag else col,mec=col,color=col,ecolor=col,elinewidth=1,capsize=2,alpha=.9 if full else .75,zorder=4 if full else 3)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5e3,1e8)
    if q=="L": ax.set_ylim(1e28,1e36); ax.set_ylabel("Thermal luminosity (erg/s)")
    else: ax.set_ylim(8,1000); ax.set_ylabel("Temperature at infinity (eV; model dependent)")
    ax.set_title(("Luminosity" if q=="L" else "Temperature")+" vs age, stars with $\\tau_c>10^5$ yr: standard vs field-decay-corrected ages")
    ax.set_xlabel("Age (yr)")
    h=[Line2D([],[],marker="o",color=CA,ls="",label="standard $\\tau_c=P/2\\dot P$ (with errors)")]
    for td,col in zip(TAUDS,CASE_COL): h.append(Line2D([],[],marker="s",color=col,ls="",label=f"corrected, $\\tau_d={fmt_td(td)}$ yr"))
    h+= [Line2D([],[],marker="D",mfc="white",color="#555",ls="",label="magnetars (V13)"),Line2D([],[],marker=".",color="#b0b0b0",ls="",label="data with independent ages (context)")]
    ax.legend(handles=h,loc="upper left",fontsize=8.5,framealpha=.95,ncol=2)
    ax.grid(True,which="major",alpha=.3); ax.grid(True,which="minor",alpha=.1)
    import textwrap
    note=("Sources: web catalogue (else P20 paper, else V13); tau_c from web/P20 tables (V13 for magnetars). Corrected age t=(tau_d/2)ln(1+2 tau_c/tau_d) for B~exp(-t/tau_d), P0<<P. "
          "Hot-spot pulsar luminosities are upper limits; CCOs excluded. Shaded boxes span the source range of each case (same colour as markers).")
    fig.text(0.01,0.005,"\n".join(textwrap.wrap(note,170)),fontsize=7.3,color="#444")
    fig.tight_layout(rect=(0,0.045,1,1))
    fn=f"{ap_args.out}/{'luminosity' if q=='L' else 'temperature'}_vs_age_old_stars_taud.png"
    fig.savefig(fn,dpi=170); plt.close(fig); print(fn)
draw("L"); draw("T")
