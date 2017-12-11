
# coding: utf-8

# In[ ]:


#Importing packages and the csv

import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

euro_data = pd.read_csv("nama_10_gdp_1_Data.csv")
available_indicators = euro_data['NA_ITEM'].unique()
available_countries = euro_data['GEO'].unique()
print(euro_data.head())


# In[ ]:


#Dashboard1
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

euro_data_alpha = euro_data[euro_data['UNIT'] == 'Current prices, million euro']
app.layout = html.Div([  
    html.Div([
        
        html.Div([
            dcc.Dropdown( 

                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators]
                #value='GDP'
            )
        ],
        style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Salaries'
            )
        ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
  dcc.Graph(id='FirstGraph'),

    
    html.Div(dcc.Slider( 
        id='year--slider',
        min=euro_data['TIME'].min(),
        max=euro_data['TIME'].max(),
        value=euro_data['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in euro_data['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),
    
#Dashboard2
        html.Div([
        
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='GDP'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "European Union (28 countries)"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
     dcc.Graph(id='SecondGraph'),

])

#App callback for Dashboard1
@app.callback(
    dash.dependencies.Output('FirstGraph', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

    euro_data_yearly = euro_data[euro_data['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            text=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 0},
            hovermode='closest'
        )
    }

#App callback for Dashboard2
@app.callback(
    dash.dependencies.Output('SecondGraph', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
   
    euro_data_yearly = euro_data_alpha[euro_data_alpha['GEO'] == yaxis_column_name]


    return {
        'data': [go.Scatter(
            x=euro_data_yearly['TIME'].unique(),
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 100, 'b': 50, 't': 25, 'r': 0},
            hovermode='closest'
        )
    }

#Running it on the server
if __name__ == '__main__':
    app.run_server()

