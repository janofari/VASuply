import dash
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import session
from services.database.sqlite_db_handler import (
    fetch_afectados,
    insert_afectado,
    search_afectados,
    update_afectado,
    delete_afectado,
)
from pages.components import navbar, register_navbar_callbacks


dash.register_page(__name__, path="/afectados", name="Afectados")

layout = [navbar, html.Div(id="afectados-content")]


@callback(Output("afectados-content", "children"), Input("url", "pathname"))
def display_afectados(_):
    if session.get("user_group") == "Admin":
        return html.Div(
            [
                html.H1("Gestión de Afectados"),
                dash_table.DataTable(
                    id="afectados-table",
                    columns=[
                        {"name": "Afectado", "id": "afectado", "editable": False},
                        {"name": "Ubicacion", "id": "ubi", "editable": True},
                        {"name": "Necesidad", "id": "necesidad", "editable": True},
                        {"name": "Telefono", "id": "tlf", "editable": True},
                    ],
                    data=fetch_afectados(),
                    row_deletable=True,
                    editable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "filtrar por ..."},
                ),
                html.Button(
                    "Añadir Afectado",
                    id="add-afectado-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                dcc.Input(id="new-afectado-name", type="text", placeholder="Nombre"),
                dcc.Input(id="new-afectado-ubi", type="text", placeholder="Ubicacion"),
                dcc.Input(id="new-afectado-nec", type="text", placeholder="Necesidad"),
                dcc.Input(id="new-afectado-dni", type="text", placeholder="DNI"),
                dcc.Input(id="new-afectado-tlf", type="text", placeholder="Telefono"),
            ],
            style={"margin": "30px"},
        )
    else:
        return html.Div(
            [
                html.H1("Busqueda de Afectados"),
                dcc.Dropdown(
                    id="search-criteria-dropdown",
                    options=[
                        {"label": "Nombre", "value": "nombre"},
                        {"label": "DNI", "value": "dni"},
                        {"label": "Telefono", "value": "tlf"},
                    ],
                    value="nombre",
                    clearable=False,
                    style={"width": "250px", "marginBottom": "10px"},
                ),
                dcc.Input(
                    id="search-afectado-input",
                    type="text",
                    placeholder="Buscar...",
                    style={"marginBottom": "10px"},
                ),
                html.Button(
                    "Buscar Afectado",
                    id="search-afectado-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                html.Div(id="output-search-afectados"),
            ],
            style={"margin": "30px"},
        )


@callback(
    Output("afectados-table", "data"),
    Input("add-afectado-btn", "n_clicks"),
    State("new-afectado-name", "value"),
    State("new-afectado-ubi", "value"),
    State("new-afectado-nec", "value"),
    State("new-afectado-dni", "value"),
    State("new-afectado-tlf", "value"),
    State("afectados-table", "data"),
)
def add_afectado(n_clicks, name, ubi, nec, dni, tlf, rows):
    if n_clicks > 0 and name and ubi and nec and dni and tlf:
        new_row = {
            "afectado": name,
            "ubi": ubi,
            "necesidad": nec,
            "dni": dni,
            "tlf": tlf,
        }
        insert_afectado(new_row)
        return fetch_afectados()
    return rows


@callback(
    Output("output-search-afectados", "children"),
    Input("search-afectado-btn", "n_clicks"),
    State("search-criteria-dropdown", "value"),
    State("search-afectado-input", "value"),
)
def search_afectados_callback(n_clicks, criterio, valor):
    if n_clicks > 0 and valor:
        if criterio == "nombre":
            afectados_match = search_afectados(name=valor)
        elif criterio == "dni":
            afectados_match = search_afectados(dni=valor)
        elif criterio == "tlf":
            afectados_match = search_afectados(tlf=valor)
        else:
            afectados_match = []
        if afectados_match:
            return html.Div(
                [
                    html.H2(f"Afectado(s) encontrados = {len(afectados_match)}"),
                    dash_table.DataTable(
                        id="afectados-table-search",
                        columns=[
                            {"name": "Afectado", "id": "afectado"},
                            {"name": "Ubicacion", "id": "ubi"},
                            {"name": "Necesidad", "id": "necesidad"},
                            {"name": "Telefono", "id": "tlf"},
                        ],
                        data=afectados_match,
                        filter_action="native",
                        filter_options={"placeholder_text": "filtrar por ..."},
                    ),
                ]
            )
        else:
            return html.H2("No se encontraron afectados coincidentes")


@callback(
    Input("afectados-table", "data_previous"),
    Input("afectados-table", "data"),
)
def update_or_delete_afectados(previous_rows, current_rows):
    if previous_rows is None:
        previous_rows = []
    previous_set = {row["id"]: row for row in previous_rows}
    current_set = {row["id"]: row for row in current_rows}
    # Detect deleted rows
    deleted_afectados = set(previous_set.keys()) - set(current_set.keys())
    for afectado_id in deleted_afectados:
        delete_afectado(afectado_id)
    # Detect updated rows
    for id, data in current_set.items():
        if id in previous_set and data != previous_set[id]:
            update_afectado(id, data)
