import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from pages.components import navbar, register_navbar_callbacks

dash.register_page(__name__, path="/", name="VASupply")

card_users = html.A(
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(
                        "Afectados",
                        style={
                            "fontFamily": "Montserrat, sans-serif",
                            "fontWeight": "bold",
                            "color": "#2e7d32",
                            "fontSize": "1.3rem",
                            "marginBottom": "10px",
                        },
                    ),
                    html.P(
                        "Administra los afectados de la plataforma",
                        style={
                            "fontFamily": "Montserrat, sans-serif",
                            "color": "#333",
                            "fontSize": "1rem",
                        },
                    ),
                ]
            )
        ],
        className="home-cards",
        style={
            "borderRadius": "12px",
            "boxShadow": "0 2px 12px #0001",
            "border": "1px solid #e0e0e0",
            "transition": "0.3s",
            "background": "#f9fff6",
        },
    ),
    href="/afectados",
    style={"textDecoration": "none"},
)
card_enseres = html.A(
    dbc.Card(
        dbc.CardBody(
            [
                html.H4(
                    "Enseres",
                    style={
                        "fontFamily": "Montserrat, sans-serif",
                        "fontWeight": "bold",
                        "color": "#2e7d32",
                        "fontSize": "1.3rem",
                        "marginBottom": "10px",
                    },
                ),
                html.P(
                    "Administra los enseres de la plataforma",
                    style={
                        "fontFamily": "Montserrat, sans-serif",
                        "color": "#333",
                        "fontSize": "1rem",
                    },
                ),
            ]
        ),
        className="home-cards",
        style={
            "borderRadius": "12px",
            "boxShadow": "0 2px 12px #0001",
            "border": "1px solid #e0e0e0",
            "transition": "0.3s",
            "background": "#f9fff6",
        },
    ),
    href="/enseres",
    style={"textDecoration": "none"},
)

layout = html.Div(
    [
        navbar,
        html.H1(
            "Bienvenido a VASupply",
            style={
                "textAlign": "center",
                "fontFamily": "Montserrat, sans-serif",
                "fontWeight": "700",
                "fontSize": "2.3rem",
                "color": "#2e7d32",
                "margin": "30px 0 10px 0",
                "letterSpacing": "2px",
                "textShadow": "0 2px 8px #0001",
            },
        ),
        html.H2(
            "Selecciona tu acción",
            style={
                "textAlign": "center",
                "marginBottom": "40px",
                "fontFamily": "Montserrat, sans-serif",
                "fontWeight": "400",
                "color": "#1976d2",
                "fontSize": "1.3rem",
            },
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(card_users, width=6),
                        dbc.Col(card_enseres, width=6),
                    ],
                    style={"marginBottom": "30px"},
                )
            ]
        ),
    ]
)

