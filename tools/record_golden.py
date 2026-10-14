"""Trainer tool: regenerate legacy_billing/golden/invoices.json.

The legacy module is Python 2.7 and cannot run on modern machines. This script is a
line-for-line Python 3 transcription of legacy_billing/billing.py with Python 2's
integer division written out as `//` (all operands are non-negative ints, so `/` in
Python 2 and `//` in Python 3 are identical).

IMPORTANT: if you have a Python 2.7 interpreter, record the golden file from the real
legacy code instead and diff it against this output:
    python2 legacy_billing/run_legacy.py legacy_billing/fixtures/visits.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "legacy_billing"
RATES = {"CONSULT": 5000, "XRAY": 12000, "LABPANEL": 3550, "VACCINE": 2799, "BANDAGE": 325}
TAX_EXEMPT = {"VACCINE", "LABPANEL"}
TAX_PERCENT = 7
COVERAGE = 80


def invoice(visit, n):
    subtotal = exempt_sub = 0
    for it in visit["items"]:
        cents = RATES[it["code"]] * it["qty"]
        subtotal += cents
        if it["code"] in TAX_EXEMPT:
            exempt_sub += cents
    pct = visit.get("discount_pct", 0)
    discount = subtotal * pct // 100
    exempt_discount = exempt_sub * pct // 100
    taxable = (subtotal - discount) - (exempt_sub - exempt_discount)
    tax = taxable * TAX_PERCENT // 100
    total = subtotal - discount + tax
    owes = total * (100 - COVERAGE) // 100 if visit.get("insured") else total
    return {
        "invoice_no": f"INV-{n:05d}",
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "patient_owes": owes,
        "avg_line": subtotal // len(visit["items"]),
    }


def main():
    visits = json.loads((ROOT / "fixtures" / "visits.json").read_text())
    golden = {v["visit_id"]: invoice(v, i) for i, v in enumerate(visits, start=1)}
    out = ROOT / "golden" / "invoices.json"
    out.write_text(json.dumps(golden, indent=2, sort_keys=True) + "\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
