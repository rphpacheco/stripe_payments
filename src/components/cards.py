from dash import html
import dash_bootstrap_components as dbc

def symbol(total_percent): 
    if total_percent <= 10:
        return f"{total_percent}% ▼"
    elif total_percent <= 20:
        return f"{total_percent}% ▶"
    else:
        return f"{total_percent}% ▲"

def color(total_percent): 
    if total_percent <= 10:
        return "#e74c3c"
    elif total_percent <= 20:
        return "#f1c40f"
    else:
        return "#27ae60"

def cards(df, df_total, title, class_icon, mode="inactive"):
    amount = df["AMOUNT"].sum()
    total_percent = round(amount / df_total['AMOUNT'].sum() * 100, 2)

    return html.Div(
        id=f"{title.lower().replace(' ','-')}-card",
        children=[
            dbc.Row([
                dbc.Col([
                    html.I(
                        className=class_icon,
                        style={
                            "background": "radial-gradient(circle, rgba(99,91,255,1) 0%, rgba(99,91,255,0) 75%)",
                            "color": "#FFF80",
                            "border-radius": "50%",
                            "padding": "10px",
                            "font-size": "2.2rem",
                        }
                    )
                ],
                style={
                    "margin": "-20px 5px 0px -20px",
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                }),
                dbc.Col([
                    html.H5(
                        title, 
                        style={
                            "text-align": "center",
                            "color": "#FFF" if mode == "active" else "#838689",
                        }),
                    html.H2(
                        id=f"{title.lower().replace(' ','-')}-amount",
                        children=[
                            "${:,.2f}".format(amount)
                        ],
                        style={
                            "font-size": "2.5rem",
                            "text-align": "center",
                            "color": "#FFF" if mode == "active" else "#9BCDFF",
                        }
                    ),
                    html.P(
                        id=f"{title.lower().replace(' ','-')}-percent",
                        children=[
                            symbol(total_percent),
                        ],
                        style={
                            "text-align": "right",
                            "color": color(total_percent),
                            "font-size": "1.8rem"
                        }
                    )
                ])
            ])
    ],
    style={
        "width": "auto",
        "margin": "auto 10px",
        "background": "linear-gradient(90deg, rgba(22,18,96,1) 0%, rgba(99,91,255,0.7987570028011204) 100%)" if mode == "active" else "#131314",
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "center",
        "align-items": "center",
        "padding-top": "15px",
        "border": "0.5px solid #2C2D33",
        "border-left-color": "#161260" if mode == "active" else "#635bffBF",
        "border-left-width": "0px" if mode == "active" else "10px",
        "border-radius": "4px",
    })