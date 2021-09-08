import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

def main(simulation_data,input_data,opts):
    # Plot a single time slice

    selected_time = -1
    selected_xaxis = 'XPSI'

    time = 999
    fig = go.Figure()
    template_plotly = 'plotly_dark'

    layout = go.Layout(
        title="Historic Prices",
        xaxis_title="time",
        yaxis_title="price"
    )

    for simulation in simulation_data:
        jsp_times = simulation['JSP']
        jst_times = simulation['JST']

        jsp = jsp_times.sel(time=time,method='nearest')
        jst = jst_times.sel(time=time,method='nearest')
        nesep = jsp["NE"][-1]
        # jsp_df = jsp.to_dataframe
        # jst_df = jst.to_dataframe
        jsp.drop('time')
        # df = jsp['TE'].to_dataframe
        # print(df)
        print(jsp['TE'].coords.values)
        print(jsp['TE'].values)
        # fig.add_trace(px.scatter(x=jsp['R'].values,y=jsp['TE'].values))
        fig.add_trace(px.scatter(x=[0,1,2],y=[10,20,30]))#,layout=layout)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
    server = app.server

    app.layout = html.Div([dcc.Graph(fig)])
    app.run_server(debug=True)
