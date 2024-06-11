from typing import List
from dtos.table_model import TableModel


class MappingModel:
    def __init__(self, 
        id: str, 
        name: str, 
        source_schema: str = '', 
        target_schema: str = '',
        source_tables: List[TableModel] = [], 
        target_tables: List[TableModel] = [],
        mappings: List[List[str]] = []
    ):
        self.id = id
        self.name = name
        self.source_schema = source_schema
        self.target_schema = target_schema
        self.source_tables = source_tables
        self.target_tables = target_tables
        self.mappings = mappings


    def add_source_column(self, table_name: str, column_name: str) -> None:
        self._add_column(table_name, column_name, self.source_tables)


    def add_target_column(self, table_name: str, column_name: str) -> None:
        self._add_column(table_name, column_name, self.target_tables)


    def _add_column(self, table_name: str, column_name: str, model: List[TableModel]) -> None:
        table_match = next((t_model for t_model in model if t_model.table_name == table_name), None)
        if table_match:
            table_match.columns.append(column_name)
        else:
            new_table = TableModel(table_name, [column_name])
            model.append(new_table)
    