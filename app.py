# -*- coding: utf-8 -*-
import os

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_auth import BasicAuth
from flask import request, Response

from pages.components import navbar, register_navbar_callbacks
from services.database.sqlite_db_handler import validate_user, insert_users


# =========================================
# Configuración de la aplicación
# =========================================
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

server = app.server
app.server.secret_key = os.urandom(24).hex()

# =========================================
# Configuración de autenticación
# =========================================

@server.before_request
def proteger_rutas():
    path = request.path.rstrip('/')

    PREFIJOS_PUBLICOS = (
        "/formulario",              
        "/assets",                  
        "/_dash-component-suites",   
        "/_dash-layout",             
        "/_dash-dependencies",       
        "/_reload-hash",             
        "/_favicon.ico",
        "/_dash-update-component"              
    )

    if path.startswith(PREFIJOS_PUBLICOS):
        return None

    auth = request.authorization
    if not auth or not validate_user(auth.username, auth.password):
        return Response(
            "Acceso denegado. Debes iniciar sesión.",
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Login Required"'}
        )
    
# =========================================
# Layout principal
# =========================================
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
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

# =========================================
# Main
# =========================================
if __name__ == "__main__":
    app.run(debug=False, dev_tools_ui=False, port=8055)