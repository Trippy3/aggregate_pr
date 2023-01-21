from dataclasses import dataclass, field, InitVar
from datetime import datetime, timezone


@dataclass(frozen=True)
class DateRange:
    start_arg: InitVar[str | None] = None
    end_arg: InitVar[str | None] = None
    start: datetime = field(init=False)
    end: datetime = field(init=False)

    def __post_init__(self, start_arg, end_arg):
        # TODO: add Secured Validation
        start = self._get_monday() if start_arg is None else datetime.fromisoformat(start_arg)
        end = datetime.now(timezone.utc) if end_arg is None else datetime.fromisoformat(end_arg)
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)
    
    def _get_monday() -> datetime:
        pass
