# Azure Pillar Reference

Per-pillar quirks for Azure services covered by the Vantage MCP and adjacent operations.

---

## Virtual Machines

### Series naming

Azure VM series are letters denoting purpose, with version digits:

- **A / Av2** — entry-level / dev/test.
- **B** — burstable, like AWS t-family. Cheap baseline, CPU credits.
- **D / Dv5 / Dasv5 / Dadsv5** — general-purpose. The most common workhorse. Suffix letters: `a` = AMD, `s` = premium SSD, `d` = local temp disk. `Dasv5` = AMD + premium SSD, `Dadsv5` = AMD + temp disk + premium SSD.
- **E / Esv5 / Easv5** — memory-optimized (8 GiB/vCPU instead of D's 4).
- **F / Fsv2** — compute-optimized (high CPU:RAM ratio).
- **L / Lsv3** — storage-optimized.
- **M / Mv2** — high-memory (multi-TB).
- **N (NC / ND / NV / NG)** — GPU. NC = HPC + ML training, ND = AI training (H100 / A100), NV = visualization (gaming, design), NG = mixed.
- **HC / HB / HBv4** — HPC.

The version digit (`v3`, `v4`, `v5`, `v6`) indicates generation. Default to current-gen (v5/v6) unless user has constraints.

### Pricing peculiarities

- **Azure Hybrid Benefit** — bring on-prem Windows Server / SQL Server licenses for a discount. Doesn't show up in standard pricing matrix; ask if user has eligible licenses.
- **Reservations** — 1 or 3 year, similar to AWS RIs.
- **Savings Plans for Compute** — 1 or 3 year, applies across VM family/region (more flexible than reservations).
- **Spot VMs** — like AWS Spot; up to 90% off but evictable with 30s notice.
- **Low Priority VMs** (Batch only) — for HPC workloads, not the same as Spot.

### Operations cheatsheet

- List: `az vm list -d -o table` (the `-d` flag includes power state)
- Stop: `az vm deallocate --resource-group RG --name NAME` (deallocate stops billing; just `stop` keeps billing)
- Resize: `az vm resize --resource-group RG --name NAME --size Standard_D8s_v5`

---

## Azure SQL Database / Cosmos DB

### Azure SQL Database

Three deployment options:

- **Single database** — most common; isolated DB.
- **Elastic pool** — multiple DBs share allocated DTUs/vCores; cost-efficient for many small DBs.
- **Managed instance** — closest to a full SQL Server VM, with VNet integration.

Pricing model: **DTU-based** (legacy, simpler) or **vCore-based** (recommended, more flexible). Within vCore, choose **Provisioned** or **Serverless** (auto-pause).

### Cosmos DB

Multi-API (SQL / MongoDB / Cassandra / Gremlin / Table). Billing by **Request Units (RUs)**:

- **Provisioned throughput** — pay for guaranteed RU/s/hour.
- **Autoscale** — provisions max, charges based on actual.
- **Serverless** — pay per request. Fine for sporadic dev/test or low-traffic apps.

Don't recommend Cosmos by default — it's expensive at scale. Reach for Cosmos when you specifically need global multi-region writes or one of the non-SQL APIs.

---

## Synapse Analytics

Three compute models inside Synapse:

- **Dedicated SQL pool** — provisioned columnar warehouse, like Redshift. Billed per **DWU-hour**.
- **Serverless SQL pool** — query files in ADLS, billed per TB scanned (like Athena).
- **Apache Spark pool** — provisioned Spark cluster, billed per **vCore-hour**.

For new analytics workloads, **Microsoft Fabric** is the recommended successor (lakehouse on OneLake) — surface this if the user is starting fresh.

---

## AKS (Azure Kubernetes Service)

### Cluster pricing

The control plane was free until recently — now there's a "Standard" SKU with SLA at $0.10/hour. Free SKU is fine for dev.

### Node pools

- **System pool** — runs cluster system pods.
- **User pools** — application workloads.
- **Spot node pool** — preemptible nodes for stateless workloads.

### Operations cheatsheet

- List: `az aks list -o table`
- Get kubeconfig: `az aks get-credentials --resource-group RG --name CLUSTER`
- Scale node pool: `az aks nodepool scale --resource-group RG --cluster-name CLUSTER --name POOL --node-count N`

---

## Cache for Redis

Three tiers:

- **Basic** — single node, no SLA.
- **Standard** — primary + replica.
- **Premium** — clustering, persistence, Redis modules, VNet support.
- **Enterprise / Enterprise Flash** — Redis Inc. tier with active geo-replication.

Pricing per cache size class (C0 / C1 / ... / C6 for Basic/Standard, P1 / ... / P5 for Premium).

---

## Azure OpenAI

### Deployment types

- **Standard** — pay-per-1k-tokens (most common).
- **Provisioned** — reserved throughput units (PTUs); priced per PTU-hour. For predictable, high-volume traffic.
- **Batch** — async, 50% cheaper than Standard, 24-hour SLA.

### Model regions

Azure OpenAI is regional and not all models are everywhere. Common patterns:

- GPT-4o / 4o-mini — most regions.
- o1 / o1-mini — limited regions.
- Whisper / TTS — limited regions.

Always confirm the model is available in the user's region before recommending.

### Comparison with alternatives

- **vs Bedrock** — Azure OpenAI is OpenAI-centric; Bedrock has Anthropic Claude, Meta Llama, Mistral, plus Amazon's own models. Pick by which model you need.
- **vs Vertex AI** — Vertex has Gemini, plus Anthropic Claude, plus Model Garden. Pick by ecosystem alignment.

---

## Storage tiers

Blob Storage tiers (per-GB-month, cheapest to most expensive):

- **Archive** — $0.001/GB; retrieval costs ~$0.02/GB and takes hours.
- **Cold** — $0.0036/GB; retrieval costs apply.
- **Cool** — $0.01/GB; minimum 30 days storage.
- **Hot** — $0.018/GB; default tier for active data.

Use lifecycle policies to auto-transition. Save real money for infrequent-access data.

---

## Networking model differences vs AWS

- **VNet** is regional (not global like GCP VPC).
- **Subnets** are zonal-by-association but the VNet itself is regional.
- **NSGs** (Network Security Groups) are like AWS Security Groups but stateful at subnet *or* NIC level.
- **Application Security Groups (ASGs)** are tag-based source/destination identifiers — useful for "only X tier can talk to Y tier".
- **Hub-and-spoke** is the standard topology — central hub VNet with peering to spoke VNets, often combined with **Azure Firewall** in the hub.

---

## Resource hierarchy

- **Tenant** (Microsoft Entra ID directory)
  - **Management group(s)**
    - **Subscription(s)**
      - **Resource group(s)**
        - **Resources**

Most operations are scoped to a resource group; cross-resource-group operations need explicit handling. This is dramatically different from AWS (account-scoped) and GCP (project-scoped).
