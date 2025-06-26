from flask import jsonify, Blueprint, request, render_template
from models.projet import Projet

project_bp = Blueprint('projet', __name__)

@project_bp.route("/projects")
def index():
    return render_template('/projects/projects.html')

@project_bp.route("/project/new")
def new_form():
    return render_template('/projects/new.html')

@project_bp.route("/project/edit/<int:id>")
def edit_form(id):
    projet = Projet.get_one(id)
    if not projet:
        return render_template('404.html'), 404

    return render_template('/projects/edit.html', projet=projet)

@project_bp.route("/api/projects")
def get_projects():
    projets = Projet.get_all()

    projets_dict = [vars(projet) for projet in projets]
    return jsonify(projets_dict)

@project_bp.route("/api/project/<int:id>")
def get_project(id):
    projet = Projet.get_one(id)
    if projet:
        return jsonify(vars(projet))
    else:
        return jsonify({"error": "Project not found"}), 404

@project_bp.route("/api/project", methods=["POST"])
def create_project():
    data = request.get_json()
    nom_projet = data.get("nom_projet")
    description = data.get("description")

    project_id = Projet.post(nom_projet, description)
    return jsonify({"message": "Project created successfully", "id": project_id}), 201

@project_bp.route("/api/project/<int:id>/edit", methods=["PUT"])
def update_project(id):
    data = request.get_json()
    nom_project = data.get("nom_projet")
    description = data.get("description")
    Projet.put(id, nom_project, description)
    return jsonify({"message": "Project updated successfully"})

@project_bp.route("/api/project/<int:id>/delete", methods=["DELETE"])
def delete_project(id):
    Projet.delete(id)
    return jsonify({"message": "Project deleted successfully"}), 204
