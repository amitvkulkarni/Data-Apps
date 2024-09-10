import ast
import os
import pandas as pd
import dash
import json
import webbrowser
import threading
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.data = []
        self.current_file = ""
        self.current_class = None
        self.current_method = None
        self.defined_functions = set()

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.current_method = node.name
        method_calls = []
        built_in_or_library_call = False

        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    if n.func.id in self.defined_functions:
                        method_calls.append(n.func.id)
                    else:
                        built_in_or_library_call = True
                elif isinstance(n.func, ast.Attribute):
                    if n.func.attr in self.defined_functions:
                        method_calls.append(n.func.attr)
                    else:
                        built_in_or_library_call = True

        if method_calls:
            referenced_methods_content = (
                f'"{self.current_method}": {{"depends_on": {json.dumps(method_calls)}}}'
            )
        elif built_in_or_library_call:
            referenced_methods_content = f'"{self.current_method}": {{"depends_on": ["Built-in function / Libraries"]}}'
        else:
            referenced_methods_content = None

        self.data.append(
            {
                "File": self.current_file,
                "Class": self.current_class,
                "Method": self.current_method,
                "Type": "Method" if self.current_class else "Function",
                "Referenced Methods": referenced_methods_content,
            }
        )

        self.generic_visit(node)
        self.current_method = None


def parse_code(code, file_path):
    tree = ast.parse(code)
    parser = CodeParser()
    parser.current_file = file_path
    parser.visit(tree)
    return parser.data


def parse_files_in_directory(directory):
    all_data = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    file_data = parse_code(code, file_path)
                    all_data.extend(file_data)

    return all_data


directory_to_parse = "Dependency_tester"
parsed_data = parse_files_in_directory(directory_to_parse)

df = pd.DataFrame(parsed_data)

features = {}

for index, row in df.iterrows():
    if row["Referenced Methods"] is not None:
        try:
            parsed_dict = ast.literal_eval("{" + row["Referenced Methods"] + "}")
            features.update(parsed_dict)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing row {index}: {row['Referenced Methods']}. Error: {e}")


def get_all_related_features(start_feature, features):
    related_features = set()

    def add_dependencies(feature):
        if feature in related_features:
            return
        related_features.add(feature)
        for dep in features.get(feature, {}).get("depends_on", []):
            add_dependencies(dep)

    def add_dependents(feature):
        if feature in related_features:
            return
        related_features.add(feature)
        for f, data in features.items():
            if feature in data.get("depends_on", []):
                add_dependents(f)

    add_dependencies(start_feature)
    add_dependents(start_feature)

    return related_features


def build_tree(features, root=None):
    labels = []
    sources = []
    targets = []
    label_to_index = {}

    if root is None:
        related_features = set(features.keys())
    else:
        related_features = get_all_related_features(root, features)

    for feature in related_features:
        if feature not in label_to_index:
            label_to_index[feature] = len(label_to_index)
            labels.append(feature)

    for feature in related_features:
        for parent in features.get(feature, {}).get("depends_on", []):
            if parent in related_features:
                sources.append(label_to_index[parent])
                targets.append(label_to_index[feature])

    return labels, sources, targets


def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")


app = dash.Dash(__name__)

# Updated layout with flexbox to arrange dropdown and graph side by side
app.layout = html.Div(
    style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
    children=[
        html.H1(
            "Feature Dependency Analysis", style={"textAlign": "center"}
        ),  # Centered title
        html.Div(
            style={
                "display": "flex",
                "width": "100%",
                "justifyContent": "space-between",
            },
            children=[
                html.Div(
                    style={"flex": "1", "padding": "20px"},
                    children=[
                        dcc.Dropdown(
                            id="feature-dropdown",
                            options=[{"label": "All features", "value": "All features"}]
                            + [
                                {"label": feature, "value": feature}
                                for feature in features.keys()
                            ],
                            value="All features",
                            clearable=True,
                            style={"width": "100%"},
                        )
                    ],
                ),
                html.Div(
                    style={"flex": "3", "padding": "20px"},
                    children=[dcc.Graph(id="sankey-graph", style={"width": "100%"})],
                ),
            ],
        ),
    ],
)


@app.callback(Output("sankey-graph", "figure"), Input("feature-dropdown", "value"))
def update_sankey(selected_feature):
    if selected_feature == "All features":
        root = None
    else:
        root = selected_feature

    labels, sources, targets = build_tree(features, root=root)

    node_colors = [
        "LightSalmon" if label == selected_feature else "lightblue" for label in labels
    ]

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=node_colors,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=[1] * len(sources),
                color="gray",  # Link color
            ),
        )
    )

    fig.update_layout(
        title_text=f"Feature Dependency - {selected_feature}", font_size=15
    )
    return fig


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run_server(debug=False)
