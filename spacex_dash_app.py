# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

label_list = ['All Sites']
label_list.extend([i for i in list(spacex_df['Launch Site'].unique())])
value_list = ['ALL']
value_list.extend([i for i in list(spacex_df['Launch Site'].unique())])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
        
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        
        dcc.Dropdown(
            id='site-dropdown', 
            options=[
                {'label': label, 'value': value} for label, value in zip(label_list, value_list)
            ],
            value='ALL', 
            placeholder='Select Launch Site:'
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(min=0, max=10000,
            value=[min_payload, max_payload], 
            marks={value: f'{value}' for value in range(0, 12500, 2500)},
            id='payload-slider'
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(launch_site):
    if launch_site == 'ALL': 
        filtered_df = spacex_df.copy()
        filtered_df = filtered_df.groupby('Launch Site').aggregate(
            {'class': 'sum'}).reset_index()
        filtered_df.sort_values('class', inplace=True)
        figure = px.pie(
            filtered_df, values='class', names='Launch Site', color='Launch Site',
            title='Total Success Launches By Site', 
            color_discrete_sequence=px.colors.sequential.algae
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==launch_site].copy()
        filtered_df = filtered_df['class'].value_counts().to_frame().reset_index()
        filtered_df.sort_values(by='class', inplace=True)
        filtered_df['class'] = filtered_df['class'].replace({1: 'Success', 0: 'Failure'})
        figure = px.pie(
            filtered_df, values='count', names='class', 
            color='class',
            color_discrete_map={'Success': 'paleturquoise', 'Failure': 'lightpink'}, 
            title='Total Success Launches of site {}'.format(launch_site),
        )
    return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'), 
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id='payload-slider', component_property='value')]
)
def get_payload_scatter(launch_site, payload_range):
    print(payload_range)
    cond = ((spacex_df['Payload Mass (kg)'] >= payload_range[0])
            & (spacex_df['Payload Mass (kg)'] <= payload_range[1]))
    filtered_df = spacex_df[cond].copy()
    if launch_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site']==launch_site]
        label = 'site {}'.format(launch_site)
    else:
        label = 'all Sites'
    figure = px.scatter(
        x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', data_frame=filtered_df, 
        title='Correlation between Payload and Success for {}'.format(label)
    )
    return figure


# Run the app
if __name__ == '__main__':
    app.run_server()
