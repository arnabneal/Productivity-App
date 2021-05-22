# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:19:04 2020

@author: Arnab Basak
"""

# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output

# from app import app

# layout = html.Div([
#     html.H3('App 1'),
#     dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'NYC', 'MTL', 'LA'
#             ]
#         ]
#     ),
#     html.Div(id='app-1-display-value'),
#     dcc.Link('Go to App 2', href='/apps/app2')
# ])


# @app.callback(
#     Output('app-1-display-value', 'children'),
#     [Input('app-1-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
# # Import required libraries
# import dash
import dash_core_components as dcc
import dash_html_components as html
# import geopandas as gpd
# import folium
# import branca.colormap as cm
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
# import pathlib
import dash_bootstrap_components as dbc
# import dash_table
# from statistics import stdev 
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
#import plotly.offline as pyo
from app import app


# # get relative data folder
# #PATH = pathlib.Path(__file__).parent
# #DATA_PATH = PATH.joinpath("data").resolve()




# # Load data
crop_df = pd.read_csv("D:\Dash_Arnab\Productivity app\Data\crop_data.csv", low_memory=False)
crop_df["Productivity"]= crop_df.Production/crop_df.Area
crop_df=crop_df[["District","Crop_Year","Crop","Season","Production","Productivity","Area"]]
all=crop_df.groupby(['Crop_Year','Season','Crop'])["Production","Productivity","Area"].mean().reset_index()
all["District"]='All'
crop_df=pd.concat([crop_df, all],ignore_index=True)



#crop_time=crop_df[(crop_df['District'] == "All") & (crop_df['Crop'] == "Rice") & (crop_df['Season'] == "Kharif     ")]
#crop_time=crop_time.dropna()


#graph=px.line(crop_time,x="Crop_Year",y='Productivity')
#pyo.plot(graph)

#crop_season=crop_df['Season'].unique().tolist()
#print(len(crop_season))
#crops=crop_df['Crop'].unique().tolist()
#print(len(crops))
main_dict={k: g["Crop"].tolist() for k,g in crop_df.groupby("District")}
names = list(main_dict.keys())
nestedOptions = main_dict[names[11]]

#dist=crop_df['District'].sort_values().dropna().unique().tolist()

# #app=dash.Dash().
# # Create app layout
layout = html.Div(
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
      value="Rice",
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
      value='Kharif     ',
    style={'color':'red'},
    ),width=3),
    
           
      ]),
            ],style={'padding':'4px'}),
           
      #Crop Table   
     
      html.Div([
    dbc.Row(
                        [
                                dbc.Col( dbc.Alert(
                                        html.H5("District Wise Time Analysis",style={"text-align":"center"},className="alert-heading"),color="info"), width=12),
                
            
                        ]
                        ),
                        
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
    
   
    html.Div([
        dbc.Row([
        
            
            dbc.Col(dcc.Graph(id='time'),width=12),
        
        ]),
    
    ]),
    
    ]),
    ])
      ])



@app.callback([Output('tdd2','options'),Output('tdd3','options')],[Input('tdd1','value')])

def drp_update(tdd1):
    global crop_df
    #crop_df= crop_df[(crop_df["District"] == tdd1)]
    
    
    crop_dd=crop_df[["District","Crop","Season"]]
    
    main_dict={k: g["Crop"].tolist() for k,g in crop_dd.groupby("District")}
    #names = list(main_dict.keys())
    #crops = main_dict[names[0]]
    
    main_dict1={k: g["Season"].unique().tolist() for k,g in crop_dd.groupby("District")}
    #names1 = list(main_dict.keys())
    #crop_season= main_dict1[names1[0]]
    
    
    
    return [{'label':i, 'value':i} for i in main_dict[tdd1]],[{'label':j, 'value':j} for j in main_dict1[tdd1]]

    
                        
# #crop table callback                        

@app.callback(Output('time','figure'),
                [Input('radio-items1','value'),Input('tdd1','value'),Input('tdd2','value'),Input('tdd3','value')]) 


def time_update(sel,tdd1,tdd2,tdd3):
        crop_time=crop_df[crop_df["District"]== tdd1]
        print(tdd1)
        crop_time=crop_df[(crop_df['Crop'] == tdd2) & (crop_df['Season'] == tdd3)]
        
        crop_time=crop_df[(crop_df['District'] == tdd1) & (crop_df['Crop'] == tdd2) & (crop_df['Season'] == tdd3)]
        crop_time=crop_time.dropna()
        
        if sel == 'first':
            graph=px.line(crop_time,x="Crop_Year",y='Production')
            #graph.update_layout(xaxis_title="Year")
            return graph
        elif sel == 'second':
            graph1=px.line(crop_time,x="Crop_Year",y='Area')
            graph1.update_layout(xaxis_title="Year")
            return graph1
        elif sel == 'third':
            graph2=px.line(crop_time,x="Crop_Year",y='Productivity')
            graph2.update_layout(xaxis_title="Year")
            return graph2
    
    

   


# #Map Callback
# @app.callback(Output(component_id='map', component_property='srcDoc'),[Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),Input('radio-items','value'),])

# def folium_callback(dd1,dd2,dd3,val):
    
#     print(dd1,dd2,dd3)
#     #crop_df_req=crop_df[(crop_df['Crop_Year'] == crop_year[15])  & (crop_df['Season'] == crop_season[0]) & (crop_df['Crop'] == crops[0]) ]
#     crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
#    # print(crop_df_req)
#    #for Prodution Map Data
#     india_dist = nil
#     req_df_map =crop_df_req.filter(["State_Name","District","Production"])
#     new_map_data=pd.merge(req_df_map,
#                       india_dist,
#                       left_on=['State_Name','District'],
#                       right_on=['NAME_1','NAME_2'],
#                       how='outer')

#     new_map_data=new_map_data[['GID_2','State_Name', 'District', 'Production']]
#     x_map=nil1.centroid.x.mean()
#     y_map=nil1.centroid.y.mean()
#     print(x_map,y_map)

#     nilpop=nil2.merge(new_map_data,on="GID_2")
    
#     #for Area Map Data
#     req_df_map1 =crop_df_req.filter(["State_Name","District","Area"])
#     new_map_data1=pd.merge(req_df_map1,
#                       india_dist,
#                       left_on=['State_Name','District'],
#                       right_on=['NAME_1','NAME_2'],
#                       how='outer')

#     new_map_data1=new_map_data1[['GID_2','State_Name', 'District', 'Area']]
#     x_map=nil1.centroid.x.mean()
#     y_map=nil1.centroid.y.mean()
#     print(x_map,y_map)

#     nilpop1=nil2.merge(new_map_data1,on="GID_2")
    
#     #for Productivity Map Data
#     req_df_map2 =crop_df_req.filter(["State_Name","District",'Productivity'])
#     new_map_data2=pd.merge(req_df_map2,
#                       india_dist,
#                       left_on=['State_Name','District'],
#                       right_on=['NAME_1','NAME_2'],
#                       how='outer')

#     new_map_data2=new_map_data2[['GID_2','State_Name', 'District', 'Productivity']]
#     x_map=nil1.centroid.x.mean()
#     y_map=nil1.centroid.y.mean()
#     print(x_map,y_map)

#     nilpop2=nil2.merge(new_map_data2,on="GID_2")
#     #print(nilpop2)
    
    
    
    
#     #print(req_df_map)
    
#     #india_dist.columns.values[0:2]=['State_Name', 'District']
    
    
    
        
    
    
#     if val == 'first':
    
            
        
        
#         mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
#                zoom_start=4,tiles=None)
#     #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



#         #myscale = (nilpop.Production.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
#         folium.Choropleth(
#         geo_data=nilpop,
#         name='Choropleth',
#         data=nilpop,
#         columns=['GID_2','Production'],
#         key_on="feature.properties.GID_2",
#         fill_color="YlOrBr",
#         #threshold_scale=myscale,
#         fill_opacity=1,
#         line_opacity=0.2,
#         nan_fill_color='purple',
#         legend_name='Production capacity in tonnes',
#         smooth_factor=0
#         ).add_to(mymap)

#         style_function = lambda x: {'fillColor': '#ffffff', 
#                             'color':'#000000', 
#                             'fillOpacity': 0.1, 
#                             'weight': 0.1}
#         highlight_function = lambda x: {'fillColor': '#000000', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.50, 
#                                 'weight': 0.1}
#         NIL = folium.features.GeoJson(
#             nilpop,
#             style_function=style_function, 
#             control=False,
#             highlight_function=highlight_function, 
#             tooltip=folium.features.GeoJsonTooltip(
#                 fields=['District','Production'],
#                 aliases=['District Name: ','Production in tonnes : '],
#                 style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#                 )
#             )
#         mymap.add_child(NIL)
#         mymap.keep_in_front(NIL)
#         folium.LayerControl().add_to(mymap)


#         mymap.save('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data2.html')


        
#         return open('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data2.html', 'r').read()

#     elif val == 'second':
        


    
        
#         mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
#                zoom_start=4,tiles=None)
# #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)



#         #myscale = (nilpop1.Area.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
#         folium.Choropleth(
#         geo_data=nilpop1,
#         name='Choropleth',
#         data=nilpop1,
#         columns=['GID_2','Area'],
#         key_on="feature.properties.GID_2",
#         fill_color="YlOrBr",
#         #threshold_scale=myscale,
#         fill_opacity=1,
#         line_opacity=0.2,
#         nan_fill_color='purple',
#         legend_name='Area capacity in SqKm',
#         smooth_factor=0
#         ).add_to(mymap)

#         style_function = lambda x: {'fillColor': '#ffffff', 
#                             'color':'#000000', 
#                             'fillOpacity': 0.1, 
#                             'weight': 0.1}
#         highlight_function = lambda x: {'fillColor': '#000000', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.50, 
#                                 'weight': 0.1}
#         NIL = folium.features.GeoJson(
#             nilpop1,
#             style_function=style_function, 
#             control=False,
#             highlight_function=highlight_function, 
#             tooltip=folium.features.GeoJsonTooltip(
#             fields=['District','Area'],
#             aliases=['District Name: ','Area in tonnes : '],
#             style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#             )
#             )
#         mymap.add_child(NIL)
#         mymap.keep_in_front(NIL)
#         folium.LayerControl().add_to(mymap)


#         mymap.save('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data3.html')


#         return open('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data3.html', 'r').read()
        
        
        
#     elif val == 'third':
        
#         mymap = folium.Map(location=[y_map, x_map], min_zoom=4, max_zoom=6,
#                zoom_start=4,position='relative', tiles=None)
#         #folium.TileLayer('Open',name="Light Map",control=False).add_to(mymap)



#         #myscale = (nilpop2.Productivity.quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
#         folium.Choropleth(
#         geo_data=nilpop2,
#         name='Choropleth',
#         data=nilpop2,
#         columns=['GID_2','Productivity'],
#         key_on="feature.properties.GID_2",
#         fill_color="YlOrBr",
#         #threshold_scale=myscale,
#         fill_opacity=1,
#         line_opacity=0.2,
#         legend_name='Productivity',
#         smooth_factor=0,
#         nan_fill_color='purple',
#         reset=True,
#         ).add_to(mymap)

#         style_function = lambda x: {'fillColor': '#ffffff', 
#                             'color':'#000000', 
#                             'fillOpacity': 0.1, 
#                             'weight': 0.1}
#         highlight_function = lambda x: {'fillColor': '#000000', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.50, 
#                                 'weight': 0.1}
#         NIL = folium.features.GeoJson(
#             nilpop2,
#             style_function=style_function, 
#             control=False,
#             highlight_function=highlight_function, 
#             tooltip=folium.features.GeoJsonTooltip(
#                 fields=['District','Productivity'],
#                 aliases=['District Name: ','Productivity : '],
#         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#             )
#         )
#         mymap.add_child(NIL)
#         mymap.keep_in_front(NIL)
#         folium.LayerControl().add_to(mymap)


#         mymap.save('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data4.html')


#         return open('D:/Dash_Arnab/WB_GVT_DATA/WB_GVT_DATA/assets/plot_data4.html', 'r').read()

  

# #Pareto-chart
# @app.callback(Output('pareto','figure'),
#               [Input('radio','value'),Input('dd1','value'),Input('dd2','value'),Input('dd3','value'),]) 

# def update_pareto(val,dd1,dd2,dd3):
    
#     crop_df_req= crop[(crop['Crop_Year'] == dd1) & (crop['Crop'] == dd2) & (crop['Season'] == dd3)]
#     crop_df_dup=crop_df_req[crop_df_req["District"].duplicated()]
        
#     if val == "first":
        
#         if len(crop_df_dup.District) == 0:
            
#             crop_df_req_new = crop_df_req
            
#         else:
#             crop_df_dup["Dup"] = "1"
#             new=crop_df_dup["Dup"].copy()
#             crop_df_dup["District"]= crop_df_dup["District"].str.cat(new,sep=None) 
#             crop_df_dup=crop_df_dup.drop(["Dup"],axis=1)
#             crop_df_not_dup = crop_df_req.drop_duplicates(subset ="District",keep="first")
#             crop_df_req_new = pd.concat([crop_df_not_dup,crop_df_dup])
    
#         crop_df_req1=crop_df_req_new[["District","Production"]]
#         crop_df_req1 = crop_df_req1.sort_values(by=["Production"],ascending=False)
#         crop_df_req1["cumprod"]= crop_df_req1.Production.cumsum()
#         crop_df_req1 = crop_df_req1.dropna(subset=["Production"])
#         crop_df_req1["cumproper"] = ((crop_df_req1["cumprod"])/(crop_df_req1.Production).sum())*100
        
#         fig = make_subplots(specs=[[{"secondary_y": True}]])
#         fig.add_trace(go.Bar(x=crop_df_req1.District, y=crop_df_req1.Production),secondary_y=False)
#         fig.add_trace(go.Scatter(x=crop_df_req1.District, y=crop_df_req1.cumproper),secondary_y=True,)
#         fig.update_layout(title="Production(tonnes)-District Wise Pareto",xaxis_title="<b>District</b>",yaxis_title="<b>Production</b>",showlegend=False)

#         fig.update_yaxes(title_text="<b>Cumulative Production(%)</b> ", secondary_y=True)
#         return fig
    
#     elif val == "second":

        
#         #crop_df_dup=crop_df_req[crop_df_req["District"].duplicated()]

        
        
#         if len(crop_df_dup.District) == 0:
            
#             crop_df_req_new = crop_df_req
            
#         else:
#             crop_df_dup["Dup"] = "1"
#             new=crop_df_dup["Dup"].copy()
#             crop_df_dup["District"]= crop_df_dup["District"].str.cat(new,sep=None) 
#             crop_df_dup=crop_df_dup.drop(["Dup"],axis=1)
#             crop_df_not_dup = crop_df_req.drop_duplicates(subset ="District",keep="first")
#             crop_df_req_new = pd.concat([crop_df_not_dup,crop_df_dup])
    
#         crop_df_req1=crop_df_req_new[["District","Area"]]
#         crop_df_req1 = crop_df_req1.sort_values(by=["Area"],ascending=False)
#         crop_df_req1["cumprod"]= crop_df_req1.Area.cumsum()
#         crop_df_req1 = crop_df_req1.dropna(subset=["Area"])
#         crop_df_req1["cumproper"] = ((crop_df_req1["cumprod"])/(crop_df_req1.Area).sum())*100
        
#         fig = make_subplots(specs=[[{"secondary_y": True}]])
#         fig.add_trace(go.Bar(x=crop_df_req1.District, y=crop_df_req1.Area),secondary_y=False)
#         fig.add_trace(go.Scatter(x=crop_df_req1.District, y=crop_df_req1.cumproper),secondary_y=True,)
#         fig.update_yaxes(title_text="<b>Cumulative Percentage(%)</b> ", secondary_y=True)
#         fig.update_layout(title="Area(sqKm)-District Wise Pareto",xaxis_title="<b>District</b>",yaxis_title="<b>Area</b>",showlegend=False)

#         return fig
        
# if __name__=="__main__":
#     app.run_server()
            
    

    
    