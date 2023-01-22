from datetime import datetime, timezone, timedelta

import pytest

from .. import pullreq as pr


class Test_get_pullreq_data:
    def test_ReturnsLazyFrame(self):
        start = datetime.fromisoformat("2023-01-21") - timedelta(hours=9)
        end = datetime.now(timezone.utc).replace(tzinfo=None)
        df = pr.get_pullreq_data("pola-rs", "polars", start, end)
        print(df)
        print(df.collect())
