"""
ns_cooling_data.py - observed thermal luminosities, temperatures and ages of isolated neutron stars
==============================================================================================
Generated from the catalogue CSV tables. Intended to be imported and overplotted on
theoretical cooling curves.

References (keys of DATA)
  V13   Vigano et al. 2013, MNRAS 434, 123
  P20   Potekhin et al. 2020, MNRAS 496, 5052 (paper table; some values superseded by WEB)
  WEB   Potekhin catalogue page, last update 03.08.2026 (supersedes P20 for many sources)
  M24   Marino et al. 2024, arXiv:2404.05371 (three cold sources, hot-spot blackbody)
  HO26  Ho, Simkhayeva & Potekhin 2026, arXiv:2601.14388 (Vela Jr, cool surface and total)
  COMPARISON  One luminosity record per source with an independent age, see Cooling_comparison

Units (all quantities are as seen by a distant observer, i.e. redshifted)
  age  : years      (independent of spin-down timing)
  L    : erg/s      (thermal luminosity)
  T    : eV         (kT_inf; model dependent, NOT comparable across references - see notes)
Each entry: name, cls, age, age_lo, age_hi, L, L_lo, L_hi, L_ul, T, T_lo, T_hi, T_ul, note
  *_lo/_hi are the ends of the quoted range (not offsets); None = not available.
  L_ul / T_ul = True means the value is an upper limit.
  cls in {"CCO/TINS","RPP","HB-PSR","XINS","UL","Hot-spot PSR","MAG"}.
Caveats: V13 L is a range and its kT carries no error; V13 and M24 use hot-spot blackbody-type kT,
WEB/P20 often use atmosphere models. Known errors in the source tables are listed in the workbook (Findings).

Quick use
    import ns_cooling_data as ns
    ax.set_xscale("log"); ax.set_yscale("log")
    ns.plot_observations(ax, quantity="L", xunit="yr")            # all references
    ns.plot_observations(ax, "T", refs=("WEB","M24","HO26"), label_names=("PSR J0205+6449",))
    ns.plot_observations(ax, "L", refs=("COMPARISON",))
    a = ns.get("WEB", "L")   # dict of numpy arrays: name, x, xerr (2,N), y, yerr (2,N), ul, cls
"""
import numpy as np

STYLE = {
    "V13":  dict(color="#1f77b4", marker="o", ms=6,  label="Viganò+13"),
    "P20":  dict(color="#2ca02c", marker="s", ms=5,  label="Potekhin+20 paper", alpha=0.5),
    "WEB":  dict(color="#7b2d8e", marker="^", ms=6.5, label="Potekhin web (03.08.2026)"),
    "M24":  dict(color="#d62728", marker="*", ms=14, label="Marino+24"),
    "HO26": dict(color="#c97823", marker="D", ms=7, label="Ho+26 (Vela Jr)"),
    "COMPARISON": dict(color="#1b6668", marker="o", ms=6, label="Cooling comparison"),
}

DATA = {
    "V13": [
        dict(name='RX J0822.0-4300', cls='CCO/TINS', age=3545.26, age_lo=3162.28, age_hi=3981.07, L=3.97971e+33, L_lo=3.16228e+33, L_hi=5.01187e+33, L_ul=False, T=400.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='1E 1207.4-5209', cls='CCO/TINS', age=6662.1, age_lo=2511.89, age_hi=19952.6, L=3.13522e+33, L_lo=1e+33, L_hi=1e+34, L_ul=False, T=190.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='CXOU J185238.6+004020', cls='CCO/TINS', age=6290.48, age_lo=5011.87, age_hi=7943.28, L=3.97971e+33, L_lo=3.16228e+33, L_hi=5.01187e+33, L_ul=False, T=440.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='CXOU J232327.8+584842', cls='CCO/TINS', age=316.228, age_lo=316.228, age_hi=316.228, L=3.16119e+33, L_lo=2.51189e+33, L_hi=3.98107e+33, L_ul=False, T=450.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR J0538+2817', cls='RPP', age=39810.7, age_lo=39810.7, age_hi=39810.7, L=6.30736e+32, L_lo=5.01187e+32, L_hi=7.94328e+32, L_ul=False, T=160.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR B0656+14', cls='RPP', age=79432.8, age_lo=79432.8, age_hi=79432.8, L=5.62292e+32, L_lo=5.01187e+32, L_hi=6.30957e+32, L_ul=False, T=100.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR B0833-45', cls='RPP', age=8751.46, age_lo=5011.87, age_hi=15848.9, L=1.58433e+32, L_lo=1.25893e+32, L_hi=1.99526e+32, L_ul=False, T=120.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR B2334+61', cls='RPP', age=10000.0, age_lo=10000.0, age_hi=10000.0, L=2.46716e+31, L_lo=5.01187e+30, L_hi=1.25893e+32, L_ul=False, T=160.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR J1119-6127', cls='HB-PSR', age=5584.69, age_lo=3981.07, age_hi=7943.28, L=1.77689e+33, L_lo=1.25893e+33, L_hi=2.51189e+33, L_ul=False, T=270.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='RX J0720.4-3125', cls='XINS', age=792780.0, age_lo=630957.0, age_hi=1000000.0, L=1.99455e+32, L_lo=1.58489e+32, L_hi=2.51189e+32, L_ul=False, T=84.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='RX J1308.6+2127', cls='XINS', age=998083.0, age_lo=794328.0, age_hi=1258930.0, L=1.41241e+32, L_lo=1.25893e+32, L_hi=1.58489e+32, L_ul=False, T=94.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='RX J1605.3+3249', cls='XINS', age=501187.0, age_lo=501187.0, age_hi=501187.0, L=8.91168e+30, L_lo=7.94328e+30, L_hi=1e+31, L_ul=False, T=99.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='RX J1856.5-3754', cls='XINS', age=397289.0, age_lo=316228.0, age_hi=501187.0, L=3.97962e+31, L_lo=3.16228e+31, L_hi=5.01187e+31, L_ul=False, T=63.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='1E 2259+586', cls='MAG', age=14037.5, age_lo=10000.0, age_hi=19952.6, L=1.58282e+35, L_lo=1e+35, L_hi=2.51189e+35, L_ul=False, T=400.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='CXOU J171405.7-381031', cls='MAG', age=5011.87, age_lo=5011.87, age_hi=5011.87, L=1.12119e+35, L_lo=7.94328e+34, L_hi=1.58489e+35, L_ul=False, T=540.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='1E 1841-045', cls='MAG', age=701.536, age_lo=501.187, age_hi=1000.0, L=2.23708e+35, L_lo=1.58489e+35, L_hi=3.16228e+35, L_ul=False, T=480.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='SGR 0501+4516', cls='MAG', age=10000.0, age_lo=10000.0, age_hi=10000.0, L=3.95931e+33, L_lo=1.58489e+33, L_hi=1e+34, L_ul=False, T=570.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='SGR 1627-41', cls='MAG', age=5011.87, age_lo=5011.87, age_hi=5011.87, L=3.97578e+34, L_lo=2.51189e+34, L_hi=6.30957e+34, L_ul=False, T=450.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='SGR 0526-66', cls='MAG', age=5011.87, age_lo=5011.87, age_hi=5011.87, L=3.97593e+35, L_lo=2.51189e+35, L_hi=6.30957e+35, L_ul=False, T=480.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='SGR 1900+14', cls='MAG', age=5584.69, age_lo=3981.07, age_hi=7943.28, L=1.58282e+35, L_lo=1e+35, L_hi=2.51189e+35, L_ul=False, T=390.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='SGR 1806-20', cls='MAG', age=791.18, age_lo=630.957, age_hi=1000.0, L=1.99266e+35, L_lo=1.25893e+35, L_hi=3.16228e+35, L_ul=False, T=690.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
    ],
    "P20": [
        dict(name='RX J0822.0-4300', cls='CCO/TINS', age=4386.34, age_lo=3700.0, age_hi=5200.0, L=5e+33, L_lo=3.9e+33, L_hi=6.1e+33, L_ul=False, T=276.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 276/455 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J085201.4-461753', cls='CCO/TINS', age=3367.49, age_lo=2100.0, age_hi=5400.0, L=2e+33, L_lo=1e+33, L_hi=3e+33, L_ul=False, T=90.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 90 eV.', component='whole_surface', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='2XMM J104608.7-594306', cls='CCO/TINS', age=18165.9, age_lo=11000.0, age_hi=30000.0, L=2.19e+32, L_lo=8e+31, L_hi=6e+32, L_ul=False, T=55.0, T_lo=40.0, T_hi=70.0, T_ul=False, note='Temperature transcription: 40-70 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='1E 1207.4-5209', cls='CCO/TINS', age=6480.74, age_lo=2000.0, age_hi=21000.0, L=1.31e+33, L_lo=1.15e+33, L_hi=1.8e+33, L_ul=False, T=170.0, T_lo=90.0, T_hi=250.0, T_ul=False, note='Temperature transcription: 90-250 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J160103.1-513353', cls='CCO/TINS', age=774.597, age_lo=600.0, age_hi=1000.0, L=5.8e+33, L_lo=5.6e+33, L_hi=6e+33, L_ul=False, T=118.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 118 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='1WGA J1713.4-3949', cls='CCO/TINS', age=1608.0, age_lo=1608.0, age_hi=1608.0, L=4.9e+33, L_lo=2e+33, L_hi=1.2e+34, L_ul=False, T=138.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 138 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='XMMU J172054.5-372652', cls='CCO/TINS', age=848.528, age_lo=600.0, age_hi=1200.0, L=2.01e+34, L_lo=1.5e+34, L_hi=2.7e+34, L_ul=False, T=161.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 161 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='XMMU J173203.3-344518', cls='CCO/TINS', age=3464.1, age_lo=2000.0, age_hi=6000.0, L=1.74e+34, L_lo=1.35e+34, L_hi=1.93e+34, L_ul=False, T=153.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 153 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J181852.0-150213', cls='CCO/TINS', age=4024.92, age_lo=2700.0, age_hi=6000.0, L=8.4e+33, L_lo=4.2e+33, L_hi=1.52e+34, L_ul=False, T=130.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 130 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J185238.6+004020', cls='CCO/TINS', age=4996.0, age_lo=3200.0, age_hi=7800.0, L=1.04e+34, L_lo=8.4e+33, L_hi=1.28e+34, L_ul=False, T=133.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 133 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J232327.8+584842', cls='CCO/TINS', age=328.877, age_lo=320.0, age_hi=338.0, L=7.75e+33, L_lo=6.1e+33, L_hi=9.4e+33, L_ul=False, T=154.0, T_lo=123.0, T_hi=185.0, T_ul=False, note='Temperature transcription: 123-185 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR J0205+6449', cls='RPP', age=819.0, age_lo=819.0, age_hi=819.0, L=1.9e+32, L_lo=8e+31, L_hi=3.4e+32, L_ul=False, T=49.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 49 eV. Ritter et al. (2021) associate SN 1181 with Pa 30.', component='whole_surface', reference='P20', age_reference='P20', age_ul=None, age_status='disputed_association'),
        dict(name='PSR J0357+3205', cls='RPP', age=509902.0, age_lo=200000.0, age_hi=1300000.0, L=1.5e+31, L_lo=4e+30, L_hi=4e+31, L_ul=False, T=36.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 36 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR J0538+2817', cls='RPP', age=34641.0, age_lo=20000.0, age_hi=60000.0, L=1.09e+33, L_lo=6.3e+32, L_hi=1.36e+33, L_ul=False, T=91.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 91 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='CXOU J061705.3+222127', cls='RPP', age=30000.0, age_lo=30000.0, age_hi=30000.0, L=2.6e+32, L_lo=2.5e+32, L_hi=2.7e+32, L_ul=False, T=58.4, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 58.4 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR B0833-45', cls='RPP', age=19773.7, age_lo=17000.0, age_hi=23000.0, L=4.24e+32, L_lo=4.12e+32, L_hi=4.36e+32, L_ul=False, T=57.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 57 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR B1951+32', cls='RPP', age=61416.6, age_lo=46000.0, age_hi=82000.0, L=1.8e+32, L_lo=7e+31, L_hi=4.8e+32, L_ul=False, T=130.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 130 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR B2334+61', cls='RPP', age=7700.0, age_lo=7700.0, age_hi=7700.0, L=4.7e+31, L_lo=1.2e+31, L_hi=8.2e+31, L_ul=False, T=38.0, T_lo=None, T_hi=None, T_ul=False, note='Temperature transcription: 38 eV.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR J1119-6127', cls='HB-PSR', age=5460.77, age_lo=4200.0, age_hi=7100.0, L=1.9e+33, L_lo=1.1e+33, L_hi=3.8e+33, L_ul=False, T=145.0, T_lo=80.0, T_hi=210.0, T_ul=False, note='Temperature transcription: 80-210 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='RX J0720.4-3125', cls='XINS', age=836660.0, age_lo=700000.0, age_hi=1000000.0, L=1.9e+32, L_lo=1.1e+32, L_hi=3.2e+32, L_ul=False, T=95.0, T_lo=90.0, T_hi=100.0, T_ul=False, note='Temperature transcription: 90-100 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='RX J1308.6+2127', cls='XINS', age=489898.0, age_lo=300000.0, age_hi=800000.0, L=3.3e+32, L_lo=2.6e+32, L_hi=3.8e+32, L_ul=False, T=70.0, T_lo=50.0, T_hi=90.0, T_ul=False, note='Temperature transcription: 50-90 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='RX J1605.3+3249', cls='XINS', age=440227.0, age_lo=380000.0, age_hi=510000.0, L=1.9e+32, L_lo=7e+30, L_hi=5e+32, L_ul=False, T=77.5, T_lo=35.0, T_hi=120.0, T_ul=False, note='Temperature transcription: 35-120 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='RX J1856.5-3754', cls='XINS', age=412311.0, age_lo=340000.0, age_hi=500000.0, L=6.5e+31, L_lo=5e+31, L_hi=8e+31, L_ul=False, T=49.5, T_lo=36.0, T_hi=63.0, T_ul=False, note='Temperature transcription: 36-63 eV. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR J0007+7303', cls='UL', age=9200.0, age_lo=9200.0, age_hi=9200.0, L=3e+31, L_lo=None, L_hi=None, L_ul=True, T=200.0, T_lo=None, T_hi=None, T_ul=True, note='Temperature transcription: <200 eV.', component='surface_upper_limit', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR B0531+21', cls='UL', age=954.0, age_lo=954.0, age_hi=954.0, L=3e+34, L_lo=None, L_hi=None, L_ul=True, T=180.0, T_lo=None, T_hi=None, T_ul=True, note='Temperature transcription: <180 eV.', component='surface_upper_limit', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
        dict(name='PSR B1727-47', cls='UL', age=48989.8, age_lo=40000.0, age_hi=60000.0, L=3.5e+31, L_lo=None, L_hi=None, L_ul=True, T=33.0, T_lo=None, T_hi=None, T_ul=True, note='Temperature transcription: <33 eV.', component='surface_upper_limit', reference='P20', age_reference='P20', age_ul=None, age_status='reported'),
    ],
    "WEB": [
        dict(name='RX J0822.0-4300', cls='CCO/TINS', age=4450.0, age_lo=3700.0, age_hi=5200.0, L=5e+33, L_lo=3.9e+33, L_hi=6.1e+33, L_ul=False, T=337.639, T_lo=240.0, T_hi=475.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J085201.4-461753', cls='CCO/TINS', age=3498.57, age_lo=2400.0, age_hi=5100.0, L=5e+32, L_lo=1.3e+32, L_hi=6e+32, L_ul=False, T=122.474, T_lo=50.0, T_hi=300.0, T_ul=False, note='Web range combines Ho+26 cool and total luminosity. Temperature is a plotting representative; see Measurements.', component='mixed_component_range', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='2XMM J104608.7-594306', cls='CCO/TINS', age=18165.9, age_lo=11000.0, age_hi=30000.0, L=2.18495e+32, L_lo=7.7e+31, L_hi=6.2e+32, L_ul=False, T=52.915, T_lo=40.0, T_hi=70.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1E 1207.4-5209', cls='CCO/TINS', age=7000.0, age_lo=2333.0, age_hi=21000.0, L=1.31e+33, L_lo=1.15e+33, L_hi=1.8e+33, L_ul=False, T=150.0, T_lo=90.0, T_hi=250.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1RXS J141256.0+792204', cls='CCO/TINS', age=14142.1, age_lo=10000.0, age_hi=20000.0, L=3.67423e+33, L_lo=1.5e+33, L_hi=9e+33, L_ul=False, T=105.404, T_lo=101.0, T_hi=110.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J160103.1-513353', cls='CCO/TINS', age=800.0, age_lo=600.0, age_hi=1000.0, L=4.9e+33, L_lo=4.4e+33, L_hi=6.3e+33, L_ul=False, T=133.0, T_lo=125.0, T_hi=147.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1WGA J1713.4-3949', cls='CCO/TINS', age=1608.5, age_lo=1608.0, age_hi=1609.0, L=2e+33, L_lo=1.7e+33, L_hi=2.3e+33, L_ul=False, T=136.0, T_lo=128.0, T_hi=145.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='XMMU J172054.5-372652', cls='CCO/TINS', age=648.074, age_lo=600.0, age_hi=700.0, L=1.18e+34, L_lo=1.08e+34, L_hi=1.28e+34, L_ul=False, T=162.0, T_lo=156.0, T_hi=168.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=700.0, age_status='reported'),
        dict(name='XMMU J173203.3-344518', cls='CCO/TINS', age=3464.1, age_lo=2000.0, age_hi=6000.0, L=1.08e+34, L_lo=7.8e+33, L_hi=1.45e+34, L_ul=False, T=156.0, T_lo=150.0, T_hi=162.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J181852.0-150213', cls='CCO/TINS', age=3400.0, age_lo=2700.0, age_hi=6000.0, L=8.4e+33, L_lo=4.2e+33, L_hi=1.52e+34, L_ul=False, T=130.0, T_lo=110.0, T_hi=150.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J185238.6+004020', cls='CCO/TINS', age=6000.0, age_lo=3200.0, age_hi=7800.0, L=1.04e+34, L_lo=8.4e+33, L_hi=1.28e+34, L_ul=False, T=133.0, T_lo=132.0, T_hi=134.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J232327.8+584842', cls='CCO/TINS', age=326.2, age_lo=319.5, age_hi=338.7, L=7.21665e+33, L_lo=5.6e+33, L_hi=9.3e+33, L_ul=False, T=123.935, T_lo=120.0, T_hi=128.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0205+6449', cls='RPP', age=819.5, age_lo=819.4, age_hi=819.6, L=1.9e+32, L_lo=8e+31, L_hi=3.4e+32, L_ul=False, T=49.0, T_lo=43.0, T_hi=54.0, T_ul=False, note='Ritter et al. (2021) associate SN 1181 with Pa 30.', component='whole_surface', reference='WEB', age_reference='WEB', age_ul=None, age_status='disputed_association'),
        dict(name='PSR J0357+3205', cls='RPP', age=509902.0, age_lo=200000.0, age_hi=1300000.0, L=1.5e+31, L_lo=4e+30, L_hi=4e+31, L_ul=False, T=36.0, T_lo=30.0, T_hi=45.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0538+2817', cls='RPP', age=30000.0, age_lo=20000.0, age_hi=60000.0, L=1.09e+33, L_lo=6.3e+32, L_hi=1.36e+33, L_ul=False, T=91.0, T_lo=86.0, T_hi=96.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J061705.3+222127', cls='RPP', age=30000.0, age_lo=25000.0, age_hi=35000.0, L=2.6e+32, L_lo=2.5e+32, L_hi=2.7e+32, L_ul=False, T=58.4, T_lo=58.0, T_hi=59.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0833-45', cls='RPP', age=21424.3, age_lo=17000.0, age_hi=27000.0, L=4.24e+32, L_lo=4.12e+32, L_hi=4.36e+32, L_ul=False, T=57.0, T_lo=56.0, T_hi=60.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B1951+32', cls='RPP', age=64000.0, age_lo=46000.0, age_hi=82000.0, L=1.8e+32, L_lo=7e+31, L_hi=4.8e+32, L_ul=False, T=130.0, T_lo=110.0, T_hi=150.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B2334+61', cls='RPP', age=7700.0, age_lo=7600.0, age_hi=7800.0, L=4.7e+31, L_lo=1.2e+31, L_hi=8.2e+31, L_ul=False, T=46.0, T_lo=30.0, T_hi=52.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J1119-6127', cls='HB-PSR', age=5460.77, age_lo=4200.0, age_hi=7100.0, L=1.9e+33, L_lo=1.1e+33, L_hi=3.8e+33, L_ul=False, T=129.615, T_lo=80.0, T_hi=210.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J0720.4-3125', cls='XINS', age=850000.0, age_lo=700000.0, age_hi=1000000.0, L=1.9e+32, L_lo=1.1e+32, L_hi=3.2e+32, L_ul=False, T=92.4, T_lo=91.4, T_hi=93.3, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1308.6+2127', cls='XINS', age=550000.0, age_lo=300000.0, age_hi=800000.0, L=3.3e+32, L_lo=2.6e+32, L_hi=3.8e+32, L_ul=False, T=67.082, T_lo=50.0, T_hi=90.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1605.3+3249', cls='XINS', age=440000.0, age_lo=380000.0, age_hi=510000.0, L=5.91608e+31, L_lo=7e+30, L_hi=5e+32, L_ul=False, T=64.8074, T_lo=35.0, T_hi=120.0, T_ul=False, note='Published distance bounds are inconsistent. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1856.5-3754', cls='XINS', age=420000.0, age_lo=340000.0, age_hi=500000.0, L=6.32456e+31, L_lo=5e+31, L_hi=8e+31, L_ul=False, T=47.6235, T_lo=36.0, T_hi=63.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0007+7303', cls='UL', age=9200.0, age_lo=9100.0, age_hi=9300.0, L=3e+31, L_lo=None, L_hi=None, L_ul=True, T=200.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0531+21', cls='UL', age=953.6, age_lo=953.5, age_hi=953.7, L=3e+34, L_lo=None, L_hi=None, L_ul=True, T=180.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B1727-47', cls='UL', age=50000.0, age_lo=40000.0, age_hi=60000.0, L=3.5e+31, L_lo=None, L_hi=None, L_ul=True, T=33.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0950+08', cls='RPP', age=1900000.0, age_lo=600000.0, age_hi=7600000.0, L=8e+28, L_lo=2e+28, L_hi=2.3e+29, L_ul=False, T=7.0, T_lo=5.0, T_hi=11.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='SN 1987A remnant', cls='UL', age=28.4637, age_lo=28.342, age_hi=28.586, L=3.44e+35, L_lo=None, L_hi=None, L_ul=True, T=None, T_lo=None, T_hi=None, T_ul=False, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
    ],
    "M24": [
        dict(name='CXOU J085201.4-461753', cls='CCO/TINS', age=3535.53, age_lo=2500.0, age_hi=5000.0, L=2e+32, L_lo=1.4e+32, L_hi=2.6e+32, L_ul=False, T=397.0, T_lo=388.0, T_hi=406.0, T_ul=False, note='Paper distance range 0.5–1.0 kpc. About 0.8 kpc is inferred from the quoted flux and luminosity.', component='hot_spot', reference='M24', age_reference='M24', age_ul=None, age_status='reported'),
        dict(name='PSR J0205+6449', cls='RPP', age=841.0, age_lo=841.0, age_hi=841.0, L=1.44e+32, L_lo=9.4e+31, L_hi=2.04e+32, L_ul=False, T=200.0, T_lo=160.0, T_hi=280.0, T_ul=False, note='The paper adopts a 10% age uncertainty for its analysis. Ritter et al. (2021) associate SN 1181 with Pa 30.', component='hot_spot', reference='M24', age_reference='M24', age_ul=None, age_status='disputed_association'),
        dict(name='PSR B2334+61', cls='RPP', age=7700.0, age_lo=7700.0, age_hi=7700.0, L=7.8e+31, L_lo=6.8e+31, L_hi=1.08e+32, L_ul=False, T=160.0, T_lo=150.0, T_hi=170.0, T_ul=False, note='The paper adopts a 10% age uncertainty for its analysis.', component='hot_spot', reference='M24', age_reference='M24', age_ul=None, age_status='reported'),
    ],
    "HO26": [
        dict(name='CXOU J085201.4-461753 (cool surface)', cls='CCO/TINS', age=3498.57, age_lo=2400.0, age_hi=5100.0, L=2.28035e+32, L_lo=1.3e+32, L_hi=4e+32, L_ul=False, T=53.7275, T_lo=46.0521, T_hi=61.4029, T_ul=False, note='', component='cool_surface', reference='HO26', age_reference='HO26', age_ul=None, age_status='reported'),
        dict(name='CXOU J085201.4-461753 (total)', cls='CCO/TINS', age=3498.57, age_lo=2400.0, age_hi=5100.0, L=5e+32, L_lo=4e+32, L_hi=6e+32, L_ul=False, T=None, T_lo=None, T_hi=None, T_ul=False, note='Total includes the hot spot, which dominates the observed flux.', component='total_thermal', reference='HO26', age_reference='HO26', age_ul=None, age_status='reported'),
    ],
    "COMPARISON": [
        dict(name='RX J0822.0-4300', cls='CCO/TINS', age=4450.0, age_lo=3700.0, age_hi=5200.0, L=5e+33, L_lo=3.9e+33, L_hi=6.1e+33, L_ul=False, T=337.639, T_lo=240.0, T_hi=475.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J085201.4-461753', cls='CCO/TINS', age=2297.83, age_lo=1600.0, age_hi=3300.0, L=2.28035e+32, L_lo=1.3e+32, L_hi=4e+32, L_ul=False, T=53.7275, T_lo=46.0521, T_hi=61.4029, T_ul=False, note='Ho et al. luminosity paired with the Suherli et al. age estimate.', component='cool_surface', reference='HO26', age_reference='SU26', age_ul=None, age_status='reported'),
        dict(name='2XMM J104608.7-594306', cls='CCO/TINS', age=18165.9, age_lo=11000.0, age_hi=30000.0, L=2.18495e+32, L_lo=7.7e+31, L_hi=6.2e+32, L_ul=False, T=52.915, T_lo=40.0, T_hi=70.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1E 1207.4-5209', cls='CCO/TINS', age=7000.0, age_lo=2333.0, age_hi=21000.0, L=1.31e+33, L_lo=1.15e+33, L_hi=1.8e+33, L_ul=False, T=150.0, T_lo=90.0, T_hi=250.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1RXS J141256.0+792204', cls='CCO/TINS', age=14142.1, age_lo=10000.0, age_hi=20000.0, L=3.67423e+33, L_lo=1.5e+33, L_hi=9e+33, L_ul=False, T=105.404, T_lo=101.0, T_hi=110.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J160103.1-513353', cls='CCO/TINS', age=800.0, age_lo=600.0, age_hi=1000.0, L=4.9e+33, L_lo=4.4e+33, L_hi=6.3e+33, L_ul=False, T=133.0, T_lo=125.0, T_hi=147.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='1WGA J1713.4-3949', cls='CCO/TINS', age=1608.5, age_lo=1608.0, age_hi=1609.0, L=2e+33, L_lo=1.7e+33, L_hi=2.3e+33, L_ul=False, T=136.0, T_lo=128.0, T_hi=145.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='XMMU J172054.5-372652', cls='CCO/TINS', age=648.074, age_lo=600.0, age_hi=700.0, L=1.18e+34, L_lo=1.08e+34, L_hi=1.28e+34, L_ul=False, T=162.0, T_lo=156.0, T_hi=168.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=700.0, age_status='reported'),
        dict(name='XMMU J173203.3-344518', cls='CCO/TINS', age=3464.1, age_lo=2000.0, age_hi=6000.0, L=1.08e+34, L_lo=7.8e+33, L_hi=1.45e+34, L_ul=False, T=156.0, T_lo=150.0, T_hi=162.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J181852.0-150213', cls='CCO/TINS', age=3400.0, age_lo=2700.0, age_hi=6000.0, L=8.4e+33, L_lo=4.2e+33, L_hi=1.52e+34, L_ul=False, T=130.0, T_lo=110.0, T_hi=150.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J185238.6+004020', cls='CCO/TINS', age=6000.0, age_lo=3200.0, age_hi=7800.0, L=1.04e+34, L_lo=8.4e+33, L_hi=1.28e+34, L_ul=False, T=133.0, T_lo=132.0, T_hi=134.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J232327.8+584842', cls='CCO/TINS', age=326.2, age_lo=319.5, age_hi=338.7, L=7.21665e+33, L_lo=5.6e+33, L_hi=9.3e+33, L_ul=False, T=123.935, T_lo=120.0, T_hi=128.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0357+3205', cls='RPP', age=509902.0, age_lo=200000.0, age_hi=1300000.0, L=1.5e+31, L_lo=4e+30, L_hi=4e+31, L_ul=False, T=36.0, T_lo=30.0, T_hi=45.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0538+2817', cls='RPP', age=30000.0, age_lo=20000.0, age_hi=60000.0, L=1.09e+33, L_lo=6.3e+32, L_hi=1.36e+33, L_ul=False, T=91.0, T_lo=86.0, T_hi=96.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='CXOU J061705.3+222127', cls='RPP', age=30000.0, age_lo=25000.0, age_hi=35000.0, L=2.6e+32, L_lo=2.5e+32, L_hi=2.7e+32, L_ul=False, T=58.4, T_lo=58.0, T_hi=59.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0656+14', cls='RPP', age=79432.8, age_lo=79432.8, age_hi=79432.8, L=5.62292e+32, L_lo=5.01187e+32, L_hi=6.30957e+32, L_ul=False, T=100.0, T_lo=None, T_hi=None, T_ul=False, note='', component='reported_thermal', reference='V13', age_reference='V13', age_ul=None, age_status='reported'),
        dict(name='PSR B0833-45', cls='RPP', age=21424.3, age_lo=17000.0, age_hi=27000.0, L=4.24e+32, L_lo=4.12e+32, L_hi=4.36e+32, L_ul=False, T=57.0, T_lo=56.0, T_hi=60.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B1951+32', cls='RPP', age=64000.0, age_lo=46000.0, age_hi=82000.0, L=1.8e+32, L_lo=7e+31, L_hi=4.8e+32, L_ul=False, T=130.0, T_lo=110.0, T_hi=150.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B2334+61', cls='RPP', age=7700.0, age_lo=7600.0, age_hi=7800.0, L=4.7e+31, L_lo=1.2e+31, L_hi=8.2e+31, L_ul=False, T=46.0, T_lo=30.0, T_hi=52.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J1119-6127', cls='HB-PSR', age=5460.77, age_lo=4200.0, age_hi=7100.0, L=1.9e+33, L_lo=1.1e+33, L_hi=3.8e+33, L_ul=False, T=129.615, T_lo=80.0, T_hi=210.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J0720.4-3125', cls='XINS', age=850000.0, age_lo=700000.0, age_hi=1000000.0, L=1.9e+32, L_lo=1.1e+32, L_hi=3.2e+32, L_ul=False, T=92.4, T_lo=91.4, T_hi=93.3, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1308.6+2127', cls='XINS', age=550000.0, age_lo=300000.0, age_hi=800000.0, L=3.3e+32, L_lo=2.6e+32, L_hi=3.8e+32, L_ul=False, T=67.082, T_lo=50.0, T_hi=90.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1605.3+3249', cls='XINS', age=440000.0, age_lo=380000.0, age_hi=510000.0, L=5.91608e+31, L_lo=7e+30, L_hi=5e+32, L_ul=False, T=64.8074, T_lo=35.0, T_hi=120.0, T_ul=False, note='Published distance bounds are inconsistent. Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='RX J1856.5-3754', cls='XINS', age=420000.0, age_lo=340000.0, age_hi=500000.0, L=6.32456e+31, L_lo=5e+31, L_hi=8e+31, L_ul=False, T=47.6235, T_lo=36.0, T_hi=63.0, T_ul=False, note='Temperature is a plotting representative; see Measurements.', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR J0007+7303', cls='UL', age=9200.0, age_lo=9100.0, age_hi=9300.0, L=3e+31, L_lo=None, L_hi=None, L_ul=True, T=200.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0531+21', cls='UL', age=953.6, age_lo=953.5, age_hi=953.7, L=3e+34, L_lo=None, L_hi=None, L_ul=True, T=180.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B1727-47', cls='UL', age=50000.0, age_lo=40000.0, age_hi=60000.0, L=3.5e+31, L_lo=None, L_hi=None, L_ul=True, T=33.0, T_lo=None, T_hi=None, T_ul=True, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='PSR B0950+08', cls='RPP', age=1900000.0, age_lo=600000.0, age_hi=7600000.0, L=8e+28, L_lo=2e+28, L_hi=2.3e+29, L_ul=False, T=7.0, T_lo=5.0, T_hi=11.0, T_ul=False, note='', component='reported_thermal', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
        dict(name='SN 1987A remnant', cls='UL', age=28.4637, age_lo=28.342, age_hi=28.586, L=3.44e+35, L_lo=None, L_hi=None, L_ul=True, T=None, T_lo=None, T_hi=None, T_ul=False, note='', component='surface_upper_limit', reference='WEB', age_reference='WEB', age_ul=None, age_status='reported'),
    ],
}


def get(ref, quantity="L", include_magnetars=True, classes=None):
    """Return numpy arrays for one reference and quantity ('L' or 'T').
    x in years; xerr = [[x-age_lo],[age_hi-x]]; y and yerr likewise; ul = upper-limit flags."""
    q = quantity.upper()
    if q not in ("L", "T"):
        raise ValueError("quantity must be L or T")
    if ref == "COMPARISON" and q == "T":
        raise ValueError("COMPARISON is a luminosity sample; use a literature reference for temperature")
    names, x, xl, xh, y, yl, yh, ul, xul, cl = [], [], [], [], [], [], [], [], [], []
    for e in DATA[ref]:
        v = e[q]
        if v is None: continue
        if (not include_magnetars) and e["cls"] == "MAG": continue
        if classes is not None and e["cls"] not in classes: continue
        lo, hi = e[q + "_lo"], e[q + "_hi"]
        names.append(e["name"]); cl.append(e["cls"])
        xul.append(e["age_ul"] is not None)
        if xul[-1]:
            x.append(e["age_ul"]); xl.append(0.25 * e["age_ul"]); xh.append(0)
        else:
            x.append(e["age"]); xl.append(max(e["age"] - e["age_lo"], 0)); xh.append(max(e["age_hi"] - e["age"], 0))
        y.append(v)
        yl.append(0 if lo is None else max(v - lo, 0)); yh.append(0 if hi is None else max(hi - v, 0))
        ul.append(bool(e[q + "_ul"]))
    return dict(name=np.array(names), cls=np.array(cl), x=np.array(x, float),
                xerr=np.array([xl, xh], float), y=np.array(y, float), yerr=np.array([yl, yh], float),
                ul=np.array(ul, bool), xul=np.array(xul, bool))


def plot_observations(ax, quantity="L", refs=("V13", "P20", "WEB", "M24", "HO26"), xunit="yr",
                      include_magnetars=False, label_names=(), legend=True, zorder=5, **kw):
    """Overplot observations on an existing axes (e.g. next to theoretical cooling curves).
    xunit: 'yr' or 'kyr'. Extra keyword arguments (e.g. elinewidth, capsize) go to ax.errorbar.
    Magnetars (V13 only) are off by default. Returns the list of plotted references."""
    scale = {"yr": 1.0, "kyr": 1e-3}[xunit]
    done = []
    for ref in refs:
        d = get(ref, quantity, include_magnetars)
        if len(d["x"]) == 0: continue
        st = dict(STYLE[ref]); lab = st.pop("label"); ms = st.pop("ms"); mk = st.pop("marker"); col = st.pop("color")
        alpha = st.pop("alpha", 0.9)
        first = True
        for i in range(len(d["x"])):
            ul = d["ul"][i]
            ye = np.array([[0.0], [0.0]]) if ul else d["yerr"][:, i:i+1]
            style = {"mfc": "white"} if (ref == "HO26" and d["name"][i].endswith(" (total)")) else {}
            if ref == "V13" and d["cls"][i] == "MAG":
                style = {"mfc": "white", "fmt": "D"}
            else:
                style["fmt"] = mk
            ax.errorbar(d["x"][i]*scale, d["y"][i], xerr=d["xerr"][:, i:i+1]*scale, xuplims=bool(d["xul"][i]),
                        yerr=(np.array([[d["y"][i]*0.45], [0.0]]) if ul else ye), uplims=bool(ul),
                        ms=ms, color=col, ecolor=col,
                        **(dict(elinewidth=1.0, capsize=2, alpha=alpha, zorder=zorder,
                                label=lab if first else None) | style | kw))
            first = False
            if d["name"][i] in label_names:
                ax.annotate(d["name"][i], (d["x"][i]*scale, d["y"][i]), xytext=(6, 6),
                            textcoords="offset points", fontsize=8, color=col)
        done.append(ref)
    ax.set_xlabel(f"Age ({xunit})")
    ax.set_ylabel("Thermal luminosity (erg/s)" if quantity.upper() == "L" else "Temperature at infinity (eV)")
    if legend: ax.legend(fontsize=8)
    return done


if __name__ == "__main__":      # demo: observations with a dummy power-law curve
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    t = np.logspace(2, 6, 100)
    for ax, q, curve in ((axs[0], "L", 3e34*(t/1e3)**-0.35), (axs[1], "T", 160*(t/1e3)**-0.1)):
        ax.plot(t, curve, "k-", label="theory (dummy)")
        ax.set_xscale("log"); ax.set_yscale("log")
        plot_observations(ax, q, xunit="yr", label_names=("PSR J0205+6449", "PSR B2334+61"))
        ax.set_xlim(2e2, 3e6)
    fig.tight_layout(); fig.savefig("ns_cooling_data_demo.png", dpi=120)
    print({k: len(v) for k, v in DATA.items()})
