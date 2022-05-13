from dash import html, dcc
from datetime import datetime, date

def date_picker(df):
    start_date = df["CREATED"].min()
    end_date = df["CREATED"].max()
    return html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            className="date-picker",
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            initial_visible_month=end_date,
            start_date=start_date,
            end_date=end_date
        )
    ],
    style={
        "border": "0.5px solid #2C2D33",
        "border-radius": "5px",
    })