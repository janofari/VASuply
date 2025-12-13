import dash
from dash import Input, Output, State, callback, dash_table, dcc, html
from flask import session
from dash.exceptions import PreventUpdate
import unicodedata
import pandas as pd
from datetime import datetime
from services.database.sqlite_db_handler import (
    fetch_afectados,
    insert_afectado,
    search_afectados,
    update_afectado,
    delete_afectado,
)
from pages.components import navbar, register_navbar_callbacks


def remove_accents(text: str) -> str:
    replace_characters = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
    }
    return "".join(replace_characters.get(c, c) for c in text)


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
                        "fontSize": "clamp(1.2rem, 4vw, 1.68rem)",
                        "color": "#2e7d32",
                        "marginBottom": "18px",
                        "letterSpacing": "1px",
                    },
                ),
                html.Div(
                    [
                        # Popup de confirmación
                        dcc.ConfirmDialog(
                            id="afectados-delete-confirm",
                            message=(
                                "¿Seguro que quieres eliminar a este afectado o afectados? "
                                "Esta acción NO se puede deshacer."
                            ),
                        ),
                        # Botón de borrado
                        html.Button(
                            "🗑️ Eliminar afectados seleccionados",
                            id="afectados-delete-button",
                            n_clicks=0,
                            style={
                                "marginBottom": "10px",
                                "backgroundColor": "#c62828",
                                "color": "white",
                                "border": "none",
                                "padding": "8px 16px",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontFamily": "Montserrat, sans-serif",
                                "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
                            },
                        ),
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
                                    "editable": True,
                                },
                                {"name": "Teléfono", "id": "tlf", "editable": True},
                                {
                                    "name": "Email",
                                    "id": "email",
                                    "editable": True,
                                },
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
                                    "name": "Personas a cargo",
                                    "id": "personas_a_cargo",
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
                                {
                                    "name": "Baja",
                                    "id": "baja",
                                    "type": "numeric",
                                    "editable": True,
                                },
                            ],
                            data=fetch_afectados(),
                            editable=True,
                            row_selectable="multi",
                            selected_rows=[],
                            filter_action="native",
                            filter_options={
                                "placeholder_text": "filtrar por ...",
                                "case": "insensitive",
                                "normalize": True,
                            },
                            sort_action="native",
                            sort_mode="single",
                            sort_by=[{"column_id": "dia_alta", "direction": "desc"}],
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
                                "fontSize": "clamp(0.68rem, 2vw, 0.88rem)",
                                "border": "none",
                                "padding": "12px 8px",
                                "whiteSpace": "normal",
                                "height": "auto",
                                "textAlign": "left",
                            },
                            style_cell={
                                "fontFamily": "Montserrat, sans-serif",
                                "fontSize": "clamp(0.64rem, 1.6vw, 0.8rem)",
                                "padding": "10px 8px",
                                "minWidth": "120px",
                                "maxWidth": "300px",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "whiteSpace": "normal",
                                "height": "auto",
                                "lineHeight": "1.4",
                                "textAlign": "left",
                            },
                            style_cell_conditional=[
                                # Día de alta
                                {
                                    "if": {"column_id": "dia_alta"},
                                    "minWidth": "120px",
                                    "width": "120px",
                                    "maxWidth": "120px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                # Teléfono
                                {
                                    "if": {"column_id": "tlf"},
                                    "minWidth": "110px",
                                    "width": "110px",
                                    "maxWidth": "110px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                # Día de visita
                                {
                                    "if": {"column_id": "dia_visita"},
                                    "minWidth": "120px",
                                    "width": "120px",
                                    "maxWidth": "120px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                # Población
                                {
                                    "if": {"column_id": "poblacion"},
                                    "minWidth": "120px",
                                    "width": "120px",
                                    "maxWidth": "120px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                # Baja
                                {
                                    "if": {"column_id": "baja"},
                                    "minWidth": "80px",
                                    "width": "80px",
                                    "maxWidth": "80px",
                                    "textAlign": "center",
                                    "whiteSpace": "nowrap",
                                },
                            ],
                            style_data_conditional=[
                                {
                                    "if": {"state": "selected"},
                                    "backgroundColor": "#f2f7fa",
                                    "border": "1px solid #1976d2",
                                },
                                {
                                    "if": {"state": "selected"},
                                    "backgroundColor": "#f2f7fa",
                                    "border": "1px solid #1976d2",
                                },
                                {
                                    "if": {"filter_query": "{baja} = 1"},
                                    "backgroundColor": "#eeeeee",
                                    "color": "#757575",
                                },
                            ],
                            css=[
                                {
                                    "selector": ".dash-table-container .Select-menu-outer",
                                    "rule": "display: block !important; position: fixed !important; z-index: 9999;",
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
                                    display_format="YYYY-MM-DD",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                    display_format="YYYY-MM-DD",
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
                                    id="new-afectado-personas-cargo",
                                    type="text",
                                    placeholder="Personas a cargo",
                                    style={
                                        "width": "100%",
                                        "height": "40px",
                                        "borderRadius": "6px",
                                        "border": "1px solid #bdbdbd",
                                        "padding": "0 10px",
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                    id="new-afectado-email",
                                    type="email",
                                    placeholder="Email",
                                    style={
                                        "width": "100%",
                                        "height": "40px",
                                        "borderRadius": "6px",
                                        "border": "1px solid #bdbdbd",
                                        "padding": "0 10px",
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.72rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.72rem, 1.6vw, 0.8rem)",
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
                        "fontSize": "clamp(1.2rem, 4vw, 1.68rem)",
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
                                        "fontSize": "clamp(0.68rem, 1.6vw, 0.8rem)",
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
                                        "fontSize": "clamp(0.72rem, 1.6vw, 0.8rem)",
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
    Output("afectados-delete-confirm", "displayed"),
    Input("afectados-delete-button", "n_clicks"),
    State("afectados-table", "selected_rows"),
    prevent_initial_call=True,
)
def show_delete_confirm(n_clicks, selected_rows):
    if not n_clicks:
        raise PreventUpdate

    # Si no hay filas seleccionadas, no mostramos el popup
    if not selected_rows:
        return False

    # Hay al menos una fila seleccionada -> mostrar popup
    return True


@callback(
    Output("afectados-table", "data"),
    Output("afectados-table", "selected_rows"),
    Input("add-afectado-btn", "n_clicks"),
    Input("afectados-delete-confirm", "submit_n_clicks"),
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
    State("new-afectado-personas-cargo", "value"),
    State("new-afectado-email", "value"),
    State("afectados-table", "data"),
    State("afectados-table", "selected_rows"),
    State("afectados-table", "derived_virtual_data"),
    State("afectados-table", "derived_virtual_selected_rows"),
)
def add_or_delete_afectado(
    add_clicks,
    delete_confirm_clicks,
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
    personas_a_cargo,
    email,
    rows,
    selected_rows,
    virtual_rows,
    virtual_selected_rows,
):

    if rows is None:
        rows = []

    ctx = dash.callback_context
    if not ctx.triggered:
        return rows, selected_rows

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # 1) Alta de afectado
    if triggered_id == "add-afectado-btn":
        if add_clicks and name:
            new_row = {
                "afectado": remove_accents(name),
                "ubi": remove_accents(ubi) if ubi else None,
                "necesidad": nec,
                "dni": dni,
                "tlf": tlf,
                "dia_alta": dia_alta,  # Guardar en formato ISO (YYYY-MM-DD)
                "direccion_afectada": remove_accents(direccion) if direccion else None,
                "poblacion": remove_accents(poblacion) if poblacion else None,
                "situacion_personal": situacion,
                "dia_visita": dia_visita,  # Guardar en formato ISO (YYYY-MM-DD)
                "personas_a_cargo": personas_a_cargo,
                "email": email,
                # NUEVO: siempre entra como no de baja (0)
                "baja": 0,
            }
            insert_afectado(new_row)
            # Recargamos desde BD para traer id, baja, etc. coherentes
            return fetch_afectados(), []
        return rows, selected_rows

    # 2) Borrado de afectados seleccionados (tras confirmar)
    if triggered_id == "afectados-delete-confirm":
        if not delete_confirm_clicks:
            return rows, selected_rows

        # Usar siempre los índices sobre derived_virtual_data,
        # que son los correctos cuando hay sorting/filters
        if not virtual_selected_rows:
            return rows, selected_rows

        data_for_indices = virtual_rows if virtual_rows is not None else rows

        ids_to_delete: list[int] = []
        for idx in virtual_selected_rows:
            if 0 <= idx < len(data_for_indices):
                rid = data_for_indices[idx].get("id")
                if rid is not None:
                    ids_to_delete.append(rid)

        if not ids_to_delete:
            return rows, selected_rows

        # Borrado en BD
        for afectado_id in ids_to_delete:
            delete_afectado(afectado_id)

        # Recargar desde BD tras borrar y resetear selected_rows
        return fetch_afectados(), []

    return rows, selected_rows


def normalize_text(text):
    if not text:
        return ""
    # Convertir a minúsculas y normalizar caracteres
    return "".join(
        c
        for c in unicodedata.normalize("NFKD", str(text).lower())
        if not unicodedata.combining(c)
    )


@callback(
    Output("output-search-afectados", "children"),
    Input("search-afectado-btn", "n_clicks"),
    State("search-criteria-dropdown", "value"),
    State("search-afectado-input", "value"),
)
def search_afectados_callback(n_clicks, criterio, valor):
    if n_clicks > 0 and valor:
        # Normalizar el valor de búsqueda
        valor_normalizado = normalize_text(valor)

        # Obtener todos los afectados según el criterio
        if criterio == "nombre":
            afectados = search_afectados(name="")  # Traer todos para filtrar localmente
            afectados_match = [
                afectado
                for afectado in afectados
                if valor_normalizado in normalize_text(afectado["afectado"])
            ]
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
                                    {"name": "Email", "id": "email"},
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
                                    {
                                        "name": "Personas a cargo",
                                        "id": "personas_a_cargo",
                                    },
                                    {"name": "Necesidad", "id": "necesidad"},
                                    {"name": "Día de visita", "id": "dia_visita"},
                                ],
                                data=afectados_match,
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
                                    "textAlign": "left",
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
                                    "textAlign": "left",
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
        data_to_export = filtered_data if filtered_data else data

        if data_to_export:
            df = pd.DataFrame(data_to_export)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            return dcc.send_data_frame(
                df.to_csv, f"afectados_{timestamp}.csv", index=False
            )
