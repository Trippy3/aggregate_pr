from dataclasses import dataclass, field, InitVar
from urllib.parse import urlparse

@dataclass(frozen=True)
class Repository:
    addr: InitVar[str]
    owner: str = field(init=False)
    name: str = field(init=False)

    def __post_init__(self, addr):
        # TODO: add Secured Validation
        url_path = urlparse(addr).path
        object.__setattr__(self, "owner", url_path.split("/")[0])
        object.__setattr__(self, "name", url_path.split("/")[1])
