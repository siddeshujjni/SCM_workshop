-- ==========================================================================
-- Enbridge SCM - Bronze Layer (Streaming Tables with Auto Loader)
-- ==========================================================================
-- Ingests raw CSV files from UC Volume into streaming tables.
-- ${volume_path} is set from the pipeline's configuration block.

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
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Agreements - BPA.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_agreements_cpa
COMMENT 'Raw Contract Purchase Agreements from Oracle ENBOAC.'
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Agreements - CPA.csv',
  format => 'csv',
  header => 'true'
);

CREATE OR REFRESH STREAMING TABLE bronze_contracts
COMMENT 'Raw legal contracts from Oracle ENBOAC.'
AS SELECT
  *,
  _metadata.file_name AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${volume_path}/Contracts.csv',
  format => 'csv',
  header => 'true'
);