from pathlib import Path
from dataclasses import dataclass, field, InitVar
from urllib.parse import urlparse

me = Path(__file__).resolve()


@dataclass(frozen=True)
class Repository:
    addr: InitVar[str]
    token_file: InitVar[Path | None] = None
    owner: str = field(init=False)
    name: str = field(init=False)
    token: str | None = field(init=False, default=None)

    def __post_init__(self, addr, token_file):
        # TODO: add Secured Validation
        url_path = urlparse(addr).path
        object.__setattr__(self, "owner", url_path.split("/")[1])  # path is "/owner/repo"
        object.__setattr__(self, "name", url_path.split("/")[2])
        if token_file is None:
            token_file = me.parents[1] / ".token"
        if not token_file.exists():
            print(f"Warning: Token file does not exist. path: {token_file}")
            return
        with open(token_file, "r") as f:
            object.__setattr__(self, "token", f.readline().rstrip())  # Exclude trailing \n
