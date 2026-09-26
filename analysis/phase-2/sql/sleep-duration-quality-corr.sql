SELECT
    id,
    ROUND(((julianday(end_at) - julianday(start_at)) * 86400), 0) AS sleep_duration_seconds,
    quality
FROM sleep
WHERE sleep_type IS NOT 'nap';
