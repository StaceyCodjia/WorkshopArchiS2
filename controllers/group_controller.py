from flask import jsonify, Blueprint, request, render_template
from models.groupe import Groupe
from models.projet import Projet
from models.etudiant import Etudiant
from models.etudiant_groupe import EtudiantGroupe
from models.etudiant_competence import EtudiantCompetence
from models.competence import Competence

group_bp = Blueprint('groupe', __name__)

@group_bp.route("/groups")
def index():
    return render_template('/groups/groups.html')

@group_bp.route("/group/new")
def new_form():
    return render_template('/groups/new.html')

@group_bp.route("/group/edit/<int:id>")
def edit_form(id):
    groupe = Groupe.get_one(id)
    if not groupe:
        return render_template('404.html'), 404

    return render_template('/groups/edit.html', groupe=groupe)

@group_bp.route("/api/groups")
def get_groups():
    groupes = Groupe.get_all()

    for groupe in groupes:
        projet = Projet.get_one(groupe.projet_id)
        groupe.nom_projet = projet.nom_projet if projet else None

        groupe.etudiants = EtudiantGroupe.get_all_by_groupe_id(groupe.id)
        for etudiant in groupe.etudiants:
            infos = Etudiant.get_one(etudiant.etudiant_id)
            comp_ids = EtudiantCompetence.get_competence_of_etudiant(etudiant.etudiant_id)
            etudiant.competences = []
            for comp_id in comp_ids:
                comp = Competence.get_one(comp_id.competence_id)
                if comp:
                    etudiant.competences.append({"nom": comp.nom_competence})
            etudiant.nom = infos.nom if infos else None
            etudiant.prenom = infos.prenom if infos else None
            etudiant.num_etudiant = infos.num_etudiant if infos else None

    # Pour sérialiser proprement, transforme chaque étudiant en dict
    def etudiant_to_dict(etudiant):
        return {
            "id": etudiant.etudiant_id,
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "num_etudiant": etudiant.num_etudiant,
            "competences": etudiant.competences
        }

    groupes_dict = []
    for groupe in groupes:
        groupes_dict.append({
            "id": groupe.id,
            "nom_groupe": groupe.nom_groupe,
            "nbr_personnes": groupe.nbr_personnes,
            "nom_projet": groupe.nom_projet,
            "etudiants": [etudiant_to_dict(e) for e in groupe.etudiants]
        })

    return jsonify(groupes_dict)

@group_bp.route("/api/group/<int:id>")
def get_group(id):
    groupe = Groupe.get_one(id)
    if groupe:
        return jsonify(vars(groupe))
    else:
        return jsonify({"error": "Group not found"}), 404

@group_bp.route("/api/group", methods=["POST"])
def create_group():
    data = request.get_json()
    nom_groupe = data.get("nom_groupe")
    nbr_personnes = data.get("nbr_personnes")
    projet_id = data.get("projet_id")
    etudiants = data.get("etudiants", [])

    group_id = Groupe.post(nom_groupe, nbr_personnes, projet_id)

    for etudiant_id in etudiants:
        EtudiantGroupe.post(etudiant_id, group_id)

    return jsonify({"message": "Group created successfully", "id": group_id}), 201

@group_bp.route("/api/group/<int:id>/edit", methods=["PUT"])
def update_group(id):
    data = request.get_json()
    nom_groupe = data.get("nom_groupe")
    nbr_personnes = data.get("nbr_personnes")
    projet_id = data.get("projet_id")
    etudiants = data.get("etudiants", [])

    Groupe.put(id, nom_groupe, nbr_personnes, projet_id)

    EtudiantGroupe.delete_all_by_groupe_id(id)
    for etudiant_id in etudiants:
        EtudiantGroupe.post(etudiant_id, id)

    return jsonify({"message": "Group updated successfully"})

@group_bp.route("/api/group/<int:id>/delete", methods=["DELETE"])
def delete_group(id):
    EtudiantGroupe.delete_all_by_groupe_id(id)
    Groupe.delete(id)
    return jsonify({"message": "Group deleted successfully"}), 204
