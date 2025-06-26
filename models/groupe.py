from connexion import get_db_connection

class Groupe:
    def __init__(self, id, nom_groupe, nbr_personnes, projet_id):
        self.id = id
        self.nom_groupe = nom_groupe
        self.nbr_personnes = nbr_personnes
        self.projet_id = projet_id

    def get_one(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Groupe WHERE Id = %s", (id,))
        groupe = cursor.fetchone()

        cursor.close()
        conn.close()

        if groupe:
            return Groupe(groupe['Id'], groupe['Nom_Groupe'], groupe['Nbr_Personnes'], groupe['Projet_Id'])
        return None
    
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Groupe")
        groupes = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Groupe(groupe['Id'],groupe['Nom_Groupe'], groupe['Nbr_Personnes'], groupe['Projet_Id']) for groupe in groupes]
    
    def post(nom_groupe, nbr_personnes, projet_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Groupe (Nom_Groupe, Nbr_Personnes, Projet_Id) VALUES (%s, %s, %s)"
        cursor.execute(query, (nom_groupe, nbr_personnes, projet_id))
        conn.commit()

        cursor.close()
        conn.close()

        return cursor.lastrowid
    
    def put(id, nom_groupe, nbr_personnes, projet_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE Groupe SET Nom_Groupe = %s, Nbr_Personnes = %s, Projet_Id = %s WHERE Id = %s"
        cursor.execute(query, (nom_groupe, nbr_personnes, projet_id, id))
        conn.commit()

        cursor.close()
        conn.close()

    def delete(id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM Groupe WHERE Id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        conn.close()