# Reference cooling curves

This observational project includes the output arrays in data/cooling_reference_curves.csv and brief model metadata only. The cooling solver, input files, run scripts and diagnostic outputs are maintained separately.

Tracks: BSk26, 1.4 and 1.8 solar masses; Gudmundsson envelope; B=0; supplied pairing models 7/12/8; Yakovlev et al. 2001 modified Urca and Bottaro-Caputo-Fiorillo nucleon bremsstrahlung. The high-mass run changes only mass; the reference uses the supplied default central pressure. Model metadata and the input archive hash are in run_metadata.json.

Largest per-window energy-closure residuals from t >= 1 year: 0.349% and 0.271%. This is an energy check, not a spatial convergence study. The supplied EOS loader omits a slightly non-monotonic pressure row. Tracks stop at their first accepted L_infinity < 1e31 erg/s, with no extrapolation. Both panels display true-age theoretical tracks; characteristic age is only an observational proxy. These are reference curves, not fits to the observations.
