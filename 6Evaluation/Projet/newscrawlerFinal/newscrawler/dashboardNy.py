import pandas as pd
import dash
import folium
import plotly_express as px
import pandas as pd
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go
import json
import requests
from branca.element import Template, MacroElement


def get_new_york_data():
    url = 'https://cocl.us/new_york_dataset'
    resp = requests.get(url).json()
    # all data is present in features label
    features = resp['features']
    # define the dataframe columns
    column_names = ['Borough', 'Neighborhood', 'Latitude', 'Longitude']
    # instantiate the dataframe
    new_york_data = pd.DataFrame(columns=column_names)
    for data in features:
        borough = data['properties']['borough']
        neighborhood_name = data['properties']['name']
        neighborhood_latlon = data['geometry']['coordinates']
        neighborhood_lat = neighborhood_latlon[1]
        neighborhood_lon = neighborhood_latlon[0]
        new_york_data = new_york_data.append({'Borough': borough,
                                              'Neighborhood': neighborhood_name,
                                              'Latitude': neighborhood_lat,
                                              'Longitude': neighborhood_lon}, ignore_index=True)
    return new_york_data


def map_ny():
    expedia = pd.read_csv("expedia.csv")
    hotelscom = pd.read_csv('hotelscom.csv', encoding="utf-8", dayfirst=True)

    expedia['notes'] = 1
    expedia['avis2'] = 1
    expedia = expedia.fillna(0)
    expedia = expedia[["site", "id", 'title', 'dateDepart', 'dateArrive',
                       'localisation', 'prix', 'nombreNuits', 'avis', 'notes', 'images']]
    expedia.loc[expedia.nombreNuits ==
                'pour 6 nuits', 'nombreNuits'] = '6 nuits'
    expedia.prix = expedia.prix.replace('\D', '', regex=True).astype(int)
    expedia = expedia.rename(columns={'avis': 'nombreAvis'})
    expedia = expedia.rename(columns={'dateDepart': 'Debut'})
    expedia = expedia.rename(columns={'dateArrive': 'Fin'})

    expedia.notes = expedia.nombreAvis
    expedia.notes = expedia.notes.str.split(expand=True)
    expedia.notes = expedia.notes.replace('\D', '', regex=True).astype(int)
    expedia.notes = (expedia.notes/10)*2
    a = expedia.nombreAvis.str.split(expand=True)
    expedia.nombreAvis = expedia.nombreAvis = a[4] + a[5]
    expedia.nombreAvis = expedia.nombreAvis.replace(
        '\D', '', regex=True).astype(int)

    hotelscom = hotelscom.fillna(0)
    hotelscom.dateDepart = pd.to_datetime(hotelscom.dateDepart, dayfirst=True)
    hotelscom.dateArrive = pd.to_datetime(hotelscom.dateArrive, dayfirst=True)
    hotelscom.loc[hotelscom.nombreNuits ==
                  'pour 1 chambre pour 6 nuits', 'nombreNuits'] = '6 nuits'
    hotelscom.prix = hotelscom.prix.str.strip(" €")
    hotelscom.prixbis = hotelscom.prixbis.str.strip(" €")
    hotelscom.prix = hotelscom.prix.fillna(0)
    hotelscom.prixbis = hotelscom.prixbis.fillna(0)
    hotelscom.prix = hotelscom.prix.replace('\D', '', regex=True).astype(int)
    hotelscom.prixbis = hotelscom.prixbis.replace(
        '\D', '', regex=True).astype(int)
    hotelscom['prixfinal'] = hotelscom.prix + hotelscom.prixbis
    hotelscom.drop(columns='prix', inplace=True)
    hotelscom.drop(columns='prixbis', inplace=True)
    hotelscom = hotelscom[["site", "id", 'title', 'dateArrive', 'dateDepart',
                           'localisation', 'prixfinal', 'nombreNuits', 'avis', 'notes', 'images']]
    hotelscom = hotelscom.rename(columns={'prixfinal': 'prix'})
    hotelscom = hotelscom.rename(columns={'avis': 'nombreAvis'})
    hotelscom = hotelscom.rename(columns={'dateArrive': 'Debut'})
    hotelscom = hotelscom.rename(columns={'dateDepart': 'Fin'})

    hotelscom.nombreAvis = hotelscom.nombreAvis.fillna(0)
    hotelscom.nombreAvis = hotelscom.nombreAvis.replace(
        '\D', '', regex=True).astype(int)
    hotelscom.notes = hotelscom.notes.replace('\D', '', regex=True).astype(int)
    hotelscom.notes = hotelscom.notes/10

    df = pd.concat([expedia, hotelscom])
    df = df.fillna(0)
    df.Debut = pd.to_datetime(df.Debut)
    df.Fin = pd.to_datetime(df.Fin)
    df.loc[df.nombreNuits == 'pour 6 nuits', 'nombreNuits'] = '6 nuits'
    df.drop(df.loc[df['nombreAvis'] == 0].index, inplace=True)
    df = df.reset_index()
    df.drop(columns='index', inplace=True)

    import json
    with open('newyork_data.json') as json_data:
        newyork_data = json.load(json_data)

    import requests

    ny_data = get_new_york_data()

    ny_data['mean'] = 1.0
    ny_data['id'] = 'a'
    ny_data.drop(columns='Borough', inplace=True)
    ny_data.columns = ['Localisation', 'Latitude', 'Longitude', 'mean', 'id']
    ny_data = ny_data[['id', 'Localisation', 'mean', 'Latitude', 'Longitude']]

    df_ville = df.groupby(['id', 'localisation', ]).agg(
        {'prix': ['mean']}).reset_index()
    df_ville.columns = ['id', 'Localisation', 'mean']
    df_ville = df_ville.sort_values(by='mean', ascending=False).reset_index()
    df_ville.drop(columns='index', inplace=True)
    df_ville['Latitude'] = 1.0
    df_ville['Longitude'] = 1.0

    df4 = pd.merge(df_ville, ny_data, on='Localisation', how='right')
    df4 = df4.fillna(0)
    df4 = df4[(df4 != 0).all(1)]
    df4.drop(columns='Latitude_x', inplace=True)
    df4.drop(columns='Longitude_x', inplace=True)
    df4.drop(columns='id_y', inplace=True)
    df4.drop(columns='mean_y', inplace=True)

    df4.reset_index()
    df4 = df4[df4.id_x == 'New York']
    df4 = df4.rename(columns={'id_x': 'id'})
    df4 = df4.rename(columns={'mean_x': 'mean'})
    df4 = df4.rename(columns={'Latitude_y': 'Latitude'})
    df4 = df4.rename(columns={'Longitude_y': 'Longitude'})

    uptown = {'id': 'New York', 'Localisation': 'Uptown', 'mean': '3695.00',
              'Latitude': "40.7528793", 'Longitude': '-74.0243068'}
    cinquante = {'id': 'New York', 'Localisation': '59e rue',
                 'mean': '2993.25', 'Latitude': "40.765994", 'Longitude': '-73.976963'}
    mideast = {'id': 'New York', 'Localisation': 'Midtown East',
               'mean': '2863.3', 'Latitude': "40.756445", 'Longitude': '-73.970366'}
    theater = {'id': 'New York', 'Localisation': 'Theater District',
               'mean': '2840.00', 'Latitude': "40.75659", 'Longitude': '-73.98626'}
    manhattan = {'id': 'New York', 'Localisation': 'Manhattan',
                 'mean': '2374.75', 'Latitude': "40.747745", 'Longitude': '-73.985474'}
    timesquare = {'id': 'New York', 'Localisation': 'Times Square',
                  'mean': '2134.375', 'Latitude': "40.757447", 'Longitude': '-73.98595'}
    brooklyn = {'id': 'New York', 'Localisation': 'Brooklyn',
                'mean': '1637.00', 'Latitude': "40.692303", 'Longitude': '-73.988653'}
    df4 = df4.append(uptown, ignore_index=True)
    df4 = df4.append(cinquante, ignore_index=True)
    df4 = df4.append(mideast, ignore_index=True)
    df4 = df4.append(theater, ignore_index=True)
    df4 = df4.append(manhattan, ignore_index=True)
    df4 = df4.append(timesquare, ignore_index=True)
    df4 = df4.append(brooklyn, ignore_index=True)

    map_ny = folium.Map(
        location=[40.723916, -73.994657], tiles="cartodbpositron", zoom_start=12)

    df4 = df4.astype(str)
    df4 = df4.sort_values(by='mean', ascending=False)

    locations2 = df4[['Latitude', 'Longitude']]
    locationlist2 = locations2.values.tolist()

    msg2 = df4['Localisation']
    msglist2 = msg2.values.tolist()

    prix2 = df4['mean']
    prixlist2 = prix2.values.tolist()

    for point in range(10, len(locationlist2)):
        folium.Marker(locationlist2[point],
                      prixlist2[point],
                      msglist2[point], icon=folium.Icon(color="green"),).add_to(map_ny)

    for point in range(4, 10):
        folium.Marker(locationlist2[point],
                      prixlist2[point],
                      msglist2[point], icon=folium.Icon(color="orange"),).add_to(map_ny)

    for point in range(1, 4):
        folium.Marker(locationlist2[point],
                      prixlist2[point],
                      msglist2[point], icon=folium.Icon(color="red"),).add_to(map_ny)

    for point in range(0, 1):
        folium.Marker(locationlist2[point],
                      prixlist2[point],
                      msglist2[point], icon=folium.Icon(color="black"),).add_to(map_ny)

    title_html = '''
             <h3 align="center" style="font-size:20px"><b>Carte distinguant la moyenne des prix des hôtels en fonction de leur quartier.</b></h3>
             '''
    map_ny.get_root().html.add_child(folium.Element(title_html))

    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>Legende</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:green;opacity:1;'></span>Prix Bas</li>
        <li><span style='background:orange;opacity:1;'></span>Prix Moyen</li>
        <li><span style='background:red;opacity:1;'></span>Prix Élevé</li>
        <li><span style='background:black;opacity:1;'></span>Prix très élevé</li>

    </ul>
    </div>
    </div>
    
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    map_ny.get_root().add_child(macro)

    return map_ny


location_ny = map_ny()
location_ny.save("mapNy.html")


class GraphDash3:
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app3 = dash_app
        self.dash_app3.layout = html.Div(children=[
            html.Iframe(id='dash3', srcDoc=open('mapNy.html', 'r').read(), style={
                        'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100vh', 'height': '80vh'}),
        ],)
