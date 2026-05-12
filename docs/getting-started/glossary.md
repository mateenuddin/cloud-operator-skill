# Glossary

Every acronym used in the skill, the references, and the operations catalog.

## A

- **A100 / H100** — NVIDIA datacenter GPUs. A100 is the workhorse for ML training (~80 GB HBM); H100 is the newest with FP8 support. Found in EC2 p4d/p5, GCE a2/a3, Azure ND.
- **ACI** — Azure Container Instances; serverless single-container compute.
- **ACM** — AWS Certificate Manager; TLS cert provisioning and rotation.
- **AD / Entra** — Microsoft directory service. AD is the on-prem service; **Entra ID** (formerly Azure AD) is the cloud directory.
- **AKS** — Azure Kubernetes Service.
- **AlloyDB** — GCP-built Postgres-compatible database, optimized for analytical workloads.
- **APIM** — Azure API Management.
- **ARM** (Azure) — Azure Resource Manager, the control plane for all Azure resources.
- **ARM** (CPU) — Architecture used by AWS Graviton (`*g` families) and GCP Tau T2A — typically ~20% cheaper for compatible workloads.
- **Aurora** — AWS-built Postgres / MySQL with separated storage layer.
- **AZ** — Availability Zone (AWS / Azure).

## B

- **Bedrock** — AWS managed access to foundation models (Anthropic Claude, Llama, Mistral, Amazon's own).
- **Bicep** — Azure's declarative IaC language, transpiles to ARM JSON.
- **Blob** — Azure object storage equivalent of S3.
- **BYOL** — Bring Your Own License (e.g., RDS Oracle BYOL is much cheaper than license-included).

## C

- **CDN** — Content Delivery Network (CloudFront on AWS, Cloud CDN on GCP, Azure CDN / Front Door on Azure).
- **CDK** — AWS Cloud Development Kit, code-defined IaC that synthesizes to CloudFormation.
- **CloudWatch** — AWS metrics, logs, alarms.
- **Cosmos DB** — Azure multi-API NoSQL (SQL / MongoDB / Cassandra / Gremlin / Table).
- **CSPM / CWPP** — Cloud Security Posture Management / Cloud Workload Protection Platform. Defender for Cloud does both.
- **CUD** — Committed Use Discount (GCP). 1- or 3-year commitment, resource-based or spend-based.

## D

- **Datadog** — Third-party observability platform. Wraps multi-cloud telemetry.
- **DBU** — Databricks Unit (Databricks pricing).
- **Dedicated tenancy** (AWS) — instance isolation; dramatically more expensive than default.
- **Direct Connect / ExpressRoute / Cloud Interconnect** — Dedicated private networking from on-prem to AWS / Azure / GCP respectively.
- **DLP** — Data Loss Prevention.
- **DR** — Disaster Recovery.
- **DTU** — Database Transaction Unit (legacy Azure SQL DB pricing). vCore is the modern replacement.
- **DWU** — Data Warehouse Unit (Synapse dedicated SQL pool pricing).

## E

- **EBS** — Elastic Block Store (AWS). Per-GB-month, paid separately from EC2 compute.
- **EC2** — Elastic Compute Cloud. AWS's foundational VM service.
- **ECS / EKS / Fargate** — Elastic Container Service / Kubernetes Service / serverless container runtime underneath.
- **EFS / FSx** — Elastic File System (NFS) / managed Windows / NetApp / Lustre.
- **EventBridge** — AWS event bus.

## F

- **Fargate** — AWS serverless container compute (used by ECS and EKS).
- **FinOps** — Financial Operations. The discipline of cloud cost management.
- **FPGA** — Field-Programmable Gate Array. AWS f1/f2 family.

## G

- **gp3 / gp2** — EBS general-purpose SSD volume types. gp3 is newer and cheaper.
- **Granite Rapids** — Intel Xeon, powers AWS c8i / m8i / r8i.
- **Graviton** — AWS's ARM CPU. Suffix `g` in family name (e.g., `m7g`).
- **GuardDuty** — AWS managed threat detection.

## H

- **HSM** — Hardware Security Module. Backing for KMS / Key Vault keys.
- **HPC** — High Performance Computing.

## I

- **IaC** — Infrastructure as Code (Terraform, CloudFormation, Bicep, Deployment Manager).
- **IAM** — Identity and Access Management.
- **IAP** — Identity-Aware Proxy (GCP). Zero-trust access to apps and SSH/RDP.
- **iops** — Input/Output Operations Per Second. EBS / Persistent Disk billing dimension.

## K

- **K8s** — Kubernetes.
- **KMS** — Key Management Service.
- **KQL** — Kusto Query Language. Used by Azure Monitor logs, Sentinel, Application Insights, Resource Graph.

## L

- **L4 / L40S** — NVIDIA GPUs targeted at inference. EC2 g6 / g6e have them.
- **Lambda** — AWS serverless functions.
- **LB** — Load Balancer.

## M

- **MCP** — Model Context Protocol. The standard for connecting Claude to external tools and data sources.
- **MFA** — Multi-Factor Authentication.
- **MSK** — Managed Streaming for Kafka (AWS).

## N

- **NAT** — Network Address Translation.
- **NSG / ASG** — Network Security Group / Application Security Group (Azure).
- **NUMA** — Non-Uniform Memory Access (CPU architecture).

## O

- **OAuth** — Authorization framework, used widely for SSO.
- **OD** — On-demand (pricing).
- **OLTP / OLAP** — Online Transaction Processing / Online Analytical Processing.

## P

- **PaaS** — Platform as a Service.
- **PD** — Persistent Disk (GCP).
- **PII** — Personally Identifiable Information.
- **PIM** — Privileged Identity Management (Microsoft Entra).
- **POD** — Kubernetes Pod.
- **PostgreSQL / Postgres** — open-source relational DB. RDS / Cloud SQL / Azure DB for Postgres all manage it.
- **PTU** — Provisioned Throughput Unit (Azure OpenAI).

## R

- **RAG** — Retrieval-Augmented Generation. Vector DB + LLM pattern.
- **RBAC** — Role-Based Access Control.
- **RDS** — Relational Database Service (AWS).
- **RG** — Resource Group (Azure).
- **RI** — Reserved Instance. Older AWS commitment mechanism; Savings Plans replace it for most cases.
- **RU** — Request Unit (Cosmos DB billing dimension).

## S

- **S3** — Simple Storage Service (AWS object storage).
- **SaaS** — Software as a Service.
- **SAML** — Security Assertion Markup Language. Federation protocol.
- **SCC** — Security Command Center (GCP).
- **SCP** — Service Control Policy (AWS Organizations).
- **SDK** — Software Development Kit.
- **SES** — Simple Email Service (AWS).
- **SG** — Security Group.
- **SLO** — Service Level Objective.
- **SMB** — Server Message Block (Windows file sharing protocol).
- **SNS / SQS** — Simple Notification Service (pub/sub) / Simple Queue Service.
- **Spanner** — GCP globally consistent SQL DB.
- **Spot** — Discounted preemptible compute (AWS Spot, GCP Spot, Azure Spot).
- **SP** — Savings Plan (AWS or Azure flexible commitment).
- **SSE** — Server-Side Encryption.
- **SSO** — Single Sign-On.
- **SSM** — Systems Manager (AWS).
- **STS** — Security Token Service (AWS).
- **SUD** — Sustained Use Discount (GCP). Auto-applies above usage thresholds.
- **Synapse** — Azure unified analytics platform.

## T

- **TEE** — Trusted Execution Environment. Foundation for Confidential Computing.
- **Terraform** — Cross-cloud IaC tool by HashiCorp.
- **TLS / SSL** — Transport Layer Security.

## V

- **vCore / vCPU** — virtual core / virtual CPU. Azure SQL DB vCore-based pricing model; EC2 vCPU count.
- **Vertex AI** — GCP's ML platform and foundation-model umbrella.
- **VNet** — Virtual Network (Azure equivalent of VPC).
- **VPC** — Virtual Private Cloud.
- **VPN** — Virtual Private Network.

## W

- **WAF** — Web Application Firewall.
