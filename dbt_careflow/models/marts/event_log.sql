select distinct
    case_id         as Case_ID,
    activity_name   as Activity_Name,
    event_timestamp as event_time,
    doctor,
    age_group
from {{ ref('stg_ehr_events') }}