from datetime import datetime
from dataclasses import dataclass, field, InitVar

import requests

from fmodules.dict_wrapper import AttrDict


@dataclass
class PullReq:
    number: int
    title: str
    user: str
    labels: list(str)
    milestone: str
    created_at: datetime
    merged_at: datetime
    addition: int
    deletion: int
    changed_files: int

    def __post_init__(self):
        pass


def get_pullreq_lists() -> list(PullReq):
    pass

def get_pullreq() -> AttrDict:
    pass
