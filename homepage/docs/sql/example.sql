/***************************************************************************************************
  _______           _            ____          _
 |__   __|         | |          |  _ \        | |
    | |  __ _  ___ | |_  _   _  | |_) | _   _ | |_  ___  ___
    | | / _` |/ __|| __|| | | | |  _ < | | | || __|/ _ \/ __|
    | || (_| |\__ \| |_ | |_| | | |_) || |_| || |_|  __/\__ \
    |_| \__,_||___/ \__| \__, | |____/  \__, | \__|\___||___/
                          __/ |          __/ |
                         |___/          |___/
Demo:         Tasty Bytes
Version:      v1.1
Vignette:     Financial Governance
Create Date:  2023-01-13
Author:       Jacob Kranzler
Copyright(c): 2023 Snowflake Inc. All rights reserved.
****************************************************************************************************
Description:

    Financial Governance
    1 - Virtual Warehouses and Settings
    2 - Resource Monitors
    3 - Timeout Parameters - Session
    4 - Timeout Parameters - Account
    5 - Manual WH Suspend

****************************************************************************************************
SUMMARY OF CHANGES
Date(yyyy-mm-dd)    Author              Comments
------------------- ------------------- ------------------------------------------------------------
2023-01-13          Jacob Kranzler      Initial Release
2023-02-16          Jacob Kranzler      Adjusted WHERE clause in first query in Step 5
2023-06-20          Luke Crumley        Convert to use DataOps.live template variables
***************************************************************************************************/

/*----------------------------------------------------------------------------------
Step 1 -
 As a Tasty Bytes Snowflake Administrator we have been tasked with gaining an
 understanding of the features Snowflake provides to help ensure proper
 Financial Governance is in place before we begin querying and analyzing data.

 Let's get started by creating our first Warehouse.
----------------------------------------------------------------------------------*/

-- first set our role and warehouse context
USE ROLE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_admin;
USE WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_de_wh;


-- to start, let's look at all of the warehouses available in our account
-- by running a SHOW command and look at some of the columns returned.
  --> demo tip: to execute a query use the top-right ▶️ button or press COMMAND/CONTROL + ENTER
SHOW WAREHOUSES LIKE '%tasty%';


-- having seen the various settings a Snowflake Virtual Warehouse can have, let's create our own
-- {{ DATAOPS_CATALOG_SOLUTION_PREFIX }}_TEST_WH and read through what each parameter is handling.
CREATE OR REPLACE WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh WITH
COMMENT = 'test warehouse for tasty bytes'
    WAREHOUSE_TYPE = 'standard'
    WAREHOUSE_SIZE = 'xsmall'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 2
    SCALING_POLICY = 'standard'
    AUTO_SUSPEND = 60
    AUTO_RESUME = true
    INITIALLY_SUSPENDED = true;

    /**
     1) WAREHOUSE_TYPE: Warehouses are required for queries, as well as all DML operations, including
         loading data into tables. Snowflake supports Standard (most-common) or Snowpark-optimized
          Warehouse Types.

     2) WAREHOUSE_SIZE: Size specifies the amount of compute resources available per cluster in a warehouse.
         Snowflake supports X-Small through 6X-Large sizes.

     3) MIN/MAX_CLUSTER_COUNT: With multi-cluster warehouses, Snowflake supports allocating, either statically
         or dynamically, additional clusters to make a larger pool of compute resources available.
         A multi-cluster warehouse is defined by specifying the following properties:
            - MIN_CLUSTER_COUNT: Minimum number of clusters, equal to or less than the maximum (up to 10).
            - MAX_CLUSTER_COUNT: Maximum number of clusters, greater than 1 (up to 10).

     4) SCALING_POLICY: Specifies the policy for automatically starting and shutting down clusters in a
         multi-cluster warehouse running in Auto-scale mode.

     5) AUTO_SUSPEND: By default, Auto-Suspend is enabled. Snowflake automatically suspends the warehouse
         if it is inactive for the specified period of time, in our case 60 seconds.

     6) AUTO_RESUME: By default, auto-resume is enabled. Snowflake automatically resumes the warehouse
         when any statement that requires a warehouse is submitted and the warehouse is the
         current warehouse for the session.

     7) INITIALLY_SUSPENDED: Specifies whether the warehouse is created initially in the ‘Suspended’ state.
    **/


/*----------------------------------------------------------------------------------
Step 2 -
 With a Warehouse in place, let's now leverage Snowflakes Resource Monitors to ensure
 the Warehouse has a monthly quota that will allow our admins to track it's
 consumed credits and ensure it is suspended if it exceeds it's assigned quota.
----------------------------------------------------------------------------------*/

    /**
     RESOURCE MONITOR: A resource monitor can be used to monitor credit usage by virtual warehouses
       and the cloud services needed to support those warehouses. If desired, the warehouse can be
       suspended when it reaches a credit limit.
    **/

-- assume the role of accountadmin
USE ROLE accountadmin;

-- now we can create our resource monitor
CREATE OR REPLACE RESOURCE MONITOR {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_rm
WITH
    CREDIT_QUOTA = 100 -- 100 credits
    FREQUENCY = monthly -- reset the monitor monthly
    START_TIMESTAMP = immediately -- begin tracking immediately
    TRIGGERS
        ON 75 PERCENT DO NOTIFY -- notify accountadmins at 75%
        ON 100 PERCENT DO SUSPEND -- suspend warehouse at 100 percent, let queries finish
        ON 110 PERCENT DO SUSPEND_IMMEDIATE; -- suspend warehouse and cancel all queries at 110 percent


-- with the Resource Monitor created let's now apply it to our {{ DATAOPS_CATALOG_SOLUTION_PREFIX }}_TEST_WH
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh SET RESOURCE_MONITOR = {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_rm;


/*----------------------------------------------------------------------------------
Step 3 -
 With monitoring in place, let's now make sure we are protecting ourselves from bad,
 long running queries ensuring timeout parameters are adjusted on the Warehouse
----------------------------------------------------------------------------------*/

-- to begin, let's look at a few parameters available on our Warehouse
SHOW PARAMETERS IN WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh;

-- above we saw three available parameters, let's start by adjusting the two related to timeouts

    /**
     STATEMENT_TIMEOUT_IN_SECONDS: Timeout in seconds for statements: statements are automatically canceled if they
      run for longer; if set to zero, max value (604800) is  enforced.

     STATEMENT_QUEUED_TIMEOUT_IN_SECONDS: Timeout in seconds for queued statements: statements will automatically be
      canceled if they are queued on a warehouse for longer than this  amount of time; disabled if set to zero.
    **/


-- adjust STATEMENT_TIMEOUT_IN_SECONDS on WAREHOUSE to 30 minutes
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh
SET statement_timeout_in_seconds = 1800; -- 1800 seconds = 30 minutes


-- adjust STATEMENT_QUEUED_TIMEOUT_IN_SECONDS on WAREHOUSE to 10 minutes
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh
SET statement_queued_timeout_in_seconds = 600; -- 600 seconds = 10 minutes


/*----------------------------------------------------------------------------------
Step 4 -
 These timeout parameters are also available at the Account, User and Session level.
 As we do not expect any extremely long running queries let's also adjust these
 parameters on our Account.

 Moving forward we will plan to monitor these as our Snowflake Workloads and Usage
 grow to ensure they are continuing to protect our account from unneccesary consumption
 but also not cancelling longer jobs we expect to be running.
----------------------------------------------------------------------------------*/

-- adjust STATEMENT_TIMEOUT_IN_SECONDS on ACCOUNT to 5 hours
ALTER ACCOUNT
SET statement_timeout_in_seconds = 18000; -- 18000 seconds = 5 hours


-- adjust STATEMENT_QUEUED_TIMEOUT_IN_SECONDS on ACCOUNT to 1 hour
ALTER ACCOUNT
SET statement_queued_timeout_in_seconds = 3600; -- 3600 seconds = 1 hour;


/*----------------------------------------------------------------------------------
Step 5 -
 Now let's use the Warehouse we've created and test manually suspending it before
 ultimately dropping it as we complete our testing.
----------------------------------------------------------------------------------*/

-- with the warehouse created, let's now USE it and execute our first query
USE ROLE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_admin;
USE WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh;

SELECT
    m.menu_type,
    m.truck_brand_name,
    m.menu_item_id,
    m.menu_item_name
FROM {{ DATAOPS_DATABASE | lower }}.raw_pos.menu m
WHERE truck_brand_name = 'Plant Palace';


-- to showcase Snowflakes instant scalability let's scale our warehouse up
-- and run a few larger, more complex query against nearly 1 billion rows
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh SET warehouse_size = 'XLarge';


-- calculate orders and total sales for truck brand names
SELECT
    o.truck_brand_name,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.price) AS total_sales
FROM {{ DATAOPS_DATABASE | lower }}.analytics.orders_v o
GROUP BY o.truck_brand_name
ORDER BY total_sales DESC;


-- calculate orders and total sales for our customer loyalty members
SELECT
    o.customer_id,
    CONCAT(clm.first_name, ' ', clm.last_name) AS name,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.price) AS total_sales
FROM {{ DATAOPS_DATABASE | lower }}.analytics.orders_v o
JOIN {{ DATAOPS_DATABASE | lower }}.analytics.customer_loyalty_metrics_v clm
    ON o.customer_id = clm.customer_id
GROUP BY o.customer_id, name
ORDER BY order_count DESC;


-- let's now scale our warehouse back down
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh SET warehouse_size = 'XSmall';


-- based on our AUTO_SUSPEND setting from earlier the Warehouse will automatically turn off in 60 seconds
-- unless another query is issued. let's instead manually suspend it to get a feel of how it works
ALTER WAREHOUSE {{ DATAOPS_CATALOG_SOLUTION_PREFIX | lower }}_test_wh SUSPEND;

    /*--
     "Invalid state. Warehouse cannot be suspended." - AUTO_SUSPEND already occured
    --*/
