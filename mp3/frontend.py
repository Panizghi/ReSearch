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
import dash
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Default styles for Cytoscape elements
default_stylesheet = [
    {"selector": "node", "style": {"label": "data(label)", "width": "data(size)", "height": "data(size)"}},
    {"selector": "edge", "style": {"curve-style": "bezier", "line-color": "#a3a3a3"}},
]

# Navbar
navbar = dbc.NavbarSimple(
    brand="Research Visualization",
    brand_href="#",
    color="dark",
    dark=True,
)

# Layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label("Search"),
                dcc.Input(id="search-input", type="text", placeholder="Enter query...", debounce=True),
                html.Button("Search", id="search-button", n_clicks=0),
                html.Div(id="search-results", style={"margin-top": "20px"}),
            ], md=4),
            dbc.Col([
                html.Label("Filters"),
                dcc.Dropdown(id="filter-journals", multi=True, placeholder="Select Journals"),
                dcc.Slider(id="filter-citations", min=0, max=50, step=1, value=10, marks={0: "0", 50: "50+"}),
            ], md=4),
            dbc.Col([
                html.Label("Visualization Parameters"),
                dcc.RadioItems(
                    id="dim-reduction-method",
                    options=[
                        {"label": "TSNE", "value": "tsne"},
                        {"label": "UMAP", "value": "umap"}
                    ],
                    value="tsne",
                    labelStyle={"display": "block"}
                ),
                dcc.Slider(id="tsne-perplexity", min=5, max=50, step=5, value=30, marks={5: "5", 50: "50"}),
            ], md=4),
        ]),
        dbc.Row([
            dbc.Col([
                cyto.Cytoscape(
                    id="graph",
                    style={"width": "100%", "height": "500px"},
                    layout={"name": "preset"},
                    stylesheet=default_stylesheet,
                )
            ], md=8),
            dbc.Col([
                html.Div(id="node-info", children="Select a node to view details", style={"padding": "20px"})
            ], md=4),
        ])
    ], fluid=True)
])

# Callbacks
@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    Input("search-input", "value"),
)
def update_search_results(n_clicks, query):
    if n_clicks > 0 and query:
        try:
            response = requests.get("http://127.0.0.1:8000/search_with_scores", params={"query": query, "k": 5})
            response.raise_for_status()
            data = response.json()
            return html.Div([
                html.H5("Search Results"),
                html.Ul([html.Li(f"{res['title']} - {res['similarity_score']:.2f}") for res in data.get("results", [])])
            ])
        except Exception as e:
            return f"Error fetching search results: {str(e)}"
    return "Enter a query and click Search."

@app.callback(
    Output("graph", "elements"),
    Input("search-input", "value"),
    Input("filter-journals", "value"),
    Input("filter-citations", "value"),
    Input("dim-reduction-method", "value"),
    Input("tsne-perplexity", "value"),
)
def update_graph(query, journals, citations, method, perplexity):
    try:
        response = requests.get("http://127.0.0.1:8000/get_profile")
        response.raise_for_status()
        data = response.json()["data"]

        # Create a DataFrame
        df = pd.DataFrame(data)
        if journals:
            df = df[df["journal"].isin(journals)]
        df = df[df["n_citations"] >= citations]

        # Create Cytoscape elements
        nodes = [{"data": {"id": str(idx), "label": row["title"], "size": row["n_citations"] * 10}} for idx, row in df.iterrows()]
        edges = [{"data": {"source": str(row["source"]), "target": str(row["target"])}} for _, row in df.iterrows() if "source" in row and "target" in row]
        return nodes + edges
    except Exception as e:
        return []

@app.callback(
    Output("node-info", "children"),
    Input("graph", "selectedNodeData"),
)
def display_node_info(selected_node_data):
    if selected_node_data:
        node = selected_node_data[-1]
        return html.Div([
            html.H5(f"Title: {node['label']}"),
            html.P(f"Citations: {node['size'] // 10}"),
        ])
    return "Select a node to view details"


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
