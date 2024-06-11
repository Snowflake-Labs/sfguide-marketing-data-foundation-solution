
class DynamicTableParams: 
    def __init__(self, connector, provider, source_db, source_schema):
        self.connector = connector
        self.provider = provider
        self.source_db = source_db
        self.source_schema = source_schema
    def values(self):
        return [self.connector, self.provider, self.source_db, self.source_schema]

