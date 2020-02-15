import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read in the data
df = pd.read_csv('honeyproduction.csv')

# CSS courtesy of the Plotly tutorials
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'text': '#FFCD33'
}

# Setup layout
app.layout = html.Div(style={'margin-left': '100px', 'margin-right': '100px'}, children=[
    
    # Page title
    html.H1(
        children='US Honey Production',
        style={ 
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),  
    
    # Placeholder for map
    dcc.Graph(id='map-with-slider'),
    
    # Slider to select year
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])

# Callback function to update the map
@app.callback(
    Output('map-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    dff = df[df.year == selected_year]
    
    trace = go.Choropleth(
        locations=dff['state'], # Spatial coordinates
        z = dff['totalprod'], # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'YlOrBr',
        colorbar_title = "Honey Production (lbs)",
    )
    
    return {"data": [trace],
            "layout": go.Layout(title="{} Production".format(selected_year),
            height=500,
            geo_scope='usa')}

if __name__ == '__main__':
    app.run_server(debug=False)