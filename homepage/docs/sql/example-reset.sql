/**********************************************************************/
/*------               Vignette Reset Scripts                   ------*/
/**********************************************************************/

USE ROLE accountadmin;
ALTER ACCOUNT SET statement_timeout_in_seconds = default;
ALTER ACCOUNT SET statement_queued_timeout_in_seconds = default;
DROP WAREHOUSE IF EXISTS {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh;
DROP RESOURCE MONITOR IF EXISTS {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_rm;