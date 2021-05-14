import pandas as pd
import json
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px

pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

with open('Bridge_Condition.geojson') as f:
    data = json.load(f)
    df = pd.json_normalize(data['features'])

new = df.drop(['type', 'properties.REPORTING_YEAR', 'properties.FID', 'properties.ROUTE_NUMBER', 'properties.LOG_MILE', 'properties.YEAR_BUILT', 'properties.OBJECTID', 'geometry.type'], axis=1)
new.rename(columns={
                    'properties.STRUCTURE_ID': 'STRUCTURE_ID',
                    'properties.COUNTY': 'COUNTY',
                    'properties.OWNER': 'OWNER',
                    'properties.AGE': 'AGE',
                    'properties.OVERALL_CONDITION': 'CONDITION',
                    'geometry.coordinates': 'COORDINATES',
                    }, inplace=True)
new.insert(loc=5, column='COLOR', value=None)
new.loc[new['CONDITION'] == 'Good', 'COLOR'] = 'Green'
new.loc[new['CONDITION'] == 'Fair', 'COLOR'] = 'Yellow'
new.loc[new['CONDITION'] == 'Poor', 'COLOR'] = 'Orange'
new.loc[new['CONDITION'] == 'Critical', 'COLOR'] = 'Red'
new.loc[:, 'LATITUDE'] = new.COORDINATES.map(lambda x: x[1])
new.loc[:, 'LONGITUDE'] = new.COORDINATES.map(lambda x: x[0])
new.drop(['COORDINATES'], 1, inplace=True)
print(new)
new.to_csv('Bridge_Condition.csv')
"""
    type: Feature
    properties:
        FID
        REPORTING_YEAR
        STRUCTURE_ID
        COUNTY
        ROUTE_NUMBER
        LOG_MILE
        OWNER
        YEAR_BUILT
        AGE
        OVERALL_CONDITION
        OBJECTID
    geometry:
        type: Point
        coordinates: [lat lon]
"""
# colors = {
#     'Good': 'blue',
#     'Fair': 'pink',
#     'Poor': 'yellow',
#     'Critical': 'red',
# }
#
# fig = px.scatter_mapbox(df,
#                         lat=df['geometry.coordinates'].str[1],
#                         lon=df['geometry.coordinates'].str[0],
#                         hover_data=['properties.OVERALL_CONDITION'],
#                         color=['properties.OVERALL_CONDITION'],
#                         color_discrete_map=colors)
# fig.update_layout(mapbox_style="carto-darkmatter")
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()


# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     dcc.Graph(id='choropleth')
# ])
#
# def display_choropleth():
#     fig = px.choropleth(df,
#                         geojson=)
