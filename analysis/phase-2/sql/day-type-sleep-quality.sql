SELECT
    CASE
        WHEN STRFTIME('%w', sleep.end_at) IN ('0', '6') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    ROUND(AVG(sleep.quality), 2) AS avg_sleep_quality,
    COUNT(*) AS n
FROM sleep
WHERE sleep.sleep_type IS NOT 'nap'
GROUP BY day_type;
