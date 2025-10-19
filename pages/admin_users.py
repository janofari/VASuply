import dash
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import current_app, session

from services.database.sqlite_db_handler import fetch_users, insert_users, delete_db, update_db
from pages.components import navbar, register_navbar_callbacks

dash.register_page(__name__, path="/admin_usuarios", name="Usuarios")

layout = [navbar,html.Div(id="admin-users-content")]


@callback(Output("admin-users-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if session.get("user_group") == "Admin":
        users_data = pd.DataFrame(fetch_users())
        return html.Div(
            [
                html.H1("Gestión de Usuarios", style={
                    "fontFamily": "Montserrat, sans-serif",
                    "fontWeight": "700",
                    "fontSize": "2.1rem",
                    "color": "#2e7d32",
                    "marginBottom": "18px",
                    "letterSpacing": "1px"
                }),
                dash_table.DataTable(
                    id="usuarios-table",
                    columns=[
                        {"name": "Nombre", "id": "nombre", "editable": True},
                        {"name": "Email", "id": "email", "editable": True},
                        {"name": "Rol", "id": "rol", "editable": True},
                    ],
                    data=users_data.to_dict("records"),
                    row_deletable=True,
                    editable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "filtrar por ..."},
                    page_size=20,
                    style_table={"marginBottom": "30px", "borderRadius": "10px", "overflow": "hidden", "boxShadow": "0 2px 12px #0002", "tableLayout": "fixed", "width": "100%"},
                    style_header={
                        "backgroundColor": "#2e7d32",
                        "color": "white",
                        "fontWeight": "bold",
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "1.1rem",
                        "border": "none"
                    },
                    style_cell={
                        "fontFamily": "Montserrat, sans-serif",
                        "fontSize": "1rem",
                        "padding": "8px",
                        "maxWidth": "200px",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "whiteSpace": "nowrap"
                    },
                    style_data_conditional=[
                        {
                            "if": {"state": "selected"},
                            "backgroundColor": "#f2f7fa",
                            "border": "1px solid #1976d2"
                        }
                    ],
                    style_as_list_view=True,
                ),
                html.Div(
                    [
                        dcc.Input(id="new-user-name", type="text", placeholder="Nombre", style={"margin": "5px", "width": "140px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                        dcc.Input(id="new-user-password", type="password", placeholder="Contraseña", style={"margin": "5px", "width": "140px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                        dcc.Input(id="new-user-email", type="email", placeholder="Email", style={"margin": "5px", "width": "180px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                        dcc.Dropdown(
                            id="new-user-rol",
                            options=[
                                {"label": "Admin", "value": "Admin"},
                                {"label": "User", "value": "User"},
                            ],
                            placeholder="Rol",
                            style={"width": "150px", "margin": "5px", "height": "40px", "borderRadius": "6px"},
                        ),
                        html.Button(
                            "Añadir Usuario",
                            id="add-user-btn",
                            n_clicks=0,
                            style={
                                "margin": "5px 0 5px 10px",
                                "padding": "8px 18px",
                                "backgroundColor": "#2e7d32",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "6px",
                                "fontWeight": "bold",
                                "cursor": "pointer",
                                "height": "40px",
                                "boxShadow": "0 2px 8px #1976d233"
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "alignItems": "center",
                        "gap": "8px",
                        "marginBottom": "25px",
                        "background": "#f7f7f7",
                        "padding": "15px 10px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 12px #0001"
                    },
                ),
                html.Div(id="output-users"),
            ],
            style={"margin": "30px", "background": "#fff", "borderRadius": "12px", "boxShadow": "0 2px 16px #0001", "padding": "20px"}
        )
    else:
        return html.Div("No tiene permisos para acceder a esta página.", style={
            "fontFamily": "Montserrat, sans-serif",
            "fontSize": "1.2rem",
            "color": "#b71c1c",
            "margin": "30px"
        })


@callback(
    Output("usuarios-table", "data"),
    Input("add-user-btn", "n_clicks"),
    State("new-user-name", "value"),
    State("new-user-password", "value"),
    State("new-user-email", "value"),
    State("new-user-rol", "value"),
    State("usuarios-table", "data"),
)
def add_user(n_clicks, name, password, email, rol, rows):
    if n_clicks > 0 and name and password and email and rol:
        new_row = {"nombre": name, "email": email, "rol": rol}
        rows.append(new_row)
        insert_users(
            "user_info", {"usuario": name, "psw": password, "email": email, "role": rol}
        )
    return rows


@callback(
    Output("output-users", "children"),
    Input("usuarios-table", "data_previous"),
    Input("usuarios-table", "data"),
)
def update_or_delete_users(previous_rows, current_rows):
    if previous_rows is None:
        previous_rows = []

    previous_set = {row["nombre"]: row for row in previous_rows}
    current_set = {row["nombre"]: row for row in current_rows}

    # Detect deleted rows
    deleted_users = set(previous_set.keys()) - set(current_set.keys())
    for user in deleted_users:
        delete_db("user_info", {"usuario": user})

    # Detect updated rows
    for user, data in current_set.items():
        if user in previous_set and data != previous_set[user]:
            update_db(
                "user_info",
                {"email": data["email"], "role": data["rol"]},
                {"usuario": user},
            )

    return "Usuarios actualizados"
