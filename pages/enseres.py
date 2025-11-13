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
            html.H1(
                "Gestión de Enseres",
                style={
                    "fontFamily": "Montserrat, sans-serif",
                    "fontWeight": "700",
                    "fontSize": "clamp(1.5rem, 5vw, 2.1rem)",
                    "color": "#2e7d32",
                    "marginBottom": "18px",
                    "letterSpacing": "1px",
                },
            ),
            html.Div(
                [
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
                        filter_options={
                            "placeholder_text": "filtrar por ...",
                            "case": "insensitive",
                            "normalize": True,
                        },
                        sort_action="native",
                        sort_mode="single",
                        page_size=10,
                        style_table={
                            "marginBottom": "20px",
                            "borderRadius": "10px",
                            "overflowX": "auto",
                            "boxShadow": "0 2px 12px #0002",
                        },
                        style_header={
                            "backgroundColor": "#2e7d32",
                            "color": "white",
                            "fontWeight": "bold",
                            "fontFamily": "Montserrat, sans-serif",
                            "fontSize": "clamp(0.85rem, 2.5vw, 1.1rem)",
                            "border": "none",
                            "padding": "12px 8px",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "textAlign": "left",
                        },
                        style_cell={
                            "fontFamily": "Montserrat, sans-serif",
                            "fontSize": "clamp(0.8rem, 2vw, 1rem)",
                            "padding": "10px 8px",
                            "minWidth": "120px",
                            "maxWidth": "220px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "lineHeight": "1.4",
                            "textAlign": "left",
                        },
                        style_data_conditional=[
                            {
                                "if": {"state": "selected"},
                                "backgroundColor": "#f2f7fa",
                                "border": "1px solid #1976d2",
                            }
                        ],
                        style_as_list_view=True,
                    ),
                ],
                style={"overflowX": "auto", "width": "100%"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Input(
                                id="new-enser-name",
                                type="text",
                                placeholder="Enser",
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "borderRadius": "6px",
                                    "border": "1px solid #bdbdbd",
                                    "padding": "0 10px",
                                    "fontSize": "clamp(0.85rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 140px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="new-enser-tipo",
                                options=[
                                    {"label": "Diverso", "value": "Diverso"},
                                    {"label": "Karcher", "value": "Karcher"},
                                    {"label": "Bomba Calor", "value": "Bomba Calor"},
                                    {"label": "Cama", "value": "Cama"},
                                    {"label": "Mueble", "value": "Mueble"},
                                    {
                                        "label": "Electrodoméstico",
                                        "value": "Electrodoméstico",
                                    },
                                    {"label": "Estufa", "value": "Estufa"},
                                ],
                                placeholder="Tipo",
                                style={"width": "100%", "borderRadius": "6px"},
                                searchable=True,
                                clearable=True,
                                multi=False,
                                persistence=True,
                                persistence_type="session",
                                disabled=False,
                            ),
                        ],
                        style={
                            "flex": "1 1 120px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Input(
                                id="new-enser-cantidad",
                                type="number",
                                placeholder="Cantidad",
                                min=0,
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "borderRadius": "6px",
                                    "border": "1px solid #bdbdbd",
                                    "padding": "0 10px",
                                    "fontSize": "clamp(0.85rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 100px",
                            "minWidth": "100px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Input(
                                id="new-enser-medidas",
                                type="text",
                                placeholder="Medidas",
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "borderRadius": "6px",
                                    "border": "1px solid #bdbdbd",
                                    "padding": "0 10px",
                                    "fontSize": "clamp(0.85rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 120px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
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
                                style={"width": "100%", "borderRadius": "6px"},
                            ),
                        ],
                        style={
                            "flex": "1 1 130px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Input(
                                id="new-enser-donante",
                                type="text",
                                placeholder="Donante",
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "borderRadius": "6px",
                                    "border": "1px solid #bdbdbd",
                                    "padding": "0 10px",
                                    "fontSize": "clamp(0.85rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 120px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            dcc.Input(
                                id="new-enser-agraciado",
                                type="text",
                                placeholder="Agraciado",
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "borderRadius": "6px",
                                    "border": "1px solid #bdbdbd",
                                    "padding": "0 10px",
                                    "fontSize": "clamp(0.85rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 120px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                    html.Div(
                        [
                            html.Button(
                                "Añadir Enser",
                                id="add-enser-btn",
                                n_clicks=0,
                                style={
                                    "width": "100%",
                                    "padding": "10px 18px",
                                    "backgroundColor": "#2e7d32",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "6px",
                                    "fontWeight": "bold",
                                    "cursor": "pointer",
                                    "height": "44px",
                                    "boxShadow": "0 2px 8px #1976d233",
                                    "fontSize": "clamp(0.9rem, 2vw, 1rem)",
                                },
                            ),
                        ],
                        style={
                            "flex": "1 1 140px",
                            "minWidth": "120px",
                            "marginBottom": "10px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "10px",
                    "marginBottom": "25px",
                    "background": "#f7f7f7",
                    "padding": "15px",
                    "borderRadius": "10px",
                    "boxShadow": "0 2px 12px #0001",
                },
            ),
        ],
        style={
            "margin": "15px",
            "background": "#fff",
            "borderRadius": "12px",
            "boxShadow": "0 2px 16px #0001",
            "padding": "clamp(15px, 3vw, 20px)",
        },
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
    ):
        new_row = {
            "enser": enser,
            "cantidad": cantidad if cantidad is not None else 1,
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
                        page_size=10,
                        style_table={"tableLayout": "fixed", "width": "100%", "overflow": "auto"},
                        style_cell={
                            "fontFamily": "Montserrat, sans-serif",
                            "fontSize": "1rem",
                            "padding": "6px",
                            "maxWidth": "220px",
                            "overflow": "visible",
                            "textOverflow": "clip",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "lineHeight": "18px",
                        },
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
