import datetime

def get_dates_between(start: datetime.date | datetime.datetime, end: datetime.date | datetime.datetime | None = None) -> list[datetime.datetime]:
    dates = []

    start = start.date() if isinstance(start, datetime.datetime) else start
    end = end.date() if isinstance(end, datetime.datetime) else end

    current_date = start
    while current_date <= (end or start):
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)

    return dates


def get_dates_in_month(_date: datetime.date | datetime.datetime) -> list[datetime.date]:
    start = _date.replace(day=1)
    end = start.replace(month=start.month + 1) - datetime.timedelta(days=1)

    return get_dates_between(start, end)
