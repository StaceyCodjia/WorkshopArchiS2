import mysql.connector

mydb = mysql.connector.connect(
    host="163.172.165.87",
    user="SAC",
    password="ImAc4RVR",
    database="SAC"
)
mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True)


from flask import Flask, request, render_template, jsonify, abort, url_for, redirect

app = Flask(__name__)

etudiants = []

competences = [
    {"id": 1, "nom": "Python"},
    {"id": 2, "nom": "JavaScript"},
    {"id": 3, "nom": "HTML/CSS"},
    {"id": 4, "nom": "SQL"},
    {"id": 5, "nom": "Machine Learning"}
]

etudiants_competences = []

# @app.route("/")
# def index():
#     return render_template('index.html', etudiants=etudiants)

@app.route("/")
def index():
    # conn = mydb()
    # cursor = conn.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM Etudiant")
    etudiants = mycursor.fetchall()

    return render_template('index.html', etudiants=etudiants)


# @app.route("/new")
# def new():
#     return render_template('/student/new.html', competences=competences)

@app.route("/new", methods=["POST"])
def ajouter_etudiant():
    num_etud = request.form["num_etud"]
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    conn = mydb()
    cursor = conn.cursor()

    query = "INSERT INTO Etudiant (Id, Num_Etudiant, Nom, Prenom) VALUES (%s, %s, %s, %s)"
    # On génère un Id (exemple simple : auto-incrémentation manuelle ici, ou mieux : AUTO_INCREMENT dans ta table plus tard)
    cursor.execute("SELECT MAX(Id) FROM Etudiant")
    last_id = cursor.fetchone()[0]
    new_id = 1 if last_id is None else last_id + 1

    cursor.execute(query, (new_id, num_etud, nom, prenom))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


# @app.route("/reponse", methods=["POST"])
# def traitement():
#     nomEtud = request.form["nom"]
#     prenomEtud = request.form["prenom"]
#     NumEtud = request.form["num_etud"]
#     competences_list = request.form.getlist("competences")

#     etudiants.append({
#         "id": len(etudiants) + 1,
#         "nom": nomEtud,
#         "prenom": prenomEtud,
#         "num_etud": NumEtud
#     })

#     for competence_id in competences_list:
#         competence_id = int(competence_id)
        
#         etudiants_competences.append({
#             "etudiant_id": len(etudiants),
#             "competence_id": competence_id
#         })

#     return redirect(url_for('index'))

@app.route("/reponse", methods=["POST"])
def traitement():
    nomEtud = request.form["nom"]
    prenomEtud = request.form["prenom"]
    NumEtud = request.form["num_etud"]
    competences_list = request.form.getlist("competences")

    conn = mydb()
    cursor = conn.cursor()

    # Insérer l'étudiant
    insert_etudiant = "INSERT INTO etudiant (nom, prenom, num_etud) VALUES (%s, %s, %s)"
    cursor.execute(insert_etudiant, (nomEtud, prenomEtud, NumEtud))
    etudiant_id = cursor.lastrowid

    # Insérer les compétences liées
    insert_comp = "INSERT INTO etudiant_competence (etudiant_id, competence_id) VALUES (%s, %s)"
    for competence_id in competences_list:
        cursor.execute(insert_comp, (etudiant_id, int(competence_id)))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


# @app.route("/details/<int:id>")
# def details(id):
#     if id < 1 or id > len(etudiants):
#         abort(404)
    
#     etudiant = etudiants[id - 1]
#     comp_etud = []
#     for comp in etudiants_competences:
#         if(comp['etudiant_id'] == id):
#             comp_etud.append(comp['competence_id'])

#     competences_etudiant = [c for c in competences if c['id'] in comp_etud]
#     return render_template('/student/details.html', etudiant=etudiant, competences=competences_etudiant)

# @app.route("/details/<int:id>")
# def details(id):
#     conn = mydb()
#     cursor = conn.cursor(dictionary=True)

#     # Récupérer l'étudiant
#     cursor.execute("SELECT * FROM etudiant WHERE id = %s", (id))
#     etudiant = cursor.fetchone()

#     if etudiant is None:
#         abort(404)

#     # Récupérer les compétences de l'étudiant
#     query = """
#         SELECT c.id, c.nom FROM competence c
#         JOIN etudiant_competence ec ON c.id = ec.competence_id
#         WHERE ec.etudiant_id = %s
#     """
#     cursor.execute(query, (id))
#     competences_etudiant = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return render_template('/student/details.html', etudiant=etudiant, competences=competences_etudiant)


@app.route("/edit/<int:id>")
def edit(id):
    etudiant = etudiants[id - 1]
    competence_ids_etudiant = [
        ec["competence_id"] for ec in etudiants_competences if ec["etudiant_id"] == etudiant["id"]
    ]

    return render_template('/student/edit.html', etudiant=etudiant, competences=competences, competence_ids_etudiant=competence_ids_etudiant)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    nomEtud = request.form["nom"]
    prenomEtud = request.form["prenom"]
    NumEtud = request.form["num_etud"]
    competences_list = request.form.getlist("competences")

    etudiants[id - 1] = {
        "id": id,
        "nom": nomEtud,
        "prenom": prenomEtud,
        "num_etud": NumEtud
    }

    global etudiants_competences
    etudiants_competences = [ec for ec in etudiants_competences if ec["etudiant_id"] != id]
    for competence_id in competences_list:
        competence_id = int(competence_id)
        
        etudiants_competences.append({
            "etudiant_id": len(etudiants),
            "competence_id": competence_id
        })

    return redirect(url_for('index'))

# @app.route("/delete/<int:id>")
# def delete(id):
#     if id < 1 or id > len(etudiants):
#         abort(404)
    
#     etudiants.pop(id - 1)
    
#     # Reindex the list
#     for i in range(id - 1, len(etudiants)):
#         etudiants[i]['id'] = i + 1

#     return redirect(url_for('index'))

@app.route("/delete/<int:id>")
def delete(id):
    conn = mydb()
    cursor = conn.cursor()

    # Supprimer les compétences liées
    cursor.execute("DELETE FROM etudiant_competence WHERE etudiant_id = %s", (id))
    # Supprimer l'étudiant
    cursor.execute("DELETE FROM etudiant WHERE id = %s", (id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route("/competence/<int:id>")
def competences_list(id):
    if id < 1 or id > len(etudiants):
        abort(404)

    etudiant = etudiants[id - 1]
    return render_template('/student/competence.html', etudiant=etudiant, competences=competences)

# @app.route("/add_competence/<int:id>", methods=["POST"])
# def add_competence(id):
#     if id < 1 or id > len(etudiants):
#         abort(404)


#     return redirect(url_for('details', id=id))

# @app.route("/delete_competence/<int:etudiant_id>/<int:competence_id>")
# def delete_competence(etudiant_id, competence_id):
#     global etudiants_competences
#     etudiants_competences = [ec for ec in etudiants_competences if not (ec['etudiant_id'] == etudiant_id and ec['competence_id'] == competence_id)]
    
#     return redirect(url_for('details', id=etudiant_id))