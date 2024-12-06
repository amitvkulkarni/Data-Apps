import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import dash_bootstrap_components as dbc

# Set up the database connection
db_user = "user"
db_password = "password"
db_host = "localhost"
db_name = "retail_sales_db"

# Create the database connection
db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
)

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Set up the query generation chain
generate_query = create_sql_query_chain(llm, db)

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div(
    style={"padding": "30px", "background-color": "#f7f9fc"},
    children=[
        # Title
        html.Div(
            dbc.Row(
                dbc.Col(
                    html.H1(
                        "NL2SQL Genie | Generate, Execute, and Get Results",
                        style={
                            "textAlign": "center",
                            "color": "#2C3E50",
                            "font-weight": "bold",
                            "color": "IndianRed",  # Set the font color to blue
                        },
                    ),
                    width=12,
                )
            )
        ),
        # Input and Result Panels (Using dbc.Cards)
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Enter Your Query", className="card-title"),
                                dcc.Textarea(
                                    id="user-query",
                                    placeholder="Type your query in natural language here... \n Example: How many transactions have more than 3 Quantity?",
                                    style={
                                        "width": "100%",
                                        "height": 300,
                                        "border-radius": "8px",
                                        "border": "1px solid #ccc",
                                    },
                                ),
                                html.Button(
                                    "Submit",
                                    id="submit-btn",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "10px",
                                        "width": "100%",
                                        "backgroundColor": "#3498db",
                                        "color": "white",
                                        "border": "none",
                                        "padding": "10px",
                                        "border-radius": "5px",
                                    },
                                ),
                            ]
                        ),
                        style={"marginBottom": "20px"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Generated SQL Query", className="card-title"),
                                dcc.Textarea(
                                    id="generated-query",
                                    placeholder="Awaiting your input...",
                                    style={
                                        "width": "100%",
                                        "height": 300,
                                        "border-radius": "8px",
                                        "border": "1px solid #ccc",
                                    },
                                    disabled=True,
                                ),
                            ]
                        ),
                        style={"marginBottom": "20px"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Final Response", className="card-title"),
                                dcc.Textarea(
                                    id="final-response",
                                    placeholder="Awaiting the query...",
                                    style={
                                        "width": "100%",
                                        "height": 300,
                                        "border-radius": "8px",
                                        "border": "1px solid #ccc",
                                    },
                                    disabled=True,
                                ),
                            ]
                        ),
                        style={"marginBottom": "20px"},
                    ),
                    width=4,
                ),
            ]
        ),
    ],
)


# Define the callback to update panels
@app.callback(
    [Output("generated-query", "value"), Output("final-response", "value")],
    [Input("submit-btn", "n_clicks")],
    [dash.dependencies.State("user-query", "value")],
)
def generate_sql_and_response(n_clicks, query):
    if n_clicks > 0 and query:
        # Generate SQL query
        sql_query = generate_query.invoke({"question": query})

        # Check if result is a string or dictionary and get query if necessary
        if isinstance(sql_query, dict):
            sql_query = sql_query.get("query", "")

        # Execute the query
        execute_query = QuerySQLDataBaseTool(db=db)
        sql_result = execute_query.invoke(sql_query)

        # Prepare the response
        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: """
        )

        rephrase_answer = answer_prompt | llm | StrOutputParser()
        final_answer = rephrase_answer.invoke(
            {"question": query, "query": sql_query, "result": sql_result}
        )

        # Return the SQL query and final response
        return sql_query, final_answer
    return "", ""


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
