import dash
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import session
from services.database.sqlite_db_handler import (
    fetch_enseres,
    insert_enser,
    search_enseres,
    update_enser,
    delete_enser,
)
from pages.components import navbar, register_navbar_callbacks


dash.register_page(__name__, path="/enseres", name="Enseres")

layout = [navbar, html.Div(id="enseres-content")]


@callback(Output("enseres-content", "children"), Input("url", "pathname"))
def display_enseres(_):
    return html.Div(
        [
            html.H1("Gestión de Enseres"),
            dash_table.DataTable(
                id="enseres-table",
                columns=[
                    {"name": "Enser", "id": "enser", "editable": False},
                    {"name": "Cantidad", "id": "cantidad", "editable": True},
                    {"name": "Medidas", "id": "medidas", "editable": True},
                    {"name": "Estado", "id": "estado", "presentation": "dropdown"},
                    {"name": "Donante", "id": "donante", "editable": True},
                    {"name": "Agraciado", "id": "agraciado", "editable": True},
                ],
                data=fetch_enseres(),
                row_deletable=True,
                editable=True,
                filter_action="native",
                filter_options={"placeholder_text": "filtrar por ..."},
                dropdown={
                    "estado": {
                        "options": [
                            {"label": "Perfecto", "value": "Perfecto"},
                            {"label": "Bueno", "value": "Bueno"},
                            {"label": "Aceptable", "value": "Aceptable"},
                            {"label": "Malo", "value": "Malo"},
                            {"label": "Deplorable", "value": "Deplorable"},
                        ]
                    }
                },
            ),
            html.Div(
                [
                    dcc.Input(id="new-enser-name", type="text", placeholder="Enser"),
                    dcc.Input(
                        id="new-enser-cantidad", type="number", placeholder="Cantidad", min=0
                    ),
                    dcc.Input(id="new-enser-medidas", type="text", placeholder="Medidas"),
                    dcc.Dropdown(
                        id="new-enser-estado",
                        options=[
                            {"label": "Perfecto", "value": "Perfecto"},
                            {"label": "Bueno", "value": "Bueno"},
                            {"label": "Aceptable", "value": "Aceptable"},
                            {"label": "Malo", "value": "Malo"},
                            {"label": "Deplorable", "value": "Deplorable"},
                        ],
                        placeholder="Estado",
                        style={"marginBottom": "0px"},
                    ),
                    dcc.Input(id="new-enser-donante", type="text", placeholder="Donante"),
                    dcc.Input(
                        id="new-enser-agraciado", type="text", placeholder="Agraciado"
                    ),
                ],
                className="enseres-form-row",
            ),
            html.Button(
                "Añadir Enser",
                id="add-enser-btn",
                n_clicks=0,
                style={"margin": "10px"},
            ),
        ],
        style={"margin": "30px"},
    )


@callback(
    Output("enseres-table", "data"),
    Input("add-enser-btn", "n_clicks"),
    State("new-enser-name", "value"),
    State("new-enser-cantidad", "value"),
    State("new-enser-medidas", "value"),
    State("new-enser-estado", "value"),
    State("new-enser-donante", "value"),
    State("new-enser-agraciado", "value"),
    State("enseres-table", "data"),
)
def add_enser(n_clicks, enser, cantidad, medidas, estado, donante, agraciado, rows):
    if (
        n_clicks > 0
        and enser
        and cantidad
        and medidas
        and estado
        and donante
        and agraciado
    ):
        new_row = {
            "enser": enser,
            "cantidad": cantidad,
            "medidas": medidas,
            "estado": estado,
            "donante": donante,
            "agraciado": agraciado,
        }
        insert_enser(new_row)
        return fetch_enseres()
    return rows


@callback(
    Output("output-search-enseres", "children"),
    Input("search-enser-btn", "n_clicks"),
    State("search-enser-name", "value"),
    State("search-enser-cantidad", "value"),
    State("search-enser-medidas", "value"),
    State("search-enser-estado", "value"),
    State("search-enser-donante", "value"),
    State("search-enser-agraciado", "value"),
)
def search_enseres_callback(n_clicks, enser, cantidad, medidas, estado, donante, agraciado):
    if n_clicks > 0:
        enseres_match = search_enseres(enser, cantidad, medidas, estado, donante, agraciado)
        if enseres_match:
            return html.Div(
                [
                    html.H2(f"Enser(es) encontrados = {len(enseres_match)}"),
                    dash_table.DataTable(
                        id="enseres-table-search",
                        columns=[
                            {"name": "Enser", "id": "enser"},
                            {"name": "Cantidad", "id": "cantidad"},
                            {"name": "Medidas", "id": "medidas"},
                            {"name": "Estado", "id": "estado"},
                            {"name": "Donante", "id": "donante"},
                            {"name": "Agraciado", "id": "agraciado"},
                        ],
                        data=enseres_match,
                        filter_action="native",
                        filter_options={"placeholder_text": "filtrar por ..."},
                    ),
                ]
            )
        else:
            return html.H2("No se encontraron enseres coincidentes")


@callback(
    Input("enseres-table", "data_previous"),
    Input("enseres-table", "data"),
)
def update_or_delete_enseres(previous_rows, current_rows):
    if previous_rows is None:
        previous_rows = []
    previous_set = {row["id"]: row for row in previous_rows}
    current_set = {row["id"]: row for row in current_rows}
    # Detect deleted rows
    deleted_enseres = set(previous_set.keys()) - set(current_set.keys())
    for enser_id in deleted_enseres:
        delete_enser(enser_id)
    # Detect updated rows
    for id, data in current_set.items():
        if id in previous_set and data != previous_set[id]:
            update_enser(id, data)
