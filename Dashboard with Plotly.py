# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                                    {'label':'All Sites', 'value':'ALL'},
                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                    ], value='ALL', placeholder='Select a Launch Site', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(site):
    if site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='All Sites')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == site]
        df['values'] = 1
        fig = px.pie(df, names='class', values='values', title=site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')]
)
def get_scatter_chart(site, payload):
    min, max = payload
    if site == 'ALL':
        mask = (spacex_df['Payload Mass (kg)'] >= min) & (spacex_df['Payload Mass (kg)'] <= max)
        fig = px.scatter(spacex_df[mask], y='class', x='Payload Mass (kg)', color='Booster Version Category')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == site]
        mask = (df['Payload Mass (kg)'] >= min) & (df['Payload Mass (kg)'] <= max)
        fig = px.scatter(df[mask], y='class', x='Payload Mass (kg)', color='Booster Version Category')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()