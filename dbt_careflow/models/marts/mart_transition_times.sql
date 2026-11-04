with ordered as (
    select
        Case_ID,
        Activity_Name as from_activity,
        event_time    as t1,
        lead(Activity_Name) over (partition by Case_ID order by event_time) as to_activity,
        lead(event_time)    over (partition by Case_ID order by event_time) as t2
    from {{ ref('event_log') }}
)
select
    from_activity,
    to_activity,
    count(*)                                         as cases,
    round(avg(timestamp_diff(t2, t1, minute)), 1)    as avg_minutes
from ordered
where to_activity is not null
group by from_activity, to_activity
order by avg_minutes desc