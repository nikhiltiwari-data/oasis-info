import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)

DOCTORS = ["Dr_Sharma", "Dr_Rao", "Dr_Khan", "Dr_Iyer"]
AGE_GROUPS = ["0-17", "18-40", "41-65", "65+"]
LOOPBACK_PROB = 0.40   # X-Ray ke baad Triage pe wapas (missing form)
XRAY_PROB = 0.55
LAB_PROB = 0.30
N_CASES = 5000

rows = []
start = datetime(2026, 10, 1, 8, 0)

def add(case, activity, t, doctor=None, age=None):
    rows.append({"case_id": case, "activity": activity, "timestamp": t,
                 "doctor": doctor, "age_group": age})

for i in range(N_CASES):
    case = f"P{i:05d}"
    age = random.choice(AGE_GROUPS)
    t = start + timedelta(minutes=random.randint(0, 60 * 24 * 30))

    add(case, "Registration", t, age=age)
    t += timedelta(minutes=random.randint(3, 15))
    add(case, "Triage", t, age=age)
    t += timedelta(minutes=random.randint(10, 40))

    if random.random() < XRAY_PROB:
        add(case, "X-Ray", t, age=age)
        t += timedelta(minutes=random.randint(15, 45))
        if random.random() < LOOPBACK_PROB:      # hidden bottleneck
            add(case, "Triage", t, age=age)
            t += timedelta(minutes=random.randint(20, 60))

    if random.random() < LAB_PROB:
        add(case, "Lab Test", t, age=age)
        t += timedelta(minutes=random.randint(30, 90))

    add(case, "Doctor Consultation", t, doctor=random.choice(DOCTORS), age=age)
    t += timedelta(minutes=random.randint(10, 30))
    add(case, random.choice(["Discharge", "Admission"]), t, age=age)

df = pd.DataFrame(rows)

# Data ko thoda messy banao (dbt isko clean karega)
dup = df.sample(frac=0.02, random_state=1)                 # duplicate rows
df = pd.concat([df, dup], ignore_index=True)
upper = df["activity"].sample(frac=0.05, random_state=2).index
df.loc[upper, "activity"] = df.loc[upper, "activity"].str.upper()
spaced = df["activity"].sample(frac=0.03, random_state=3).index
df.loc[spaced, "activity"] = "  " + df.loc[spaced, "activity"] + " "

df = df.sample(frac=1, random_state=4).reset_index(drop=True)   # shuffle
df.to_csv("raw_events.csv", index=False)
print(f"Wrote {len(df)} events for {N_CASES} cases -> raw_events.csv")