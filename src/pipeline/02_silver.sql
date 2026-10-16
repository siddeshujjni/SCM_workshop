-- ==========================================================================
-- Enbridge SCM - Silver Layer (Materialized Views + Expectations)
-- ==========================================================================
-- Cleans, unifies, and applies Enbridge business rules (R1-R5).

CREATE OR REFRESH MATERIALIZED VIEW silver_preferred_suppliers (
  CONSTRAINT valid_supplier_number EXPECT (supplier_number IS NOT NULL)
    ON VIOLATION DROP ROW,
  CONSTRAINT valid_supplier_name EXPECT (supplier_name IS NOT NULL AND TRIM(supplier_name) != '')
    ON VIOLATION DROP ROW,
  CONSTRAINT known_business_unit EXPECT (bu_code IN ('LP', 'GTM', 'GDS', 'GPT'))
    ON VIOLATION FAIL UPDATE
)
COMMENT 'Unified preferred suppliers with BU name resolution (Rule R4) and data quality enforcement.'
AS
SELECT
  supplier_name,
  CAST(supplier_number AS INT) AS supplier_number,
  business_unit AS bu_code,
  -- Business Rule R4: Map BU code to full name
  CASE business_unit
    WHEN 'LP'  THEN 'Liquids Pipelines'
    WHEN 'GTM' THEN 'Gas Transmission'
    WHEN 'GDS' THEN 'Enbridge Gas'
    WHEN 'GPT' THEN 'Power Operations'
    ELSE business_unit
  END AS business_unit_name,
  region,
  'Category Managed' AS supplier_type,
  source_file
FROM bronze_category_managed

UNION ALL

SELECT
  supplier_name,
  CAST(supplier_number AS INT) AS supplier_number,
  business_unit AS bu_code,
  CASE business_unit
    WHEN 'LP'  THEN 'Liquids Pipelines'
    WHEN 'GTM' THEN 'Gas Transmission'
    WHEN 'GDS' THEN 'Enbridge Gas'
    WHEN 'GPT' THEN 'Power Operations'
    ELSE business_unit
  END AS business_unit_name,
  region,
  'Regional Sourcing' AS supplier_type,
  source_file
FROM bronze_regional_sourcing;


CREATE OR REFRESH MATERIALIZED VIEW silver_agreements (
  CONSTRAINT valid_supplier EXPECT (supplier_number IS NOT NULL)
    ON VIOLATION DROP ROW,
  CONSTRAINT valid_agreement EXPECT (agreement_number IS NOT NULL)
    ON VIOLATION DROP ROW
)
COMMENT 'Unified BPA and CPA agreements. Silver layer with standardized schema.'
AS
WITH bpa AS (
  SELECT
    `Document Type` AS document_type,
    CAST(`Supplier Number` AS INT) AS supplier_number,
    `Supplier` AS supplier_name,
    `Site` AS site,
    `Agreement Number` AS agreement_number,
    `Agreement Status Lookup Code` AS agreement_status,
    `Report Date` AS report_start_date,
    `Preferred Status` AS preferred_status,
    source_file
  FROM bronze_agreements_bpa
),
cpa AS (
  SELECT
    `Document Type` AS document_type,
    CAST(`Supplier Number` AS INT) AS supplier_number,
    `Supplier` AS supplier_name,
    `Site` AS site,
    `Agreement Number` AS agreement_number,
    `Agreement Status Lookup Code` AS agreement_status,
    `Report Date` AS report_start_date,
    `Preferred Status` AS preferred_status,
    source_file
  FROM bronze_agreements_cpa
)
SELECT * FROM bpa
UNION ALL
SELECT * FROM cpa;