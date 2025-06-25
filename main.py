from flask import Flask
from connexion import create_tables
from controllers.etudiant_controller import etudiant_bp

app = Flask(__name__)
app.register_blueprint(etudiant_bp)

create_tables()

if __name__ == "__main__":
    app.run(debug=True)