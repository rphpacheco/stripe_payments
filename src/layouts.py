import json
import numpy as np
from dash import html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from src.app import app
import pandas as pd
from datetime import datetime, date

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
                        status_controller(df),
                        controllers(df),
                        date_picker(),
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
)
def update_status_dropdown(status, start_date, end_date, clickData):
    ctx = callback_context
    print(ctx.args_grouping)
    # if clickData is None:
    if start_date is None and end_date is not None:
        df_dt_filtered = df.loc[df["CREATED"] <= end_date]
    elif start_date is not None and end_date is None:
        df_dt_filtered = df.loc[df["CREATED"] >= start_date]
    elif start_date is not None and end_date is not None:
        df_dt_filtered = df.loc[(df["CREATED"] >= start_date) & (df["CREATED"] <= end_date)]
    else:
        df_dt_filtered = df
    # else:
    #     chart_date = clickData['points'][0]['x']
    #     df_dt_filtered = df.loc[(df["CREATED"] == chart_date)]
    #     # print(df_dt_filtered.head())
    #     clickData == None
    
    amount = df_dt_filtered["AMOUNT"].sum()
    total_prefix = ["Total Payments"]
    methods_list = df_dt_filtered["PAYMENTMETHOD"].unique()
    payment_methods = np.append(total_prefix,methods_list)
    
    if 'df' in globals() and status not in ["Success", "Fail"] or status == None:
        filtered_results = []
        for method in payment_methods:
            if method == "Total Payments":
                filtered_results.append("${:,.2f}".format(df_dt_filtered["AMOUNT"].sum() or 0))
                filtered_results.append(symbol(round(df_dt_filtered["AMOUNT"].sum() / amount * 100, 2) or 0))
                filtered_results.append({
                    "text-align": "right",
                    "color": "#27ae60",
                    "font-size": "1.8rem"
                }),
            else:
                filtered_results.append("${:,.2f}".format(df_dt_filtered.loc[df_dt_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() or 0))
                filtered_results.append(symbol(round(df_dt_filtered.loc[df_dt_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0))
                filtered_results.append({
                    "text-align": "right",
                    "color": color(round(df_dt_filtered.loc[df_dt_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0),
                    "font-size": "1.8rem"
                })
        
        return [ 
            *filtered_results,
            px.bar(
                df_dt_filtered,
                x="CREATED",
                y="AMOUNT",
                color="PAYMENTMETHOD",
                title="Payments",
                template="plotly_dark",
                labels={"CREATED": "Date", "AMOUNT": "Amount", "STATUS": "Status", "PAYMENTMETHOD": "Method"},
            )
        ]
    else:
        df_filtered = df_dt_filtered.loc[df_dt_filtered["STATUS"] == status, :]
        filtered_results = []
        for method in payment_methods:
            if method == "Total Payments":
                filtered_results.append("${:,.2f}".format(df_filtered["AMOUNT"].sum() or 0))
                filtered_results.append(symbol(round(df_filtered["AMOUNT"].sum() / amount * 100, 2) or 0))
                filtered_results.append({
                    "text-align": "right",
                    "color": color(round(df_filtered["AMOUNT"].sum() / amount * 100, 2) or 0),
                    "font-size": "1.8rem"
                }),
            else:
                filtered_results.append("${:,.2f}".format(df_filtered.loc[df_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() or 0))
                filtered_results.append(symbol(round(df_filtered.loc[df_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0))
                filtered_results.append({
                    "text-align": "right",
                    "color": color(round(df_filtered.loc[df_filtered["PAYMENTMETHOD"] == method]["AMOUNT"].sum() / amount * 100, 2) or 0),
                    "font-size": "1.8rem"
                })
        
        return [ 
            *filtered_results,
            px.bar(
                df_filtered,
                x="CREATED",
                y="AMOUNT",
                color="PAYMENTMETHOD",
                title="Payments",
                template="plotly_dark",
                labels={"CREATED": "Date", "AMOUNT": "Amount", "STATUS": "Status", "PAYMENTMETHOD": "Method"},
            )
        ]
