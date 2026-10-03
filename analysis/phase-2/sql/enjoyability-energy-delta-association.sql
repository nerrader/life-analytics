SELECT
    enjoyability,
    AVG((energy_after - energy_before)) AS energy_delta,
    COUNT(*) AS count
FROM activities
GROUP BY enjoyability
ORDER BY enjoyability DESC;
