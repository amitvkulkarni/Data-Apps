import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import pulp
import dash_table
from dash import dcc
from dash import html
import UI


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = UI.Layout

shopping_list = []


@app.callback(
    [Output("shopping_table", "figure"), Output("total_cost_initial", "children")],
    [Input("add_button", "n_clicks")],
    [
        State("product_name", "value"),
        State("min_qty", "value"),
        State("max_qty", "value"),
        State("unit_price", "value"),
        State("discount_rate", "value"),
    ],
)
def update_shopping_list(
    n_clicks, product_name, min_qty, max_qty, unit_price, discount_rate
):

    if n_clicks is None or n_clicks == 0:
        return {
            "data": [
                {
                    "type": "table",
                    "header": {
                        "values": [
                            "No Shopping List Created. Add items to the shopping list"
                        ]
                    },
                    # "cells": {"values": [["Add items to the shopping list"]]},
                }
            ]
        }, None
    if n_clicks:
        actual_cost = unit_price * max_qty
        discount = (unit_price * discount_rate / 100) * max_qty
        total_cost = actual_cost - discount

        shopping_list.append(
            {
                "Product Name": product_name,
                "Min Qty": min_qty,
                "Max Qty": max_qty,
                "Unit Price": unit_price,
                "Discount Rate": discount_rate,
                "Actual Cost": actual_cost,
                "Total Cost": total_cost,
            }
        )

    df = pd.DataFrame(shopping_list)

    total_cost_initial = df["Total Cost"].sum()

    return {
        "data": [
            {
                "type": "table",
                "header": {"values": list(df.columns)},
                "cells": {"values": [df[col] for col in df.columns]},
            }
        ]
    }, f"Total Cost (Initial): ${total_cost_initial:.2f}"


@app.callback(
    [
        Output("optimization_results", "figure"),
        Output("total_cost_optimized", "children"),
    ],
    [Input("optimize_button", "n_clicks")],
    [State("budget", "value")],
)
def optimize_shopping_list(n_clicks, budget):
    if n_clicks is None or n_clicks == 0:
        return (
            {
                "data": [
                    {
                        "type": "table",
                        "header": {
                            "values": [
                                [
                                    'If you have added items to list then click "Optimize" to see results'
                                ]
                            ]
                        },
                        # "cells": {"values": [['Click "Optimize" to see results']]},
                    }
                ]
            },
            None,
        )

    df = pd.DataFrame(shopping_list)

    if df.empty:
        return (
            {
                "data": [
                    {
                        "type": "table",
                        "header": {"values": ["No Data"]},
                        "cells": {"values": [["Add items to the list first"]]},
                    }
                ]
            },
            "Total Cost (Optimized): N/A",
        )

    prob = pulp.LpProblem("Shopping_Optimization", pulp.LpMinimize)

    qty_vars = {
        i: pulp.LpVariable(
            f"qty_{i}",
            lowBound=row["Min Qty"],
            upBound=row["Max Qty"],
            cat="Continuous",
        )
        for i, row in df.iterrows()
    }

    total_cost_expr = pulp.lpSum(
        [
            qty_vars[i] * row["Unit Price"] * (1 - row["Discount Rate"] / 100)
            for i, row in df.iterrows()
        ]
    )

    prob += total_cost_expr == budget, "Budget Constraint"

    dummy_var = pulp.LpVariable("dummy", 0)
    prob += dummy_var

    prob.solve()

    if pulp.LpStatus[prob.status] != "Optimal":
        return {
            "data": [
                {
                    "type": "table",
                    "header": {"values": ["Optimization Error"]},
                    "cells": {"values": [["No optimal solution found"]]},
                }
            ]
        }

    df["Optimized Qty"] = [qty_vars[i].varValue for i in df.index]
    df["Optimized Total Cost"] = round(
        df["Optimized Qty"] * df["Unit Price"] * (1 - df["Discount Rate"] / 100), 1
    )

    df["Optimized Qty"] = df[["Min Qty", "Optimized Qty", "Max Qty"]].apply(
        lambda x: min(max(x["Optimized Qty"], x["Min Qty"]), x["Max Qty"]), axis=1
    )

    total_cost_optimized = df["Optimized Total Cost"].sum()

    return (
        {
            "data": [
                {
                    "type": "table",
                    "header": {
                        "values": df[
                            ["Product Name", "Optimized Qty", "Optimized Total Cost"]
                        ].columns.tolist()
                    },
                    "cells": {
                        "values": [
                            df[col]
                            for col in df[
                                [
                                    "Product Name",
                                    "Optimized Qty",
                                    "Optimized Total Cost",
                                ]
                            ].columns
                        ]
                    },
                }
            ]
        },
        f"Total Cost (Optimized): ${total_cost_optimized:.2f}",
    )


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False, dev_tools_ui=False)
