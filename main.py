from flask import Flask, request, render_template, jsonify, abort, url_for, redirect

app = Flask(__name__)

etudiants = []

@app.route("/")
def index():
    return render_template('index.html', etudiants=etudiants)

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/reponse", methods=["POST"])
def traitement():
    nomEtud = request.form["nom"]
    prenomEtud = request.form["prenom"]
    NumEtud = request.form["num-etud"]

    etudiants.append({
        "nom": nomEtud,
        "prenom": prenomEtud,
        "num-etud": NumEtud
    })

    return redirect(url_for('index'))