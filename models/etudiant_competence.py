from connexion import get_db_connection

class EtudiantCompetence:
    def __init__(self, etudiant_id, competence_id):
        self.etudiant_id = etudiant_id
        self.competence_id = competence_id

    def get_competence_of_etudiant(etudiant_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Possede WHERE Etudiant_Id = %s", (etudiant_id,))
        etudiant_competence = cursor.fetchall()

        cursor.close()
        conn.close()

        return [EtudiantCompetence(ec['Etudiant_Id'], ec['Competence_Id']) for ec in etudiant_competence]
    
    def post(etudiant_id, competence_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Possede (Etudiant_Id, Competence_Id) VALUES (%s, %s)"
        cursor.execute(query, (etudiant_id, competence_id))
        conn.commit()

        cursor.close()
        conn.close()

    def delete_all_competences_of_etudiant(etudiant_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Possede WHERE Etudiant_Id = %s", (etudiant_id,))
        conn.commit()

        cursor.close()
        conn.close()