from dash.dependencies import Input, Output, State
import requests
from dash import html
import json

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