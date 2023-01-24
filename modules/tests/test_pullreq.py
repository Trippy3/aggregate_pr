from datetime import datetime, timezone, timedelta

import pytest

from .. import pullreq as pr
from ..repository import Repository
from ..date_range import DateRange


class Test_get_pullreq_data:
    def test_ReturnsLazyFrame(self):
        repo = Repository("https://github.com/Trippy3/aggregate_pr")
        print(repo)
        dr = DateRange("2023-01-21")
        df = pr.get_pullreq_data(repo, dr)
        print("step1: ", df)
        print("step2: ", df.collect())
