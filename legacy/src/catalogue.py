"""Normalize the Master sheet into source, measurement and comparison tables."""
from collections import Counter
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MARINO_INPUT = json.loads((RAW / "marino2024_sources.json").read_text())
ADDITIONAL = json.loads((RAW / "additional_measurements.json").read_text())
MARINO = ADDITIONAL["marino2024"]
VELA_JR = ADDITIONAL["vela_jr_2026"]

REFERENCES = {
    "V13": ("Viganò et al. 2013, MNRAS 434, 123", "https://doi.org/10.1093/mnras/stt1008"),
    "P20": ("Potekhin et al. 2020, MNRAS 496, 5052", "https://doi.org/10.1093/mnras/staa1871"),
    "WEB": ("Potekhin catalogue, 2026-08-03 snapshot", "https://www.ioffe.ru/astro/NSG/thermal/cooldat.html"),
    "M24": ("Marino et al. 2024, Nature Astronomy 8, 1020", "https://doi.org/10.1038/s41550-024-02291-y"),
    "HO26": ("Ho, Simkhayeva & Potekhin 2026, MNRAS 546, stag126", "https://doi.org/10.1093/mnras/stag126"),
    "R21": ("Ritter et al. 2021, ApJL 918, L33", "https://doi.org/10.3847/2041-8213/ac2253"),
    "B06": ("Bietenholz 2006, ApJ 645, 1180", "https://doi.org/10.1086/504584"),
    "SU26": ("Suherli et al. 2026, ApJL 997, L36", "https://doi.org/10.3847/2041-8213/ae27c4"),
}

THREE_C_58 = 14
RETIRED_SOURCE = 1  # 1E 0102.2-7219, retained from P20 for provenance.
M24_OBS = {MARINO[obj["name"]]["id"]: obj for obj in MARINO_INPUT["objects"]}
if len(M24_OBS) != len(MARINO_INPUT["objects"]) or set(M24_OBS) != {
    item["id"] for item in MARINO.values()
}:
    raise ValueError("Marino input and cross-identifications disagree")


def triplet(low=None, mid=None, high=None, *, scale=1, logarithmic=False):
    """Bounds in original units; synthesize a plotting midpoint when both exist."""
    if mid is None and low is not None and high is not None:
        mid = math.sqrt(low * high)
    return tuple(
        None if value is None else (10**value if logarithmic else value) * scale
        for value in (low, mid, high)
    )


def web_value(low, mid, high, *, scale=1):
    if low is None and mid is None and high is not None:
        return triplet(mid=high, scale=scale), True
    return triplet(low, mid, high, scale=scale), False


def paper_temperature(raw):
    if raw is None:
        return triplet(), False
    if raw.startswith("<"):
        return triplet(mid=float(raw[1:])), True
    if "/" in raw:
        low, high = map(float, raw.split("/"))
        return (low, None, high), False
    if "-" in raw:
        low, high = map(float, raw.split("-"))
        return (low, None, high), False
    return triplet(mid=float(raw)), False


def make_record(source, ref, locator, age, tau_c, luminosity, temperature, distance, *,
                component="reported_thermal", L_ul=False, T_ul=False, model=None,
                uncertainty=None, age_ref=None, age_basis=None, suffix=None, note=None,
                temperature_kind=None, age_upper_limit_yr=None):
    source_id = source["source_id"]
    age_status = "unavailable" if age[1] is None else "reported"
    if source_id == THREE_C_58:
        age_status = "disputed_association"
        age_basis = age_basis or "SN 1181 association adopted by the cited compilation"
        note = " ".join(filter(None, (note, "Ritter et al. (2021) associate SN 1181 with Pa 30.")))
    row = {
        "measurement_id": f"{source_id}:{ref}" + (f":{suffix}" if suffix else ""),
        "source_id": source_id, "name": source["name"], "class": source["class"],
        "reference": ref, "locator": locator, "reference_url": REFERENCES[ref][1],
        "age_reference": age_ref or ref, "age_basis": age_basis or "Independent age as compiled",
        "age_status": age_status,
        "tau_c_yr": tau_c, "age_upper_limit_yr": age_upper_limit_yr,
        "component": component, "spectral_model": model,
        "temperature_kind": temperature_kind,
        "luminosity_upper_limit": L_ul, "temperature_upper_limit": T_ul,
        "uncertainty": uncertainty, "note": note,
    }
    for unit, values in (
        ("age_yr", age), ("L_inf_erg_s", luminosity), ("kT_inf_eV", temperature),
        ("distance_kpc", distance),
    ):
        low, mid, high = values
        row.update({unit: mid, f"{unit}_lo": low, f"{unit}_hi": high})
    return row


def catalogue(master):
    sources, measurements, ages = [], [], []
    for cells in master.iter_rows(min_row=5, values_only=True):
        pid, name, association, cls, in_v13, in_p20, in_m24 = cells[:7]
        if pid is None:
            continue
        source = {
            "source_id": pid, "name": name, "class": cls, "association": association,
            "aliases": "CXOU J0852-4617; Vela Jr" if pid == 3 else None,
            "status": "historical_disputed" if pid == RETIRED_SOURCE else
                      "remnant_upper_limit" if name == "SN 1987A remnant" else "catalogued",
        }
        sources.append(source)
        if in_v13:
            _, _, _, log_tc, log_lo, log_hi, distance, log_Llo, log_Lhi, kT, model = cells[7:18]
            age = triplet(log_lo, None, log_hi, logarithmic=True)
            measurements.append(make_record(
                source, "V13", "Tables 1 and 3", age,
                triplet(mid=log_tc, logarithmic=True)[1],
                triplet(log_Llo, None, log_Lhi, logarithmic=True),
                triplet(mid=kT), triplet(mid=distance), model=model,
                uncertainty="Luminosity range includes statistical and distance errors",
                temperature_kind="Blackbody colour temperature",
            ))
            cool_limit = ADDITIONAL["vigano2013_cool_limits"].get(str(pid))
            if cool_limit:
                T_limit, log_Llimit = cool_limit
                measurements.append(make_record(
                    source, "V13", "Table 3, kTcool and log Lcool", age,
                    triplet(mid=log_tc, logarithmic=True)[1],
                    triplet(mid=log_Llimit, logarithmic=True),
                    triplet(mid=T_limit), triplet(mid=distance),
                    component="cool_surface_upper_limit", model="Additional blackbody",
                    L_ul=True, T_ul=True, suffix="cool_limit",
                    uncertainty="Conditional on the adopted spectral model and distance",
                    temperature_kind="Blackbody limit",
                ))
        if in_p20:
            _, _, distance, dlo, dhi, tc, alo, ahi, L, Llo, Lhi, kT = cells[18:30]
            temperature, tul = paper_temperature(kT)
            component = {"UL": "surface_upper_limit", "Hot-spot PSR": "hot_spot"}.get(cls, "reported_thermal")
            if pid in (3, 14):
                component = "whole_surface"
            measurements.append(make_record(
                source, "P20", f"Tables 1 and 2, row {pid}",
                triplet(alo, None, ahi, scale=1e3), None if tc is None else tc * 1e3,
                triplet(Llo, L, Lhi, scale=1e32), temperature, triplet(dlo, distance, dhi),
                component=component, L_ul=cls == "UL", T_ul=tul,
                uncertainty="See Table 2: typically 1σ; luminosity upper limits 3σ",
                note=f"Temperature transcription: {kT} eV." if kT else None,
                temperature_kind="Model dependent; see Table 2",
            ))
        if cells[58]:
            dlo, distance, dhi, _, _, _, tc, alo, age, ahi, Llo, L, Lhi, Tlo, T, Thi, date = cells[59:76]
            luminosity, lul = web_value(Llo, L, Lhi, scale=1e32)
            temperature, tul = web_value(Tlo, T, Thi)
            if T is None and Tlo is not None and Thi is not None:
                temperature = (Tlo, None, Thi)
            component = {"UL": "surface_upper_limit", "Hot-spot PSR": "hot_spot"}.get(cls, "reported_thermal")
            if pid == 3:
                component = "mixed_component_range"
            if pid == 14:
                component = "whole_surface"
            measurements.append(make_record(
                source, "WEB", f"Catalogue row, update {date}" if date else "Catalogue row",
                triplet(alo, age, ahi, scale=1e3), None if tc is None else tc * 1e3,
                luminosity, temperature, triplet(dlo, distance, dhi),
                component=component, L_ul=lul, T_ul=tul,
                age_upper_limit_yr=700 if pid == 9 else None,
                uncertainty="Catalogue min/max; may combine spectral models or components",
                note=("Web range combines Ho+26 cool and total luminosity."
                      if pid == 3 else "Published distance bounds are inconsistent."
                      if name == "RX J1605.3+3249" else None),
                temperature_kind="Model dependent; range can span components",
            ))
        if in_m24:
            obj = M24_OBS[pid]
            meta = MARINO[obj["name"]]
            age = triplet(obj["age_yr"][0], None, obj["age_yr"][1])
            L = obj["L32"]
            minus, plus = obj["L32_err"]
            distance = triplet(mid=meta["distance_kpc"])
            measurements.append(make_record(
                source, "M24", "Main text; Extended Data Table 2; Supplementary Data Table 6",
                age, None, triplet(L-minus, L, L+plus, scale=1e32), tuple(meta["kT_eV"]),
                distance, component="hot_spot", model=meta["model"], uncertainty="90%",
                age_basis=meta["age_basis"], note=meta["note"],
                temperature_kind="Blackbody colour temperature",
            ))
            measurements.append(make_record(
                source, "M24", "Extended Data Table 2; Supplementary Data Table 6",
                age, None, triplet(mid=meta["cool_L32_limit"], scale=1e32),
                triplet(mid=meta["cool_kT_limit_eV"]), distance,
                component="cool_surface_upper_limit", model="Additional blackbody, radius fixed",
                age_basis=meta["age_basis"], L_ul=True, T_ul=True, suffix="cool_limit",
                uncertainty="Conditional on the adopted spectral model and distance",
                note=meta["note"], temperature_kind="Blackbody limit",
            ))
        if pid == VELA_JR["id"]:
            meta = VELA_JR
            distance = tuple(meta["distance_kpc"])
            age = triplet(meta["ho_age_yr"][0], None, meta["ho_age_yr"][1])
            model = "Two hydrogen atmospheres"
            cool_low, cool_high = meta["cool_L32_range"]
            T_low, T_high = [8.617333262e-5 * T / meta["redshift_factor"]
                             for T in meta["cool_T_local_K_range"]]
            measurements.extend((
                make_record(
                    source, "HO26", "Section 4 and Table 6", age, None,
                    triplet(cool_low, None, cool_high, scale=1e32),
                    (T_low, (T_low + T_high) / 2, T_high), distance,
                    component="cool_surface", model=model, suffix="cool",
                    uncertainty="Range across best-fit spectral models",
                    age_basis="Allen et al. (2015), as adopted by Ho et al.",
                    temperature_kind="Redshifted atmosphere effective temperature",
                ),
                make_record(
                    source, "HO26", "Section 4", age, None,
                    triplet(*meta["total_L32"], scale=1e32), triplet(), distance,
                    component="total_thermal", model=model, suffix="total",
                    uncertainty="Quoted bolometric luminosity uncertainty",
                    age_basis="Allen et al. (2015), as adopted by Ho et al.",
                    note="Total includes the hot spot, which dominates the observed flux.",
                ),
            ))
            for ref, limits, basis in (
                ("HO26", meta["ho_age_yr"], "Allen et al. (2015) estimate adopted by Ho et al."),
                ("SU26", meta["suherli_age_yr"], "SNR radius and shock speeds at the revised distance"),
            ):
                ages.append({
                    "source_id": pid, "name": name, "reference": ref, "reference_url": REFERENCES[ref][1],
                    "age_yr_lo": limits[0], "age_yr_hi": limits[1], "age_basis": basis,
                    "distance_kpc": distance[1] if ref == "SU26" else None,
                })

    comparison = comparison_sample(sources, measurements)
    validate(sources, measurements, comparison)
    return {"Sources": sources, "Measurements": measurements,
            "Cooling_comparison": comparison, "VelaJr_ages": ages}


def comparison_sample(sources, measurements):
    """One representative L per source with an independent age and documented provenance."""
    by_source = {}
    for row in measurements:
        if (row["age_status"] != "reported" or row["L_inf_erg_s"] is None or
                row["class"] == "MAG" or row["source_id"] == RETIRED_SOURCE or
                row["component"] not in ("cool_surface", "whole_surface", "reported_thermal", "surface_upper_limit")):
            continue
        by_source.setdefault(row["source_id"], []).append(row)
    preference = ("HO26", "WEB", "P20", "V13")
    sample = []
    for source in sources:
        options = by_source.get(source["source_id"])
        if not options:
            continue
        best = min(options, key=lambda row: preference.index(row["reference"])).copy()
        if best["reference"] == "HO26":
            low, high = VELA_JR["suherli_age_yr"]
            best.update(age_yr=math.sqrt(low * high), age_yr_lo=low, age_yr_hi=high,
                        age_reference="SU26", age_basis="SNR radius and shock speeds at the revised distance",
                        note="Ho et al. luminosity paired with the Suherli et al. age estimate.")
        sample.append(best)
    return sample


def validate(sources, measurements, comparison):
    """Fail the rebuild if cross-matching or value transformations corrupt coverage."""
    ids = {source["source_id"] for source in sources}
    keys = {row["measurement_id"] for row in measurements}
    if len(ids) != len(sources) or len(keys) != len(measurements):
        raise ValueError("Duplicate source or measurement ID")
    if ids != {row["source_id"] for row in measurements}:
        raise ValueError("Catalogue source and measurement coverage disagree")
    counts = Counter(row["reference"] for row in measurements)
    if counts["M24"] != 2 * len(M24_OBS):
        raise ValueError("Incomplete Marino measurements")
    if len({row["source_id"] for row in comparison}) != len(comparison):
        raise ValueError("Duplicate source in cooling comparison")
    for row in (*measurements, *comparison):
        for field in ("age_yr", "L_inf_erg_s", "kT_inf_eV"):
            bounds = [row[key] for key in (f"{field}_lo", field, f"{field}_hi") if row[key] is not None]
            if any(not math.isfinite(value) or value <= 0 for value in bounds) or bounds != sorted(bounds):
                raise ValueError(f"{row['measurement_id']}: invalid {field} values {bounds}")


def export_csv(tables):
    for title, rows in tables.items():
        filename = "vela_jr_ages" if title == "VelaJr_ages" else title.lower()
        with (ROOT / "data" / f"{filename}.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    bibliography = [{"reference": key, "citation": citation, "url": url}
                    for key, (citation, url) in REFERENCES.items()]
    with (ROOT / "data" / "references.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(bibliography[0]))
        writer.writeheader()
        writer.writerows(bibliography)
