from dash import html, dcc
from datetime import datetime, date

def date_picker():
    return dcc.DatePickerRange(
        id='date-picker-range',
        className="date-picker",
        min_date_allowed=date(2018, 1, 1),
        max_date_allowed=date(2018, 4, 30),
        initial_visible_month=date(2018, 4, 30),
        start_date=datetime(2017, 1, 31),
        end_date=date(2018, 4, 30)
    )