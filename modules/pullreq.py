import sys
from typing import Any
from datetime import datetime
from dataclasses import dataclass, field, asdict

import requests
import polars as pl

from fmodules.dict_wrapper import AttrDict

from .repository import Repository
from .date_range import DateRange


@dataclass
class PullReqData:
    number: list[int] = field(default_factory=list)
    title: list[str] = field(default_factory=list)
    user: list[str] = field(default_factory=list)
    labels: list[str | None] = field(default_factory=list)
    milestone: list[str | None] = field(default_factory=list)
    created_at: list[datetime] = field(default_factory=list)
    merged_at: list[datetime] = field(default_factory=list)
    read_time_hr: list[float] = field(default_factory=list)
    additions: list[int] = field(default_factory=list)
    deletions: list[int] = field(default_factory=list)
    difference: list[int] = field(default_factory=list)
    changed_files: list[int] = field(default_factory=list)

    def to_lazyframe(self) -> pl.LazyFrame:
        return pl.DataFrame(asdict(self)).lazy()


def _request(addr: str, token: str | None) -> requests.Response:
    headers = {"User-Agent": "githubapi", "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    res = requests.get(addr, headers=headers)
    if res.status_code != requests.codes.ok:
        print(f"Error: GET Status: {res.status_code}, Address: {addr}", file=sys.stderr)
        sys.exit(1)
    return res


def _make_data_sources(repo: Repository, date_range: DateRange, json: Any) -> PullReqData:
    prd = PullReqData()
    for pull_request in json:
        if (pr := AttrDict(pull_request)) is False:
            print("Warning: The retrieved json content was empty.")
            return prd
        if pr.merged_at is None:  # PRs closed without merging are not needed for aggregation
            continue
        if (created_at := datetime.strptime(pr.created_at, "%Y-%m-%dT%H:%M:%S%z")) < date_range.start or (
            merged_at := datetime.strptime(pr.merged_at, "%Y-%m-%dT%H:%M:%S%z")
        ) > date_range.end:
            continue
        # Code diff information can only be obtained from a separate query.
        pr_detail = AttrDict(
            _request(f"https://api.github.com/repos/{repo.owner}/{repo.name}/pulls/{pr.number}", repo.token).json()
        )
        prd.number.append(pr.number)
        prd.title.append(pr.title)
        prd.user.append(pr.user.login)
        prd.labels.append(",".join([lable["name"] for lable in pr.labels]) if pr.labels else None)
        prd.milestone.append(pr.milestone.title if pr.milestone is not None else None)
        prd.created_at.append(created_at)
        prd.merged_at.append(merged_at)
        prd.read_time_hr.append(round((merged_at - created_at).total_seconds() / (60 * 60), 2))  # sec. to hour
        prd.additions.append(pr_detail.additions)
        prd.deletions.append(pr_detail.deletions)
        prd.difference.append(pr_detail.additions + pr_detail.deletions)
        prd.changed_files.append(pr_detail.changed_files)
    return prd


def get_pullreq_data(repo: Repository, date_range: DateRange) -> pl.LazyFrame:
    res = _request(
        f"https://api.github.com/repos/{repo.owner}/{repo.name}/pulls?state=closed&per_page=10", repo.token
    )  # TODO: 50
    data_src = _make_data_sources(repo, date_range, res.json())
    return data_src.to_lazyframe()
