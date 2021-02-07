"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc

import plotly_express as px
import pandas as pd
import math
import sys
import re
import plotly
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go
import json
import requests
from flask import Flask


"""Create a Plotly Dash dashboard."""
class GraphDash:
    def __init__(self, dash_app):
        super().__init__()
        self.dash_app = dash_app

        # Load DataFrame
        expedia = pd.read_csv("expedia.csv")
        hotelscom = pd.read_csv('hotelscom.csv',encoding = "utf-8",dayfirst=True)

        expedia['notes'] = 1
        expedia['avis2'] = 1
        expedia = expedia.fillna(0)
        expedia = expedia[["site", "id",'title','dateDepart','dateArrive','localisation','prix','nombreNuits','avis','notes','images']]
        #expedia = expedia.reindex(columns = ["site", "id",'title','dateArrive','dateDepart','localisation','prix','nombreNuits','avis','notes','images'])
        expedia.loc[expedia.nombreNuits == 'pour 6 nuits','nombreNuits'] = '6 nuits'
        expedia.prix = expedia.prix.replace('\D', '', regex=True).astype(int)
        #expedia.images = expedia.images.fillna(0)
        expedia = expedia.rename(columns = {'avis' : 'nombreAvis'})
        expedia = expedia.rename(columns = {'dateDepart' : 'Debut'})
        expedia = expedia.rename(columns = {'dateArrive' : 'Fin'})
        #expedia = expedia.rename(columns = {'avis2' : 'avis'})
        expedia.notes=expedia.nombreAvis
        expedia.notes = expedia.notes.str.split(expand=True)
        expedia.notes = expedia.notes.replace('\D', '', regex=True).astype(int)
        expedia.notes = (expedia.notes/10)*2
        a = expedia.nombreAvis.str.split(expand=True)
        expedia.nombreAvis = expedia.nombreAvis = a[4] + a[5]
        expedia.nombreAvis = expedia.nombreAvis.replace('\D', '', regex=True).astype(int)


        #hotelscom.dateArrive = pd.to_datetime(hotelscom.dateArrive)
        #hotelscom.dateDepart = pd.to_datetime(hotelscom.dateDepart)
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
        #hotelscom = hotelscom.rename(columns = {'avis2' : 'avis'})
        hotelscom.nombreAvis = hotelscom.nombreAvis.fillna(0)
        #hotelscom.notes = hotelscom.notes.fillna(0)
        #hotelscom.notes = hotelscom.notes.astype(str)
        hotelscom.nombreAvis = hotelscom.nombreAvis.replace('\D', '', regex=True).astype(int)
        #hotelscom.nombreAvis = hotelscom.nombreAvis.str.replace(' avis',"")
        hotelscom.notes = hotelscom.notes.replace('\D', '', regex=True).astype(int)
        hotelscom.notes = hotelscom.notes/10
        #hotelscom.nombreAvis = hotelscom.nombreAvis.astype(int)
        hotelscom


        df = pd.concat([expedia,hotelscom])
        df = df.fillna(0)
        df.Debut = pd.to_datetime(df.Debut)
        df.Fin = pd.to_datetime(df.Fin)
        df.loc[df.nombreNuits == 'pour 6 nuits','nombreNuits'] = '6 nuits'
        df.drop(df.loc[df['nombreAvis']==0].index, inplace=True)
        df = df.reset_index()
        df.drop(columns = 'index',inplace = True)
        #df[df.Debut == '2021-01-02'] = df[df.Debut == '2021-02-01']
        #df[df.Debut == '2021-08-02'] = df[df.Debut == '2021-02-08']
        df.nombreAvis = df.nombreAvis.fillna(0)
        #df[df.title == 'The Okura Tokyo']
        df.Debut = df.Debut.astype(str)
        df.Fin = df.Fin.astype(str)

        df_test = df[df['notes']>=9.5]
        df_test2 = df_test.groupby(['site','id']).agg({'notes': np.count_nonzero}).reset_index()

        df_prix = df.groupby(['site','id','Debut']).agg({'prix': np.mean}).reset_index()

        df_nombreavis = df.groupby(['site','id']).agg({'nombreAvis': ['mean']}).reset_index()
        df_nombreavis.columns = ['site','id','NombreAvisMoyenne']

        df_semaine = df.groupby(['site','id','Debut','Fin']).agg({'title': np.count_nonzero}).reset_index()

        df_tokyo = df.groupby(['site','id','title']).agg({'prix': ['mean','min','max']}).reset_index()
        df_tokyo.columns = ['site','id','title','mean','min','max']
        df_tokyo = df_tokyo.sort_values(by = 'mean',ascending=False).reset_index()
        df_tokyo = df_tokyo[df_tokyo.id == 'Tokyo']
        df_tokyo = df_tokyo.drop(df_tokyo.index[[2]])
        df_tokyo = df_tokyo[df_tokyo.id == 'Tokyo'][0:16]


        df_ny = df.groupby(['site','id','title']).agg({'prix': ['mean']}).reset_index()
        df_ny.columns = ['site','id','title','mean']
        #df_title.id = df_title.id[df_title.id == 'Los Angeles']
        df_ny = df_ny.sort_values(by = 'mean',ascending=False).reset_index()
        #df_title = df_title[0:20]
        #df6 = df6.drop('Mandarin Oriental Jumeira, Dubai', axis=0)
        df_ny = df_ny.drop(df_ny.index[[19,34]])
        df_ny = df_ny[df_ny.id == 'New York'][0:12]


        df_dubai = df.groupby(['site','id','title']).agg({'prix': ['mean']}).reset_index()
        df_dubai.columns = ['site','id','title','mean']
        #df_title.id = df_title.id[df_title.id == 'Los Angeles']
        df_dubai = df_dubai.sort_values(by = 'mean',ascending=False).reset_index()
        #df_title = df_title[0:20]
        #df6 = df6.drop('Mandarin Oriental Jumeira, Dubai', axis=0)
        df_dubai = df_dubai.drop(df_dubai.index[[3, 25, 33,50,58,61,64,67,70,82]])
        df_dubai = df_dubai[df_dubai.id == 'Dubaï'][0:10]

        df_la = df.groupby(['site','id','title']).agg({'prix': ['mean','min','max']}).reset_index()
        df_la.columns = ['site','id','title','mean','min','max']
        df_la = df_la.sort_values(by = 'mean',ascending=False)
        df_la = df_la.reset_index()
        df_la = df_la.drop(df_la.index[[13,20,26,43]])
        df_la = df_la[df_la.id == 'Los Angeles'][0:12]


        df_ville = df.groupby(['id','localisation',]).agg({'prix': ['mean']}).reset_index()
        df_ville.columns = ['id','Localisation','mean']
        #df_title.id = df_title.id[df_title.id == 'Los Angeles']
        df_ville = df_ville.sort_values(by = 'mean',ascending=False).reset_index()
        df_ville.drop(columns = 'index',inplace = True)
        df_ville['Latitude'] = 1.0
        df_ville['Longitude'] = 1.0



        # Create Layout
        self.dash_app.layout = html.Div(children=[dcc.Graph(
                                    id='graph1',
                                    figure= {px.bar(df_test2, x="id", y="notes", color="site", category_orders={"site": ["site"]},barmode="group",title = "Nombre d'hôtels ayant une note excellente superieure à 9.5 proposés par expedia et hotels.com en fonction des critères et selon la destination",labels = {"notes": "Meilleures notes d'hotels", "id":"Destination"})

                                    }
                                ),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph2',
                                    figure= {px.bar(df_ny, x="mean", y="title", barmode="group",category_orders={"site": ["site"]},color="site",text = 'mean',title = "Comparaison des prix des hôtels selon expedia et hotels.com pour New York",labels = {"title": "Nom des hôtels", "mean":"Prix Moyen"})}
                                ),

                                #  html.Div(children=f'''
                                #     Moyenne des prix des hotels sur Expedia et Hotels.com en fonction des semaines
                                # ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph3',
                                    figure={px.bar(df_dubai, x="mean", y="title", barmode="group",category_orders={"site": ["site"]},color="site",text = 'mean',title = "Comparaison des prix des hôtels selon expedia et hotels.com pour Dubaï",labels = {"title": "Nom des hôtels", "max":"Prix Max"})}
                                ),

                                    html.Div(children=f'''
                                    Moyenne des prix des hotels sur Expedia et Hotels.com en fonction des semaines
                                ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph4',
                                    figure={px.bar(df_la, x='mean',y="title", barmode="group",category_orders={"site": ["site"]},color="site",text = 'mean',title = "Comparaison des prix des hôtels selon expedia et hotels.com pour Los Angeles",labels = {"title": "Nom des hôtels", "mean":"Prix Moyen"})}
                                ),

                                    html.Div(children=f'''
                                    Moyenne des prix des hotels sur Expedia et Hotels.com en fonction des semaines
                                ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph5',
                                    figure={px.bar(df_tokyo, x='mean',y="title", barmode="group",category_orders={"site": ["site"]},color="site",text = 'mean',title = "Comparaison des prix des hôtels selon expedia et hotels.com pour Tokyo",labels = {"title": "Nom des hôtels", "mean":"Prix Moyen"})}
                                ),
                                

                                # html.Div(children=f'''
                                #     Moyenne des prix des hotels sur Expedia et Hotels.com en fonction des semaines
                                # ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph6',
                                    figure={px.scatter(df_prix, x="id", y="prix", color="site",size = 'prix',animation_frame = 'Debut',size_max=30,title = 'Moyenne des prix des hotels sur Expedia et Hotels.com en fonction des semaines',labels = {"prix": "Prix moyen", "id":"Destination"})}
                                ),
                                
                                    

                                # html.Div(children=f'''
                                # Nombre d'avis moyen sur les hôtels en fonction de la destination
                                # ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                dcc.Graph(
                                    id='graph7',
                                    figure={px.bar(df_nombreavis, x="id", y="NombreAvisMoyenne", color="site", barmode="group",category_orders={"site": ["site"]},title = "Nombre d'avis moyen sur les hôtels en fonction de la destination",labels = {"id": "Destination", "NombreAvisMoyenne":"Nombre d'avis des hôtels par destination"})}
                                ),
                                
                                    

                                # html.Div(children=f'''
                                # Nombre d'hôtels proposés par expedia et hotels.com en fonction des critères et selon la destination
                                # ''',style={'textAlign': 'center'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),

                                # html.H4(children=f"""Plateformes""",
                                #             style={'textAlign': 'center', 'color': 'black'}),

                                html.Br(),
                                html.Br(),
                                html.Br(),          

                                dcc.Graph(
                                    id='graph8',
                                    figure={px.scatter(df_semaine, x="id", y="title", color="site", size = 'title',animation_frame = 'Debut',size_max=30,title = "Nombre d'hôtels proposés par expedia et hotels.com en fonction des critères et selon la destination",labels = {"title": "Nombre d'hôtels proposés", "id":"Destination"})},
                                ),
        ],





        )
