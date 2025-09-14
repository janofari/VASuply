import dash
import pandas as pd
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import session  # , current_app


dash.register_page(__name__, path="/afectados", name="Afectados")

layout = html.Div(id="afectados-content")


global dummy_data
dummy_data = [
    {
        "id": 1,
        "afectado": "Juan Perez",
        "ubi": "Madrid",
        "necesidad": "Agua",
        "dni": "50256778F",
        "tlf": "123456789",
    },
    {
        "id": 2,
        "afectado": "Antonio Ruin",
        "ubi": "Torrelodones",
        "necesidad": "Amigos",
        "dni": "12346778F",
        "tlf": "123456789",
    },
    {
        "id": 3,
        "afectado": "El Fari",
        "ubi": "Grieta",
        "necesidad": "Elo",
        "dni": "43256778F",
        "tlf": "123456789",
    },
    {
        "id": 4,
        "afectado": "Don Cerve",
        "ubi": "Bar",
        "necesidad": "Cerveza",
        "dni": "50456778F",
        "tlf": "123456789",
    },
    {
        "id": 5,
        "afectado": "Fernando Alonso",
        "ubi": "Asturias",
        "necesidad": "33",
        "dni": "90256778F",
        "tlf": "123456789",
    },
]


# Dummy data function
def fetch_users():
    global dummy_data
    dummy_data = [
        {
            "id": 1,
            "afectado": "Juan Perez",
            "ubi": "Madrid",
            "necesidad": "Agua",
            "dni": "50256778F",
            "tlf": "123456789",
        },
        {
            "id": 2,
            "afectado": "Antonio Ruin",
            "ubi": "Torrelodones",
            "necesidad": "Amigos",
            "dni": "12346778F",
            "tlf": "123456789",
        },
        {
            "id": 3,
            "afectado": "El Fari",
            "ubi": "Grieta",
            "necesidad": "Elo",
            "dni": "43256778F",
            "tlf": "123456789",
        },
        {
            "id": 4,
            "afectado": "Don Cerve",
            "ubi": "Bar",
            "necesidad": "Cerveza",
            "dni": "50456778F",
            "tlf": "123456789",
        },
        {
            "id": 5,
            "afectado": "Fernando Alonso",
            "ubi": "Asturias",
            "necesidad": "33",
            "dni": "90256778F",
            "tlf": "123456789",
        },
    ]
    return pd.DataFrame(dummy_data)


# Dummy data function
def search_afectado(name, ubi, nec, dni, tlf):
    global dummy_data
    matches_list = []
    for i in dummy_data:
        if (
            i["afectado"] == name
            and i["ubi"] == ubi
            and i["necesidad"] == nec
            and i["dni"] == dni
            and i["tlf"] == tlf
        ):
            matches_list.append(i)
    return pd.DataFrame(matches_list)





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
                        {"name": "DNI", "id": "dni", "editable": True},
                        {"name": "Telefono", "id": "tlf", "editable": True},
                    ],
                    data=fetch_users().to_dict("records"),
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
                html.Button(
                    "Buscar Afectado",
                    id="search-afectado-btn",
                    n_clicks=0,
                    style={"margin": "10px"},
                ),
                dcc.Input(id="search-afectado-name", type="text", placeholder="Nombre"),
                dcc.Input(
                    id="search-afectado-ubi", type="text", placeholder="Ubicacion"
                ),
                dcc.Input(
                    id="search-afectado-nec", type="text", placeholder="Necesidad"
                ),
                dcc.Input(id="search-afectado-dni", type="text", placeholder="DNI"),
                dcc.Input(
                    id="search-afectado-tlf", type="text", placeholder="Telefono"
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
        new_id = max(row["id"] for row in rows) + 1 if rows else 1
        new_row = {
            "id": new_id,
            "afectado": name,
            "ubi": ubi,
            "necesidad": nec,
            "dni": dni,
            "tlf": tlf,
        }
        rows.append(new_row)
        dummy_data.append(new_row)

    return rows


@callback(
    Output("output-search-afectados", "children"),
    Input("search-afectado-btn", "n_clicks"),
    State("search-afectado-name", "value"),
    State("search-afectado-ubi", "value"),
    State("search-afectado-nec", "value"),
    State("search-afectado-dni", "value"),
    State("search-afectado-tlf", "value"),
)
def search_afectados(n_clicks, name, ubi, nec, dni, tlf):
    if n_clicks > 0:
        afectados_match = search_afectado(name, ubi, nec, dni, tlf)
        # mongo_handler = current_app.config["mongo_handler"]
        # afectados_match = pd.DataFrame(mongo_handler.search_afectado(name, ubi, nec, dni, tlf))
        if not afectados_match.empty:
            return html.Div(
                [
                    html.H2(f"Afectado(s) encontrados = {len(afectados_match)}"),
                    dash_table.DataTable(
                        id="afectados-table",
                        columns=[
                            {"name": "Afectado", "id": "afectado"},
                            {"name": "Ubicacion", "id": "ubi"},
                            {"name": "Necesidad", "id": "necesidad"},
                            {"name": "DNI", "id": "dni"},
                            {"name": "Telefono", "id": "tlf"},
                        ],
                        data=afectados_match.to_dict("records"),
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
def update_or_delete_users(previous_rows, current_rows):
    if previous_rows is None:
        previous_rows = []

    previous_set = {row["id"]: row for row in previous_rows}
    current_set = {row["id"]: row for row in current_rows}

    # mongo_handler = current_app.config["mongo_handler"]
    # afectados_match = pd.DataFrame(mongo_handler.search_afectado(name, ubi, nec, dni, tlf))

    # Detect deleted rows
    deleted_afectados = set(previous_set.keys()) - set(current_set.keys())
    for afectado in deleted_afectados:
        # mongo_handler.delete_afectado(afectado)
        print(f"Deleted afectado with id {afectado}")
        dummy_data[:] = [row for row in dummy_data if row["id"] != afectado]

    # Detect updated rows
    for id, data in current_set.items():
        for row in dummy_data:
            if row["id"] == id and data != row:
                print(f"Updated afectado with id {id}")
                row.update_db(data)
