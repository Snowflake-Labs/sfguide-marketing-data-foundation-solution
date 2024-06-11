import yaml

from snowflake.snowpark.session import Session


def read_yaml_file(sp_session: Session, file_path: str) -> dict:
    with sp_session.file.get_stream(file_path) as conf_f:
        content = conf_f.read()
        content = yaml.safe_load(content)
    return content
