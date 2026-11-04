with seq as (
    select
        Case_ID,
        any_value(age_group)                  as age_group,
        max(doctor)                           as doctor,
        countif(Activity_Name = 'Triage')     as triage_visits,
        countif(Activity_Name = 'X-Ray')      as xray_visits,
        min(event_time)                       as case_start,
        max(event_time)                       as case_end
    from {{ ref('event_log') }}
    group by Case_ID
)
select
    *,
    triage_visits > 1                                   as sent_back_to_triage,
    triage_visits = 1                                   as is_compliant,
    timestamp_diff(case_end, case_start, minute)        as total_minutes
from seq