-- ==========================================================================
-- Enbridge SCM - Bronze Layer (Streaming Tables with Auto Loader)
-- ==========================================================================
-- Ingests raw CSV files from UC Volume into streaming tables.
-- ${volume_path} = original training volume (Agreements, Contracts, Category Managed CSVs)
-- ${volume_path_psl} = enriched PSL Dashboard volume (Supplier Headers, Contract Mapping, etc.)

-- ============================================================
-- ORIGINAL BRONZE TABLES (from training volume)
-- ============================================================

CREATE OR REFRESH STREAMING TABLE bronze_category_managed
COMMENT 'Raw category-managed suppliers ingested incrementally from UC Volume. Source: Oracle ENBOAC.'
AS SELECT
  `Supplier Name`  AS supplier_name,
  `Supplier Number` AS supplier_number,
  `Business Unit`   AS business_unit,
  `Region`          AS region,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/*Category Managed*.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_regional_sourcing
COMMENT 'Raw regional sourcing suppliers ingested incrementally from UC Volume.'
AS SELECT
  `Supplier Name`  AS supplier_name,
  `Supplier Number` AS supplier_number,
  `Business Unit`   AS business_unit,
  `Region`          AS region,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/*Regional Sourcing*.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_agreements_bpa
COMMENT 'Raw Blanket Purchase Agreements from Oracle ENBOAC.'
-- CSV headers contain spaces; column mapping lets Delta keep them as-is
TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Agreements - BPA*.csv',  -- streaming read_files needs a directory or glob, not a single file
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_agreements_cpa
COMMENT 'Raw Contract Purchase Agreements from Oracle ENBOAC.'
TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Agreements - CPA*.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_contracts
COMMENT 'Raw legal contracts from Oracle ENBOAC.'
TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Contracts*.csv',
  format => 'csv',
  header => 'true'
);

-- ============================================================
-- ENRICHED BRONZE TABLES (from PSL Dashboard volume)
-- ============================================================

CREATE OR REFRESH STREAMING TABLE bronze_supplier_headers
COMMENT 'Comprehensive supplier dimension from Oracle Cloud (29,909 suppliers). Source: PSL Dashboard export.'
AS SELECT
  `Supplier Name`    AS supplier_name,
  `Supplier Number` AS supplier_number,
  `Status`          AS supplier_status,
  `Relationship`    AS supplier_relationship,
  `ISN#`           AS isn_number,
  `Registry ID`     AS registry_id,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path_psl}/Supplier Header Info*.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_contract_mapping
COMMENT 'Contract-to-supplier mapping by BU, region, and L3 category. Source: PSL Dashboard export (3 regional CSVs).'
AS SELECT
  `Business Unit`    AS business_unit,
  `Region`           AS region,
  `Supplier Name`    AS supplier_name,
  `Supplier Number`  AS supplier_number,
  `Contract Number`  AS contract_number,
  `L3 Category`     AS l3_category,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path_psl}/*Contract Mapping*.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_supplier_responses
COMMENT 'Supplier responses to Enbridge Standard Terms and Conditions. Source: PSL Dashboard export.'
AS SELECT
  `Supplier Number`   AS supplier_number,
  `Supplier Name`     AS supplier_name,
  `ServiceNow Number` AS servicenow_number,
  `Question Name`     AS question_name,
  `Response Value`    AS response_value,
  `Response Date`     AS response_date,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path_psl}/Enbridge Standard Terms and Conditions*.csv',
  format => 'csv',
  header => 'true'
);

-- Note: Excel sources (Output1.xlsx, Cost Centers, ISN Mapping, Region Mapping, CM Supplier Lists)
-- are loaded in the Lesson 2 notebook with read_files(format => 'excel'). Excel headers contain
-- spaces, so columns must be renamed to snake_case before writing to Delta.