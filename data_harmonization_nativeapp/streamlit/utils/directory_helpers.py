import re


# Helper function to get the top level directories in a stage
# Ex: 'stage_dir/directory/file_name', returns 'directory'
def get_toplevel_subdirectories(stage_name: str, directories):
    pattern = rf'{stage_name}/([^/]+)/'
    dirs = []
    for row in directories:
        directory = row['name']
        match = re.findall(pattern, directory, flags=re.IGNORECASE)
        dirs = dirs + match if match and match[0] not in dirs else dirs
    return dirs

# Filter files to only the ones in the selected directory
def filter_files_in_subdirectories(subdir: str, directories):
    subdirs_regex = rf'^{subdir}'
    filtered = filter(lambda row: re.search(subdirs_regex, row['name'], re.IGNORECASE) is not None, directories)
    return list(filtered)