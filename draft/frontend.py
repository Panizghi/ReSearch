import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Research Analytics"
server = app.server

# Define the API base URL
API_BASE_URL = "http://127.0.0.1:8000"

# App Layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value="search-tab", children=[
        dcc.Tab(label="Search", value="search-tab"),
        dcc.Tab(label="Visualization", value="visualization-tab"),
    ]),
    html.Div(id="tabs-content")
])

@app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "search-tab":
        return html.Div([
            html.H3("Search Documents", style={"margin-bottom": "10px"}),
            html.Div([
                dcc.Input(
                    id="search-query",
                    type="text",
                    placeholder="Enter your query...",
                    debounce=True,
                    style={"width": "70%", "margin-right": "10px"}
                ),
                html.Button("Search", id="search-button"),
            ], style={"margin-bottom": "20px"}),
            html.Div(id="search-results"),
        ], style={"padding": "20px"})
    elif tab == "visualization-tab":
        return html.Div([
            html.H3("3D Visualization", style={"margin-bottom": "10px"}),
            html.Button("Load Visualization", id="load-visualization", style={"margin-bottom": "20px"}),
            dcc.Loading(
                id="loading-visualization",
                type="circle",
                children=dcc.Graph(id="3d-scatter-plot")
            ),
        ], style={"padding": "20px"})

# Callback for Search Functionality
@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("search-query", "value"),
)
def update_search(n_clicks, query):
    if n_clicks and query:
        try:
            response = requests.get(f"{API_BASE_URL}/search_with_scores", params={"query": query, "k": 5})
            if response.status_code != 200:
                return html.Div("Error fetching search results. Please try again.", style={"color": "red"})

            data = response.json()
            results = data.get("results", [])
            suggestions = data.get("suggestions", [])

            if not results and not suggestions:
                return html.Div("No results found for your query.", style={"color": "blue"})

            # Display results
            result_divs = [
                html.Div([
                    html.H4(result["title"], style={"margin": "5px 0"}),
                    html.P(result["content_snippet"], style={"margin": "5px 0", "font-size": "12px"}),
                    html.A("Read More", href=result["url"], target="_blank", style={"color": "blue"})
                ], style={"border-bottom": "1px solid #ccc", "padding": "10px 0"})
                for result in results
            ]

            # Display suggestions
            suggestion_divs = [
                html.Div([
                    html.H4(suggestion["title"], style={"margin": "5px 0", "font-size": "14px"}),
                    html.A("Read More", href=suggestion["url"], target="_blank", style={"color": "blue"})
                ], style={"padding": "10px 0"})
                for suggestion in suggestions
            ]

            return html.Div(result_divs + [
                html.H5("You might also like:", style={"margin-top": "20px", "color": "gray"}),
            ] + suggestion_divs)
        except Exception as e:
            return html.Div(f"Error: {str(e)}", style={"color": "red"})
    return "Enter a query and click Search."

# Callback for Visualization Functionality
@app.callback(
    Output("3d-scatter-plot", "figure"),
    Input("load-visualization", "n_clicks")
)
def update_visualization(n_clicks):
    if n_clicks:
        try:
            response = requests.get(f"{API_BASE_URL}/visualize_embeddings")
            if response.status_code != 200:
                return px.scatter_3d(title="Error loading visualization data. Please try again.")

            data = response.json().get("data", [])
            if not data:
                return px.scatter_3d(title="No visualization data available.")

            df = pd.DataFrame(data)
            fig = px.scatter_3d(
                df,
                x="x",
                y="y",
                z="z",
                color="cluster",
                hover_data=["citation", "last_name", "given_name"],
                title="3D Semantic Similarity Map"
            )
            return fig
        except Exception as e:
            return px.scatter_3d(title=f"Error loading visualization: {str(e)}")
    return px.scatter_3d(title="Click 'Load Visualization' to begin")

if __name__ == "__main__":
    app.run_server(debug=True, port=8050, use_reloader=False)
