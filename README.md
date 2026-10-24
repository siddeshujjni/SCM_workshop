# Enbridge SCM Workshop — Databricks Enablement

[![Databricks](https://img.shields.io/badge/Databricks-DABs-red)](https://docs.databricks.com)

A Declarative Automation Bundle (DAB) for the Enbridge Supply Chain Management
team's Databricks enablement training.

> **Nothing runs automatically.** Deploying this bundle only creates the jobs, pipeline and schema.
> There is no schedule and the pipeline is not continuous: every run is started manually.

## Deploying in the Enbridge environment

### Prerequisites

| Requirement | Details |
|-------------|---------|
| Workspace | Unity Catalog enabled, serverless compute enabled for notebooks, jobs and pipelines |
| Permissions | `USE CATALOG` and `CREATE SCHEMA` on the target catalog (or an existing schema you own) |
| Databricks CLI | v0.250 or later (`databricks -v`). Not needed if you deploy from the workspace UI (Option B in Step 5) |
| Source files | 26 original CSVs (Agreements, Contracts, Category Managed, Regional Sourcing) and 17 PSL Dashboard files (CSV + Excel) |

### Step 1 - Authenticate the CLI

```bash
databricks auth login --host https://<your-workspace-url> --profile enbridge
```

Add `--profile enbridge` to every `databricks` command below (or set `DATABRICKS_CONFIG_PROFILE=enbridge`).

### Step 2 - Create the schema and volumes

Run once in a SQL editor or notebook. Replace `<catalog>` with your catalog name:

```sql
CREATE SCHEMA IF NOT EXISTS <catalog>.enbridge_scm;
CREATE VOLUME IF NOT EXISTS <catalog>.enbridge_scm.training;
CREATE VOLUME IF NOT EXISTS <catalog>.enbridge_scm.enbridge_psl_dashboard;
```

The bundle creates the second schema (`enbridge_scm_pipeline`) for the Lakeflow pipeline itself.

### Step 3 - Upload the source files

Upload with **Catalog Explorer > volume > Upload to this volume**, or with the CLI:

```bash
databricks fs cp -r ./training dbfs:/Volumes/<catalog>/enbridge_scm/training
databricks fs cp -r ./enbridge_psl_dashboard dbfs:/Volumes/<catalog>/enbridge_scm/enbridge_psl_dashboard
```

Keep the original file names; the code matches on them (e.g. `Agreements - BPA.csv`, `*Category Managed*.csv`, `Output1.xlsx`, `*CM*.xlsx`).
Put the files directly in the volume root, not in a subfolder.

### Step 4 - Get the code and set your environment

```bash
git clone https://github.com/siddeshujjni/SCM_workshop.git
cd SCM_workshop
```

Edit the `enbridge` target in `databricks.yml`:

```yaml
targets:
  enbridge:
    mode: production
    variables:
      catalog: <catalog>                                              # your catalog
      schema: enbridge_scm                                            # schema from Step 2
      volume_path: /Volumes/<catalog>/enbridge_scm/training
      volume_path_psl: /Volumes/<catalog>/enbridge_scm/enbridge_psl_dashboard
      # pipeline_schema: enbridge_scm_pipeline                        # optional override
```

### Step 5 - Validate and deploy

**Option A - CLI**

```bash
databricks bundle validate --target enbridge
databricks bundle deploy --target enbridge
```

**Option B - Workspace UI:** create a Git folder from this repo (Workspace > Create > Git folder),
open `databricks.yml`, and use the **Deployments** panel to deploy the `enbridge` target.

The deployment lands in `/Workspace/Users/<you>/.bundle/enbridge_scm_workshop/enbridge`.

### Step 6 - Run

```bash
# Builds all notebook tables: Lesson 2 then Lesson 3 (~6 min)
databricks bundle run scm_training_setup --target enbridge

# Runs the Lakeflow pipeline once (~1-2 min)
databricks bundle run scm_pipeline_refresh --target enbridge
```

You can also start both from **Jobs & Pipelines** in the workspace UI (click **Run now**).

### Step 7 - Verify

```sql
SELECT table_schema, count(*) AS objects
FROM <catalog>.information_schema.tables
WHERE table_schema IN ('enbridge_scm', 'enbridge_scm_pipeline')
  AND table_name NOT LIKE '\_\_%'        -- skip internal pipeline tables (__materialization_*)
  AND table_name NOT LIKE 'event_log%'
GROUP BY table_schema;
```

Expected: `enbridge_scm` has 25 objects (24 tables + 1 view, plus any tables you already had);
`enbridge_scm_pipeline` has 17 (8 Bronze streaming tables, 4 Silver and 5 Gold materialized views).
Spot check: `SELECT count(*) FROM <catalog>.enbridge_scm.silver_agreements` returns 4,754.

### Optional - Turn on the daily schedule

In `resources/scm_pipeline_refresh.job.yml`, uncomment the `schedule:` block (daily 6 AM Toronto time) and run
`databricks bundle deploy --target enbridge` again.

### Updating or removing the deployment

* **After pulling new changes:** `git pull`, then `databricks bundle deploy --target enbridge`.
* **Reprocess all pipeline data from scratch:** `databricks bundle run scm_preferred_supplier_pipeline --target enbridge --full-refresh-all`
* **Remove everything the bundle created:** `databricks bundle destroy --target enbridge`. This deletes both jobs, the pipeline,
  and the `enbridge_scm_pipeline` schema including its tables. Tables the notebooks created in `enbridge_scm` and the volumes are not removed.

### Troubleshooting

| Error | Cause / fix |
|-------|-------------|
| `PATH_NOT_FOUND` / `Input path ... does not exist` | Files missing, renamed, or in a subfolder of the volume. Check Step 3 and the volume paths in Step 4. |
| `UC_TAG_POLICY_VALUE_NOT_ALLOWED` (Lesson 2, A4 cell) | Your workspace restricts that tag key. Change the tag key/value in the cell to one your tag policy allows. |
| `PERMISSION_DENIED` creating schema | You need `CREATE SCHEMA` on the catalog, or set `pipeline_schema` to a schema you own and remove `resources/scm_pipeline_schema.schema.yml`. |
| `known_business_unit` expectation failed | A Category Managed / Regional Sourcing file has a BU code other than LP, GTM, GDS, GPT. Fix the file or extend the list in `src/pipeline/02_silver.sql`. |
| `Validation failed ... root_path` | Keep the `workspace.root_path` line in the `enbridge` target; production mode requires it. |

### Personal sandbox (optional)

To try it without touching shared resources, use the `dev` target with your own values:

```bash
databricks bundle deploy --target dev --var="catalog=<catalog>" \
  --var="volume_path=/Volumes/<catalog>/enbridge_scm/training" \
  --var="volume_path_psl=/Volumes/<catalog>/enbridge_scm/enbridge_psl_dashboard"
```

Dev mode prefixes job/pipeline names and the pipeline schema with your username. Pass the same `--var` flags to `bundle run`.

## Bundle Structure

```
SCM_workshop/
├── databricks.yml                            # Bundle config & variable definitions
├── README.md                                 # This file
├── resources/
│   ├── scm_pipeline.pipeline.yml             # Lakeflow SDP pipeline definition
│   ├── scm_pipeline_schema.schema.yml        # Schema for pipeline tables (created by the bundle)
│   ├── scm_etl_job.job.yml                   # Job: training setup (runs Lesson 2, then Lesson 3)
│   └── scm_pipeline_refresh.job.yml          # Job: pipeline refresh (manual; schedule commented out)
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
| **Job 1** | Enbridge SCM - Training Setup (Bronze to Gold) | Manual: runs Lesson 2 (all notebook tables), then Lesson 3 |
| **Job 2** | Enbridge SCM - Pipeline Refresh | Manual: runs the Lakeflow pipeline (no schedule) |
| **Schema** | `${catalog}.${pipeline_schema}` | Created by the bundle for pipeline tables (separate from the notebook tables) |

## Variables

| Variable | Default | Description |
|----------|---------|------------|
| `catalog` | `serverless_stable_qr9if1_catalog` | Unity Catalog catalog |
| `schema` | `enbridge_scm` | Existing schema holding the source volumes; Lesson 2 notebook tables are written here |
| `pipeline_schema` | `enbridge_scm_pipeline` | Schema the bundle creates for Lakeflow pipeline tables |
| `volume_path` | `/Volumes/.../enbridge_scm/training` | UC Volume with original source CSVs |
| `volume_path_psl` | `/Volumes/.../enbridge_scm/enbridge_psl_dashboard` | UC Volume with enriched PSL Dashboard files (CSV + Excel) |

Set these per environment under `targets:` in `databricks.yml` (see Step 4).

## Running the notebooks manually

Complete Steps 2-3 above first.

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