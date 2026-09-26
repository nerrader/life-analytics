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

> Result produced by query: `sql/second-phase-findings.sql`

- SPORTS and MAINT activities are associated with positive energy deltas.
- IDLE and DEV have energy deltas close to zero.
- SOCIAL and SCHOOL activities are associated with negative energy deltas.

I find it interesting that the MAINT category increases my energy, while IDLE does not.
You would think that taking a break or resting would potentially increase energy later on, but apparently not?

And another observation is that the SOCIAL category apparently tends to decrease my energy, despite having a relatively high average enjoyability rate of 3.84/5.

> Average enjoyability rate produced by query: `sql/average-social-enjoyability`

These observations led to two new questions, that I will be adding in the unanswered questions list:

- Why are MAINT activities associated with a positive energy delta, while IDLE has a neutral change?
- Why are SOCIAL activities associated with a negative energy delta, despite having a high average enjoyability?
