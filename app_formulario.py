import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

from services.database.sqlite_db_handler import insert_afectado
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Formulario de Ayuda – DANA"

# LAYOUT PAGINA FORMULARIO
app.layout = html.Div(
    [
        dbc.Container(
            [
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
                        html.Div(
                            [
                                html.Label(
                                    "Nombre completo",
                                    htmlFor="afectado",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="afectado",
                                    type="text",
                                    className="form-control",
                                    placeholder="Ej. Juan Pérez",
                                ),
                            ],
                            className="mb-3",
                        ),
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
                                    placeholder="Ej. 12345678A",
                                ),
                            ],
                            className="mb-3",
                        ),
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
                                    placeholder="Ej. 600123456",
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Ubicación",
                                    htmlFor="ubicacion",
                                    style={"fontWeight": "bold", "fontSize": "1.1em"},
                                ),
                                dcc.Input(
                                    id="ubicacion",
                                    type="text",
                                    className="form-control",
                                    placeholder="Ej. Orihuela, barrio San Antón",
                                ),
                            ],
                            className="mb-3",
                        ),
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
                        html.Div(
                            [
                                html.Button(
                                    "Enviar solicitud",
                                    id="submit",
                                    n_clicks=0,
                                    className="btn",
                                    style={
                                        "backgroundColor": "#2b3d2c",  # verde clarito
                                        "color": "white",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            className="d-flex justify-content-center",
                        ),
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

# Comprobado que una vez que el registro haya sido satisfactorio, no se pueda volver a enviar
# Callback para guardar en la base de datos
@app.callback(
    [
        Output("mensaje_confirmacion", "children"),
        Output("submit", "disabled"),  
    ],
    Input("submit", "n_clicks"),
    State("afectado", "value"),
    State("DNI", "value"),
    State("telefono", "value"),
    State("ubicacion", "value"),
    State("necesidad", "value"),
    prevent_initial_call=True,  
)
def guardar_solicitud(n_clicks, afectado, dni, telefono, ubicacion, necesidad):
    if not n_clicks:
        raise PreventUpdate

    # Validación de campos obligatorios
    if not afectado or not dni or not telefono or not necesidad:
        return (
            "⚠️ Por favor, completa al menos nombre, DNI, teléfono y necesidad.",
            False,
        )

    try:
        new_afectado = {
            "afectado": afectado.strip(),
            "ubi": ubicacion.strip() if ubicacion else None,
            "necesidad": necesidad.strip(),
            "dni": dni.strip(),
            "tlf": int(telefono) if telefono else None,
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


if __name__ == "__main__":
    app.run(debug=True, port=8055)
