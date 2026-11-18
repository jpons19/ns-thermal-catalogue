"""Overplot, on the NS cooling data plot, the stars whose characteristic age exceeds 1e5 yr at
(a) their standard tau_c and (b) the field-decay-corrected age t=(tau_d/2) ln(1+2 tau_c/tau_d).
Usage: python3 plot_taud_group.py [--taud 3e5] [--tcmin 1e5]   (needs ns_cooling_data.py and the xlsx in the same folder)"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # project root

import argparse, sys, os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from openpyxl import load_workbook
here=str(ROOT/"data"); sys.path.insert(0,here)
import ns_cooling_data as ns
ap=argparse.ArgumentParser(); ap.add_argument("--taud",type=float,default=3e5); ap.add_argument("--tcmin",type=float,default=1e5)
ap.add_argument("--xlsx",default=os.path.join(here,"NS_thermal_crossmatch.xlsx")); a=ap.parse_args()
corr=lambda tc:(a.taud/2)*np.log(1+2*tc/a.taud)
m=load_workbook(a.xlsx,data_only=True)["Master"]
tc={}
for r in range(5,m.max_row+1):
    nm=m.cell(r,2).value; v=m.cell(r,66).value or m.cell(r,24).value          # web, else P20 (kyr)
    if v not in (None,""): tc[nm]=float(v)*1e3
    elif m.cell(r,11).value not in (None,""): tc[nm]=10**float(m.cell(r,11).value)   # V13 log tau_c
group,seen=[],set()
for ref in ("WEB","P20","V13"):
    for e in ns.DATA[ref]:
        n=e["name"].replace(" (cool surface)","")
        if n in seen or n not in tc or tc[n]<a.tcmin or e["cls"] in ("CCO/TINS","UL"): continue
        seen.add(n); group.append(dict(e,name=n,tc=tc[n],tcor=corr(tc[n])))
CA,CB="#e07b00","#0a8f7a"
for q in ("L","T"):
    fig,ax=plt.subplots(figsize=(10.5,6.6)); ax.set_xscale("log"); ax.set_yscale("log")
    ns.plot_observations(ax,q,xunit="yr",include_magnetars=True,legend=False,zorder=3)
    G=[g for g in group if g[q] is not None]; ys=np.array([g[q] for g in G]); pad=1.25
    for key,col in (("tc",CA),("tcor",CB)):
        xs=np.array([g[key] for g in G])
        ax.add_patch(Rectangle((xs.min()/1.15,ys.min()/pad),xs.max()*1.15-xs.min()/1.15,ys.max()*pad-ys.min()/pad,facecolor=col,alpha=.12,edgecolor=col,lw=1.6,zorder=0))
    for g in G:
        y=g[q]; lo,hi=g[q+"_lo"],g[q+"_hi"]; yerr=None if lo is None or hi is None else [[max(y-lo,0)],[max(hi-y,0)]]
        ax.annotate("",xy=(g["tcor"],y),xytext=(g["tc"],y),arrowprops=dict(arrowstyle="->",color="#777",lw=.8),zorder=4)
        ax.errorbar(g["tc"],y,yerr=yerr,fmt="o",ms=8,color=CA,mec="black",mew=.5,ecolor=CA,capsize=2,zorder=6)
        ax.errorbar(g["tcor"],y,yerr=yerr,fmt="s",ms=8,color=CB,mec="black",mew=.5,ecolor=CB,capsize=2,zorder=6)
        ax.annotate(g["name"].replace("PSR ","").replace("RX ","RX "),(g["tcor"],y),xytext=(-4,7),textcoords="offset points",fontsize=7.5,color=CB,ha="right")
    ax.set_xlim(1e2,1e8)
    ax.set_ylim(*( (1e28,3e36) if q=="L" else (5,1000)))
    ax.set_xlabel("Age (yr)"); ax.set_ylabel("Thermal luminosity (erg/s)" if q=="L" else "Temperature at infinity (eV; model dependent)")
    ax.set_title(f"{'Luminosity' if q=='L' else 'Temperature'} vs age: stars with $\\tau_c>10^5$ yr at standard and corrected age ($\\tau_d=3\\times10^5$ yr)")
    h=[Line2D([],[],marker=m_,color=c_,mec="black",ls="",ms=7,alpha=al,label=l_) for m_,c_,al,l_ in
       (("o","#1f77b4",.9,"Viganò+13 (independent ages)"),("s","#2ca02c",.5,"Potekhin+20 paper"),("^","#7b2d8e",.9,"Potekhin web"),("*","#d62728",1,"Marino+24"),("D","#e08a00",1,"Ho+26"))]
    h+=[Line2D([],[],marker="o",color=CA,mec="black",ls="",ms=8,label=f"standard $\\tau_c$ ({len(G)} stars, orange box)"),
        Line2D([],[],marker="s",color=CB,mec="black",ls="",ms=8,label=f"corrected, $\\tau_d=3\\times10^5$ yr (teal box)")]
    ax.legend(handles=h,loc="upper right",fontsize=8,framealpha=.95)
    ax.grid(True,which="major",alpha=.3); ax.grid(True,which="minor",alpha=.1)
    fig.text(0.01,0.005,"Orange/teal markers use the same L (or T) as the star's independent-age point; the colored reference markers are the independent ages. tau_c from web/P20 (V13 for B0656+14, 1E 2259+586).",fontsize=7.3,color="#444")
    fig.tight_layout(rect=(0,0.02,1,1))
    fn=os.path.join(str(ROOT/"figures"),f"{'luminosity' if q=='L' else 'temperature'}_vs_age_taud3e5.png"); fig.savefig(fn,dpi=170); plt.close(fig); print(fn)
for g in group: print(f"{g['name']:26s} tau_c={g['tc']:.2e}  corrected={g['tcor']:.2e}  independent age={g['age']:.2e}")
