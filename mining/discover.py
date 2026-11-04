import os
import pandas as pd
import pm4py
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT = "careflow-project-513611"
KEY = "gcp_key.json"
os.makedirs("outputs", exist_ok=True)

creds = service_account.Credentials.from_service_account_file(KEY)
client = bigquery.Client(project=PROJECT, credentials=creds)
df = client.query(f"""
    select Case_ID, Activity_Name, event_time, doctor, age_group
    from `{PROJECT}.careflow_analytics.event_log`
""").to_dataframe()

df["event_time"] = pd.to_datetime(df["event_time"], utc=True).dt.tz_localize(None)
df = pm4py.format_dataframe(df, case_id="Case_ID",
                            activity_key="Activity_Name",
                            timestamp_key="event_time")
print(f"{df['case:concept:name'].nunique()} cases, {len(df)} events")

# 1) Spaghetti diagram (frequency)
dfg, start_acts, end_acts = pm4py.discover_dfg(df)
pm4py.save_vis_dfg(dfg, start_acts, end_acts, "outputs/as_is_frequency.png")

# 2) Performance map (average time on each arrow)
perf, s, e = pm4py.discover_performance_dfg(df)
pm4py.save_vis_performance_dfg(perf, s, e, "outputs/as_is_performance.png")

# 3) Petri net
net, im, fm = pm4py.discover_petri_net_inductive(df)
pm4py.save_vis_petri_net(net, im, fm, "outputs/petri_net.png")

print("Done. Images saved in outputs/")