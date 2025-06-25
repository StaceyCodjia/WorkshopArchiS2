from flask import jsonify, Blueprint, request, render_template
from models.etudiant import Etudiant
from models.etudiant_competence import EtudiantCompetence
from models.competence import Competence

etudiant_bp = Blueprint('etudiant', __name__)

@etudiant_bp.route("/")
def index():
    return render_template('index.html')

@etudiant_bp.route("/etudiant/new")
def new_form():
    competences = Competence.get_all()
    return render_template('/student/new.html', competences=competences)

@etudiant_bp.route("/etudiant/edit/<int:id>")
def edit_form(id):
    etudiant = Etudiant.get_one(id)
    if not etudiant:
        return render_template('404.html'), 404

    competence_objs = EtudiantCompetence.get_competence_of_etudiant(etudiant.id)
    competence_ids_etudiant = [c.competence_id for c in competence_objs]
    competences = Competence.get_all()
    return render_template('/student/edit.html', etudiant=etudiant, competences=competences, competence_ids_etudiant=competence_ids_etudiant)

@etudiant_bp.route("/api/etudiants")
def get_etudiants():
    etudiants = Etudiant.get_all()

    for etudiant in etudiants:
        etudiant.competences = []
        etu_comps = EtudiantCompetence.get_competence_of_etudiant(etudiant.id)
        for etu_comp in etu_comps:
            competence = Competence.get_one(etu_comp.competence_id)
            if competence:
                etudiant.competences.append({"nom": competence.nom_competence})

    etudiants_dict = [vars(etudiant) for etudiant in etudiants]
    return jsonify(etudiants_dict)

@etudiant_bp.route("/api/etudiant/<int:id>")
def get_etudiant(id):
    etudiant = Etudiant.get_one(id)
    if etudiant:
        return jsonify(vars(etudiant))
    else:
        return jsonify({"error": "Etudiant not found"}), 404

@etudiant_bp.route("/api/etudiant", methods=["POST"])
def create_etudiant():
    data = request.get_json()
    num_etudiant = data.get("num_etudiant")
    nom = data.get("nom")
    prenom = data.get("prenom")
    competences = data.get("competences", [])

    etudiant = Etudiant.post(num_etudiant, nom, prenom)
    for competence_id in competences:
        EtudiantCompetence.post(etudiant.id, competence_id)
    return jsonify({"message": "Etudiant created successfully"}), 201

@etudiant_bp.route("/api/etudiant/<int:id>/edit", methods=["PUT"])
def update_etudiant(id):
    data = request.get_json()
    num_etudiant = data.get("num_etudiant")
    nom = data.get("nom")
    prenom = data.get("prenom")
    competences = data.get("competences", [])

    Etudiant.put(id, num_etudiant, nom, prenom)
    EtudiantCompetence.delete_all_competences_of_etudiant(id)
    for competence_id in competences:
        EtudiantCompetence.post(id, competence_id)
    return jsonify({"message": "Etudiant updated successfully"})

@etudiant_bp.route("/api/etudiant/<int:id>/delete", methods=["DELETE"])
def delete_etudiant(id):
    EtudiantCompetence.delete_all_competences_of_etudiant(id)
    Etudiant.delete(id)
    return jsonify({"message": "Etudiant deleted successfully"}), 204
