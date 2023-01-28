from datetime import datetime, timezone

import pytest

from ..date_range import DateRange


class TestDateRange:
    ios = [
        (
            {},
            datetime(2023, 1, 22, 15, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 29, 10, 0, 0, tzinfo=timezone.utc),
        ),
        (
            {"start_arg": "2022-12-31 01:11:11"},
            datetime(2022, 12, 30, 16, 11, 11, tzinfo=timezone.utc),
            datetime(2023, 1, 29, 10, 0, 0, tzinfo=timezone.utc),
        ),
        (
            {"end_arg": "2023-12-31 01:11:11"},
            datetime(2023, 1, 22, 15, 0, 0, tzinfo=timezone.utc),
            datetime(2023, 12, 30, 16, 11, 11, tzinfo=timezone.utc),
        ),
        (
            {"start_arg": "2022-12-31 01:11:11", "end_arg": "2023-12-31 01:11:11"},
            datetime(2022, 12, 30, 16, 11, 11, tzinfo=timezone.utc),
            datetime(2023, 12, 30, 16, 11, 11, tzinfo=timezone.utc),
        ),
    ]

    @pytest.mark.parametrize("kwargs, start, end", ios)
    @pytest.mark.freeze_time("2023-01-29 10:00:00")  # freeze time is utc.
    def test_ReturnsDate_TakeDate(self, kwargs, start, end):
        dr = DateRange(**kwargs)
        assert dr.start == start
        assert dr.end == end

    def test_Exit_TakeInvalidDate(self):
        with pytest.raises(SystemExit):
            DateRange("2023-01-28 23:30:30", "2023-01-28 23:30:29")
