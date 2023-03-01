import sys

import pytest

from .. import aggregate_pullreq as ap


class Test_main:
    def test_Exit_IfOutputDirIsFile(self, mocker):
        mocker.patch.object(
            sys, "argv", ["aggregate_pillreq.py", "https://github.com/Trippy3/aggregate_pr", "-o", "./data/.gitkeep"]
        )
        with pytest.raises(SystemExit):
            ap.main()

    def test_Exit_IfTokenDoesNotExist(self, mocker):
        mocker.patch.object(
            sys, "argv", ["aggregate_pillreq.py", "https://github.com/Trippy3/aggregate_pr", "-t", "./no_exist/.no_key"]
        )
        with pytest.raises(SystemExit):
            ap.main()
