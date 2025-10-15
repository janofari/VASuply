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
            html.H1("Gestión de Enseres", style={
                "fontFamily": "Montserrat, sans-serif",
                "fontWeight": "700",
                "fontSize": "2.1rem",
                "color": "#2e7d32",
                "marginBottom": "18px",
                "letterSpacing": "1px"
            }),
            dash_table.DataTable(
                id="enseres-table",
                columns=[
                    {"name": "Enser", "id": "enser", "editable": False},
                    {"name": "Tipo", "id": "tipo", "editable": True},
                    {"name": "Cantidad", "id": "cantidad", "editable": True},
                    {"name": "Medidas", "id": "medidas", "editable": True},
                    {"name": "Estado", "id": "estado", "editable": True},
                    {"name": "Donante", "id": "donante", "editable": True},
                    {"name": "Agraciado", "id": "agraciado", "editable": True}, 
                ],
                data=fetch_enseres(),
                row_deletable=True,
                editable=True,
                filter_action="native",
                filter_options={"placeholder_text": "filtrar por ..."},
                style_table={"marginBottom": "30px", "borderRadius": "10px", "overflow": "hidden", "boxShadow": "0 2px 12px #0002"},
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
                        "padding": "10px",
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
                    dcc.Input(id="new-enser-name", type="text", placeholder="Enser", style={"margin": "5px", "width": "140px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                    dcc.Dropdown(
                        id="new-enser-tipo",
                        options=[
                            {"label": "Diverso", "value": "Diverso"},
                            {"label": "Karcher", "value": "Karcher"},
                            {"label": "Bomba Calor", "value": "Bomba Calor"},
                            {"label": "Cama", "value": "Cama"},
                            {"label": "Mueble", "value": "Mueble"},
                            {"label": "Electrodoméstico", "value": "Electrodoméstico"},
                            {"label": "Estufa", "value": "Estufa"},
                        ],
                        placeholder="Tipo",
                        style={"margin": "5px", "width": "120px", "height": "40px", "borderRadius": "6px"},
                        searchable=True,
                        clearable=True,
                        multi=False,
                        persistence=True,
                        persistence_type="session",
                        disabled=False,
                    ),
                    dcc.Input(id="new-enser-cantidad", type="number", placeholder="Cantidad", min=0, style={"margin": "5px", "width": "100px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                    dcc.Input(id="new-enser-medidas", type="text", placeholder="Medidas", style={"margin": "5px", "width": "120px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
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
                        style={"margin": "5px", "width": "130px", "height": "40px", "borderRadius": "6px"},
                    ),
                    dcc.Input(id="new-enser-donante", type="text", placeholder="Donante", style={"margin": "5px", "width": "120px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                    dcc.Input(id="new-enser-agraciado", type="text", placeholder="Agraciado", style={"margin": "5px", "width": "120px", "height": "40px", "borderRadius": "6px", "border": "1px solid #bdbdbd"}),
                    html.Button(
                        "Añadir Enser",
                        id="add-enser-btn",
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
        ],
        style={"margin": "30px", "background": "#fff", "borderRadius": "12px", "boxShadow": "0 2px 16px #0001", "padding": "20px"}
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
    State("new-enser-tipo", "value"),
    State("enseres-table", "data"),
)
def add_enser(n_clicks, enser, cantidad, medidas, estado, donante, agraciado, tipo, rows):
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
            "tipo": tipo,
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
    State("search-enser-tipo", "value"),
)
def search_enseres_callback(n_clicks, enser, cantidad, medidas, estado, donante, agraciado, tipo):
    if n_clicks > 0:
        enseres_match = search_enseres(enser, cantidad, medidas, estado, donante, agraciado, tipo)
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
                            {"name": "Tipo", "id": "tipo"},
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
