# Pricing Models — The Pricing Pillars

Reference for the columns that come back from `get-<pillar>-region-pricing`. The matrix is wide because AWS sells the same hardware on many contractual terms — your job is to pick the column that fits the user's workload, not to enumerate them all.

!!! info "Terminology — pricing pillar / high-cost pillar"
    Throughout this skill the term **pricing pillar** (sometimes "high-cost pillar" or "Vantage pillar") refers to a service area covered by the Vantage pricing MCP: **EC2** (compute), **RDS** (relational DB), **ElastiCache** (cache), **OpenSearch** (search), and **Redshift** (warehouse) on AWS, plus their Azure and GCP equivalents. Each pillar exposes the same `get-<pillar>-region-pricing` tool shape with the same matrix of columns described below. Per-pillar quirks live in [aws-pillars.md](aws-pillars.md), [gcp-pillars.md](gcp-pillars.md), and [azure-pillars.md](azure-pillars.md).

---

## The four pricing model families

### 1. On-demand

Pay-per-hour, no commitment. Highest hourly price, maximum flexibility. The right answer for:
- Bursty workloads
- Workloads under 50% utilization
- Anything where you might switch instance families soon

In the matrix: the `On Demand` column.

### 2. Spot

Same hardware, but AWS can reclaim it on ~2 minutes' notice. Discount typically 60–90% off on-demand. The right answer for:
- Stateless, restartable batch jobs (training runs, render farms, CI workers)
- Anything that checkpoints
- Anything you're already running fault-tolerantly

In the matrix: `Spot Min`, `Spot Avg`, `Spot Max` (because spot prices vary across the day) and crucially `Spot Interrupt Frequency`.

**Watch the interrupt frequency.** Vantage returns one of: `<5%`, `5-10%`, `10-15%`, `15-20%`, `>20%`, or `N/A`. If it's `>20%`, this region/instance combination is heavily contested — surface that to the user. A 75% discount with daily evictions is wrong for a stateful workload.

### 3. Savings Plans

Compute commitment ($/hr for 1 or 3 years) that applies to *any* instance in a family (Compute SP) or any compute (Generic SP). Flexible — you're committing to a dollar amount, not a specific instance type. The right answer for:
- Steady baseline compute that you'll definitely keep using
- Workloads where you might rebalance across families

Columns:
- `1yr No Upfront (Savings Plan)` — pay monthly, smallest discount (~20–30% off on-demand)
- `1yr Partial Upfront (Savings Plan)` — half up front, slightly bigger discount
- `1yr All Upfront (Savings Plan)` — all paid up front, maximum 1yr discount
- `3yr No Upfront (Savings Plan)` — bigger discount than 1yr (~40–50%)
- `3yr Partial Upfront (Savings Plan)` — even bigger
- `3yr All Upfront (Savings Plan)` — maximum discount (~50–65% off on-demand)

### 4. Reserved Instances

Older mechanism. Locked to a specific instance family (or, for Convertible RIs, you can change family). Pricing is similar to Savings Plans but the contract is more rigid. Columns named without `(Savings Plan)` and with optional `(Convertible)` suffix.

In modern AWS accounts, **Savings Plans replace standard RIs for most cases**. Reserved Instances still matter for:
- RDS, ElastiCache, OpenSearch, Redshift — these don't have Savings Plans, so RI is the only commitment option.
- Existing RIs that are already on the books.

Convertible RIs (suffix `(Convertible)`) are middle ground — you can change family if needs shift, at slightly worse pricing than standard RI.

---

## Decision heuristic

Walk down this list with the user's workload in mind:

1. **Is the workload restartable and fault-tolerant?** → Spot (but check interrupt frequency).
2. **Is utilization steady at >70% for the next year+?** → 3yr commitment (Savings Plan if EC2, RI otherwise).
3. **Is utilization steady at >50% for the next year?** → 1yr Savings Plan (no upfront) — easiest sell internally.
4. **Will the family/region change soon?** → Convertible RI or stay on-demand.
5. **Otherwise** → on-demand.

Always present the user with at least the on-demand price plus the most-attractive commitment option. They'll often have organizational rules about whether 3yr or all-upfront is allowed.

---

## Worked example

User asks: "How much for an `r6i.4xlarge` in us-east-1 if we run it 24/7?"

Steps:
1. Call `get-ec2-region-pricing(instanceType="r6i.4xlarge", region="us-east-1")`.
2. From the matrix:
   - On-demand Linux: $X.XXX/hr → $X×730 = $Y/month
   - 1yr Savings Plan, no upfront: $A.AAA/hr → $A×730 = $B/month
   - 3yr Savings Plan, all upfront: $C.CCC/hr → $C×730 = $D/month
3. Output:

> Running `r6i.4xlarge` 24/7 in us-east-1:
>
> | Term | Hourly | Monthly | 3-yr total |
> | --- | --- | --- | --- |
> | On-demand | $X.XXX | $Y | $Y×36 |
> | 1yr Savings Plan, no upfront | $A.AAA | $B | $B×36 |
> | 3yr Savings Plan, all upfront | $C.CCC | $D | $D×36 |
>
> If you're confident about needing this exact spend for 3 years, the All Upfront Savings Plan saves ~$Z over on-demand. If you might rebalance families, stay on a 1yr no-upfront for flexibility.

Note: only show the columns that are relevant. Don't show Windows pricing if the user said Linux. Don't show Spot if the user said "24/7" — that contradicts Spot's purpose.

---

## Edge cases

- **Dedicated tenancy** is shown as a separate row, dramatically more expensive. Only mention it if the user is in a regulated industry or asks about compliance isolation.
- **N/A in a column** means that pricing model isn't offered for that combination. Don't fabricate a number — just skip the column.
- **Some columns appear for EC2 but not for RDS / ElastiCache** (e.g., Spot doesn't exist for RDS). Don't promise Spot pricing for managed services.
- **Region availability** — instances aren't supported in every region. `get-<pillar>-instance` lists supported regions; check before recommending a region.
