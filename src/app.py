from dash import dash_table, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import dash
import plotly.express as px
from geopy.geocoders import Nominatim
import os


def get_lat_long(row):
    location = row['Region']
    print("For Location:", location)
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")
    # entering the location name
    try:
        getLoc = loc.geocode(location)
        # printing address
        # print(getLoc.address)
        print("Latitude = ", getLoc.latitude)
        print("Longitude = ", getLoc.longitude)
        row['lat'] = getLoc.latitude
        row['long'] = getLoc.longitude

    except:
        row['lat'] = 0
        row['long'] = 0
        print("Latitude and Longitude not found")

    return row


# df2 = pd.read_excel(os.getcwd()+"\\..\\data\\UK_Regions.xlsx")
df2 = pd.read_excel(os.getcwd() + "/../data/UK_Regions.xlsx")
df3 = df2.apply(lambda row: get_lat_long(row), axis=1)

fig = px.scatter_mapbox(df3,
                        lat='lat',
                        lon='long',
                        size='Count',
                        color='Region',
                        mapbox_style='carto-positron',
                        hover_name='lat',
                        hover_data=['lat'],
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=50,
                        zoom=10)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='maps', figure=fig)
        ], width={'size': 8}),
    ]),
    dbc.Row([
        dbc.Col([html.Div(id='contents')
                 ], width={'size': 2})
    ])
], fluid=True)


@app.callback(Output('contents', 'children'),
              Input('maps', 'clickData'))
def update_contents(clickData):
    if clickData:
        fips = clickData['points'][0]['hovertext']
        dff = df3[df3['lat'] == fips]
        return html.Div([dash_table.DataTable(id='table',
                                              columns=[{"name": i, "id": i} for i in dff.columns],
                                              data=dff.to_dict(orient='records'))
                         ])


if __name__ == "__main__":
    app.run(debug=False)
