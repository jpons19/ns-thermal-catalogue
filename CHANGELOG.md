# Changelog

## Review revision · 20 November 2026

The generated plot sample and HTML pages are regenerated in this revision; the figures are not. They take effect at the next `python scripts/rebuild.py`.

- PSR J0538+2817 / S147: luminosity outer envelope adopted as (5.0–13.6)×10³² erg/s; display marker at ~8.2×10³² erg/s (geometric midpoint) and 30 kyr kinematic midpoint. Low end: V13 BB+PL at 1.3 kpc. High end: P20 NSA family at 1.47 kpc. Both distances within Kochanek et al. (2024) 90% interval; no d²-rescaling applied (Option A). Exporter updated to set luminosity fields for source 16; McGowan2003 and Kochanek2024 added to references.bib.
- J0205+6449: luminosity lower edge raised from 2×10³¹ (small-area fit) to 0.8×10³² erg/s. Age 0.8–7 kyr and the ~819 yr display marker kept. Conditional hidden-surface limit not plotted. Kothes (2013) check deferred.
- J0007+7303: 3×10³¹ erg/s ceiling documented as the NSA local-temperature conversion of Caraveo et al. (2010). Conservative ceiling of about 10³² erg/s added as a dotted extension; the plotting code draws it for any upper limit with `L_inf_erg_s_upper_limit_conservative`. Reanalysis recommended.
- B2334+61: single original box kept. Two-scenario analysis recorded in the audit only.
- Vela: marker description corrected to 21.4 kyr (geometric midpoint of P20's 17–27 kyr). No data change.
- Vela Jr: distance 1.41 (1.27–1.55) kpc adopted (Suherli2026), complementing the 19 November luminosity and marker decision.
- Audit entries for J0205, J0007, B2334 and Vela Jr report their position relative to the minimal-cooling band of the 2026-11-20 cooling sweeps. That comparison is for information only and is not used to select ages.

## 0.1.0-review · 18 November 2026

- Consolidated the current source catalogue, literature audit, raw measurements and reproducible plotting code.
- Recorded B2334's adopted Marino distance and provisional luminosity envelope, with unresolved remnant age at that distance.
- Adopted Vela age 11–40 kyr and luminosity (2.0–4.4) × 10³² erg/s; excluded V13 from its selected envelope.
- Added machine-readable decisions and generated 40-source display sample.
- Added offline rebuild/integrity commands and static GitHub Pages catalogue.
- Preserved the complete original project as historical material in `legacy/`.

- Monogem: adopt 70–120 kyr and (2.5–9.0) × 10³² erg/s, deliberately retaining the unresolved P20 luminosity. Added primary spectral checks and nine-entry working bibliography.

- J0205+6449: provisionally retain 0.8–7 kyr with Pa 30/SN 1181, expansion-history and corrected timing caveats; luminosity still open.

- 2026-11-18: Adopt J0205 luminosity (0.2–3.4)×10³² erg/s with provisional age 0.8–7 kyr; add four-source box plot and two actual BSk26 cooling runs, arrays, logs and reproduction script.

- 2026-11-18: Include Cas A as accepted CCO exception, with 320–339 yr and (5.6–9.3)×10³³ erg/s error bars only; add four primary references. Cooling solver materials excluded from GitHub release.

- 2026-11-18: Include Vela Jr provisionally; document Allen, Suherli and Ho age/distance/component scenarios with final selections pending.

- 2026-11-18: Record Vela Jr age 1.6–5.1 kyr; open B1727/J0007 upper-limit audits, tracing spectral provenance and J0007 whole-surface temperatures and model ages.

- 2026-11-18: Adopt B1727−47 age 40–80 kyr and J0007+7303 age 9–13 kyr; update horizontal error bars and retain luminosity upper limits.

- 2026-11-18: Open IC 443 age review; record young remnant, 3D hydrodynamic and proposed runaway-companion scenarios and cooling-age circularity caveat. Plot unchanged pending selection.

- 2026-11-18: Adopt IC 443 age 3–20 kyr; exclude old Chevalier and cooling-age arguments from selection. Document NSA/BB luminosity comparison and conditional distance sensitivity; final luminosity selection pending.

- 2026-11-18: Adopt IC 443 distance 1.6–1.7 kpc; record modern distance methods and conditional luminosity sensitivity. Luminosity selection pending.

- 2026-11-18: Adopt IC 443 luminosity (1.0–3.5)×10³² erg/s; update vertical error bars and documentation alongside the agreed 3–20 kyr age range.

- 2026-11-18: Simplify Vela Jr plot label while retaining provisional status in documentation; display Monogem accepted ranges as error bars without shading.

- 18 November 2026: B1951+32 age 45–85 kyr accepted; reviewed distance and separate hot-spot/whole-surface luminosity constraints, decisions pending. Added primary bibliography and synchronized data, plot and audit.

- 18 November 2026: Adopt B1951+32 distance 1–2 kpc and published whole-surface L∞ < 3.8e32 erg/s; replace current hot-spot point by an upper-limit arrow with 45–85 kyr age extent. Fixed-radius/reference-distance caveats retained.

- 19 November 2026: Replace single HTML source assessment by age/distance/flux/temperature columns with explicit reasons, quantity-aware filters and an offline reproducible assessment map. Numerical catalogue decisions unchanged.

- 19 November 2026: Remove SN 1987A remnant and eRASSU J131716.9−402647 from active data, HTML and all regenerated figures; 75 catalogue entries and 41 plotted sources remain. Preserve exclusion provenance separately.

- 19 November 2026: Remove 1E 0102.2−7219 from active catalogue (74 entries remain; plots unchanged at 41). Change 3C 58 pulsar age assessment from Disputed to Open issue; keep 0.8–7 kyr and caveats.

- 19 November 2026: Split 17 magnetars into docs/magnetar.html (57 main entries); display numerical adopted/catalogue values in coloured cells and add equatorial dipole-field column with provenance. Add conditional Fbol conversion alongside L∞ and show B1951 whole-surface temperature limit. Cooling plots unchanged.
