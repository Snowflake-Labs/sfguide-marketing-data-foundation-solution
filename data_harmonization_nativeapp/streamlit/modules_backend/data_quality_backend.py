from utils.model_helpers import connect_to_snowflake


def notebook_urls():
    sp_session = connect_to_snowflake()
    account_name = sp_session.sql("SELECT CURRENT_ACCOUNT_NAME()").collect()[0].__getitem__("CURRENT_ACCOUNT_NAME()")
    org_name = sp_session.sql("SELECT CURRENT_ORGANIZATION_NAME()").collect()[0].__getitem__("CURRENT_ORGANIZATION_NAME()")
    urls = {1 : f"https://app.snowflake.com/{org_name}/{account_name}/#/notebooks/LLM_DEMO.DEMO.DATA_QUALITY_DEMO_1",
            2 : f"https://app.snowflake.com/{org_name}/{account_name}/#/notebooks/LLM_DEMO.DEMO.DATA_QUALITY_DEMO_2",
            3 : f"https://app.snowflake.com/{org_name}/{account_name}/#/notebooks/LLM_DEMO.DEMO.DATA_QUALITY_DEMO_3"
            
            }
    return urls
