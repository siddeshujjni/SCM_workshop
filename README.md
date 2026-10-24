# Enbridge SCM Workshop — Databricks Enablement

[![Databricks](https://img.shields.io/badge/Databricks-DABs-red)](https://docs.databricks.com)

A Declarative Automation Bundle (DAB) for the Enbridge Supply Chain Management
team's Databricks enablement training.

## Quick Start

Complete the **Prerequisites** below first (schema + 2 volumes with source files).

```bash
# 1. Clone this repo into your Databricks workspace (Git folder) or locally
# 2. Edit the `enbridge` target in databricks.yml: catalog, schema, volume paths
# 3. Validate and deploy
databricks bundle validate --target enbridge
databricks bundle deploy --target enbridge

# 4. Build all notebook tables (runs Lesson 2 end-to-end, ~5 min)
databricks bundle run scm_training_setup --target enbridge

# 5. Run the Lakeflow pipeline (writes to the separate pipeline schema)
databricks bundle run scm_preferred_supplier_pipeline --target enbridge
```

Use `--target dev` instead for a personal sandbox: resources are prefixed with your username and schedules are paused.

## Bundle Structure

```
SCM_workshop/
├── databricks.yml                            # Bundle config & variable definitions
├── README.md                                 # This file
├── resources/
│   ├── scm_pipeline.pipeline.yml             # Lakeflow SDP pipeline definition
│   ├── scm_pipeline_schema.schema.yml        # Schema for pipeline tables (created by the bundle)
│   ├── scm_etl_job.job.yml                   # Job: training setup (runs Lesson 2 notebook)
│   └── scm_pipeline_refresh.job.yml          # Job: daily pipeline refresh
└── src/
    ├── notebooks/
    │   ├── Lesson_02_Building_Data_Pipelines.ipynb   # Hands-on: 13 Bronze, 5 Silver, 6 Gold tables + governance
    │   └── Lesson_03_Self_Service_Analytics_AI.ipynb # Hands-on: Dashboards, Genie, MLflow, AI
    └── pipeline/
        ├── 01_bronze.sql                      # SDP: 8 streaming tables (Auto Loader)
        ├── 02_silver.sql                      # SDP: 4 materialized views + expectations
        └── 03_gold.sql                        # SDP: 5 materialized views for dashboards
```

## What Gets Deployed

| Resource | Name | Purpose |
|----------|------|--------|
| **Pipeline** | Enbridge SCM - Preferred Supplier Pipeline | Lakeflow SDP: Bronze→Silver→Gold |
| **Job 1** | Enbridge SCM - Training Setup | One-time: runs Lesson 2 notebook to create all tables |
| **Job 2** | Enbridge SCM - Pipeline Refresh | Daily at 6 AM: incremental pipeline refresh |
| **Schema** | `${catalog}.${pipeline_schema}` | Created by the bundle for pipeline tables (separate from the notebook tables) |

## Variables

| Variable | Default | Description |
|----------|---------|------------|
| `catalog` | `serverless_stable_qr9if1_catalog` | Unity Catalog catalog |
| `schema` | `enbridge_scm` | Existing schema holding the source volumes; Lesson 2 notebook tables are written here |
| `pipeline_schema` | `enbridge_scm_pipeline` | Schema the bundle creates for Lakeflow pipeline tables |
| `volume_path` | `/Volumes/.../enbridge_scm/training` | UC Volume with original source CSVs |
| `volume_path_psl` | `/Volumes/.../enbridge_scm/enbridge_psl_dashboard` | UC Volume with enriched PSL Dashboard files (CSV + Excel) |

Override for your environment:
```yaml
# In databricks.yml under your target:
targets:
  enbridge:
    variables:
      catalog: your_catalog
      schema: your_schema
      volume_path: /Volumes/your_catalog/your_schema/training
      volume_path_psl: /Volumes/your_catalog/your_schema/enbridge_psl_dashboard
```

## Prerequisites

1. **Create the schema and volumes** (once):
   ```sql
   CREATE SCHEMA IF NOT EXISTS your_catalog.enbridge_scm;
   CREATE VOLUME IF NOT EXISTS your_catalog.enbridge_scm.training;
   CREATE VOLUME IF NOT EXISTS your_catalog.enbridge_scm.enbridge_psl_dashboard;
   ```
2. **Upload source data**: the 26 original CSVs to the `training` volume, and the 17 PSL Dashboard files (CSV + Excel) to the `enbridge_psl_dashboard` volume. Keep the original file names.
3. **Workspace permissions**: CREATE SCHEMA on the catalog; ability to create jobs and pipelines
4. **Compute**: Serverless enabled for notebooks, jobs and pipelines
5. **Databricks CLI** v0.250+ (or deploy from the workspace Git folder UI)

## Running the notebooks manually

1. Open `src/notebooks/Lesson_02_Building_Data_Pipelines.ipynb`, attach serverless compute, set the `catalog` / `schema` widgets, and **Run all** (~3 min). This builds all 24 tables + 1 view.
2. Open `src/notebooks/Lesson_03_Self_Service_Analytics_AI.ipynb` and run it (uses the tables from Lesson 2).

The notebook widgets `catalog`, `schema`, `volume_path` and `volume_path_psl` control where data is read from and written to; the volume paths default to `/Volumes/<catalog>/<schema>/training` and `/Volumes/<catalog>/<schema>/enbridge_psl_dashboard`.

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