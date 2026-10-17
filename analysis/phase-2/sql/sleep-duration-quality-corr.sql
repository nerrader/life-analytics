SELECT
    id,
    quality,
    ROUND(((JULIANDAY(end_at) - JULIANDAY(start_at)) * 86400), 0)
        AS sleep_duration_seconds
FROM sleep
WHERE sleep_type IS NOT 'nap';
