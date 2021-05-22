# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:19:04 2020

@author: Arnab Basak
"""

# Import required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
import folium
import branca.colormap as cm
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import pathlib
import dash_bootstrap_components as dbc
import dash_table
from statistics import stdev 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from app import app


# get relative data folder
#PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("data").resolve()




# Load data
crop = pd.read_csv("D:\Dash_Arnab\Productivity app\Data\crop_data.csv", low_memory=False)
#pd.read_csv(DATA_PATH.joinpath("crop_data.csv"), low_memory=False)

#Reading Shapefile
fname = 'D:/Dash_Arnab/Productivity app/shape_file/gadm36_IND_2.shp'
nil1= gpd.read_file(fname)
nil1.head()

#Reading another Shapefile for District
fname1='D:/Dash_Arnab/Productivity app/shape_file/gadm36_IND_1.shp'
ind11=gpd.read_file(fname1)

ind1=ind11[["NAME_1","GID_1"]]
state=ind11[["GID_1","geometry","NAME_1"]]

#crop_df_req= crop[(crop['Crop_Year'] == 2013) & (crop['Crop'] == "Rice") & (crop['Season'] =="Kharif     " )]

# new_map_data=crop_df_req.filter(["State_Name","District","Productivity"])
# new_map_data1=pd.merge(new_map_data,
#                       ind1,
#                       left_on=['State_Name'],
#                       right_on=['NAME_1'],
#                       how='outer')
# new_map_data1=new_map_data1.dropna(subset=["GID_1"])
# new_map_data1=new_map_data1.groupby("NAME_1")["Productivity"].mean().reset_index()
# map_req_df=new_map_data1.merge(state,on="NAME_1")
# map_req_df=gpd.GeoDataFrame(map_req_df,crs=crs, geometry='geometry')



#filtering out data
nil=nil1[['NAME_1','NAME_2','GID_2']]
nil2=nil1[['GID_2','geometry']]
#manupulate data
crop_year=crop["Crop_Year"].sort_values().unique().tolist()
crop["Productivity"]= crop.Production/crop.Area
crop_season=crop['Season'].unique().tolist()
crops=crop['Crop'].unique().tolist()
dist=crop['State_Name'].unique().tolist()

# Create app layout
layout=html.Div([dbc.FormGroup(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            options=[
                {'label': 'State', 'value': 'first'},
                {'label': 'District', 'value': 'second'},
            ],
            value='second',
            id="radio-items",
            inline=True,
            switch=True,
        ),
    ]
    ),
    

 html.Div(id="div",children=[])
 ])

#District Layout
layout1 = html.Div(
    [
    
      #Heading Cols           
    dbc.Row(
                [
      dbc.Col(
        dbc.Alert(html.H6("Select a Year",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),
    
      dbc.Col(
        dbc.Alert(html.H6("Select The Crop",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),  
      dbc.Col(
        dbc.Alert(html.H6("Select The Season",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),
      
              ]
        ),
      # Dropdown cols design
    html.Div([         
    dbc.Row(
                [
      dbc.Col(
      dcc.Dropdown(
              id="dd1",
    options=[
        {'label':i, 'value':i} for i in crop_year
    ],
    placeholder="Select a year",
      value=2013,
    style={'color':'red'},
    ),width=4),
    
    dbc.Col(
      dcc.Dropdown(
              id="dd2",
    options=[
        {'label':i, 'value':i} for i in crops
    ],
    placeholder="Select The Crops",
      value="Rice",
    style={'color':'blue'},
    ),width=4),
    
    dbc.Col(
      dcc.Dropdown(
              id="dd3",
    options=[
        {'label':i, 'value':i} for i in crop_season
    ],
    placeholder="Select The Season",
      value='Kharif     ',
    style={'color':'red'},
    ),width=4),
    
           
      ]),
            ],style={'padding':'4px'}),
           
      #Crop Table   
     
      html.Div([
    dbc.Row(
                        [
                                dbc.Col( dbc.Alert(
                                        html.H5("SUMMARY",style={"text-align":"center"},className="alert-heading"),color="info"), width={"size": 9, "offset": 1}),
                
            
                        ]
                        ),
                  dbc.Row(
                          [
                                 
                                  dbc.Col(
                                         
                                          dash_table.DataTable(
                                                  id='table',
                
                                                  data=[],
                                                  style_table={
                                                'height': '250px',
                                                'overflowY': 'scroll',
                                            },
                                            style_cell={'textAlign': 'center',
                                                        'font_family': 'cursive',
                                                        'font_size': '18px',
                                                        },
                                            style_header={'fontWeight': 'bold',
                                                          'font_size': '20px',
                                                          'color': 'white',
                                                          'backgroundColor': 'black'

                                                          },
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }
                                                ],
                
                                            #added 
                                            #      style_table={
                                            #     'height': '200px',
                                            #     'overflowY': 'scroll',
                                            # },
                                            # style_cell={'textAlign': 'center',
                                            #             'font_family': 'cursive',
                                            #             'font_size': '18px',
                                            #             'color': 'blue'
                                            #             },
                                            # style_header={'fontWeight': 'bold',
                                            #               'font_size': '20px',
                                            #               'color': 'red',
                                            #               'backgroundColor': 'White'

                                            #               },
                                                          ),
                                                  width={"size": 9, "offset": 1})
                                          ]
                    ),
                    ],style={'padding':'4px'}),
                        
          #District Dropdown  


        html.Div([             
                        
       
      # Map Radio Button
      dbc.FormGroup(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            options=[
                {'label': 'Production', 'value': 'first'},
                {'label': 'Area', 'value': 'second'},
                {'label': 'Productivity', 'value': 'third'},

            ],
            value='second',
            id="radio-items1",
            inline=True,
            switch=True,
        ),
    ]
    ),
      
     
      #Map Show
    
        dbc.Row([
            dbc.Col(
            
        html.Iframe(id='map', srcDoc=open('D:/Dash_Arnab/Productivity app/assests/plot_data1.html', 'r').read(), width='100%', height='600'),
       width={"size": 9, "offset": 1} ),]),
        ]),
    # html.Div([
    #     dbc.Row([
        
    #     dbc.Col(dbc.Alert("Pareto Chart",color="info"),width={"size": 9, "offset": 1}),

    #     ])
    #     ]),
    html.Div([
        dbc.Row(
                       
                dbc.Col(
                    html.Div(
                        dbc.FormGroup(
                            [
                                dbc.Label("Choose one"),
                                dbc.RadioItems(
                                    options=[
                                        {'label': 'Production', 'value': 'first'},
                                        {'label': 'Area', 'value': 'second'},
                

                            ],
                            value='second',
                            id="radio",
                            inline=True,
                            switch=True,
                            ),
                            ]
                            ),
                   ),align="end"
            ))
        ]),
    html.Div([
        dbc.Row([
        
            
            dbc.Col(dcc.Graph(id='pareto'),width={"size": 10, "offset": 1}),
        
        ]),
    
    ]),
    
    ]),



#2nd layout it is state-wise 

layout2 = html.Div([
    
     #Heading Cols           
    dbc.Row(
                [
     dbc.Col(
        dbc.Alert(html.H6("Select a Year",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),
    
      dbc.Col(
        dbc.Alert(html.H6("Select The Crop",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),  
      dbc.Col(
        dbc.Alert(html.H6("Select The Season",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=4),
      
              ]
        ),
      # Dropdown cols design
    html.Div([         
    dbc.Row(
                [
     dbc.Col(
     dcc.Dropdown(
             id="dd1",
    options=[
        {'label':i, 'value':i} for i in crop_year
    ],
    placeholder="Select a year",
     value=2013,
    style={'color':'red'},
    ),width=4),
    
    dbc.Col(
     dcc.Dropdown(
             id="dd2",
    options=[
        {'label':i, 'value':i} for i in crops
    ],
    placeholder="Select The Crops",
     value="Rice",
    style={'color':'blue'},
    ),width=4),
    
    dbc.Col(
     dcc.Dropdown(
             id="dd3",
    options=[
        {'label':i, 'value':i} for i in crop_season
    ],
    placeholder="Select The Season",
     value='Kharif     ',
    style={'color':'red'},
    ),width=4),
    
           
     ]),
           ],style={'padding':'4px'}),
           
     #Crop Table   
     
     html.Div([
    dbc.Row(
                        [
                                dbc.Col( dbc.Alert(
                                        html.H5("SUMMARY",style={"text-align":"center"},className="alert-heading"),color="info"), width={"size": 9, "offset": 1}),
                
            
                        ]
                        ),
                 dbc.Row(
                         [
                                 
                                 dbc.Col(
                                         
                                         dash_table.DataTable(
                                                 id='table',
                
                                                 data=[],
                                                 style_table={
                                                'height': '250px',
                                                'overflowY': 'scroll',
                                            },
                                            style_cell={'textAlign': 'center',
                                                        'font_family': 'cursive',
                                                        'font_size': '18px',
                                                        },
                                            style_header={'fontWeight': 'bold',
                                                          'font_size': '20px',
                                                          'color': 'white',
                                                          'backgroundColor': 'black'

                                                          },
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }
                                                ],
                
                                            #added 
                                            #      style_table={
                                            #     'height': '200px',
                                            #     'overflowY': 'scroll',
                                            # },
                                            # style_cell={'textAlign': 'center',
                                            #             'font_family': 'cursive',
                                            #             'font_size': '18px',
                                            #             'color': 'blue'
                                            #             },
                                            # style_header={'fontWeight': 'bold',
                                            #               'font_size': '20px',
                                            #               'color': 'red',
                                            #               'backgroundColor': 'White'

                                            #               },
                                                          ),
                                                 width={"size": 9, "offset": 1})
                                         ]
                    ),
                    ],style={'padding':'4px'}),
                        
         #District Dropdown  


        html.Div([             
                        
        dbc.Row(
                [
     dbc.Col(
        dbc.Alert(html.H6("Select a State",style={"text-align":"center"},className="alert-heading"),color="light"),
          width=3),
        ]),                 
                        
                        
        html.Div([         
    dbc.Row(
                [
     dbc.Col(
     dcc.Dropdown(
             id="dd_1",
    options=[
        
    ],
    placeholder="Select A State",
     #value="",
    style={'color':'red'},
    ),width=3),
    ])
    ]),
     ],style={'padding':'4px'}),
     
     
     #District Table
     
     
     html.Div([
    dbc.Row(
                        [
                                dbc.Col( dbc.Alert(
                                        html.H5("State Wise Summary",style={"text-align":"center"},className="alert-heading"),color="info"), width={"size": 9, "offset": 1}),
                                        
            
                        ]
                        ),
                 dbc.Row(
                         [
                                 
                                 dbc.Col(
                                         
                                         dash_table.DataTable(
                                                 id='table1',
                
                                                 data=[],
                                                 
                                                 style_table={
                                                'height': '250px',
                                                'overflowY': 'scroll',
                                            },
                                            style_cell={'textAlign': 'center',
                                                        'font_family': 'cursive',
                                                        'font_size': '18px',
                                                        },
                                            style_header={'fontWeight': 'bold',
                                                          'font_size': '20px',
                                                          'color': 'white',
                                                          'backgroundColor': 'black'

                                                          },
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }
                                                ],
                                            
                                            
                                                          ),
                                                 width={"size": 9, "offset": 1})
                                         ]
                    ),
                    ],style={'padding':'4px'}),
     
     # Map Radio Button
     dbc.FormGroup(
    [
        dbc.Label("Choose one"),
        dbc.RadioItems(
            options=[
                {'label': 'Production', 'value': 'first'},
                {'label': 'Area', 'value': 'second'},
                {'label': 'Productivity', 'value': 'third'},

            ],
            value='second',
            id="radio-items2",
            inline=True,
            switch=True,
        ),
    ]
    ),
     
     
     #Map Show
    # html.Div([
    #     dbc.Row([dbc.Col(dbc.Alert("Map View",color="info"),width={"size": 9, "offset": 1}),
    #         ]),
        dbc.Row([
            dbc.Col(
        html.Iframe(id='map1', srcDoc=open('D:/Dash_Arnab/Productivity app/assests/plot_data1.html', 'r').read(), width='100%', height='600'),
        width={"size": 9, "offset": 1}),
        ]),
        
    html.Div([dbc.Row([
        
        dbc.Col(dbc.Alert("Pareto Chart",color="info"),width=6),
        dbc.Col(dbc.Alert("State Wise Productivity Distribution",color="info"),width=6)
        ])
        ]),
    html.Div([
        dbc.Row(
                       
                dbc.Col(
                    html.Div(
                        dbc.FormGroup(
                            [
                                dbc.Label("Choose one"),
                                dbc.RadioItems(
                                    options=[
                                        {'label': 'Production', 'value': 'first'},
                                        {'label': 'Area', 'value': 'second'},
                                        

                            ],
                            value='first',
                            id="radio",
                            inline=True,
                            switch=True,
                                ),
                            ]
                            ),
                    ),align="end"
            ))
        ]),
    html.Div([
        dbc.Row([
        
            
            dbc.Col(dcc.Graph(id='pareto'),width=6),
            dbc.Col(dcc.Graph(id='box'),width=6)
        ]),
    
    ]),
    
    
    ])



#Radio Button Callback
@app.callback(Output('div', 'children'),
    [Input('radio-items', 'value')])
def render_charts(value):
    
    if value == 'first':
        
        
        return layout2
    elif value == 'second': 
        
        
        return layout1
    
                        
#crop table callback                        
@app.callback([Output('table','data'),Output('table', 'columns')],
               [Input('dd1','value'),Input('dd2','value'),Input('dd3','value')])

def table_update(dd1,dd2,dd3):
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    #crop_df_req= crop[(crop['Season'] == dd3)]
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    #crop_df_req= crop[(crop.Crop_Year == dd1 & crop.Crop == dd2 & crop.Season == dd3)]
    states=len(crop_df_req.State_Name.unique())
    districts = len(crop_df_req.District_Name.unique())   
    area = crop_df_req.Area.sum(skipna=True)
    area = "{:,}".format(area)    
    production = crop_df_req.Production.sum(skipna=True) 
    production = "{:,}".format(production)
    productivity = round(crop_df_req.Productivity.mean(),2)
    columns=[{'name': "Crop Summary", 'id':0},
             {'name': "Values", 'id': 1},
            ]
    
    
    col=("States under cultivation","No.of Districts under cultivation", "Total Area under cultivation (sq km)", "Total Production (tonnes)", "Average Productivity")
    req_cols=pd.Series(col).reset_index()
    value=[states,districts, area, production, productivity]
    req_vals=pd.Series(value).reset_index()
    data=req_cols.merge(req_vals,on='index')
    data=data.drop('index',axis=1)
    
    
    return data.values,columns   

@app.callback(Output('dd_1','options'),
               [Input('dd1','value'),Input('dd2','value'),Input('dd3','value')]) 


def dropdown_update(dd1,dd2,dd3):
    
    
    #crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    #crop_df_req= crop[(crop['Crop'] == dd2)]
    #crop_df_req= crop[(crop['Season'] == dd3)]
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    dropdown_req= crop_df_req["State_Name"].unique().tolist()
    
    return [{'label':i, 'value':i} for i in dropdown_req]



#district table callback
@app.callback([Output('table1','data'),Output('table1', 'columns')],
               [Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),Input('dd_1','value')]) 

def state_update(dd1,dd2,dd3,sel_st):
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    
    #crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    #crop_df_req= crop[(crop['Crop'] == dd2)]
    #crop_df_req= crop[(crop['Season'] == dd3)]
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    crop_df_req1 = crop_df_req[(crop_df_req.State_Name == sel_st)]
    nd = len(crop_df_req1.District.unique())
    sl_st=sel_st
    #ndt = ("The number of districts under cultivation for the state of ", sel_st, " are ", nd)
    q1 = round(crop_df_req1.Productivity.quantile(0.25),2)
    med = round(crop_df_req1.Productivity.median(skipna=True),2)
    q3 = round(crop_df_req1.Productivity.quantile(0.75),2)
    avg_pro = round(crop_df_req1.Productivity.mean(skipna=True),2)
    min_pro = round(crop_df_req1.Productivity.min(skipna=True),2)
    max_pro = round(crop_df_req1.Productivity.max(skipna=True),2)
    std_pro = round(crop_df_req1.Productivity.std(skipna=True),2)
    columns1=[{'name': "Measures", 'id':0},
             {'name': "District Summary", 'id': 1},
            ]
    
    
    dist_summ=("Selected State","No of Districts for Selected State","Minimum", "First Quartile", "Median", "Third Quartile", "Average", "Maximum","Standard Deviation")
    req_cols1=pd.Series(dist_summ).reset_index()
    values1=[sl_st,nd,min_pro,q1,med,q3,avg_pro,max_pro,std_pro]
    req_vals1=pd.Series(values1).reset_index()
    data1=req_cols1.merge(req_vals1,on='index')
    data1=data1.drop('index',axis=1)
    
    #if crop_df_req1 is not None:
    return data1.values,columns1,
    

#Map Callback
@app.callback(Output(component_id='map', component_property='srcDoc'),[Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),Input('radio-items1','value'),])

def folium_callback(dd1,dd2,dd3,val):
    
    print(dd1,dd2,dd3)
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    #crop_df_req=crop_df[(crop_df['Crop_Year'] == crop_year[15])  & (crop_df['Season'] == crop_season[0]) & (crop_df['Crop'] == crops[0]) ]
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    #making percentile column
    crop_df_req["per_prdtn"]=round(crop_df_req.Production.rank(pct=True)*100)
    crop_df_req["per_area"]=round(crop_df_req.Area.rank(pct=True)*100)
    crop_df_req["per_prdtvty"]=round(crop_df_req.Productivity.rank(pct=True)*100)


    
   # print(crop_df_req)
   #for Prodution Map Data
    india_dist = nil
    req_df_map =crop_df_req.filter(["State_Name","District","Production","per_prdtn"])
    new_map_data=pd.merge(req_df_map,
                      india_dist,
                      left_on=['State_Name','District'],
                      right_on=['NAME_1','NAME_2'],
                      how='outer')

    new_map_data=new_map_data[['NAME_1','NAME_2', 'GID_2', 'Production',"per_prdtn"]]
    new_map_data=new_map_data.dropna(subset=["GID_2"])
    x_map=nil1.centroid.x.mean()
    y_map=nil1.centroid.y.mean()
    print(x_map,y_map)

    nilpop=nil2.merge(new_map_data,on="GID_2")
    
    #for Area Map Data
    req_df_map1 =crop_df_req.filter(["State_Name","District","Area","per_area"])
    new_map_data1=pd.merge(req_df_map1,
                      india_dist,
                      left_on=['State_Name','District'],
                      right_on=['NAME_1','NAME_2'],
                      how='outer')

    new_map_data1=new_map_data1[['NAME_1','NAME_2', 'GID_2', 'Area',"per_area"]]
    new_map_data1=new_map_data1.dropna(subset=["GID_2"])
    x_map=nil1.centroid.x.mean()
    y_map=nil1.centroid.y.mean()
    print(x_map,y_map)

    nilpop1=nil2.merge(new_map_data1,on="GID_2")
    
    #for Productivity Map Data
    req_df_map2 =crop_df_req.filter(["State_Name","District",'Productivity',"per_prdtvty"])
    new_map_data2=pd.merge(req_df_map2,
                      india_dist,
                      left_on=['State_Name','District'],
                      right_on=['NAME_1','NAME_2'],
                      how='outer')

    new_map_data2=new_map_data2[['NAME_1','NAME_2', 'GID_2', 'Productivity',"per_prdtvty"]]
    new_map_data2=new_map_data2.dropna(subset=["GID_2"])
    x_map=nil1.centroid.x.mean()
    y_map=nil1.centroid.y.mean()
    print(x_map,y_map)

    nilpop2=nil2.merge(new_map_data2,on="GID_2")
    #print(nilpop2)
    
    
    
    
    #print(req_df_map)
    
    #india_dist.columns.values[0:2]=['State_Name', 'District']
    
    
    
        
    
    
    if val == 'first':
    
            
        
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,tiles=None)
    #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop.Production.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        #myscale=(nilpop.Production.rank(pct=True)).tolist()
        folium.Choropleth(
        geo_data=nilpop,
        name='Choropleth',
        data=nilpop,
        columns=['GID_2','Production'],
        key_on="feature.properties.GID_2",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        nan_fill_color='purple',
        legend_name='Production capacity in tonnes',
        smooth_factor=0
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            nilpop,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['NAME_2','per_prdtn',"Production"],
                aliases=['District Name: ','Production in tonnes(percentile): ','Production(In Tonnes)'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)


        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data2.html')


        
        return open('D:/Dash_Arnab/Productivity app/assests/plot_data2.html', 'r').read()

    elif val == 'second':
        


    
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,tiles=None)
#folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop1.Area.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        folium.Choropleth(
        geo_data=nilpop1,
        name='Choropleth',
        data=nilpop1,
        columns=['GID_2','Area'],
        key_on="feature.properties.GID_2",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        nan_fill_color='purple',
        legend_name='Area capacity in SqKm',
        smooth_factor=0
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            nilpop1,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
            fields=['NAME_2','per_area','Area'],
            aliases=['District Name: ','Percentile : ','Area(Hecters)'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
            )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)


        #mymap.save('D:/Dash_Arnab/Productivity app/assets/plot_data3.html')
        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data3.html')



        return open('D:/Dash_Arnab/Productivity app/assests/plot_data3.html', 'r').read()
        
        
        
    elif val == 'third':
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,position='relative', tiles=None)
        #folium.TileLayer('Open',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop2.Productivity.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        folium.Choropleth(
        geo_data=nilpop2,
        name='Choropleth',
        data=nilpop2,
        columns=['GID_2','Productivity'],
        key_on="feature.properties.GID_2",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Productivity',
        smooth_factor=0,
        nan_fill_color='purple',
        reset=True,
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            nilpop2,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['NAME_2','per_prdtvty','Productivity'],
                aliases=['District Name: ','Productivity(percentile) : ','Productivity'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)
        
        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data4.html')



        return open('D:/Dash_Arnab/Productivity app/assests/plot_data4.html', 'r').read()
        


        #mymap.save('D:/Dash_Arnab/Productivity app/assets/plot_data4.html')


        #return open('D:/Dash_Arnab/Productivity app/assets/plot_data4.html', 'r').read()


#Box-Plot Callback        
@app.callback(Output('box','figure'),
              [Input('dd1','value'),Input('dd2','value'),Input('dd3','value')]) 

def update_boxplot(dd1,dd2,dd3):
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    
    crop_df_req=crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    fig = px.box(crop_df_req,y='Productivity',color='State_Name')
    fig.update_traces(quartilemethod="exclusive",alignmentgroup=True)
    fig.update_layout(xaxis_title="<b>State</b>",yaxis_title="<b>Productivity</b>",showlegend=True)
    
    return fig

#Pareto-chart
@app.callback(Output('pareto','figure'),
              [Input('radio','value'),Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),]) 

def update_pareto(val,dd1,dd2,dd3):
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    crop_df_dup=crop_df_req[crop_df_req["District"].duplicated()]
        
    if val == "first":
        
        if len(crop_df_dup.District) == 0:
            
            crop_df_req_new = crop_df_req
            
        else:
            crop_df_dup["Dup"] = "1"
            new=crop_df_dup["Dup"].copy()
            crop_df_dup["District"]= crop_df_dup["District"].str.cat(new,sep=None) 
            crop_df_dup=crop_df_dup.drop(["Dup"],axis=1)
            crop_df_not_dup = crop_df_req.drop_duplicates(subset ="District",keep="first")
            crop_df_req_new = pd.concat([crop_df_not_dup,crop_df_dup])
    
        crop_df_req1=crop_df_req_new[["District","Production"]]
        crop_df_req1 = crop_df_req1.sort_values(by=["Production"],ascending=False)
        crop_df_req1["cumprod"]= crop_df_req1.Production.cumsum()
        crop_df_req1 = crop_df_req1.dropna(subset=["Production"])
        crop_df_req1["cumproper"] = ((crop_df_req1["cumprod"])/(crop_df_req1.Production).sum())*100
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=crop_df_req1.District, y=crop_df_req1.Production),secondary_y=False)
        fig.add_trace(go.Scatter(x=crop_df_req1.District, y=crop_df_req1.cumproper),secondary_y=True,)
        fig.update_layout(title="Production(tonnes)-District Wise Pareto",xaxis_title="<b>District</b>",yaxis_title="<b>Production</b>",showlegend=False)

        fig.update_yaxes(title_text="<b>Cumulative Production(%)</b> ", secondary_y=True)
        return fig
    
    elif val == "second":

        
        #crop_df_dup=crop_df_req[crop_df_req["District"].duplicated()]

        
        
        if len(crop_df_dup.District) == 0:
            
            crop_df_req_new = crop_df_req
            
        else:
            crop_df_dup["Dup"] = "1"
            new=crop_df_dup["Dup"].copy()
            crop_df_dup["District"]= crop_df_dup["District"].str.cat(new,sep=None) 
            crop_df_dup=crop_df_dup.drop(["Dup"],axis=1)
            crop_df_not_dup = crop_df_req.drop_duplicates(subset ="District",keep="first")
            crop_df_req_new = pd.concat([crop_df_not_dup,crop_df_dup])
    
        crop_df_req1=crop_df_req_new[["District","Area"]]
        crop_df_req1 = crop_df_req1.sort_values(by=["Area"],ascending=False)
        crop_df_req1["cumprod"]= crop_df_req1.Area.cumsum()
        crop_df_req1 = crop_df_req1.dropna(subset=["Area"])
        crop_df_req1["cumproper"] = ((crop_df_req1["cumprod"])/(crop_df_req1.Area).sum())*100
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=crop_df_req1.District, y=crop_df_req1.Area),secondary_y=False)
        fig.add_trace(go.Scatter(x=crop_df_req1.District, y=crop_df_req1.cumproper),secondary_y=True,)
        fig.update_yaxes(title_text="<b>Cumulative Percentage(%)</b> ", secondary_y=True)
        fig.update_layout(title="Area(sqKm)-District Wise Pareto",xaxis_title="<b>District</b>",yaxis_title="<b>Area</b>",showlegend=False)

        return fig
        
    
#Map Callback State
@app.callback(Output(component_id='map1', component_property='srcDoc'),[Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),Input('radio-items2','value'),])

def folium1_callback(dd1,dd2,dd3,val):
    
    print(dd1,dd2,dd3)
    crop_df_req= crop[(crop['Crop_Year'] == dd1)]
    crop_df_req= crop[(crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    
    #crop_df_req=crop_df[(crop_df['Crop_Year'] == crop_year[15])  & (crop_df['Season'] == crop_season[0]) & (crop_df['Crop'] == crops[0]) ]
    crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
    #crop_df_req["percentile"]=crop_df_req.rank(pct=True)
    crop_df_req["per_prdtn"]=round(crop_df_req.Production.rank(pct=True)*100)
    crop_df_req["per_area"]=round(crop_df_req.Area.rank(pct=True)*100)
    crop_df_req["per_prdtvty"]=round(crop_df_req.Productivity.rank(pct=True)*100)


    ind_state=ind1
    crs = {'init': 'epsg:4326'}
   # print(crop_df_req)
   #for Prodution Map Data
    new_map_data=crop_df_req.filter(["State_Name","District","Production","per_prdtn"])
    new_map_data=pd.merge(new_map_data,
                      ind_state,
                      left_on=['State_Name'],
                      right_on=['NAME_1'],
                      how='outer')
    new_map_data=new_map_data.dropna(subset=["GID_1"])
    new_map_data=new_map_data.groupby("NAME_1")["Production","per_prdtn"].mean().reset_index()
    new_map_data["per_prdtn"]=round(new_map_data.per_prdtn)
    map_req_df=new_map_data.merge(state,on="NAME_1")
    
    map_req_df=gpd.GeoDataFrame( map_req_df,crs=crs,geometry='geometry')

    x_map=map_req_df.centroid.x.mean()
    y_map=map_req_df.centroid.y.mean()
    print(x_map,y_map)
    


    
    
    #for Area Map Data
    new_map_data1=crop_df_req.filter(["State_Name","District","Area","per_area"])
    new_map_data1=pd.merge(new_map_data1,
                      ind_state,
                      left_on=['State_Name'],
                      right_on=['NAME_1'],
                      how='outer')
    new_map_data1=new_map_data1.dropna(subset=["GID_1"])
    new_map_data1=new_map_data1.groupby("NAME_1")["Area","per_area"].mean().reset_index()
    new_map_data1["per_area"]=round(new_map_data1.per_area)
    
    map_req_df1=new_map_data1.merge(state,on="NAME_1")
    map_req_df1=gpd.GeoDataFrame(map_req_df1,crs=crs, geometry='geometry')

    x_map=map_req_df1.centroid.x.mean()
    y_map=map_req_df1.centroid.y.mean()
    print(x_map,y_map)
    
    
    #for Productivity Map Data
    new_map_data2=crop_df_req.filter(["State_Name","District","Productivity","per_prdtvty"])
    new_map_data2=pd.merge(new_map_data2,
                      ind_state,
                      left_on=['State_Name'],
                      right_on=['NAME_1'],
                      how='outer')
    new_map_data2=new_map_data2.dropna(subset=["GID_1"])
    new_map_data2=new_map_data2.groupby("NAME_1")["Productivity","per_prdtvty"].mean().reset_index()
    new_map_data2["per_prdtvty"]=round(new_map_data2.per_prdtvty)
    
    
    map_req_df2=new_map_data2.merge(state,on="NAME_1")
    map_req_df2=gpd.GeoDataFrame(map_req_df2,crs=crs, geometry='geometry')

    x_map=map_req_df2.centroid.x.mean()
    y_map=map_req_df2.centroid.y.mean()
    print(x_map,y_map)
    #print(nilpop2)
    
    
    
    
    #print(req_df_map)
    
    #india_dist.columns.values[0:2]=['State_Name', 'District']
    
    
    
        
    
    
    if val == 'first':
    
            
        
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,tiles=None)
    #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop.Production.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        folium.Choropleth(
        geo_data=map_req_df,
        name='Choropleth',
        data=map_req_df,
        columns=['GID_1','Production'],
        key_on="feature.properties.GID_1",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        nan_fill_color='purple',
        legend_name='Production capacity in tonnes',
        smooth_factor=0
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            map_req_df,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['NAME_1','per_prdtn','Production'],
                aliases=['District Name: ','Production in tonnes(percentile) : ','Production(Tonnes)'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)
        
        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data5.html')



        return open('D:/Dash_Arnab/Productivity app/assests/plot_data5.html', 'r').read()
        


        #mymap.save('D:/Dash_Arnab/Productivity app/assets/plot_data5.html')


        
        #return open('D:/Dash_Arnab/Productivity app/assets/plot_data5.html', 'r').read()

    elif val == 'second':
        


    
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,tiles=None)
#folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop1.Area.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        folium.Choropleth(
        geo_data=map_req_df1,
        name='Choropleth',
        data=map_req_df1,
        columns=['GID_1','Area'],
        key_on="feature.properties.GID_1",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        nan_fill_color='purple',
        legend_name='Area capacity in SqKm',
        smooth_factor=0
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            map_req_df1,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
            fields=['NAME_1','per_area','Area'],
            aliases=['District Name: ','Percentile : ','Area(Hectres)'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
            )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)
        
        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data6.html')



        return open('D:/Dash_Arnab/Productivity app/assests/plot_data6.html', 'r').read()
        
        


        #mymap.save('D:/Dash_Arnab/Productivity app/assets/plot_data6.html')


        #return open('D:/Dash_Arnab/Productivity app/assets/plot_data6.html', 'r').read()
        
        
        
    elif val == 'third':
        
        mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
               zoom_start=4,position='relative', tiles=None)
        #folium.TileLayer('Open',name="Light Map",control=False).add_to(mymap)



        #myscale = (nilpop2.Productivity.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        folium.Choropleth(
        geo_data=map_req_df2,
        name='Choropleth',
        data=map_req_df2,
        columns=['GID_1','Productivity'],
        key_on="feature.properties.GID_1",
        fill_color="YlOrBr",
        #threshold_scale=myscale,
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='Productivity',
        smooth_factor=0,
        nan_fill_color='purple',
        reset=True,
        ).add_to(mymap)

        style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
        NIL = folium.features.GeoJson(
            map_req_df2,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['NAME_1','per_prdtvty','Productivity'],
                aliases=['District Name: ','Productivity(Percentile) : ','Productivity'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        mymap.add_child(NIL)
        mymap.keep_in_front(NIL)
        folium.LayerControl().add_to(mymap)
        
        mymap.save('D:/Dash_Arnab/Productivity app/assests/plot_data7.html')



        return open('D:/Dash_Arnab/Productivity app/assests/plot_data7.html', 'r').read()
        


        #mymap.save('D:/Dash_Arnab/Productivity app/assets/plot_data7.html')


        #return open('D:/Dash_Arnab/Productivity app/assets/plot_data7.html', 'r').read()

       
    

    
    #2002 Arecanut Kharif  