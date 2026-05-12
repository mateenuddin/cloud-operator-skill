# Cloud Operator Operations Catalog

Operation-level catalog for the five priority capability areas. Each row = a concrete API call an agent could invoke.

**MCP availability legend** (status reflects the Cowork MCP registry as scanned today):
- ✅ **Connected today** — wirable right now in this session
- 🟡 **Registry / upstream** — MCP exists in this registry or is published upstream (AWS Labs, Microsoft Azure MCP, etc.) but not connected
- ❌ **No known MCP** — would need a custom MCP wrapper around the SDK/CLI

References used for upstream MCPs: AWS Labs `awslabs/mcp` (EC2, S3, Lambda, IAM, CloudFormation, CloudWatch, Cost Explorer, Bedrock-KB, etc.); Microsoft Azure MCP Server (Resource Manager, Cosmos, Storage, Key Vault, AKS); community Google Cloud MCPs (BigQuery, Compute Engine, Cloud Run).

---

## 1. Pricing & Billing

The most important area for the existing skill. Vantage covers most of the *list pricing* surface. The *actual spend* surface (Cost Explorer, billing exports) needs separate MCPs.

### AWS

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_pricing_describe_services` | List all AWS services tracked in pricing | 🟡 AWS Labs cost-explorer MCP |
| `aws_pricing_get_attribute_values` | Get valid filter values per service (e.g. instanceType) | 🟡 AWS Labs |
| `aws_pricing_get_products` | Query SKU + price for any service | 🟡 AWS Labs (or use Vantage for compute/db) |
| `aws_ce_get_cost_and_usage` | Pull historical cost grouped by service/account/tag | 🟡 AWS Labs cost-explorer MCP |
| `aws_ce_get_cost_forecast` | Forecast next-N-day spend | 🟡 AWS Labs |
| `aws_ce_get_reservation_utilization` | RI utilization for past period | 🟡 AWS Labs |
| `aws_ce_get_savings_plans_utilization` | Savings Plans utilization | 🟡 AWS Labs |
| `aws_ce_get_anomalies` | Listed cost anomalies detected | 🟡 AWS Labs |
| `aws_budgets_describe_budgets` | List configured budgets | 🟡 AWS Labs |
| `aws_budgets_create_budget` | Create new budget threshold | 🟡 AWS Labs |
| `aws_compute_optimizer_get_ec2_recommendations` | Right-sizing recs for EC2 | 🟡 AWS Labs |
| `aws_compute_optimizer_get_ebs_recommendations` | Right-sizing recs for EBS | 🟡 AWS Labs |
| `aws_compute_optimizer_get_lambda_recommendations` | Right-sizing recs for Lambda | 🟡 AWS Labs |
| `aws_trustedadvisor_describe_checks` | All Trusted Advisor checks | ❌ |
| `aws_trustedadvisor_describe_check_result` | Result for one check | ❌ |
| `vantage_get_ec2_indexes` | Pre-filtered instance categories (RAM/vCPU/price/GPU) | ✅ Vantage (connected) |
| `vantage_use_ec2_index` | Instances matching an index | ✅ Vantage |
| `vantage_get_ec2_region_pricing` | Full pricing matrix for instance × region | ✅ Vantage |
| (same shape) `vantage_*_rds`, `*_elasticache`, `*_opensearch`, `*_redshift` | Same pattern for other AWS pillars | ✅ Vantage |

### GCP

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `gcp_billing_list_billing_accounts` | List billing accounts | ❌ |
| `gcp_billing_get_project_billing_info` | Which billing account a project bills to | ❌ |
| `gcp_billing_list_services` | All GCP services with pricing | ❌ |
| `gcp_billing_list_skus` | SKUs for a service (pricing tier rows) | ❌ |
| `gcp_billing_query_export_table` | SQL over BigQuery billing export | 🟡 BigQuery MCP (registered) |
| `gcp_billing_create_budget` | Create alert budget | ❌ |
| `gcp_recommender_list_recommendations` | Cost / security / perf / reliability recs | ❌ |
| `gcp_recommender_apply_recommendation` | Apply a recommendation | ❌ |
| `vantage_get_gcp_*` | Same pricing pattern as AWS for GCP compute | ✅ Vantage |

### Azure

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `azure_billing_list_billing_accounts` | Billing accounts visible | 🟡 Azure MCP Server |
| `azure_billing_query_costs` | Cost by subscription/resource group/tag | 🟡 Azure MCP Server |
| `azure_billing_get_invoice` | Get invoice doc for period | 🟡 Azure MCP Server |
| `azure_consumption_list_usage_details` | Per-resource detailed usage | 🟡 Azure MCP Server |
| `azure_costmanagement_query` | Custom cost query (Kusto-style) | 🟡 Azure MCP Server |
| `azure_costmanagement_create_budget` | Budget with alert rules | 🟡 Azure MCP Server |
| `azure_advisor_list_recommendations` | Cost / security / reliability / performance | 🟡 Azure MCP Server |
| `azure_reservations_list` | Existing reservations | 🟡 Azure MCP Server |
| `azure_savings_plans_list` | Compute Savings Plans | 🟡 Azure MCP Server |
| `azure_retail_prices_list` | Retail price lookup (no auth needed) | 🟡 (public REST API) |
| `vantage_get_azure_*` | Vantage Azure pricing pattern | ✅ Vantage |

---

## 2. Compute & Storage

### AWS — Compute (EC2, Lambda, ECS, EKS)

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_ec2_describe_instances` | List EC2 instances with filters | 🟡 AWS Labs ec2-mcp |
| `aws_ec2_run_instances` | Launch new instance(s) | 🟡 AWS Labs |
| `aws_ec2_start_instances` / `stop_instances` / `terminate_instances` | Lifecycle | 🟡 AWS Labs |
| `aws_ec2_modify_instance_attribute` | Change instance type, sg, etc. | 🟡 AWS Labs |
| `aws_ec2_describe_images` | List AMIs | 🟡 AWS Labs |
| `aws_ec2_create_image` | Snapshot AMI from running instance | 🟡 AWS Labs |
| `aws_ec2_describe_volumes` / `attach_volume` / `detach_volume` | EBS volume ops | 🟡 AWS Labs |
| `aws_ec2_create_snapshot` | EBS snapshot | 🟡 AWS Labs |
| `aws_ec2_describe_security_groups` / `authorize_security_group_ingress` | SG rules | 🟡 AWS Labs |
| `aws_lambda_list_functions` / `get_function` | Function inventory | 🟡 AWS Labs lambda-mcp |
| `aws_lambda_invoke` / `create_function` / `update_function_code` | Run / deploy | 🟡 AWS Labs |
| `aws_ecs_list_clusters` / `describe_clusters` | ECS inventory | 🟡 AWS Labs |
| `aws_ecs_list_services` / `describe_services` / `update_service` | Service ops | 🟡 AWS Labs |
| `aws_ecs_list_tasks` / `describe_tasks` / `run_task` / `stop_task` | Task ops | 🟡 AWS Labs |
| `aws_ecs_register_task_definition` | New task def | 🟡 AWS Labs |
| `aws_eks_list_clusters` / `describe_cluster` / `get_cluster_health` | EKS cluster ops | 🟡 AWS Labs |
| `aws_eks_list_nodegroups` / `describe_nodegroup` / `update_nodegroup_config` | Worker node ops | 🟡 AWS Labs |
| `aws_eks_list_addons` / `describe_addon` | Cluster addons | 🟡 AWS Labs |
| `aws_eks_list_fargate_profiles` / `describe_fargate_profile` | Serverless k8s ops | 🟡 AWS Labs |

### AWS — Storage (S3, EFS, FSx)

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_s3_list_buckets` | List buckets | 🟡 AWS Labs s3-mcp |
| `aws_s3_create_bucket` / `delete_bucket` | Bucket lifecycle | 🟡 AWS Labs |
| `aws_s3_list_objects` / `get_object` / `put_object` / `delete_object` | Object ops | 🟡 AWS Labs |
| `aws_s3_get_bucket_policy` / `put_bucket_policy` | Bucket policy | 🟡 AWS Labs |
| `aws_s3_put_bucket_lifecycle_configuration` | Tier / expiration rules | 🟡 AWS Labs |
| `aws_s3_get_bucket_encryption` / `put_bucket_encryption` | SSE config | 🟡 AWS Labs |
| `aws_efs_describe_file_systems` / `create_file_system` | EFS inventory | 🟡 AWS Labs |
| `aws_fsx_describe_file_systems` / `create_file_system` | FSx ops | 🟡 AWS Labs |
| `aws_backup_list_backup_plans` / `start_backup_job` | Backup orchestration | 🟡 AWS Labs |

### GCP — Compute & Storage

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `gcp_compute_list_instances` | List GCE instances | 🟡 GCE MCP (registry) |
| `gcp_compute_create_instance` / `delete_instance` | Lifecycle | 🟡 GCE MCP |
| `gcp_compute_start_instance` / `stop_instance` / `reset_instance` | Instance state | 🟡 GCE MCP |
| `gcp_compute_get_instance_basic_info` | Spec + status | 🟡 GCE MCP |
| `gcp_compute_set_instance_machine_type` | Resize | 🟡 GCE MCP |
| `gcp_compute_list_instance_attached_disks` | Disk inventory | 🟡 GCE MCP |
| `gcp_compute_attach_disk` / `detach_disk` | Disk ops | 🟡 GCE MCP |
| `gcp_compute_create_disk` / `delete_disk` | PD lifecycle | 🟡 GCE MCP |
| `gcp_storage_list_buckets` / `create_bucket` / `delete_bucket` | GCS bucket ops | ❌ (community MCPs exist) |
| `gcp_storage_list_objects` / `get_object` / `put_object` | Object ops | ❌ |
| `gcp_run_list_services` / `deploy_service` / `delete_service` | Cloud Run service ops | ❌ |
| `gcp_functions_list` / `deploy` / `call` | Cloud Functions | ❌ |
| `gcp_gke_list_clusters` / `create_cluster` / `delete_cluster` | GKE | ❌ |
| `gcp_gke_get_credentials` | kubeconfig fetch | ❌ |
| `gcp_filestore_list_instances` | Filestore inventory | ❌ |

### Azure — Compute & Storage

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `azure_vm_list` | List VMs in subscription/resource group | 🟡 Azure MCP Server |
| `azure_vm_create_or_update` | Provision/modify VM | 🟡 Azure MCP Server |
| `azure_vm_start` / `power_off` / `restart` / `deallocate` | Lifecycle | 🟡 Azure MCP Server |
| `azure_vm_resize` | Change size | 🟡 Azure MCP Server |
| `azure_vmss_list` / `update_instances` / `scale` | Scale Set ops | 🟡 Azure MCP Server |
| `azure_disks_list` / `create_or_update` / `delete` | Managed disks | 🟡 Azure MCP Server |
| `azure_storage_list_blobs` | List blobs in container | 🟡 Azure MCP Server (Storage) |
| `azure_storage_create_container` / `delete_container` | Container ops | 🟡 Azure MCP Server |
| `azure_storage_upload_blob` / `download_blob` / `delete_blob` | Blob ops | 🟡 Azure MCP Server |
| `azure_storage_set_container_access_policy` | Access policy | 🟡 Azure MCP Server |
| `azure_files_list_shares` / `create_share` | Azure Files | 🟡 Azure MCP Server |
| `azure_aks_list_clusters` / `create_or_update` / `delete` | AKS cluster ops | 🟡 Azure MCP Server |
| `azure_aks_list_node_pools` / `update_node_pool` | Node pool ops | 🟡 Azure MCP Server |
| `azure_functions_list_apps` / `deploy_function` | Functions | 🟡 Azure MCP Server |
| `azure_appservice_list_webapps` / `restart` / `swap_slots` | App Service | 🟡 Azure MCP Server |

---

## 3. Identity & Security

### AWS

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_iam_list_users` / `get_user` / `create_user` / `delete_user` | User ops | 🟡 AWS Labs iam-mcp |
| `aws_iam_create_user_with_policy` | Convenience: user + initial policy | 🟡 AWS Labs |
| `aws_iam_list_roles` / `get_role` / `create_role` / `delete_role` | Role ops | 🟡 AWS Labs |
| `aws_iam_attach_user_policy` / `detach_user_policy` | User-policy bind | 🟡 AWS Labs |
| `aws_iam_attach_role_policy` / `detach_role_policy` | Role-policy bind | 🟡 AWS Labs |
| `aws_iam_pass_role` | Pass role to a service | 🟡 AWS Labs |
| `aws_sts_assume_role` / `assume_role_with_saml` / `assume_role_with_web_identity` | Cross-account / federated | 🟡 AWS Labs |
| `aws_sts_get_caller_identity` | Who am I | 🟡 AWS Labs |
| `aws_iam_simulate_principal_policy` | "Can principal X do action Y" reasoning | 🟡 AWS Labs |
| `aws_kms_list_keys` / `describe_key` / `create_key` / `schedule_key_deletion` | Key lifecycle | 🟡 AWS Labs kms-mcp |
| `aws_kms_encrypt` / `decrypt` / `generate_data_key` | Crypto ops | 🟡 AWS Labs |
| `aws_secrets_get_secret_value` / `put_secret_value` / `rotate_secret` | Secrets ops | 🟡 AWS Labs |
| `aws_acm_list_certificates` / `request_certificate` | Cert ops | 🟡 AWS Labs |
| `aws_guardduty_list_findings` / `get_findings` | Threat findings | ❌ |
| `aws_securityhub_get_findings` / `update_findings` | Aggregated findings | ❌ |

### GCP

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `gcp_iam_list_service_accounts` / `create` / `delete` | SA inventory | ❌ |
| `gcp_iam_get_iam_policy` / `set_iam_policy` (per-resource) | Policy reads/writes | ❌ |
| `gcp_iam_test_iam_permissions` | "Can principal do action" | ❌ |
| `gcp_iam_create_role` / `update_role` | Custom role ops | ❌ |
| `gcp_resource_manager_list_projects` / `get_project` | Project tree | ❌ |
| `gcp_resource_manager_set_org_policy` | Org policy guardrails | ❌ |
| `gcp_kms_list_key_rings` / `list_crypto_keys` | KMS inventory | ❌ |
| `gcp_kms_encrypt` / `decrypt` | Crypto | ❌ |
| `gcp_secretmanager_list_secrets` / `access_secret_version` / `add_secret_version` | Secrets | ❌ |
| `gcp_certificate_manager_list_certificates` | Certs | ❌ |
| `gcp_scc_list_findings` / `update_finding` | Security Command Center | ❌ |

### Azure

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `azure_entra_list_users` / `get_user` / `create_user` / `delete_user` | Microsoft Entra ID users | 🟡 (Azure MCP Server / Microsoft Graph MCP) |
| `azure_entra_list_groups` / `add_member` / `remove_member` | Group ops | 🟡 |
| `azure_entra_list_role_assignments` | Directory role assignments | 🟡 |
| `azure_rbac_list_role_assignments` / `create` / `delete` | Subscription RBAC | 🟡 Azure MCP Server |
| `azure_rbac_list_role_definitions` | Built-in + custom roles | 🟡 |
| `azure_managed_identities_list` | Workload identities | 🟡 |
| `azure_keyvault_list_secrets` / `get_secret` / `set_secret` | Secrets | 🟡 Azure MCP Server (Key Vault) |
| `azure_keyvault_list_keys` / `create_key` / `encrypt` / `decrypt` | Keys | 🟡 |
| `azure_keyvault_list_certificates` / `import_certificate` | Certs | 🟡 |
| `azure_defender_list_alerts` / `dismiss_alert` | Defender for Cloud alerts | 🟡 |
| `azure_sentinel_run_query` | KQL query against Sentinel | 🟡 |
| `azure_policy_list_assignments` / `create_assignment` | Azure Policy | 🟡 |

---

## 4. Management & Observability

### AWS

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_cloudformation_describe_stacks` | Stack list + status | 🟡 AWS Labs cfn-mcp |
| `aws_cloudformation_create_stack` / `update_stack` / `delete_stack` | Stack lifecycle | 🟡 AWS Labs |
| `aws_cloudformation_describe_stack_events` | Recent events for debugging | 🟡 AWS Labs |
| `aws_cloudformation_detect_stack_drift` / `describe_stack_resource_drifts` | Drift detection | 🟡 AWS Labs |
| `aws_cdk_synth` / `cdk_diff` / `cdk_deploy` | CDK lifecycle (via wrapper) | ❌ |
| `aws_ssm_describe_instance_information` | Inventory of SSM-managed nodes | 🟡 AWS Labs ssm-mcp |
| `aws_ssm_send_command` | Run shell command on instances | 🟡 AWS Labs |
| `aws_ssm_get_parameter` / `put_parameter` | Parameter Store | 🟡 AWS Labs |
| `aws_ssm_start_session` | Session Manager session | 🟡 AWS Labs |
| `aws_config_describe_compliance_by_resource` | Compliance state | ❌ |
| `aws_cloudtrail_lookup_events` | Audit log search | 🟡 AWS Labs cloudtrail-mcp |
| `aws_cloudwatch_get_metric_data` | Time-series metrics | 🟡 AWS Labs cloudwatch-mcp |
| `aws_cloudwatch_get_metric_statistics` | Aggregated metrics | 🟡 AWS Labs |
| `aws_cloudwatch_describe_alarms` | Alarm inventory + state | 🟡 AWS Labs |
| `aws_cloudwatch_set_alarm_state` | Force alarm state (testing) | 🟡 AWS Labs |
| `aws_cloudwatch_logs_filter_log_events` | Search log streams | 🟡 AWS Labs |
| `aws_cloudwatch_logs_start_query` / `get_query_results` | Logs Insights query | 🟡 AWS Labs |
| `aws_xray_get_trace_summaries` / `batch_get_traces` | Distributed tracing | 🟡 AWS Labs |
| `aws_eventbridge_list_rules` / `put_rule` / `put_targets` | Event routing | 🟡 AWS Labs |

### GCP

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `gcp_deployment_manager_list_deployments` / `insert` / `delete` | Native IaC | ❌ |
| `gcp_config_connector_apply_yaml` | Manage GCP via k8s CRDs | ❌ |
| `gcp_asset_search_all_resources` | Cloud Asset Inventory cross-resource search | ❌ |
| `gcp_asset_export_assets` | Snapshot to BQ/GCS | ❌ |
| `gcp_logging_list_log_entries` | Cloud Logging query | ❌ |
| `gcp_logging_write_log_entries` | Append to a log | ❌ |
| `gcp_monitoring_list_time_series` | Metric query | ❌ |
| `gcp_monitoring_create_alert_policy` | Alerting | ❌ |
| `gcp_trace_list_traces` / `get_trace` | Distributed tracing | ❌ |
| `gcp_profiler_list_profiles` | Continuous profiler | ❌ |
| `gcp_error_reporting_list_events` / `list_groups` | Error reporting | ❌ |
| `gcp_audit_log_query` (subset of logging) | Cloud Audit Logs | ❌ |
| `gcp_eventarc_list_triggers` / `create_trigger` | Event routing | ❌ |
| `gcp_workflows_create` / `execute` / `get_execution` | Workflow orchestration | ❌ |

### Azure

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `azure_resource_manager_list_resource_groups` / `create` / `delete` | RG lifecycle | 🟡 Azure MCP Server |
| `azure_resource_manager_list_resources` | Per-RG resource list | 🟡 |
| `azure_arm_deploy_template` | Deploy ARM/Bicep template | 🟡 |
| `azure_arm_what_if` | Preview deployment changes | 🟡 |
| `azure_resource_graph_query` | Cross-subscription Kusto query | 🟡 (this is a marquee one) |
| `azure_policy_evaluate` / `list_compliance_states` | Policy compliance | 🟡 |
| `azure_arc_list_machines` | Arc-enabled servers | 🟡 |
| `azure_lighthouse_list_assignments` | Multi-tenant delegation | 🟡 |
| `azure_automation_list_runbooks` / `start_runbook` | Automation runbooks | 🟡 |
| `azure_monitor_query_metrics` | Metric query | 🟡 Azure MCP Server (Monitor) |
| `azure_monitor_query_logs` | KQL log query | 🟡 |
| `azure_monitor_list_alerts` / `update_alert` | Alert ops | 🟡 |
| `azure_application_insights_query` | App Insights KQL | 🟡 |
| `azure_eventgrid_list_topics` / `publish_event` | Event Grid | 🟡 |
| `azure_logicapps_list_workflows` / `trigger` | Logic Apps | 🟡 |

---

## 5. AI / GPU

The newest priority area. Distinguish three sub-capabilities: (a) **foundation-model invocation** (Bedrock / Vertex / Azure OpenAI), (b) **ML platform** (SageMaker / Vertex AI / Azure ML), (c) **GPU compute provisioning** (EC2 P/G families + Vantage GPU indexes; GCE A2/G2; Azure ND/NC/NV).

### AWS

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `aws_bedrock_list_foundation_models` | Available FMs in account/region | 🟡 AWS Labs bedrock-mcp |
| `aws_bedrock_invoke_model` | Direct model invocation | 🟡 AWS Labs |
| `aws_bedrock_invoke_model_with_response_stream` | Streamed invocation | 🟡 AWS Labs |
| `aws_bedrock_get_model_invocation_logging_configuration` | Logging config | 🟡 AWS Labs |
| `aws_bedrock_agent_create_agent` / `prepare_agent` / `invoke_agent` | Bedrock Agents | 🟡 AWS Labs |
| `aws_bedrock_kb_create_knowledge_base` / `retrieve` | Knowledge Base ops | 🟡 AWS Labs |
| `aws_sagemaker_list_endpoints` / `describe_endpoint` | Inference endpoints | 🟡 AWS Labs sagemaker-mcp |
| `aws_sagemaker_create_endpoint` / `update_endpoint` / `delete_endpoint` | Endpoint lifecycle | 🟡 AWS Labs |
| `aws_sagemaker_invoke_endpoint` | Inference call | 🟡 AWS Labs |
| `aws_sagemaker_create_training_job` / `describe_training_job` | Training | 🟡 AWS Labs |
| `aws_sagemaker_create_processing_job` | Data processing | 🟡 AWS Labs |
| `aws_sagemaker_list_models` / `create_model` | Model registry | 🟡 AWS Labs |
| `aws_ec2_describe_instances` (filter GPU) | Find GPU instances | 🟡 (covered above) |
| `vantage_use_ec2_index` (`has-1-gpu` etc.) | Pre-filtered GPU instance lists | ✅ Vantage |
| `aws_comprehend_detect_entities` / `detect_sentiment` | NLP | 🟡 AWS Labs |
| `aws_rekognition_detect_labels` / `detect_faces` | Vision | 🟡 AWS Labs |
| `aws_textract_analyze_document` / `start_document_analysis` | OCR + structured extract | 🟡 AWS Labs |
| `aws_transcribe_start_transcription_job` | Speech-to-text | 🟡 AWS Labs |
| `aws_polly_synthesize_speech` | Text-to-speech | 🟡 AWS Labs |
| `aws_translate_translate_text` | MT | 🟡 AWS Labs |

### GCP

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `gcp_vertex_list_models` / `get_model` | Vertex Model Registry | ❌ |
| `gcp_vertex_deploy_model` / `undeploy_model` | Endpoint deployment | ❌ |
| `gcp_vertex_predict` / `raw_predict` | Inference | ❌ |
| `gcp_vertex_list_endpoints` / `create_endpoint` | Endpoint inventory | ❌ |
| `gcp_vertex_create_custom_job` / `cancel_custom_job` | Training jobs | ❌ |
| `gcp_vertex_create_pipeline_run` | Pipelines | ❌ |
| `gcp_gemini_generate_content` | Gemini API direct | ❌ (community) |
| `gcp_automl_create_dataset` / `import_data` / `train` | AutoML lifecycle | ❌ |
| `gcp_compute_list_instances` (filter accelerator) | Find GPU/TPU instances | 🟡 GCE MCP |
| `vantage_use_gcp_index` (gpu indexes) | Pre-filtered GPU instances | ✅ Vantage |
| `gcp_speech_recognize` / `long_running_recognize` | Speech-to-Text | ❌ |
| `gcp_translate_translate_text` | Translation | ❌ |
| `gcp_vision_annotate_image` | Vision API | ❌ |
| `gcp_documentai_process_document` | Doc AI | ❌ |
| `gcp_dialogflow_detect_intent` / `streaming_detect_intent` | Conversational AI | ❌ |

### Azure

| Operation | What it does | MCP availability |
| --- | --- | --- |
| `azure_openai_list_deployments` | Deployed model endpoints | 🟡 Azure MCP Server / Azure OpenAI MCP |
| `azure_openai_create_deployment` / `delete_deployment` | Deployment lifecycle | 🟡 |
| `azure_openai_chat_completions` | Chat inference | 🟡 |
| `azure_openai_embeddings` | Embedding inference | 🟡 |
| `azure_openai_audio_transcriptions` / `audio_translations` | Whisper | 🟡 |
| `azure_aifoundry_list_projects` / `list_models` | AI Foundry inventory | 🟡 |
| `azure_ml_list_workspaces` / `list_endpoints` / `invoke_endpoint` | Azure ML | 🟡 |
| `azure_ml_create_job` / `cancel_job` | Training jobs | 🟡 |
| `azure_ml_list_models` / `register_model` | Model registry | 🟡 |
| `azure_aisearch_search` / `index_documents` | AI Search (vector + keyword) | 🟡 |
| `azure_vision_analyze_image` | AI Vision | 🟡 |
| `azure_speech_recognize` / `synthesize` | AI Speech | 🟡 |
| `azure_doc_intelligence_analyze` | Document Intelligence | 🟡 |
| `azure_translator_translate` | Translator | 🟡 |
| `azure_vm_list` (filter `Standard_NC*`/`ND*`/`NV*`) | Find GPU VMs | 🟡 (covered above) |
| `vantage_use_azure_index` (gpu) | Pre-filtered GPU VMs | ✅ Vantage |

---

## What's actually wirable today vs. tomorrow

| Status | Coverage |
| --- | --- |
| **Wirable today (Vantage)** | List pricing + instance specs across AWS EC2/RDS/ElastiCache/OpenSearch/Redshift, plus Azure and GCP compute. Used as Pattern A/B/C in the existing skill. |
| **Wirable with one connect** (Cowork registry) | GCE VM management (29+ tools), BigQuery SQL, AWS Marketplace discovery. *No general AWS / Azure management MCP appears in the registry yet.* |
| **Wirable upstream** (would need plugin install) | AWS Labs `awslabs/mcp` (~30 servers), Microsoft Azure MCP Server, community GCP MCPs (Cloud Run, GKE, Cloud Logging). These are mature; we'd need to add them as plugins. |
| **Custom-build today** | Anything in the ❌ rows above — wrap the AWS / GCP / Azure SDK in a small MCP. Cheapest for narrow jobs (e.g. only 5 ops). |
