WITH energy_differences AS (
    SELECT
        category,
        (energy_after - energy_before) AS energy_delta,
        AVG(energy_after - energy_before)
            OVER (PARTITION BY category)
            AS avg_energy_delta,
        COUNT(*) OVER (PARTITION BY category) AS total_category_rows,
        ROW_NUMBER()
            OVER (PARTITION BY category ORDER BY (energy_after - energy_before))
            AS row_number
    FROM activities
)

SELECT
    category,
    ROUND(avg_energy_delta, 2) AS avg_energy_delta,
    MEDIAN(energy_delta) AS median_energy_delta,
    MAX(
        CASE
            WHEN row_number = CEIL(total_category_rows * 0.25) THEN energy_delta
        END
    ) AS q1,
    MAX(
        CASE
            WHEN row_number = CEIL(total_category_rows * 0.75) THEN energy_delta
        END
    ) AS q3,
    (
        MAX(
            CASE
                WHEN
                    row_number = CEIL(total_category_rows * 0.75)
                    THEN energy_delta
            END
        )
        - MAX(
            CASE
                WHEN
                    row_number = CEIL(total_category_rows * 0.25)
                    THEN energy_delta
            END
        )
    ) AS iqr_energy_delta,
    ROUND(SQRT(AVG(POWER(energy_delta - avg_energy_delta, 2))), 2)
        AS sd_energy_delta,
    COUNT(*) AS n
FROM energy_differences
GROUP BY category
HAVING n > 10 -- to remove the ones with low sample size
ORDER BY avg_energy_delta DESC;
