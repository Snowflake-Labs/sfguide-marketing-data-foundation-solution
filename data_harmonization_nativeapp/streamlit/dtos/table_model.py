from typing import List


class TableModel:
    def __init__(self, table_name: str, columns: List[str]):
        self.table_name = table_name
        self.columns = columns
