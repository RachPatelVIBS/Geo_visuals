from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go
import dash_auth
from flask import request


def get_heatmap(df2):
    figure = go.Figure(go.Densitymapbox(lat=df2['Latitude'], lon=df2['Longitude'], z=df2['Count'], radius=50))
    figure.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return figure


df2 = pd.read_excel(os.getcwd() + "/../data/UK_Regions.xlsx")
fig = get_heatmap(df2)

heatapp = Dash(__name__)
server = heatapp.server

heatapp.layout = html.Div([
    html.H4('HeatMap for UK Regions '),
    html.Br(),
    dcc.Graph(figure=fig),
])


if __name__ == '__main__':
    heatapp.run(debug=True)
