from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def status_controller(df):
    list_of_methods = dict(enumerate(df["STATUS"].unique(),1))
    return dbc.Row([
        dcc.Dropdown(
            id="status-dropdown",
            options=[{"label": j, "value": j} for i, j in list_of_methods.items()],
            value=0,
            placeholder="Select a Status"
        )
    ],
    style={
        "width": "250px",
    })