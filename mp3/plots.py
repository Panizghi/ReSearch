import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def make_top_key_words(df, query):
    # Implement based on your data structure
    fig = px.bar(
        # Your implementation here
    )
    fig.update_layout(
        title="<span style='font-size: 22px;'><b>Top key words<b></span>",
        title_x=0.5,
        paper_bgcolor="rgba(104, 207, 247,0.0)",
        plot_bgcolor="rgba(104, 207, 247,0.0)"
    )
    return fig

def make_access_pie(df):
    # Implement based on your data structure
    fig = px.pie(
        # Your implementation here
    )
    fig.update_layout(
        title="<span style='font-size: 20px;'><b>Open access publications<b></span>",
        title_x=0.5,
        showlegend=False
    )
    return fig

# Add other plot functions... 