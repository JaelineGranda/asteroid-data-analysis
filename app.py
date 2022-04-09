import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('asteroid-filtered-dataset.csv')
my_data = df.sort_values(by = 'diameter', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')

app = dash.Dash(__name__)

#def albedo():
#    fig =px.scatter(x=my_data["moid_ld"].head(10), y=my_data["albedo"].head(10),
#	         size=my_data["diameter"].head(10), color=my_data["full_name"].head(10),
#                 hover_name=my_data["full_name"].head(10), log_x=True, size_max=60)
#    return fig

def diameters():
    fig = px.bar(df, x=my_data['full_name'].head(10), y=my_data['diameter'].head(10), color=my_data['diameter'].head(10),
    labels={'x':'name of asteroid','y':'kilometers'}, color_discrete_sequence=['indianred'])
    fig.update_layout(title_text='Top 10 Diameters')
    return fig


def neo():
    df = my_data["neo"].value_counts()
    fig = px.pie(my_data, values=df.values, names=df.index, title='Near Earth', color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(hoverinfo='value', textinfo='percent+label')
    return fig

def pha():
    df = my_data["pha"].value_counts()
    fig = px.pie(my_data, values=df.values, names=df.index, title='Potentially Hazardous', color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_traces(hoverinfo='value', textinfo='percent+label')
    return fig

def ranges():
    fig = px.histogram(my_data, x="diameter", color_discrete_sequence=['midnightblue'])
    fig.update_layout(bargap=0.9, title_text='Diameter Distribution')
    return fig

def focusedRanges():
    #df = my_data.loc[my_data["diameter"] < 20]
    fig = px.histogram(my_data, x="diameter", range_x=[0, 20], color_discrete_sequence=['rebeccapurple'])
    fig.update_layout(bargap=0.2, title_text='Focused Diameter Distribution')
    return fig

def absMag():
    fig = px.histogram(my_data, x="H", color_discrete_sequence=['midnightblue'])
    fig.update_layout(bargap=0.9, title_text='Absoulte Magnitude Distribution')
    return fig

def availDiameters():
    percentage = 100 -(((my_data['diameter'].isna().sum()) / len(my_data. index)) *100)
    fig = go.Figure()
    fig.add_trace(go.Indicator(
    mode = "gauge+number",
    value = percentage,
    number= {'suffix': "%" },
    gauge= {'axis': {'range': [None, 100]},
            'steps' : [
                 {'range': [0, 100], 'color': "lightgray"}]},
    delta = {'reference': 100},
    title = {'text': "Measurable Diameters"},
    domain = {'x': [0, 1], 'y': [0, 1]}))
    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Asteroid Analytics",),
        html.P(
            children="Analyze Potential Dangers of Asteroids",
        ),
        dcc.Graph(id='Top 10 Diameters',
            figure= diameters()
        ),
        dcc.Graph(
            figure= availDiameters()
        ),
        dcc.Graph(
            figure= neo()
        ),
        dcc.Graph(
            figure= pha()
        ),
        dcc.Graph(
            figure= ranges()
        ),
        dcc.Graph(
            figure= focusedRanges()
        ),
        dcc.Graph(
            figure= absMag()
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)