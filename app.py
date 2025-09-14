# -*- coding: utf-8 -*-
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_auth import BasicAuth

from pages.components import navbar, register_navbar_callbacks
from services.database.sqlite_db_handler import validate_user


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap",
    ],
    use_pages=True,
)
app.title = "VASupply"

# BasicAuth(app, auth_func=validate_user)

server = app.server
app.server.secret_key = os.urandom(24).hex()

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        html.Div(
            style={
                "position": "fixed",
                "top": "0",
                "right": "0",
                "left": "0",
                "bottom": "0",
                "zIndex": "-1",
                "backgroundColor": "#ffffff",
                "height": "100vh",
                "width": "100%",
                "font-family": "Montserrat, sans-serif",
            }
        ),
        dash.page_container,
    ]
)

register_navbar_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
