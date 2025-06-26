from connexion import get_db_connection

class EtudiantGroupe:
    def __init__(self, etudiant_id, groupe_id):
        self.etudiant_id = etudiant_id
        self.groupe_id = groupe_id

    def get_all_by_groupe_id(groupe_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT *
        FROM Etudiant
        JOIN Appartient ON Etudiant.Id = Appartient.Etudiant_Id
        WHERE Appartient.Groupe_Id = %s
        """, (groupe_id,))
        
        etudiants = cursor.fetchall()

        cursor.close()
        conn.close()

        return [EtudiantGroupe(etudiant['Id'], groupe_id) for etudiant in etudiants]
    
    def post(etudiant_id, groupe_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Appartient (Etudiant_Id, Groupe_Id) VALUES (%s, %s)"
        cursor.execute(query, (etudiant_id, groupe_id))
        conn.commit()

        cursor.close()
        conn.close()

        return cursor.lastrowid
    
    def put(etudiant_id, groupe_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE Appartient SET Etudiant_Id = %s WHERE Groupe_Id = %s"
        cursor.execute(query, (etudiant_id, groupe_id))
        conn.commit()

        cursor.close()
        conn.close()
    
    def delete_all_by_groupe_id(groupe_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Appartient WHERE Groupe_Id = %s", (groupe_id,))
        conn.commit()

        cursor.close()
        conn.close()