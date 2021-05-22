# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:09:53 2020

@author: Arnab Basak
"""

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output ,State
import socket

from app import app
from apps import app1,app2
#from Tabs import app1,app1_1


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    #"background-color": "#4b7475",
    "background-color":"#f1f1f1"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

submenu_1 = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Agro Productivity Dashboard"),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3"), width="auto"
                ),
            ],
            className="my-1",
        ),
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Crop Production", href="/page-1/1"),
            #dbc.NavLink("Page 1.2", href="/page-1/2"),
        ],
        id="submenu-1-collapse",
    ),
]


sidebar = html.Div(
    [
        html.H3("Crop Production", className="display-5"),
        html.Hr(),
        html.P("AGRO PRODUCTIVITY DASHBOARD", className="lead"
        ),
        dbc.Nav(submenu_1, vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout =  html.Div([dcc.Location(id="url"), sidebar, content])
 #html.Div([
#     #common header
#      dbc.Row(
#                 [
#      dbc.Col(
#         dbc.Alert(html.H1("Crops Productivity Application",style={"text-align":"center"},className="alert-heading"),color="info"),
#           width=12),
     
#                 ]
#         ),
#      )],
        #sidebar Design
    


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1/1"]:
        #return html.P("This is the content of page 1.1!")
        return html.Div([
                dbc.Tabs(
             [
                dbc.Tab(label="TIME TREND",tab_id='tab-1',tab_style={"margin-left": "auto"},label_style={"color": "#bef7ea"}),
                        
                dbc.Tab(label="CROP ANALYSIS",tab_id='tab-2', label_style={"color": "#00AEF9"}),
                
       ],
        
         id="tabs",#
         active_tab="tab-2",
 ),
     html.Div(id='tabs-content'),
      html.Footer("© 2020 Business Brio. All Rights Reserved.")
      ],style={"display": "flex", "flex-direction": "column"}
    )

                
    elif pathname == "/page-1/2":
        return html.P("This is the content of page 1.2. Yay!")
    elif pathname == "/page-2/1":
        return html.P("Oh cool, this is page 2.1!")
    elif pathname == "/page-2/2":
        return html.P("No way! This is page 2.2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab')])
def render_content(tab):
    if tab == 'tab-1':
        
        return app2.layout
        #return html.P("I am on it") 
        #Tab1.tab_1_layout
    
    elif tab == 'tab-2':
        #return test_map_table
        return app1.layout
        #return html.P("I am changing it")#Tab2.tab_2_layout
   
     
    
if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    app.run_server(debug=False, host=host, port =8080)

