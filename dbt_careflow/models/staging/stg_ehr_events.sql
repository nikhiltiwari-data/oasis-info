select
    trim(case_id)                     as case_id,
    initcap(lower(trim(activity)))    as activity_name,
    cast(`timestamp` as timestamp)    as event_timestamp,
    doctor,
    age_group
from {{ source('careflow_raw', 'ehr_events') }}
where case_id is not null
  and activity is not null
  and `timestamp` is not null