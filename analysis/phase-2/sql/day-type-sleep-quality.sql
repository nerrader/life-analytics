SELECT
    CASE
        WHEN strftime('%w', sleep.end_at) IN ('0', '6') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    avg(sleep.quality) AS avg_sleep_quality,
    count(*) AS n
FROM sleep
WHERE sleep.sleep_type IS NOT 'nap'
GROUP BY day_type;
