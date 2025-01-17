from typing import Any

from .column import Column
from .database import Database
from .icolumn import IColumn
from .idatabase import IDatabase
from .iloader import ISQLLoader, ISQLLoaderExecutor
from .itable import ITable
from .itype import IType
from .table import Table
from .types import VARCHAR


QUERIES = {
    "tables": """
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public'
    """,
    "columns": """
        SELECT table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = any($1::string[]);
    """,
}


class SQLLoader(ISQLLoader):
    def __init__(self, executor: ISQLLoaderExecutor) -> None:
        self.executor = executor

    async def load(self) -> IDatabase:
        tables_rows = await self.executor.execute(QUERIES["tables"])
        tables_names = list(map(lambda r: r[0], tables_rows))
        columns_rows = await self.executor.execute(
            QUERIES["columns"], (tables_names,)
        )
        columns: dict[str, list[IColumn[IType[Any]]]] = {
            t_name: [] for t_name in tables_names
        }
        for t_name, c_name, c_type, c_nullable in columns_rows:
            columns[t_name].append(
                Column(
                    c_name,
                    self.from_pgtype(c_type),
                    self.from_pgnullable(c_nullable),
                    default=None,
                )
            )
        tables: list[ITable] = []
        for name in tables_names:
            tables.append(Table(name=name, columns=columns[name]))
        return Database(
            tables=tables,
        )

    def from_pgtype(self, pg_type: str) -> IType[Any]:
        if pg_type == "character varying":
            return VARCHAR(255)
        else:
            raise ValueError(f"Unknown pgtype: {pg_type}")

    def from_pgnullable(self, pg_nullable: str) -> bool:
        return pg_nullable == "YES"
