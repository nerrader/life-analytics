# Second Phase Findings

This file will be focused on documenting my findings for the second phase, the EDA part of my life analysis.

## Category Energy Deltas

I decided to first investigate if different categories had varying energy deltas, and sure enough, while these were minor changes, there was.

| Category | Energy Delta | Count |
| --- | ---: | ---: |
| SPORTS | +0.694 | 18 |
| MAINT | +0.276 | 106 |
| IDLE | -0.020 | 76 |
| DEV | -0.051 | 79 |
| SOCIAL | -0.145 | 19 |
| SCHOOL | -0.392 | 60 |

> Result produced by [sql/category-energy-deltas.sql](sql/category-energy-deltas.sql)

- SPORTS and MAINT activities are associated with positive energy deltas.
- IDLE and DEV have energy deltas close to zero.
- SOCIAL and SCHOOL activities are associated with negative energy deltas.

I find it interesting that the MAINT category increases my energy, while IDLE does not.
You would think that taking a break or resting would potentially increase energy later on, but apparently not?

And another observation is that the SOCIAL category apparently tends to decrease my energy, despite having a relatively high average enjoyability rate of 3.84/5.

> Average enjoyability rate produced by [sql/average-social-enjoyability](sql/average-social-enjoyability.sql)

These observations led to two new questions, that I will be adding in the unanswered questions list:

- Why are MAINT activities associated with a positive energy delta, while IDLE has a neutral change?
- Why are SOCIAL activities associated with a negative energy delta, despite having a high average enjoyability?

## Things about Sleep

First, I wanted to see if your sleep quality had anything to do with duration.

![A graph showing no correlation between sleep quality and sleep duration](assets/analysis-images/no-sleep-duration-quality-correlation.png)
Results produced by [sql/no-sleep-duration-quality-correlation.sql](sql/no-sleep-duration-quality-correlation.sql) and Tableau Public.

Yeah, no, there isn't.
At least not an obvious one, the points are pretty scattered, with no obvious trend. This doesn't prove that they aren't correlated, but there is just not enough evidence of a relationship so far.

I also decided to look at if sleep quality had anything to do with daily summary metrics (mood, productivity, stress)

| Quality | Avg Mood | Avg Productivity | Avg Stress | n |
| ---: | ---: | ---: | ---: | ---: |
| 1.5 | 2.50 | 3.00 | 1.00 | 1 |
| 2.0 | 3.50 | 2.25 | 1.00 | 2 |
| 2.5 | 3.50 | 4.25 | 1.00 | 1 |
| 3.0 | 3.25 | 3.20 | 1.60 | 10 |
| 3.5 | 2.93 | 3.64 | 1.86 | 7 |
| 4.0 | 3.31 | 4.13 | 1.81 | 8 |
| 4.5 | 4.17 | 3.50 | 1.00 | 3 |

Results produced by [sql/sleep-quality-summary-metrics-corr.sql](sql/sleep-quality-summary-metrics-corr.sql)
There are some potentially interesting patterns here, with mood and productivity somewhat increasing with the quality, except at 4.5 where productivity drops (though it only has n = 3, so take that with a grain of salt) while stress showing no pattern whatsoever.

Though this is more of an interesting observation rather than a conclusion, as the sample size (n) is way too small to draw strong conclusions.

I also wanted to take a look at sleep quality during the weekends.

| Day Type | Avg Sleep Quality | n |
| ---: | ---: | ---: |
| Weekday | 3.25 | 22 |
| Weekend | 3.70 | 10 |

Results produced by [sql/day-type-sleep-quality.sql](sql/day-type-sleep-quality.sql)
Unsurprisingly, weekends are associated with a higher sleep quality than weekdays.

| Day Type | Avg Mood | Avg Productivity | Avg Stress | n |
| --- | ---: | ---: | ---: | ---: |
| Weekday | 3.1364 | 3.3068 | 1.6591 | 22 |
| Weekend | 3.6111 | 4.0000 | 1.4444 | 9 |

And weekends are also associated with higher productivity and higher mood.

Though again, the sample size (n) is too small to draw strong conclusions, so please keep that in mind and take this with a grain of salt.

So another question I would add is:

- Are the observed differences from weekends and weekdays consistent enough to be investigated further?
- Is a higher sleep quality really associated with overall higher performance on daily summary metrics?
