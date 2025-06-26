from flask import Flask
from connexion import create_tables
from controllers.etudiant_controller import etudiant_bp
from controllers.project_controller import project_bp
from controllers.group_controller import group_bp

app = Flask(__name__)
app.register_blueprint(etudiant_bp)
app.register_blueprint(project_bp)
app.register_blueprint(group_bp)

create_tables()

if __name__ == "__main__":
    app.run(debug=True)