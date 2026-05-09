"""
Holiday-aware shipment date compute.

Real exporter use case: given an ETD (Estimated Time of Departure) from the
carrier, compute SI (Shipping Instructions) cut-off, VGM cut-off, gate-in
cut-off, and document submission deadlines — all with weekend + Indonesian
public holiday shifting.

Author: Gamma Wira <gammawirawibowo@gmail.com>
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, timedelta
from typing import Iterable


# Indonesian national holidays — extend as needed. For production, sync from
# Kemendagri / Kemnaker official calendar each year.
ID_HOLIDAYS_2026 = {
    date(2026, 1, 1):   "New Year",
    date(2026, 1, 17):  "Isra Mi'raj",
    date(2026, 2, 17):  "Imlek",
    date(2026, 3, 19):  "Nyepi",
    date(2026, 3, 20):  "Idul Fitri (eve)",
    date(2026, 3, 21):  "Idul Fitri",
    date(2026, 3, 22):  "Idul Fitri",
    date(2026, 5, 1):   "Labour Day",
    date(2026, 5, 14):  "Ascension Day",
    date(2026, 5, 27):  "Idul Adha",
    date(2026, 6, 1):   "Pancasila Day",
    date(2026, 6, 17):  "Islamic New Year",
    date(2026, 8, 17):  "Independence Day",
    date(2026, 8, 26):  "Mawlid",
    date(2026, 12, 25): "Christmas",
}


def is_business_day(d: date, holidays: dict[date, str] = ID_HOLIDAYS_2026) -> bool:
    if d.weekday() >= 5:  # Sat=5, Sun=6
        return False
    if d in holidays:
        return False
    return True


def shift_to_business_day(d: date, *, direction: str = "back", holidays: dict[date, str] = ID_HOLIDAYS_2026) -> date:
    """If d is non-business, shift backward (or forward) until it is."""
    step = -1 if direction == "back" else 1
    while not is_business_day(d, holidays):
        d += timedelta(days=step)
    return d


def offset_business_days(start: date, n: int, holidays: dict[date, str] = ID_HOLIDAYS_2026) -> date:
    """Return the date n BUSINESS days before/after start. Negative n = before."""
    step = 1 if n > 0 else -1
    remaining = abs(n)
    cur = start
    while remaining > 0:
        cur += timedelta(days=step)
        if is_business_day(cur, holidays):
            remaining -= 1
    return cur


@dataclass
class ShipmentSchedule:
    etd: date
    si_cutoff: date          # 4 business days before ETD
    vgm_cutoff: date         # 3 business days before ETD
    gate_in_cutoff: date     # 2 business days before ETD
    docs_to_buyer: date      # 1 business day after ETD
    bl_release: date         # 5 business days after ETD


def compute_schedule(etd: date) -> ShipmentSchedule:
    """Compute the standard cut-off schedule for an exporter shipment."""
    return ShipmentSchedule(
        etd=etd,
        si_cutoff=shift_to_business_day(offset_business_days(etd, -4), direction="back"),
        vgm_cutoff=shift_to_business_day(offset_business_days(etd, -3), direction="back"),
        gate_in_cutoff=shift_to_business_day(offset_business_days(etd, -2), direction="back"),
        docs_to_buyer=shift_to_business_day(offset_business_days(etd, 1), direction="forward"),
        bl_release=shift_to_business_day(offset_business_days(etd, 5), direction="forward"),
    )


# ---- demo ------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser()
    ap.add_argument("--etd", required=True, help="Estimated Time of Departure (YYYY-MM-DD)")
    args = ap.parse_args()

    etd = date.fromisoformat(args.etd)
    sched = compute_schedule(etd)
    out = {k: v.isoformat() for k, v in asdict(sched).items()}
    print(json.dumps(out, indent=2))
