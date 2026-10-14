"""Trainer tool: regenerate seed/patients.csv (synthetic PII, deterministic)."""
import csv
import random
from pathlib import Path

random.seed(7)
FIRST = ["Asha", "Ravi", "Meera", "Karan", "Sana", "Vikram", "Isha", "Arjun", "Neha", "Rohan",
         "Priya", "Dev", "Tara", "Kabir", "Anaya", "Rahul", "Divya", "Nikhil", "Pooja", "Sameer"]
LAST = ["Rao", "Mehta", "Kulkarni", "Iyer", "Shah", "Nair", "Gupta", "Reddy", "Das", "Joshi"]
NOTES = ["Hypertension", "Type 2 diabetes", "Asthma", "Migraine", "Routine check-up"]

out = Path(__file__).resolve().parent.parent / "seed" / "patients.csv"
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["patient_id", "full_name", "dob", "phone", "email", "national_id", "diagnosis_note"])
    for i, first in enumerate(FIRST, start=1):
        name = f"{first} {random.choice(LAST)}"
        w.writerow([
            i, name,
            f"19{random.randint(55, 99)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"+91-9{random.randint(100000000, 999999999)}",
            f"{first.lower()}{i}@example.test",
            f"SYN-{random.randint(10000000, 99999999)}",
            random.choice(NOTES),
        ])
print(f"wrote {out}")
