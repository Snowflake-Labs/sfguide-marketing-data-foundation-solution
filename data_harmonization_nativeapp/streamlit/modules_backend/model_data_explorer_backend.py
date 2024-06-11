import pandas as pd
import streamlit as st
from globals import *
from modules.pages import get_page_params
from utils.model_helpers import connect_to_snowflake
from snowflake.snowpark.functions import col, sum as sum_, iff, lit, monthname, year, concat, month, to_date, round as round_

# TODO the plataform column should be replace to use linkedin and facebook data
def get_spend_by_year(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql("""WITH spend_data AS
    (
            SELECT  Date_part('YEAR', date)    AS year_data,
                    platform_name,
                    Sum(spend)::FLOAT          AS overall_spend
            FROM    Identifier(:1)
            GROUP BY 1,
                    2
            ORDER BY year_data)
    SELECT   year_data,
            "'facebook'" AS facebook,
            "'linkedin'" AS linkedin
    FROM     spend_data PIVOT(Sum(overall_spend) FOR platform_name IN ('facebook',
                                                                'linkedin')) AS p
    ORDER BY year_data""", params=[f'{app_db}.{app_sch}.{table_name}']).collect()
    df = pd.DataFrame(df_out)
    return df

def get_impressions_by_year(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql("""WITH spend_data AS
(
         SELECT   Date_part('YEAR', date) AS year_data,
                  platform_name,
                  Sum(impressions)::FLOAT AS overall_impressions
         FROM     Identifier(:1)
         GROUP BY 1,
                  2
         ORDER BY year_data)
SELECT   year_data,
         "'facebook'" AS facebook,
         "'linkedin'" AS linkedin
FROM     spend_data PIVOT(Sum(overall_impressions) FOR platform_name IN ('facebook',
                                                                    'linkedin')) AS p
ORDER BY year_data""", params=[f'{app_db}.{app_sch}.{table_name}']).collect()
    df = pd.DataFrame(df_out)
    return df

def get_account_spend_by_year(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql(f"""WITH spend_data AS (
    SELECT
        Date_part ('YEAR', date) AS year_data,
        account_name,
        Sum(spend)::FLOAT AS overall_spend
    FROM
        {app_db}.{app_sch}.{table_name}
    GROUP BY
        1,
        2
    ORDER BY
        year_data
)
SELECT
    *
FROM
    spend_data PIVOT (
        Sum(overall_spend) FOR account_name IN (ANY ORDER BY account_name)
    ) AS p
ORDER BY
    year_data""").collect()
    df = pd.DataFrame(df_out)
    return df

def get_account_with_spend(_sp_session, app_db, app_sch, table_name):
    df = _sp_session.table([app_db, app_sch, table_name])\
        .withColumnRenamed('account_name', 'Account Name')\
        .groupBy('Account Name').agg(sum_('spend').alias("Overall spend")).toPandas()
    return df

def get_total_spend(_sp_session, app_db, app_sch, table_name):
   total_spend = _sp_session.sql("SELECT Sum(spend) AS overall_spend FROM Identifier(:1) ", params=[f'{app_db}.{app_sch}.{table_name}']).collect()[0][0]
   return total_spend

def get_spend_per_day(_sp_session, app_db, app_sch, table_name):
    df = _sp_session.table([app_db, app_sch, table_name]).withColumn(MONTH_YEAR_COLUMN,concat(monthname(DATE_COLUMN),lit("-"), year(DATE_COLUMN)))\
                        .orderBy(col(DATE_COLUMN).asc())\
                        .withColumn(MONTH_COLUMN, month(DATE_COLUMN))\
                        .withColumn(YEAR_COLUMN, year(DATE_COLUMN))\
                        .group_by(col(MONTH_YEAR_COLUMN), col(MONTH_COLUMN), col(YEAR_COLUMN)).agg(sum_(SPEND_COLUMN).alias(SPEND_COLUMN))\
                        .withColumn(SORT_DATE_COLUMN, to_date(concat(col(YEAR_COLUMN), lit("-"), col(MONTH_COLUMN)), "yyyy-MM"))\
                        .orderBy(col(SORT_DATE_COLUMN).asc())\
                        .na.fill(0)\
                        .select(col(MONTH_YEAR_COLUMN).alias(DATE_COLUMN), round_(col(SPEND_COLUMN),1).alias(SPEND_COLUMN))\
                        .toPandas()

    return df

def get_clicks_per_day(_sp_session, app_db, app_sch, table_name):
    df = _sp_session.table([app_db, app_sch, table_name]).withColumn(MONTH_YEAR_COLUMN,concat(monthname(DATE_COLUMN),lit("-"), year(DATE_COLUMN)))\
                        .orderBy(col(DATE_COLUMN).asc())\
                        .withColumn(MONTH_COLUMN, month(DATE_COLUMN))\
                        .withColumn(YEAR_COLUMN, year(DATE_COLUMN))\
                        .group_by(col(MONTH_YEAR_COLUMN), col(MONTH_COLUMN), col(YEAR_COLUMN)).agg(sum_(CLICKS_COLUMN).alias(CLICKS_COLUMN))\
                        .withColumn(SORT_DATE_COLUMN, to_date(concat(col(YEAR_COLUMN), lit("-"), col(MONTH_COLUMN)), "yyyy-MM"))\
                        .orderBy(col(SORT_DATE_COLUMN).asc())\
                        .na.fill(0)\
                        .select(col(MONTH_YEAR_COLUMN).alias(DATE_COLUMN), round_(col(CLICKS_COLUMN),1).alias(CLICKS_COLUMN))\
                        .toPandas()
    return df

def get_spend_per_clicks(_sp_session, app_db, app_sch, table_name):
    df = _sp_session.table([app_db, app_sch, table_name]).withColumn(MONTH_YEAR_COLUMN,concat(monthname(DATE_COLUMN),lit("-"), year(DATE_COLUMN)))\
                        .orderBy(col(DATE_COLUMN).asc())\
                        .withColumn(MONTH_COLUMN, month(DATE_COLUMN))\
                        .withColumn(YEAR_COLUMN, year(DATE_COLUMN))\
                        .group_by(col(MONTH_YEAR_COLUMN), col(MONTH_COLUMN), col(YEAR_COLUMN)).agg(sum_(SPEND_COLUMN).alias(SPEND_COLUMN), sum_(CLICKS_COLUMN).alias(CLICKS_COLUMN))\
                        .withColumn(SORT_DATE_COLUMN, to_date(concat(col(YEAR_COLUMN), lit("-"), col(MONTH_COLUMN)), "yyyy-MM"))\
                        .orderBy(col(SORT_DATE_COLUMN).asc())\
                        .na.fill(0)\
                        .withColumn(SPEND_PER_CLICKS_COLUMN, iff(col(CLICKS_COLUMN)== lit(0), lit(0), col(SPEND_COLUMN) / col(CLICKS_COLUMN)))\
                        .select(col(MONTH_YEAR_COLUMN).alias(DATE_COLUMN), round_(col(SPEND_PER_CLICKS_COLUMN),1).alias(SPEND_PER_CLICKS_COLUMN))\
                        .toPandas()
    return df


def get_top_5_spend_per_clicks(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql("""SELECT   IFNULL(CAMPAIGN_NAME, '-') AS "Campaign name",
        DIV0NULL(Sum(spend), Sum(CLICKS)) AS SPEND_PER_CLICKS
FROM     Identifier(:1)
GROUP BY 1
ORDER BY spend_per_clicks DESC limit 5""", params=[f'{app_db}.{app_sch}.{table_name}']).collect()
    df = pd.DataFrame(df_out)
    return df

def get_top_5_ad_groups_with_impressions(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql("""SELECT   IFNULL(AD_GROUP_NAME, '-') AS "Ad Group name",
         Sum(impressions) AS impressions
FROM     Identifier(:1)
GROUP BY 1
ORDER BY impressions DESC limit 5""", params=[f'{app_db}.{app_sch}.{table_name}']).collect()
    df = pd.DataFrame(df_out)
    return df

def get_top_5_ad_groups_with_clicks(_sp_session, app_db, app_sch, table_name):
    df_out = _sp_session.sql("""SELECT   IFNULL(AD_GROUP_NAME, '-') AS "Ad Group name",
         Sum(CLICKS) AS clicks
FROM     Identifier(:1)
GROUP BY 1
ORDER BY clicks DESC limit 5""", params=[f'{app_db}.{app_sch}.{table_name}']).collect()
    df = pd.DataFrame(df_out)
    return df

def format_num(num):
    if num >= 10**12:
        return f"{num / 10**12:.2f}T"
    elif num >= 10**9:
        return f"{num / 10**9:.2f}B"
    elif num >= 10**6:
        return f"{num / 10**6:.2f}M"
    elif num >= 1000:
        return f"{num / 1000:.2f}K"
    else:
        return str(round(num, 2))

def get_model_information():
    model_information = st.session_state[MODEL_INFORMATION_KEY] if MODEL_INFORMATION_KEY in st.session_state else None
    return model_information

def get_value_index(elemets_list, value):
    for element in elemets_list:
        if element[0] == value.upper():
            return elemets_list.index(element)
    return 0