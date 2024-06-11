import os


# Directories to ignore
dirs_ignore = ['/streamlit/frontend', 'pycache', 'tests']
is_ignore = lambda path: len(list(filter(lambda ignore: ignore in path, dirs_ignore))) > 0


def upload_files_stage(sp_session, database: str, schema: str, stage: str, app_dir: str) -> None:
    for path, currentDirectory, files in os.walk(app_dir):
        for file in files:
            dir = app_dir.replace("./","")
            if not file.startswith('.') and not is_ignore(path):
                # build the relative paths to the file
                local_file = os.path.join(path, file)
                replace_path = os.path.join('.',dir)

                # build the path to where the file will be staged
                stage_dir = path.replace(replace_path,'')
                print(f'{local_file} => @{stage}{stage_dir}')
                sp_session.file.put(
                    local_file_name = local_file,
                    stage_location = f'{database}.{schema}.{stage}/{stage_dir}',
                    auto_compress=False,
                    overwrite=True)

    sp_session.sql(f'alter stage {database}.{schema}.{stage} refresh; ').collect()
