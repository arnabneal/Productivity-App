# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:08:28 2020

@author: User
"""

import dash
import dash_bootstrap_components as dbc
import warnings
#import pandas as pd
#import geopandas as gpd

app=dash.Dash(__name__ ,suppress_callback_exceptions=True,meta_tags=[{"name": "viewport", "content": "width=device-width"}] ,external_stylesheets=[dbc.themes.SPACELAB])

#app.scripts.config.serve_locally=True
#app.css.config.serve_locally=True
warnings.filterwarnings("ignore")
application = app.server
#for ignoring warnings

