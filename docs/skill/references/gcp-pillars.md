# GCP Pillar Reference

Per-pillar quirks for GCP services covered by the Vantage MCP and adjacent operations.

---

## Compute Engine

### Family naming

GCP machine families have less convention-baked-in than AWS, but the patterns are:

- `e2` — economical / general-purpose, shared core or up to small RAM. Cheap baseline.
- `n2` / `n2d` — general-purpose Intel / AMD, the most common workhorse.
- `n4` — newest general-purpose Intel (Sapphire Rapids).
- `c3` / `c3d` — compute-optimized Intel / AMD; high clock speeds.
- `c4` — newest compute-optimized.
- `m1` / `m2` / `m3` — memory-optimized (multi-TB RAM).
- `t2a` / `t2d` — Tau (ARM / AMD) general-purpose, cost-optimized.
- `a2` — A100 GPU instances.
- `a3` — H100 GPU instances.
- `g2` — L4 GPU instances.
- `h3` — HPC-tuned.
- `z3` — storage-optimized.

Suffix letters: `d` = local SSD, `s` = standard, `n` = high network.

### Indexes

`get-gcp-indexes` returns the same four-axis filter system as EC2: RAM bands, vCPU bands, on-demand price bands, and GPU count bands. Same intersection pattern — call `use-gcp-index` for each constraint, intersect, then enrich finalists.

### Pricing peculiarities

- **Sustained Use Discounts (SUD)** apply *automatically* for usage above thresholds (no commitment needed). Non-trivial — up to 30% off list. Mention this when comparing GCP to AWS where AWS has no equivalent.
- **Committed Use Discounts (CUD)** are 1-year or 3-year commitments analogous to AWS Savings Plans. Resource-based (lock specific machine type) or spend-based (commit dollars/hour, flexible).
- **Preemptible / Spot VMs** — 60–91% discount. Max 24-hour life for preemptible (legacy); Spot is the modern variant with no max lifetime but interruptible.
- Pricing in the matrix is per **machine type**, not per node — multiply by replica count for clusters.

### Operations cheatsheet

- List: `gcloud compute instances list --filter="zone:us-central1-* AND status=RUNNING"`
- Stop: `gcloud compute instances stop INSTANCE --zone=ZONE`
- Resize: `gcloud compute instances set-machine-type INSTANCE --machine-type=n2-standard-4 --zone=ZONE` (instance must be stopped)

---

## Cloud SQL / AlloyDB

### Engines

- **Cloud SQL** — Postgres 13/14/15/16, MySQL 5.7/8.0, SQL Server 2017/2019/2022.
- **AlloyDB** — Postgres-compatible, GCP-built. Better TPC-H performance and pgvector-aware. Pricier than Cloud SQL.

Pick AlloyDB for analytical Postgres workloads, Cloud SQL for general OLTP.

### Pricing

The Vantage RDS-equivalent pillar in GCP doesn't exist as a separate Vantage tool — Cloud SQL pricing flows through the underlying Compute Engine machine type pricing plus a Cloud SQL premium. Use `gcp_billing_list_skus` (when wired) for exact list pricing, or estimate from GCE pricing × 1.5 to 2.0× for Cloud SQL premium.

---

## BigQuery

### Pricing models

Two billing modes — pick one per project:

- **On-demand** — $6.25 per TB scanned. Predictable per query but unpredictable monthly.
- **Editions (Standard / Enterprise / Enterprise Plus)** — slot-based. Pay for committed slots (capacity) per hour. Better for steady analytical workloads.

If wired, the BigQuery MCP can run SQL directly. Use `EXECUTE IMMEDIATE` and `BYTES_PROCESSED` to estimate query cost before running expensive ones.

### Storage pricing

Separate from compute: **active storage** ($0.02/GB/month) vs **long-term storage** ($0.01/GB/month — applies after 90 days untouched).

---

## Spanner

Globally consistent SQL DB. Billed per **node-hour** + per **GB-month** of storage:

- **Regional** instances — single region, ~$0.90/node-hour.
- **Multi-regional** instances — two-region with strong consistency, ~$3/node-hour.
- **Granular instance** sizing — Processing Units (PU); 1000 PU = 1 node.

Don't pick Spanner unless you need global strong consistency. For regional OLTP, AlloyDB or Cloud SQL is dramatically cheaper.

---

## GKE (Kubernetes Engine)

### Two modes

- **Standard** — you manage node pools. Free control plane for one zonal cluster per billing account; $0.10/hr per cluster after that.
- **Autopilot** — GCP manages nodes; pay per pod-vCPU/memory-hour with a premium.

For most teams Autopilot is the right default. Standard if you need GPU node pools or specific machine types.

### Operations cheatsheet

- List: `gcloud container clusters list`
- Get kubeconfig: `gcloud container clusters get-credentials CLUSTER --region=REGION`
- Resize node pool: `gcloud container clusters resize CLUSTER --num-nodes=N --node-pool=POOL`

---

## Memorystore (Redis / Memcached)

### Tiers

- **Basic** — single node Redis, no HA.
- **Standard** — primary + replica, automatic failover.
- **Cluster** — Redis Cluster mode, sharded, larger working sets.

Pricing is per **GB-hour** of memory. Standard tier costs ~2× Basic for HA.

---

## Vertex AI (foundation models + ML platform)

### Foundation models

- **Gemini API** — text + multimodal. Billed per 1k tokens.
- **PaLM 2** — legacy.
- **Model Garden** — Mistral, Llama 3, Anthropic Claude (also available here), etc. Some are usage-based, some require deploying to an endpoint (per-hour).

When the user wants to use Anthropic Claude, mention that Vertex AI is one of three places (Anthropic API direct, AWS Bedrock, GCP Vertex) — there's no general "best" — depends on existing cloud commitment.

### ML platform

- **Endpoints** — billed per machine-type-hour while running, regardless of traffic. Stop endpoints when idle.
- **Custom training jobs** — billed per machine-type-hour during the job.
- **Pipelines** — orchestrated workflows; pay for underlying jobs.

---

## Pub/Sub vs Pub/Sub Lite

Pub/Sub is global, auto-scaling, pay-per-message. Pub/Sub Lite is regional, pay-per-throughput-unit-hour, ~10× cheaper for high steady throughput. If the user mentions ingest of "millions of messages per second steady-state," consider Lite.

---

## Cross-pillar advice

- **GCS vs Cloud SQL for cold data** — sometimes "I have a 500 GB Postgres table I rarely query" is cheaper as a Parquet export to GCS + BigQuery external table.
- **Spanner vs AlloyDB** — Spanner only when you need *global* strong consistency. AlloyDB is the default for high-end Postgres.
- **Cloud Run vs GKE** — Cloud Run for stateless HTTP services; GKE when you need stateful sets, daemons, or specific networking.
