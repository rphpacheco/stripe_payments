from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def controllers(df):
    list_of_methods = dict(enumerate(df["PAYMENTMETHOD"].unique(),1))
    return dbc.Row([
        dcc.Dropdown(
            id="methods-dropdown",
            options=[{"label": j, "value": j} for i, j in list_of_methods.items()],
            value=0,
            placeholder="Select a Method"
        )
    ],
    style={
        "width": "250px",
    })