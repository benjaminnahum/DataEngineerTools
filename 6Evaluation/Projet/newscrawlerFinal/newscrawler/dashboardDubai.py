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



def map_dubai():
    expedia = pd.read_csv("expedia.csv")
    hotelscom = pd.read_csv('hotelscom.csv',encoding = "utf-8",dayfirst=True)

    expedia['notes'] = 1
    expedia['avis2'] = 1
    expedia = expedia.fillna(0)
    expedia = expedia[["site", "id",'title','dateDepart','dateArrive','localisation','prix','nombreNuits','avis','notes','images']]
    expedia.loc[expedia.nombreNuits == 'pour 6 nuits','nombreNuits'] = '6 nuits'
    expedia.prix = expedia.prix.replace('\D', '', regex=True).astype(int)
    expedia = expedia.rename(columns = {'avis' : 'nombreAvis'})
    expedia = expedia.rename(columns = {'dateDepart' : 'Debut'})
    expedia = expedia.rename(columns = {'dateArrive' : 'Fin'})

    expedia.notes=expedia.nombreAvis
    expedia.notes = expedia.notes.str.split(expand=True)
    expedia.notes = expedia.notes.replace('\D', '', regex=True).astype(int)
    expedia.notes = (expedia.notes/10)*2
    a = expedia.nombreAvis.str.split(expand=True)
    expedia.nombreAvis = expedia.nombreAvis = a[4] + a[5]
    expedia.nombreAvis = expedia.nombreAvis.replace('\D', '', regex=True).astype(int)


    hotelscom = hotelscom.fillna(0)
    hotelscom.dateDepart = pd.to_datetime(hotelscom.dateDepart,dayfirst=True)
    hotelscom.dateArrive = pd.to_datetime(hotelscom.dateArrive,dayfirst=True)
    hotelscom.loc[hotelscom.nombreNuits == 'pour 1 chambre pour 6 nuits','nombreNuits'] = '6 nuits'
    hotelscom.prix = hotelscom.prix.str.strip(" €")
    hotelscom.prixbis = hotelscom.prixbis.str.strip(" €")
    hotelscom.prix = hotelscom.prix.fillna(0)
    hotelscom.prixbis = hotelscom.prixbis.fillna(0)
    hotelscom.prix = hotelscom.prix.replace('\D', '', regex=True).astype(int)
    hotelscom.prixbis = hotelscom.prixbis.replace('\D', '', regex=True).astype(int)
    hotelscom['prixfinal'] = hotelscom.prix + hotelscom.prixbis
    hotelscom.drop(columns = 'prix',inplace = True)
    hotelscom.drop(columns = 'prixbis',inplace = True)
    hotelscom = hotelscom[["site", "id",'title','dateArrive','dateDepart','localisation','prixfinal','nombreNuits','avis','notes','images']]
    hotelscom = hotelscom.rename(columns = {'prixfinal' : 'prix'})
    hotelscom = hotelscom.rename(columns = {'avis' : 'nombreAvis'})
    hotelscom = hotelscom.rename(columns = {'dateArrive' : 'Debut'})
    hotelscom = hotelscom.rename(columns = {'dateDepart' : 'Fin'})

    hotelscom.nombreAvis = hotelscom.nombreAvis.fillna(0)
    hotelscom.nombreAvis = hotelscom.nombreAvis.replace('\D', '', regex=True).astype(int)
    hotelscom.notes = hotelscom.notes.replace('\D', '', regex=True).astype(int)
    hotelscom.notes = hotelscom.notes/10

    df = pd.concat([expedia,hotelscom])
    df = df.fillna(0)
    df.Debut = pd.to_datetime(df.Debut)
    df.Fin = pd.to_datetime(df.Fin)
    df.loc[df.nombreNuits == 'pour 6 nuits','nombreNuits'] = '6 nuits'
    df.drop(df.loc[df['nombreAvis']==0].index, inplace=True)
    df = df.reset_index()
    df.drop(columns = 'index',inplace = True)

    dubai = pd.read_csv("properties_data.csv")
    df_ville = df.groupby(['id','localisation',]).agg({'prix': ['mean']}).reset_index()
    df_ville.columns = ['id','Localisation','mean']
    df_ville = df_ville.sort_values(by = 'mean',ascending=False).reset_index()
    df_ville.drop(columns = 'index',inplace = True)
    df_ville['Latitude'] = 1.0
    df_ville['Longitude'] = 1.0




    dubai = dubai[['neighborhood','latitude','longitude']]
    dubai = dubai.rename(columns = {'neighborhood' : 'Localisation'})
    dubai = dubai.rename(columns = {'latitude' : 'Latitude'})
    dubai = dubai.rename(columns = {'longitude' : 'Longitude'})
    dubai['mean'] =1.0
    dubai['id'] ='a'
    dubai.columns = ['Localisation','Latitude','Longitude','mean','id']
    dubai = dubai[['id','Localisation','mean','Latitude','Longitude']]


    df_dubai = df.groupby(['id','localisation',]).agg({'prix': ['mean']}).reset_index()
    df_dubai.columns = ['id','Localisation','mean']
    df_dubai = df_dubai.sort_values(by = 'mean',ascending=False).reset_index()
    df_dubai.drop(columns = 'index',inplace = True)
    df_dubai['Latitude'] = 1.0
    df_dubai['Longitude'] = 1.0


    dubai2 = pd.merge(df_ville,dubai,on='Localisation',how='right')
    dubai2 = dubai2.fillna(0)
    dubai2 = dubai2[(dubai2 != 0).all(1)]

    dubai2 = dubai2.rename(columns = {'Latitude_y' : 'Latitude'})
    dubai2 = dubai2.rename(columns = {'Longitude_y' : 'Longitude'})
    dubai2 = dubai2.rename(columns = {'Latitude_x' : 'La'})
    dubai2 = dubai2.rename(columns = {'Longitude_x' : 'Long'})


    dubai2=dubai2.groupby((dubai2.Localisation != dubai2.Localisation.shift()).cumsum().values).first().reset_index()
    dubai2.drop(columns = 'La',inplace = True)
    dubai2.drop(columns = 'Long',inplace = True)
    dubai2.drop(columns = 'mean_y',inplace = True)
    dubai2.drop(columns = 'index',inplace = True)
    dubai2.drop(columns = 'id_y',inplace = True)
    dubai2 = dubai2.rename(columns = {'id_x' : 'id'})
    dubai2 = dubai2.rename(columns = {'mean_x' : 'mean'})

    downtown = {'id':'Dubaï','Localisation':'Downtown Dubaï','mean':'3695.00','Latitude':"25.194935",'Longitude':'55.282665'}
    jebel = {'id':'Dubaï','Localisation':'Jebel Ali','mean':'2993.25','Latitude':"24.948068",'Longitude':'55.069311'}
    alsufouh1 = {'id':'Dubaï','Localisation':'Al Sufouh 1','mean':'2863.3','Latitude':"25.120920",'Longitude':'55.182731'}
    wtc = {'id':'Dubaï','Localisation':"World Trade Center",'mean':'2863.3','Latitude':"25.223728",'Longitude':'55.285118'}
    dubai = {'id':'Dubaï','Localisation':'Centre Ville de Dubaï','mean':'2840.00','Latitude':"25.198518",'Longitude':'55.279619'}
    ummsuqeim3 = {'id':'Dubaï','Localisation':'Umm Suqeim 3','mean':'2134.375','Latitude':"25.138546",'Longitude':'55.194301'}
    marina = {'id':'Dubaï','Localisation':'Marina de Dubaï','mean':'1637.00','Latitude':"25.079225",'Longitude':'55.135536'}
    deira = {'id':'Dubaï','Localisation':'Deira','mean':'1637.00','Latitude':"25.283769",'Longitude':'55.330409'}
    dubai2 = dubai2.append(downtown,ignore_index=True)
    dubai2 = dubai2.append(alsufouh1,ignore_index=True)
    dubai2 = dubai2.append(jebel,ignore_index=True)
    dubai2 = dubai2.append(wtc,ignore_index=True)
    dubai2 = dubai2.append(dubai,ignore_index=True)
    dubai2 = dubai2.append(ummsuqeim3,ignore_index=True)
    dubai2 = dubai2.append(marina,ignore_index=True)
    dubai2 = dubai2.append(deira,ignore_index=True)

    map_du=folium.Map(location=[25.2048493,55.2707828],tiles="cartodbpositron",zoom_start=10)
    

    dubai2 = dubai2.astype(str)
    dubai2 = dubai2.sort_values(by = 'mean', ascending=False)

    locations4 = dubai2[['Latitude', 'Longitude']]
    locationlist4 = locations4.values.tolist()

    msg4 = dubai2['Localisation']
    msglist4= msg4.values.tolist()

    prix4 = dubai2['mean']
    prixlist4= prix4.values.tolist()


    map_du=folium.Map(location=[25.132290,55.252421],tiles="cartodbpositron",zoom_start=10)

    for point in range(9, len(locationlist4)):
        folium.Marker(locationlist4[point],
        prixlist4[point], 
        msglist4[point], icon=folium.Icon(color="green"),).add_to(map_du)

    for point in range(8, 9):
        folium.Marker(locationlist4[point],
        prixlist4[point], 
        msglist4[point], icon=folium.Icon(color="orange"),).add_to(map_du)

    for point in range(3, 8):
        folium.Marker(locationlist4[point],
        prixlist4[point], 
        msglist4[point], icon=folium.Icon(color="red"),).add_to(map_du)

    for point in range(0, 3):
        folium.Marker(locationlist4[point],
        prixlist4[point], 
        msglist4[point], icon=folium.Icon(color="black"),).add_to(map_du)
    
    title_html = '''
             <h3 align="center" style="font-size:20px"><b>Carte distinguant la moyenne des prix des hôtels en fonction de leur quartier.</b></h3>
             '''
    map_du.get_root().html.add_child(folium.Element(title_html))

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

    map_du.get_root().add_child(macro)


    
    return map_du


location_dubai = map_dubai()
location_dubai.save("mapDubai.html")


class GraphDash2:   
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app2 = dash_app
        self.dash_app2.layout = html.Div(children=[
        html.Iframe(id = 'dash2', srcDoc = open('mapDubai.html', 'r').read(), style={'display': 'block','margin-left': 'auto','margin-right': 'auto','width': '100vh', 'height': '80vh'}),
        
        ],)

   
        




