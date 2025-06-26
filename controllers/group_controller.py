from flask import jsonify, Blueprint, request, render_template
from models.groupe import Groupe
from models.projet import Projet

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

    groupes_dict = [vars(groupe) for groupe in groupes]
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

    group_id = Groupe.post(nom_groupe, nbr_personnes, projet_id)
    return jsonify({"message": "Group created successfully", "id": group_id}), 201

@group_bp.route("/api/group/<int:id>/edit", methods=["PUT"])
def update_group(id):
    data = request.get_json()
    nom_groupe = data.get("nom_groupe")
    nbr_personnes = data.get("nbr_personnes")
    projet_id = data.get("projet_id")

    Groupe.put(id, nom_groupe, nbr_personnes, projet_id)
    return jsonify({"message": "Group updated successfully"})

@group_bp.route("/api/group/<int:id>/delete", methods=["DELETE"])
def delete_group(id):
    Groupe.delete(id)
    return jsonify({"message": "Group deleted successfully"}), 204
