# AWS Pillar Reference

Per-pillar quirks for the five AWS services covered by the Vantage MCP. Read the section for the pillar the user is asking about before diving into tool calls.

---

## EC2 (compute)

The widest pillar — ~180 instance families, from old `t1`/`m1` through current-gen Graviton (`*g`, `*gd`, `*gn`), Intel (`m7i`, `c7i`), AMD (`m7a`, `c7a`), and specialty (Mac, FPGA `f2`, training `trn1n`/`trn2`, inference `inf2`, GPU `p5/p6`, HPC `hpc7g`).

### Family naming conventions

The first letter is the **purpose**:
- `t` — burstable (cheap baseline + CPU credits)
- `m` — general purpose (balanced CPU:RAM)
- `c` — compute optimized (CPU-heavy)
- `r` / `x` — memory optimized (RAM-heavy; `x` is the big one)
- `i` / `is` / `i7ie` — storage / IOPS optimized (NVMe local)
- `d` — dense storage (HDD)
- `g` / `p` — GPU
- `f` — FPGA
- `inf` / `trn` — Inferentia / Trainium ML accelerators
- `hpc` — HPC-tuned
- `mac` — macOS bare metal
- `u` / `u7i` — high-memory (TB-scale RAM, SAP HANA)

The numeric is the **generation** (`m5` → `m6i` → `m7i` → `m8i`, getting newer). Default to the highest generation available unless the user has constraints.

Suffix letters mean:
- `a` — AMD
- `g` — Graviton (ARM)
- `i` — Intel
- `d` — local NVMe SSD
- `n` — enhanced networking
- `b` — bandwidth-optimized
- `flex` — flex (cheaper, occasional throttling)
- `e` — extended memory or enhanced
- `z` — high frequency

Common right-sizing pattern: if a user says "general purpose, current-gen, ~16 GB RAM," that's almost always `m7i.xlarge` or `m7g.xlarge` (Graviton, ~20% cheaper if their workload is ARM-portable).

### EC2 indexes

`get-ec2-indexes` returns categories across **four axes**:
- RAM bands (`under-16gb-ram`, ..., `over-512gb-ram`)
- vCPU bands (`under-4-vcpu`, ..., `over-128-vcpu`)
- Hourly on-demand price bands (`under-0.15-hr-on-demand`, ..., `more-than-8-hr-on-demand`)
- GPU count (`has-1-gpu`, `has-over-1-under-3-gpus`, `has-over-3-under-8-gpus`, `has-over-8-gpus`)

You can call `use-ec2-index` with each, then intersect the resulting instance lists for AND queries (e.g., "32 GB RAM AND under $0.50/hr AND 1 GPU").

### EC2 pricing matrix rows

The OS rows in `get-ec2-region-pricing` are: `Linux`, `RHEL`, `RHEL with HA`, `RHEL SQL Server`, `RHEL SQL Web`, `rhelHASQL`, `SLES`, `Ubuntu`, `Windows`, `Windows SQL Server`, `Windows SQL Web`, `Linux SQL Server`, `Linux SQL Web`, `Dedicated`. Default to `Linux` unless the user mentions a Microsoft stack or a paid Linux distro.

Note that **Dedicated** is dramatically more expensive (it's tenancy isolation, not a license SKU). Don't surface it unless the user explicitly asks about dedicated tenancy.

---

## RDS (managed relational databases)

### Engine pricing

The pricing matrix's rows are AWS RDS engines. Common ones:
- `PostgreSQL`, `MySQL`, `MariaDB`, `Aurora PostgreSQL`, `Aurora MySQL` — fully managed AWS pricing.
- `Oracle BYOL`, `Oracle SE`, `Oracle EE` — Oracle. BYOL = bring-your-own-license, much cheaper than license-included.
- `SQL Server SE`, `SQL Server EE`, `SQL Server Web`, `SQL Server Express` — Microsoft. Express is free-tier-ish.

Pricing varies up to **10×** between engines for the same instance class. PostgreSQL on `db.r6g.large` is dramatically cheaper than Oracle EE on the same hardware. Always pick the engine row that matches what the user is running.

### RDS instance class naming

The class prefix follows EC2 with `db.` (e.g., `db.r6g.4xlarge` is the RDS counterpart of `r6g.4xlarge`). Memory-optimized (`db.r*`) is most common; general-purpose (`db.m*`) and burstable (`db.t*`) are also frequent.

### Right-sizing tip for RDS

- If they're running OLTP with steady connection counts, prefer `db.r*` (more RAM helps the buffer pool).
- If they're running smaller workloads or dev/test, `db.t*` burstable is cheap and fine.
- Aurora has its own pricing and isn't always one-to-one with classic RDS — make sure to confirm whether the user is on Aurora.

---

## ElastiCache (Redis / Memcached)

### Engine

The two engines are **Redis** (most common; persistence, replication, pub/sub) and **Memcached** (simpler, sharded). Pricing is similar but Redis with multi-AZ replication doubles your spend roughly.

### Right-sizing

ElastiCache pricing is mostly RAM-bound. Pick the smallest `cache.r*` (memory-optimized) that holds the working set + ~30% headroom. `cache.t4g.micro` is the cheap entry point for dev/test (single-digit cents per hour).

### Common gotcha

Reserved nodes for ElastiCache are per-node, not per-cluster. A user with a 6-shard Redis cluster needs 6 reservations (or 12 with replicas).

---

## OpenSearch

### Right-sizing

Three node roles: data, master, ingest. The Vantage MCP returns instances suitable for any role; you have to apply judgment:
- **Data nodes** — pick by the storage and RAM ratio you need (typically `r*` family or storage-optimized `i3*`).
- **Master nodes** — small (`m*.large` is fine for clusters under ~10 data nodes) but you need 3 for HA, so it's a flat overhead.
- **Ingest** — usually colocated with data unless the user has heavy preprocessing.

Pricing matrix is engine-aware (OpenSearch vs older Elasticsearch SKUs may both appear). Default to OpenSearch.

---

## Redshift

### Smallest pillar

Only ~7 instance types: `dc2.large`, `dc2.8xlarge`, `ra3.large`, `ra3.xlplus`, `ra3.4xlarge`, `ra3.16xlarge`, `rg.xlarge`. **Skip indexes entirely** — just enumerate with `get-redshift-instance-types` and compare directly.

### Three node generations

- `dc2` — older, attached SSD storage. Storage scales with node count.
- `ra3` — modern, **separates compute and storage** (managed S3 storage, "RMS"). Almost always the right answer for new workloads — you can pause clusters without losing data.
- `rg` — newest serverless-adjacent option.

### Pricing notes

Redshift bills per node-hour; storage is separate for `ra3`. The Vantage MCP returns node-hour pricing — make sure to multiply by node count and add storage cost (which Vantage may not have). If the user wants total spend, flag that storage is a separate line item.

---

## Cross-pillar advice

When the user is choosing between, say, "RDS Postgres vs running Postgres myself on EC2," remember:

- **RDS price includes** managed backups, patching, automatic failover, monitoring. EC2 is naked compute; you'd run all that yourself.
- A rough rule of thumb: RDS costs **~50–80% more** than the equivalent EC2 instance, and that delta is what you're paying for managed operations.
- For most teams, RDS is worth it. For teams with strong DBA capacity or unusual configs, self-managed on EC2 can be cheaper but rarely *that* much cheaper after you factor in your time.

Same logic applies for ElastiCache vs DIY Redis on EC2, OpenSearch vs DIY ES, etc.
