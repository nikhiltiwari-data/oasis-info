from google.cloud import bigquery

PROJECT_ID = "careflow-project-513611"     # <-- yahan apna Project ID likho
DATASET = "careflow_raw"
TABLE = "ehr_events"
CSV_FILE = "raw_events.csv"

client = bigquery.Client(project=PROJECT_ID)

# Dataset banao (agar pehle se hai to koi problem nahi)
client.create_dataset(f"{PROJECT_ID}.{DATASET}", exists_ok=True)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,          # header row skip
    autodetect=True,              # columns ke types khud pehchane
    write_disposition="WRITE_TRUNCATE",   # dobara chalane pe table replace ho jaye
)

with open(CSV_FILE, "rb") as f:
    job = client.load_table_from_file(
        f, f"{PROJECT_ID}.{DATASET}.{TABLE}", job_config=job_config
    )
job.result()   # load poora hone tak wait

table = client.get_table(f"{PROJECT_ID}.{DATASET}.{TABLE}")
print(f"Loaded {table.num_rows} rows into {PROJECT_ID}.{DATASET}.{TABLE}")