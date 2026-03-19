import math
import numpy as np
import dash
from dash import dcc, html, Input, Output, ClientsideFunction
import plotly.graph_objects as go

# ── Reproducible seed ─────────────────────────────────────────────────────────
np.random.seed(42)

# ── Colour tokens (mirrored in assets/clientside.js) ─────────────────────────
COLOR_A = "#6c63ff"  # purple-blue
COLOR_B = "#ff6584"  # pink
COLOR_C = "#43b89c"  # teal
PLOT_BG = "#1a1d27"
GRID_COL = "#2d2f45"
TEXT_COL = "#e0e0e0"

# ═════════════════════════════════════════════════════════════════════════════
#  DATASETS
# ═════════════════════════════════════════════════════════════════════════════

# Example 1 — Grouped Bar Chart: monthly sales for two products
BAR_DATA = dict(
    categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    series_a=[45, 62, 38, 71, 55, 83],
    series_b=[30, 45, 52, 43, 67, 58],
    label_a="Product A",
    label_b="Product B",
)

# Example 2 — Multi-Line Chart: average monthly temperature (°C)
LINE_DATA = dict(
    months=[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
    city_a=[2, 4, 9, 15, 20, 25, 27, 26, 21, 14, 7, 3],
    city_b=[18, 19, 22, 26, 30, 33, 35, 34, 30, 25, 20, 17],
    label_a="New York",
    label_b="Miami",
)

# Example 3 — Scatter Plot: three labelled groups with variable point sizes
_n = 60
_x = np.random.randn(_n)
_y = _x * 1.5 + np.random.randn(_n) * 0.8
SCATTER_DATA = dict(
    x=_x.tolist(),
    y=_y.tolist(),
    size=np.random.randint(6, 18, _n).tolist(),
    group=(["Group A"] * 20 + ["Group B"] * 20 + ["Group C"] * 20),
)

# Example 4 — Force-Directed Network Graph: 8 nodes, 12 edges, 3 groups
# Pre-compute a circular starting layout for Plotly; D3 will use physics.
_net_nodes = [
    {"id": 0, "label": "Hub A", "group": 0},
    {"id": 1, "label": "Node B", "group": 0},
    {"id": 2, "label": "Node C", "group": 1},
    {"id": 3, "label": "Node D", "group": 1},
    {"id": 4, "label": "Node E", "group": 2},
    {"id": 5, "label": "Node F", "group": 2},
    {"id": 6, "label": "Node G", "group": 0},
    {"id": 7, "label": "Node H", "group": 1},
]
for _i, _nd in enumerate(_net_nodes):
    _angle = 2 * math.pi * _i / len(_net_nodes)
    _nd["x"] = round(math.cos(_angle), 4)
    _nd["y"] = round(math.sin(_angle), 4)

NETWORK_DATA = dict(
    nodes=_net_nodes,
    edges=[
        {"source": 0, "target": 1},
        {"source": 0, "target": 2},
        {"source": 0, "target": 3},
        {"source": 0, "target": 6},
        {"source": 1, "target": 4},
        {"source": 1, "target": 5},
        {"source": 2, "target": 5},
        {"source": 2, "target": 6},
        {"source": 3, "target": 7},
        {"source": 4, "target": 7},
        {"source": 5, "target": 6},
        {"source": 6, "target": 7},
    ],
)

# Example 5 — Chord Diagram: department cross-collaboration flow matrix
CHORD_DATA = dict(
    names=["Sales", "Tech", "Ops", "Finance", "HR"],
    matrix=[
        [0, 25, 18, 12, 8],
        [25, 0, 30, 15, 10],
        [18, 30, 0, 22, 14],
        [12, 15, 22, 0, 20],
        [8, 10, 14, 20, 0],
    ],
)

# Example 6 — Arc Diagram: software module dependency graph
# Nodes are laid out on a horizontal axis; arcs curve above the baseline.
# Arc height ∝ distance between nodes; stroke width ∝ dependency weight.
ARC_DATA = dict(
    nodes=[
        {"id": 0, "label": "Core", "group": 0},
        {"id": 1, "label": "Config", "group": 0},
        {"id": 2, "label": "Logger", "group": 0},
        {"id": 3, "label": "Auth", "group": 1},
        {"id": 4, "label": "API", "group": 1},
        {"id": 5, "label": "Queue", "group": 1},
        {"id": 6, "label": "DB", "group": 2},
        {"id": 7, "label": "Cache", "group": 2},
        {"id": 8, "label": "UI", "group": 3},
        {"id": 9, "label": "Tests", "group": 3},
    ],
    edges=[
        {"source": 0, "target": 1, "weight": 5},
        {"source": 0, "target": 2, "weight": 4},
        {"source": 0, "target": 3, "weight": 6},
        {"source": 0, "target": 6, "weight": 7},
        {"source": 1, "target": 3, "weight": 3},
        {"source": 1, "target": 4, "weight": 4},
        {"source": 2, "target": 5, "weight": 2},
        {"source": 3, "target": 4, "weight": 5},
        {"source": 3, "target": 6, "weight": 6},
        {"source": 4, "target": 7, "weight": 4},
        {"source": 4, "target": 8, "weight": 3},
        {"source": 5, "target": 7, "weight": 2},
        {"source": 6, "target": 9, "weight": 3},
        {"source": 7, "target": 8, "weight": 5},
        {"source": 8, "target": 9, "weight": 4},
    ],
)

# ═════════════════════════════════════════════════════════════════════════════
#  PLOTLY FIGURE BUILDERS
# ═════════════════════════════════════════════════════════════════════════════


def _base_layout(title: str) -> dict:
    """Shared dark-theme layout for every Plotly figure."""
    return dict(
        title=dict(text=title, font=dict(color=TEXT_COL, size=15)),
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COL, size=12),
        xaxis=dict(gridcolor=GRID_COL, zeroline=False, linecolor=GRID_COL),
        yaxis=dict(gridcolor=GRID_COL, zeroline=False, linecolor=GRID_COL),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        margin=dict(l=50, r=20, t=50, b=50),
    )


def fig_bar() -> go.Figure:
    fig = go.Figure(
        [
            go.Bar(
                name=BAR_DATA["label_a"],
                x=BAR_DATA["categories"],
                y=BAR_DATA["series_a"],
                marker_color=COLOR_A,
            ),
            go.Bar(
                name=BAR_DATA["label_b"],
                x=BAR_DATA["categories"],
                y=BAR_DATA["series_b"],
                marker_color=COLOR_B,
            ),
        ]
    )
    fig.update_layout(**_base_layout("Monthly Sales — Grouped Bar"), barmode="group")
    return fig


def fig_line() -> go.Figure:
    fig = go.Figure(
        [
            go.Scatter(
                name=LINE_DATA["label_a"],
                x=LINE_DATA["months"],
                y=LINE_DATA["city_a"],
                mode="lines+markers",
                line=dict(color=COLOR_A, width=2.5),
                marker=dict(size=7),
                fill="tozeroy",
                fillcolor="rgba(108,99,255,0.08)",
            ),
            go.Scatter(
                name=LINE_DATA["label_b"],
                x=LINE_DATA["months"],
                y=LINE_DATA["city_b"],
                mode="lines+markers",
                line=dict(color=COLOR_B, width=2.5),
                marker=dict(size=7),
                fill="tozeroy",
                fillcolor="rgba(255,101,132,0.08)",
            ),
        ]
    )
    fig.update_layout(**_base_layout("Avg Monthly Temperature (°C)"))
    return fig


def fig_scatter() -> go.Figure:
    color_map = {"Group A": COLOR_A, "Group B": COLOR_B, "Group C": COLOR_C}
    fig = go.Figure()
    for grp in ["Group A", "Group B", "Group C"]:
        idx = [i for i, g in enumerate(SCATTER_DATA["group"]) if g == grp]
        fig.add_trace(
            go.Scatter(
                name=grp,
                x=[SCATTER_DATA["x"][i] for i in idx],
                y=[SCATTER_DATA["y"][i] for i in idx],
                mode="markers",
                marker=dict(
                    color=color_map[grp],
                    size=[SCATTER_DATA["size"][i] for i in idx],
                    opacity=0.85,
                    line=dict(width=1, color="rgba(255,255,255,0.25)"),
                ),
            )
        )
    fig.update_layout(**_base_layout("Scatter Plot — Three Groups"))
    return fig


def fig_network() -> go.Figure:
    """Static circular-layout network — Plotly's closest approximation."""
    fig = go.Figure()
    group_colors = {0: COLOR_A, 1: COLOR_B, 2: COLOR_C}
    nodes_by_id = {n["id"]: n for n in NETWORK_DATA["nodes"]}
    # Edges (drawn first so nodes appear on top)
    for e in NETWORK_DATA["edges"]:
        src = nodes_by_id[e["source"]]
        tgt = nodes_by_id[e["target"]]
        fig.add_trace(
            go.Scatter(
                x=[src["x"], tgt["x"], None],
                y=[src["y"], tgt["y"], None],
                mode="lines",
                line=dict(color=GRID_COL, width=2),
                showlegend=False,
                hoverinfo="none",
            )
        )
    # Nodes per group
    for grp in [0, 1, 2]:
        grp_nodes = [n for n in NETWORK_DATA["nodes"] if n["group"] == grp]
        fig.add_trace(
            go.Scatter(
                x=[n["x"] for n in grp_nodes],
                y=[n["y"] for n in grp_nodes],
                mode="markers+text",
                text=[n["label"] for n in grp_nodes],
                textposition="middle center",
                textfont=dict(color="#fff", size=10),
                marker=dict(
                    size=38,
                    color=group_colors[grp],
                    line=dict(width=2, color="#0f1117"),
                ),
                name=f"Group {grp}",
                showlegend=False,
            )
        )
    layout = _base_layout("Network Graph — Static (Pre-computed Circular Layout)")
    layout["xaxis"] = dict(visible=False)
    layout["yaxis"] = dict(visible=False, scaleanchor="x")
    fig.update_layout(**layout)
    return fig


def fig_chord() -> go.Figure:
    """Heatmap — Plotly has no native chord chart; this is the closest option."""
    names = CHORD_DATA["names"]
    matrix = CHORD_DATA["matrix"]
    fig = go.Figure(
        go.Heatmap(
            z=matrix,
            x=names,
            y=names,
            colorscale=[
                [0.0, PLOT_BG],
                [0.3, COLOR_C],
                [0.7, COLOR_A],
                [1.0, COLOR_B],
            ],
            showscale=True,
            text=[[str(v) if v else "" for v in row] for row in matrix],
            texttemplate="%{text}",
            textfont=dict(color=TEXT_COL, size=13),
            hovertemplate="%{y} → %{x}: %{z}<extra></extra>",
        )
    )
    fig.update_layout(
        **_base_layout("Cross-Collaboration — Heatmap (Plotly's closest)")
    )
    return fig


def fig_arc() -> go.Figure:
    """Arc diagram approximation: nodes on x-axis, arcs via SVG path shapes."""
    group_colors = {0: COLOR_A, 1: COLOR_B, 2: COLOR_C, 3: "#f5a623"}
    group_labels = {0: "Core", 1: "Services", 2: "Data", 3: "Front"}
    nodes = ARC_DATA["nodes"]
    edges = ARC_DATA["edges"]
    n = len(nodes)
    xs = list(range(n))

    # Quadratic-bezier arcs drawn via layout.shapes (SVG path, data coordinates)
    shapes = []
    for e in edges:
        x1, x2 = xs[e["source"]], xs[e["target"]]
        mid_x = (x1 + x2) / 2
        height = abs(x2 - x1) * 0.45
        width = 0.6 + e["weight"] * 0.18
        col = group_colors[nodes[e["source"]]["group"]]
        shapes.append(
            dict(
                type="path",
                path=f"M {x1:.2f},0 Q {mid_x:.2f},{height:.3f} {x2:.2f},0",
                line=dict(color=col, width=width),
                fillcolor="rgba(0,0,0,0)",
                opacity=0.55,
            )
        )

    fig = go.Figure()
    # One trace per group so Plotly renders a colour legend automatically
    for grp in [0, 1, 2, 3]:
        grp_nodes = [nd for nd in nodes if nd["group"] == grp]
        fig.add_trace(
            go.Scatter(
                x=[xs[nd["id"]] for nd in grp_nodes],
                y=[0] * len(grp_nodes),
                mode="markers+text",
                name=group_labels[grp],
                text=[nd["label"] for nd in grp_nodes],
                textposition="bottom center",
                textfont=dict(color=TEXT_COL, size=10),
                marker=dict(
                    size=14,
                    color=group_colors[grp],
                    line=dict(width=2, color="#0f1117"),
                ),
            )
        )

    layout = _base_layout("Arc Diagram — Plotly (SVG Path Shapes, Static)")
    layout["shapes"] = shapes
    layout["xaxis"] = dict(visible=False, range=[-0.5, n - 0.5])
    layout["yaxis"] = dict(visible=False, range=[-1.8, 5.0])
    fig.update_layout(**layout)
    return fig


# ═════════════════════════════════════════════════════════════════════════════
#  APP
# ═════════════════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_scripts=["https://d3js.org/d3.v7.min.js"],
    suppress_callback_exceptions=True,
)
app.title = "Plotly vs D3.js — Five Examples"

# ── Shared tab chrome ─────────────────────────────────────────────────────────
_TAB = dict(
    backgroundColor="#1a1d27",
    color="#8888aa",
    border="1px solid #2d2f45",
    borderRadius="6px 6px 0 0",
    padding="10px 28px",
    fontWeight="500",
)
_TAB_SELECTED = {
    **_TAB,
    "backgroundColor": "#252836",
    "color": "#e0e0e0",
    "borderBottom": "2px solid #6c63ff",
}

# ── Reusable card builder ──────────────────────────────────────────────────────


def _badge(label: str, css_class: str) -> html.Span:
    return html.Span(label, className=f"badge {css_class}")


def _card(badge_label, badge_class, subtitle, description, body):
    return html.Div(
        [
            html.Div(
                [
                    _badge(badge_label, badge_class),
                    html.H3(subtitle, className="card-title"),
                    html.P(description, className="card-desc"),
                ],
                className="card-header",
            ),
            body,
        ],
        className="chart-card",
    )


def _comparison(plotly_fig, d3_id, plotly_desc, d3_desc, plotly_badge="Plotly"):
    """Return a two-column grid: Plotly chart | D3 chart."""
    return html.Div(
        [
            _card(
                plotly_badge,
                "badge-plotly",
                "Python · Plotly Graph Objects",
                plotly_desc,
                dcc.Graph(
                    figure=plotly_fig,
                    config={"displayModeBar": False},
                    style={"height": "370px"},
                ),
            ),
            _card(
                "D3.js v7",
                "badge-d3",
                "JavaScript · D3 v7 via clientside_callback",
                d3_desc,
                html.Div(id=d3_id, className="d3-container"),
            ),
        ],
        className="two-col",
    )


# ── Root layout ───────────────────────────────────────────────────────────────
app.layout = html.Div(
    [
        # Persistent data stores (survive tab switches)
        dcc.Store(id="store-bar", data=BAR_DATA),
        dcc.Store(id="store-line", data=LINE_DATA),
        dcc.Store(id="store-scatter", data=SCATTER_DATA),
        dcc.Store(id="store-network", data=NETWORK_DATA),
        dcc.Store(id="store-chord", data=CHORD_DATA),
        dcc.Store(id="store-arc", data=ARC_DATA),
        # Hero header
        html.Header(
            [
                html.Div("📊", className="header-icon"),
                html.Div(
                    [
                        html.H1("Plotly  vs  D3.js", className="header-title"),
                        html.P(
                            "Five side-by-side examples — the same dataset rendered with "
                            "Plotly Graph Objects (Python) and D3.js v7 (JavaScript). "
                            "The last two tabs showcase chart types where D3 has no "
                            "Plotly equivalent: force-directed graphs and chord diagrams.",
                            className="header-sub",
                        ),
                    ]
                ),
            ],
            className="hero",
        ),
        # Key-concept chips
        html.Div(
            [
                html.Span("Grouped Bar Chart", className="chip"),
                html.Span("Multi-Line Chart", className="chip"),
                html.Span("Scatter Plot", className="chip"),
                html.Span("Force-Directed Graph ★", className="chip chip-d3wins"),
                html.Span("Chord Diagram ★", className="chip chip-d3wins"),
                html.Span("Arc Diagram ★", className="chip chip-d3wins"),
                html.Span("clientside_callback", className="chip chip-accent"),
                html.Span("D3 v7", className="chip chip-accent"),
            ],
            className="chip-row",
        ),
        # Tabs
        dcc.Tabs(
            id="tabs",
            value="tab1",
            children=[
                dcc.Tab(
                    label="① Grouped Bar Chart",
                    value="tab1",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
                dcc.Tab(
                    label="② Multi-Line Chart",
                    value="tab2",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
                dcc.Tab(
                    label="③ Scatter Plot",
                    value="tab3",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
                dcc.Tab(
                    label="④ Force Graph  ★ D3 wins",
                    value="tab4",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
                dcc.Tab(
                    label="⑤ Chord Diagram  ★ D3 wins",
                    value="tab5",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
                dcc.Tab(
                    label="⑥ Arc Diagram  ★ D3 wins",
                    value="tab6",
                    style=_TAB,
                    selected_style=_TAB_SELECTED,
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        html.Div(id="tab-content"),
    ],
    className="app-shell",
)


# ═════════════════════════════════════════════════════════════════════════════
#  SERVER CALLBACK — tab routing
# ═════════════════════════════════════════════════════════════════════════════


@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab: str):
    if tab == "tab1":
        return _comparison(
            fig_bar(),
            "d3-bar",
            plotly_desc=(
                "Two go.Bar() traces with barmode='group'. "
                "Plotly handles axes, hover tooltips, and the legend automatically "
                "through its declarative Python API."
            ),
            d3_desc=(
                "d3.scaleBand() lays out the grouped categories; an inner x1 band "
                "positions the two sub-bars. Y gridlines are drawn as axis-tick "
                "extensions. Axes and legend are appended as SVG elements."
            ),
        )
    if tab == "tab2":
        return _comparison(
            fig_line(),
            "d3-line",
            plotly_desc=(
                "Two go.Scatter() traces with mode='lines+markers' and "
                "fill='tozeroy' for the translucent area gradient. "
                "Curve smoothing is applied automatically."
            ),
            d3_desc=(
                "d3.line() with curveMonotoneX generates smooth paths. "
                "A separate d3.area() path adds the filled gradient. "
                "d3.scalePoint() spaces the month labels evenly on the x-axis."
            ),
        )
    if tab == "tab4":
        return _comparison(
            fig_network(),
            "d3-force-graph",
            plotly_desc=(
                "Plotly has no force simulation. This renders the network "
                "as go.Scatter() lines (edges) + point markers (nodes) in a "
                "pre-computed circular layout. Nodes are static — no physics."
            ),
            d3_desc=(
                "d3.forceSimulation() applies charge repulsion, link springs, and "
                "collision forces. Drag any node — the graph re-settles with live "
                "physics. This real-time simulation is impossible in Plotly."
            ),
            plotly_badge="Plotly ≈",
        )
    if tab == "tab5":
        return _comparison(
            fig_chord(),
            "d3-chord",
            plotly_desc=(
                "Plotly has no chord chart. The heatmap is the closest option: "
                "it shows the same flow matrix but loses the arc topology and "
                "proportional ribbon widths that make chord diagrams powerful."
            ),
            d3_desc=(
                "d3.chord() computes the arc/ribbon geometry from a flow matrix. "
                "d3.arc() renders the outer group arcs; d3.ribbon() draws "
                "proportional inner ribbons encoding magnitude and directionality."
            ),
            plotly_badge="Plotly ≈",
        )
    if tab == "tab6":
        return _comparison(
            fig_arc(),
            "d3-arc",
            plotly_desc=(
                "Plotly approximates an arc diagram with layout.shapes using "
                "SVG path strings (M…Q…). Arc heights and stroke widths are "
                "pre-computed in Python. No hover interaction on individual arcs."
            ),
            d3_desc=(
                "Nodes placed via d3.scalePoint(); each arc is a quadratic bezier "
                "path (M…Q…) where height ∝ node distance and stroke-width ∝ "
                "edge weight. Hover a node to highlight only its connected arcs."
            ),
            plotly_badge="Plotly ≈",
        )
    return _comparison(
        fig_scatter(),
        "d3-scatter",
        plotly_desc=(
            "Three go.Scatter() traces (one per group) with variable marker size "
            "and per-trace colour. Plotly encodes the legend automatically."
        ),
        d3_desc=(
            "Each data point is a <circle> with cx/cy from d3.scaleLinear(). "
            "Fill colour and radius are mapped per point. "
            "A manual SVG legend group is appended at top-right."
        ),
    )


# ═════════════════════════════════════════════════════════════════════════════
#  CLIENTSIDE CALLBACKS — D3 rendering
#  Output targets `className` (not `children`) so React never clears the SVG
#  that D3 appends directly to the DOM.
# ═════════════════════════════════════════════════════════════════════════════

app.clientside_callback(
    ClientsideFunction("d3charts", "renderBarChart"),
    Output("d3-bar", "className"),
    Input("store-bar", "data"),
    Input("tabs", "value"),
)

app.clientside_callback(
    ClientsideFunction("d3charts", "renderLineChart"),
    Output("d3-line", "className"),
    Input("store-line", "data"),
    Input("tabs", "value"),
)

app.clientside_callback(
    ClientsideFunction("d3charts", "renderScatterPlot"),
    Output("d3-scatter", "className"),
    Input("store-scatter", "data"),
    Input("tabs", "value"),
)

app.clientside_callback(
    ClientsideFunction("d3charts", "renderForceGraph"),
    Output("d3-force-graph", "className"),
    Input("store-network", "data"),
    Input("tabs", "value"),
)

app.clientside_callback(
    ClientsideFunction("d3charts", "renderChordDiagram"),
    Output("d3-chord", "className"),
    Input("store-chord", "data"),
    Input("tabs", "value"),
)

app.clientside_callback(
    ClientsideFunction("d3charts", "renderArcDiagram"),
    Output("d3-arc", "className"),
    Input("store-arc", "data"),
    Input("tabs", "value"),
)


if __name__ == "__main__":
    app.run(debug=True)
