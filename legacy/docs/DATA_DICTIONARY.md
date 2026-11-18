# Data dictionary

## Normalized catalogue

The workbook and CSVs share the same rows. `source_id` is the stable identifier
from Master. `measurement_id` adds the reference and, when applicable, the
component. Multiple records can use the same spectrum or underlying fit.
For example, the web Vela Jr entry summarizes Ho et al. (2026).

- `Sources` includes all legacy identities. `historical_disputed` flags 1E 0102.2−7219,
  which was removed from the Potekhin web catalogue following
  [Long et al. (2020)](https://doi.org/10.3847/1538-4357/abc075).
  `remnant_upper_limit` identifies the SN 1987A constraint on a putative neutron star.
- `Measurements` contains the original literature alternatives, including sources with
  unavailable independent ages. `age_reference` and `reference` identify the age and
  thermal sources. `age_status` identifies unavailable ages and the disputed
  SN 1181 association for 3C 58. `tau_c_yr` stores characteristic age where available.
- The `age_yr`, `L_inf_erg_s`, `kT_inf_eV` and `distance_kpc` groups use years,
  erg/s, eV and kpc. Suffixes `_lo` and `_hi` are endpoints. An equal age pair is a
  point value. `age_upper_limit_yr` records an explicit ceiling when documented
  separately from the tabulated bracket, currently the web entry for XMMU J172054.5−372652.
  The independent-age plot uses a left-pointing arrow for this ceiling.
- Ranges without a quoted central age or luminosity use a geometric midpoint
  for plotting. Missing values stay blank. Temperature ranges may span multiple
  components. The CSV preserves the endpoints and leaves their representative
  temperature blank when the source provides none. The legacy Python plot
  can use a plotting midpoint or the cooler P20 component.
- For a one-sided limit, the main value is the bound and its upper-limit flag
  is true. `surface_upper_limit` indicates a reported observational constraint.
  `cool_surface_upper_limit` indicates a conditional extra blackbody component.
  A hot-spot detection is stored as a detection. `reported_thermal` means the
  emitting area or component requires consultation of the cited fit.
- `Cooling_comparison` selects one record per source with an independent age and
  luminosity, in the order Ho cool component, web, P20, V13. The selection
  excludes magnetars, the disputed 1E 0102 candidate, explicitly hot-spot-only
  measurements, mixed-component ranges, conditional extra-component limits, and the
  disputed historical age for 3C 58.
  It includes confirmed upper limits and the remnant constraint. Vela Jr uses the
  Ho luminosity with the Suherli age range. Other rows preserve the age–luminosity
  pairing from the selected compilation. Source class and component flag are
  available for tighter cuts.
- Some P20 values are legacy transcriptions with estimated midpoints or bounds.
  The web distance tuple for RX J1605.3+3249 is inconsistent as printed and flagged.
  `Findings` and the notes document further issues. Secondary references and all
  per-object spectral models have yet to be independently audited.


## `data/NS_thermal_crossmatch.xlsx`

Audit sheets: `README`, `Findings` (discrepancies, live evidence cells), `Master`, `Marino3_detail`, `VelaJr`, `Web_updates`, `Settings`.
Colour code: **blue** = value transcribed from a paper, **black** = formula, **green** = link to another sheet.

### `Master` (one row per source; 77 rows) — column groups

| Group | Columns | Content |
|---|---|---|
| Identity | A–G | ID, source name, association, harmonised class, flags "in V13 / P20 / M24" |
| Vigano+13 (V13) | H–R | P (s), log Pdot, log Bp (polar, G), log tau_c, log tau_k lo/hi (yr), d (kpc), log L lo/hi (erg/s), kT_bb (eV), best-fit model |
| Potekhin+20 paper (P20) | S–AD | P, Bdip (1e12 G, equatorial), d (+lo/hi), tau_c (kyr), t* lo/hi (kyr), L (1e32 erg/s, +lo/hi), kT_inf (eV text) |
| Marino+24 (M24) | AE–AL | d, age lo/hi (kyr), L_obs (1e32, +lo/hi, 90 % errors), kT_bb (eV), notes |
| Computed checks | AM–BF | V13 ages/luminosities in common units, Pdot from B and from tau_c, Pdot/Bp/period/distance/age/luminosity-overlap comparisons, **FLAGS** text |
| Potekhin web (03.08.2026) | BG–BX | in-web flag, d lo/mid/hi, P, Pdot, Bdip (1e12 G), tau_c (kyr), t* lo/mid/hi (kyr), L lo/mid/hi (1e32), kT lo/mid/hi (eV), last update |
| Computed checks (web) | BY–CI | Pdot consistency, V13/M24/P20 vs web comparisons, **FLAGS (web)** text |

Tolerances and constants are in `Settings` (change there; everything recalculates).

### Conventions (see also `notes/ns_thermal_data_notes.pdf`)
* Bp (V13, M24) = 6.4e19 sqrt(P Pdot) G (polar); Bdip (P20, web) = 3.2e19 sqrt(P Pdot) G (equatorial) => Bp = 2 Bdip.
* L and kT are as seen at infinity. Web luminosities are given in 1e33 erg/s on the page and converted to 1e32 here.
* Where a paper gives a range, central values are midpoints (P20) or geometric means (module); some bounds for "~" entries are the author's assumption.
* Confidence levels are **not** harmonised: V13 range (stat + distance), P20/web ~1 sigma (upper limits 3 sigma), M24 90 %, Ho+26 1 sigma.

## `data/ns_cooling_data.py`

`DATA[ref]` is a list of dicts for ref in `V13, P20, WEB, M24, HO26, COMPARISON`.
Fields: `name, cls, age, age_lo, age_hi` (yr), `L, L_lo, L_hi` (erg/s), `L_ul` (upper-limit flag), `T, T_lo, T_hi` (eV), `T_ul`, `note`.
`*_lo/_hi` are range ends, not offsets; `None` = not available. Only sources with an age independent of timing are included.
Helpers: `get(ref, "L"|"T")` returns NumPy arrays with upper-limit flags `ul` (vertical) and `xul` (horizontal); `plot_observations(ax, quantity, refs, xunit, ...)` overplots on an existing axes; `STYLE` holds colours/markers.

## `data/web_table.json`, `data/web_updates.json`
Parsed from `data/raw/Cooling_NS.html` by `src/parse_web.py`. Raw page units: kpc, s, s/s, G, yr, 1e33 erg/s, eV.

## `data/derived/calc.json`
Numbers behind the tables of the notes (estimates, not measurements).
