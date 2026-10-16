-- ==========================================================================
-- Enbridge SCM - Gold Layer (Materialized Views for Dashboards & Genie)
-- ==========================================================================

CREATE OR REFRESH MATERIALIZED VIEW gold_regional_supplier_coverage
COMMENT 'Regional supplier coverage summary by business unit and region. Gold layer for dashboards.'
AS
SELECT
  bu_code,
  business_unit_name,
  region,
  supplier_type,
  COUNT(DISTINCT supplier_number) AS unique_suppliers,
  COUNT(*) AS total_assignments
FROM silver_preferred_suppliers
GROUP BY bu_code, business_unit_name, region, supplier_type;


CREATE OR REFRESH MATERIALIZED VIEW gold_agreement_summary
COMMENT 'Aggregated agreement status summary by type and supplier. Gold layer for executive dashboards.'
AS
SELECT
  document_type,
  agreement_status,
  COUNT(DISTINCT supplier_number) AS unique_suppliers,
  COUNT(DISTINCT agreement_number) AS total_agreements,
  MIN(report_start_date) AS earliest_report_date,
  MAX(report_start_date) AS latest_report_date
FROM silver_agreements
GROUP BY document_type, agreement_status;


CREATE OR REFRESH MATERIALIZED VIEW gold_contract_analytics (
  CONSTRAINT has_business_unit EXPECT (`business_unit` IS NOT NULL)
)
COMMENT 'Contract analytics by business unit, status, and type. Gold layer for spend analysis.'
AS
SELECT
  `Enbridge Business Unit` AS business_unit,
  `Contract Status` AS contract_status,
  `Contract Type` AS contract_type,
  `Contract Classification` AS contract_classification,
  COUNT(*) AS contract_count,
  COUNT(DISTINCT `Contract Party Name`) AS unique_suppliers,
  MIN(`Contract Start Date`) AS earliest_start,
  MAX(`Contract End Date`) AS latest_end
FROM bronze_contracts
WHERE `Enbridge Business Unit` IS NOT NULL
GROUP BY ALL;