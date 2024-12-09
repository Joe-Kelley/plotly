import urllib.request, json
from datetime import datetime
import numpy as np
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Function to fetch data from the API
def fetch_data(item_id):
    url = f'http://services.runescape.com/m=itemdb_oldschool/api/graph/{item_id}.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

# Function to fetch item details from the API
def fetch_item_details(item_id):
    url = f'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item={item_id}'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return data

# Function to search for item ID by name
def search_item_id(item_name):
    item_name_lower = item_name.lower()
    page = 1
    while True:
        url = f'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={item_name_lower[0]}&page={page}'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8', errors='ignore'))
        
        # Debug: Print the data returned by the API
        print(f"API response data for page {page}:", json.dumps(data, indent=4))
        
        if 'items' not in data or not data['items']:
            break
        
        for item in data['items']:
            print(f"Checking item: {item['name'].lower()} against {item_name_lower}")
            if item['name'].lower() == item_name_lower:
                return item['id']
        
        page += 1
    
    return None

# Function to process data for plotting
def process_data(data):
    timestamps = list(data['daily'].keys())
    prices = list(data['daily'].values())
    
    # Convert timestamps to readable dates
    dates = [datetime.fromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d') for ts in timestamps]
    
    return dates, prices

# Function to calculate linear regression trendline
def calculate_trendline(dates, prices):
    x = np.arange(len(dates))
    y = np.array(prices)
    coeffs = np.polyfit(x, y, 1)
    trendline = np.polyval(coeffs, x)
    return trendline

# Create a Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("OSRS Item Price Over Time"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(html.P("Please search for an itemID and submit to view price history"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id='item-name-input', type='text', placeholder='Enter Item Name', className="mb-2"), width=1),
        dbc.Col(html.Button(id='search-button', n_clicks=0, children='Search', className="btn btn-primary mb-2"), width=1)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Input(id='item-id-input', type='text', placeholder='Enter Item ID', className="mb-2"), width=1),
        dbc.Col(html.Button(id='submit-button', n_clicks=0, children='Submit', className="btn btn-primary mb-2"), width=1)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='price-graph'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='graph-type-dropdown',
            options=[
                {'label': 'Line Plot', 'value': 'line'},
                {'label': 'Scatter Plot', 'value': 'scatter'}
            ],
            value='line',
            className="mb-2"
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Checklist(
            id='trendline-checklist',
            options=[
                {'label': 'Show Trendline', 'value': 'show_trendline'}
            ],
            value=[],
            className="mb-2"
        ), width=6)
    ])
], fluid=True)

@app.callback(
    Output('item-id-input', 'value'),
    Input('search-button', 'n_clicks'),
    State('item-name-input', 'value')
)
def update_item_id(n_clicks, item_name):
    if not item_name:
        return ''
    
    item_id = search_item_id(item_name)
    if item_id:
        return str(item_id)
    else:
        return 'Item not found'

@app.callback(
    Output('price-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    Input('graph-type-dropdown', 'value'),
    Input('trendline-checklist', 'value'),
    State('item-id-input', 'value')
)
def update_graph(n_clicks, graph_type, trendline_options, item_id):
    if not item_id:
        return go.Figure()
    
    try:
        data = fetch_data(item_id)
        item_details = fetch_item_details(item_id)
        item_name = item_details['item']['name']
        dates, prices = process_data(data)
        
        fig = go.Figure()
        if graph_type == 'line':
            fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name='Price', showlegend=True))
        elif graph_type == 'scatter':
            fig.add_trace(go.Scatter(x=dates, y=prices, mode='markers', name='Price', showlegend=True))
        
        if 'show_trendline' in trendline_options:
            trendline = calculate_trendline(dates, prices)
            fig.add_trace(go.Scatter(x=dates, y=trendline, mode='lines', name='Trendline', line=dict(dash='dash'), showlegend=True))

            
        fig.update_layout(
            title=f'Item Price Over Time for {item_name} (ID: {item_id})',
            xaxis_title='Date',
            yaxis_title='Price',
            legend_title="Legend",
            legend=dict(
                x=1.05,
                y=1,
                traceorder="normal",
                bgcolor="LightSteelBlue",
                bordercolor="Black",
                borderwidth=2
            )
        )
        return fig
    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)