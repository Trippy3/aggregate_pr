import sys
from typing import Any
from datetime import datetime
from dataclasses import dataclass, field, asdict

import requests
import polars as pl

from fmodules.dict_wrapper import AttrDict


@dataclass
class PullReqData:
    number: list[int] = field(default_factory=list)
    title: list[str] = field(default_factory=list)
    user: list[str] = field(default_factory=list)
    labels: list[list[str]] = field(default_factory=list)
    milestone: list[str] = field(default_factory=list)
    created_at: list[datetime] = field(default_factory=list)
    merged_at: list[datetime] = field(default_factory=list)
    read_time: list[datetime] = field(default_factory=list)
    addition: list[int] = field(default_factory=list)
    deletion: list[int] = field(default_factory=list)
    difference: list[int] = field(default_factory=list)
    changed_files: list[int] = field(default_factory=list)

    def to_lazyframe(self) -> pl.LazyFrame:
        return pl.DataFrame(asdict(self)).lazy()


def _request(addr: str) -> requests.Response:
    token = "xxx"
    headers = {"Authorization": f"token {token}"}
    res = requests.get(addr)
    if res.status_code != requests.codes.ok:
        print(f"Error: GET Status: {res.status_code}, Address: {addr}", file=sys.stderr)
        sys.exit(1)
    return res


def _make_data_sources(owner: str, repo: str, start: datetime, end: datetime, json: Any) -> PullReqData:
    prd = PullReqData()
    print(prd)
    print(asdict(prd))
    for pull_request in json:
        if (pr := AttrDict(pull_request)) == False:
            # TODO: print warning
            return prd
        if pr.merged_at is None:  # PRs closed without merging are not needed for aggregation
            continue
        if (
            datetime.strptime(pr.created_at, "%Y-%m-%dT%H:%M:%SZ") < start
            or datetime.strptime(pr.merged_at, "%Y-%m-%dT%H:%M:%SZ") > end
        ):
            continue
        pr_detail = AttrDict(_request(f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr.number}").json())
        # prd.number.append(pr.number)
    return prd


def get_pullreq_data(owner: str, repo: str, start: datetime, end: datetime) -> pl.LazyFrame:
    res = _request(f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=50")
    data_src = _make_data_sources(owner, repo, start, end, res.json())
    return data_src.to_lazyframe()
