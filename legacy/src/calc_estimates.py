"""Order-of-magnitude estimates quoted in the notes: redshift factors, blackbody L, detectable flux fraction, distance-driven L ranges,
birth periods, field-decay age bias, confidence conversions, polar-cap sizes. Writes data/derived/calc.json."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # project root
import numpy as np, json
from scipy.optimize import brentq
from scipy.integrate import quad
from openpyxl import load_workbook
R={}
# ---------- constants
G=6.674e-8; c=2.998e10; Msun=1.989e33; sig=5.670374e-5; kB_eV=8.617333e-5  # eV/K
# (a) redshift factors
red=[]
for M,Rk in [(1.4,10),(1.4,12),(1.4,13),(1.6,12),(1.8,12),(1.4,11.6)]:
    rg=2*G*M*Msun/c**2/1e5
    red.append((M,Rk,rg,1/np.sqrt(1-rg/Rk),Rk/np.sqrt(1-rg/Rk),(1-rg/Rk)))
R['red']=red
# (b) BB-equivalent whole surface L vs kT_inf, R_inf=14.8
Rinf=14.8e5
bb=[]
for kT in (20,30,40,50,60,75,100,112,150,200,400):
    T=kT/kB_eV
    bb.append((kT,T,4*np.pi*Rinf**2*sig*T**4))
R['bb']=bb
# (c) observed fraction of BB bolometric flux in 0.5-8 keV after absorption (approx cross-section)
def sigma(E): return 2.4e-22*E**(-8/3)  # cm2 per H, E in keV (approximate, no edges)
def frac(kT,NH,Emin=0.5,Emax=8.0):
    kT=kT/1000.
    f=lambda E: E**3/np.expm1(E/kT)*np.exp(-NH*sigma(E))
    num=quad(f,Emin,Emax,limit=200)[0]
    den=quad(lambda E:E**3/np.expm1(E/kT),1e-5,60*kT,limit=200)[0]
    return num/den
fr=[]
for kT in (30,50,75,112,200,400):
    fr.append((kT,[frac(kT,nh*1e21) for nh in (2,4.7,7)]))
R['frac']=fr
# transmission
tr=[(E,[np.exp(-nh*1e21*sigma(E)) for nh in (2,4.7,7)]) for E in (0.2,0.3,0.5,1.0,2.0)]
R['trans']=tr
# (d) age -> L sensitivity
sl=[]
for dt in (0.1,0.3,0.5,1.0):   # fractional
    up=np.log10(1+dt); dn=-np.log10(1-dt) if dt<1 else np.nan
    sl.append((dt,0.37*np.log10(1+dt),0.55*np.log10(1+dt)))
R['agesens']=sl
# (e) distance-driven L ranges from Master
wb=load_workbook(str(ROOT/'data'/'NS_thermal_crossmatch.xlsx'),data_only=True); m=wb['Master']
dl=[]
for r in range(5,m.max_row+1):
    nm=m.cell(r,2).value; dlo,dhi,dp=m.cell(r,22).value,m.cell(r,23).value,m.cell(r,21).value
    if isinstance(dlo,(int,float)) and isinstance(dhi,(int,float)) and dhi>dlo:
        dl.append((nm,dlo,dhi,2*np.log10(dhi/dlo),m.cell(r,4).value))
dl.sort(key=lambda x:-x[3]); R['dist']=dl[:14]
# competing-distance cases
comp=[("PSR B2334+61","0.7 (web HI 2020) / 1.1 (web 2026) / 2.08 (YMW17) / 3.1 (NE2001)",0.7,3.3),("CXOU J0852","0.5-1.0 (Allen+15) vs 1.27-1.55 (Suherli+26)",0.5,1.55),("PSR J0205","2.0$\\pm$0.3 (Kothes) vs 3.2 (Roberts+93)",1.7,3.2)]
R['comp']=[(a,b,lo,hi,2*np.log10(hi/lo)) for a,b,lo,hi in comp]
# (f) birth periods n=3 and braking index needed
pul=[("PSR J0205+6449",0.0657,5.37,0.819,0.819),("PSR B2334+61",0.495,40.6,7.7,7.7),("PSR J0538+2817",0.143,620,20,60),
("PSR B1951+32",0.0395,107,46,82),("PSR B1727--47",0.830,80.5,40,60),("PSR J0007+7303",0.316,13.9,9.2,9.2),
("Vela (B0833--45)",0.0893,11.3,17,23),("PSR J1119--6127",0.408,1.61,4.2,7.1)]
bp=[]
for nm,P,tc,tl,th in pul:
    row=[nm,P,tc,tl,th]
    if th<tc:
        p0=[P*np.sqrt(1-t/tc) for t in (tl,th)]
        row+= [p0[1],p0[0]]; row+=[None,None]
    else:
        row+=[None,None]; row+=[1+2*tc/th,1+2*tc/tl]   # n needed (P0<<P)
    bp.append(row)
R['birth']=bp
# (g) field decay inversion
def x_from_R(Rr):
    if Rr<=1: return np.nan
    return brentq(lambda x:(np.exp(2*x)-1)/(2*x)-Rr,1e-6,30)
dec=[]
for nm,tc,ts in [("RX J0720.4--3125",1900,850),("RX J1308.6+2127 (P20)",1460,550),("RX J1308.6+2127 (V13)",1460,1030),("RX J1856.5--3754",3760,420)]:
    Rr=tc/ts; x=x_from_R(Rr); dec.append((nm,tc,ts,Rr,x,ts/x))
R['decay']=dec
# magnetar tau_c vs tau_k (V13 log values)
mg=[("1E 2259+586",5.4,4.0,4.3),("1E 1841$-$045",3.7,2.7,3.0),("SGR 0501+4516",4.2,4.0,4.0),("SGR 0526$-$66",3.5,3.7,3.7),("SGR 1627$-$41",3.3,3.7,3.7),
("CXOU J1714$-$381",3.0,3.7,3.7),("SGR 1900+14",3.0,3.6,3.9),("SGR 1806$-$20",2.6,2.8,3.0)]
mgt=[]
for nm,ltc,a,b in mg:
    tk=10**((a+b)/2); tc=10**ltc; Rr=tc/tk
    mgt.append((nm,tc/1e3,tk/1e3,Rr,x_from_R(Rr) if Rr>1 else None))
R['mag']=mgt
# generic table (e^{2x}-1)/(2x)
R['gen']=[(x,(np.exp(2*x)-1)/(2*x)) for x in (0.1,0.25,0.5,1,1.5,2,3)]
# (h) 90% -> 1 sigma
k=1/1.645
m24=[("PSR J0205+6449",1.44,0.6,0.5),("PSR B2334+61",0.78,0.30,0.10),("CXOU J0852",2.0,0.6,0.6)]
R['conf']=[(n,L,up,dn,up*k,dn*k) for n,L,up,dn in m24]
# (n) polar cap size and Edot ratios
Rns=12e5
def Rpc(P): return Rns*np.sqrt(2*np.pi*Rns/(c*P))/1e5
R['pc']=[("PSR J0205+6449",0.0657,2.666e37,1.44e32,Rpc(0.0657),0.6,0.66),("PSR B2334+61",0.495,6.1e34,0.78e32,Rpc(0.495),0.9,3.2)]
json.dump(R,open(ROOT/'data'/'derived'/'calc.json','w'),default=float,indent=1)
print('wrote', ROOT/'data'/'derived'/'calc.json')
