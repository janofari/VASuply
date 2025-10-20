import dash
from dash import Input, Output, State, callback, dcc, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import date
from services.database.sqlite_db_handler import insert_afectado


dash.register_page(__name__, path="/formulario", name="Formulario")


layout = html.Div(
    [
        dbc.Container(
            [
                # Logo superior
                dbc.Row(
                    dbc.Col(
                        html.Img(
                            src="/assets/images/Vasupply.png",
                            height="80px",
                            style={"marginBottom": "10px"},
                        ),
                        width="auto",
                    ),
                    justify="center",
                    className="mb-3",
                ),
                html.H2(
                    "Formulario de Ayuda – Afectados por la DANA",
                    className="text-center my-4",
                ),
                dbc.Form(
                    [
                        # Nombre
                        html.Div(
                            [
                                html.Label(
                                    "Nombre",
                                    htmlFor="nombre",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="nombre",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Apellidos
                        html.Div(
                            [
                                html.Label(
                                    "Apellidos",
                                    htmlFor="apellidos",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="apellidos",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # DNI o NIE
                        html.Div(
                            [
                                html.Label(
                                    "DNI o NIE",
                                    htmlFor="DNI",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="DNI",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Teléfono
                        html.Div(
                            [
                                html.Label(
                                    "Teléfono de contacto",
                                    htmlFor="telefono",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="telefono",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Población
                        html.Div(
                            [
                                html.Label(
                                    "Población",
                                    htmlFor="poblacion",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="poblacion",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Dirección afectada
                        html.Div(
                            [
                                html.Label(
                                    "Dirección",
                                    htmlFor="direccion_afectada",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="direccion_afectada",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Ubicación alternativa
                        html.Div(
                            [
                                html.Label(
                                    "Ubicación alternativa (si te has desplazado)",
                                    htmlFor="ubi",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="ubi",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Situación personal
                        html.Div(
                            [
                                html.Label(
                                    "Situación personal",
                                    htmlFor="situacion_personal",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="situacion_personal",
                                    type="text",
                                    className="form-control",
                                ),
                            ],
                            className="mb-3",
                        ),
                        # Necesidad
                        html.Div(
                            [
                                html.Label(
                                    "¿Qué necesitas o estás buscando?",
                                    htmlFor="necesidad",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Textarea(
                                    id="necesidad",
                                    className="form-control",
                                    placeholder="Escribe aquí tus necesidades...",
                                    style={"height": "150px"},
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Botón de envío
                        html.Div(
                            [
                                html.Button(
                                    "Enviar solicitud",
                                    id="submit",
                                    n_clicks=0,
                                    className="btn",
                                    style={
                                        "backgroundColor": "#2b3d2c",
                                        "color": "white",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            className="d-flex justify-content-center",
                        ),
                        # Mensaje de confirmación
                        html.Div(
                            id="mensaje_confirmacion",
                            className="text-success fw-bold text-center mt-4",
                        ),
                    ]
                ),
            ],
            style={"maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
        )
    ]
)


# CALLBACK ACTUALIZADO
@callback(
    [
        Output("mensaje_confirmacion", "children"),
        Output("submit", "disabled"),
    ],
    Input("submit", "n_clicks"),
    State("nombre", "value"),
    State("apellidos", "value"),
    State("DNI", "value"),
    State("telefono", "value"),
    State("poblacion", "value"),
    State("direccion_afectada", "value"),
    State("ubi", "value"),
    State("situacion_personal", "value"),
    State("necesidad", "value"),
    prevent_initial_call=True,
)
def guardar_solicitud(
    n_clicks,
    nombre,
    apellidos,
    dni,
    telefono,
    poblacion,
    direccion_afectada,
    ubi,
    situacion_personal,
    necesidad,
):
    if not n_clicks:
        raise PreventUpdate

    # Validación de campos obligatorios
    if not (
        nombre
        and apellidos
        and dni
        and telefono
        and poblacion
        and direccion_afectada
        and necesidad
    ):
        return (
            "⚠️ Por favor, completa todos los campos obligatorios: nombre, apellidos, DNI, teléfono, población, dirección afectada y necesidad.",
            False,
        )

    try:
        # Generar campos derivados
        dia_alta = date.today().isoformat()
        afectado = f"{apellidos.strip()}, {nombre.strip()}"

        new_afectado = {
            "afectado": afectado,
            "ubi": ubi.strip() if ubi else None,
            "necesidad": necesidad.strip(),
            "dni": dni.strip(),
            "tlf": int(telefono) if telefono else None,
            "dia_alta": dia_alta,
            "direccion_afectada": direccion_afectada.strip(),
            "poblacion": poblacion.strip(),
            "situacion_personal": (
                situacion_personal.strip() if situacion_personal else None
            ),
            "dia_visita": None,
        }

        insert_afectado(new_afectado)

        return (
            html.Div(
                "✅ Solicitud registrada correctamente. Gracias por comunicarte con nosotros.\nPara volver a enviar el formulario, recarga la página.",
                style={"whiteSpace": "pre-line"},
            ),
            True,
        )

    except Exception as e:
        return (f"❌ Error al guardar los datos: {str(e)}", False)
