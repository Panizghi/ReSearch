import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import utils
from layouts import create_main_layout
from callbacks import register_callbacks

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Research Analytics"
server = app.server

# Set the main layout
app.layout = create_main_layout()

# Register all callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
