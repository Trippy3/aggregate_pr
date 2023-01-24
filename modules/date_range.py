from dataclasses import dataclass, field, InitVar
from datetime import datetime, timezone, timedelta


@dataclass(frozen=True)
class DateRange:
    start_arg: InitVar[str | None] = None
    end_arg: InitVar[str | None] = None
    start: datetime = field(init=False)
    end: datetime = field(init=False)

    def __post_init__(self, start_arg, end_arg):
        # TODO: add Secured Validation
        start = self._get_monday() if start_arg is None else self._jst_to_utc(start_arg)
        end = datetime.now(timezone.utc) if end_arg is None else self._jst_to_utc(end_arg)
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)

    def _get_monday(self) -> datetime:
        now_jst = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        mon = 0 - now_jst.weekday()  # Monday is 0
        # TODO: consider summer time
        return now_jst + timedelta(days=mon) - timedelta(hours=9)

    def _jst_to_utc(self, date: str) -> datetime:
        # TODO: consider summer time
        return datetime.fromisoformat(date).replace(tzinfo=timezone.utc) - timedelta(hours=9)
