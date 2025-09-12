import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from flask import session

# =====================
#   NAVBAR COMPONENT
# =====================

navlink_style = {
    "fontSize": "22px",
    "fontFamily": "Montserrat, sans-serif",
    "paddingTop": "0px",
    "color": "#0f0f0f",
    "paddingBottom": "0px",
    "marginRight": "20px",
    "border": "none",
    "boxShadow": "none",
    "outline": "none",
}

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                html.Img(
                    src="/assets/images/Vasupply.png",
                    height="40px",
                    style={"marginRight": "30px", "marginLeft": "20px"},
                ),
                href="/",
                className="me-0",
            ),
            dbc.NavbarToggler(
                id="navbar-toggler", n_clicks=0, style={"backgroundColor": "white"}
            ),  # White button
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                "Afectados",
                                href="/afectados",
                                style=navlink_style,
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "Enseres",
                                href="/enseres",
                                style=navlink_style,
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "Admin",
                                href="/admin_usuarios",
                                style=navlink_style,
                            ),
                            id="nav_admin_container",
                            style={"display": "none"},
                        ),
                    ],
                    navbar=True,
                    horizontal="start",
                    style={
                        "marginLeft": "20px",
                        "padding": "0",
                        "width": "100%",
                    },
                    className="w-100",
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
        style={"margin": "0"},
    ),
    color="#f2f2f2",
    dark=False,
    sticky="right",
    style={"minHeight": "40px", "border": "none", "boxShadow": "none"},
    expand="xl",
)


def register_navbar_callbacks(app):
    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(
        [Output("nav_admin_container", "style")],
        Input("url", "pathname"),
    )
    def show_admins_button(pathname):
        user_group = session.get("user_group", None)
        if user_group == "Admin":
            return [{"display": "block"}]
        else:
            return [{"display": "none"}]
