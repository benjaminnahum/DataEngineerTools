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


def map_tokyo():
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

    df_title.loc[df_title.Localisation == 'Chūō', 'latitude'] = '35.665287'
    df_title.loc[df_title.Localisation == 'Chūō', 'longitude'] = '139.775553'
    df_title.loc[df_title.Localisation ==
                 'Kioicho', 'latitude'] = '35.6799049377441'
    df_title.loc[df_title.Localisation ==
                 'Kioicho', 'longitude'] = '139.736892700195'
    df_title.loc[df_title.Localisation ==
                 'Quartier d’affaires Nishi Shinjuku', 'latitude'] = '35.694493'
    df_title.loc[df_title.Localisation ==
                 'Quartier d’affaires Nishi Shinjuku', 'longitude'] = '139.692546'
    df_title.loc[df_title.Localisation ==
                 'Marunouchi', 'latitude'] = '35.684907'
    df_title.loc[df_title.Localisation ==
                 'Marunouchi', 'longitude'] = '139.761945'
    df_title.loc[df_title.Localisation ==
                 'Toranomon', 'latitude'] = '35.670175'
    df_title.loc[df_title.Localisation ==
                 'Toranomon', 'longitude'] = '139.749929'
    df_title.loc[df_title.Localisation == 'Ōtemachi', 'latitude'] = '35.684699'
    df_title.loc[df_title.Localisation ==
                 'Ōtemachi', 'longitude'] = '139.765964'
    df_title.loc[df_title.Localisation == 'Tokyo', 'latitude'] = '35.689487'
    df_title.loc[df_title.Localisation == 'Tokyo', 'longitude'] = '139.691706'
    df_title.loc[df_title.Localisation ==
                 'Uchisaiwaicho', 'latitude'] = '35.6696'
    df_title.loc[df_title.Localisation ==
                 'Uchisaiwaicho', 'longitude'] = '139.7559'
    df_title.loc[df_title.Localisation ==
                 'Nihonbashi', 'latitude'] = '35.683663932'
    df_title.loc[df_title.Localisation ==
                 'Nihonbashi', 'longitude'] = '139.771330248'
    df_title.loc[df_title.Localisation ==
                 'Nagatachō', 'latitude'] = '35.678757'
    df_title.loc[df_title.Localisation ==
                 'Nagatachō', 'longitude'] = '139.740258'
    df_title.loc[df_title.Localisation ==
                 'Nihonbashimuromachi', 'latitude'] = '35.685429'
    df_title.loc[df_title.Localisation ==
                 'Nihonbashimuromachi', 'longitude'] = '139.775383'
    df_title.loc[df_title.Localisation ==
                 'Yūrakuchō', 'latitude'] = '35.673164'
    df_title.loc[df_title.Localisation ==
                 'Yūrakuchō', 'longitude'] = '139.760545'
    df_title.loc[df_title.Localisation == 'Ebisu', 'latitude'] = '35.646643'
    df_title.loc[df_title.Localisation == 'Ebisu', 'longitude'] = '139.710045'

    dfTK = df_title[df_title.id == 'Tokyo']
    map_tk = folium.Map(
        location=[35.674576, 139.741099], tiles="cartodbpositron", zoom_start=12)

    locations3 = dfTK[['latitude', 'longitude']]
    locationlist3 = locations3.values.tolist()

    msg3 = dfTK['Localisation']
    msglist3 = msg3.values.tolist()

    prix3 = dfTK['mean']
    prixlist3 = prix3.values.tolist()

    for point in range(11, len(locationlist3)):
        folium.Marker(locationlist3[point],
                      prixlist3[point],
                      msglist3[point], icon=folium.Icon(color="green"),).add_to(map_tk)

    for point in range(5, 11):
        folium.Marker(locationlist3[point],
                      prixlist3[point],
                      msglist3[point], icon=folium.Icon(color="orange"),).add_to(map_tk)

    for point in range(1, 5):
        folium.Marker(locationlist3[point],
                      prixlist3[point],
                      msglist3[point], icon=folium.Icon(color="red"),).add_to(map_tk)

    for point in range(0, 1):
        folium.Marker(locationlist3[point],
                      prixlist3[point],
                      msglist3[point], icon=folium.Icon(color="black"),).add_to(map_tk)

    title_html = '''
             <h3 align="center" style="font-size:20px"><b>Carte distinguant la moyenne des prix des hôtels en fonction de leur quartier.</b></h3>
             '''
    map_tk.get_root().html.add_child(folium.Element(title_html))

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
        border-radius:6px; padding: 10px; font-size:14px; left: 20px; bottom: 20px;'>
        
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

    map_tk.get_root().add_child(macro)

    return map_tk


location_tokyo = map_tokyo()
location_tokyo.save("mapTokyo.html")


class GraphDash5:
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app5 = dash_app
        self.dash_app5.layout = html.Div(children=[
            html.Iframe(id='dash5', srcDoc=open('mapTokyo.html', 'r', encoding='utf-8').read(), style={
                        'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '100vh', 'height': '80vh'}),
        ], )
