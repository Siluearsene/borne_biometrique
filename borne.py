from flask import Flask, render_template,request
import secrets 
import psycopg2

app = Flask(__name__)

secret_key = secrets.token_hex(16)

@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        adresse_ip = request.form.get('addresse_ip')
        port = request.form.get('port')
        lieu = request.form.get('lieu')
        print('kw', adresse_ip, port, lieu)
        # Connexion à la base de données
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='borne',
            user='borne',
            password='1234'
        )
        cursor = conn.cursor()

        # Requête d'insertion
        insert_query = "INSERT INTO borneregister (addresse_ip, port, lieu) VALUES (%s, %s, %s)"
        values = (adresse_ip, port, lieu)

        # Exécution de la requête
        cursor.execute(insert_query, values)
        conn.commit()

        # Fermeture de la connexion à la base de données
        cursor.close()
        conn.close()

        return render_template('index.html')

    # Si la méthode de requête est GET, afficher simplement le formulaire
    return render_template('index.html')

# ...


@app.route("/home")
def acceuil():
    return render_template('index.html')

@app.route("/crud",methods=['GET', 'POST'])
def crud():
    # Connexion à la base de données
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='borne',
        user='borne',
        password='1234'
    )
    cursor = conn.cursor()

    # Exécution d'une requête pour récupérer les données
    select_query = "SELECT * FROM borneregister"
    cursor.execute(select_query)
    data = cursor.fetchall()

    # Fermeture de la connexion à la base de données
    cursor.close()
    conn.close()

    return render_template('crud.html', data=data)



app.config['SECRET_KEY'] = secret_key

# Configuration de la base de données PostgreSQL
db_connection = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'borne',
    'user': 'borne',
    'password': '1234'
}


if __name__ == "__main__":
   app.run(debug = True )