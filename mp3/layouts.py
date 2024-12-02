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
        html.Div(id='start-page', children=[], className='main-body'),
        
        # Footer
        create_footer()
    ], className="app-layout")

def create_banner():
    return html.Div([
        html.A([
            html.Img(src="/assets/logo.png", alt="research analytics"),
            html.H3("research analytics")
        ], href="#", className="logo-banner"),
        
        html.Div([
            html.A("Documentation", href="#", target='_blank', className="doc-link"),
        ], className="navbar")
    ], className="banner")

def create_search_section():
    return html.Div([
        html.Div([
            # Search container with autocomplete
            html.Div([
                html.Div([
                    dcc.Input(
                        id='search-query',
                        type='text',
                        placeholder="Search for keywords...",
                        className="search-input",
                        list="suggestion-list"
                    ),
                    html.Datalist(
                        id='suggestion-list'
                    ),
                ], style={'flex': 1}),
                html.Button(
                    'Search', 
                    id='search-button',
                    n_clicks=0,
                    className="search-button"
                )
            ], className="search-container"),
            
            # Filter section
            html.Div([
                dcc.Dropdown(
                    id='author-dropdown',
                    placeholder="Filter by Author...",
                    className="filter-dropdown",
                    searchable=True,
                    clearable=True
                ),
                dcc.Dropdown(
                    id='category-dropdown',
                    placeholder="Filter by Category...",
                    className="filter-dropdown",
                    searchable=True,
                    clearable=True
                ),
                dcc.Dropdown(
                    id='location-dropdown',
                    placeholder="Filter by Location...",
                    className="filter-dropdown",
                    searchable=True,
                    clearable=True
                )
            ], className="filter-container")
        ], className="search-and-filters"),
        
        html.Div(id='search-results', className="search-results")
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