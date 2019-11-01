from flask import Flask,render_template
from bs4 import BeautifulSoup # pip3 install bs4 (pour installer la bibliotheque bs4)
from urllib.request import urlopen #Pour lire l'url
app=Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def maFonction():
    return render_template('brvm.html')

@app.route('/scrapping', methods=("POST", "GET"))
def scrapping():
    url="http://www.brvm.org"
    page=urlopen(url)
    htmlPage=BeautifulSoup(page,'html.parser')
    itemPage = htmlPage.find_all("div", class_='item')
    tableau=[]
    tab=[]
    # ne pas oublier oublier les try catch
    for item in itemPage:
        content=item.find_all("span")
        i=0
        for valeur in content:
            print(valeur.text)
            i+=1
            if i==1:        
                tab.append(valeur.text)
            elif i==2:        
                tab.append(valeur.text)
            elif i==3:        
                tab.append(valeur.text) # tab[2] correspondra variation %
                tableau.append(tab) # on met un tab de 3 éléments dans tableau
            elif i==4: # car il y a un espace
                tab=[] # on reinitialise tab pour le prochain passage
                i=0

    return render_template('brvm.html',tableau=tableau)

if __name__ == "__main__":
    app.run(debug=True) # si on modifie le server ne va pas s'eteindre