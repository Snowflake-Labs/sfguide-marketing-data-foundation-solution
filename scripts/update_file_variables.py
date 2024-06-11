import os
import re


def file_replace(file_name: str, replace: dict) -> None:
    replace = dict((re.escape(k), v) for k, v in replace.items())
    pattern = re.compile("|".join(replace.keys()))
    replace_fun = lambda m: replace[re.escape(m.group(0))]
    with open(file_name, 'r+') as f:
        file_content = f.read()
        updated_file = pattern.sub(replace_fun, file_content)
        f.seek(0)
        f.write(updated_file)
        f.truncate()
