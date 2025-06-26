from connexion import get_db_connection

class Competence:
    def __init__(self, id, nom_competence):
        self.id = id
        self.nom_competence = nom_competence

    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Competence")
        competences = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Competence(comp['Id'], comp['Nom_Competence']) for comp in competences]
    
    def get_one(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Competence WHERE Id = %s", (id,))
        competence = cursor.fetchone()

        cursor.close()
        conn.close()

        if competence:
            return Competence(competence['Id'], competence['Nom_Competence'])
        return None
    
    def get_by_name(nom_competence):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Competence WHERE Nom_Competence = %s", (nom_competence,))
        competence = cursor.fetchone()

        cursor.close()
        conn.close()

        if competence:
            return Competence(competence['Id'], competence['Nom_Competence'])
        return None
    
    def post(nom_competence):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Competence (Nom_Competence) VALUES (%s)"
        cursor.execute(query, (nom_competence,))
        conn.commit()

        cursor.close()
        conn.close()

    def put(id, nom_competence):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE Competence SET Nom_Competence = %s WHERE Id = %s"
        cursor.execute(query, (nom_competence, id))
        conn.commit()

        cursor.close()
        conn.close()

    def delete(id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Competence WHERE Id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

