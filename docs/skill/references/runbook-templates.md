# Runbook Templates

When no MCP is wired to perform an action, produce a runbook the user can execute. These templates cover the most common cases. Each template lists *verified* CLI / SDK / IaC syntax. Avoid inventing flags — if a flag isn't in this file or the official docs, prefer to omit it and let the user supply context.

The right runbook format depends on what the user values:

- **CLI snippet** — fastest to execute; good for one-off operations.
- **Terraform** — declarative, cross-cloud, idempotent; good for infrastructure changes the user wants reviewable.
- **Cloud-native IaC** — CloudFormation / Bicep / Deployment Manager — when the user has tooling already standardized on the native option.
- **SDK script** — Python / Node — when the operation has logic (loops, conditional branching) that doesn't map cleanly to CLI.

Default to **CLI** unless the request implies repeated infrastructure (then Terraform).

---

## AWS

### List EC2 instances with filters

```bash
# CLI
aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:env,Values=dev" "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId, InstanceType, State.Name, Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

### Stop a set of EC2 instances

```bash
# CLI — stop all dev instances
INSTANCE_IDS=$(aws ec2 describe-instances \
  --region us-east-1 \
  --filters "Name=tag:env,Values=dev" "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' --output text)

aws ec2 stop-instances --region us-east-1 --instance-ids $INSTANCE_IDS
```

### Cost Explorer — last 7 days by service

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d '7 days ago' '+%Y-%m-%d'),End=$(date -u '+%Y-%m-%d') \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Provision an EC2 instance (Terraform)

```hcl
resource "aws_instance" "web" {
  ami                    = "ami-0c7217cdde317cfec"  # Amazon Linux 2023 in us-east-1
  instance_type          = "m7i.xlarge"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  tags = {
    Name = "web-1"
    env  = "prod"
  }
}
```

### CloudWatch — fetch a metric

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0123456789abcdef0 \
  --start-time $(date -u -d '24 hours ago' '+%Y-%m-%dT%H:%M:%SZ') \
  --end-time $(date -u '+%Y-%m-%dT%H:%M:%SZ') \
  --period 300 \
  --statistics Average Maximum
```

### Logs Insights query

```bash
aws logs start-query \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' '+%s') \
  --end-time $(date -u '+%s') \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'

# then poll get-query-results with the returned queryId
```

---

## GCP

### List Compute Engine instances

```bash
gcloud compute instances list \
  --project=YOUR_PROJECT \
  --filter="zone:(us-central1-a us-central1-b) AND status=RUNNING" \
  --format="table(name,zone.basename(),machineType.basename(),status,networkInterfaces[0].networkIP)"
```

### Stop and resize an instance

```bash
# Stop
gcloud compute instances stop INSTANCE_NAME --zone=us-central1-a

# Resize (must be stopped)
gcloud compute instances set-machine-type INSTANCE_NAME \
  --machine-type=n2-standard-8 --zone=us-central1-a

# Restart
gcloud compute instances start INSTANCE_NAME --zone=us-central1-a
```

### BigQuery — billing export query (top 10 services last 30 days)

```sql
-- run via BigQuery MCP if connected, or via `bq query --use_legacy_sql=false`
SELECT
  service.description AS service,
  SUM(cost) AS total_cost
FROM
  `YOUR_PROJECT.billing_export.gcp_billing_export_resource_v1_*`
WHERE
  _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

### Provision a GCE instance (Terraform)

```hcl
resource "google_compute_instance" "web" {
  name         = "web-1"
  machine_type = "n2-standard-4"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 50
    }
  }
  network_interface {
    network    = "default"
    access_config {}
  }
  labels = { env = "prod" }
}
```

### Cloud Monitoring — query a metric (gcloud)

```bash
gcloud monitoring time-series list \
  --filter='metric.type="compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_id="1234567890123456789"' \
  --interval-start-time=$(date -u -d '24 hours ago' '+%Y-%m-%dT%H:%M:%SZ') \
  --interval-end-time=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
```

---

## Azure

### List VMs with power state

```bash
az vm list -d -o table --query "[].{Name:name, RG:resourceGroup, Size:hardwareProfile.vmSize, State:powerState, Region:location}"
```

### Deallocate a set of VMs

```bash
# Deallocate (stops billing — `az vm stop` keeps it)
for vm in $(az vm list -d --query "[?tags.env=='dev' && powerState=='VM running'].name" -o tsv); do
  az vm deallocate --resource-group MY_RG --name $vm --no-wait
done
```

### Cost Management — query (last 7 days, by resource group)

```bash
az costmanagement query \
  --type ActualCost \
  --timeframe Custom \
  --time-period from=$(date -u -d '7 days ago' '+%Y-%m-%dT%H:%M:%SZ') to=$(date -u '+%Y-%m-%dT%H:%M:%SZ') \
  --dataset-aggregation '{"totalCost": {"name":"Cost","function":"Sum"}}' \
  --dataset-grouping '[{"type":"Dimension","name":"ResourceGroup"}]' \
  --scope "/subscriptions/$SUBSCRIPTION_ID"
```

### Resource Graph — search resources

```bash
# Find all VMs in production tag, missing diagnostic settings
az graph query -q "
Resources
| where type == 'microsoft.compute/virtualmachines'
| where tags.env == 'prod'
| project id, name, resourceGroup, location
"
```

### Provision a VM (Bicep)

```bicep
param adminUsername string = 'azureuser'
@secure()
param adminPassword string

resource nic 'Microsoft.Network/networkInterfaces@2024-01-01' = {
  name: 'nic-web-1'
  location: resourceGroup().location
  properties: {
    ipConfigurations: [
      { name: 'ipconfig1'
        properties: {
          subnet: { id: subnet.id }
          privateIPAllocationMethod: 'Dynamic'
        }
      }
    ]
  }
}

resource vm 'Microsoft.Compute/virtualMachines@2024-07-01' = {
  name: 'web-1'
  location: resourceGroup().location
  properties: {
    hardwareProfile: { vmSize: 'Standard_D8s_v5' }
    osProfile: { computerName: 'web1', adminUsername: adminUsername, adminPassword: adminPassword }
    storageProfile: {
      imageReference: { publisher: 'Canonical', offer: 'ubuntu-24_04-lts', sku: 'server', version: 'latest' }
      osDisk: { createOption: 'FromImage', managedDisk: { storageAccountType: 'Premium_LRS' } }
    }
    networkProfile: { networkInterfaces: [ { id: nic.id } ] }
  }
}
```

Deploy:

```bash
az deployment group create \
  --resource-group MY_RG \
  --template-file vm.bicep \
  --parameters adminPassword=...
```

### Azure Monitor — log query (KQL)

```bash
az monitor log-analytics query \
  -w "$WORKSPACE_ID" \
  --analytics-query "AzureDiagnostics
| where TimeGenerated > ago(1h)
| where Category == 'NetworkSecurityGroupRuleCounter'
| summarize count() by ruleName_s
| order by count_ desc"
```

---

## Cross-cloud Terraform pattern (one config, three providers)

When user wants the same workload across clouds for comparison or hybrid:

```hcl
terraform {
  required_providers {
    aws    = { source = "hashicorp/aws",    version = "~> 5.0" }
    google = { source = "hashicorp/google", version = "~> 5.0" }
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
  }
}

provider "aws"     { region = "us-east-1" }
provider "google"  { project = var.gcp_project; region = "us-central1" }
provider "azurerm" { features {} }

# resources defined in per-cloud modules:
module "aws_workload"   { source = "./modules/aws" }
module "gcp_workload"   { source = "./modules/gcp" }
module "azure_workload" { source = "./modules/azure" }
```

This is heavier than picking one cloud, but makes side-by-side cost / latency comparison reproducible.

---

## When NOT to produce a runbook

- The user is asking a *question* ("what's the cheapest X?") — answer with data + recommendation, not a script.
- The runbook would just be a single `aws <service> describe-*` you could call via Vantage or another wired MCP.
- The action is destructive and the user hasn't explicitly confirmed (terminate, delete, drop-table, etc.).
- The user's intent is unclear — ask once before producing a multi-step runbook that might solve the wrong problem.
