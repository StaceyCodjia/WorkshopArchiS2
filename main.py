from flask import Flask, request, render_template, jsonify, abort, url_for, redirect

app = Flask(__name__)

etudiants = []

@app.route("/")
def index():
    return render_template('index.html', etudiants=etudiants)

@app.route("/new")
def new():
    return render_template('/student/new.html')

@app.route("/reponse", methods=["POST"])
def traitement():
    nomEtud = request.form["nom"]
    prenomEtud = request.form["prenom"]
    NumEtud = request.form["num_etud"]

    etudiants.append({
        "id": len(etudiants) + 1,
        "nom": nomEtud,
        "prenom": prenomEtud,
        "num_etud": NumEtud
    })

    return redirect(url_for('index'))

@app.route("/edit/<int:id>")
def edit(id):
    etudiant = etudiants[id - 1]
    return render_template('/student/edit.html', etudiant=etudiant)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    nomEtud = request.form["nom"]
    prenomEtud = request.form["prenom"]
    NumEtud = request.form["num_etud"]

    etudiants[id - 1] = {
        "id": id,
        "nom": nomEtud,
        "prenom": prenomEtud,
        "num_etud": NumEtud
    }

    return redirect(url_for('index'))