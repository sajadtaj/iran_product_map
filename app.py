import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Output,Input
import pandas as pd
import json
iran_map=pd.read_json('iran_geo.json')

app = dash.Dash( __name__ , external_stylesheets=[ dbc.themes.BOOTSTRAP ] )
df = px.data.election()
geojson = px.data.election_geojson()
candidates = df.winner.unique()



app.layout = html.Div([
    html.P("Candidate:"),
    dcc.RadioItems(
        id='candidate',
        options=[{'value': x, 'label': x}
                 for x in candidates],
        value=candidates[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])
@app.callback(
    Output("choropleth", "figure"),
    [Input("candidate", "value")])


def display_choropleth(candidate):
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="natural earth", range_color=[0, 5200] )
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port =2022)