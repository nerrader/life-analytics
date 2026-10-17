SELECT
    CASE
        WHEN STRFTIME('%w', sleep.end_at) IN ('0', '6') THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    ROUND(AVG(summary.mood), 2) AS avg_mood,
    ROUND(AVG(summary.productivity), 2) AS avg_productivity,
    ROUND(AVG(summary.stress), 2) AS avg_stress,
    COUNT(*) AS n
FROM sleep
INNER JOIN daily_summaries AS summary
    ON DATE(sleep.end_at) = summary.summary_date
WHERE sleep.sleep_type IS NOT 'nap'
GROUP BY day_type;
