from globals import *
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
from utils.resources import get_facebook_icon, get_linkedin_icon, get_google_ads_icon, get_salesforce_icon, get_fivetran_icon, get_omnata_icon
from utils.model_helpers import execute_sql_query


blocked_providers = [3, 4] # Google Ads and SalesForce

provider_images = {
    1 : get_facebook_icon(),
    2 : get_linkedin_icon(),
    3 : get_google_ads_icon(),
    4 : get_salesforce_icon()
}

connector_images = {
    1 : get_fivetran_icon(),
    2 : get_omnata_icon()
}

def get_providers_info(sp_session: Session)-> list:
    providers_table = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, PROVIDERS_TABLE]).collect()
    providers_info = []
    for row in providers_table:
        provider_info = generate_provider_info_dict(row[ID_KEY], row[NAME_KEY], provider_images[row[ID_KEY]])
        providers_info.append(provider_info)
    return providers_info


def get_existing_sources_info(sp_session: Session)-> list:
    existing_sources_table = sp_session.table([APPLICATION, USER_SETTINGS_SCHEMA, EXISTING_SOURCES_TABLE]).collect()
    providers = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, PROVIDERS_TABLE])
    connectors = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, CONNECTORS_TABLE])
    existing_sources_info = []
    for row in existing_sources_table:
        provider_name = providers.where(col(ID_KEY)==row[PROVIDER_ID_KEY]).collect()\
                                                    [0].__getitem__(NAME_KEY)
        connector_name = connectors.where(col(ID_KEY)==row[CONNECTOR_ID_KEY]).collect()\
                                                    [0].__getitem__(NAME_KEY)
        connector_image = connector_images[row[CONNECTOR_ID_KEY]]
        provider_image = provider_images[row[PROVIDER_ID_KEY]]

        source_info = generate_existing_source_dict(provider_name, provider_image, connector_name, connector_image, row[DATABASE_KEY], row[SCHEMA_KEY], row[CREATED_DATE_KEY])
        existing_sources_info.append(source_info)
    return existing_sources_info


def generate_provider_info_dict(provider_id: int, provider_name: str, provider_image: str)-> dict:
    provider_info = {
        ID_KEY   : provider_id,
        NAME_KEY : provider_name,
        IMAGE_KEY : provider_image
    }
    return provider_info

def generate_existing_source_dict(provider_name: str, provider_image: str, connector_name: str, connector_image: str, database_name: str, schema_name: str, created_date: str)-> dict:
    existing_source_info = {
        PROVIDER_NAME_KEY      : provider_name,
        PROVIDER_IMAGE_KEY     : provider_image,
        CONNECTOR_NAME_KEY     : connector_name,
        CONNECTOR_IMAGE_KEY    : connector_image,
        DATABASE_NAME_KEY      : database_name,
        SCHEMA_NAME_KEY        : schema_name,
        CREATED_DATE_KEY       : format_datetime(created_date)
    }
    return existing_source_info

def format_datetime(datetime):
    formatted_result = datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_result

def get_provider_id_by_name(sp_session, connector_name):
    provider_id_query = f"SELECT {ID_KEY} FROM {APPLICATION}.{CONFIGURATION_SCHEMA}.{PROVIDERS_TABLE} WHERE {NAME_KEY} = '{connector_name}'"
    provider_id_result = execute_sql_query(sp_session, provider_id_query)
    provider_id = provider_id_result[0][ID_KEY]
    return provider_id