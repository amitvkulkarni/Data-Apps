# csv_explorer.py — NiceGUI CSV Data Explorer
# From: "NiceGUI: Building Modern Web UIs with Pure Python"
#
# Hands-On Walkthrough: Upload a CSV, preview it as a table,
# and visualize a selected numeric column as a bar chart.
#
# Run: python csv_explorer.py
# Then open: http://localhost:8080

from nicegui import ui, events
import pandas as pd
import io

# Module-level store — single-user use only.
# For multi-user: move inside the page function and use app.storage.user
df_store = {"df": None}

# These will be assigned inside main() — referenced by handlers defined at module level
table_container = None
chart_container = None
column_select = None


async def handle_upload(e: events.UploadEventArguments):
    """Handle CSV file upload and parse it into a DataFrame."""
    # NiceGUI 3.x: file data lives in e.file, and .read() is a coroutine
    content = await e.file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
        df_store["df"] = df
        refresh_view()
        ui.notify(
            f"Loaded {len(df)} rows, {len(df.columns)} columns",
            type="positive",
        )
    except Exception as ex:
        ui.notify(f"Error reading file: {ex}", type="negative")


def refresh_view():
    """Redraw the table container and reset the column selector."""
    df = df_store["df"]
    if df is None:
        return

    table_container.clear()
    chart_container.clear()

    # Use set_options/set_value so NiceGUI 3.x pushes the update to the browser
    # Build option labels that indicate the column type (numeric vs categorical)
    options = {}
    for c in df.columns:
        dtype_tag = "numeric" if pd.api.types.is_numeric_dtype(df[c]) else "categorical"
        options[c] = f"{c}  [{dtype_tag}]"
    column_select.set_options(options)
    column_select.set_value(None)

    # Replace NaN/NaT with None so the JSON serialiser doesn't choke
    rows = df.head(20).where(pd.notnull(df.head(20)), other=None).to_dict("records")
    with table_container:
        ui.table(
            columns=[
                {"name": c, "label": c, "field": c, "align": "left"} for c in df.columns
            ],
            rows=rows,
            row_key=df.columns[0],
        ).classes("w-full")


def show_chart():
    """Render the appropriate chart for the selected column.

    - Numeric  → bar chart of the first 50 raw values
    - Categorical → horizontal bar chart of the top-20 value counts
    """
    df = df_store["df"]
    col = column_select.value
    if df is None or not col:
        ui.notify("Upload a CSV and select a column first", type="warning")
        return

    chart_container.clear()

    if pd.api.types.is_numeric_dtype(df[col]):
        # ── Numeric: bar chart of raw values (first 50) ────────────────────
        values = df[col].dropna()
        with chart_container:
            ui.echart(
                {
                    "title": {"text": f"Distribution: {col} (numeric)"},
                    "xAxis": {
                        "type": "category",
                        "data": [str(round(v, 2)) for v in values.values[:50]],
                        "axisLabel": {"rotate": 45},
                    },
                    "yAxis": {"type": "value"},
                    "series": [{"type": "bar", "data": values.values[:50].tolist()}],
                    "tooltip": {"trigger": "axis"},
                    "grid": {"bottom": "20%"},
                }
            ).classes("w-full h-72")
    else:
        # ── Categorical: horizontal bar chart of top-20 value counts ───────
        counts = df[col].dropna().value_counts().head(20)
        categories = counts.index.astype(str).tolist()
        count_values = counts.values.tolist()
        with chart_container:
            ui.echart(
                {
                    "title": {"text": f"Value Counts: {col} (categorical)"},
                    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                    "grid": {
                        "left": "25%",
                        "right": "5%",
                        "top": "10%",
                        "bottom": "5%",
                    },
                    "xAxis": {"type": "value", "name": "Count"},
                    "yAxis": {
                        "type": "category",
                        "data": categories[::-1],  # highest count at the top
                        "axisLabel": {"overflow": "truncate", "width": 120},
                    },
                    "series": [
                        {
                            "type": "bar",
                            "data": count_values[::-1],
                            "label": {"show": True, "position": "right"},
                            "itemStyle": {"color": "#6366f1"},
                        }
                    ],
                }
            ).classes("w-full h-96")


@ui.page("/")
def main():
    global table_container, chart_container, column_select

    # ── Header ────────────────────────────────────────────────────────────────
    with ui.header(elevated=True).classes(
        "bg-blue-800 text-white items-center px-6 gap-3"
    ):
        ui.icon("table_chart").classes("text-2xl")
        ui.label("CSV Data Explorer").classes("text-xl font-bold")

    # ── Body ──────────────────────────────────────────────────────────────────
    with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-6"):

        # Upload card
        with ui.card().classes("w-full"):
            ui.label("Upload CSV").classes("text-lg font-semibold mb-2")
            ui.label("Drop a .csv file or click to browse.").classes(
                "text-sm text-gray-500 mb-3"
            )
            ui.upload(on_upload=handle_upload, auto_upload=True).classes("w-full")

        # Table preview card
        with ui.card().classes("w-full"):
            ui.label("Data Preview (first 20 rows)").classes(
                "text-lg font-semibold mb-2"
            )
            table_container = ui.column().classes("w-full")

        # Visualizer card
        with ui.card().classes("w-full"):
            ui.label("Column Visualizer").classes("text-lg font-semibold mb-2")
            with ui.row().classes("items-center gap-4 mb-3"):
                column_select = ui.select([], label="Select column to plot").classes(
                    "w-72"
                )
                ui.button("Plot", on_click=show_chart, icon="bar_chart").classes(
                    "bg-blue-700 text-white"
                )
            chart_container = ui.column().classes("w-full")

    # ── Footer ────────────────────────────────────────────────────────────────
    with ui.footer().classes("bg-gray-100 text-center text-gray-500 text-sm py-3"):
        ui.label("NiceGUI CSV Explorer — csv_explorer.py")


ui.run(title="CSV Explorer", port=8080, reload=False)
