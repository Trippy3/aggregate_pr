import sys
from typing import Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
from string import Template

import requests
import polars as pl

from fmodules.dict_wrapper import AttrDict

from .repository import Repository


@dataclass
class PullReqData:
    number: list[int] = field(default_factory=list)
    title: list[str] = field(default_factory=list)
    user: list[str | None] = field(default_factory=list)
    labels: list[str | None] = field(default_factory=list)
    milestone: list[str | None] = field(default_factory=list)
    created_at: list[datetime] = field(default_factory=list)
    merged_at: list[datetime] = field(default_factory=list)
    read_time_hr: list[float] = field(default_factory=list)
    additions: list[int] = field(default_factory=list)
    deletions: list[int] = field(default_factory=list)
    difference: list[int] = field(default_factory=list)
    changed_files: list[int] = field(default_factory=list)
    url: list[str] = field(default_factory=list)

    def to_lazyframe(self) -> pl.LazyFrame:
        return pl.DataFrame(asdict(self)).lazy()


PR_QUERY = Template(
    """
    query {
        repository(owner: "$owner", name: "$reponame") {
            pullRequests(last: 100, states: MERGED, $before) {
                nodes {
                    number
                    title
                    author {
                        login
                    }
                    labels(first: 10) {
                        nodes {
                            name
                        }
                    }
                    milestone {
                        title
                    }
                    createdAt
                    mergedAt
                    additions
                    deletions
                    changedFiles
                    url
                }
                pageInfo {
                    hasPreviousPage
                    startCursor
                }
            }
        }
    }
    """
)


def _request(repo: Repository, start_cursor: str | None) -> requests.Response:
    headers = {"User-Agent": "githubapi"}
    if repo.token:
        headers["Authorization"] = f"bearer {repo.token}"
    pr_args = f'before: "{start_cursor}"' if start_cursor else ""
    query: str = PR_QUERY.substitute(owner=repo.owner, reponame=repo.name, before=pr_args)
    res = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    if res.status_code != requests.codes.ok:
        print(f"Error Status: {res.status_code}", file=sys.stderr)
        sys.exit(1)
    return res


def _make_data_sources(json: list[dict[Any]]) -> PullReqData:
    prd = PullReqData()
    for pull_request in json:
        pr = AttrDict(pull_request)
        prd.number.append(pr.number)
        prd.title.append(pr.title)
        prd.user.append(pr.author.login if pr.author else None)
        # TODO: Check if the .parquet data type accepts list[str]
        prd.labels.append(",".join([lable["name"] for lable in pr.labels.nodes]) if pr.labels.nodes else None)
        prd.milestone.append(pr.milestone.title if pr.milestone else None)
        prd.created_at.append(created_at := datetime.strptime(pr.createdAt, "%Y-%m-%dT%H:%M:%S%z"))
        prd.merged_at.append(merged_at := datetime.strptime(pr.mergedAt, "%Y-%m-%dT%H:%M:%S%z"))
        prd.read_time_hr.append(round((merged_at - created_at).total_seconds() / (60 * 60), 2))  # sec. to hour
        prd.additions.append(pr.additions)
        prd.deletions.append(pr.deletions)
        prd.difference.append(pr.additions + pr.deletions)
        prd.changed_files.append(pr.changedFiles)
        prd.url.append(pr.url)
    return prd


def get_pullreq_data(repo: Repository, is_recursive: bool = False) -> pl.LazyFrame:
    pr_nodes = []
    if is_recursive:
        has_previous_page = True
        start_cursor: str | None = None
        while has_previous_page:
            res = _request(repo, start_cursor)
            # TODO: case: res["Error"]
            pr = AttrDict(res.json()["data"]["repository"]["pullRequests"])
            has_previous_page = pr.pageInfo.hasPreviousPage
            start_cursor = pr.pageInfo.startCursor
            pr_nodes += pr.nodes
    else:
        res = _request(repo, None)
        # TODO: case: res["Error"]
        pr_nodes += res.json()["data"]["repository"]["pullRequests"]["nodes"]
    data_src = _make_data_sources(pr_nodes)
    return data_src.to_lazyframe()
