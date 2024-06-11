supported_functions = {
    'TRY_CAST': { 'description': '' },
    'TRY_TO_BINARY': { 'description': '' },
    'TRY_TO_BOOLEAN': { 'description': '' },
    'TRY_TO_DATE': { 'description': '' },
    'TRY_TO_DECIMAL': { 'description': '' },
    'TRY_TO_NUMBER': { 'description': '' },
    'TRY_TO_NUMERIC': { 'description': '' },
    'TRY_TO_DOUBLE': { 'description': '' },
    'TRY_TO_GEOGRAPHY': { 'description': '' },
    'TRY_TO_GEOMETRY': { 'description': '' },
    'TRY_TO_TIME': { 'description': '' },
    'TRY_TO_TIMESTAMP': { 'description': '' },
    'TRY_TO_TIMESTAMP_*': { 'description': '' },
}


supported_types = [
    'TEXT',
    'FIXED',
    'TIMESTAMP',
    'TIMESTAMP_NTZ'
]


supported_languages = [
    'python',
    'sql',
    'javascript'
]


def get_functions_names() -> list:
    return list(supported_functions.keys())


def get_supported_types() -> list:
    return supported_types


def get_supported_languages() -> list:
    return supported_languages
