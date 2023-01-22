from datetime import datetime, timezone, timedelta

import pytest

from .. import pullreq as pr


class Test_get_pullreq_data:
    def test_ReturnsLazyFrame(self):
        start = datetime.fromisoformat("2023-01-21") - timedelta(hours=9)
        start = start.replace(tzinfo=timezone.utc)
        end = datetime.now(timezone.utc)
        df = pr.get_pullreq_data("pola-rs", "polars", start, end)
        print("step1: ", df)
        print("step2: ", df.collect())
