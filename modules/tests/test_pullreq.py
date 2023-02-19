from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
import requests
import polars as pl

from .. import pullreq as pr
from ..repository import Repository

me = Path(__file__).resolve()

# TODO: define test json


class Test_request:
    @pytest.fixture(scope="class")
    def repo(self) -> Repository:
        # TODO: Consider testing methods that do not rely on token.
        return Repository("https://github.com/Trippy3/aggregate_pr", me.parents[2] / ".token")

    def test_Exit_IfGetErrorCode(self, mocker, repo):
        response_mock = mocker.Mock()
        response_mock.status_code = 404
        mocker.patch.object(requests, "post", return_value=response_mock)
        with pytest.raises(SystemExit):
            pr._request(repo, None)

    def test_ReturnsResponse(self, repo):
        res = pr._request(repo, "Y3Vyc29yOnYyOpHOSKqCYg==")
        assert res.json()["data"]["repository"]["pullRequests"]["nodes"][-1]["number"] == 6


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
            ["https://github.com/Trippy3/aggregate_pr/pull/7", "https://github.com/Trippy3/aggregate_pr/pull/9"],
        )
        assert isinstance(prd.to_lazyframe(), pl.LazyFrame)


class Test_get_pullreq_data:
    @pytest.fixture(scope="class")
    def repo(self) -> Repository:
        # TODO: Consider testing methods that do not rely on token.
        return Repository("https://github.com/Trippy3/aggregate_pr", me.parents[2] / ".token")

    def test_ReturnsSameLazyFrame_RecursiveOrNot(self, repo):
        recursive = pr.get_pullreq_data(repo, is_recursive=True).collect().glimpse(return_as_string=True)
        not_recursive = pr.get_pullreq_data(repo).collect().glimpse(return_as_string=True)
        assert recursive == not_recursive


class Test_make_data_sources:
    @pytest.fixture(scope="class")
    def json(self) -> list[dict[Any]]:
        return [
            {
                "number": 1,
                "title": "Feature/first version",
                "author": {"login": "Trippy3"},
                "labels": {"nodes": []},
                "milestone": None,
                "createdAt": "2023-01-20T05:21:11Z",
                "mergedAt": "2023-01-20T05:22:13Z",
                "additions": 20,
                "deletions": 0,
                "changedFiles": 3,
                "url": "https://github.com/Trippy3/aggregate_pr/pull/1",
            },
            {
                "number": 9,
                "title": "WIP: Feature/#2/tests",
                "author": {"login": "Trippy3"},
                "labels": {"nodes": [{"name": "documentation"}, {"name": "enhancement"}]},
                "milestone": None,
                "createdAt": "2023-01-28T18:03:15Z",
                "mergedAt": "2023-01-28T18:03:28Z",
                "additions": 197,
                "deletions": 31,
                "changedFiles": 11,
                "url": "https://github.com/Trippy3/aggregate_pr/pull/9",
            },
        ]

    def test_RetunrsEmptyDataSrc_IfJsonIsEmpty(self):
        prd = pr._make_data_sources([])
        assert prd == pr.PullReqData()

    def test_RetunrsDataSrc(self, json):
        prd = pr._make_data_sources(json)
        assert prd.number == [1, 9]
        assert prd.labels == [None, "documentation,enhancement"]
        assert prd.merged_at == [
            datetime(2023, 1, 20, 5, 22, 13, tzinfo=timezone.utc),
            datetime(2023, 1, 28, 18, 3, 28, tzinfo=timezone.utc),
        ]
