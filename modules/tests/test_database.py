from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import polars as pl
import duckdb as ddb

from ..database import Database, DBMode


@pytest.fixture(scope="class")
def rw_db() -> Database:
    with TemporaryDirectory() as dir:
        db = Database(Path(dir) / "read_test.db", DBMode.OVERWRITE)
        db.conn.sql(f"CREATE TABLE {db.top_table} AS SELECT 42")
        yield db


class TestDatabase:
    def test_Exit_IfTakesNotDBPath(self):
        with pytest.raises(SystemExit):
            Database(Path("aaa/pr.dd"))

    def test_ReturnsDBConnection_DBModeIsOverwrite(self):
        with TemporaryDirectory() as dir:
            db = Database(Path(dir) / "temp.db", DBMode.OVERWRITE)
            assert isinstance(db.conn, ddb.DuckDBPyConnection)

    def test_ReturnsDBConnection_DBModeIsDelta(self):
        with TemporaryDirectory() as dir:
            db = Database(Path(dir) / "temp.db", DBMode.DELTA)
            assert isinstance(db.conn, ddb.DuckDBPyConnection)
            db = Database(Path(dir) / "temp.db", DBMode.DELTA)  # Case by existing temp.db
            assert isinstance(db.conn, ddb.DuckDBPyConnection)


class Test_write_data:
    def test_WriteDB(self):
        with TemporaryDirectory() as dir:
            db = Database(Path(dir) / "test_write.db", DBMode.OVERWRITE)
            ldf = pl.DataFrame({"number": [1, 7, 9], "labels": ["bug", None, "one,two"]}).lazy()
            ret = db.write_data(ldf)
            assert ret.sql(f"SELECT * FROM {db.top_table}").pl().glimpse(return_as_string=True) == ldf.collect().glimpse(
                return_as_string=True
            )
            db.conn.close()
            db = Database(Path(dir) / "test_write.db", DBMode.DELTA)  # Case by existing db file
            add_ldf = pl.DataFrame({"number": [2, 9], "labels": ["four", None]}).lazy()
            ret = db.write_data(add_ldf)
            expected = pl.concat([ldf, add_ldf.join(ldf, on="number", how="anti")], parallel=False)
            assert ret.sql(f"SELECT * FROM {db.top_table}").pl().glimpse(
                return_as_string=True
            ) == expected.collect().glimpse(return_as_string=True)


class Test_to_parquet:
    def test_WriteParquet(self, rw_db):
        parquet: Path = rw_db.to_parquet()
        assert parquet == Path(rw_db.path.parent / "pr.parquet")


class Test_to_csv:
    def test_WriteCsv(self, rw_db):
        csv: Path = rw_db.to_csv()
        assert csv == Path(rw_db.path.parent / "pr.csv")
