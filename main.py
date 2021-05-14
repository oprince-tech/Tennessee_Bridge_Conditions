import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go


df = pd.read_csv('Bridge_Condition.csv')
df['CONDITION'] = df['CONDITION'].astype(str)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


def draw_left_nav():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Label('Condition:'),
                html.Ul([
                    html.Li(
                            "Good",
                            style={'background': 'Green'},
                            className='circle',
                            ),
                    html.Li(
                            "Fair",
                            style={'background': 'Yellow'},
                            className='circle',
                            ),
                    html.Li(
                            "Poor",
                            style={'background': 'Orange'},
                            className='circle',
                            ),
                    html.Li(
                            "Critical",
                            style={'background': 'Red'},
                            className='circle',
                            ),
                ], className='condition_ul'),
                html.Label(children=['Select: ']),
                dcc.Checklist(
                              id='condition_status',
                              options=[
                                        {
                                            'label': str(c),
                                            'value': c
                                        } for c in df['CONDITION'].unique() if c != 'nan'
                                       ],
                              value=[c for c in df['CONDITION'].unique()]
                              ),
                html.Label(children=['County:']),
                dcc.Dropdown(
                             id='county',
                             options=[
                                 {
                                     'label': str(x),
                                     'value': x
                                  } for x in sorted(df['COUNTY'].unique())
                             ],

                )
            ], className='legend_container'
            ),
        ),
    ])


def draw_report():
    return html.Div(
        dbc.Card([
            dbc.CardBody([
                html.Label('Report:'),
                    dcc.Graph(
                        id='report'
                    ),
            ])
        ], className='report_container')
    )


def draw_graph():
    return html.Div([
        dcc.Graph(
                  id='map',
                  config={'displayModeBar': False, 'scrollZoom': True}
        )
        ])


app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            draw_left_nav(),
            draw_report(),
        ], width=2),
        dbc.Col([
            html.H1('Tennessee Bridge Conditions', id='title'),
            draw_graph(),
        ], width=10),
    ]),
])


@app.callback(Output('report', 'figure'),
              [Input('condition_status', 'value'),
               Input('county', 'value')])
def update_report(select_condition, county):
    if county:
        df_cull = df[
                    (df['CONDITION'].isin(select_condition)) &
                    (df['COUNTY'] == county)
                    ]
    else:
        df_cull = df[(df['CONDITION'].isin(select_condition))]

    pie_chart = px.pie(
                       df_cull,
                       title=str(county),
                       names='CONDITION',
                       color='CONDITION',
                       color_discrete_map={
                            'Good': 'Green',
                            'Fair': 'Yellow',
                            'Poor': 'Orange',
                            'Critical': 'Red',
                            'nan': 'White'
                       }
                      )
    pie_chart.update_traces(textinfo='value', hovertemplate=None)
    pie_chart.update_layout({
        'font_color': '#eee',
        'plot_bgcolor': '#171717',
        'paper_bgcolor': '#171717',
    })
    return pie_chart


@app.callback(Output('map', 'figure'),
              [Input('condition_status', 'value'),
               Input('county', 'value')])
def update_map(select_condition, county):
    if county:
        df_cull = df[
                    (df['CONDITION'].isin(select_condition)) &
                    (df['COUNTY'] == county)
                    ]
    else:
        df_cull = df[(df['CONDITION'].isin(select_condition))]

    locations = [go.Scattermapbox(
                        lat=df_cull['LATITUDE'],
                        lon=df_cull['LONGITUDE'],
                        mode='markers',
                        hoverlabel_font={
                            'color': '#eee'
                        },
                        customdata=df_cull.loc[:, [
                                                   'STRUCTURE_ID',
                                                   'OWNER',
                                                   'AGE'
                                                  ]],
                        hoverinfo='text',
                        hovertemplate='<b>SID: %{customdata[0]}</b><br>' +
                                      '<b>Owner: %{customdata[1]}</b><br>' +
                                      '<b>Age: %{customdata[2]} yrs</b><br>' +
                                      '<extra></extra>',
                        marker={
                                'color': df_cull['COLOR'],
                                'size': 10,
                                },

    )]

    return {
        'data': locations,
        'layout': go.Layout(
            uirevision='foo',
            clickmode='event+select',
            hovermode='closest',
            mapbox=dict(
                style='open-street-map',
                center=dict(
                    lat=35.860119,
                    lon=-86
                ),
                zoom=7,
            ),
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
