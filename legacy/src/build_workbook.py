"""Build data/NS_thermal_crossmatch.xlsx: Settings, Master (V13 + P20 paper + M24 + web, with formula cross-checks and flags).
All literature values are transcribed in this file (blue cells in the workbook); the web table comes from data/web_table.json.
After building, run recalc_xlsx.py so cached values exist. Part 2 (workbook_part2.py) adds Marino3_detail, VelaJr, Findings, Web_updates, README sheets."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent   # project root
from openpyxl import Workbook
from catalogue import M24_OBS, MARINO, REFERENCES, catalogue, export_csv
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.formatting.rule import FormulaRule

# ---------------- Potekhin+20 (Tables 1 & 2) ----------------
# pid, short, assoc, class, P, Bdip(1e12), d, dlo, dhi, tc(kyr), t*lo, t*hi, L(1e32), Llo, Lhi, kT text
N=None
P20=[
(1,"1E 0102.2-7219","SNR 0102-72.3 (SMC)","CCO/TINS",N,N,62,60,64,N,1.5,2.7,110,60,270,"210"),
(2,"RX J0822.0-4300","Puppis A","CCO/TINS",0.113,0.029,2.2,1.9,2.5,2.54e5,3.7,5.2,50,39,61,"276/455"),
(3,"CXOU J085201.4-461753","Vela Jr.","CCO/TINS",N,N,0.77,0.57,0.97,N,2.1,5.4,20,10,30,"90"),
(4,"2XMM J104608.7-594306","Homunculus","CCO/TINS",N,N,2.35,1.35,3.35,N,11,30,2.19,0.8,6,"40-70"),
(5,"1E 1207.4-5209","G296.5+10.0","CCO/TINS",0.424,0.098,2.1,1.3,3.9,3.01e5,2,21,13.1,11.5,18.0,"90-250"),
(6,"1RXS J141256.0+792204","Calvera","CCO/TINS",0.0592,0.45,2,1,4,285,N,N,10,2,50,"65-210"),
(7,"CXOU J160103.1-513353","G330.2+1.0","CCO/TINS",N,N,4.9,4.6,9.9,N,0.6,1.0,58,56,60,"118"),
(8,"1WGA J1713.4-3949","G347.3-0.5","CCO/TINS",N,N,1.3,0.9,1.7,N,1.608,1.608,49,20,120,"138"),
(9,"XMMU J172054.5-372652","G350.1-0.3","CCO/TINS",N,N,6.1,5.1,7.4,N,0.6,1.2,201,150,270,"161"),
(10,"XMMU J173203.3-344518","HESS J1731-347","CCO/TINS",N,N,3.2,2.4,4.0,N,2,6,174,135,193,"153"),
(11,"CXOU J181852.0-150213","G015.9+00.2","CCO/TINS",N,N,10.0,8.5,16.7,N,2.7,6.0,84,42,152,"130"),
(12,"CXOU J185238.6+004020","Kes 79","CCO/TINS",0.105,0.031,7.1,6.5,7.5,1.92e5,3.2,7.8,104,84,128,"133"),
(13,"CXOU J232327.8+584842","Cas A","CCO/TINS",N,N,3.4,3.3,3.7,N,0.320,0.338,77.5,61,94,"123-185"),
(14,"PSR J0205+6449","3C 58","RPP",0.0657,3.6,2.0,1.7,2.3,5.37,0.819,0.819,1.9,0.8,3.4,"49"),
(15,"PSR J0357+3205","Morla","RPP",0.444,2.4,0.45,0.40,0.50,541,200,1300,0.15,0.04,0.40,"36"),
(16,"PSR J0538+2817","Sim 147","RPP",0.143,0.73,1.47,1.20,1.89,620,20,60,10.9,6.3,13.6,"91"),
(17,"CXOU J061705.3+222127","IC 443 (P~0.1-0.6 s est.; not used)","RPP",N,N,1.7,1.4,2.0,N,30,30,2.6,2.5,2.7,"58.4"),
(18,"PSR J0633+0632","Collinder 106 (?)","RPP",0.297,4.9,0.9,0.8,2.0,59.2,N,N,1.5,0.6,4.0,"53"),
(19,"PSR J0633+1746","Geminga","RPP",0.237,1.6,0.25,0.17,0.48,342,N,N,0.88,0.49,1.09,"42"),
(20,"PSR B0656+14","Monogem","RPP",0.385,4.7,0.28,0.25,0.31,111,N,N,6.7,5.2,8.8,"64/123"),
(21,"PSR B0833-45","Vela","RPP",0.0893,3.4,0.28,0.26,0.30,11.3,17,23,4.24,4.12,4.36,"57"),
(22,"PSR B1055-52","","RPP",0.197,1.1,0.35,0.20,0.50,535,N,N,1.0,0.3,2.0,"68"),
(23,"PSR J1357-6429","HESS J1356-645","RPP",0.166,7.8,2.5,2.5,2.5,7.31,N,N,3.6,2.9,4.3,"64"),
(24,"PSR B1706-44","G343.1-02.3","RPP",0.102,3.1,2.6,2.0,3.1,17.5,N,N,7.1,0.6,8.7,"71"),
(25,"PSR J1740+1000","","RPP",0.154,1.8,1.3,1.2,1.4,114,N,N,1.9,0.9,5.0,"67"),
(26,"PSR J1741-2054","","RPP",0.414,2.7,0.8,0.5,1.1,386,N,N,3.1,2.1,4.5,"60"),
(27,"PSR B1822-09","","RPP",0.769,6.4,1.4,0.9,1.9,233,N,N,0.26,0.17,0.38,"83"),
(28,"PSR B1823-13","","RPP",0.101,2.8,4,3,5,21.4,N,N,4.5,3.6,5.4,"97"),
(29,"PSR J1836+5925","Next Geminga","RPP",0.173,0.52,0.45,0.2,0.7,1830,N,N,0.014,0.008,0.030,"15.9"),
(30,"PSR B1951+32","CTB 80","RPP",0.0395,0.49,2.4,2.2,2.6,107,46,82,1.8,0.7,4.8,"130"),
(31,"PSR J1957+5033","","RPP",0.375,1.6,0.45,0.1,0.8,870,N,N,0.036,0.012,0.11,"13-25"),
(32,"PSR J2021+3651","","RPP",0.104,3.2,1.8,0.4,3.5,17.2,N,N,5,3,8,"63"),
(33,"PSR B2334+61","G114.3+00.3","RPP",0.495,9.9,0.7,0.7,0.7,40.6,7.7,7.7,0.47,0.12,0.82,"38"),
(34,"PSR J0726-2612","","HB-PSR",3.442,32,1.0,0.3,2.4,186,N,N,4.0,3.0,8.4,"74"),
(35,"PSR J1119-6127","G292.2-00.5","HB-PSR",0.408,41,8.4,8.0,8.8,1.61,4.2,7.1,19,11,38,"80-210"),
(36,"PSR B1509-58","","HB-PSR",0.151,15,5.2,3.8,6.6,1.56,N,N,90,70,110,"142"),
(37,"PSR J1718-3718","","HB-PSR",3.379,75,7.0,4.5,10,33.2,N,N,4,2,9,"57-200"),
(38,"PSR J1819-1458","RRAT","HB-PSR",4.263,50,3.6,2.7,4.5,120,N,N,30,8,80,"138"),
(39,"RX J0420.0-5022","","XINS",3.453,9.9,0.335,0.325,0.345,1980,N,N,0.06,0.04,0.08,"45"),
(40,"RX J0720.4-3125","","XINS",16.782,24,0.286,0.263,0.313,1900,700,1000,1.9,1.1,3.2,"90-100"),
(41,"RX J0806.4-4123","","XINS",11.370,26,0.2425,0.235,0.250,3240,N,N,0.205,0.16,0.25,"90-110"),
(42,"RX J1308.6+2127","RBS1223","XINS",10.312,34,0.38,0.35,0.40,1460,300,800,3.3,2.6,3.8,"50-90"),
(43,"RX J1605.3+3249","RBS1556","XINS",N,N,0.25,0.09,0.4,N,380,510,1.9,0.07,5,"35-120"),
(44,"RX J1856.5-3754","Upper Scorpius","XINS",7.055,15,0.123,0.108,0.134,3760,340,500,0.65,0.5,0.8,"36-63"),
(45,"RX J2143.0+0654","RBS1774","XINS",9.428,200,0.41,0.39,0.43,3700,N,N,1.1,0.5,1.7,"40/100"),
(46,"PSR J0007+7303","CTA 1","UL",0.316,1.1,1.4,1.1,1.7,13.9,9.2,9.2,0.3,N,N,"<200"),
(47,"PSR B0531+21","Crab","UL",0.0334,3.8,2.0,1.4,2.7,1.26,0.954,0.954,300,N,N,"<180"),
(48,"PSR B1727-47","RCW 114","UL",0.830,12,0.65,0.5,0.8,80.5,40,60,0.35,N,N,"<33"),
(49,"PSR J2043+2740","Cygnus Loop (?)","UL",0.0961,0.35,1.65,1.5,1.8,1200,N,N,0.4,N,N,"<80"),
(50,"PSR B2224+65","Guitar","UL",0.683,2.6,0.83,0.73,1.0,1130,N,N,1.7,N,N,"<110"),
(51,"PSR B0114+58","","Hot-spot PSR",0.101,0.78,1.8,1.2,2.4,275,N,N,0.044,0.041,0.047,"170"),
(52,"PSR B0943+10","","Hot-spot PSR",1.098,2.0,0.76,0.63,0.89,4980,N,N,0.003,0.001,0.005,"82"),
(53,"PSR B1133+16","","Hot-spot PSR",1.188,2.1,0.35,0.33,0.37,4980,N,N,0.0003,0.0001,0.002,"190"),
(54,"PSR J1154-6250","","Hot-spot PSR",0.282,0.40,1.55,1.36,1.77,7990,N,N,0.017,0.012,0.022,"210"),
(55,"PSR B1929+10","","Hot-spot PSR",0.227,0.52,0.31,0.26,0.40,3110,N,N,0.0084,0.0062,0.0118,"300"),
]
# ---------------- Vigano+13 (Tables 1 & 3) ----------------
# P, logPdot, logBp, logtc, logtk lo, hi, d, logL lo, hi, kTbb(eV), model
V13={
12:(0.105,-17.1,10.8,8.3,3.7,3.9,7.1,33.5,33.7,440,"BB/nsa"),
5:(0.424,-16.7,11.3,8.5,3.4,4.3,2.1,33.0,34.0,190,"BBb/nsab"),
2:(0.112,-17.0,10.8,8.3,3.5,3.6,2.2,33.5,33.7,400,"BB/nsa"),
13:(N,N,N,N,2.5,2.5,3.4,33.4,33.6,450,"BB/nsa"),
16:(0.143,-14.4,12.2,5.8,4.6,4.6,1.3,32.7,32.9,160,"BB+PL"),
22:(0.197,-14.2,12.3,5.7,N,N,0.73,32.2,32.6,190,"2BB+PL"),
19:(0.237,-14.0,12.5,5.5,N,N,0.25,31.6,32.5,140,"2BB+PL"),
24:(0.102,-13.0,12.8,4.2,N,N,2.6,31.7,32.1,160,"BB+PL"),
21:(0.089,-12.9,12.8,4.1,3.7,4.2,0.28,32.1,32.3,120,"(BB/nsa)+PL"),
20:(0.385,-13.3,13.0,5.0,4.9,4.9,0.28,32.7,32.8,100,"2BB+PL"),
33:(0.495,-12.7,13.3,4.6,4.0,4.0,3.1,30.7,32.1,160,"BB/nsa"),
25:(0.154,-11.7,13.6,3.1,N,N,1.4,32.1,32.2,170,"2BB/nsa"),
34:(3.440,-12.5,13.8,5.3,N,N,1.0,32.1,32.5,90,"BB"),
35:(0.408,-11.4,13.9,3.2,3.6,3.9,8.4,33.1,33.4,270,"BB"),
38:(4.263,-12.2,14.0,5.1,N,N,3.6,33.6,33.9,130,"BB"),
37:(3.378,-11.8,14.2,4.5,N,N,4.5,32.8,33.5,190,"BB"),
39:(3.450,-13.6,13.3,6.3,N,N,0.34,30.9,31.0,50,"BB"),
44:(7.055,-13.5,13.5,6.6,5.5,5.7,0.12,31.5,31.7,63,"BB"),
45:(9.428,-13.4,13.6,6.6,N,N,0.43,31.8,31.9,107,"BB"),
40:(8.391,-13.2,13.7,6.3,5.8,6.0,0.29,32.2,32.4,84,"BB"),
41:(11.370,-13.3,13.7,6.5,N,N,0.25,31.2,31.4,101,"BBb/nsab"),
42:(10.310,-13.0,13.8,6.2,5.9,6.1,0.50,32.1,32.2,94,"BBb"),
43:(N,N,N,N,5.7,5.7,0.10,30.9,31.0,99,"BB/nsa"),
}
MAG=[
("1E 2259+586","SNR CTB109",6.979,-12.3,14.1,5.4,4.0,4.3,3.2,35.0,35.4,400,"RCS+PL"),
("4U 0142+614","",8.689,-11.7,14.4,4.8,N,N,3.6,35.4,35.8,400,"RCS+PL"),
("CXO J164710.2-455216","Cluster Wd1",10.611,-12.0,14.3,5.2,N,N,4.0,33.1,33.6,330,"RCS"),
("XTE J1810-197","",5.540,-11.1,14.6,4.1,N,N,3.6,34.0,34.4,260,"2BB"),
("1E 1547.0-5408","SNR G327.24-0.13",2.072,-10.3,14.8,2.8,N,N,4.5,34.3,34.7,520,"RCS"),
("1E 1048.1-5937","",6.458,-10.6,14.9,3.7,N,N,2.7,33.8,34.5,640,"RCS"),
("CXOU J010043.1-721134","SMC",8.020,-10.7,14.9,3.8,N,N,60.6,35.2,35.5,350,"RCS"),
("1RXS J170849.0-400910","",11.003,-10.7,15.0,4.0,N,N,3.8,34.8,35.1,450,"RCS+PL"),
("CXOU J171405.7-381031","SNR CTB37B",3.825,-10.2,15.0,3.0,3.7,3.7,13.2,34.9,35.2,540,"RCS"),
("1E 1841-045","SNR Kes73",11.782,-10.4,15.1,3.7,2.7,3.0,9.6,35.2,35.5,480,"RCS+PL"),
("SGR 0501+4516","SNR HB9",5.762,-11.2,14.6,4.2,4.0,4.0,1.5,33.2,34.0,570,"RCS"),
("SGR 1627-41","SNR G337.0-0.1",2.595,-10.7,14.7,3.3,3.7,3.7,11.0,34.4,34.8,450,"RCS+PL"),
("SGR 0526-66","SNR N49 (LMC)",8.054,-10.4,15.0,3.5,3.7,3.7,49.7,35.4,35.8,480,"RCS"),
("SGR 1900+14","Cluster",5.200,-10.0,15.1,3.0,3.6,3.9,12.5,35.0,35.4,390,"RCS+PL"),
("SGR 1806-20","Cluster W31",7.602,-9.6,15.5,2.6,2.8,3.0,13.0,35.1,35.5,690,"RCS+PL"),
("SGR 0418+5729","",9.078,-14.4,13.1,7.6,N,N,2.0,30.7,31.1,320,"BB"),
("Swift J1822.3-1606","",8.438,-13.1,13.7,6.2,N,N,1.6,32.9,33.2,540,"RCS"),
]
# Marino ages and luminosities are read from the verbatim GitHub input.
M24 = {}
for pid, obj in M24_OBS.items():
    meta = MARINO[obj["name"]]
    low, high = obj["age_yr"]
    luminosity = obj["L32"]
    minus, plus = obj["L32_err"]
    M24[pid] = (meta["distance_kpc"], low / 1000, high / 1000,
                luminosity, round(luminosity-minus, 12), round(luminosity+plus, 12),
                meta["kT_eV"][1], meta["model"] + ". " + meta["note"])
import json
WEBROWS=json.load(open(ROOT/"data"/"web_table.json"))
WEB={w["name"]:w for w in WEBROWS}
# ---------------------------------------------------------------
wb=Workbook()
ARIAL="Arial"
f=lambda **k: Font(name=ARIAL,size=k.pop("size",10),**k)
blue=f(color="0000FF"); black=f(); bold=f(bold=True); white_b=f(bold=True,color="FFFFFF")
hdr_fill=PatternFill("solid",fgColor="1F3864")
grp={ "id":"595959","V":"2E75B6","P":"548235","M":"BF8F00","C":"7030A0","W":"7F3F98","C2":"7F7F7F"}
thin=Side(style="thin",color="BFBFBF")

# ---- Settings
ws=wb.active; ws.title="Settings"
rows=[("Parameter","Value","Meaning"),
("Pdot tolerance (dex)",0.15,"Flag if |log10 ratio| of Pdot between sources exceeds this (V13 gives log Pdot to 0.1 dex only)"),
("Bp tolerance (dex)",0.15,"Flag if V13 log Bp differs from log10(2*Bdip_P20) by more than this"),
("Distance tolerance (dex)",0.10,"Reserved (distance flag now tests V13 value against the P20 distance range)"),
("L midpoint tolerance (dex)",0.5,"Reserved (L flag now tests range overlap; midpoint difference shown in Master for information)"),
("Age tolerance (dex)",0.30,"Flag if independent ages (tau_k vs t*) differ by more than a factor 2"),
("Seconds per year",3.15576e7,"Julian year"),
("B constant for Bdip (G)",3.2e19,"P20: Bdip = 3.2e19 sqrt(P Pdot), equatorial field. V13/M24: Bp = 6.4e19 sqrt(P Pdot), polar field = 2 x Bdip"),
]
for i,r in enumerate(rows,1):
    for j,v in enumerate(r,1):
        c=ws.cell(i,j,v); c.font=white_b if i==1 else (blue if j==2 else black)
        if i==1: c.fill=hdr_fill
ws.column_dimensions["A"].width=30; ws.column_dimensions["B"].width=12; ws.column_dimensions["C"].width=110
ws["B8"].number_format="0.00E+00"; ws["B7"].number_format="0.00000E+00"

# ---- Master
m=wb.create_sheet("Master")
heads=[ # (header, group, width, fmt)
("ID","id",5,"0"),("Source","id",26,"@"),("Association","id",20,"@"),("Class (harmonised)","id",13,"@"),
("In V13","id",6,"0"),("In P20","id",6,"0"),("In M24","id",6,"0"),
("P (s)","V",8,"0.000"),("log Pdot","V",8,"0.0"),("log Bp (G, pole)","V",9,"0.0"),("log tau_c (yr)","V",9,"0.0"),
("log tau_k lo (yr)","V",9,"0.0"),("log tau_k hi (yr)","V",9,"0.0"),("d (kpc)","V",8,"0.00"),
("log L lo (erg/s)","V",9,"0.0"),("log L hi (erg/s)","V",9,"0.0"),("kT_bb (eV)","V",8,"0"),("Best-fit model","V",13,"@"),
("P (s)","P",8,"0.000"),("Bdip (1e12 G, equat.)","P",10,"0.000"),("d (kpc)","P",8,"0.000"),("d lo","P",7,"0.000"),("d hi","P",7,"0.000"),
("tau_c (kyr)","P",10,"0.0"),("t* lo (kyr)","P",8,"0.000"),("t* hi (kyr)","P",8,"0.000"),
("L_inf (1e32 erg/s)","P",10,"0.000"),("L lo","P",8,"0.000"),("L hi","P",8,"0.000"),("kT_inf (eV; cool/hot)","P",12,"@"),
("d (kpc)","M",8,"0.00"),("age lo (kyr)","M",8,"0.000"),("age hi (kyr)","M",8,"0.000"),
("L_obs (1e32 erg/s)","M",10,"0.00"),("L lo","M",8,"0.00"),("L hi","M",8,"0.00"),("kT_bb (eV)","M",8,"0"),("Notes","M",40,"@"),
# computed
("tau_k lo (kyr)","C",9,"0.000"),("tau_k hi (kyr)","C",9,"0.000"),("V13 L lo (1e32)","C",10,"0.000"),("V13 L hi (1e32)","C",10,"0.000"),
("Pdot V13","C",10,"0.00E+00"),("Pdot from P20 (B,P)","C",11,"0.00E+00"),("Pdot from P20 (tau_c,P)","C",11,"0.00E+00"),
("dlog Pdot: P20 internal (B vs tc)","C",12,"0.00"),("dlog Pdot: V13 / P20(B)","C",11,"0.00"),("dlog Bp: V13 - 2xBdip","C",11,"0.00"),
("P ratio V13/P20","C",8,"0.00"),("dlog d: P20/V13","C",9,"0.00"),("L overlap V13 vs P20","C",9,"@"),("dlog L mid: P20 - V13","C",10,"0.00"),
("dlog age mid: t*(P20)/tau_k(V13)","C",12,"0.00"),("M24 L vs V13 range","C",9,"@"),("M24 L vs P20 range","C",9,"@"),
("dlog L: M24/P20","C",9,"0.00"),("dlog d: M24/P20","C",9,"0.00"),("FLAGS","C",70,"@"),
("In web","W",6,"0"),("d lo (kpc)","W",7,"0.00"),("d mid","W",7,"0.00"),("d hi","W",7,"0.00"),("P (s)","W",8,"0.000"),("Pdot","W",10,"0.00E+00"),("Bdip (1e12 G)","W",9,"0.000"),
("tau_c (kyr)","W",10,"0.0"),("t* lo (kyr)","W",8,"0.000"),("t* mid","W",8,"0.000"),("t* hi","W",8,"0.000"),
("L lo (1e32)","W",8,"0.000"),("L mid (1e32)","W",8,"0.000"),("L hi (1e32)","W",8,"0.000"),("kT lo (eV)","W",7,"0.0"),("kT mid","W",7,"0.0"),("kT hi","W",7,"0.0"),("Last update","W",11,"@"),
("dlog Pdot: web, Pdot vs Bdip","C2",11,"0.00"),("dlog Pdot: web, Pdot vs tau_c","C2",11,"0.00"),("dlog Pdot: V13 / web","C2",10,"0.00"),("L used (1e32)","C2",9,"0.000"),
("dlog L: web / P20 paper","C2",10,"0.00"),("dlog d: web / P20 paper","C2",10,"0.00"),("L overlap V13 vs web","C2",9,"@"),("M24 L vs web range","C2",9,"@"),
("dlog L: M24 / web","C2",9,"0.00"),("dlog age: web t* / V13 tau_k","C2",11,"0.00"),("FLAGS (web comparisons)","C2",70,"@"),
]
ncol=len(heads)
col={h[0]+"|"+str(i):i+1 for i,h in enumerate(heads)}
# explicit column letters for formulas
idx={ "ID":1,"Source":2,"Assoc":3,"Class":4,"inV":5,"inP":6,"inM":7,
 "Pv":8,"lPd":9,"lBp":10,"ltc":11,"ltklo":12,"ltkhi":13,"dv":14,"lLlo":15,"lLhi":16,"kTv":17,"modv":18,
 "Pp":19,"Bd":20,"dp":21,"dplo":22,"dphi":23,"tcp":24,"tslo":25,"tshi":26,"Lp":27,"Lplo":28,"Lphi":29,"kTp":30,
 "dm":31,"tmlo":32,"tmhi":33,"Lm":34,"Lmlo":35,"Lmhi":36,"kTm":37,"notem":38,
 "tklo":39,"tkhi":40,"VLlo":41,"VLhi":42,"Pdv":43,"PdpB":44,"Pdptc":45,"dPint":46,"dPvp":47,"dBp":48,"Pr":49,"ddd":50,"Lov":51,"dLmid":52,"dage":53,"MLv":54,"MLp":55,"dLm":56,"ddm":57,"FLAGS":58,"inW":59,"wdlo":60,"wdmid":61,"wdhi":62,"wP":63,"wPd":64,"wB":65,"wtc":66,"wtlo":67,"wtmid":68,"wthi":69,"wLlo":70,"wLmid":71,"wLhi":72,"wklo":73,"wkmid":74,"wkhi":75,"wdate":76,"wPint":77,"wPtc":78,"wPv":79,"wLu":80,"wdL":81,"wdd":82,"wLv":83,"wLM":84,"wdLM":85,"wdage":86,"wFLAGS":87}
assert len(heads)==87
c=lambda k,r: f"{CL(idx[k])}{r}"
# group header row 3, header row 4
groups=[("Identity",1,7,"id"),("Vigano et al. 2013 (MNRAS 434, 123) - Tables 1 & 3",8,18,"V"),("Potekhin et al. 2020 (MNRAS 496, 5052) - Tables 1 & 2",19,30,"P"),
        ("Marino et al. 2024 (arXiv:2404.05371) - main text, Ext. Data Table 2 and Supp. Data Table 6",31,38,"M"),("Computed cross-checks (formulas)",39,58,"C"),("Potekhin web catalogue (updated 03.08.2026; L in 1e33 converted to 1e32)",59,76,"W"),("Computed cross-checks - web",77,87,"C2")]
m["A1"]="Thermally emitting isolated neutron stars - cross-matched catalogue (V13 + P20 + M24)"; m["A1"].font=f(bold=True,size=13)
m["A2"]="Blue = transcribed from papers; black = formula. Blank = not given. Units as in column headers. See README for conventions and caveats."; m["A2"].font=f(italic=True)
for name,a,b,g in groups:
    m.merge_cells(start_row=3,start_column=a,end_row=3,end_column=b)
    cell=m.cell(3,a,name); cell.font=white_b; cell.fill=PatternFill("solid",fgColor=grp[g]); cell.alignment=Alignment(horizontal="center")
for i,h in enumerate(heads,1):
    cell=m.cell(4,i,h[0]); cell.font=white_b; cell.fill=PatternFill("solid",fgColor=grp[h[1]])
    cell.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    m.column_dimensions[CL(i)].width=h[2]
m.row_dimensions[4].height=54

S="Settings!"
def build_row(r,rec):
    pid,short,assoc,cls,v,p,mm=rec[:7]; w=rec[7] if len(rec)>7 else None
    vals={"ID":pid,"Source":short,"Assoc":assoc,"Class":cls,"inV":1 if v else 0,"inP":1 if p else 0,"inM":1 if mm else 0}
    if v:
        for k,x in zip(["Pv","lPd","lBp","ltc","ltklo","ltkhi","dv","lLlo","lLhi","kTv","modv"],v): vals[k]=x
    if p:
        for k,x in zip(["Pp","Bd","dp","dplo","dphi","tcp","tslo","tshi","Lp","Lplo","Lphi","kTp"],p[4:]): vals[k]=x
    if mm:
        for k,x in zip(["dm","tmlo","tmhi","Lm","Lmlo","Lmhi","kTm","notem"],mm): vals[k]=x
    if w:
        vals["inW"]=1
        cv=lambda x,fac: None if x is None else x*fac
        for k,x in [("wdlo",w["dlo"]),("wdmid",w["dmid"]),("wdhi",w["dhi"]),("wP",w["P"]),("wPd",w["Pd"]),("wB",cv(w["B"],1e-12)),("wtc",cv(w["tc"],1e-3)),
                    ("wtlo",cv(w["tlo"],1e-3)),("wtmid",cv(w["tmid"],1e-3)),("wthi",cv(w["thi"],1e-3)),("wLlo",cv(w["Llo"],10)),("wLmid",cv(w["Lmid"],10)),("wLhi",cv(w["Lhi"],10)),
                    ("wklo",w["klo"]),("wkmid",w["kmid"]),("wkhi",w["khi"]),("wdate",w["date"])]:
            if x is not None: vals[k]=x
    else: vals["inW"]=0
    for k,x in vals.items():
        if x is None: continue
        cell=m.cell(r,idx[k],x); cell.font=blue if k not in("ID",) else black
    # formulas
    g=lambda k:c(k,r)
    F={}
    F["tklo"]=f'=IF({g("ltklo")}="","",10^{g("ltklo")}/1000)'
    F["tkhi"]=f'=IF({g("ltkhi")}="","",10^{g("ltkhi")}/1000)'
    F["VLlo"]=f'=IF({g("lLlo")}="","",10^{g("lLlo")}/1E32)'
    F["VLhi"]=f'=IF({g("lLhi")}="","",10^{g("lLhi")}/1E32)'
    F["Pdv"]=f'=IF({g("lPd")}="","",10^{g("lPd")})'
    F["PdpB"]=f'=IF(OR({g("Bd")}="",{g("Pp")}=""),"",({g("Bd")}*1E12/{S}$B$8)^2/{g("Pp")})'
    F["Pdptc"]=f'=IF(OR({g("tcp")}="",{g("Pp")}=""),"",{g("Pp")}/(2*{g("tcp")}*1000*{S}$B$7))'
    F["dPint"]=f'=IF(OR({g("PdpB")}="",{g("Pdptc")}=""),"",LOG10({g("PdpB")}/{g("Pdptc")}))'
    F["dPvp"]=f'=IF(OR({g("Pdv")}="",{g("PdpB")}=""),"",LOG10({g("Pdv")}/{g("PdpB")}))'
    F["dBp"]=f'=IF(OR({g("lBp")}="",{g("Bd")}=""),"",{g("lBp")}-LOG10(2*{g("Bd")}*1E12))'
    F["Pr"]=f'=IF(OR({g("Pv")}="",{g("Pp")}=""),"",{g("Pv")}/{g("Pp")})'
    F["ddd"]=f'=IF(OR({g("dv")}="",{g("dp")}=""),"",LOG10({g("dp")}/{g("dv")}))'
    F["Lov"]=f'=IF(OR({g("VLlo")}="",{g("Lplo")}=""),"",IF(AND({g("VLlo")}<={g("Lphi")},{g("Lplo")}<={g("VLhi")}),"OK","NO"))'
    F["dLmid"]=f'=IF(OR({g("lLlo")}="",{g("Lp")}=""),"",LOG10({g("Lp")})-(({g("lLlo")}+{g("lLhi")})/2-32))'
    F["dage"]=f'=IF(OR({g("tklo")}="",{g("tslo")}=""),"",LOG10((({g("tslo")}+{g("tshi")})/2)/(({g("tklo")}+{g("tkhi")})/2)))'
    F["MLv"]=f'=IF(OR({g("Lmlo")}="",{g("VLlo")}=""),"",IF(AND({g("VLlo")}<={g("Lmhi")},{g("Lmlo")}<={g("VLhi")}),"OK","NO"))'
    F["MLp"]=f'=IF(OR({g("Lmlo")}="",{g("Lplo")}=""),"",IF(AND({g("Lplo")}<={g("Lmhi")},{g("Lmlo")}<={g("Lphi")}),"OK","NO"))'
    F["dLm"]=f'=IF(OR({g("Lm")}="",{g("Lp")}=""),"",LOG10({g("Lm")}/{g("Lp")}))'
    F["ddm"]=f'=IF(OR({g("dm")}="",{g("dp")}=""),"",LOG10({g("dm")}/{g("dp")}))'
    def thr(k,cellref,msg,signed=False):
        return f'IF({g(k)}="","",IF(ABS({g(k)})>{S}{cellref},"{msg}; ",""))'
    F["FLAGS"]=("=TRIM("+"&".join([
        thr("dPint","$B$2","P20 internal: Pdot(Bdip) vs Pdot(tau_c) inconsistent"),
        thr("dPvp","$B$2","Pdot V13 vs P20 differ"),
        thr("dBp","$B$3","Bp V13 vs 2xBdip P20 differ"),
        f'IF({g("Pr")}="","",IF(ABS({g("Pr")}-1)>0.02,"Period differs (V13/P20 = "&TEXT({g("Pr")},"0.00")&"); ",""))',
        f'IF(OR({g("dv")}="",{g("dplo")}=""),"",IF(OR({g("dv")}<{g("dplo")}-0.005,{g("dv")}>{g("dphi")}+0.005),"Distance V13 outside P20 range; ",""))',
        f'IF({g("Lov")}="NO","L ranges do not overlap; ","")',
        thr("dage","$B$6","Age differs >2x"),
        f'IF({g("MLv")}="NO","M24 L outside V13 range; ","")',
        f'IF({g("MLp")}="NO","M24 L outside P20 range; ","")',
    ])+")")
    Sg=S
    F["wPint"]=f'=IF(OR({g("wPd")}="",{g("wB")}="",{g("wP")}=""),"",LOG10({g("wPd")}/(({g("wB")}*1E12/{S}$B$8)^2/{g("wP")})))'
    F["wPtc"]=f'=IF(OR({g("wPd")}="",{g("wtc")}="",{g("wP")}=""),"",LOG10({g("wPd")}/({g("wP")}/(2*{g("wtc")}*1000*{S}$B$7))))'
    F["wPv"]=f'=IF(OR({g("lPd")}="",{g("wPd")}=""),"",{g("lPd")}-LOG10({g("wPd")}))'
    F["wLu"]=f'=IF({g("wLlo")}="","",IF({g("wLmid")}<>"",{g("wLmid")},SQRT({g("wLlo")}*{g("wLhi")})))'
    F["wdL"]=f'=IF(OR({g("wLu")}="",{g("Lp")}="",{g("Lplo")}=""),"",LOG10({g("wLu")}/{g("Lp")}))'
    F["wdd"]=f'=IF(OR({g("wdmid")}="",{g("dp")}=""),"",LOG10({g("wdmid")}/{g("dp")}))'
    F["wLv"]=f'=IF(OR({g("wLlo")}="",{g("VLlo")}=""),"",IF(AND({g("VLlo")}<={g("wLhi")},{g("wLlo")}<={g("VLhi")}),"OK","NO"))'
    F["wLM"]=f'=IF(OR({g("wLlo")}="",{g("Lmlo")}=""),"",IF(AND({g("wLlo")}<={g("Lmhi")},{g("Lmlo")}<={g("wLhi")}),"OK","NO"))'
    F["wdLM"]=f'=IF(OR({g("wLu")}="",{g("Lm")}=""),"",LOG10({g("Lm")}/{g("wLu")}))'
    F["wdage"]=f'=IF(OR({g("tklo")}="",{g("wtlo")}=""),"",LOG10((({g("wtlo")}+{g("wthi")})/2)/(({g("tklo")}+{g("tkhi")})/2)))'
    def thw(k,cellref,msg): return f'IF({g(k)}="","",IF(ABS({g(k)})>{S}{cellref},"{msg}; ",""))'
    F["wFLAGS"]=("=TRIM("+"&".join([
        thw("wPint","$B$2","web internal: Pdot vs Bdip inconsistent"),
        thw("wPtc","$B$2","web internal: Pdot vs tau_c inconsistent"),
        thw("wPv","$B$2","Pdot V13 vs web differ"),
        f'IF(OR({g("dv")}="",{g("wdlo")}="",{g("wdhi")}=""),"",IF(OR({g("dv")}<{g("wdlo")}-0.005,{g("dv")}>{g("wdhi")}+0.005),"Distance V13 outside web range; ",""))',
        f'IF(OR({g("wdlo")}="",{g("wdmid")}=""),"",IF(OR({g("wdmid")}<{g("wdlo")},{g("wdmid")}>{g("wdhi")}),"web d mid outside its own range; ",""))',
        f'IF({g("wLv")}="NO","L ranges V13 vs web do not overlap; ","")',
        f'IF({g("wLM")}="NO","M24 L outside web range; ","")',
        f'IF({g("wdL")}="","",IF(ABS({g("wdL")})>0.3,"web L changed vs paper by "&TEXT({g("wdL")},"0.00")&" dex; ",""))',
        thw("wdage","$B$6","Age web vs V13 >2x"),
    ])+")")
    for k,x in F.items():
        cell=m.cell(r,idx[k],x); cell.font=black
    for i,h in enumerate(heads,1):
        cc=m.cell(r,i)
        if cc.font.name!=ARIAL: cc.font=black
        cc.number_format=h[3]
        cc.border=Border(bottom=thin)
r=5
byid={}
for p in P20:
    pid=p[0]; assoc=p[2]+(" [disputed candidate; removed from web 25.11.2020]" if p[1].startswith("1E 0102") else "")
    build_row(r,(pid,p[1],assoc,p[3],V13.get(pid),p,M24.get(pid),WEB.get(p[1]))); byid[pid]=r; r+=1
for i,mg in enumerate(MAG):
    pid=100+i+1
    rec=(pid,mg[0],mg[1],"MAG",mg[2:],None,None)
    # emulate V tuple order: P,logPd,logBp,logtc,tklo,tkhi,d,Llo,Lhi,kT,model
    build_row(r,rec); r+=1
known={p[1] for p in P20}
pid=200
for w in WEBROWS:
    if w["name"] in known: continue
    pid+=1
    build_row(r,(pid,w["name"],w["assoc"],w["cls"],None,None,None,w)); r+=1
last=r-1
m.freeze_panes="E5"
m.auto_filter.ref=f"A4:{CL(ncol)}{last}"
red=PatternFill("solid",fgColor="F8CBAD")
for fk in ("FLAGS","wFLAGS"):
    m.conditional_formatting.add(f"{CL(idx[fk])}5:{CL(idx[fk])}{last}",FormulaRule(formula=[f'LEN({CL(idx[fk])}5)>0'],fill=red))
for k in ("Lov","MLv","MLp","wLv","wLM"):
    m.conditional_formatting.add(f"{CL(idx[k])}5:{CL(idx[k])}{last}",FormulaRule(formula=[f'{CL(idx[k])}5="NO"'],fill=red))
tables = catalogue(m)
export_csv(tables)
tables["References"] = [
    {"reference": key, "citation": citation, "url": url}
    for key, (citation, url) in REFERENCES.items()
]
for title, records in tables.items():
    sheet = wb.create_sheet(title)
    keys = list(records[0])
    sheet.append(keys)
    for record in records:
        sheet.append([record[key] for key in keys])
    for column, key in enumerate(keys, 1):
        cell = sheet.cell(1, column)
        cell.font = white_b
        cell.fill = hdr_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        wide = key in {"association", "aliases", "locator", "reference_url", "url",
                       "citation", "uncertainty", "note", "age_basis", "temperature_kind"}
        sheet.column_dimensions[CL(column)].width = 46 if wide else max(14, min(29, len(key)+3))
        for row in sheet.iter_rows(min_row=2, min_col=column, max_col=column):
            item = row[0]
            if key.startswith("L_inf_erg_s"):
                item.number_format = "0.00E+00"
            elif key.startswith(("age_yr", "distance_kpc", "kT_inf_eV", "tau_c_yr")):
                item.number_format = "0.0##"
            elif wide:
                item.alignment = Alignment(wrap_text=True, vertical="center")
            if key in {"reference_url", "url"} and item.value:
                item.hyperlink = item.value
                item.style = "Hyperlink"
    sheet.row_dimensions[1].height = 32
    sheet.sheet_format.defaultRowHeight = 32 if title != "Sources" else 20
    sheet.freeze_panes = "D2" if title in {"Measurements", "Cooling_comparison"} else "B2"
    sheet.auto_filter.ref = sheet.dimensions

exec((ROOT / "src" / "workbook_part2.py").read_text())
