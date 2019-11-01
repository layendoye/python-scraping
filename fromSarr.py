from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
import numpy as np
from flask import Flask, request, render_template, session, redirect, url_for
from datetime import datetime


# import warnings

# pour multiple pages
app = Flask(__name__)


@app.route('/', methods=("POST", "GET"))
def acueil():
    return render_template('accueil.html')


# @app.route('/visualisation', methods=("POST", "GET"))
def dat():

    price = []
    refer = []
    poste = []
    typee = []
    lieuu = []
    descriptionn = []
    proprietaire = []
    numeroo = []

    for i in range(1, 2):
        urll = 'https://www.expat-dakar.com/voitures?page='
        url = urll+str(i)
        # url = 'https://www.expat-dakar.com/voitures?page=1'
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        ens_prix = soup.find_all(
            "div", class_='visible-xs-block price-resp-container text-center')
        # print(ens_prix)
        if ens_prix:
                for car in ens_prix:
                    try:
                        prix = car.find("span", class_='prix').text
                        poster = car.find("span", class_='picto-clock').b.text
                        ref = car.find("span", class_='reference').text
                        refe = ref.replace('\t', "")
                        refee = refe.replace('\n', "")
                        pri = prix.replace('\xa0FCFA', "").replace(' ', '')
                        price.append(pri)
                        refer.append(refee)
                        poste.append(poster)
                        # print(prix, ref, poster)
                    except Exception:
                        continue

        description = soup.find_all("div", class_='listing-details-content')
        if description:
            for des in description:
                try:
                    name = des.a.text
                    nam = name.replace('VIP', '')
                    # print(nam)
                    typ = des.find("span", class_='picto').text
                    lieu = des.find(
                        "span", class_='picto picto-place ed-icon-before icon-location').text
                    descript = des.find(
                        "div", class_='description-block').p.text
                    typee.append(typ)
                    lieuu.append(lieu)
                    descriptionn.append(descript)
                    # print(typ,lieu,descript)
                except Exception:
                    continue

        numero = soup.find_all("div", class_='modal-content')
        if numero:
            for num in numero:
                # print(num)
                try:
                    propri = num.find(
                        "h4", class_='modal-title text-center').text
                    a = num.find("div", class_='modal-body text-center')
                    # print(a)
                    # nu = a.find("a", class_='btn btn-primary btn-sm btn-rounded ed-icon-before icon-phone-2 listing-card__contact-phone first-phone')
                    nume = a.span.text
                    # print(nume)
                    proprietaire.append(propri)
                    numeroo.append(nume)
                except Exception:
                    continue
    # print(price)

    # print(proprietaire)
    # print(numeroo)

    data = []
    dff = pd.DataFrame()   # créer un nouveau dataframe
    for s, t, u, v, w, x, y, z, in zip(price, refer, poste, typee, lieuu, descriptionn, proprietaire, numeroo):
        data.append([str(s), str(t), str(u), str(v),
                    str(w), str(x), str(y), str(z)])
    # print(data)
    df = pd.DataFrame(data, columns=("prix", "reference", "jour_poste",
                      "type", "lieu", "description", "proprietaire", "numeroo"))

    q = dff.append(df, ignore_index=True)  # ajouter sur un dataframe
    # print(q)
    dfff = q.drop_duplicates()  # enlever les duplications de lignes
    # print(df)

    # print(df)
        # df = pd.DataFrame({'price': price,
        #                     'ref' : refer,
        #                 'poste': poste,
        #                 })
    # print(df)

    # Format csv
    # import csv

    
    date = datetime.today().strftime('%Y-%m-%d')
    # print(date)
    fil = "expat_dk" + str(date)
    dfff.to_csv("/home/mamadou/Bureau/Cours/cours/M2/Sonatel Academy/scraping/reseaux sociaux/site web/{}.csv".format(fil), header=False)

    # #####################################  PARTIE ANALYSE ####################################################""

    # # #Describe the DataFrame
    a = df.describe()
    # print(a)
    analyses = a.values.tolist()
    analyses[0].insert(0, "count")
    analyses[1].insert(0, "unique")
    analyses[2].insert(0, "top")
    analyses[3].insert(0, "freq")
   
    # print(analyses)

    # # #Show columns
    # # print(df.columns)

    # # #Summary by prix
    prixx = df.groupby('prix')['prix'].count()
    # print(prix)

    # # #Summary by users
    jour_poste = df.groupby('jour_poste')['jour_poste'].count()
    # # print(jour_poste)

    # # #Summary by users
    typee = df.groupby('type')['type'].count()
    # # print(typee)

    # #Summary by lieu
    lieu = df.groupby('lieu')['lieu'].count()
    # # print(lieu)

    # #Summary by proprietaire
    proprietaire = df.groupby('proprietaire')['proprietaire'].count()
    # # print(proprietaire)

    # #Summary by lieu et proprietaire
    lieu_proprietaire = df.groupby('lieu')['proprietaire'].count().nlargest(10)
    # print(lieu_proprietaire)
    nbr = [d for d in lieu_proprietaire]  #
    largest_states = lieu_proprietaire.index.tolist()
    # print(largest_states)
    # print(a)

    # print(a)

    # #Summary by type et proprietaire
    type_proprietaire = df.groupby('type')['proprietaire'].count()
    # # print(type_proprietaire)

    # #Summary by type et prix
    type_prix = df.groupby('prix')['type'].count()
    # # print(type_prix)

    # #Summary by type et proprietaire
    lieu_type = df.groupby('lieu')['type'].count()
    # # print(lieu_type)

        # "  Visualisation de données" ##################""

    # import matplotlib.pyplot as plt
    # plt.style.use('ggplot')

    # #Répartition des propriétaires en fonction des zones

    # lieu_prop=df.groupby('lieu')['proprietaire'].count().nlargest(10) #recupere les 10 personnes qui ont plus de messages
    # # print(lieu_prop)

    # def bar_chart(lieu_prop):
    #     ax = lieu_prop.plot(kind='bar', color = ['red','gold','skyblue','green','orange','teal','cyan','lime','orangered','aqua'], fontsize=12)
    #     ax.set_title("Distribution des propriétaires par zone\n", fontsize=15)
    #     ax.set_xlabel("Zones", fontsize=10)
    #     ax.set_ylabel("Propriétaires", fontsize=10)
    #     # plt.show()

    # bar_chart(lieu_prop)

    # # Répartition

    # lieuu_type=lieu_type.nlargest(10) #recupere les 10 personnes qui ont plus de messages
    # # print(lieuu_type)

    # def bar_chart(lieuu_type):
    #     ax = lieuu_type.plot(kind='bar', color = ['red','gold','skyblue','green','orange','teal','cyan','lime','orangered','aqua'], fontsize=12)
    #     ax.set_title("Distribution des types de vehicules par zone\n", fontsize=15)
    #     ax.set_xlabel("Zones", fontsize=10)
    #     ax.set_ylabel("types de vehicules", fontsize=10)
    #     # plt.show()

    # bar_chart(lieuu_type)

    # ##  Date avec le graphique de ligne de conversation de l'utilisateur

    # date=df.groupby('lieu')['proprietaire'].count().nlargest(10)
    # # print(date)
    # def user_line_chart(date):
    #     ax = date.plot(kind='line',color='green', fontsize=12)
    #     ax.set_title("Distribution des propriétaires par zone\n", fontsize=18)
    #     ax.set_xlabel("Zone", fontsize=12)
    #     ax.set_ylabel("Propriétaires", fontsize=12)
    #     # plt.show()
    # date_count=date[0:]
    # # print(date_count)
    # user_line_chart(date_count)

    # ##  Graphique en secteurs de l'utilisateur

    # user=df.groupby('lieu')['proprietaire'].count().nlargest(10)

    # def user_chat_pie(user):
    #     fig, ax = plt.subplots()
    #     explodex = []
    #     for i in np.arange(len(user)):
    #         explodex.append(0.05)
    #     ax = user.plot(kind='pie', colors = ['teal','orangered','green','red','gold','aqua','skyblue','orange','cyan','lime'], fontsize=12, autopct='%1.1f%%', startangle=180, pctdistance=0.85, explode = explodex)
    #     inner_circle = plt.Circle((0,0),0.70,fc='white')
    #     fig = plt.gcf()
    #     fig.gca().add_artist(inner_circle)
    #     ax.axis('equal')
    #     ax.set_title("Distribution de zones selon les publications\n", fontsize=18)
    #     plt.tight_layout()
    #     plt.show()

    # user_chat_pie(user)

    # print(data)
    # print(type(prix))
    # return data, analyses, largest_states, nbr
    
    return data, analyses, largest_states, nbr
# for i in data:
#     print(i)



#print(type(data))
# print(analyses)
# print(largest_states)
@app.route('/visualisation', methods=("POST", "GET"))
def visualisation():
    data, analyses, largest_states, nbr = dat()
    return render_template('b.html', data=data, analyses=analyses, largest_states=largest_states, nbr=nbr)


@app.route('/data', methods=("POST", "GET"))
def data():
        data, analyses, largest_states, nbr = dat()
        return render_template('datatable.html' , data=data)
    # return redirect(url_for('visualisation'))
        
@app.route('/analyse', methods=("POST", "GET"))
def analyse():
        data, analyses, largest_states, nbr = dat()
        return render_template('data_table_stat.html' , analyses=analyses)

if __name__ == "__main__":
    # db.create_all()

    app.run(debug=True)

