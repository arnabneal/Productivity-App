# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 22:43:12 2020

@author: User
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc



app=dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY])
crop_df = pd.read_csv("D:\Dash_Arnab\Productivity app\Data\crop_data.csv", low_memory=False)
crop_df["Productivity"]= crop_df.Production/crop_df.Area
crop_df=crop_df[["District","Crop_Year","Crop","Season","Production","Productivity","Area"]]


main_dict={k: g["Crop"].tolist() for k,g in crop_df.groupby("District")}
names = list(main_dict.keys())
#nestedOptions = main_dict[names]


app.layout = html.Div(
    [
    
      #Heading Cols           
    dbc.Row(
                [
      dbc.Col(
        dbc.Alert(html.H6("Select a District",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=3),
    
      dbc.Col(
        dbc.Alert(html.H6("Select The Crop",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=3),  
      dbc.Col(
        dbc.Alert(html.H6("Select The Season",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=3),
      
              ]
        ),
      # Dropdown cols design
    html.Div([         
    dbc.Row(
                [
      dbc.Col(
      dcc.Dropdown(
              id="tdd1",
    options=[{'label':name,'value':name}for name in names
    ],
    placeholder="Select a District",
      value=list(main_dict.keys())[0],
    style={'color':'red'},
    ),width=3),
    
    dbc.Col(
      dcc.Dropdown(
              id="tdd2",
     #options=[
    #    # {'label':i, 'value':i} for i in crops
     #],
    placeholder="Select The Crops",
      #value="Rice",
    style={'color':'blue'},
    ),width=3),
    
    dbc.Col(
      dcc.Dropdown(
              id="tdd3",
     #options=[
    #     #{'label':i, 'value':i} for i in crop_season
     #],
    placeholder="Select The Season",
      #value="",
      #value='Kharif     ',
    style={'color':'red'},
    ),width=3),
    
           
      ]),
            ],style={'padding':'4px'}),
])


@app.callback([Output('tdd2','options'),Output('tdd3','options')],[Input('tdd1','value')])

def drp_update(name):
    global crop_df
    
    
    main_dict={k: g["Crop"].tolist() for k,g in crop_df.groupby("District")}
    names = list(main_dict.keys())
    #crops = main_dict[names[0]]
    
    main_dict1={k: g["Season"].unique().tolist() for k,g in crop_df.groupby("District")}
    names1 = list(main_dict.keys())
    #crop_season= main_dict1[names1[0]]
    
    
    
    return [{'label': i, 'value': i} for i in main_dict[name]],[{'label': i, 'value': i} for i in main_dict1[name]]

if __name__ == "__main__":
    #host = socket.gethostbyname(socket.gethostname())
    app.run_server(debug=False)
