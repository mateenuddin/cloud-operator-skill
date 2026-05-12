# MCP Availability Map

Which MCPs cover which (cloud × capability) cells. Use this **before** promising the user you can act — if the cell shows "runbook only," produce a runbook rather than pretending to mutate.

This file is a snapshot. New MCPs get registered regularly; if a tool you expect to be available isn't listed, search the registry to confirm.

---

## Quick legend

- ✅ **Connected today** — the MCP is wired into the current session and tools work directly.
- 🟡 **In registry, not connected** — exists in the Cowork MCP registry; can be connected via the connector menu.
- 🟦 **Upstream available** — published by AWS Labs / Microsoft / community; would need plugin install (not one-click in Cowork).
- ❌ **No known MCP** — runbook output is the only path; or you'd need to wrap the SDK in a custom MCP.

---

## (Cloud × Capability) matrix

| Capability | AWS | GCP | Azure |
| --- | --- | --- | --- |
| **Pricing & specs** (compute, db, cache, search, warehouse) | ✅ Vantage `mcp__39ccd53b-...` | ✅ Vantage | ✅ Vantage |
| **Cost actuals** (Cost Explorer, billing export, cost mgmt) | 🟦 AWS Labs cost-explorer-mcp | 🟡 BigQuery MCP (run SQL on billing export) | 🟦 Azure MCP Server (Cost Mgmt) |
| **Compute lifecycle** (VMs / instances) | 🟦 AWS Labs ec2-mcp | 🟡 Google Compute Engine MCP | 🟦 Azure MCP Server |
| **Container orchestration** (ECS / GKE / AKS) | 🟦 AWS Labs ecs / eks | 🟦 community gke-mcp | 🟦 Azure MCP Server (AKS) |
| **Serverless functions** | 🟦 AWS Labs lambda-mcp | 🟦 community cloud-functions / cloud-run | 🟦 Azure MCP Server (Functions) |
| **Object storage** | 🟦 AWS Labs s3-mcp | 🟦 community gcs-mcp | 🟦 Azure MCP Server (Storage) |
| **Relational DB** (RDS / Cloud SQL / SQL Database) | 🟦 AWS Labs rds-mcp (read-only) | 🟦 community | 🟦 Azure MCP Server |
| **NoSQL DB** (DynamoDB / Firestore / Cosmos DB) | 🟦 AWS Labs dynamodb-mcp | 🟦 community firestore-mcp | 🟦 Azure MCP Server (Cosmos) |
| **Data warehouse** (Redshift / BigQuery / Synapse) | 🟦 AWS Labs redshift-mcp | ✅ Google Cloud BigQuery MCP (when connected) | 🟦 Azure MCP Server (Synapse) |
| **Identity & access** (IAM, RBAC, Entra) | 🟦 AWS Labs iam-mcp | 🟦 community gcp-iam-mcp | 🟦 Azure MCP Server / Microsoft Graph |
| **Secrets & keys** (KMS / Secrets Mgr / Key Vault) | 🟦 AWS Labs kms / secretsmgr | 🟦 community | 🟦 Azure MCP Server (Key Vault) |
| **Observability** (metrics, logs, traces) | 🟦 AWS Labs cloudwatch-mcp | 🟦 community cloud-monitoring / logging | 🟦 Azure MCP Server (Monitor) |
| **IaC** (CloudFormation / Bicep / Terraform / DM) | 🟦 AWS Labs cfn-mcp | 🟦 community | 🟦 Azure MCP Server (ARM/Bicep) |
| **AI inference** (Bedrock / Vertex / Azure OpenAI) | 🟦 AWS Labs bedrock-mcp | 🟦 community vertex-mcp | 🟦 Azure OpenAI MCP |
| **Marketplace / procurement** | 🟡 AWS Marketplace MCP | ❌ | ❌ |

### Cross-cloud third-party MCPs that help

- **Datadog** 🟡 — multi-cloud observability proxy (logs, metrics, traces, monitors). One MCP, all three clouds. Useful when the user has a Datadog account.
- **Grafana Cloud** 🟦 — similar to Datadog but Grafana-flavored.
- **Snowflake / Databricks** 🟦 — when the user's analytical data is there, not in BigQuery / Redshift / Synapse.

---

## How to use this map

When the user asks for an action, walk these steps:

1. **Look up the (cloud × capability) cell.**
2. If ✅ → use the MCP directly.
3. If 🟡 → ask the user *"This needs MCP X which is in your registry but not connected. Want to connect it, or shall I produce a runbook?"* and act on their answer.
4. If 🟦 → tell the user *"There's a public MCP for this (AWS Labs / Microsoft / community) that you'd need to install. In the meantime, here's the runbook."* and produce one.
5. If ❌ → produce a runbook directly with a brief note that no MCP exists for this today.

Never invent an MCP server name or assume one is connected. If you're unsure, call `list_connectors` (or `search_mcp_registry` if even the registry status is in question) to confirm before acting.

---

## Suggesting connections

If a 🟡 MCP would unblock the user's work, you can call the `suggest_connectors` tool with the directoryUuid to render an in-chat connect card. Don't do this every time — only when the user has indicated they'd like to act and the unwired MCP is the obvious next step.

Known UUIDs at the time of this snapshot:

- Vantage `instances`: `39ccd53b-73e2-463a-8f4f-10062e5da508` (already connected)
- Google Compute Engine: `3afecfe4-46be-4f31-9050-9b8a67909028`
- Google Cloud BigQuery: `7c316b77-98a0-4dbb-8b54-a96ae26a884f`
- AWS Marketplace: `2ed43e1e-f547-48a3-85cc-b9baa412d06b`
- Datadog: `68268024-1a91-4316-a9e1-14ecb814cb18`
- Microsoft Learn (docs only, not management): `89a7ddf5-2a6b-410c-be11-aa0e1a1b35a6`

(These UUIDs are stable per registry but verify via `search_mcp_registry` if a connect attempt fails.)
