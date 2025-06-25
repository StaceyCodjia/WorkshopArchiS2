from connexion import get_db_connection

class Etudiant:
    def __init__(self, id, num_etudiant, nom, prenom):
        self.id = id
        self.num_etudiant = num_etudiant
        self.nom = nom
        self.prenom = prenom

    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Etudiant")
        etudiants = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Etudiant(etudiants['Id'], etudiants['Num_Etudiant'], etudiants['Nom'], etudiants['Prenom']) for etudiants in etudiants]

    def get_one(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Etudiant WHERE Id = %s", (id,))
        etudiant = cursor.fetchone()

        cursor.close()
        conn.close()

        if etudiant:
            return Etudiant(etudiant['Id'], etudiant['Num_Etudiant'], etudiant['Nom'], etudiant['Prenom'])
        return None

    def post(num_etudiant, nom, prenom):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Etudiant (Num_Etudiant, Nom, Prenom) VALUES (%s, %s, %s)"
        cursor.execute(query, (num_etudiant, nom, prenom))
        conn.commit()

        cursor.close()
        conn.close()

    def put(id, num_etudiant, nom, prenom):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE Etudiant SET Num_Etudiant = %s, Nom = %s, Prenom = %s WHERE Id = %s"
        cursor.execute(query, (num_etudiant, nom, prenom, id))
        conn.commit()

        cursor.close()
        conn.close()

    def delete(id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Etudiant WHERE Id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()