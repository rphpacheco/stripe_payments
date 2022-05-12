from dash import html
from src.app import app

logo = html.Img(
    src=app.get_asset_url("logo_dark.png"), 
    style={
        "width": "250px",
        "margin": "6px",
    }
)