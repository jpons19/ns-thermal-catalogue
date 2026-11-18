"""Second half of build_workbook.py (executed from it): Marino3_detail, VelaJr, Findings, Web_updates and README sheets, sheet order, save."""
# ================= Marino3 detail =================
d3=wb.create_sheet("Marino3_detail")
d3["A1"]="Marino+24 sources: flux -> luminosity checks and model dependence of L_th"; d3["A1"].font=f(bold=True,size=13)
d3["A2"]="Blue = transcribed (M24 Ext. Data Tab. 2, 4, Supp. Tab. 6; P20 Tab. 2); black = formula. Fluxes in 1e-13 erg/cm2/s."; d3["A2"].font=f(italic=True)
d3["A4"]="Constants"; d3["A4"].font=bold
consts=[("kpc in cm",3.0857e21),("sigma_SB (erg/cm2/s/K4)",5.670374e-5),("K per eV",11604.5),("cm per km",1e5)]
for i,(a,b) in enumerate(consts):
    d3.cell(5+i,1,a).font=black; x=d3.cell(5+i,2,b); x.font=blue; x.number_format="0.000E+00"
hd=["Source","d adopted (kpc)","F_th BB","F_th NSMAXG-H","F_th NSMAXG-C","F_th NSMAXG-O","kT_bb (eV)","R_bb (km)","N_nsmaxg (H)",
    "L from BB flux (1e32)","L from H-atm flux (1e32)","L_obs in M24 table (1e32)","L(BB flux)/L_obs","d implied by L_obs (kpc)","M24 L_cool limit (1e32)","P20 L_inf (1e32)","P20 range lo","P20 range hi","P20 kT_inf (eV)","P20 spectral basis"]
r0=10
for j,h in enumerate(hd,1):
    cc=d3.cell(r0,j,h); cc.font=white_b; cc.fill=hdr_fill; cc.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
d3.row_dimensions[r0].height=58
data=[("PSR J0205+6449",2.0,3.02,0.70,0.80,0.70,200,0.6,3.0e-3,1.44,1e-4,1.9,0.8,3.4,"49","NSMAXG+PL, whole surface, d=2 kpc, R=13 km (this work, P20)"),
("PSR B2334+61",3.1,0.68,0.80,0.56,0.68,160,0.9,70e-3,0.78,0.4,0.47,0.12,0.82,"38","NSA (McGowan+06); L for d=1.1 kpc, Table 1 lists d~0.7"),
("CXOU J0852-4617",0.8,25.9,27.0,None,None,397,0.24,2.1e-3,2.0,1.3,20,10,30,"90","NSX carbon, whole surface, T_inf=1.3 MK (Danilenko+15); d=0.77 kpc")]
for i,rw in enumerate(data):
    r=r0+1+i
    src,d,fbb,fh,fc,fo,kt,rbb,nn,lobs,lcool,lp,lplo,lphi,ktp,basis=rw
    lobs = M24_OBS[MARINO[src]["id"]]["L32"]
    lcool = MARINO[src]["cool_L32_limit"]
    for j,v in zip([1,2,3,4,5,6,7,8,9,12,15,16,17,18,19,20],[src,d,fbb,fh,fc,fo,kt,rbb,nn,lobs,lcool,lp,lplo,lphi,ktp,basis]):
        if v is None: continue
        cc=d3.cell(r,j,v); cc.font=blue
    d3.cell(r,10,f'=4*PI()*(B{r}*$B$5)^2*C{r}*1E-13/1E32').font=black
    d3.cell(r,11,f'=IF(D{r}="","",4*PI()*(B{r}*$B$5)^2*D{r}*1E-13/1E32)').font=black
    d3.cell(r,13,f'=J{r}/L{r}').font=black
    d3.cell(r,14,f'=SQRT(L{r}*1E32/(4*PI()*C{r}*1E-13))/$B$5').font=black
    for j,fm in [(2,"0.00"),(3,"0.00"),(4,"0.00"),(5,"0.00"),(6,"0.00"),(7,"0"),(8,"0.00"),(9,"0.0E+00"),(10,"0.000"),(11,"0.000"),(12,"0.00"),(13,"0.00"),(14,"0.00"),(15,"0.0E+00"),(16,"0.00"),(17,"0.00"),(18,"0.00")]:
        d3.cell(r,j).number_format=fm
# web comparison columns
extra=["Web d mid (kpc)","Web L lo (1e32)","Web L mid (1e32)","Web L hi (1e32)","M24 L scaled to web d (1e32)"]
for j,h in enumerate(extra,21):
    cc=d3.cell(r0,j,h); cc.font=white_b; cc.fill=PatternFill("solid",fgColor=grp["W"]); cc.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
for i,pid in enumerate((14,33,3)):
    r=r0+1+i; mrow=4+pid
    for j,k in zip((21,22,23,24),("wdmid","wLlo","wLmid","wLhi")):
        cc=d3.cell(r,j,f"=Master!{CL(idx[k])}{mrow}"); cc.font=f(color="008000"); cc.number_format="0.00"
    cc=d3.cell(r,25,f"=L{r}*(U{r}/N{r})^2"); cc.font=black; cc.number_format="0.00"
    d3.column_dimensions[CL(21)].width=11
    for j in range(22,26): d3.column_dimensions[CL(j)].width=12
d3.cell(r0+4,1,"CXOU J0852 d adopted = 0.8 kpc is the distance implied by M24's own L_obs and flux (col N); the paper gives only the range 0.5-1.0 kpc. Yellow = assumption.").font=f(italic=True)
d3.cell(r0+1+2,2).fill=PatternFill("solid",fgColor="FFFF00")
# BB-equivalent whole-surface luminosity calculator
b0=r0+7
d3.cell(b0-1,1,"Blackbody-equivalent whole-surface luminosity: L = 4 pi R^2 sigma T^4 (order-of-magnitude only; real atmospheres have harder spectra than a BB of the same T_eff)").font=bold
for j,h in enumerate(["Case","kT_inf (eV)","R_inf (km)","L (1e32 erg/s)","Comment"],1):
    cc=d3.cell(b0,j,h); cc.font=white_b; cc.fill=hdr_fill; cc.alignment=Alignment(wrap_text=True,horizontal="center")
cases=[("J0852: M24 hidden-surface limit",50,11,"M24 quotes kT<0.05 keV, L_cool<1.3e32 (BB, R fixed 11 km)"),
("J0852: P20 (2020 paper) whole-surface carbon atmosphere",112,12.6,"T_inf=1.3 MK as quoted in the 2020 paper (superseded on the web page by Ho+2026: L 1.3-6e32, kT 50-300 eV); R_inf assumed here"),
("J0205: M24 hidden-surface limit",4,11,"M24 quotes kT<4e-3 keV, L_cool<1e-4 x 1e32"),
("J0205: P20 whole-surface NSMAXG",49,13,"T_inf=0.57 MK (P20 re-analysis)")]
for i,(a,kt,R,cm) in enumerate(cases):
    r=b0+1+i
    d3.cell(r,1,a).font=black
    for j,v in ((2,kt),(3,R)): d3.cell(r,j,v).font=blue
    d3.cell(r,4,f'=4*PI()*(C{r}*$B$8)^2*$B$6*(B{r}*$B$7)^4/1E32').font=black
    d3.cell(r,4).number_format="0.000"; d3.cell(r,5,cm).font=black
widths=[34,11,9,11,11,11,9,9,11,12,12,12,11,12,12,11,9,9,11,60]
for j,w in enumerate(widths,1): d3.column_dimensions[CL(j)].width=w
d3.column_dimensions["A"].width=44

# ================= Vela Jr analyses =================
vj=wb.create_sheet("VelaJr")
vj["A1"]="CXOU J0852.0-4617 (Vela Jr): published spectral analyses side by side (Ho, Simkhayeva & Potekhin 2026 = Ho+26, arXiv:2601.14388)"; vj["A1"].font=f(bold=True,size=13)
vj["A2"]="Blue = transcribed from Ho+26 Table 2/6 and text, Marino+24, Potekhin+20; black = formula. 'L at ref d' = 4 pi d^2 F x 1e-12 / 1e32 using the quoted unabsorbed flux."; vj["A2"].font=f(italic=True)
vj["A3"]="Reference distance (kpc)"; vj["A3"].font=black; vj["B3"]=1.41; vj["B3"].font=blue
vj["C3"]="Suherli+26, as adopted by Ho+26 (1.41 +- 0.14 kpc)"; vj["C3"].font=black
vh=["Reference","Data","Model","N_H (1e21 cm-2)","kT (eV)","R/d (km/kpc)","L quoted (1e32 erg/s)","Unabs. flux F (1e-12 cgs)","d used (kpc)","L at ref d from F (1e32)","Notes"]
for j,h in enumerate(vh,1):
    cc=vj.cell(5,j,h); cc.font=white_b; cc.fill=hdr_fill; cc.alignment=Alignment(wrap_text=True,horizontal="center",vertical="center")
vj.row_dimensions[5].height=44
vrows=[
("Kargaltsev+02","ACIS-S","BB",3.45,404,0.28,None,None,None,"1-sigma errors"),
("Becker+06","MOS+pn 2001+03","BB",3.22,391,0.285,None,None,None,""),
("Potekhin+20 (Shternin, priv. comm.)","MOS+pn 2003-10","nsx carbon",6.8,133,5.0,20,None,0.77,"Source of the 2020 paper's L = 2e33 (20e32); superseded"),
("Wu+21","pn 2010","carbatm",7.0,145,4.3,None,None,None,""),
("Alford & Halpern 23","pn 2005","carbatm",4.70,132,5.2,None,None,None,""),
("Marino+24","ACIS-S (CC mode) only","BB (hot spot)",4.7,397,0.30,2.0,2.59,0.80,"R/d from R_bb = 0.24 km at d ~ 0.8; d implied by L_obs and flux (Marino3_detail); paper quotes 0.5-1.0 kpc"),
("Ho+26","All XMM+Chandra, joint fit","nsx+nsx (H): hot spot + cool surface",5.68,298,0.64,5.0,2.2,1.41,"kT = hot-spot kT_eff; cool surface kT_eff 57 eV (nsx) / 6.6-8.8e5 K range; total L dominated by hot spot; chi2/dof 511/471"),
]
for i,rw in enumerate(vrows):
    r=6+i
    ref,dat,mod,nh,kt,rd,lq,fl,dd,nt=rw
    for j,v in zip((1,2,3,4,5,6,7,8,9,11),(ref,dat,mod,nh,kt,rd,lq,fl,dd,nt)):
        if v is None: continue
        cc=vj.cell(r,j,v); cc.font=blue if j in (4,5,6,7,8,9) else black
        cc.alignment=Alignment(wrap_text=True,vertical="top")
    if fl is not None:
        cc=vj.cell(r,10,f"=4*PI()*($B$3*Marino3_detail!$B$5)^2*H{r}*1E-12/1E32"); cc.font=f(color="008000"); cc.number_format="0.00"
    for j,fm in ((4,"0.00"),(5,"0"),(6,"0.00"),(7,"0.0"),(8,"0.00"),(9,"0.00")): vj.cell(r,j).number_format=fm
vj.cell(15,1,"Cross-checks").font=bold
chk=[("Unabsorbed flux ratio, Marino+24 / Ho+26","=H11/H12","0.00"),
("Distance-squared ratio, (d Ho+26 / d Marino+24)^2","=(I12/I11)^2","0.00"),
("L ratio, Marino+24 quoted / Ho+26 total","=G11/G12","0.00"),
("Ho+26 cool-surface L, low (1e32)",1.3,"0.0"),
("Ho+26 cool-surface L, high (1e32)",4.0,"0.0"),
("Marino+24 hidden-surface L limit (1e32)",1.3,"0.0"),
("Ratio: Ho+26 cool L (high) / Marino+24 limit","=B20/B21","0.0")]
for i,(a,v,fm) in enumerate(chk):
    r=16+i
    vj.cell(r,1,a).font=black
    cc=vj.cell(r,2,v); cc.font=blue if not isinstance(v,str) else black; cc.number_format=fm
vj.cell(24,1,"Reading: the unabsorbed fluxes agree within ~20%, so Marino's lower L (2.0e32 vs 5e32) comes mainly from the smaller distance, not from the spectrum. At the new distance their flux gives ~6e32. Ho+26 attribute the 'similar' luminosity to ACIS-S-only contamination compensating the smaller distance; the quoted fluxes show only a ~20% flux excess, not the factor ~3 needed.").font=f(italic=True)
vj.cell(26,1,"Published SNR ages: 2.4–5.1 kyr (Allen et al. 2015, used by Ho+26); 1.6–3.3 kyr (Suherli et al. 2026, shock speeds at the revised distance). See VelaJr_ages.").font=f(italic=True)
vj.cell(25,1,"The Potekhin web entry for Vela Jr (L 1.3-6e32, d 1.27-1.55 kpc) is derived from Ho+26, so it is not an independent confirmation.").font=f(italic=True)
for j,w in enumerate([40,24,30,12,9,12,14,14,10,14,70],1): vj.column_dimensions[CL(j)].width=w
vj.freeze_panes="A6"

# ================= Findings =================
fd=wb.create_sheet("Findings")
fd["A1"]="Discrepancies and interpretation issues (updated with Potekhin web catalogue, 03.08.2026)"; fd["A1"].font=f(bold=True,size=13)
fd["A2"]="Evidence column links live to Master / Marino3_detail. 'Confidence' = how sure I am it is an error rather than a modelling choice. 'web' = Potekhin catalogue page; 'P20' = 2020 paper."; fd["A2"].font=f(italic=True)
H=["#","Type","Confidence","Source(s)","Item","Evidence (live)","Evidence meaning","Suggested next step"]
for j,h in enumerate(H,1):
    cc=fd.cell(4,j,h); cc.font=white_b; cc.fill=hdr_fill; cc.alignment=Alignment(wrap_text=True,horizontal="center")
mr=lambda pid:4+pid
byname={}
for rr in range(5,last+1): byname[m.cell(rr,2).value]=rr
R=lambda n:byname[n]
Mx=lambda k,n:f"=Master!{CL(idx[k])}{R(n)}"
rngF=lambda k:f"Master!{CL(idx[k])}5:{CL(idx[k])}{last}"
items=[
("Data error","High","V13","PSR J1740+1000: V13 log Pdot = -11.7. The web table lists dP/dt = 2.15e-14 (log -13.67) with Bdip and tau_c that agree with it, so V13 is ~2 dex too high. V13's log Bp (13.6 vs 12.6), Edot and tau_c (3.1 vs 5.1) inherit the error.",Mx("wPv","PSR J1740+1000"),"dlog Pdot, V13 / web","Correct V13 row; J1740 is not a high-B object."),
("Data error","High","web (and P20)","PSR J0007+7303: Bdip = 1.1e12 G is inconsistent with the same row's dP/dt = 3.6e-13 and tau_c = 13.9 kyr (implies ~1.1e13 G). The typo is still on the web page.",Mx("wPint","PSR J0007+7303"),"dlog Pdot, web Pdot vs Bdip","Treat Bdip as 11e12 G; report to the maintainers."),
("Data error","High","web","PSR J0633+1746 (Geminga): web dP/dt = 1.10e-15, but its own Bdip (1.6e12) and tau_c (343 kyr) need 1.1e-14, which is also what V13 has. One-digit typo on the web page.",Mx("wPint","PSR J0633+1746"),"dlog Pdot, web Pdot vs Bdip","Use 1.1e-14."),
("Resolved","High","P20 paper","Typos in the 2020 paper are fixed on the web: RX J2143 Bdip (200 -> 20e12 G, fixed 14.09.2020) and PSR J1154-6250 L error (now L = 1.2-2.2e30, matching my recomputation). RX J0720 period: paper has 16.78 s, web has 8.391 s (Bogdanov & Ho 2024), in line with V13. Use the web values.",Mx("wP","RX J0720.4-3125"),"Web P (s) for RX J0720","Cite the web page, not the paper table, for these."),
("Data error","High","M24","PSR J0205+6449: M24 tau_c = 58.8 kyr (Table 1) / 54 kyr (Methods). M24's own P and Pdot (1.935e-13) match the web (1.94e-13), and the web gives tau_c = 5.37 kyr; P/(2 Pdot) gives 5.4 kyr.",Mx("wtc","PSR J0205+6449"),"Web tau_c (kyr)","Re-check the 'even at the tau_c upper limit' argument with 5.4 kyr."),
("Convention","High","V13, M24 vs P20","Bp (polar, 6.4e19 sqrt(P Pdot)) vs Bdip (equatorial, 3.2e19): factor 2. Across matched pulsars log Bp(V13) - log(2 Bdip) ~ 0 (example: B1706-44).",Mx("dBp","PSR B1706-44"),"dlog Bp, B1706-44","Store Bp and Bdip both, labelled."),
("Update","High","M24 vs Ho+26 / web","Vela Jr (CXOU J0852): Ho+26 analyse all XMM and Chandra spectra at d = 1.41 +- 0.14 kpc (Suherli+26) and find total L = (5+-1)e32, dominated by a hot spot, and a cool-surface L = (1.3-4.0)e32. M24's L = 2.0e32 is 2.5x lower than the total but matches the cool range; the two analyses agree to within a factor ~2.5 and Ho+26 independently conclude Vela Jr is cold. The 2020 paper's 2e33 is superseded. Note the web entry is derived from Ho+26, so it is not independent.",f"=VelaJr!B18","L ratio, M24 quoted / Ho+26 total","Use Ho+26 as the Vela Jr baseline (cool L for cooling comparison, total L for energetics)."),
("Distance","High","M24 vs Ho+26","M24 adopts d = 0.5-1.0 kpc (Allen+15); Ho+26 use 1.41 kpc. The quoted unabsorbed fluxes (2.59 vs 2.2e-12) agree within ~20%, so M24's lower L is mainly the distance. Scaled to 1.41 kpc, M24's flux gives ~6e32. Ho+26 say the contamination of the ACIS-S-only flux compensates the smaller distance; the numbers show a ~20% flux excess, not a factor ~3.",f"=VelaJr!B16","Flux ratio, M24 / Ho+26","Recompute M24's Vela Jr point at 1.41 kpc and check it against their SLy4 band."),
("Interpretation","Medium","M24 vs Ho+26","Spectral model: Ho+26 find that a single BB fits poorly (chi2/dof 1.21), that non-magnetic or magnetic hydrogen atmospheres with a hot spot (kT_eff ~3.5e6 K) plus a cooler surface fit best, and that carbon is a worse fit than hydrogen. This agrees with M24's finding that only hydrogen (NSMAXG) works, and with M24's R_bb ~0.24 km hot spot. It undercuts the 2020 paper's carbon whole-surface fit as the preferred model. Ho+26 find a cool component at kT_inf ~46-61 eV with L = (1.3-4.0)e32, at or above M24's hidden-surface limit (kT < 50 eV, L < 1.3e32), which used only ACIS-S.",f"=VelaJr!B22","Ratio: Ho+26 cool L (high) / M24 hidden-surface limit","Treat M24's hidden-surface limits for the other two sources with caution."),
("Interpretation","Medium","M24","Hidden-surface limits are conditional on the hot-spot BB model and an 11 km BB. For J0205 the limit (kT < 4 eV, L < 1e-4 x 1e32) is far below P20/web's whole-surface NSMAXG fit (kT_inf 49 eV, L ~ 2e32) to the same Chandra data.",f"=Marino3_detail!D{b0+4}","BB-equivalent L for the whole-surface fit (1e32)","Show both decompositions in the unified table."),
("Distance","High","V13/M24 vs web","PSR B2334+61: V13 and M24 use 3.1 kpc (DM, NE2001). The web now gives 1.1 kpc (0.5-1.7), consistent with its L = 0.12-0.82e32 (the 2020 paper's d ~0.7 is gone). L scales as d^2; at 1.1 kpc M24's blackbody L (0.78e32 at 3.1 kpc) would fall to ~0.1e32.",f"=LOG10(Master!{CL(idx['wdmid'])}{R('PSR B2334+61')}/Master!N{R('PSR B2334+61')})","dlog d, web / V13","Carry L for each distance candidate; check which d M24's SLy4 exclusion needs."),
("Distance","Medium","V13 vs web","V13 distances outside the web range (PSR B1055-52 0.73 vs 0.2-0.5; RX J1308 0.50 vs 0.35-0.40; B2334+61).",f'=COUNTIF({rngF("wFLAGS")},"*Distance V13 outside*")',"Count of V13 distances outside web range","Update distances; recompute L."),
("Spectral model","Medium","V13 vs web","Matched sources whose V13 and web L ranges do not overlap: Kes 79, Cas A, B0656+14, Vela pulsar, RX J1308. Cause is model choice (BB/NSA in V13, carbon atmospheres and updated fits on the web).",f'=COUNTIF({rngF("wLv")},"NO")',"Number of non-overlapping L ranges","Keep the model name next to every L."),
("Update","Medium","web vs P20","Values changed since the paper: Vela Jr, Calvera (d 3-4 kpc, L 1.5-9e33, age 10-20 kyr), 1WGA J1713, J1957, J1740, J0538 (d), Cas A, PSR B0656+14 (L now 3.5e32 vs 6.7e32). Sources with |dlog L| > 0.3 dex:",f'=COUNTIF({rngF("wdL")},">0.3")+COUNTIF({rngF("wdL")},"<-0.3")',"Count of L changes > 0.3 dex","Use web values as the baseline."),
("Data error","Medium","web","RX J1605.3+3249 distance row reads 0.035 / 0.5 / 0.40 (min << max, mid above max); looks like typos for 0.35 / 0.40 / 0.5.",Mx("wdlo","RX J1605.3+3249"),"Web d min (kpc)","Use P20-paper 0.09-0.4 or V13 0.10 until confirmed."),
("Missing data","Medium","M24","The 70-source sample is not available (Dehman+ in prep). M24 Fig.1 shows B0656+14 near 2-3e31 by eye; V13, P20 and the web give 3.5-7e32 (web changed to 3.5e32 on 01.02.2021, Zharikov+21); Vela ~4e32 by eye matches web 4.2e32 rather than V13.",Mx("wLmid","PSR B0656+14"),"Web L mid for B0656+14 (1e32)","Obtain the M24 table; verify B0656 first."),
("Context","Medium","M24 vs Ho+26 / web","Prior art: Ho+26 and P20/web already cite Page+04/09 and Yakovlev & Pethick 04 for J0205, B2334 and J0007 needing fast cooling, and list J0007 as L < 3e31 at ~9 kyr, colder than any M24 source. P20 is not in M24's references. Ho+26's BSk24 code puts the direct-Urca threshold at 1.59 Msun, so M24's best-fit 1.6 Msun BSK24 model sits just above it (M24 says DU opens above 1.6): results are close to the threshold and need a check of the central density vs 8.25e14 g/cm3.",Mx("wLhi","PSR J0007+7303"),"Web L upper limit for J0007 (1e32)","Check M24's 1.6 Msun BSK24 central density; add J0007 to the cold-source set."),
("Interpretation","Medium","M24 vs V13","'Standard' cooling is not the same: V13 curves include direct Urca for M > ~1.5 Msun and attribute B2334, Vela, J1740 to it; M24 uses SLy4 (no DU at any mass) as 'minimal'.",None,"","Define the baseline per EoS (DU threshold mass) in the unified table."),
("Statistics","Medium","M24","Ages: 10% assumed (V13 used 50%); classifier marginal EoS accuracy ~50% at 0.2 dex; 4D table gives SLy4 = 5.4% for J0205 (text: <5%).",None,"","Rerun the exclusion with 30-50% age errors."),
("Coverage","Info","web","The web page adds J0554+3107, B0950+08, J0837-2454, eRASSU J1317 and the SN 1987A remnant (upper limit), and drops the disputed 1E 0102.2-7219 candidate. Magnetars exist only in V13.",None,"",""),
]
for i,it in enumerate(items):
    r=5+i
    typ,conf,src,txt,ev,evm,nxt=it
    for j,v in enumerate([i+1,typ,conf,src,txt,ev,evm,nxt],1):
        if v is None: continue
        cc=fd.cell(r,j,v); cc.alignment=Alignment(wrap_text=True,vertical="top")
        cc.font=f(color="008000") if (j==6 and isinstance(v,str) and v.startswith("=")) else black
    fd.cell(r,6).number_format="0.00"
for j,w in enumerate([4,15,11,16,90,12,32,48],1): fd.column_dimensions[CL(j)].width=w
fd.freeze_panes="A5"

# ================= Web updates =================
wu=wb.create_sheet("Web_updates")
wu["A1"]="Potekhin catalogue page - summary of updates since the 2020 paper (verbatim from the page)"; wu["A1"].font=f(bold=True,size=13)
import json
for i,t in enumerate(json.load(open(ROOT/"data"/"web_updates.json"))):
    cc=wu.cell(3+i,1,t); cc.font=black; cc.alignment=Alignment(wrap_text=True,vertical="top")
wu.column_dimensions["A"].width=160

# ================= README =================
rd=wb.create_sheet("README")
lines=[
("Cross-matched catalogue of thermally emitting isolated neutron stars",True),
("References: Vigano et al. 2013 (V13); Potekhin et al. 2020 paper (P20); Potekhin catalogue web page, last update 03.08.2026 (web); Marino et al. 2024 (M24, three cold sources).",False),
("The web page supersedes the P20 paper table for many sources (see Web_updates); both are kept so changes are visible.",False),
("",False),
("Sheets",True),
("Findings - discrepancies / errors / updates, with live evidence cells.",False),
("Sources and Measurements contain the full cross-match and literature values. Cooling_comparison is a plotting sample with one luminosity per source and independent ages. See docs/DATA_DICTIONARY.md.",False),
("Master retains the original wide cross-match and formula checks. VelaJr_ages records both published SNR age estimates.",False),
("Marino3_detail - flux-to-luminosity checks for the three M24 sources, with web L and distance-scaled M24 L.",False),
("VelaJr - published analyses of CXOU J0852-4617 side by side, including Ho et al. 2026, with flux/distance cross-checks.",False),
("Web_updates - the page's update log. Settings - tolerances and constants used by formulas.",False),
("",False),
("Conventions",True),
("Blue = transcribed input; black = formula; green = cross-sheet link. Blank = not given.",False),
("V13: log values as printed; Bp is the POLAR field (6.4e19 sqrt(P Pdot)); kT_bb is a blackbody-type temperature at infinity.",False),
("P20 / web: Bdip is the EQUATORIAL field (3.2e19 sqrt(P Pdot)), so Bp = 2 Bdip. L and kT are redshifted and may come from atmosphere models. The web gives L in 1e33 erg/s; converted here to 1e32. Web ages in yr and tau_c in yr; converted to kyr.",False),
("Web ranges: min / mid / max; where mid is '---' the geometric mean of min and max is used for comparisons ('L used').",False),
("M24: L_obs in 1e32 erg/s from hot-spot BB flux, 90% errors; ages are the main-text values from the archived GitHub JSON. Marino et al. adopted 10% analysis uncertainties for the first two sources.",False),
("",False),
("Transcription choices (please review)",True),
("P20 paper: ranges converted to midpoints / lo-hi bounds; '~' values have no uncertainty, so lo = hi or my own plausible bound was used (soft). P20 J1154 L error taken as +-0.005 (recomputed).",False),
("P20 paper L upper limits have no lo/hi, so overlap tests skip them. IC 443 timing left blank (estimates only).",False),
("Web table parsed automatically from the saved HTML (59 rows, 16 numeric fields each, all rows parsed). Web J1957+5033 and some others have blank mid values.",False),
("M24 J0852 distance 0.8 kpc is implied by M24's flux and L_obs (the paper gives 0.5-1.0 kpc).",False),
("",False),
("Flag logic",True),
("FLAGS (col BF): V13 vs P20-paper vs M24. FLAGS web (col CI): V13, P20 paper and M24 vs web. Distance flag = V13 value outside the other range; L flag = ranges do not overlap; Pdot/age use Settings tolerances.",False),
("Figure-derived statements (M24 Fig.1) are my visual reading and are marked as such.",False),
]
for i,(t,b) in enumerate(lines,1):
    cc=rd.cell(i,1,t); cc.font=f(bold=True,size=12 if i==1 else 10) if b else black; cc.alignment=Alignment(wrap_text=True,vertical="top")
rd.column_dimensions["A"].width=150
order = ["README", "Cooling_comparison", "Sources", "Measurements", "References",
         "VelaJr_ages", "Findings", "Master", "Marino3_detail", "VelaJr", "Web_updates", "Settings"]
wb._sheets=[wb[n] for n in order]
wb.active=0
wb.save(str(ROOT/"data"/"NS_thermal_crossmatch.xlsx"))
print("saved")
