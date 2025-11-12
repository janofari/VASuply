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
                html.H1(
                    "Gestión de Afectados",
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
                            id="afectados-table",
                            columns=[
                                {
                                    "name": "Día de alta",
                                    "id": "dia_alta",
                                    "editable": True,
                                },
                                {
                                    "name": "Afectado",
                                    "id": "afectado",
                                    "editable": False,
                                },
                                {"name": "Teléfono", "id": "tlf", "editable": True},
                                {
                                    "name": "Dirección afectada",
                                    "id": "direccion_afectada",
                                    "editable": True,
                                },
                                {
                                    "name": "Ubicación alternativa",
                                    "id": "ubi",
                                    "editable": True,
                                },
                                {
                                    "name": "Población",
                                    "id": "poblacion",
                                    "editable": True,
                                },
                                {
                                    "name": "Situación personal",
                                    "id": "situacion_personal",
                                    "editable": True,
                                },
                                {
                                    "name": "Necesidad",
                                    "id": "necesidad",
                                    "editable": True,
                                },
                                {
                                    "name": "Día de visita",
                                    "id": "dia_visita",
                                    "editable": True,
                                },
                            ],
                            data=fetch_afectados(),
                            row_deletable=True,
                            editable=True,
                            filter_action="native",
                            filter_options={"placeholder_text": "filtrar por ..."},
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
                            },
                            style_cell={
                                "fontFamily": "Montserrat, sans-serif",
                                "fontSize": "clamp(0.8rem, 2vw, 1rem)",
                                "padding": "10px 8px",
                                "minWidth": "120px",
                                "maxWidth": "300px",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "whiteSpace": "normal",
                                "height": "auto",
                                "lineHeight": "1.4",
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
                                dcc.DatePickerSingle(
                                    id="new-afectado-dia-alta",
                                    placeholder="Día de alta",
                                    display_format="DD/MM/YYYY",
                                    style={
                                        "width": "100%",
                                        "minWidth": "150px",
                                    },
                                    month_format="MM/YYYY",
                                    first_day_of_week=1,
                                ),
                            ],
                            style={
                                "flex": "1 1 150px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="new-afectado-name",
                                    type="text",
                                    placeholder="Nombre",
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
                                "flex": "1 1 180px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="new-afectado-tlf",
                                    type="text",
                                    placeholder="Teléfono",
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
                                    id="new-afectado-dni",
                                    type="text",
                                    placeholder="DNI",
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
                                    id="new-afectado-direccion",
                                    type="text",
                                    placeholder="Dirección afectada",
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
                                "flex": "1 1 200px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="new-afectado-ubi",
                                    type="text",
                                    placeholder="Ubicación alternativa",
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
                                "flex": "1 1 180px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="new-afectado-poblacion",
                                    type="text",
                                    placeholder="Población",
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
                                dcc.Input(
                                    id="new-afectado-situacion",
                                    type="text",
                                    placeholder="Situación personal",
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
                                "flex": "1 1 180px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="new-afectado-nec",
                                    type="text",
                                    placeholder="Necesidad",
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
                                "flex": "1 1 180px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    id="new-afectado-dia-visita",
                                    placeholder="Día de visita",
                                    display_format="DD/MM/YYYY",
                                    style={
                                        "width": "100%",
                                        "minWidth": "150px",
                                    },
                                    month_format="MM/YYYY",
                                    first_day_of_week=1,
                                ),
                            ],
                            style={
                                "flex": "1 1 150px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Añadir Afectado",
                                    id="add-afectado-btn",
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
                                "flex": "1 1 180px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "🖨️ Imprimir",
                                    id="export-csv-btn",
                                    n_clicks=0,
                                    style={
                                        "width": "100%",
                                        "padding": "10px 18px",
                                        "backgroundColor": "#1976d2",
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
                                "flex": "1 1 120px",
                                "minWidth": "100px",
                                "marginBottom": "10px",
                            },
                        ),
                        dcc.Download(id="download-csv"),
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
    else:
        return html.Div(
            [
                html.H1(
                    "Búsqueda de Afectados",
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
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="search-criteria-dropdown",
                                    options=[
                                        {"label": "Nombre", "value": "nombre"},
                                        {"label": "DNI", "value": "dni"},
                                        {"label": "Teléfono", "value": "tlf"},
                                    ],
                                    value="nombre",
                                    clearable=False,
                                    style={"width": "100%", "borderRadius": "6px"},
                                ),
                            ],
                            style={
                                "flex": "1 1 150px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="search-afectado-input",
                                    type="text",
                                    placeholder="Buscar...",
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
                                "flex": "1 1 200px",
                                "minWidth": "150px",
                                "marginBottom": "10px",
                            },
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Buscar",
                                    id="search-afectado-btn",
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
                                "flex": "1 1 120px",
                                "minWidth": "100px",
                                "marginBottom": "10px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "gap": "10px",
                        "marginBottom": "20px",
                        "background": "#f7f7f7",
                        "padding": "15px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 12px #0001",
                    },
                ),
                html.Div(id="output-search-afectados"),
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
    Output("afectados-table", "data"),
    Input("add-afectado-btn", "n_clicks"),
    State("new-afectado-name", "value"),
    State("new-afectado-ubi", "value"),
    State("new-afectado-nec", "value"),
    State("new-afectado-dni", "value"),
    State("new-afectado-tlf", "value"),
    State("new-afectado-dia-alta", "date"),
    State("new-afectado-direccion", "value"),
    State("new-afectado-poblacion", "value"),
    State("new-afectado-situacion", "value"),
    State("new-afectado-dia-visita", "date"),
    State("afectados-table", "data"),
)
def add_afectado(
    n_clicks,
    name,
    ubi,
    nec,
    dni,
    tlf,
    dia_alta,
    direccion,
    poblacion,
    situacion,
    dia_visita,
    rows,
):
    from datetime import datetime

    def format_date(date_str):
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                return ""
        return ""

    if n_clicks > 0 and name:
        new_row = {
            "afectado": name,
            "ubi": ubi,
            "necesidad": nec,
            "dni": dni,
            "tlf": tlf,
            "dia_alta": format_date(dia_alta),
            "direccion_afectada": direccion,
            "poblacion": poblacion,
            "situacion_personal": situacion,
            "dia_visita": format_date(dia_visita),
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
                    html.H2(
                        f"Afectado(s) encontrados = {len(afectados_match)}",
                        style={
                            "fontSize": "clamp(1.2rem, 4vw, 1.5rem)",
                            "marginBottom": "15px",
                        },
                    ),
                    html.Div(
                        [
                            dash_table.DataTable(
                                id="afectados-table-search",
                                columns=[
                                    {"name": "Día de alta", "id": "dia_alta"},
                                    {"name": "Afectado", "id": "afectado"},
                                    {"name": "Teléfono", "id": "tlf"},
                                    {
                                        "name": "Dirección afectada",
                                        "id": "direccion_afectada",
                                    },
                                    {"name": "Ubicación alternativa", "id": "ubi"},
                                    {"name": "Población", "id": "poblacion"},
                                    {
                                        "name": "Situación personal",
                                        "id": "situacion_personal",
                                    },
                                    {"name": "Necesidad", "id": "necesidad"},
                                    {"name": "Día de visita", "id": "dia_visita"},
                                ],
                                data=afectados_match,
                                filter_action="native",
                                filter_options={"placeholder_text": "filtrar por ..."},
                                page_size=10,
                                style_table={
                                    "overflowX": "auto",
                                    "width": "100%",
                                },
                                style_header={
                                    "backgroundColor": "#2e7d32",
                                    "color": "white",
                                    "fontWeight": "bold",
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "clamp(0.85rem, 2.5vw, 1.1rem)",
                                    "padding": "12px 8px",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                },
                                style_cell={
                                    "fontFamily": "Montserrat, sans-serif",
                                    "fontSize": "clamp(0.8rem, 2vw, 1rem)",
                                    "padding": "10px 8px",
                                    "minWidth": "120px",
                                    "maxWidth": "300px",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "lineHeight": "1.4",
                                },
                            ),
                        ],
                        style={"overflowX": "auto", "width": "100%"},
                    ),
                ]
            )
        else:
            return html.H2(
                "No se encontraron afectados coincidentes",
                style={"fontSize": "clamp(1.2rem, 4vw, 1.5rem)"},
            )


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


@callback(
    Output("download-csv", "data"),
    Input("export-csv-btn", "n_clicks"),
    State("afectados-table", "data"),
    State("afectados-table", "derived_virtual_data"),
    prevent_initial_call=True,
)
def export_to_csv(n_clicks, data, filtered_data):
    if n_clicks > 0:
        import pandas as pd
        from datetime import datetime

        data_to_export = filtered_data if filtered_data else data

        if data_to_export:
            df = pd.DataFrame(data_to_export)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            return dcc.send_data_frame(
                df.to_csv, f"afectados_{timestamp}.csv", index=False
            )
