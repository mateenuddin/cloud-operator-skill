# Cloud Operator Toolset — AWS / GCP / Azure

A capability-organized catalog of services a cloud operator agent can drive across the three major providers. Each entry includes a one-line "what it does" summary. Use this as the menu of operations to expose to an operator agent.

---

## AWS

### Pricing, Billing & Cost Optimization

- **AWS Pricing API** — Programmatic price lists for every AWS SKU and region.
- **AWS Cost Explorer** — Visualize and forecast spend; query historical cost and usage.
- **AWS Cost & Usage Reports (CUR)** — Hourly granularity cost data exported to S3 for warehouse analysis.
- **AWS Budgets** — Set thresholds; alert or auto-take action when spend or usage drifts.
- **AWS Cost Anomaly Detection** — ML-based detection of unexpected spend spikes.
- **AWS Compute Optimizer** — Right-sizing recommendations for EC2, Lambda, EBS, RDS.
- **AWS Trusted Advisor** — Cross-account checks for cost, security, fault tolerance, performance.
- **Savings Plans / Reserved Instances API** — Purchase, modify, and inspect commitment-based discounts.
- **AWS Marketplace Metering** — Track third-party SaaS spend that bills through AWS.

### Compute

- **EC2** — Virtual machines; the foundational compute primitive.
- **Lambda** — Serverless function execution, event-driven.
- **ECS** — Container orchestration on AWS-managed cluster (with Fargate or EC2 capacity).
- **EKS** — Managed Kubernetes control plane; you bring nodes or use Fargate.
- **Fargate** — Serverless container execution layer underneath ECS/EKS.
- **AWS Batch** — Managed queue + execution for batch jobs at scale.
- **Lightsail** — Pre-priced bundled VMs, simpler than EC2.
- **App Runner** — Source-to-URL container service with autoscaling.
- **Elastic Beanstalk** — Managed application platform on EC2.

### Storage

- **S3** — Object storage; the backbone for nearly every AWS architecture.
- **EBS** — Block storage volumes attached to EC2.
- **EFS** — NFS-compatible elastic file shares.
- **FSx** — Managed Windows / NetApp / OpenZFS / Lustre file systems.
- **Storage Gateway** — Hybrid bridge from on-prem storage to AWS.
- **S3 Glacier** — Cold-tier archival storage with retrieval delays.
- **AWS Backup** — Centralized backup orchestration across services.

### Database

- **RDS** — Managed Postgres, MySQL, MariaDB, Oracle, SQL Server.
- **Aurora** — AWS-native cloud-optimized Postgres / MySQL with separated storage.
- **DynamoDB** — Managed wide-column/key-value NoSQL with global tables.
- **ElastiCache** — Managed Redis or Memcached.
- **Redshift** — Petabyte-scale columnar data warehouse.
- **DocumentDB** — MongoDB-compatible document store.
- **Neptune** — Managed graph database (Gremlin / SPARQL).
- **Timestream** — Time-series database optimized for IoT / metrics.
- **Keyspaces** — Managed Cassandra-compatible store.
- **MemoryDB** — Redis-compatible durable in-memory database.

### Networking & Edge

- **VPC** — Isolated virtual network with subnets, route tables, peering.
- **Route 53** — Managed DNS with health checks and latency routing.
- **CloudFront** — Global CDN with edge functions (Lambda@Edge).
- **API Gateway** — REST/HTTP/WebSocket API frontends.
- **Elastic Load Balancing (ALB / NLB / GWLB)** — L4/L7 load balancing.
- **Direct Connect** — Dedicated line from on-prem to AWS.
- **Transit Gateway** — Hub for connecting VPCs and on-prem at scale.
- **Global Accelerator** — Anycast static IPs for global TCP/UDP traffic.
- **PrivateLink** — Private endpoints for cross-account / cross-VPC service access.

### Identity, Access & Security

- **IAM** — Users, roles, policies; the access control core.
- **AWS Organizations** — Multi-account hierarchy, SCPs, consolidated billing.
- **IAM Identity Center (SSO)** — SSO across accounts and external apps.
- **KMS** — Managed encryption keys with HSM backing.
- **Secrets Manager** — Rotated credential storage.
- **Cognito** — End-user identity for apps (sign-in, federation).
- **GuardDuty** — Threat detection from VPC flow / DNS / CloudTrail.
- **Macie** — PII / sensitive data discovery in S3.
- **WAF** — Web application firewall in front of CloudFront / ALB / API GW.
- **Shield** — DDoS protection (Advanced for sophisticated attacks).
- **Security Hub** — Aggregator and finding view across security services.
- **Inspector** — Vulnerability scanning for EC2, ECR images, Lambda.
- **Detective** — Investigative graph for security findings.
- **Certificate Manager (ACM)** — TLS cert provisioning and rotation.

### Management, Governance & DevOps

- **CloudFormation** — Declarative IaC stacks with rollback and drift detection.
- **AWS CDK** — Code-defined IaC, synthesizes to CloudFormation.
- **Systems Manager (SSM)** — Patch, run-command, parameter store, session manager, automation.
- **AWS Config** — Resource inventory + compliance rules + change history.
- **CloudTrail** — API audit log for every AWS account action.
- **Service Catalog** — Curated approved IaC products for end users.
- **Control Tower** — Multi-account landing zone with guardrails.
- **AWS Resource Explorer** — Cross-region/account search across resources.
- **CodeCommit / CodeBuild / CodeDeploy / CodePipeline / CodeArtifact** — Git, build, deploy, pipeline, package mgmt.
- **CloudShell** — Browser shell with credentials pre-loaded.

### Observability & Operations

- **CloudWatch** — Metrics, logs, dashboards, alarms.
- **CloudWatch Logs Insights** — Query language over log streams.
- **X-Ray** — Distributed tracing for services and Lambdas.
- **Amazon Managed Grafana / Prometheus** — Open-source observability managed.
- **EventBridge** — Event bus with schemas, partner sources, rules.
- **Health Dashboard / Health API** — Account-specific service health and operational issues.

### Analytics & Streaming

- **Athena** — Serverless SQL over S3.
- **Glue** — ETL, data catalog, schema discovery.
- **EMR** — Managed Hadoop / Spark / Presto clusters.
- **Kinesis (Data Streams / Firehose / Analytics)** — Real-time streaming pipeline.
- **MSK** — Managed Kafka.
- **OpenSearch Service** — Managed search/log analytics (formerly Elasticsearch).
- **Lake Formation** — Lake permissions, blueprints, data sharing.
- **QuickSight** — BI dashboards and ML insights.
- **DataZone** — Data catalog and governance for cross-team sharing.

### Machine Learning & AI

- **SageMaker** — Build, train, host ML models end-to-end.
- **Bedrock** — Managed access to foundation models (Anthropic Claude, Llama, etc.).
- **Comprehend / Rekognition / Translate / Transcribe / Polly / Textract** — Pre-built AI APIs (NLP, vision, speech, OCR).
- **Q (Developer / Business)** — AI assistant for builders and business users.
- **Personalize / Forecast / Lex / Kendra** — Domain-specific ML services (recs, forecasting, chatbots, search).

### Integration / Workflow

- **SNS** — Pub/sub topics with email/SMS/push fanout.
- **SQS** — Decoupled message queues (standard / FIFO).
- **Step Functions** — Visual workflow orchestrator with state machines.
- **AppFlow** — Managed SaaS-to-AWS data movement.
- **MQ** — Managed RabbitMQ / ActiveMQ.
- **EventBridge Pipes / Scheduler** — Point-to-point event routing and cron-like scheduling.

---

## GCP

### Pricing, Billing & Cost Optimization

- **Cloud Billing API** — Programmatic access to billing accounts, invoices, budgets.
- **BigQuery Billing Export** — Stream detailed usage costs to BigQuery for SQL analysis.
- **Pricing Calculator** — Estimate workload cost ahead of provisioning.
- **Cloud Billing Budgets** — Threshold alerts on actual or forecast spend.
- **Active Assist (Recommender)** — ML-driven cost / security / performance recommendations.
- **Committed Use Discounts (CUDs) / Sustained Use Discounts** — Commitment and automatic discount mechanics.
- **Carbon Footprint** — Per-project / per-service emissions reporting.

### Compute

- **Compute Engine** — Virtual machines, the foundational primitive.
- **Cloud Run** — Stateless container service with autoscaling to zero.
- **Cloud Run Functions / Cloud Functions** — Event-driven serverless functions.
- **GKE (Standard + Autopilot)** — Managed Kubernetes (Autopilot is fully managed nodes).
- **App Engine (Standard / Flexible)** — Managed application platform.
- **Cloud Batch** — Managed batch processing (analogous to AWS Batch).
- **Bare Metal Solution** — Dedicated hardware (often for Oracle / SAP).
- **Cloud Workstations** — Browser-accessible developer VMs.

### Storage

- **Cloud Storage** — Object storage with multi-region / nearline / coldline tiers.
- **Persistent Disk / Hyperdisk** — Block storage attached to GCE / GKE.
- **Filestore** — Managed NFS file shares.
- **Cloud Storage Transfer Service** — Bulk moves between cloud or on-prem.
- **NetApp Volumes** — Managed NetApp NFS / SMB.
- **Backup and DR** — Snapshot, backup, replication for VMs, DBs, Filestore.

### Database

- **Cloud SQL** — Managed Postgres, MySQL, SQL Server.
- **AlloyDB** — Postgres-compatible, GCP-native warehouse-grade DB.
- **Spanner** — Globally distributed strongly consistent SQL.
- **Firestore** — Document database with real-time sync.
- **Bigtable** — Wide-column NoSQL for time-series / IoT.
- **Memorystore** — Managed Redis / Memcached.
- **BigQuery** — Serverless data warehouse, also serves as a database for analytics.
- **Datastream** — CDC replication into BigQuery / Spanner.

### Networking & Edge

- **VPC** — Global virtual network spanning regions.
- **Cloud Load Balancing** — Global L4/L7 LB tiers (HTTPS, TCP, UDP, SSL Proxy).
- **Cloud CDN** — Edge caching tied to Cloud Load Balancing.
- **Cloud DNS** — Managed authoritative DNS with private zones.
- **Cloud Interconnect / VPN** — Private and IPsec connectivity to on-prem.
- **Cloud NAT** — Egress NAT for private subnets.
- **Cloud Armor** — DDoS protection and WAF.
- **Network Connectivity Center** — Hub-and-spoke for global connectivity.
- **Service Directory** — Service registry across networks.

### Identity, Access & Security

- **Cloud IAM** — Roles and policies; the access control core.
- **Resource Manager** — Org / folder / project hierarchy.
- **Cloud Identity** — Workforce identity (free / paid tiers).
- **Identity-Aware Proxy (IAP)** — Zero-trust access to apps and SSH/RDP.
- **Cloud KMS / Cloud HSM / Cloud External Key Manager** — Key management options.
- **Secret Manager** — Versioned secret storage.
- **Identity Platform** — End-user identity (CIAM).
- **Security Command Center** — Findings aggregator across security tools.
- **Cloud Armor** — WAF + DDoS (also listed under networking).
- **Confidential Computing** — TEE-protected VMs.
- **Certificate Manager / Certificate Authority Service** — TLS certs and private CA.
- **Binary Authorization** — Signed-image enforcement for GKE / Cloud Run.

### Management, Governance & DevOps

- **Resource Manager** — Org tree, projects, folders.
- **Deployment Manager** — Native IaC (legacy; many use Terraform / Config Connector).
- **Config Connector** — Manage GCP resources via Kubernetes CRDs.
- **Cloud Asset Inventory** — Search and audit every resource and policy.
- **Cloud Build** — CI/CD service with private worker pools.
- **Cloud Deploy** — Managed continuous delivery for GKE / Cloud Run.
- **Artifact Registry** — Container and language package registry.
- **Cloud Source Repositories** — Managed Git.
- **Organization Policy** — Constraint-based guardrails across the org.
- **Service Usage** — Enable/disable APIs per project.
- **Cloud Shell** — Browser shell with credentials pre-loaded.

### Observability & Operations

- **Cloud Monitoring** — Metrics, dashboards, alerting.
- **Cloud Logging** — Log aggregation, query, export to BigQuery / Pub/Sub.
- **Cloud Trace** — Distributed tracing.
- **Cloud Profiler** — Continuous CPU/heap profiling.
- **Error Reporting** — Aggregated production error tracker.
- **Cloud Debugger / Snapshot** — Production debug capture.
- **Personalized Service Health** — Per-project service incident view.

### Analytics & Streaming

- **BigQuery** — Serverless data warehouse with ML and BI built-in.
- **Dataflow** — Managed Apache Beam streaming + batch.
- **Dataproc** — Managed Hadoop / Spark.
- **Pub/Sub** — Global messaging at scale.
- **Pub/Sub Lite** — Cheaper regional Pub/Sub variant.
- **Looker / Looker Studio** — BI and embedded analytics.
- **Data Fusion** — Visual data integration on top of CDAP.
- **Dataplex** — Data fabric and governance over distributed lakes.
- **Analytics Hub** — Curated dataset exchange.

### Machine Learning & AI

- **Vertex AI** — End-to-end ML platform (training, registry, endpoints).
- **Vertex AI Model Garden / Gemini API** — Managed access to Google's foundation models.
- **AutoML** — No-code training for vision / language / tabular.
- **Document AI** — OCR + structured doc parsing.
- **Speech-to-Text / Text-to-Speech / Translation** — Pre-built APIs.
- **Vision AI / Video AI** — Image and video understanding APIs.
- **Contact Center AI / Dialogflow** — Conversational AI.
- **Natural Language API** — Sentiment, entities, syntax extraction.

### Integration / Workflow

- **Pub/Sub** — Global pub-sub messaging (also under analytics).
- **Cloud Tasks** — Asynchronous task execution with retries.
- **Workflows** — Serverless YAML-based workflow orchestrator.
- **Eventarc** — Event routing across GCP services and to Cloud Run.
- **Cloud Scheduler** — Managed cron service.
- **Application Integration / Apigee** — Enterprise integration and API management.

---

## Azure

### Pricing, Billing & Cost Optimization

- **Microsoft Cost Management + Billing** — View, analyze, allocate cost; budgets and exports.
- **Azure Pricing Calculator** — Estimate workload cost before provisioning.
- **Azure Advisor** — Cost / security / reliability / operational recommendations.
- **Reservations / Savings Plans for Compute** — Commitment discount mechanics.
- **Azure Hybrid Benefit** — Use existing on-prem licenses for cloud discounts.
- **Cost Anomaly (preview)** — ML-based spend anomaly detection.
- **Carbon Optimization** — Emissions reporting per subscription / service.

### Compute

- **Virtual Machines** — Foundational IaaS compute.
- **Virtual Machine Scale Sets** — Auto-scaled identical VMs.
- **Azure Functions** — Serverless functions, event-driven.
- **App Service** — Managed web app / API hosting.
- **AKS (Azure Kubernetes Service)** — Managed Kubernetes.
- **Container Instances (ACI)** — Single-container serverless compute.
- **Container Apps** — Serverless Kubernetes-backed services and microservices.
- **Azure Batch** — HPC / batch workloads.
- **Azure Spot VMs** — Discounted preemptible capacity.
- **Service Fabric** — Microservice runtime (legacy but supported).

### Storage

- **Blob Storage** — Object storage; hot / cool / cold / archive tiers.
- **Azure Files** — SMB / NFS managed file shares.
- **Disk Storage** — Managed block disks for VMs.
- **NetApp Files** — Enterprise NAS (NFS / SMB).
- **Data Lake Storage Gen2** — Hierarchical namespace on top of Blob for analytics.
- **Azure Backup / Site Recovery** — Backup orchestration and DR.
- **Storage Mover / Data Box** — Online and offline migration tooling.

### Database

- **Azure SQL Database** — Managed SQL Server (single DB / elastic pool / managed instance).
- **Azure Database for PostgreSQL / MySQL / MariaDB** — Managed open-source RDBMS.
- **Cosmos DB** — Multi-model globally distributed DB (SQL, MongoDB, Cassandra, Gremlin, Table APIs).
- **Cache for Redis** — Managed Redis.
- **Synapse Analytics (dedicated SQL pool)** — Cloud data warehouse.
- **Azure Managed Instance for Apache Cassandra** — Cassandra control plane on user-owned VMs.

### Networking & Edge

- **Virtual Network (VNet)** — Isolated virtual network.
- **Azure Load Balancer / Application Gateway** — L4 and L7 load balancing.
- **Azure Front Door** — Global L7 entrypoint with WAF and CDN.
- **Azure CDN** — Edge content delivery.
- **ExpressRoute** — Dedicated private connectivity to Azure.
- **VPN Gateway** — Site-to-site / point-to-site IPsec.
- **Azure DNS / Private DNS** — Managed authoritative DNS.
- **Azure Firewall** — Stateful managed firewall.
- **Network Watcher** — Diagnostics, flow logs, packet capture.
- **Private Link** — Private endpoints to Azure PaaS services.

### Identity, Access & Security

- **Microsoft Entra ID** (formerly Azure AD) — Workforce and customer identity.
- **Microsoft Entra Permissions Management** — CIEM across multi-cloud.
- **Microsoft Entra ID External Identities (B2B / B2C)** — Federated guest and consumer identity.
- **Azure RBAC** — Role-based access for Azure resources.
- **Managed Identities** — Workload identity without secret management.
- **Key Vault** — Keys, secrets, certs.
- **Microsoft Defender for Cloud** — CSPM + CWPP across Azure / AWS / GCP.
- **Microsoft Sentinel** — SIEM and SOAR.
- **Azure Policy** — Policy-as-code guardrails.
- **Microsoft Purview** — Data governance, classification, lineage.
- **Confidential Computing** — TEE-backed VMs / containers.

### Management, Governance & DevOps

- **Azure Resource Manager (ARM)** — Control plane for all Azure resources.
- **Bicep / ARM Templates** — Native IaC syntaxes.
- **Azure Resource Graph** — Cross-subscription resource search via Kusto.
- **Azure Lighthouse** — Multi-tenant management for service providers.
- **Azure Blueprints / Landing Zones** — Govern initial subscription scaffolding.
- **Azure Automation** — Runbooks, configuration mgmt, update mgmt.
- **Azure Arc** — Bring on-prem / other-cloud resources under Azure control plane.
- **Azure DevOps (Boards / Repos / Pipelines / Artifacts / Test Plans)** — Full DevOps suite.
- **GitHub Actions for Azure** — CI/CD via GitHub.
- **Azure Cloud Shell** — Browser shell with credentials pre-loaded.

### Observability & Operations

- **Azure Monitor** — Unified observability surface.
- **Log Analytics** — KQL-based log query engine, backs Sentinel and others.
- **Application Insights** — APM for application telemetry.
- **Azure Service Health** — Per-subscription incident and maintenance view.
- **Managed Grafana / Managed Prometheus** — Open-source observability hosted.

### Analytics & Streaming

- **Synapse Analytics** — Unified analytics platform (SQL, Spark, pipelines).
- **Microsoft Fabric** — Unified data + AI platform with OneLake.
- **Data Factory** — Managed ETL / ELT.
- **Stream Analytics** — Real-time streaming SQL.
- **Event Hubs** — Kafka-compatible event ingestion at scale.
- **HDInsight** — Managed Hadoop / Spark / Kafka / HBase.
- **Databricks (Azure-native)** — Fully integrated Databricks.
- **Power BI** — BI dashboards.
- **Data Lake Analytics / Purview** — Lake compute and governance.

### Machine Learning & AI

- **Azure AI Foundry** — Unified umbrella for AI development on Azure.
- **Azure OpenAI Service** — Hosted OpenAI models with Azure controls.
- **Azure Machine Learning** — End-to-end ML platform.
- **AI Vision / Speech / Translator / Document Intelligence** — Pre-built AI APIs.
- **AI Search** (formerly Cognitive Search) — Hybrid search with vector and semantic ranking.
- **Bot Service** — Conversational AI hosting.

### Integration / Workflow

- **Service Bus** — Enterprise message broker (queues, topics, sessions).
- **Event Grid** — Event routing for Azure events and custom topics.
- **Logic Apps** — Visual no-code/low-code workflow orchestration.
- **API Management (APIM)** — Full API gateway and developer portal.
- **Azure Relay** — Hybrid connections for on-prem services.

---

## Cross-cutting capability map

| Capability | AWS | GCP | Azure |
| --- | --- | --- | --- |
| Cost discovery API | Pricing API | Cloud Billing API | Retail Prices API |
| Spend visualization | Cost Explorer | Billing in console + BQ export | Cost Management |
| Right-sizing recs | Compute Optimizer | Recommender / Active Assist | Advisor |
| Anomaly detection | Cost Anomaly Detection | (Recommender) | Cost Anomaly (preview) |
| IaC native | CloudFormation / CDK | Deployment Manager / Config Connector | ARM / Bicep |
| Resource search | Resource Explorer | Cloud Asset Inventory | Resource Graph |
| Audit log | CloudTrail | Cloud Audit Logs | Activity Log |
| Multi-account/project | Organizations | Resource Manager | Management Groups |
| Secrets | Secrets Manager | Secret Manager | Key Vault |
| Workload identity | IAM Roles for SA | Workload Identity | Managed Identities |
| Foundation models | Bedrock | Vertex AI / Gemini | Azure OpenAI / AI Foundry |
| Cloud-of-clouds posture | (Security Hub partial) | (SCC partial) | Defender for Cloud (multi-cloud native) |
