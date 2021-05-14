import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


df = pd.read_csv('Bridge_Condition.csv')
df['CONDITION'] = df['CONDITION'].astype(str)

app = dash.Dash(__name__)

app.layout = html.Div([
    # LEGEND
    html.Div([
        html.Label('Condition: '),
        html.Ul([
            html.Li(
                    "Good",
                    className='circle legend',
                    style={'background': 'Green'}
                    ),
            html.Li(
                    "Fair",
                    className='circle legend', style={'background': 'Yellow'}
                    ),
            html.Li(
                    "Poor",
                    className='circle legend', style={'background': 'Orange'}
                    ),
            html.Li(
                    "Critical",
                    className='circle legend',
                    style={'background': 'Red'}
                    ),
        ], style={'border-bottom': 'solid 1px', 'padding-top': '6px'}),
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
        html.Label(children=['County: ']),
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
    html.Div([
        dcc.Graph(id='graph', config={'displayModeBar': False}),
    ], className='graph_container'
    ),
])


@app.callback(Output('graph', 'figure'),
              [Input('condition_status', 'value'),
               Input('county', 'value')])
def update_figure(select_condition, county):
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
                        hoverinfo='text',
                        hovertemplate='<b>lat: %{lat}</b><br>'+
                                      '<b>lon: %{lon}</b><br>'+
                                      '<extra></extra>',
                        marker={
                            'color': df_cull['COLOR'],
                            'size': 8,
                            },

    )]

    return {
        'data': locations,
        'layout': go.Layout(
            uirevision='foo',
            clickmode='event+select',
            hovermode='closest',
            hoverdistance=1,
            mapbox=dict(
                style='carto-darkmatter',
                center=dict(
                    lat=36.174465,
                    lon=-86.767960
                ),
                zoom=10,
            ),
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
