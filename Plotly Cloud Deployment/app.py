import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date

# ── Synthetic Data ────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)

COUNTRIES = [
    ("United States", "USA"),
    ("United Kingdom", "GBR"),
    ("Germany",        "DEU"),
    ("France",         "FRA"),
    ("Australia",      "AUS"),
    ("Canada",         "CAN"),
    ("Japan",          "JPN"),
    ("Brazil",         "BRA"),
    ("India",          "IND"),
    ("Spain",          "ESP"),
]
STATUSES = ["Shipped", "Processing", "Cancelled", "On Hold"]
N = 1_024

dates   = pd.date_range("2003-01-01", "2005-03-31", freq="D")
c_idx   = rng.choice(len(COUNTRIES), size=N, p=[.35,.12,.10,.09,.08,.07,.06,.05,.04,.04])
s_idx   = rng.choice(len(STATUSES),  size=N, p=[.70,.20,.05,.05])

df = pd.DataFrame({
    "order_date":   rng.choice(dates, size=N),
    "country":      [COUNTRIES[i][0] for i in c_idx],
    "country_code": [COUNTRIES[i][1] for i in c_idx],
    "status":       [STATUSES[i]     for i in s_idx],
    "quantity":     rng.integers(1, 50, N),
    "unit_price":   rng.uniform(100, 500, N).round(2),
})
df["sales"]      = (df["quantity"] * df["unit_price"]).round(2)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values("order_date").reset_index(drop=True)

ALL_COUNTRIES = ["All countries"] + sorted(df["country"].unique())
ALL_STATUSES  = ["All statuses"]  + sorted(df["status"].unique())
MIN_DATE, MAX_DATE = date(2003, 1, 1), date(2005, 3, 31)

df.head()


# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server   # ← Required for Plotly Cloud / Gunicorn

# ── Layout helpers ────────────────────────────────────────────────────────────
def _fmt_currency(v: float) -> str:
    if v >= 1_000_000: return f"${v/1_000_000:.1f}M"
    if v >= 1_000:     return f"${v/1_000:.1f}K"
    return f"${v:,.0f}"

CARD_STYLE = {"border": "none", "borderRadius": "12px", "boxShadow": "0 2px 8px rgba(0,0,0,.08)"}

def metric_card(icon: str, label: str, value: str, sub: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Span(label, className="text-muted small fw-semibold text-uppercase"),
                html.Span(icon, style={"fontSize": "1.1rem", "opacity": ".6", "float": "right"}),
            ]),
            html.H3(value, className="fw-bold mt-2 mb-0", style={"fontSize": "1.8rem"}),
            html.Small(sub, className="text-muted"),
        ]),
        style=CARD_STYLE,
        className="h-100",
    )

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = dbc.Container(
    [
        # ── Header ──────────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                html.H4("📊 Sales Dashboard", className="fw-bold mb-0 py-3"),
            ),
            className="border-bottom mb-3",
        ),

        # ── Filters ─────────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    dcc.DatePickerRange(
                        id="date-range",
                        min_date_allowed=MIN_DATE,
                        max_date_allowed=MAX_DATE,
                        start_date=MIN_DATE,
                        end_date=MAX_DATE,
                        display_format="MMM D, YYYY",
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        ALL_STATUSES, "All statuses", id="status-filter",
                        clearable=False, style={"minWidth": "160px"},
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        ALL_COUNTRIES, "All countries", id="country-filter",
                        clearable=False, style={"minWidth": "180px"},
                    ),
                    width="auto",
                ),
            ],
            align="center", className="mb-3 g-2",
        ),

        # ── KPI Cards ────────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(html.Div(id="card-sales"),  md=3, xs=6, className="mb-3"),
                dbc.Col(html.Div(id="card-orders"), md=3, xs=6, className="mb-3"),
                dbc.Col(html.Div(id="card-qty"),    md=3, xs=6, className="mb-3"),
                dbc.Col(html.Div(id="card-avg"),    md=3, xs=6, className="mb-3"),
            ],
            className="g-3",
        ),

        # ── Charts ───────────────────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Sales map", className="fw-semibold bg-white border-0 pt-3 pb-0"),
                            dbc.CardBody(dcc.Graph(id="map-chart", config={"displayModeBar": False}, style={"height": "360px"})),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=5, xs=12, className="mb-3",
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Sales per day", className="fw-semibold bg-white border-0 pt-3 pb-0"),
                            dbc.CardBody(dcc.Graph(id="bar-chart", config={"displayModeBar": False}, style={"height": "360px"})),
                        ],
                        style=CARD_STYLE,
                    ),
                    md=7, xs=12, className="mb-3",
                ),
            ],
            className="g-3",
        ),



    ],
    fluid=True,
    className="bg-light min-vh-100 px-4",
)

# ── Callbacks ─────────────────────────────────────────────────────────────────
@callback(
    Output("card-sales",  "children"),
    Output("card-orders", "children"),
    Output("card-qty",    "children"),
    Output("card-avg",    "children"),
    Output("map-chart",   "figure"),
    Output("bar-chart",   "figure"),
    Input("date-range",    "start_date"),
    Input("date-range",    "end_date"),
    Input("status-filter", "value"),
    Input("country-filter","value"),
)
def update_dashboard(start, end, status, country):
    dff = df.copy()

    if start:
        dff = dff[dff["order_date"] >= pd.to_datetime(start)]
    if end:
        dff = dff[dff["order_date"] <= pd.to_datetime(end)]
    if status and status != "All statuses":
        dff = dff[dff["status"] == status]
    if country and country != "All countries":
        dff = dff[dff["country"] == country]

    # ── KPI values ──────────────────────────────────────────────────────────
    total_sales = dff["sales"].sum()
    n_orders    = len(dff)
    total_qty   = dff["quantity"].sum()
    avg_sale    = dff["sales"].mean() if n_orders else 0.0

    date_span = max(
        (dff["order_date"].max() - dff["order_date"].min()).days, 1
    ) if n_orders else 1

    cards = [
        metric_card("$",  "Sales",    _fmt_currency(total_sales),
                    f"{_fmt_currency(total_sales / date_span)} per day"),
        metric_card("🛒", "Orders",   f"{n_orders:,}",
                    f"{n_orders / date_span:.2f} per day"),
        metric_card("#",  "Quantity", f"{total_qty / 1_000:.1f}K",
                    f"{total_qty / date_span:.0f} per day"),
        metric_card("↑",  "Avg. sale", _fmt_currency(avg_sale),
                    "per order"),
    ]

    # ── Choropleth map ───────────────────────────────────────────────────────
    map_df = (
        dff.groupby(["country", "country_code"], as_index=False)["sales"].sum()
    )
    fig_map = px.choropleth(
        map_df,
        locations="country_code",
        color="sales",
        hover_name="country",
        color_continuous_scale=[[0, "#d0e8f7"], [1, "#0d3d6b"]],
        labels={"sales": "Sales ($)"},
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Sales ($)", tickformat="$,.0f", len=0.6),
        geo=dict(showframe=False, showcoastlines=True, bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # ── Monthly bar chart ────────────────────────────────────────────────────
    dff2 = dff.copy()
    dff2["month"] = dff2["order_date"].dt.to_period("M").dt.to_timestamp()
    bar_df = dff2.groupby("month", as_index=False)["sales"].sum()

    fig_bar = px.bar(
        bar_df, x="month", y="sales",
        labels={"month": "Date", "sales": "Total Sales ($)"},
        color_discrete_sequence=["#3a7fbf"],
    )
    fig_bar.update_layout(
        margin=dict(l=40, r=10, t=10, b=40),
        xaxis=dict(tickformat="%b %Y", showgrid=False),
        yaxis=dict(tickformat="$,.0f", gridcolor="#e9ecef"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        bargap=0.15,
    )

    return *cards, fig_map, fig_bar


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=True)
