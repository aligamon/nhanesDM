import dash_bootstrap_components as dbc
from dash import Dash,State, html, dcc, Input, Output, Patch, clientside_callback, callback
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio

load_figure_template(["minty", "minty_dark"])


vizDF = pd.read_csv('vizDF.csv')

# Color map for diabetes categories
diabetes_colors = {
    'No Diabetes': '#58D68D',
    'Pre-diabetes': '#FFFB9D',
    'Diabetes': '#E74C3C'
}

# Color map for gender categories
gender_colors = {
    'Male': '#1f77b4',
    'Female': '#ff7f0e'
}

# Category order for diabetes
diabetes_order = ['No Diabetes', 'Pre-diabetes', 'Diabetes']

# Initialize app with Bootstrap CSS
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch( id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

# App layout
dash_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Diabetes Dashboard", className='text-center mb-4'))
    ]),
    color_mode_switch,
    dbc.Row([
        dbc.Col(
            dcc.Link(
                dbc.Button("Home", href="/", color="primary", className="text-end"),
                href="/", refresh=True
            ), 
            width="auto", className="text-end"
        ),
        dbc.Col(
            dbc.Button('> Filters', id="toggle-sidebar", color="light", className="me-1", outline=False, style={"position": "fixed", "top": "10px", "left": "10px", "zIndex": "1000"}),
            width='auto'
        )
    ]),
    dcc.Store(id='sidebar-state', data=True),
    dbc.Offcanvas(
        html.Div([
            html.Label("Diabetes Filter"),
             dcc.Dropdown(
                id='diabetes-filter',
                options=[{'label': val, 'value': val} for val in vizDF['diabetes'].unique()],
                placeholder='Filter by Diabetes',
                multi=True
            ),
            html.Label("Race Filter"),
            dcc.Dropdown(
                id='race-filter',
                options=[{'label': val, 'value': val} for val in vizDF['race'].unique()],
                placeholder='Filter by Race',
                multi=True
            ),
            html.Label("Marital Status Filter"),
            dcc.Dropdown(
                id='marital-filter',
                options=[{'label': val, 'value': val} for val in vizDF['maritalStatus'].unique()],
                placeholder='Filter by Marital Status',
                multi=True
            ),
            html.Label("Gender Filter"),
            dcc.Dropdown(
                id='gender-filter',
                options=[{'label': val, 'value': val} for val in vizDF['gender'].unique()],
                placeholder='Filter by Gender'
            ),
            html.Label("Color Filter"),
            dcc.Dropdown(
                id='color-column1',
                options=[
                    {'label': 'Diabetes', 'value': 'diabetes'},
                    {'label': 'Race', 'value': 'race'},
                    {'label': 'Gender', 'value': 'gender'}
                ],
                placeholder='Select Color Column',
                value='diabetes',
                clearable=False
            ),
            html.Label("Age Range"),
            dcc.RangeSlider(
                id='age-slider',
                min=vizDF['age'].min(),
                max=vizDF['age'].max(),
                value=[vizDF['age'].min(), vizDF['age'].max()],
                marks={i: str(i) for i in range(int(vizDF['age'].min()), int(vizDF['age'].max()) + 1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label("Glucose Level Range"),
            dcc.RangeSlider(
                id='glucose-slider',
                min=vizDF['glucose_level'].min(),
                max=vizDF['glucose_level'].max(),
                value=[vizDF['glucose_level'].min(), vizDF['glucose_level'].max()],
                marks={i: str(i) for i in range(int(vizDF['glucose_level'].min()), int(vizDF['glucose_level'].max()) + 1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label("BMI Range"),
            dcc.RangeSlider(
                id='bmi-slider',
                min=vizDF['bmi'].min(),
                max=vizDF['bmi'].max(),
                value=[vizDF['bmi'].min(), vizDF['bmi'].max()],
                marks={i: str(i) for i in range(int(vizDF['bmi'].min()), int(vizDF['bmi'].max()) + 1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Label("Systolic Blood Pressure Range"),
            dcc.RangeSlider(
                id='bpsys-slider',
                min=vizDF['bpSys'].min(),
                max=vizDF['bpSys'].max(),
                value=[vizDF['bpSys'].min(), vizDF['bpSys'].max()],
                marks={i: str(i) for i in range(int(vizDF['bpSys'].min()), int(vizDF['bpSys'].max()) + 1, 50)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ]),
        id='sidebar',
        is_open=False,
        title='Filters'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='pie-chart'), xs=12, sm=12, md=6, lg=6),
                dbc.Col(dcc.Graph(id='stacked-bar-chart'), xs=12, sm=12, md=6, lg=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='marital-status-bar'), xs=12, sm=12, md=6, lg=6),
                dbc.Col(dcc.Graph(id='family-size-bar'), xs=12, sm=12, md=6, lg=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='box-plot'), xs=12, sm=12, md=6, lg=6),
                dbc.Col(dcc.Graph(id='box_plot_glucose'), xs=12, sm=12, md=6, lg=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='scatter_age_glucose'), xs=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='scatter_bmi_glucose'), xs=12, sm=12, md=6, lg=6),
                dbc.Col(dcc.Graph(id='scatter-age-bmi'), xs=12, sm=12, md=6, lg=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='scatter-age-bpsys'), xs=12, sm=12, md=6, lg=6),
                dbc.Col(dcc.Graph(id='scatter-age-mental'), xs=12, sm=12, md=6, lg=6),
            ])
        ], xs=12, sm=12, md=12, lg=12, id='main-content')
    ])
], fluid=True)


# Callback to update the sidebar visibility
@dash_app.callback(
    Output('sidebar', 'is_open'),
    Input('toggle-sidebar', 'n_clicks'),
    State('sidebar', 'is_open')
)
def toggle_sidebar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# Callback to update the graphs based on filters
@dash_app.callback(
    [
        Output('pie-chart', 'figure'),
        Output('stacked-bar-chart', 'figure'),
        Output('marital-status-bar', 'figure'),
        Output('family-size-bar', 'figure'),
        Output('box-plot', 'figure'),
        Output('scatter-age-bmi', 'figure'),
        Output('scatter-age-bpsys', 'figure'),
        Output('scatter-age-mental', 'figure'),
        Output('scatter_age_glucose', 'figure'),
        Output('scatter_bmi_glucose', 'figure'),
        Output('box_plot_glucose', 'figure')
    ],
    [
        Input('diabetes-filter', 'value'),
        Input('race-filter', 'value'),
        Input('marital-filter', 'value'),
        Input('gender-filter', 'value'),
        Input('color-column1', 'value'),
        Input('age-slider', 'value'),
        Input('glucose-slider', 'value'),
        Input('bmi-slider', 'value'),
        Input('bpsys-slider', 'value'),
        Input("color-mode-switch", "value")
        
    ]
)
def update_charts(diabetes, race, marital_status, gender, color_column1, age_range, glucose_range, bmi_range, bpsys_range, theme):
    # Filter based on the selected filters
    df_filtered = vizDF.copy()
    if diabetes:
        df_filtered = df_filtered[df_filtered['diabetes'].isin(diabetes)]
    if race:
        df_filtered = df_filtered[df_filtered['race'].isin(race)]
    if marital_status:
        df_filtered = df_filtered[df_filtered['maritalStatus'].isin(marital_status)]
    if gender:
        df_filtered = df_filtered[df_filtered['gender'] == gender]
    df_filtered = df_filtered[
        (df_filtered['age'] >= age_range[0]) & (df_filtered['age'] <= age_range[1]) &
        (df_filtered['glucose_level'] >= glucose_range[0]) & (df_filtered['glucose_level'] <= glucose_range[1]) &
        (df_filtered['bmi'] >= bmi_range[0]) & (df_filtered['bmi'] <= bmi_range[1]) &
        (df_filtered['bpSys'] >= bpsys_range[0]) & (df_filtered['bpSys'] <= bpsys_range[1])
    ]

    # Color map and category order based on the selected color column
    if color_column1 == 'diabetes':
        color_map = diabetes_colors
        category_order = diabetes_order
    elif color_column1 == 'gender':
        color_map = gender_colors
        category_order = list(gender_colors.keys())
    elif color_column1 == 'race':
        color_map = {race: px.colors.qualitative.Plotly[i] for i, race in enumerate(vizDF['race'].unique())}
        category_order = list(vizDF['race'].unique())

    template = pio.templates["minty"] if theme else pio.templates["minty_dark"]
    pio.templates.default = template
    # Update the figures with the filtered DataFrame
    pie_chart = px.pie(
        df_filtered,
        names='diabetes',
        title='Diabetes Distribution',
        color='diabetes',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    stacked_bar_chart = px.histogram(
        df_filtered,
        y='gender',
        color='diabetes',
        barmode='relative',
        title='Gender Distribution by Diabetes',
        orientation='h',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    marital_status_bar = px.histogram(
        df_filtered,
        y='maritalStatus',
        color=color_column1,
        title='Marital Status Distribution',
        barnorm='percent',
        orientation='h',
        color_discrete_map=color_map,
        category_orders={color_column1: category_order}
    )

    family_size_bar = px.histogram(
        df_filtered,
        y='familySize',
        color='diabetes',
        title='Family Size Distribution',
        orientation='h',
        barmode='relative',
        barnorm='percent',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    box_plot = px.box(
        df_filtered,
        x='diabetes',
        y='age',
        title='Age Distribution by Diabetes',
        color=color_column1,
        color_discrete_map=color_map,
        category_orders={color_column1: category_order}
    )

    box_plot_glucose = px.box(
        df_filtered,
        x='diabetes',
        y='glucose_level',
        title='Glucose Distribution by Diabetes',
        color=color_column1,
        color_discrete_map=color_map,
        category_orders={color_column1: category_order}
    )

    scatter_age_glucose = px.scatter(
        df_filtered,
        x='age',
        y='glucose_level',
        color='diabetes',
        title='Age vs Glucose Level',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    scatter_bmi_glucose = px.scatter(
        df_filtered,
        x='bmi',
        y='glucose_level',
        color='diabetes',
        title='Glucose level vs BMI',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    scatter_age_bmi = px.scatter(
        df_filtered,
        x='age',
        y='bmi',
        color='diabetes',
        title='Age vs BMI',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    scatter_age_bmi.add_shape(
        type='line',
        x0=df_filtered['age'].min(), x1=df_filtered['age'].max(),
        y0=25, y1=25,
        line=dict(color='Black', width=2, dash='dash')
    )

    scatter_age_bmi.add_annotation(
        x=df_filtered['age'].max() + 4, y=23,
        text='Overweight',
        showarrow=False,
        yshift=10
    )

    scatter_age_bmi.add_shape(
        type='line',
        x0=df_filtered['age'].min(), x1=df_filtered['age'].max(),
        y0=30, y1=30,
        line=dict(color='Black', width=2, dash='dash')
    )

    scatter_age_bmi.add_annotation(
        x=df_filtered['age'].max() + 4, y=28,
        text='Obese',
        showarrow=False,
        yshift=10
    )

    scatter_age_bpsys = px.scatter(
        df_filtered,
        x='age',
        y='bpSys',
        color='diabetes',
        title='Age vs Systolic Blood Pressure',
        color_discrete_map=diabetes_colors,
        category_orders={'diabetes': diabetes_order}
    )

    scatter_age_mental = px.scatter(
        df_filtered,
        x='age',
        y='mentalHealthScore',
        color='diabetes',
        title='Age vs Mental Health Score',
        color_discrete_map=diabetes_colors,
        
        category_orders={'diabetes': diabetes_order}
    )

    


    return pie_chart, stacked_bar_chart, marital_status_bar, family_size_bar, box_plot, scatter_age_bmi, scatter_age_bpsys, scatter_age_mental, scatter_age_glucose, scatter_bmi_glucose, box_plot_glucose



def update_figure_template(switch_on):
        # Using Patch() to update the figure template, Using the figure template dict from plotly.io  and not just the template name
        template = pio.templates["minty"] if switch_on else pio.templates["minty_dark"]

        patched_figure = Patch()
        patched_figure["layout"]["template"] = template
        return patched_figure


# Clientside callback to switch the theme
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

if __name__ == "__main__":
    dash_app.run_server(debug=True)
