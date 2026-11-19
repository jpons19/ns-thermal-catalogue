from pathlib import Path
from collections import defaultdict, Counter
import csv
import argparse
import json
from matplotlib.patches import Rectangle, Patch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from adjustText import adjust_text

ROOT = Path(__file__).resolve().parents[1]
with (ROOT/'data/review_decisions.json').open() as stream:
    REVIEW = json.load(stream)['sources']
VELA = REVIEW['21']
B2334 = REVIEW['33']
MONOGEM = REVIEW['20']

parser = argparse.ArgumentParser(description='Labelled neutron-star luminosity-age diagram')
parser.add_argument('--b2334-extended', action='store_true', help='Overlay provisional B2334 uncertainty envelope')
parser.add_argument('--b2334-marino-distance', action='store_true', help='Compare Marino distance with original point and conditional Potekhin rescaling')
parser.add_argument('--vela-revised', action='store_true', help='Show accepted Vela age-luminosity box; carry B2334 working selection')
parser.add_argument('--original-catalogue', action='store_true', help='Reproduce original catalogue locations without review overlays')
parser.add_argument('--monogem-revised', action='store_true', help='Show current review ranges, with Monogem error bars (default)')
parser.add_argument('--cooling-curves', action='store_true', help='Overlay the five saved 1.4-solar-mass cooling curves')
args = parser.parse_args()
if sum([args.b2334_extended,args.b2334_marino_distance,args.vela_revised,args.original_catalogue,args.monogem_revised]) > 1:
    parser.error('Choose at most one plotting mode')
if not any([args.b2334_extended,args.b2334_marino_distance,args.vela_revised,args.original_catalogue,args.monogem_revised]):
    args.monogem_revised = True
if args.monogem_revised:
    args.vela_revised = True
if args.b2334_marino_distance:
    args.b2334_extended = True

# Outer bounds of alternative scenarios, with their published uncertainties.
# Age: M24 7.7 kyr minus its assumed 10% error, through M24 tau_c=41.1 kyr.
# L low: M24 bolometric BB flux (0.68-0.10)e-13 at d=0.5 kpc.
# L high: McGowan R=13 km, M=1.4 Msun, quoted T_inf=(0.65+0.13) MK.
# This high branch takes McGowan's redshift labels literally; convention unresolved.
# No covariance or refitting enters this conservative rectangular projection.
B2334_AGE_LO = 7.7e3 * 0.9
B2334_AGE_HI = 41.1e3
B2334_L_LO = 4 * np.pi * (0.5 * 3.0856775814913673e21)**2 * (0.68-0.10) * 1e-13
redshift_13km = 1 / np.sqrt(1 - 2.95325 * 1.4 / 13)
B2334_L_HI = 4 * np.pi * (13e5 * redshift_13km)**2 * 5.670374419e-5 * ((0.65+0.13)*1e6)**4

DATA = ROOT/'data'
EXCLUDED=set(json.loads((ROOT/'data/excluded_sources.json').read_text())['sources'])
(ROOT/'figures').mkdir(exist_ok=True)
with (DATA/'measurements.csv').open() as stream:
    entries = list(csv.DictReader(stream))
by_id = defaultdict(list)
for row in entries:
    if (row['class'] in ('RPP', 'XINS', 'UL', 'Hot-spot PSR') or row['source_id'] in ('3','13')) and row['source_id'] not in EXCLUDED:
        by_id[int(row['source_id'])].append(row)
points=[]
for source_id, alternatives in by_id.items():
    row=next(r for r in alternatives if r['reference']=='WEB').copy()
    if row['age_yr']:
        basis='independent'
    else:
        age_options=[r for r in alternatives if r['age_yr'] and r['reference'] in ('V13','P20')]
        if age_options:
            age_row=age_options[-1]
            for field in ('age_yr','age_yr_lo','age_yr_hi'):
                row[field]=age_row[field]
            row['age_reference']=age_row['reference']
            basis='independent'
        else:
            row['age_yr']=row['tau_c_yr']
            row['age_yr_lo']=row['age_yr_hi']=''
            basis='characteristic'
    if not row['age_yr'] or not row['L_inf_erg_s']:
        raise ValueError(row['name'])
    row['basis']=basis
    row['id']=source_id
    points.append(row)
assert len(points)==41
print(Counter(p['basis'] for p in points))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':12,
 'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False,
 'savefig.facecolor':'white','mathtext.fontset':'dejavusans'})
fig,axes=plt.subplots(1,2,figsize=(18,10.2),sharex=True,sharey=True)
fig.subplots_adjust(left=.07,right=.98,bottom=.185,top=.87,wspace=.10)
fig.suptitle('Thermally emitting neutron stars — catalogue locations',x=.07,y=.965,ha='left',fontsize=21,weight='medium')
fig.text(.07,.927,'Rotation-powered pulsars and X-ray isolated neutron stars · provisional values for discussion',fontsize=12,color='#56646b')
colors={'RPP':'#246187','XINS':'#b36a15','UL':'#246187','Hot-spot PSR':'#86719f','CCO/TINS':'#287549'}
markers={'RPP':'o','XINS':'D','UL':'v','Hot-spot PSR':'s','CCO/TINS':'*'}
aliases={3:'Vela Jr.',13:'Cas A',14:'J0205+6449 †',17:'J0617+2221 (IC 443)',19:'Geminga',20:'B0656+14 (Monogem)',21:'Vela',33:'B2334+61 †',42:'RX J1308 (RBS 1223)',47:'Crab',202:'B0950+08'}

def label(p):
    if p['id'] in aliases:
        return aliases[p['id']]
    return p['name'].replace('PSR ','').replace('RX J','RX J').replace('.0-5022','−5022').replace('.4-3125','−3125').replace('.4-4123','−4123').replace('.3+3249','+3249').replace('.5-3754','−3754').replace('.0+0654','+0654')

COOLING_STYLES = [('BSk22','#b23a48','-'),('BSk24','#176aa3','-'),('BSk25*','#8a5b19','--'),('BSk26','#363636','-.'),('DDFGOS(APR)*','#7653a3',':')]

for ax,basis in zip(axes,('independent','characteristic')):
    ax.set(xscale='log',yscale='log',xlim=(220,5e7),ylim=(1.1e28,1.4e35))
    ax.set_xlabel('Age (yr)' if basis=='independent' else r'Characteristic age $\tau_c=P/(2\dot P)$ (yr)',labelpad=10)
    ax.grid(axis='both',which='major',color='#dce2e4',linewidth=.7,zorder=0)
    ax.tick_params(which='both',direction='out')
    group=[p for p in points if p['basis']==basis]
    ax.set_title(('Independent age estimate' if basis=='independent' else 'Characteristic age only in the catalogue')+f'  ·  {len(group)} sources',loc='left',pad=15)
    texts=[]
    if args.cooling_curves:
        curves=np.genfromtxt(DATA/'cooling_five_eos.csv',delimiter=',',names=True,dtype=None,encoding='utf-8')
        for model,color,style in COOLING_STYLES:
            c=curves[curves['model']==model]
            ax.plot(c['time_years'],c['L_infinity_erg_s'],style,color=color,lw=1.7,zorder=2)
    if args.b2334_extended and basis == 'independent':
        ax.add_patch(Rectangle(
            (B2334_AGE_LO, B2334_L_LO),
            B2334_AGE_HI-B2334_AGE_LO, B2334_L_HI-B2334_L_LO,
            facecolor='#cf5260', edgecolor='#b92d40', alpha=.19, linewidth=1.5, zorder=1))
        ax.plot([B2334_AGE_LO, B2334_AGE_HI, B2334_AGE_HI, B2334_AGE_LO, B2334_AGE_LO],
                [B2334_L_LO, B2334_L_LO, B2334_L_HI, B2334_L_HI, B2334_L_LO],
                color='#b92d40', linewidth=1, alpha=.8, zorder=2)
    if args.b2334_marino_distance and basis == 'independent':
        # Cover the previous box with no fill: old bounds remain dashed for comparison.
        ax.patches[-1].set_facecolor('none')
        ax.patches[-1].set_edgecolor('#999999')
        ax.patches[-1].set_linestyle('--')
        ax.lines[-1].set_color('#999999')
        ax.lines[-1].set_linestyle('--')
        # Marino Supplementary Table 6: propagated 90% luminosity interval.
        ax.add_patch(Rectangle((B2334_AGE_LO, 2.4e31), B2334_AGE_HI-B2334_AGE_LO,
                               2.5e32-2.4e31, facecolor='#e5a83f', edgecolor='#b67517', alpha=.30, zorder=2))
        ax.errorbar(1.1e4, 1.5e32, yerr=[[1.2e32],[1.0e32]], fmt='s', mfc='white', color='#267b77', capsize=3, zorder=6)
        texts.append(ax.text(1.2e4, 1.6e32, 'P20: 13 km', fontsize=9, color='#267b77', zorder=7))
        # Sensitivity calculation only: fixed spectral shape, freely varying area.
        scaled = 4.7e31*(3.1/1.1)**2
        ax.scatter([7.7e3], [scaled], s=85, marker='D', facecolors='white', edgecolors='#643994', zorder=6)
        ax.errorbar(7.7e3, scaled, yerr=[[scaled-1.2e31*(2.1/1.1)**2],
                                       [8.2e31*(3.3/1.1)**2-scaled]],
                    fmt='none', ecolor='#643994', capsize=4, linestyle='--', zorder=4)
        texts.append(ax.text(1.5e4, 5e32, 'Potekhin rescaled*', fontsize=9, color='#643994', zorder=7))
    if args.vela_revised and basis == 'independent':
        ax.add_patch(Rectangle((VELA['age_yr_lo'],VELA['L_inf_erg_s_lo']),VELA['age_yr_hi']-VELA['age_yr_lo'],VELA['L_inf_erg_s_hi']-VELA['L_inf_erg_s_lo'],facecolor='#339d91',edgecolor='#086f66',alpha=.28,linewidth=1.6,zorder=1))
        ax.add_patch(Rectangle((B2334['display_age_yr_lo'],B2334['L_inf_erg_s_lo']),B2334['display_age_yr_hi']-B2334['display_age_yr_lo'],B2334['L_inf_erg_s_hi']-B2334['L_inf_erg_s_lo'],facecolor='#e5a83f',edgecolor='#b67517',alpha=.22,zorder=1))
    if args.monogem_revised and basis == 'independent':
        d=REVIEW['14']
        ax.add_patch(Rectangle((d['age_yr_lo'],d['L_inf_erg_s_lo']),d['age_yr_hi']-d['age_yr_lo'],d['L_inf_erg_s_hi']-d['L_inf_erg_s_lo'],facecolor='#d96a78',edgecolor='#b03850',alpha=.23,lw=1.6,zorder=1))
    for p in group:
        x=float(p['age_yr']); y=float(p['L_inf_erg_s'])
        lo=float(p['age_yr_lo']) if p['age_yr_lo'] else x
        hi=float(p['age_yr_hi']) if p['age_yr_hi'] else x
        lower=float(p['L_inf_erg_s_lo']) if p['L_inf_erg_s_lo'] else y
        upper=float(p['L_inf_erg_s_hi']) if p['L_inf_erg_s_hi'] else y
        if args.b2334_marino_distance and p['id']==33:
            ax.scatter([x],[y],s=60,marker='o',facecolors='white',edgecolors='#777777',zorder=5)
            ax.errorbar(x,y,yerr=[[y-lower],[upper-y]],fmt='none',ecolor='#777777',capsize=3,zorder=4)
            y=7.8e31; lower=2.4e31; upper=1.09e32
            lo=B2334_AGE_LO; hi=7.7e3*1.1
        if args.vela_revised and p['id']==33:
            y=B2334['fiducial_L_inf_erg_s']; lower=B2334['marker_L_inf_erg_s_lo']; upper=B2334['marker_L_inf_erg_s_hi']; lo=B2334['display_age_yr_lo']; hi=B2334['marker_age_yr_hi']
        if args.vela_revised and p['id']==14:
            lo=REVIEW['14']['age_yr_lo']; hi=REVIEW['14']['age_yr_hi']
        if p['id']==3:
            d=REVIEW['3'];x=d['display_age_yr'];y=d['display_L_inf_erg_s']
            lo=d['display_age_yr_lo'];hi=d['display_age_yr_hi'];lower=d['display_L_inf_erg_s_lo'];upper=d['display_L_inf_erg_s_hi']
        if p['id']==13:
            d=REVIEW['13'];x=d['display_marker_age_yr'];y=d['fiducial_L_inf_erg_s']
            lo=d['age_yr_lo'];hi=d['age_yr_hi'];lower=d['L_inf_erg_s_lo'];upper=d['L_inf_erg_s_hi']
        if args.monogem_revised and p['id'] in (17,30,46,48):
            d=REVIEW[str(p['id'])];lo=d['age_yr_lo'];hi=d['age_yr_hi']
            if p['id']==17:
                x=d['display_marker_age_yr'];lower=d['L_inf_erg_s_lo'];upper=d['L_inf_erg_s_hi']
        if args.monogem_revised and p['id']==20:
            lo=MONOGEM['age_yr_lo'];hi=MONOGEM['age_yr_hi']
            lower=MONOGEM['L_inf_erg_s_lo'];upper=MONOGEM['L_inf_erg_s_hi']
        ul=p['luminosity_upper_limit']=='True'
        if args.monogem_revised and p['id']==30:
            y=REVIEW['30']['L_inf_erg_s_upper_limit'];ul=True
        color='#b92d40' if args.b2334_extended and p['id']==33 else colors[p['class']]
        if args.monogem_revised and p['id']==14: color='#b03850'

        if args.vela_revised and p['id']==21: color='#086f66'
        if args.vela_revised and p['id']==33: color='#a67320'
        ax.errorbar(x,y,xerr=[[max(0,x-lo)],[max(0,hi-x)]],
            yerr=[[y*.48],[0]] if ul else [[max(0,y-lower)],[max(0,upper-y)]],
            uplims=ul,fmt='none',ecolor=color,alpha=.65,capsize=2,elinewidth=1,zorder=2)
        face=color if basis=='independent' else 'white'
        if p['id'] in (3,14):
            face='white'
        if not (args.monogem_revised and p['id']==30):
            ax.scatter(x,y,s=100 if p['id']==13 else 46,marker=markers[p['class']],facecolors=face,edgecolors=color,linewidths=1.3,zorder=4)
        texts.append(ax.text(x,y,label(p),fontsize=9.2,color=color,zorder=6,
                            bbox={'facecolor':'white','edgecolor':'none','alpha':.8,'pad':.5}))
    fig.canvas.draw()
    np.random.seed(6)
    adjust_text(texts,ax=ax, x=[float(p['age_yr']) for p in group], y=[float(p['L_inf_erg_s']) for p in group],
       expand=(1.12,1.35),force_text=(.55,.7),force_static=(.25,.4),force_pull=(.015,.015),
       ensure_inside_axes=True,iter_lim=650,min_arrow_len=8,
       arrowprops={'arrowstyle':'-','color':'#8a959b','lw':.6},prevent_crossings=True)
axes[0].set_ylabel(r'Redshifted thermal luminosity $L_\gamma^\infty$ (erg s$^{-1}$)',labelpad=9)
legend=[Line2D([],[],marker='o',ls='',color=colors['RPP'],label='Pulsar',ms=6),
 Line2D([],[],marker='D',ls='',color=colors['XINS'],label='XINS',ms=6),
 Line2D([],[],marker='s',ls='',color=colors['Hot-spot PSR'],label='Small hot spot',ms=6),
 Line2D([],[],marker='v',ls='',color=colors['UL'],label='Thermal upper limit',ms=6)]
if args.vela_revised:
    legend.extend([Patch(facecolor='#339d91',alpha=.4,label='Vela accepted envelope'),Patch(facecolor='#e5a83f',alpha=.35,label='B2334 provisional envelope')])
elif args.b2334_marino_distance:
    legend.extend([Patch(facecolor='#e5a83f',alpha=.4,label='Marino + P20 compatible fit'),
                   Line2D([],[],marker='D',ls='',color='#643994',mfc='white',label='Potekhin rescaled*')])
elif args.b2334_extended:
    legend.append(Patch(facecolor='#cf5260', edgecolor='#b92d40', alpha=.3, label='B2334 extended range'))
if args.monogem_revised:
    legend.append(Patch(facecolor='#d96a78',alpha=.4,label='J0205 selected envelope'))
if args.cooling_curves:
    for model,color,style in COOLING_STYLES:
        axes[1].plot([],[],style,color=color,label=model,lw=1.7)
    axes[1].legend(title='EOS, 1.4 M☉',loc='upper right',framealpha=.95,fontsize=9,title_fontsize=9)
fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.065,.081 if args.monogem_revised else .087 if args.b2334_marino_distance or args.vela_revised else .10),ncol=4 if args.monogem_revised else 6 if args.b2334_marino_distance or args.vela_revised else (5 if args.b2334_extended else 4),frameon=False,columnspacing=1.7 if args.b2334_extended else 2.4)
if args.monogem_revised:
    fig.text(.07,.060,'IC 443: adopted age 3–20 kyr and L∞ = (1.0–3.5) × 10³² erg/s, shown as error bars. Luminosity marker retained for comparison.',fontsize=9.6,color='#4d5b62')
    fig.text(.07,.038,'J0205 spans small-area and whole-surface interpretations; its historical age is disputed. Review boxes have no common confidence level.',fontsize=9.6,color='#4d5b62')
    fig.text(.07,.016,'Open green star: Vela Jr.; filled green star: Cas A. Monogem: error bars only. Tracks use true age; τc is a proxy.',fontsize=9.6,color='#4d5b62')
    filename = 'ns_monogem_revised_errors.png'
elif args.vela_revised:
    fig.text(.07,.073,f"Vela: accepted age {VELA['age_yr_lo']/1e3:g}–{VELA['age_yr_hi']/1e3:g} kyr; L∞ = ({VELA['L_inf_erg_s_lo']/1e32:g}–{VELA['L_inf_erg_s_hi']/1e32:g}) × 10³² erg/s. Catalogue point retained for comparison.",fontsize=9.6,color='#4d5b62')
    fig.text(.07,.048,'Vela envelope spans spectral/radius interpretations; Viganò 2013 excluded. Selected bounds have no common statistical confidence level.',fontsize=9.6,color='#4d5b62')
    fig.text(.07,.023,'B2334 retains the working Marino-distance selection; its age extent remains provisional. All other sources retain the original catalogue values.',fontsize=9.6,color='#4d5b62')
    filename = 'ns_vela_revised_errors.png'
elif args.b2334_marino_distance:
    fig.text(.07,.073,'B2334: red = Marino; teal = P20 13 km fit (offset horizontally for clarity). Gold luminosity envelope: 2.4 × 10³¹–2.5 × 10³² erg/s; mixed confidence levels.',fontsize=9.4,color='#4d5b62')
    fig.text(.07,.048,'* Purple: conditional fixed-spectrum rescaling of Potekhin from 1.1 to 3.1 (+0.2/−1.0) kpc; requires a different emitting area, not a refit.',fontsize=9.4,color='#4d5b62')
    fig.text(.07,.023,'Age span retained provisionally; reassess remnant age at 3.1 kpc. Teal fit has inferred d = 3.2 ± 1.7 kpc, compatible with Marino; no refit. Grey = previous bounds.',fontsize=9.4,color='#4d5b62')
    filename = 'ns_b2334_marino_distance.png'
elif args.b2334_extended:
    fig.text(.07,.073, 'B2334 current point: 7.7 kyr; L∞ = 4.7 × 10³¹ erg/s, published range (1.2–8.2) × 10³¹ erg/s.',fontsize=9.7,color='#4d5b62')
    fig.text(.07,.048, 'Shaded box: age 6.93–41.1 kyr; L∞ = 1.73 × 10³⁰–6.54 × 10³² erg/s. Includes alternative distances, spectral models and the redshift-convention ambiguity.',fontsize=9.7,color='#4d5b62')
    fig.text(.07,.023, 'Provisional outer envelope of scenarios and quoted errors. The rectangle also encloses combinations unsupported by an individual scenario.',fontsize=9.7,color='#4d5b62')
    filename = 'ns_b2334_extended_errors.png'
else:
    fig.text(.07,.073,'Web catalogue luminosities (3 Aug 2026 snapshot); independent ages where tabulated, otherwise current spin-down ages. Bounds retain the quoted conventions.',fontsize=9.7,color='#4d5b62')
    fig.text(.07,.048,'† J0205: historical SN 1181 association disputed. B2334: atmosphere temperature/redshift convention under review. Monogem uses the V13 remnant age (~79 kyr).',fontsize=9.7,color='#4d5b62')
    fig.text(.07,.023,'Each source appears once. Temperature components, emitting areas, distances and age assumptions remain to be selected source by source.',fontsize=9.7,color='#4d5b62')
    filename = 'ns_luminosity_vs_age_labelled.png'
if args.cooling_curves:
    filename = 'ns_original_with_cooling.png' if args.original_catalogue else 'ns_velajr_with_cooling.png'
fig.savefig(ROOT/'figures'/filename,dpi=185)
print('Saved plot; all 41 sources labelled.')
