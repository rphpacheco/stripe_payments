from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from src.app import app
from src.layouts import layout

app.layout = layout

if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)