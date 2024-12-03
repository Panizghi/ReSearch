from dash.dependencies import Input, Output, State
from dash import html, Input, Output
import requests
from dash import html
import json
import pandas as pd
import numpy as np
import plotly.express as px

def register_callbacks(app):
    @app.callback(
        Output("search-results", "children"),
        [Input("search-button", "n_clicks"), Input("search-query", "value")]
    )
    def update_search(n_clicks, query):
        if n_clicks and query:
            try:
                response = requests.get(
                    "http://127.0.0.1:8000/search_with_scores",
                    params={"query": query, "k": 5}
                )
                print(f"Search response: {response.text}")  # Debug print
                
                if response.status_code != 200:
                    return html.Div(
                        f"Error: {response.json().get('message', 'Unknown error')}", 
                        style={"color": "red"}
                    )
                
                data = response.json()
                results = data.get("results", [])
                suggestions = data.get("suggestions", [])

                result_divs = [
                    html.Div([
                        html.H4(result["title"]),
                        html.P(result["content_snippet"]),
                        html.A("Read More", href=result["url"], target="_blank"),
                    ], className="result-item") 
                    for result in results
                ]
                
                suggestion_divs = [
                    html.Div([
                        html.H4(suggestion["title"]),
                        html.A("Read More", href=suggestion["url"], target="_blank"),
                    ], className="suggestion-item")
                    for suggestion in suggestions
                ]

                return html.Div(result_divs + suggestion_divs)

            except Exception as e:
                print(f"Error in callback: {str(e)}")  # Debug print
                return html.Div(f"Error: {str(e)}", style={"color": "red"})
        return "Enter a query and click Search."
    @app.callback(
        [Output('tsne-graph', 'figure'),
        Output('umap-graph', 'figure')],
        [Input('search-button', 'n_clicks')]
        # Input('cluster-dropdown', 'value'),
        # Input('fellow-dropdown', 'value')]
    )
    def update_visualizations(n_clicks, selected_cluster = None, selected_fellow = None):
       # If no data is selected from the dropdown, we handle it gracefully
        # Load the data
        tsne_df = pd.read_csv('data/tsne_visualization.csv')
        umap_df = pd.read_csv('data/umap_visualization.csv')

        # Initialize filtered data as a copy of the original data
        tsne_filtered = tsne_df.copy()
        umap_filtered = umap_df.copy()
        
        # Apply cluster filtering if a cluster is selected
        if selected_cluster is not None:
            tsne_filtered = tsne_filtered[tsne_filtered['cluster'] == selected_cluster]
            umap_filtered = umap_filtered[umap_filtered['cluster'] == selected_cluster]
        
        # Apply fellow filtering if a fellow is selected
        if selected_fellow is not None:
            tsne_filtered = tsne_filtered[tsne_filtered['Full Name'] == selected_fellow]
            umap_filtered = umap_filtered[umap_filtered['Full Name'] == selected_fellow]
        
        # Create t-SNE figure
        tsne_fig = px.scatter(
            tsne_filtered, 
            x='x', 
            y='y',
            color='cluster',
            hover_data=['Full Name', 'Citation', 'keywords'],
            title='t-SNE Visualization of Research Areas',
            color_continuous_scale='Viridis'
        )
        
        # Create UMAP figure
        umap_fig = px.scatter(
            umap_filtered,
            x='x',
            y='y',
            color='cluster',
            hover_data=['Full Name', 'Citation', 'keywords'],
            title='UMAP Visualization of Research Areas',
            color_continuous_scale='Viridis'
        )
        
        # Update layout for better visualization
        for fig in [tsne_fig, umap_fig]:
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=True
            )
        
        return tsne_fig, umap_fig 