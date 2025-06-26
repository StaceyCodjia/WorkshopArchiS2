from connexion import get_db_connection

class Projet:
    def __init__(self, id, nom_projet, description):
        self.id = id
        self.nom_projet = nom_projet
        self.description = description

    def get_one(id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Projet WHERE Id = %s", (id,))
        projet = cursor.fetchone()

        cursor.close()
        conn.close()

        if projet:
            return Projet(projet['Id'], projet['Nom_Projet'], projet['Description'])
        return None
    
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Projet")
        projets = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Projet(projet['Id'], projet['Nom_Projet'], projet['Description']) for projet in projets]
    

    def post(nom_projet, description):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO Projet (Nom_Projet, Description) VALUES (%s, %s)"
        cursor.execute(query, (nom_projet, description))
        conn.commit()

        cursor.close()
        conn.close()

        return cursor.lastrowid
    
    def put(id, nom_projet, description):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE Projet SET Nom_Projet = %s, Description = %s WHERE Id = %s"
        cursor.execute(query, (nom_projet, description, id))
        conn.commit()

        cursor.close()
        conn.close()

    def delete(id):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM Projet WHERE Id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        conn.close()
    


    
