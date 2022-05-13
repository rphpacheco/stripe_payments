import numpy as np
from dash import html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from src.app import app
import pandas as pd

import plotly.express as px

from src.components.logo import *
from src.components.controllers import *
from src.components.date_picker import date_picker
from src.components.status_controller import *
from src.components.cards import cards, symbol, color

df = pd.read_csv("src/data/stripe_payments.csv")
df["STATUS"] = df["STATUS"].str.title()
df["PAYMENTMETHOD"] = df["PAYMENTMETHOD"].str.replace("_", " ").str.title()

fig = px.bar(
    df,
    x="CREATED",
    y="AMOUNT",
    color="PAYMENTMETHOD",
    title="Payments",
    template="plotly_dark",
    labels={"CREATED": "Date", "AMOUNT": "Amount", "STATUS": "Status", "PAYMENTMETHOD": "Method"},
    hover_data=["AMOUNT", "STATUS", "PAYMENTMETHOD"],
)

layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Row([
                html.Header(id="header", children=[
                    html.Div(id="logo", children=[
                        logo,
                    ]),
                ], 
                style={
                    "padding-left": "8px",
                    "padding-right": "8px",
                    "border-bottom": "0.5px solid #2C2D33",
                })
            ]),
            dbc.Row([
                dbc.Col([
                    html.H3(id="title", children=[
                        html.I(
                            className="fa-brands fa-cc-stripe",
                            style={
                                "margin-right": "10px",
                                "color": "#635bff",

                            }
                        ),
                        "Stripe Payments Analysis",
                    ],
                    style={
                        "font-size": "2.5rem",
                        "color": "#838689",
                    }),
                    html.Div(id="selectors", children=[
                        html.Button(
                            id="reset-all-button",
                            children=[
                                html.I(
                                    className="fa-solid fa-undo-alt",
                                    style={
                                        "color": "#635bff",
                                        "font-size": "1.5rem",
                                    }
                                ),
                            ],
                            style={
                                "width": "auto",
                                "background-color": "#1E1E1E",
                                "padding": "2px 10px 10px 10px",
                                "border": "0.5px solid #2C2D33",
                                "border-radius": "5px",
                            },
                        ),
                        status_controller(df),
                        controllers(df),
                        date_picker(df),
                    ],
                    style={
                        "width": "auto",
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "flex-end",
                        "align-items": "center",
                        "gap": "20px",
                    }),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "space-between",
                    "align-items": "center",
                }),
            ],
            style={
                "padding": "15px 20px 15px 22px",
            }),
            dbc.Row(
                id="cards",
                children=[
                    dbc.Col([
                        cards(df, df, "Total Payments", "fa-solid fa-sack-dollar", "active"),
                    ]),
                    dbc.Col([
                        cards(df.loc[df["PAYMENTMETHOD"] == "Credit Card"], df, "Credit Card", "fa-solid fa-credit-card"),
                    ]),
                    dbc.Col([
                        cards(df.loc[df["PAYMENTMETHOD"] == "Coupons"], df, "Coupons", "fa-solid fa-ticket-simple"),
                    ]),
                    dbc.Col([
                        cards(df.loc[df["PAYMENTMETHOD"] == "Bank Transfer"], df, "Bank Transfers", "fa-solid fa-building-columns"),
                    ]),
                    dbc.Col([
                        cards(df.loc[df["PAYMENTMETHOD"] == "Gift Card"], df, "Gift Cards", "fa-solid fa-gift"),
                    ]),
                ],
                style={
                    "display": "flex",
                    "justify-content": "space-around",
                    "align-items": "center",
                    "padding": "0 10px",
                }
            ),
            dbc.Row([
                html.Button(
                    id="reset-graph-button",
                    children=[
                        html.I(
                            className="fa-solid fa-undo-alt",
                            style={
                                "margin-right": "10px",
                                "color": "#635bff",
                            }
                        ),
                        "Reset Filter Graph",
                    ],
                    style={
                        "width": "18em",
                        "background-color": "#131314",
                        "color": "#fff",
                        "font-size": "1.2rem",
                        "margin": "0px 0px 20px 0px",
                        "padding": "0px 10px 10px 10px",
                        "border": "0.5px solid #2C2D33",
                        "border-radius": "5px",
                    },
                ),
                dcc.Graph(
                    id="graph",
                    figure=fig,
                    style={
                        "width": "100%",
                        "border": "0.5px solid #2C2D33",
                        "border-radius": "4px",
                    }
                ),
            ], 
            style={
                "padding": "20px",
            }),
        ])
    ],
    fluid=True,
)    

def filter_dataframe(df, status, start_date, end_date):
    if status is None or status == 0:
        dff = df.loc[(df["CREATED"] >= start_date) & (df["CREATED"] <= end_date)]
    else:  
        dff = df.loc[(df["STATUS"] == status) & (df["CREATED"] >= start_date) & (df["CREATED"] <= end_date)]
    return dff

@app.callback(
    Output("total-payments-amount", "children"),
    Output("total-payments-percent", "children"),
    Output("total-payments-percent", "style"),
    Output("credit-card-amount", "children"),
    Output("credit-card-percent", "children"),
    Output("credit-card-percent", "style"),
    Output("coupons-amount", "children"),
    Output("coupons-percent", "children"),
    Output("coupons-percent", "style"),
    Output("bank-transfers-amount", "children"),
    Output("bank-transfers-percent", "children"),
    Output("bank-transfers-percent", "style"),
    Output("gift-cards-amount", "children"),
    Output("gift-cards-percent", "children"),
    Output("gift-cards-percent", "style"),
    Output("graph", "figure"),
    Input("status-dropdown", "value"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("graph", "clickData"),
    Input("reset-all-button", "n_clicks"),
    Input("reset-graph-button", "n_clicks"),
)
def update_status_dropdown(status, start_date, end_date, clickData, reset_all_button, reset_graph_button):
    ctx = callback_context

    dff = filter_dataframe(df, status, start_date, end_date)

    if ctx.triggered[0]["prop_id"] == "reset-all-button.n_clicks":
        date_min = df["CREATED"].min()
        date_max = df["CREATED"].max()
        dff = filter_dataframe(df, None, date_min, date_max)
    
    if ctx.triggered[0]["prop_id"] == "graph.clickData":
        date_graph = clickData["points"][0]["x"]
        dff = df.loc[df["CREATED"] == date_graph]

    if ctx.triggered[0]["prop_id"] == "reset-graph-button.n_clicks":
        dff = filter_dataframe(df, status, start_date, end_date)


    amount = dff["AMOUNT"].sum()
    total_prefix = ["Total Payments"]
    methods_list = df["PAYMENTMETHOD"].unique()
    payment_methods = np.append(total_prefix,methods_list)

    filtered_results = []
    for method in payment_methods:
        if method == "Total Payments":
            filtered_results.append("${:,.2f}".format(dff["AMOUNT"].sum() or 0))
            filtered_results.append(symbol(round(dff["AMOUNT"].sum() / amount * 100, 2) or 0))
            filtered_results.append({
                "text-align": "right",
                "color": "#27ae60",
                "font-size": "1.8rem"
            }),
        else:
            filtered_results.append("${:,.2f}".format(dff.loc[dff["PAYMENTMETHOD"] == method]["AMOUNT"].sum() or 0))
            filtered_results.append(symbol(round(dff.loc[dff["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0))
            filtered_results.append({
                "text-align": "right",
                "color": color(round(dff.loc[dff["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0),
                "font-size": "1.8rem"
            })

    return [
        *filtered_results,
        px.bar(
            dff,
            x="CREATED",
            y="AMOUNT",
            color="PAYMENTMETHOD",
            title="Payments",
            template="plotly_dark",
            labels={"CREATED": "Date", "AMOUNT": "Amount", "STATUS": "Status", "PAYMENTMETHOD": "Method"},
            hover_data=["AMOUNT", "STATUS", "PAYMENTMETHOD"],
        )
    ]