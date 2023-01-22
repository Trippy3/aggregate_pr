from ..repository import Repository


def test_RetunrsRepo_TakeAddr():
    addr = "https://github.com/Trippy3/aggregate_pr"
    repo = Repository(addr)
    assert (repo.owner, "Trippy3")
    assert (repo.name, "aggregate_pr")
