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


def map_la():
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

    dubai = pd.read_csv("properties_data.csv")
    df_ville = df.groupby(['id', 'localisation', ]).agg(
        {'prix': ['mean']}).reset_index()
    df_ville.columns = ['id', 'Localisation', 'mean']
    df_ville = df_ville.sort_values(by='mean', ascending=False).reset_index()
    df_ville.drop(columns='index', inplace=True)
    df_ville['Latitude'] = 1.0
    df_ville['Longitude'] = 1.0

    df_title = df.groupby(['id', 'localisation', ]).agg(
        {'prix': ['mean']}).reset_index()
    df_title.columns = ['id', 'Localisation', 'mean']
    df_title = df_title.sort_values(by='mean', ascending=False).reset_index()
    df_title.drop(columns='index', inplace=True)
    df_title['latitude'] = 0
    df_title['longitude'] = 0

    df_title.loc[df_title.Localisation ==
                 'Santa Monica', 'latitude'] = '34.008991'
    df_title.loc[df_title.Localisation ==
                 'Santa Monica', 'longitude'] = '-118.497269'
    df_title.loc[df_title.Localisation ==
                 'Rancho Palos Verdes', 'latitude'] = '33.7531'
    df_title.loc[df_title.Localisation ==
                 'Rancho Palos Verdes', 'longitude'] = '-118.367'
    df_title.loc[df_title.Localisation ==
                 'Beverly Hills', 'latitude'] = '34.067213'
    df_title.loc[df_title.Localisation ==
                 'Beverly Hills', 'longitude'] = '-118.400028'
    df_title.loc[df_title.Localisation == 'Pasadena', 'latitude'] = '33.7866'
    df_title.loc[df_title.Localisation ==
                 'Pasadena', 'longitude'] = '-118.2987'
    df_title.loc[df_title.Localisation ==
                 'West Hollywood', 'latitude'] = '34.0883'
    df_title.loc[df_title.Localisation ==
                 'West Hollywood', 'longitude'] = '-118.372'
    df_title.loc[df_title.Localisation ==
                 'Los Angeles', 'latitude'] = '34.052234'
    df_title.loc[df_title.Localisation ==
                 'Los Angeles', 'longitude'] = '-118.243685'
    df_title.loc[df_title.Localisation ==
                 'Thousand Oaks', 'latitude'] = '34.1933'
    df_title.loc[df_title.Localisation ==
                 'Thousand Oaks', 'longitude'] = '-118.874'
    df_title.loc[df_title.Localisation ==
                 'Marina del Rey', 'latitude'] = '33.7866'
    df_title.loc[df_title.Localisation ==
                 'Marina del Rey', 'longitude'] = '-118.2987'
    df_title.loc[df_title.Localisation ==
                 'Centre-ville de Los Angeles', 'latitude'] = '34.003342'
    df_title.loc[df_title.Localisation ==
                 'Centre-ville de Los Angeles', 'longitude'] = '-118.485832'
    df_title.loc[df_title.Localisation == 'Bel Air', 'latitude'] = '34.0833418'
    df_title.loc[df_title.Localisation ==
                 'Bel Air', 'longitude'] = '-118.4486913'
    df_title.loc[df_title.Localisation ==
                 'The Flats', 'latitude'] = '34.077457'
    df_title.loc[df_title.Localisation ==
                 'The Flats', 'longitude'] = '-118.406049'
    df_title.loc[df_title.Localisation ==
                 'Ocean Park', 'latitude'] = '34.0022327'
    df_title.loc[df_title.Localisation ==
                 'Ocean Park', 'longitude'] = '-118.4836906'
    df_title.loc[df_title.Localisation ==
                 'Norma Triangle', 'latitude'] = '34.08732'
    df_title.loc[df_title.Localisation ==
                 'Norma Triangle', 'longitude'] = '-118.38558'
    df_title.loc[df_title.Localisation == 'Downtown', 'latitude'] = '34.041742'
    df_title.loc[df_title.Localisation ==
                 'Downtown', 'longitude'] = '-118.246893'
    df_title.loc[df_title.Localisation ==
                 'Beverly Grove', 'latitude'] = '34.074499'
    df_title.loc[df_title.Localisation ==
                 'Beverly Grove', 'longitude'] = '-118.371635'

    dfLA = df_title[df_title.id == 'Los Angeles']

    map_la = folium.Map(
        location=[34.003342, -118.485832], tiles="cartodbpositron", zoom_start=9)

    locations = dfLA[['latitude', 'longitude']]
    locationlist = locations.values.tolist()

    msg = dfLA['Localisation']
    msglist = msg.values.tolist()

    prix = dfLA['mean']
    prixlist = prix.values.tolist()

    for point in range(11, len(locationlist)):
        folium.Marker(locationlist[point],
                      prixlist[point],
                      msglist[point], icon=folium.Icon(color="green"),).add_to(map_la)

    for point in range(7, 11):
        folium.Marker(locationlist[point],
                      prixlist[point],
                      msglist[point], icon=folium.Icon(color="orange"),).add_to(map_la)

    for point in range(2, 7):
        folium.Marker(locationlist[point],
                      prixlist[point],
                      msglist[point], icon=folium.Icon(color="red"),).add_to(map_la)

    for point in range(0, 2):
        folium.Marker(locationlist[point],
                      prixlist[point],
                      msglist[point], icon=folium.Icon(color="black"),).add_to(map_la)

    title_html = '''
             <h3 align="center" style="font-size:20px"><b>Carte distinguant la moyenne des prix des hôtels en fonction de leur quartier.</b></h3>
             '''
    map_la.get_root().html.add_child(folium.Element(title_html))

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

    map_la.get_root().add_child(macro)

    return map_la


location_la = map_la()
location_la.save("mapLa.html")


class GraphDash4:
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app4 = dash_app
        self.dash_app4.layout = html.Div(children=[
            html.Iframe(id='dash4', srcDoc=open('mapLa.html', 'r').read(), style={
                        'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100vh', 'height': '80vh'}),

        ],)
