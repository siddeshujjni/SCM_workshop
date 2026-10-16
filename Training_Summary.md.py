# Databricks notebook source
# Enbridge Supply Chain Management — Databricks Enablement Training Summary

**Prepared for:** Enbridge SCM Team
**Prepared by:** Databricks Enablement Team
**Date:** September 2026

---

## 1. Training Overview

This enablement program is designed to transition the Enbridge Supply Chain Management team from their current Oracle + Power BI environment to Databricks. The training uses **Enbridge's own datasets** (26 CSVs covering agreements, contracts, preferred suppliers across all business units and regions) and replicates the existing "Preferred Supplier List" Power BI report as a Databricks data pipeline.

### Source Data
- 26 CSV files in UC Volume: `/Volumes/serverless_stable_qr9if1_catalog/enbridge_scm/training/`
- 1 PBIX file: `Preferred Supplier List.pbix` (original Power BI report)
- 1 SQL Transformation doc: Documents 4 Power BI tables and 5 shared business rules (R1-R5)
- Target schema: `serverless_stable_qr9if1_catalog.enbridge_scm`

### Datasets Covered
| Dataset Category | Files | Total Rows | Key Fields |
|----------------|-------|-----------|-----------|
| Agreements — BPA | 1 | 2,793 | Supplier, Contract #, Agreement #, Status, BU, Region |
| Agreements — CPA | 1 | 1,961 | Supplier, Contract #, Agreement #, Status, BU, Region |
| Contracts | 1 | 1,858 | Contract #, Party, Amount, Status, Type, BU, Dates |
| Category Managed | 12 | ~1,200 | Supplier Name, Number, BU, Region |
| Regional Sourcing | 7 | ~1,200 | Supplier Name, Number, BU, Region |

---

## 2. Training Agenda & Timing

### Lesson 2 — Building Clean, Governed & Efficient Data Pipelines (~2.5 hours)

| Section | Topic | Duration | Hands-On Content |
|---------|-------|----------|----------------|
| A | **Data Governance & Quality using Unity Catalog** | 45 min | Schema creation, Bronze ingestion (5 tables), table types, column comments, tags, rescued data, quarantine patterns |
| B | **Building Silver & Gold Layers** | 40 min | Unified preferred suppliers (Rule R4), unified agreements (BPA+CPA with rescued data), 3 Gold aggregation tables |
| C | **Performance and Cost-Aware Design** | 30 min | Liquid clustering, broadcast joins, CTE patterns, query plans, best practices summary |
| D | **Building Pipelines with Notebooks & Lakeflow** | 40 min | Notebook+Jobs orchestration, Lakeflow SDP syntax (streaming tables, materialized views, expectations), data quality expectations (warn/drop/fail) |
| E | **Monitoring, Re-runs & Troubleshooting** | 20 min | Table history, DESCRIBE DETAIL, alert setup, re-run strategies, troubleshooting guide |
| Bonus | **Compute Selection** | 10 min | All-purpose vs Jobs vs SQL Warehouse vs Serverless, matching compute to workloads |
| Exercise | **Hands-On Practice** | 15 min | 3 exercises + 1 stretch (bronze ingestion, silver transform, gold aggregation, SDP expectations) |

### Lesson 3 — Enabling Self-Service Analytics & AI for Business Users (~2.5 hours)

| Section | Topic | Duration | Hands-On Content |
|---------|-------|----------|----------------|
| A | **Dashboards & Visualizations** | 30 min | 4 dashboard-ready SQL queries (supplier coverage, regional heatmap, agreement status, contract analytics), Power BI migration mapping |
| B | **Designing Genie Q&A Experiences** | 30 min | Table preparation for Genie, column comments, semantic context instructions, sample questions, Genie Space creation guide |
| C | **MLflow for Model Lifecycle Management** | 30 min | Feature engineering from Gold tables, supplier risk classifier (RandomForest), MLflow experiment tracking, model registration concepts |
| D | **Agentic AI & Generative AI with Mosaic AI** | 30 min | AI functions in SQL (ai_gen, ai_extract), agent architecture, Mosaic AI building blocks, governance for GenAI, SCM use cases |
| E | **Databricks One for Self-Service Delivery** | 15 min | Databricks One overview, access model, Enbridge SCM delivery plan |
| F | **End-User Access, Security & Governance** | 15 min | GRANT statements, row-level security, column masking, tags, audit logs, access model diagram |
| Exercise | **Hands-On Practice** | 15 min | 3 exercises + 1 stretch (dashboard query, Genie prep, AI enhancement, RLS setup) |

---

## 3. Hands-On Deliverables

### Notebooks Created
1. **Lesson_02_Building_Data_Pipelines** — 37+ cells
   - Location: `/Users/siddesh.ujjni@databricks.com/enbridge_enablement/Lesson_02_Building_Data_Pipelines`
   - 5 Bronze tables, 2 Silver tables, 3 Gold tables, 1 view
   - Lakeflow SDP syntax examples (commented, ready for pipeline creation)
   - 3 hands-on exercises + 1 stretch

2. **Lesson_03_Self_Service_Analytics_AI** — 30+ cells
   - Location: `/Users/siddesh.ujjni@databricks.com/enbridge_enablement/Lesson_03_Self_Service_Analytics_AI`
   - 4 dashboard queries, Genie setup guide, MLflow model training, AI function demos
   - 3 hands-on exercises + 1 stretch

### Tables Created (in enbridge_scm schema)

| Layer | Table | Rows | Purpose |
|-------|-------|------|--------|
| Bronze | `bronze_agreements_bpa` | 2,793 | Raw BPA data |
| Bronze | `bronze_agreements_cpa` | 1,961 | Raw CPA data (with rescued data demo) |
| Bronze | `bronze_contracts` | 1,858 | Raw legal contracts |
| Bronze | `bronze_category_managed` | ~1,200 | Unioned from 12 CSV files |
| Bronze | `bronze_regional_sourcing` | ~1,200 | Unioned from 7 CSV files |
| Silver | `silver_preferred_suppliers` | ~2,400 | Unified suppliers with BU name resolution (R4) |
| Silver | `silver_agreements` | ~4,754 | Unified BPA+CPA with standardized schema |
| Gold | `gold_regional_supplier_coverage` | ~50 | Supplier counts by BU/region/type |
| Gold | `gold_agreement_summary` | ~8 | Agreement status summary |
| Gold | `gold_contract_analytics` | ~30 | Contract analytics by BU/status/type |
| View | `vw_active_contracts` | — | Active contracts filter view |

### Enbridge Business Rules Implemented
| Rule | Description | Applied In |
|------|-------------|----------|
| R1 | ISN Grade logic (expired→NULL, blocking→N/A) | Referenced in docs |
| R2 | BU code parsing from sourcing rule name | Referenced in docs |
| R3 | Geography formatting (Parent - Region) | Referenced in docs |
| R4 | BU code → full name (LP→Liquids Pipelines, etc.) | silver_preferred_suppliers |
| R5 | Approval status mapping (rank 1-5 → text) | Referenced in docs |

---

## 4. Prerequisites

### For Participants
- Databricks workspace access with compute permissions
- Ability to create schemas in `serverless_stable_qr9if1_catalog`
- Basic SQL knowledge (SELECT, JOIN, GROUP BY)
- Familiarity with supply chain data concepts

### For Instructors
- Run Lesson 2 notebook first (creates all Bronze/Silver/Gold tables)
- Verify volume path: `/Volumes/serverless_stable_qr9if1_catalog/enbridge_scm/training/`
- Prepare a live dashboard demo and Genie Space demo
- Have the Power BI report available for comparison

---

## 5. Scheduling Recommendations

### Recommended Schedule
| Day | Session | Duration |
-----|---------|----------|
| Day 1 AM | Lesson 2 — Sections A-C (Governance, Silver/Gold, Performance) | 2.5 hours |
| Day 1 PM | Lesson 2 — Sections D-E + Bonus + Exercises (Pipelines, Monitoring) | 1.5 hours |
| Day 2 AM | Lesson 3 — Sections A-C (Dashboards, Genie, MLflow) | 2.5 hours |
| Day 2 PM | Lesson 3 — Sections D-F + Exercises (AI, Databricks One, Security) | 1.5 hours |

### Alternative: Single-Day Intensive
- 8 hours with 2 breaks and 1 lunch
- Compress exercises to instructor-led demos
- Best for teams with prior Databricks exposure

### Group Size
- Ideal: 8-15 participants (enough for discussion, small enough for hands-on help)
- Each participant should have their own schema to avoid collisions

---

## 6. Post-Training Next Steps

1. **Create production Lakeflow pipeline** from the SDP syntax in Lesson 2
2. **Build live dashboards** from the 4 SQL queries in Lesson 3
3. **Set up Genie Space** with the provided semantic instructions
4. **Configure access groups** (scm_business_users, scm_analysts, scm_data_engineers)
5. **Connect Oracle source** to replace volume CSVs with live ingestion
6. **Deploy MLflow model** to Model Serving for supplier risk scoring
7. **Set up Databricks One** access for business users

---

## 7. Key Concepts Covered

### Data Engineering
- Medallion architecture (Bronze → Silver → Gold)
- Unity Catalog governance (3-level namespace, tags, comments, constraints)
- Schema handling (inference, rescued data, evolution)
- Table types (managed, external, views, materialized views, streaming tables)
- Lakeflow Spark Declarative Pipelines (SDP)
- Auto Loader for incremental ingestion
- Expectations for data quality (warn, drop, fail)
- Performance optimization (liquid clustering, broadcast joins, CTEs)
- Monitoring (table history, alerts, troubleshooting)

### Analytics & AI
- AI/BI Dashboards on Gold tables
- Genie natural language Q&A
- MLflow experiment tracking and model registry
- AI functions in SQL (ai_gen, ai_extract)
- Mosaic AI agent framework
- Vector Search for RAG
- AI Gateway for governed LLM access

### Security & Governance
- GRANT statements for access control
- Row-level security (RLS)
- Column masking
- Unity Catalog tags for classification
- Audit logging
- Databricks One for business user access

---

## 8. Implementation Guide — Setting Up in the Customer Environment

This section provides step-by-step instructions for deploying the training environment
in Enbridge's (or any customer's) Databricks workspace.

### Option A: Declarative Automation Bundle (Recommended)

The training content is packaged as a **Declarative Automation Bundle (DAB)** — a single
deployable unit that provisions the schema, pipeline, jobs, and notebooks in one command.

#### Prerequisites (Customer Side)

| Requirement | Details |
|------------|--------|
| Databricks workspace | With Unity Catalog enabled |
| Serverless compute | Enabled for notebooks and pipelines |
| Databricks CLI | v0.230+ installed on a local machine or workspace terminal |
| Git access | Clone permissions for the training repo |
| UC permissions | `CREATE SCHEMA` on the target catalog |
| UC Volume | Writable volume for uploading source CSV files |

#### Step 1 — Clone the Repository

```bash
# In the Databricks workspace: Repos → Add Repo → paste the URL
# OR from local machine:
git clone https://github.com/siddesh-ujjni/enbridge_scm_workshop.git
cd enbridge_scm_workshop
```

#### Step 2 — Configure for Your Environment

Edit `databricks.yml` and update the `enbridge` target with your workspace details:

```yaml
targets:
  enbridge:
    mode: production
    workspace:
      host: https://your-workspace.cloud.databricks.com  # <-- Your workspace URL
    variables:
      catalog: your_catalog_name          # <-- Your Unity Catalog catalog
      schema: enbridge_scm               # <-- Schema name (will be created)
      volume_path: /Volumes/your_catalog_name/enbridge_scm/training  # <-- Volume path
```

#### Step 3 — Upload Source Data to UC Volume

Create the UC Volume and upload the 26 CSV files:

```sql
-- Run in a Databricks notebook or SQL editor
CREATE VOLUME IF NOT EXISTS your_catalog_name.enbridge_scm.training;
```

Then upload all files from the `source_data/` folder:
```bash
# From local machine with Databricks CLI
databricks fs cp ./source_data/ /Volumes/your_catalog_name/enbridge_scm/training/ --recursive
```

Alternatively, upload via the **Catalog Explorer UI**:
1. Navigate to **Catalog** → your catalog → `enbridge_scm` → **Volumes** → `training`
2. Click **Upload** and select all 26 CSV files + the PBIX file

#### Step 4 — Validate the Bundle

```bash
databricks bundle validate --target enbridge
```

Expected output: no errors. Warnings about development mode are normal for `dev` target.

#### Step 5 — Deploy

```bash
databricks bundle deploy --target enbridge
```

This creates:
- Schema `enbridge_scm` in your catalog (if it doesn't exist)
- Lakeflow pipeline: **Enbridge SCM - Preferred Supplier Pipeline**
- Job: **Enbridge SCM - Training Setup** (one-time notebook run)
- Job: **Enbridge SCM - Pipeline Refresh** (daily at 6 AM ET)
- Both lesson notebooks deployed to the workspace

#### Step 6 — Run the Initial Pipeline

```bash
# Option A: Run the Lakeflow pipeline (creates all Bronze/Silver/Gold tables)
databricks bundle run scm_pipeline_refresh --target enbridge

# Option B: Run the training setup job (runs Lesson 2 notebook end-to-end)
databricks bundle run scm_training_setup --target enbridge
```

#### Step 7 — Verify the Deployment

```sql
-- Run in a Databricks SQL editor or notebook
USE CATALOG your_catalog_name;
SHOW TABLES IN enbridge_scm;

-- Should show:
-- bronze_agreements_bpa, bronze_agreements_cpa, bronze_contracts,
-- bronze_category_managed, bronze_regional_sourcing,
-- silver_preferred_suppliers, silver_agreements,
-- gold_regional_supplier_coverage, gold_agreement_summary, gold_contract_analytics
```

---

### Option B: Manual Setup (Without DABs)

If the customer prefers not to use DABs, follow these manual steps.

#### Step 1 — Create the Schema and Volume

```sql
CREATE CATALOG IF NOT EXISTS your_catalog_name;
CREATE SCHEMA IF NOT EXISTS your_catalog_name.enbridge_scm
  COMMENT 'Enbridge SCM - Preferred Supplier List pipeline. Source: Oracle ENBOAC.';
CREATE VOLUME IF NOT EXISTS your_catalog_name.enbridge_scm.training;
```

#### Step 2 — Upload Source CSVs

Upload all 26 CSV files to the volume via the Catalog Explorer UI or CLI:

```bash
databricks fs cp ./source_data/ /Volumes/your_catalog_name/enbridge_scm/training/ --recursive
```

Expected files:
```
Agreements - BPA.csv, Agreements - CPA.csv, Contracts.csv,
12x *Category Managed*.csv files,
7x *Regional Sourcing*.csv files,
Preferred Supplier List.pbix,
SQL_Source_Transformation_Documentation 1.docx
```

#### Step 3 — Import Notebooks

1. Download the two `.ipynb` notebook files from the Git repo
2. In Databricks: **Workspace** → navigate to the desired folder → **Import**
3. Import both:
   - `Lesson_02_Building_Data_Pipelines.ipynb`
   - `Lesson_03_Self_Service_Analytics_AI.ipynb`

#### Step 4 — Update Notebook Widgets

Before running, update the default widget values in both notebooks:
- **Cell: "Setup: Configure Catalog and Schema"**
  - Change `catalog` default from `serverless_stable_qr9if1_catalog` → `your_catalog_name`
  - Change `VOLUME_PATH` to match your volume location

#### Step 5 — Run Lesson 2 Notebook (Creates All Tables)

Attach to a cluster or serverless compute and **Run All**. This creates:
- 5 Bronze tables (raw ingestion from Volume CSVs)
- 2 Silver tables (cleaned, business rules applied)
- 3 Gold tables (aggregated for dashboards/Genie)
- 1 View (active contracts filter)

#### Step 6 — (Optional) Create the Lakeflow Pipeline

To set up the automated pipeline:
1. Navigate to **Lakeflow Pipelines** → **Create Pipeline**
2. Name: `Enbridge SCM - Preferred Supplier Pipeline`
3. Set catalog and schema to your values
4. Add the three pipeline SQL files as source:
   - `01_bronze.sql`, `02_silver.sql`, `03_gold.sql`
5. Select **Serverless** compute
6. Click **Start** to run the pipeline

#### Step 7 — (Optional) Schedule the Pipeline

1. Navigate to **Lakeflow Jobs** → **Create Job**
2. Add a **Pipeline task** pointing to the pipeline created above
3. Set schedule: daily at 6:00 AM (or as needed)
4. Enable email notifications for failures

---

### Multi-Participant Setup (Workshop Day)

When running a live workshop with multiple participants, each person should have
their own schema to avoid collisions:

```sql
-- Instructor runs once to create per-participant schemas
CREATE SCHEMA IF NOT EXISTS your_catalog_name.enbridge_scm_alice;
CREATE SCHEMA IF NOT EXISTS your_catalog_name.enbridge_scm_bob;
CREATE SCHEMA IF NOT EXISTS your_catalog_name.enbridge_scm_charlie;
-- etc.
```

Participants then set the `schema` widget to their personal schema name
(e.g., `enbridge_scm_alice`) when running the notebooks.

Alternatively, use a naming convention:
```
enbridge_scm_{initials}   e.g., enbridge_scm_jd for John Doe
```

---

### Environment Configuration Reference

| Parameter | Description | Example |
|-----------|------------|--------|
| `catalog` | Unity Catalog catalog name | `enbridge_prod` |
| `schema` | Target schema for all tables | `enbridge_scm` |
| `volume_path` | UC Volume with source CSVs | `/Volumes/enbridge_prod/enbridge_scm/training` |
| `workspace_url` | Databricks workspace URL | `https://enbridge.cloud.databricks.com` |

### Post-Deployment Validation Checklist

- [ ] All 26 CSV files uploaded to UC Volume
- [ ] Schema `enbridge_scm` created with correct catalog
- [ ] Lesson 2 notebook runs without errors (all tables created)
- [ ] Lesson 3 notebook runs without errors (MLflow experiment logged)
- [ ] 10 tables + 1 view visible in Catalog Explorer
- [ ] Lakeflow pipeline runs successfully (if using Option A)
- [ ] Gold tables have expected row counts (see Section 3 table above)
- [ ] Column comments visible on Gold tables (for Genie readiness)
- [ ] Participants can access the schema with their credentials
- [ ] SQL Warehouse available for dashboard queries

### Troubleshooting Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `SCHEMA_NOT_FOUND` | Schema not created yet | Run `CREATE SCHEMA IF NOT EXISTS ...` |
| `VOLUME_NOT_FOUND` | Volume doesn't exist or wrong path | Verify volume path in Catalog Explorer |
| `FILE_NOT_FOUND` in read_files | CSVs not uploaded to volume | Upload files to the correct volume path |
| `_rescued_data` has unexpected values | Schema mismatch in source CSV | Expected for CPA (duplicate Report Date) — this is by design |
| MLflow experiment fails | No cluster/compute attached | Ensure notebook is attached to compute with MLflow installed |
| `ai_gen()` / `ai_extract()` fails | AI functions not enabled | Verify workspace has Foundation Model APIs enabled |
| `PERMISSION_DENIED` on catalog | Insufficient UC permissions | Grant `USE CATALOG`, `USE SCHEMA`, `CREATE TABLE` to user/group |
| Bundle deploy fails | CLI version too old | Upgrade: `pip install databricks-cli --upgrade` (need v0.230+) |