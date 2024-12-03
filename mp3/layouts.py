from dash import dcc, html

def create_main_layout():
    return html.Div([
        # Banner
        create_banner(),
        
        # Search bar
        create_search_section(),
        
        # Data stores
        create_data_stores(),
        
        # Main content
        html.Div(id='start-page', children=[
            # Add the tabs content here
            create_tabs_content(),
            # Add the graphs inside a div
            html.Div([
                dcc.Graph(id='tsne-graph', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='umap-graph', style={'width': '48%', 'display': 'inline-block'})
            ], id='graphs-container')
        ], className='main-body'),
        
        # Footer
        create_footer()
    ], className="app-layout")

def create_banner():
    return html.Div([
        html.A([
            html.Img(src="/assets/logo.png", alt="research analytics"),
            html.H3("Research analytics Dashboard")
        ], href="#", className="logo-banner"),
        
        html.Div([
            html.A("Documentation", href="#", target='_blank', className="doc-link"),
        ], className="navbar")
    ], className="banner")

def create_search_section():
    return html.Div([
        html.H1(id='topic', children=[]),
        html.Div([
            html.Div([  # Search container
                dcc.Input(
                    id='search-query',
                    type='text',
                    placeholder="Search for anything...",
                    debounce=True,
                    className="search-input"
                ),
                html.Button(
                    'Search', 
                    id='search-button',
                    n_clicks=0,
                    className="search-button"
                )
            ], className="search-container"),
            html.Div(id='search-results', className="search-results")  # Results container
        ], className="search-bar")
    ], className="search-wrapper")

def create_data_stores():
    return html.Div([
        dcc.Store(id='store-initial-query-response', storage_type='memory'),
        dcc.Store(id='store-references-query-response', storage_type='memory')
    ])

def create_footer():
    return html.Footer([
        html.P(["Built with ", html.A("Plotly Dash", href="https://plotly.com/dash/", target="_blank")]),
    ])

def create_tabs_content():
    return html.Div([
        dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', className="tabs", children=[
            dcc.Tab(label=' Search results 📊', value='tab-1-example-graph',
                   className="single-tab", selected_className="single-tab-selected"),
            dcc.Tab(label='🤝 Author network 🤝', value='tab-2-example-graph',
                   className="single-tab", selected_className="single-tab-selected"),
            dcc.Tab(label='🌐 Paper network 🌐', value='tab-3-example-graph',
                   className="single-tab", selected_className="single-tab-selected")
        ])
    ], className="tabs-container") 