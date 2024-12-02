import plotly.express as px
import pandas as pd

from dash import Input, Output
import plotly.express as px
import pandas as pd
from dash import Input, Output, Dash

# Create the Dash app instance here instead of importing it
app = Dash(__name__)

# Load the visualization data
tsne_df = pd.read_csv('/Users/paniz/ReSearch/mp3/data/tsne_visualization.csv')
umap_df = pd.read_csv('/Users/paniz/ReSearch/mp3/data/umap_visualization.csv')

@app.callback(
    [Output('tsne-graph', 'figure'),
     Output('umap-graph', 'figure')],
    [Input('search-button', 'n_clicks'),
     Input('cluster-dropdown', 'value'),
     Input('fellow-dropdown', 'value')]
)
def update_visualizations(n_clicks, selected_cluster, selected_fellow):
    # Filter data based on selections
    tsne_filtered = tsne_df.copy()
    umap_filtered = umap_df.copy()
    
    if selected_cluster is not None:
        tsne_filtered = tsne_filtered[tsne_filtered['cluster'] == selected_cluster]
        umap_filtered = umap_filtered[umap_filtered['cluster'] == selected_cluster]
    
    if selected_fellow is not None:
        tsne_filtered = tsne_filtered[tsne_filtered['Full Name'] == selected_fellow]
        umap_filtered = umap_filtered[umap_filtered['Full Name'] == selected_fellow]
    
    # Create t-SNE visualization
    tsne_fig = px.scatter(
        tsne_filtered, 
        x='x', 
        y='y',
        color='cluster',
        hover_data=['Full Name', 'Citation', 'keywords'],
        title='t-SNE Visualization of Research Areas',
        color_continuous_scale='Viridis'
    )
    
    # Create UMAP visualization
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