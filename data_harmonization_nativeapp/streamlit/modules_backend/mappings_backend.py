import json
from globals import *
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
from dtos.dynamic_table import DynamicTableParams
from utils.model_helpers import connect_to_snowflake



def call_grant(tables: list, schema: str,sp_session: Session):
    sp_session.call(f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{GRANTER_KEY}", APPLICATION, schema, tables)


def get_template(connector: str,provider: str, target_table: str, sp_session: Session)-> dict:
    query_templates = json.loads(sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, QUERY_TEMPLATES_TABLE]).first()[0])
    return query_templates[SOURCE_QUERIES_KEY][connector][provider][target_table]



def get_columns_definition(table: str, sp_session: Session)-> str:
    col_definition = sp_session.table([APPLICATION, CONFIGURATION_SCHEMA, DYNAMIC_TABLES_DEFINITION_TABLE])\
                         .where(col(NAME_KEY)==table).collect()
    
    if len(col_definition) > 0:
        return str(col_definition[0].__getitem__(COLUMNS_KEY))
    else:
        return None


def generate_unified_model(dynamic_tables_params: DynamicTableParams) -> None:

    
    sp_session = connect_to_snowflake()

    connector,provider,database,schema = dynamic_tables_params.values()
    query_header = json.loads(sp_session.table([APPLICATION,CONFIGURATION_SCHEMA,QUERY_TEMPLATES_TABLE]).first()[0])[HEADER_KEY]
    target_tables = list(json.loads(sp_session.table([APPLICATION,CONFIGURATION_SCHEMA,QUERY_TEMPLATES_TABLE]).first()[0])\
                                                                                [SOURCE_QUERIES_KEY][connector][provider].keys())

    existing_tables = [row[0].lower() for row in sp_session.table([APPLICATION, INFORMATION_SCHEMA, TABLES_TABLE])\
                                                            .where(col(TABLE_SCHEMA_COLUMN)==UNIFIED_MODEL_SCHEMA)\
                                                            .select(col(TABLE_NAME_KEY)).collect()]
    
    for table in target_tables:

        if table in existing_tables:
            table_ddl = sp_session.sql(f"select GET_DDL('{DYNAMIC_TABLE_KEY}' ,'{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.{table}')").first()[0]\
                                        .replace(";","").replace(table.upper(), f"{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.{table}")
            table_ddl += "\nunion all\n" + get_template(connector,provider,table,sp_session).replace(DATABASE_KEY, database)\
                                        .replace(SCHEMA_KEY,schema).replace(APPLICATION_KEY, APPLICATION)
            try:
                sp_session.call(f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{CREATE_DYNAMIC_TABLE_KEY}", 
                                                      f"{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.{table}", 
                                                      table_ddl)
                
            except:
                continue #TODO Error handling
        else:
            col_definition = get_columns_definition(table.upper(), sp_session)
            if col_definition is not None:
                table_ddl = query_header.replace(TABLE_NAME_KEY, table).replace(COLUMNS_DEFINITION_KEY, col_definition)\
                                                                       .replace(APPLICATION_KEY, APPLICATION).replace(TAG_KEY,TAG)
                table_ddl+= get_template(connector,provider,table,sp_session).replace(DATABASE_KEY, database)\
                                                                            .replace(APPLICATION_KEY, APPLICATION)\
                                                                            .replace(SCHEMA_KEY,schema)
                                                                            

                try:
                    sp_session.call(f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{CREATE_DYNAMIC_TABLE_KEY}", 
                                                      f"{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.{table}", 
                                                      table_ddl)
                except:
                    
                    continue #TODO Error handling
    
    call_grant([x for x in target_tables if x not in existing_tables], UNIFIED_MODEL_SCHEMA, sp_session)
  

def generate_aggregated_model()-> None:
    sp_session = connect_to_snowflake()
    existing_tables = [row[0].lower() for row in sp_session.table([APPLICATION, INFORMATION_SCHEMA, TABLES_TABLE])\
                       .where(col(TABLE_SCHEMA_COLUMN)==AGGREGATED_REPORTS_KEY)\
                       .select(col(TABLE_NAME_KEY)).collect()]
    table_ddls = json.loads(sp_session.table([APPLICATION,CONFIGURATION_SCHEMA,QUERY_TEMPLATES_TABLE])\
                                                .first()[0])[AGGREGATED_REPORTS_KEY]

    reports = [report for report in table_ddls if report not in existing_tables]
    for report in reports:

        table_ddl = table_ddls[report].replace(AGGREGATED_REPORTS_KEY, f"{APPLICATION}.{AGGREGATED_REPORTS_KEY}")\
                                    .replace(f"{UNIFIED_MODEL_SCHEMA}.",f"{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.")\
                                    .replace(TAG_KEY,TAG)
     
        try:
            sp_session.call(f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{CREATE_DYNAMIC_TABLE_KEY}", 
                                                      f"{APPLICATION}.{AGGREGATED_REPORTS_KEY}.{report}", 
                                                      table_ddl)
        except:

            continue #TODO Error handling

    call_grant(reports, AGGREGATED_REPORTS_KEY, sp_session)

def generate_standardize_model(dynamic_tables_params: DynamicTableParams) -> None:
    connector,provider,database,schema = dynamic_tables_params.values()

    provider = provider.upper()

    sp_session = connect_to_snowflake()
    

    table_ddls = json.loads(sp_session.table([APPLICATION,CONFIGURATION_SCHEMA,QUERY_TEMPLATES_TABLE]).first()[0])[STANDARDIZE_MODEL_KEY][provider]
    for table in table_ddls:
        table_ddl = table_ddls[table].replace(STANDARDIZE_MODEL_KEY, f"{APPLICATION}.{STANDARDIZE_MODEL_KEY}")\
                                    .replace(f"{UNIFIED_MODEL_SCHEMA}.",f"{APPLICATION}.{UNIFIED_MODEL_SCHEMA}.")\
                                    .replace(DATABASE_KEY, database).replace(SCHEMA_KEY,schema)\
                                    .replace(TAG_KEY,TAG)
        try:
            sp_session.call(f"{APPLICATION}.{USER_SETTINGS_SCHEMA}.{CREATE_DYNAMIC_TABLE_KEY}", 
                                                      f"{APPLICATION}.{STANDARDIZE_MODEL_KEY}.{table}", 
                                                      table_ddl)
        except:

            continue #TODO Error handling
    
    call_grant([table for table in table_ddls],STANDARDIZE_MODEL_KEY, sp_session)
def get_columns_info_schema(sp_session, source_db: str, source_schema: str) -> 'DataFrame':
    get_cols_query = f"""
    select TABLE_NAME, COLUMN_NAME 
    FROM {source_db}.INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = '{source_schema}';
    """
    return sp_session.sql(get_cols_query).collect()
