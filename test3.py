from flask import Flask,render_template, request
import pymysql.cursors  # pip install PyMySQL
app=Flask(__name__)

# Connectez- vous à la base de données.
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',                             
                             db='testPython',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
 
print ("connect successful!!")

@app.route('/add', methods=("POST", "GET"))
def add():
    if request.method == "POST":
        details = request.form
        nom = details['nom']
        email = details['email']
        password = details['password']
        telephone = details['telephone']
        cursor = connection.cursor() # mettre try: 
        cursor.execute("INSERT INTO Users(nom, email,telephone,password) VALUES (%s, %s, %s, %s)", (nom, email,telephone,password))
        connection.commit() 
        cursor.close()
        connection.close()
            
    return render_template('formulaire.html')

@app.route('/liste', methods=("POST", "GET"))
def liste():
    cursor = connection.cursor() # mettre try: 
    cursor.execute("SELECT * FROM Users")
    connection.commit() 
    tab=[]
    tableau=[]
    for row in cursor:
        tab.append(row["nom"])
        tab.append(row["telephone"])
        tab.append(row["email"])
        tab.append(row["password"])
        tableau.append(tab)
        tab=[]

    cursor.close()
    connection.close()
    return render_template('liste.html',tableau=tableau)


if __name__ == "__main__":
    app.run(debug=True) # si on modifie le server ne va pas s'eteindre