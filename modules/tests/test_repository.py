import pytest
from pathlib import Path

from ..repository import Repository


ADDR = "https://github.com/Trippy3/aggregate_pr"


class TestRepository:
    def test_RetunrsRepo_TakeAddr(self):
        repo = Repository(ADDR)
        assert repo.owner == "Trippy3"
        assert repo.name == "aggregate_pr"
        assert repo.token is None

    token_files = [
        (None),
        ("./nonexistent_file"),
        (Path("./nonexistent_file")),
    ]

    @pytest.mark.parametrize("token_file", token_files)
    def test_RetunrsRepo_TakeAddrAndInvalidTokenFile(self, token_file):
        repo = Repository(ADDR, token_file)
        assert repo.owner == "Trippy3"
        assert repo.name == "aggregate_pr"
        assert repo.token is None

    def test_RetunrsRepo_TakeAddrAndTokenFile(self, tmp_path):
        CONTENT = "ghp_XXXXXXXXXXXXX"
        (test_token := tmp_path / ".test_token").write_text(CONTENT)
        repo = Repository(ADDR, test_token)
        assert repo.owner == "Trippy3"
        assert repo.name == "aggregate_pr"
        assert repo.token == CONTENT
