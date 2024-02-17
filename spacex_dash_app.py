# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash import no_update
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(
                                    [html.Div([html.H2('Launch Site: ', style={'margin-right':'2em'})]),
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[
                                            {'label':'All Sites', 'value':'ALL'},
                                            {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                            {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                            {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                            {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site Location Here',
                                            style={
                                                'width': '80%',
                                                'padding': '3px',
                                                'font-size': '20px',
                                                'textAlign': 'center'
                                            },
                                            searchable=True
                                            )
                                    ], style={'display': 'flex'}
                                ),
                                
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id = 'payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    marks = {0:{'label':'0 kg', 'style':{'color':'#040C48', 'font-weight':'bold'}}, 500: '500 kg',
                                             1000: '1000 kg', 1500: '1500 kg',
                                             2000: '2000 kg', 2500: '2500 kg',
                                             3000: '3000 kg', 3500: '3500 kg',
                                             4000: '4000 kg', 4500: '4500 kg',
                                             5000: '5000 kg', 5500: '5500 kg',
                                             6000: '6000 kg', 6500: '6500 kg',
                                             7000: '7000 kg', 7500: '7500 kg',
                                             8000: '8000 kg', 8500: '8500 kg',
                                             9000: '9000 kg', 9500: '9500 kg',
                                             10000:{'label':'10000 kg', 'style':{'color':'#5C0000', 'font-weight':'bold'}}
                                    },
                                    value = [min_payload, max_payload]
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    newspacex = spacex_df
    newspacex['Status'] = newspacex['class']
    newspacex['Status'] = newspacex['Status'].map({0:'Failed', 1:'Success'})
    filtered_df = newspacex[newspacex['Launch Site']==entered_site]
    filtered_df = filtered_df.groupby(['Launch Site', 'Status']).size()
    filtered_df = filtered_df.reset_index(name='Status count')
    if entered_site == 'ALL':
        fig = px.pie(
            newspacex[newspacex['class']==int(1)],
            values = 'class',
            names = 'Launch Site',
            color_discrete_sequence = ['#87D3F9', '#FEFE82', '#CFA3FF', '#BEE395'],
            title = 'Total Success Launches by Launch Site'
        )
        return fig
    else:
        fig = px.pie(
            filtered_df,
            values = 'Status count',
            names = 'Status',
            color_discrete_sequence = ['#FF8181', '#92D050'],
            title = (f'Total Success Launches for site {entered_site}')
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]   
)

def get_scatter_plot(entered_site, payload_quantity):
    
    spacexscatter = spacex_df[
        (spacex_df['Payload Mass (kg)']>=payload_quantity[0])&
        (spacex_df['Payload Mass (kg)']<=payload_quantity[1])
    ]
    
    spacexscatter['Status'] = spacexscatter['class']
    spacexscatter['Status'] = spacexscatter['Status'].map({0:'Failed', 1:'Success'})

    filtscatter_df = spacexscatter[spacexscatter['Launch Site']==entered_site]

    if entered_site == 'ALL':
        fig = px.scatter(
            spacexscatter,
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version Category',
            symbol = 'Booster Version Category',
            hover_data = 'Booster Version',
            color_discrete_sequence = ['#ED7D31', '#7030A0', '#517D33', '#C00000', '#002060'],
            title = 'Correlation Between Payload Mass (kg) and Launch Success for All Launch Sites'
        )
        return fig
    else:
        fig = px.scatter(
            filtscatter_df,
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version Category',
            symbol = 'Booster Version Category',
            hover_data = 'Booster Version',
            color_discrete_sequence = ['#ED7D31', '#7030A0', '#517D33', '#C00000', '#002060'],
            title = (f'Correlation Between Payload Mass (kg) and Launch Success for site {entered_site}')
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
