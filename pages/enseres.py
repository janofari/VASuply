import dash
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import session


dash.register_page(__name__, path="/enseres", name="Enseres")

layout = html.Div(id="enseres-content")

global dummy_enseres
dummy_enseres = [
    {
        "id": 1,
        "enser": "Mesa",
        "cantidad": 2,
        "medidas": "120x60",
        "estado": "Nuevo",
        "donante": "Juan Perez",
        "agraciado": "Maria",
    },
    {
        "id": 2,
        "enser": "Silla",
        "cantidad": 4,
        "medidas": "40x40",
        "estado": "Usado",
        "donante": "Antonio Ruin",
        "agraciado": "Luis",
    },
    {
        "id": 3,
        "enser": "Cama",
        "cantidad": 1,
        "medidas": "200x150",
        "estado": "Nuevo",
        "donante": "El Fari",
        "agraciado": "Fernando Alonso",
    },
    {
        "id": 4,
        "enser": "Escritorio",
        "cantidad": 1,
        "medidas": "150x75",
        "estado": "Usado",
        "donante": "Don Cerve",
        "agraciado": "Pedro",
    },
    {
        "id": 5,
        "enser": "Armario",
        "cantidad": 1,
        "medidas": "180x90",
        "estado": "Nuevo",
        "donante": "Fernando Alonso",
        "agraciado": "Juan Perez",
    },
    {
        "id": 6,
        "enser": "Sofá",
        "cantidad": 1,
        "medidas": "200x100",
        "estado": "Usado",
        "donante": "Luis",
        "agraciado": "Antonio Ruin",
    },
    {
        "id": 7,
        "enser": "Lámpara",
        "cantidad": 3,
        "medidas": "50x50",
        "estado": "Nuevo",
        "donante": "Maria",
        "agraciado": "El Fari",
    },
]


# Dummy data function
def fetch_enseres():
    global dummy_enseres
    return pd.DataFrame(dummy_enseres)


# Dummy data function
def search_enser(enser, cantidad, medidas, estado, donante, agraciado):
    global dummy_enseres
    matches_list = []
    for i in dummy_enseres:
        if (
            (enser is None or i["enser"] == enser)
            and (cantidad is None or i["cantidad"] == cantidad)
            and (medidas is None or i["medidas"] == medidas)
            and (estado is None or i["estado"] == estado)
            and (donante is None or i["donante"] == donante)
            and (agraciado is None or i["agraciado"] == agraciado)
        ):
            matches_list.append(i)
    return pd.DataFrame(matches_list)




@callback(Output("enseres-content", "children"), Input("url", "pathname"))
def display_enseres(_):
    if session.get("user_group") == "Admin":
        return html.Div(
            [
                html.H1("Gestión de Enseres"),
                dash_table.DataTable(
                    id="enseres-table",
                    columns=[
                        {"name": "Enser", "id": "enser", "editable": False},
                        {"name": "Cantidad", "id": "cantidad", "editable": True},
                        {"name": "Medidas", "id": "medidas", "editable": True},
                        {"name": "Estado", "id": "estado", "editable": True},
                        {"name": "Donante", "id": "donante", "editable": True},
                        {"name": "Agraciado", "id": "agraciado", "editable": True},
                    ],
                    data=fetch_enseres().to_dict("records"),
                    row_deletable=True,
                    editable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "filtrar por ..."},
                ),
                html.Button(
                    "Añadir Enser",
                    id="add-enser-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                dcc.Input(id="new-enser-name", type="text", placeholder="Enser"),
                dcc.Input(
                    id="new-enser-cantidad", type="number", placeholder="Cantidad"
                ),
                dcc.Input(id="new-enser-medidas", type="text", placeholder="Medidas"),
                dcc.Input(id="new-enser-estado", type="text", placeholder="Estado"),
                dcc.Input(id="new-enser-donante", type="text", placeholder="Donante"),
                dcc.Input(
                    id="new-enser-agraciado", type="text", placeholder="Agraciado"
                ),
            ],
            style={"margin": "30px"},
        )
    else:
        return html.Div(
            [
                html.H1("Busqueda de Enseres"),
                html.Button(
                    "Buscar Enser",
                    id="search-enser-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                dcc.Input(id="search-enser-name", type="text", placeholder="Enser"),
                dcc.Input(
                    id="search-enser-cantidad", type="number", placeholder="Cantidad"
                ),
                dcc.Input(
                    id="search-enser-medidas", type="text", placeholder="Medidas"
                ),
                dcc.Input(id="search-enser-estado", type="text", placeholder="Estado"),
                dcc.Input(
                    id="search-enser-donante", type="text", placeholder="Donante"
                ),
                dcc.Input(
                    id="search-enser-agraciado", type="text", placeholder="Agraciado"
                ),
                html.Div(id="output-search-enseres"),
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
        new_id = max(row["id"] for row in rows) + 1 if rows else 1
        new_row = {
            "id": new_id,
            "enser": enser,
            "cantidad": cantidad,
            "medidas": medidas,
            "estado": estado,
            "donante": donante,
            "agraciado": agraciado,
        }
        rows.append(new_row)
        dummy_enseres.append(new_row)

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
def search_enseres(n_clicks, enser, cantidad, medidas, estado, donante, agraciado):
    if n_clicks > 0:
        enseres_match = search_enser(
            enser, cantidad, medidas, estado, donante, agraciado
        )
        if not enseres_match.empty:
            return html.Div(
                [
                    html.H2(f"Enser(es) encontrados = {len(enseres_match)}"),
                    dash_table.DataTable(
                        id="enseres-table",
                        columns=[
                            {"name": "Enser", "id": "enser"},
                            {"name": "Cantidad", "id": "cantidad"},
                            {"name": "Medidas", "id": "medidas"},
                            {"name": "Estado", "id": "estado"},
                            {"name": "Donante", "id": "donante"},
                            {"name": "Agraciado", "id": "agraciado"},
                        ],
                        data=enseres_match.to_dict("records"),
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
    for enser in deleted_enseres:
        print(f"Deleted enser with id {enser}")
        dummy_enseres[:] = [row for row in dummy_enseres if row["id"] != enser]

    # Detect updated rows
    for id, data in current_set.items():
        for row in dummy_enseres:
            if row["id"] == id and data != row:
                print(f"Updated enser with id {id}")
                row.update_db(data)
