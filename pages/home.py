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
                    html.H4("Afectados"),
                    html.P("Administra los afectados de la plataforma"),
                ]
            )
        ],
        className="home-cards",
    ),
    href="/afectados",
    style={"text-decoration": "none"},
)
card_enseres = html.A(
    dbc.Card(
        dbc.CardBody(
            [
                html.H4("Enseres"),
                html.P("Administra los enseres de la plataforma"),
            ]
        ),
        className="home-cards",
    ),
    href="/enseres",
    style={"text-decoration": "none"},
)
# card_admin = html.A(
#     dbc.Card(
#         dbc.CardBody(
#             [
#                 html.H4("Admin"),
#                 html.P("Administra la plataforma"),
#             ]
#         ),
#         className="home-cards",
#     ),
#     href="/admin_usuarios",
#     style={"text-decoration": "none"},
#     className="home-cards",
# )

layout = html.Div(
    [
        navbar,
        html.H1("Bienvenido a VASupply", style={"textAlign": "center"}),
        html.H2(
            "Selecciona tu acción",
            style={"textAlign": "center", "marginBottom": "40px"},
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(card_users, width=6),
                        dbc.Col(card_enseres, width=6),
                    ]
                )
            ]
        ),
    ]
)

