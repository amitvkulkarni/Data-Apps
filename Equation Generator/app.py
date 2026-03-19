"""
Latexify App — Main entry point
Spec reference: specs/app.spec.md
"""

from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html, no_update

from utils.latex_engine import convert_to_latex

# ── Example snippets (spec § 6) ──────────────────────────────────────────────
EXAMPLES = [
    {
        "label": "Quadratic",
        "preview": "x² + 2x + 1",
        "code": "def quadratic(x):\n    return x**2 + 2*x + 1",
    },
    {
        "label": "Cubic",
        "preview": "x³ − 3x² + 3x − 1",
        "code": "def cubic(x):\n    return x**3 - 3*x**2 + 3*x - 1",
    },
    {
        "label": "Trigonometric",
        "preview": "sin²(x) + cos²(x)",
        "code": "import math\n\ndef trig(x):\n    return math.sin(x)**2 + math.cos(x)**2",
    },
    {
        "label": "Gaussian",
        "preview": "e^(−x²/2) / √(2π)",
        "code": "import math\n\ndef gaussian(x):\n    return math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)",
    },
    {
        "label": "Pythagorean",
        "preview": "√(a² + b²)",
        "code": "import math\n\ndef pythagorean(a, b):\n    return math.sqrt(a**2 + b**2)",
    },
]

PLACEHOLDER = (
    "Write your Python function here, e.g.:\n\ndef f(x):\n    return x**2 + 2*x + 1"
)

# ── MathJax external script ───────────────────────────────────────────────────
MATHJAX_CDN = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"


# ── Layout ───────────────────────────────────────────────────────────────────
def create_layout() -> dbc.Container:
    # Dynamic Bootstrap theme stylesheet — href is swapped by switch_theme callback (FR-7)
    theme_link = html.Link(
        id="theme-link",
        rel="stylesheet",
        href=dbc.themes.BOOTSTRAP,
    )

    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Equation Generator", className="navbar__brand"),
                html.Span(
                    [
                        html.I(className="bi bi-sun-fill text-warning me-1"),
                        dbc.Switch(
                            id="toggle-theme",
                            value=False,
                            className="mb-0 mx-1",
                            persistence=True,
                            persistence_type="session",
                        ),
                        html.I(className="bi bi-moon-fill text-light ms-1"),
                    ],
                    className="ms-auto d-flex align-items-center",
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-0",
    )

    sidebar = html.Div(
        [
            html.P("Examples", className="sidebar__title"),
            *[
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(ex["label"], className="example-card__label"),
                                html.Div(
                                    ex["preview"], className="example-card__snippet"
                                ),
                            ],
                            className="py-2 px-3",
                        ),
                        className="example-card",
                    ),
                    id={"type": "example-card", "index": i},
                    n_clicks=0,
                    style={"cursor": "pointer"},
                )
                for i, ex in enumerate(EXAMPLES)
            ],
        ],
        className="sidebar",
    )

    input_panel = html.Div(
        [
            html.P("Python Function", className="input-panel__label"),
            dcc.Textarea(
                id="input-source",
                placeholder=PLACEHOLDER,
                value="",
                rows=7,
                className="form-control input-panel__textarea w-100",
            ),
            html.Div(
                [
                    dbc.Button(
                        "Generate LaTeX",
                        id="btn-generate",
                        color="primary",
                        className="me-2 mt-3 btn-generate",
                    ),
                    dbc.Button(
                        "Clear",
                        id="btn-clear",
                        color="secondary",
                        outline=True,
                        className="mt-3",
                    ),
                ]
            ),
        ],
        className="input-panel",
    )

    output_panel = html.Div(
        [
            html.P("Rendered Equation", className="output-panel__label"),
            html.Div(
                id="output-rendered",
                children=html.Span(
                    "Your equation will appear here",
                    className="output-panel__equation--empty",
                ),
                className="output-panel__equation",
            ),
            html.P("LaTeX Source", className="output-panel__label mt-3"),
            dcc.Textarea(
                id="output-latex-source",
                value="",
                readOnly=True,
                rows=3,
                className="form-control output-panel__raw-textarea w-100",
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Clipboard(
                        target_id="output-latex-source",
                        title="Copy LaTeX to clipboard",
                        id="btn-copy",
                        className="mt-2 btn btn-sm btn-outline-secondary",
                        style={
                            "display": "inline-flex",
                            "alignItems": "center",
                            "gap": "4px",
                        },
                    )
                ),
            ),
        ],
        className="output-panel",
    )

    error_area = dbc.Alert(
        id="error-alert",
        color="danger",
        is_open=False,
        dismissable=True,
        className="error-alert",
    )

    main_content = html.Div(
        [input_panel, output_panel, error_area],
        className="main-content",
    )

    body = dbc.Row(
        [
            dbc.Col(sidebar, xs=12, md=3, className="p-0"),
            dbc.Col(main_content, xs=12, md=9),
        ],
        className="g-0",
    )

    return dbc.Container(
        [
            theme_link,
            html.Div(id="app-shell", children=[navbar, body]),
        ],
        fluid=True,
        className="p-0",
    )


# ── App initialisation ────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        # Bootstrap theme is loaded dynamically via html.Link(id="theme-link")
        # so it can be swapped at runtime without a page reload (FR-7)
        dbc.icons.BOOTSTRAP,
    ],
    external_scripts=[
        {"src": MATHJAX_CDN, "id": "MathJax-script", "async": True},
    ],
    title="Latexify — Math Equation Generator",
)

app.layout = create_layout()


# ── Callbacks ─────────────────────────────────────────────────────────────────


# FR-3: clicking an example card populates the input textarea
@callback(
    Output("input-source", "value"),
    Input({"type": "example-card", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def load_example(n_clicks_list):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    triggered_id = ctx.triggered[0]["prop_id"]
    # extract index from pattern-match id like {"index":2,"type":"example-card"}.n_clicks
    import json, re

    match = re.search(r'"index"\s*:\s*(\d+)', triggered_id)
    if not match:
        return no_update
    idx = int(match.group(1))
    return EXAMPLES[idx]["code"]


# FR-1 (Clear) + FR-2 (Generate)
@callback(
    Output("output-rendered", "children"),
    Output("output-latex-source", "value"),
    Output("error-alert", "children"),
    Output("error-alert", "is_open"),
    Output("input-source", "value", allow_duplicate=True),
    Input("btn-generate", "n_clicks"),
    Input("btn-clear", "n_clicks"),
    State("input-source", "value"),
    prevent_initial_call=True,
)
def handle_generate_clear(gen_clicks, clear_clicks, source):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"] if ctx.triggered else ""

    empty_rendered = html.Span(
        "Your equation will appear here",
        className="output-panel__equation--empty",
    )

    if "btn-clear" in triggered:
        return empty_rendered, "", "", False, ""

    # Generate path
    result = convert_to_latex(source or "")

    if result["error"]:
        return empty_rendered, "", result["error"], True, no_update

    latex_str = result["latex"]
    # Wrap in $$ for MathJax block rendering
    rendered = dcc.Markdown(
        f"$$\n{latex_str}\n$$",
        mathjax=True,
        style={"margin": 0},
    )
    return rendered, latex_str, "", False, no_update


# FR-7: Dark / Light mode toggle
@callback(
    Output("theme-link", "href"),
    Output("app-shell", "className"),
    Input("toggle-theme", "value"),
    prevent_initial_call=True,
)
def switch_theme(dark_mode):
    if dark_mode:
        return dbc.themes.DARKLY, "dark-mode"
    return dbc.themes.BOOTSTRAP, ""


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
