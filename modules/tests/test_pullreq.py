from datetime import datetime, timezone

import pytest
import requests
import polars as pl

from .. import pullreq as pr

# TODO: define test json


class Test_request:
    def test_Exit_IfGetErrorCode(self, mocker):
        response_mock = mocker.Mock()
        response_mock.status_code = 404
        mocker.patch.object(requests, "get", return_value=response_mock)
        with pytest.raises(SystemExit):
            pr._request("addr", None)


class TestPullReqData:
    def test_ReturnsLazyFrame(self):
        prd = pr.PullReqData(
            [1, 2],
            ["a", "b"],
            ["a", "b"],
            ["a", None],
            ["a", None],
            [datetime(2023, 1, 29, 10, 0, 0, tzinfo=timezone.utc), datetime(2023, 1, 29, 11, 0, 0, tzinfo=timezone.utc)],
            [datetime(2023, 1, 29, 10, 30, 0, tzinfo=timezone.utc), datetime(2023, 1, 29, 12, 00, 0, tzinfo=timezone.utc)],
            [0.5, 1.0],
            [1, 2],
            [1, 2],
            [2, 4],
            [1, 2],
        )
        assert isinstance(prd.to_lazyframe(), pl.LazyFrame)


class Test_make_data_sources:
    def test_RetunrsEmptyDataSrc_IfJsonIsEmpty(self):
        pass

    def test_RetunrsDataSrc(self):
        pass
