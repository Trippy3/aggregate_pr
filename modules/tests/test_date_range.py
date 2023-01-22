import pytest

from ..date_range import DateRange


class TestDateRange:
    def test_ReturnsData_NoArgs(self):
        dr = DateRange()
        print(dr)
