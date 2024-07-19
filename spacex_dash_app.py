import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                dcc.Dropdown(id='site-dropdown',
                                             options = [{'label':'All Sites', 'value':'ALL'},
                                                        {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                        {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                        {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                        {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                                        ],
                                             value='ALL',
                                             placeholder='Select a Launch Site Here ',
                                             searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
 
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0:'0', 10000:'10000'},
                                                value=[min_payload, max_payload]),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(inputted_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == inputted_site]
    fg_df = filtered_df.groupby('class')['Launch Site'].count().reset_index()

    if inputted_site == 'ALL':
        fig = px.pie(spacex_df,
                     values='class',
                     names='Launch Site',
                     title='Total Success Launches By Site')
        return fig
    else:
        fig = px.pie(fg_df,
                     values= 'Launch Site',
                     names='class',
                     title=f'Total Success Launches for {inputted_site}')
        return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_plot(inputted_site, slider_values):
    minvalue, maxvalue = slider_values
    if inputted_site =='ALL':
        df_payloaded = spacex_df[(spacex_df['Payload Mass (kg)'] > minvalue) & (spacex_df['Payload Mass (kg)'] < maxvalue)]
        fig1 = px.scatter(df_payloaded,
                        x='Payload Mass (kg)',
                        y='class',
                        color='Booster Version Category')
        return fig1
    else:
        df_grouped = spacex_df[spacex_df['Launch Site'] == inputted_site]
        df_payloaded = df_grouped[(df_grouped['Payload Mass (kg)'] > minvalue) & (df_grouped['Payload Mass (kg)'] < maxvalue)]
        fig2 = px.scatter(df_payloaded,
                          x='Payload Mass (kg)',
                          y='class',
                          color='Booster Version Category')
        return fig2

if __name__ == '__main__':
    app.run_server()
