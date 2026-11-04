-- Ideal journey: Registration > Triage > [X-Ray] > [Lab Test] > Doctor Consultation > Discharge/Admission
with paths as (
    select
        Case_ID,
        string_agg(Activity_Name, ' > ' order by event_time) as path
    from {{ ref('event_log') }}
    group by Case_ID
)
select
    path,
    count(*)                                              as cases,
    round(100 * count(*) / sum(count(*)) over (), 1)      as pct_cases,
    regexp_contains(
        path,
        r'^Registration > Triage( > X-Ray)?( > Lab Test)? > Doctor Consultation > (Discharge|Admission)$'
    )                                                     as is_compliant_path
from paths
group by path
order by cases desc