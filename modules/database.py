import sys
from enum import Flag, auto
from pathlib import Path
from dataclasses import dataclass, field

import duckdb as ddb
import polars as pl

TOP_TABLE = "merged_pr"
ALL_SELECT = f"SELECT * FROM {TOP_TABLE}"
me = Path(__file__).resolve()


class DBMode(Flag):
    OVERWRITE = auto()
    DELTA = auto()
    # TODO: If there are more modes, move to DB Interface(abs).


@dataclass(frozen=True)
class Database:
    path: Path = me.parents[1] / "data" / "pr.db"
    mode: DBMode = DBMode.DELTA
    top_table: str = field(init=False, default=TOP_TABLE)
    conn: ddb.DuckDBPyConnection = field(init=False, default=None)

    def __post_init__(self):
        if self.path.suffix != ".db":
            print(f'"{self.path}" is not a .db file.', file=sys.stderr)
            sys.exit(1)
        if self.mode == DBMode.DELTA and not self.path.exists():
            print(f'"{self.path}" does not exist. Create a new DB file and continue.')
            object.__setattr__(self, "mode", DBMode.OVERWRITE)
        object.__setattr__(self, "conn", self._make_connection())

    def _make_connection(self) -> ddb.DuckDBPyConnection:
        if self.mode == DBMode.OVERWRITE:
            # Delete files first because duckdb.connect() does not have an overwrite option.
            self.path.unlink(missing_ok=True)
        return ddb.connect(str(self.path))

    def write_data(self, ldf: pl.LazyFrame) -> ddb.DuckDBPyConnection:
        def get_only_additional(new: pl.LazyFrame) -> pl.LazyFrame:
            original = self.to_ldf()
            return new.join(original, on="number", how="anti")

        if self.mode == DBMode.OVERWRITE:
            self.conn.sql(f"CREATE TABLE {self.top_table} AS SELECT * FROM ldf")
        elif self.mode == DBMode.DELTA:
            only_add = get_only_additional(ldf)  # noqa
            self.conn.sql(f"INSERT INTO {self.top_table} SELECT * FROM only_add")
        return self.conn

    def to_ldf(self) -> pl.LazyFrame:
        return self.conn.sql(f"{ALL_SELECT}").pl().lazy()

    def to_parquet(self) -> Path:
        parquet = self.path.parent / "pr.parquet"
        self.conn.sql(f"{ALL_SELECT}").write_parquet(str(parquet))
        return parquet

    def to_csv(self) -> Path:
        csv = self.path.parent / "pr.csv"
        self.conn.sql(f"{ALL_SELECT}").write_csv(str(csv), header=True)
        return csv
