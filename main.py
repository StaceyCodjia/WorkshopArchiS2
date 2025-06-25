from flask import Flask
from connexion import create_tables
from controllers.etudiant_controller import etudiant_bp

app = Flask(__name__)
app.register_blueprint(etudiant_bp)

#create_tables()

competences = [
    {"id": 1, "nom": "Python"},
    {"id": 2, "nom": "JavaScript"},
    {"id": 3, "nom": "HTML/CSS"},
    {"id": 4, "nom": "SQL"},
    {"id": 5, "nom": "Machine Learning"}
]

etudiants_competences = []

# @app.route("/competence/<int:id>")
# def competences_list(id):
#     if id < 1 or id > len(etudiants):
#         abort(404)

#     etudiant = etudiants[id - 1]
#     return render_template('/student/competence.html', etudiant=etudiant, competences=competences)

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

if __name__ == "__main__":
    app.run(debug=True)