import pandas as pd
import numpy as np

# CareFlow Project - Phase 1 Event Log Preparation
patient_data = [
    {'Patient_ID': 'PAT-101', 'Activity': 'Triage', 'Timestamp': '2026-10-01 09:00:00'},
    {'Patient_ID': 'PAT-101', 'Activity': 'Consultation', 'Timestamp': '2026-10-01 09:30:00'},
    {'Patient_ID': 'PAT-101', 'Activity': 'Lab Test', 'Timestamp': '2026-10-01 10:15:00'},
    {'Patient_ID': 'PAT-101', 'Activity': 'Discharge', 'Timestamp': '2026-10-01 12:00:00'},
    {'Patient_ID': 'PAT-102', 'Activity': 'Triage', 'Timestamp': '2026-10-01 09:15:00'},
    {'Patient_ID': 'PAT-102', 'Activity': 'Consultation', 'Timestamp': '2026-10-01 10:00:00'},
    {'Patient_ID': 'PAT-102', 'Activity': 'Discharge', 'Timestamp': '2026-10-01 11:30:00'}
]

# Loading into dataframe
df = pd.DataFrame(patient_data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Cleaning duplicate records
df = df.sort_values(by=['Patient_ID', 'Timestamp']).drop_duplicates()

# Phase 2: Calculating Length of Stay (LOS) per patient
summary = df.groupby('Patient_ID').agg(
    Start_Time=('Timestamp', 'min'),
    End_Time=('Timestamp', 'max'),
    Total_Activities=('Activity', 'count')
).reset_index()

summary['LOS_Hours'] = (summary['End_Time'] - summary['Start_Time']).dt.total_seconds() / 3600

# Results output
print("Cleaned Event Log:")
print(df.head())

print("\nPatient Throughput Analytics:")
print(summary)
