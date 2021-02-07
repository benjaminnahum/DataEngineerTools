from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
import dash
from dash import Dash
#from . import app
#app = init_app()
import dash_core_components as dcc
import dash_html_components as html
import pymongo
import dashboard
import dashboardDubai
import dashboardNy
import dashboardLa
import dashboardTokyo
import pandas as pd
import jinja2



from pymongo import MongoClient
from flask import request

from elasticsearch import Elasticsearch

ES_LOCAL = True
es_client = Elasticsearch(hosts=["localhost" if ES_LOCAL else "elasticsearch"])

df2 = pd.read_csv('Export_DataFrame.csv')
df2 = df2.to_dict(orient='records')

client = pymongo.MongoClient()

database = client['df2']

collection = database['products']
collection.delete_many({})
collection.insert_many(df2)

#es_client.indices.delete(index='id', ignore= [400,404])
#json2 = df2.to_dict( orient = 'records')
#collection.insert_many(json2)



app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash/')
dashboard.GraphDash(dash_app=dash_app)

dash_app2 = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash2/')
dashboardDubai.GraphDash2(dash_app=dash_app2)

dash_app3 = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash3/')
dashboardNy.GraphDash3(dash_app=dash_app3)

dash_app4 = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash4/')
dashboardLa.GraphDash4(dash_app=dash_app4)

dash_app5 = dash.Dash(__name__, server=app, routes_pathname_prefix= '/dash5/')
dashboardTokyo.GraphDash5(dash_app=dash_app5)


sem_1 = df2[['Debut']== '2021-02-01']
sem_2 = df2[['Debut']== '2021-02-08']
sem_3 = df2[['Debut']== '2021-02-15']
sem_4 = df2[['Debut']== '2021-02-22']

@app.route('/')
@app.route('/index.html')
def acceuil():
    return render_template('index.html')



@app.route('/dubai.html', methods=['GET','POST'])
def dubai():
    ddubai = collection.find({"id": "Dubaï"})
    response =[]

    for document in ddubai:
        response.append(document)
    
    if request.method == 'POST':    
        query = es_client.search(
        index="hotels",
        body={"query": {"term" : { 'id': 'Dubaï'} }
            }
        )
        [elt['_source'] for elt in query["hits"]["hits"]]
        return render_template('dubai.html', res=query)
    else:
        return render_template("dubai.html", hotels=response)
    
        #es_client.search(index="suggest_product", body=suggest, size=10)
    

    # if request.method == 'POST':
    #     ddubai = collection.find({"id": "Dubaï"})

    #return render_template('dubai.html',du = response)

@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route("/comp.html")
def my_dash_app():
    return render_template('comp.html')

@app.route('/la.html')
def la():
    lla = collection.find({"id": "Los Angeles"})
    response2 =[]
    for document in lla:
        response2.append(document)
        
    if request.method == 'POST':    
        query = es_client.search(
        index="hotels",
        body={query :{"query": {"term" : { 'id': 'Los Angeles'} }}
            }
        )
        [elt['_source'] for elt in query["hits"]["hits"]]
        return render_template('la.html', res=query)
    else:
        return render_template("la.html", hotels=response2)

@app.route('/ny.html')
def ny():
    nny = collection.find({"id": "New York"})
    response3 =[]
    for document in nny:
        response3.append(document)
        
    if request.method == 'POST':    
        query = es_client.search(
        index="hotels",
        body={query :{"query": {"term" : { 'id': 'New York'} }}
            }
        )
        [elt['_source'] for elt in query["hits"]["hits"]]
        return render_template('ny.html', res=query)
    else:
        return render_template("ny.html", hotels=response3)

@app.route('/tokyo.html')
def tokyo():
    ttokyo = collection.find({"id": "Tokyo"})
    response4 =[]
    for document in ttokyo:
        response4.append(document)
        
    if request.method == 'POST':    
        query = es_client.search(
        index="hotels",
        body={query :{"query": {"term" : { 'id': 'Tokyo'} }}
            }
        )
        [elt['_source'] for elt in query["hits"]["hits"]]
        return render_template('tokyo.html', res=query)
    else:
        return render_template("tokyo.html", hotels=response4)


@app.route('/search', methods=['POST'])
def search():

    if request.method == 'POST':
        documentsD = collection.find({"id": "Dubaï", "Debut":'01-02-2021'})
        documentsDD = collection.find({"id": "Dubaï", "Debut":'08-02-2021'})
        documentsDDD = collection.find({"id": "Dubaï", "Debut":'15-02-2021'})
        documentsDDDD = collection.find({"id": "Dubaï", "Debut":'22-02-2021'})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Semaine du 01/02 au 07/02':
            for document in documentsD:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Semaine du 08/02 au 14/02':
            for document in documentsDD:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 15/02 au 21/02':
            for document in documentsDDD:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 22/02 au 28/02':
            for document in documentsDDDD:
                response_4.append(document)
            pass

        return render_template('searchDubai.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)


@app.route('/searchla', methods=['POST'])
def search1():

    if request.method == 'POST':
        documentsD = collection.find({"id": "Los Angeles", "Debut":'01-02-2021'})
        documentsDD = collection.find({"id": "Los Angeles", "Debut":'08-02-2021'})
        documentsDDD = collection.find({"id": "Los Angeles", "Debut":'15-02-2021'})
        documentsDDDD = collection.find({"id": "Los Angeles", "Debut":'22-02-2021'})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Semaine du 01/02 au 07/02':
            for document in documentsD:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Semaine du 08/02 au 14/02':
            for document in documentsDD:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 15/02 au 21/02':
            for document in documentsDDD:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 22/02 au 28/02':
            for document in documentsDDDD:
                response_4.append(document)
            pass

        return render_template('searchLa.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)


@app.route('/searchny', methods=['POST'])
def search2():

    if request.method == 'POST':
        documentsD = collection.find({"id": "New York", "Debut":'01-02-2021'})
        documentsDD = collection.find({"id": "New York", "Debut":'08-02-2021'})
        documentsDDD = collection.find({"id": "New York", "Debut":'15-02-2021'})
        documentsDDDD = collection.find({"id": "New York", "Debut":'22-02-2021'})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Semaine du 01/02 au 07/02':
            for document in documentsD:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Semaine du 08/02 au 14/02':
            for document in documentsDD:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 15/02 au 21/02':
            for document in documentsDDD:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 22/02 au 28/02':
            for document in documentsDDDD:
                response_4.append(document)
            pass

        return render_template('searchNy.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)


@app.route('/searchtokyo', methods=['POST'])
def search3():

    if request.method == 'POST':
        documentsD = collection.find({"id": "Tokyo", "Debut":'01-02-2021'})
        documentsDD = collection.find({"id": "Tokyo", "Debut":'08-02-2021'})
        documentsDDD = collection.find({"id": "Tokyo", "Debut":'15-02-2021'})
        documentsDDDD = collection.find({"id": "Tokyo", "Debut":'22-02-2021'})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Semaine du 01/02 au 07/02':
            for document in documentsD:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Semaine du 08/02 au 14/02':
            for document in documentsDD:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 15/02 au 21/02':
            for document in documentsDDD:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Semaine du 22/02 au 28/02':
            for document in documentsDDDD:
                response_4.append(document)
            pass

        return render_template('searchTokyo.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)

@app.route('/couleurdubai', methods=['POST'])
def couleur():

    if request.method == 'POST':
        couleuR = collection.find({"id":"Dubaï", "prix" : {"$gte": 1500,"$lt" : 2099}})
        couleuRR = collection.find({"id":"Dubaï", "prix" : {"$gte": 2100,"$lt" : 2499}})
        couleuRRR = collection.find({"id":"Dubaï", "prix" : {"$gte": 2500,"$lt" : 2999}})
        couleuRRRR = collection.find({"id":"Dubaï", "prix" : {"$gte": 3000}})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Prix Bas':
            for document in couleuR:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Prix Moyen':
            for document in couleuRR:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Prix Élevé':
            for document in couleuRRR:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Prix très Élevé':
            for document in couleuRRRR:
                response_4.append(document)
            pass

        return render_template('searchDubai.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)

@app.route('/couleurla', methods=['POST'])
def couleur2():

    if request.method == 'POST':
        couleuR = collection.find({"id":"Los Angeles", "prix" : {"$gte": 1800,"$lt" : 1999}})
        couleuRR = collection.find({"id":"Los Angeles", "prix" : {"$gte": 2000,"$lt" : 2550}})
        couleuRRR = collection.find({"id":"Los Angeles", "prix" : {"$gte": 2551,"$lt" : 3200}})
        couleuRRRR = collection.find({"id":"Los Angeles", "prix" : {"$gte": 3201}})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Prix Bas':
            for document in couleuR:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Prix Moyen':
            for document in couleuRR:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Prix Élevé':
            for document in couleuRRR:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Prix très Élevé':
            for document in couleuRRRR:
                response_4.append(document)
            pass

        return render_template('searchLa.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)

@app.route('/couleurny', methods=['POST'])
def couleur3():

    if request.method == 'POST':
        couleuR = collection.find({"id":"New York", "prix" : {"$gte": 1500,"$lt" : 1999}})
        couleuRR = collection.find({"id":"New York", "prix" : {"$gte": 2000,"$lt" : 2999}})
        couleuRRR = collection.find({"id":"New York", "prix" : {"$gte": 3000,"$lt" : 3799}})
        couleuRRRR = collection.find({"id":"New York", "prix" : {"$gte": 3800}})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Prix Bas':
            for document in couleuR:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Prix Moyen':
            for document in couleuRR:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Prix Élevé':
            for document in couleuRRR:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Prix très Élevé':
            for document in couleuRRRR:
                response_4.append(document)
            pass

        return render_template('searchNy.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)

@app.route('/couleurtokyo', methods=['POST'])
def couleur4():

    if request.method == 'POST':
        couleuR = collection.find({"id":"Tokyo", "prix" : {"$gte": 1700,"$lt" : 1999}})
        couleuRR = collection.find({"id":"Tokyo", "prix" : {"$gte": 2000,"$lt" : 2300}})
        couleuRRR = collection.find({"id":"Tokyo", "prix" : {"$gte": 2301,"$lt" : 2999}})
        couleuRRRR = collection.find({"id":"Tokyo", "prix" : {"$gte": 3000}})
        # documentsNY = collection.find({"id" : "New York"})
        # documentsLA = collection.find({"id" : "Los Angeles"})
        # documentsT = collection.find({"id" : "Tokyo"})

        response_1 = []
        response_2 = []
        response_3 = []
        response_4 = []

        
        if request.form['submit_button'] == 'Prix Bas':
            for document in couleuR:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Prix Moyen':
            for document in couleuRR:
                response_2.append(document)
            pass
        elif request.form['submit_button'] == 'Prix Élevé':
            for document in couleuRRR:
                response_3.append(document)
            pass
        elif request.form['submit_button'] == 'Prix très Élevé':
            for document in couleuRRRR:
                response_4.append(document)
            pass

        return render_template('searchTokyo.html',hotels1 = response_1, hotels2 = response_2, hotels3 = response_3, hotels4 = response_4)

@app.route('/sitedubai', methods=['POST'])
def site():

    if request.method == 'POST':
        site = collection.find({"id" : "Dubaï","site" : "expedia"})
        sitee = collection.find({"id" : "Dubaï","site" : "hotels.com"})
        
        response_1 = []
        response_2 = []
        

        
        if request.form['submit_button'] == 'Expedia':
            for document in site:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Hotels.com':
            for document in sitee:
                response_2.append(document)
            pass

        return render_template('searchDubai.html',hotels1 = response_1, hotels2 = response_2)


@app.route('/siteny', methods=['POST'])
def site2():

    if request.method == 'POST':
        site = collection.find({"id" : "New York","site" : "expedia"})
        sitee = collection.find({"id" : "New York","site" : "hotels.com"})
        
        response_1 = []
        response_2 = []
        

        
        if request.form['submit_button'] == 'Expedia':
            for document in site:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Hotels.com':
            for document in sitee:
                response_2.append(document)
            pass

        return render_template('searchNy.html',hotels1 = response_1, hotels2 = response_2)

@app.route('/sitela', methods=['POST'])
def site3():

    if request.method == 'POST':
        site = collection.find({"id" : "Los Angeles","site" : "expedia"})
        sitee = collection.find({"id" : "Los Angeles","site" : "hotels.com"})
        
        response_1 = []
        response_2 = []
        

        
        if request.form['submit_button'] == 'Expedia':
            for document in site:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Hotels.com':
            for document in sitee:
                response_2.append(document)
            pass

        return render_template('searchLa.html',hotels1 = response_1, hotels2 = response_2)

@app.route('/sitetokyo', methods=['POST'])
def site4():

    if request.method == 'POST':
        site = collection.find({"id" : "Tokyo","site" : "expedia"})
        sitee = collection.find({"id" : "Tokyo","site" : "hotels.com"})
        
        response_1 = []
        response_2 = []
        

        
        if request.form['submit_button'] == 'Expedia':
            for document in site:
                response_1.append(document)
            pass 
        elif request.form['submit_button'] == 'Hotels.com':
            for document in sitee:
                response_2.append(document)
            pass

        return render_template('searchTokyo.html',hotels1 = response_1, hotels2 = response_2)






if __name__=='__main__':
     app.run(debug=True)

     