from flask import Flask,render_template
from bs4 import BeautifulSoup # pip3 install bs4 (pour installer la bibliotheque bs4)
from urllib.request import urlopen #Pour lire l'url
app=Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def maFonction():
    return render_template('test.html')

@app.route('/scrapping', methods=("POST", "GET"))
def scrapping():
    url="https://www.sikafinance.com/marches/historiques.aspx?s=BRVMC"
    page=urlopen(url)
    htmlPage=BeautifulSoup(page,'html.parser')
    itemPage = htmlPage.find("table",class_="tablenosort tbl100_6").find_all("td") # tous les td du tableau
    tableau=[]
    tab=[]
    i=0
    for item in itemPage: # dans itemPage il y a tous les td contenus dans la table
        i+=1
        if i==1:        
            tab.append(item.text) # tab[0] correspondra à la date
        elif i==2:        
            tab.append(item.text)# tab[1] correspondra Cloture
        elif i==3:        
            tab.append(item.text)# tab[2] correspondra Plus haut
        elif i==4:        
            tab.append(item.text)
        elif i==5:        
            tab.append(item.text)
        elif i==6:        
            tab.append(item.text)
        elif i==7:        
            tab.append(item.text) # tab[6] correspondra variation %
            tableau.append(tab) # on met un tab de 7 éléments dans tableau
            tab=[] # on reinitialise tab pour le prochain passage
            i=0 # pour récuperer 7 autres
    return render_template('sika.html',tableau=tableau)





if __name__ == "__main__":
    app.run(debug=True) # si on modifie le server ne va pas s'eteindre