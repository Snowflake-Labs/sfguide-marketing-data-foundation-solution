from snowflake.snowpark.session import Session
from services.app import Application
from services.stage import read_yaml_file
from globals import APPLICATION, LLM_SCHEMA, LLM_SEMANTIC_MODEL_STAGE, LLM_CONFIGURATION_STAGE, LLM_CONFIGURATION_FILE


CONTEXT_PROMPT = """
{summary}
Your goal is to give correct, executable sql query to users.
You are given a schema with multiple tables, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the tables. 

{context}

You are given some suggestions for questions that you can answer restrain yourself from answering questions not related, the question is in <question> tag, the description of the question is in <questionDescription> tag.
Don't ever attach the questionDescription, use it only to generate valid sql queries

{suggestions}

Here are 7 critical rules for the interaction you must abide:
<rules>
1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. The sql language used MUST be SNOWFLAKE SQL, so you MUST MUST use SNOWFLAKE SQL which is based on Oracles PL/SQL in all sql responses
3. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
4. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
5. DO NOT put numerical at the very front of sql variable.
6. You MUST wrap generated suggestion within <suggestions> tag in this format e.g
<suggestions>["suggestion1", "suggestion2", "suggestion3"]</suggestions>
7. You should only provide and answer the questions given in <question> tag
</rules>

Don't forget to wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

Now to get started, please briefly introduce yourself.
Then provide the suggested questions using the tag <suggestions>
"""

TABLES_CONTEXT = """
<tables>{tables}</tables>
"""

TABLE_CONTEXT = """
Here is the table name <tableName>{table_path}</tableName>
<tableDescription>{description}</tableDescription>

Here are the columns of the {table_path}

<columns>\n\n{columns}\n\n</columns>
"""

COLUM_CONTEXT = "- **{name}**: {type}"

SUGGESTION_CONTEXT = """
<question>{question}</question>
<questionDescription>{description}</questionDescription>
"""

RESULT_CONTEXT_PROMPT = """
You are given a schema with multiple tables, the table name is in <tableName> tag, the columns are in <columns> tag.
Also you are given a structure with the resulting data from a query withing the <result> tag.
Your goal is to summarize the data and provide usefull information about the data to the user.

{context}
"""

RESULT_PROMPT = "Please provide a summarization and insides of the next result data provided <result>{data}</result>"

# LLM configuration YAML file keys
ASSISTANT_CONFIG_OVERVIEW_KEY = 'assistant_config_overview'
LLM_CONFIG_KEY = 'llm_config'
INSTRUCTIONS_KEY = 'instructions'
SYSTEM_PROMPT_KEY = 'system_prompt'
SUGGESTIONS_KEY = 'suggestions'
TRAINING_SAMPLES_KEY = 'training_samples'
QUESTION_CATEGORIES_KEY = 'question_categories'
QUESTION_EXAMPLE_KEY = 'question_example'
QUESTION_DESCRIPTION_KEY = 'description'


# Semantic model YAML file keys
TABLES_KEY = 'tables'
BASE_TABLE_INFO_KEY = 'base_table'
BASE_DATABASE_KEY = 'database'
BASE_SCHEMA_KEY = 'schema'
BASE_TABLE_KEY = 'table'
TABLE_NAME_KEY = 'name'
TABLE_DESCRIPTION_KEY = 'description'
COLUMNS_DIMENSIONS_KEY = 'dimensions'
COLUMNS_TIME_DIMENSIONS_KEY = 'time_dimensions'
COLUMNS_MEASURES_KEY = 'measures'
COLUMN_NAME_KEY = 'name'
COLUMN_TYPE_KEY = 'data_type'


def system_prompt(sp_session: Session, semantic_model_file: str) -> str:
    config_f = _get_config_llm_file(sp_session)
    config_f_instuctions = config_f[ASSISTANT_CONFIG_OVERVIEW_KEY][LLM_CONFIG_KEY][INSTRUCTIONS_KEY]
    config_f_sys_prompt = config_f_instuctions[SYSTEM_PROMPT_KEY]
    config_f_suggestions = config_f[TRAINING_SAMPLES_KEY][QUESTION_CATEGORIES_KEY]
    suggestions = _get_suggestions_context(config_f_suggestions)

    semantic_model_f = _get_semantic_model_file(sp_session, semantic_model_file)
    context = _get_context(semantic_model_f)
    
    return CONTEXT_PROMPT.format(summary=config_f_sys_prompt, context=context, suggestions=suggestions)


def result_system_prompt(sp_session: Session, semantic_model_file: str) -> str:
    semantic_model_f = _get_semantic_model_file(sp_session, semantic_model_file)
    context = _get_context(semantic_model_f)
    return RESULT_CONTEXT_PROMPT.format(context=context)


def result_prompt(data: str) -> str:
    return RESULT_PROMPT.format(data=data)


def _get_config_llm_file(sp_session: Session) -> dict:
    stage_path = f'@{Application().app_name}.{LLM_SCHEMA}.{LLM_CONFIGURATION_STAGE}/{LLM_CONFIGURATION_FILE}'
    return read_yaml_file(sp_session, stage_path)


def _get_semantic_model_file(sp_session: Session, semantic_model_file: str) -> dict:
    stage_path = f'@{Application().app_name}.{LLM_SCHEMA}.{LLM_SEMANTIC_MODEL_STAGE}/{semantic_model_file}'
    return read_yaml_file(sp_session, stage_path)


def _get_context(semantic_model: dict) -> str:
    tables = semantic_model[TABLES_KEY]
    tables = _get_tables_context(tables)
    return TABLES_CONTEXT.format(tables=tables)


def _get_tables_context(tables: list) -> str:
    tables = "\n".join(_get_table_context(table=table) for table in tables)
    return tables


def _get_table_context(table: dict) -> str:
    base_table = table[BASE_TABLE_INFO_KEY]
    table_path = f"{base_table[BASE_DATABASE_KEY]}.{base_table[BASE_SCHEMA_KEY]}.{base_table[BASE_TABLE_KEY]}"
    table_description = table[TABLE_DESCRIPTION_KEY]
    
    columns = table[COLUMNS_DIMENSIONS_KEY] + table[COLUMNS_TIME_DIMENSIONS_KEY] + table[COLUMNS_MEASURES_KEY]
    columns = _get_table_columns_context(columns)

    return TABLE_CONTEXT.format(table_path=table_path, description=table_description, columns=columns)


def _get_table_columns_context(columns: dict) -> str:
    columns = "\n".join(
        COLUM_CONTEXT.format(name=column[COLUMN_NAME_KEY], type=column[COLUMN_TYPE_KEY])
        for column in columns
    )
    return columns


def _get_suggestions_context(suggestions: list) -> str:
    suggestions = "\n".join(
        SUGGESTION_CONTEXT.format(question=s[QUESTION_EXAMPLE_KEY], description=s[QUESTION_DESCRIPTION_KEY])
        for s in suggestions
    )
    return suggestions
