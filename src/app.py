import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME, "assets/style.css"])
app.scripts.config.serve_locally = True
server = app.server