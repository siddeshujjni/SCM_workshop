# Enbridge SCM Workshop — Databricks Enablement

[![Databricks](https://img.shields.io/badge/Databricks-DABs-red)](https://docs.databricks.com)

A Declarative Automation Bundle (DAB) for the Enbridge Supply Chain Management
team's Databricks enablement training.

## Quick Start

```bash
# 1. Clone this repo into your Databricks workspace (Git folder)
# 2. Set your target variables in databricks.yml
# 3. Deploy
databricks bundle deploy --target dev

# 4. Run the Lakeflow pipeline
databricks bundle run scm_pipeline_refresh --target dev
```

## Bundle Structure

```
SCM_workshop/
├── databricks.yml                            # Bundle config & variable definitions
├── README.md                                 # This file
├── Training_Summary.md                       # Full training agenda, timing, implementation guide
├── resources/
│   ├── scm_pipeline.pipeline.yml             # Lakeflow SDP pipeline definition
│   └── scm_etl_job.job.yml                   # Jobs: training setup + daily refresh
└── src/
    ├── notebooks/
    │   ├── Lesson_02_Building_Data_Pipelines  # Hands-on: Bronze→Silver→Gold + governance
    │   └── Lesson_03_Self_Service_Analytics_AI # Hands-on: Dashboards, Genie, MLflow, AI
    └── pipeline/
        ├── 01_bronze.sql                      # SDP: 5 streaming tables (Auto Loader)
        ├── 02_silver.sql                      # SDP: 2 materialized views + expectations
        └── 03_gold.sql                        # SDP: 3 materialized views for dashboards
```

## What Gets Deployed

| Resource | Name | Purpose |
|----------|------|--------|
| **Pipeline** | Enbridge SCM - Preferred Supplier Pipeline | Lakeflow SDP: Bronze→Silver→Gold |
| **Job 1** | Enbridge SCM - Training Setup | One-time: runs Lesson 2 notebook to create all tables |
| **Job 2** | Enbridge SCM - Pipeline Refresh | Daily at 6 AM: incremental pipeline refresh |
| **Schema** | `${catalog}.${schema}` | Unity Catalog schema for all tables |

## Variables

| Variable | Default | Description |
|----------|---------|------------|
| `catalog` | `serverless_stable_qr9if1_catalog` | Unity Catalog catalog |
| `schema` | `enbridge_scm` | Target schema for all tables |
| `volume_path` | `/Volumes/.../enbridge_scm/training` | UC Volume with source CSVs |

Override for your environment:
```yaml
# In databricks.yml under your target:
targets:
  enbridge:
    variables:
      catalog: your_catalog
      schema: your_schema
      volume_path: /Volumes/your_catalog/your_schema/training
```

## Prerequisites

1. **Upload source data**: Place the 26 CSV files into the UC Volume at `${volume_path}`
2. **Workspace permissions**: Ability to create schemas, tables, and pipelines
3. **Compute**: Serverless enabled (used by the pipeline)

## Training Agenda

### Lesson 2 — Building Clean, Governed & Efficient Data Pipelines (~2.5 hours)
- Data governance & quality using Unity Catalog
- Building Silver & Gold layers with Enbridge business rules (R1-R5)
- Performance and cost-aware design
- Lakeflow Spark Declarative Pipelines with expectations
- Monitoring, re-runs, and troubleshooting

### Lesson 3 — Enabling Self-Service Analytics & AI (~2.5 hours)
- Dashboards & visualizations
- Designing Genie Q&A experiences
- MLflow for model lifecycle management
- Agentic AI & Generative AI with Mosaic AI
- Databricks One for self-service delivery
- End-user access, security, and governance

## Enbridge Business Rules Implemented

| Rule | Description |
|------|------------|
| R1 | ISN Grade: expired→NULL, blocking→'N/A - Contractor Blocking' |
| R2 | BU code parsing from sourcing rule name |
| R3 | Geography formatting: 'Parent Region - Region' |
| R4 | BU code→full name: LP→Liquids Pipelines, GTM→Gas Transmission, etc. |
| R5 | Approval Status: rank 1→Approved, 2→In Process, 3→Debarred, etc. |