import mysql.connector

# POur se connecter
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="--------",
    database="talents"
)
mycursor = mydb.cursor()

# Table Etudiant
mycursor.execute("""
CREATE TABLE Etudiant (
    Id INT PRIMARY KEY,
    Num_Etudiant INT,
    Nom VARCHAR(50),
    Prenom VARCHAR(50)
)
""")

# Table Competence
mycursor.execute("""
CREATE TABLE Competence (
    Id INT PRIMARY KEY,
    Nom_Competence VARCHAR(50)
)
""")

# Table Groupe
mycursor.execute("""
CREATE TABLE Groupe (
    Id INT PRIMARY KEY,
    Nbr_Personnes INT
)
""")

# Table Projet
mycursor.execute("""
CREATE TABLE Projet (
    Id INT PRIMARY KEY,
    Nom_Projet VARCHAR(50),
    Description VARCHAR(255)
)
""")
# Possede (Etudiant <-> Competence)
mycursor.execute("""
CREATE TABLE Possede (
    Etudiant_Id INT,
    Competence_Id INT,
    PRIMARY KEY (Etudiant_Id, Competence_Id),
    FOREIGN KEY (Etudiant_Id) REFERENCES Etudiant(Id),
    FOREIGN KEY (Competence_Id) REFERENCES Competence(Id)
)
""")

# Appartient (Etudiant <-> Groupe)
mycursor.execute("""
CREATE TABLE Appartient (
    Etudiant_Id INT,
    Groupe_Id INT,
    PRIMARY KEY (Etudiant_Id, Groupe_Id),
    FOREIGN KEY (Etudiant_Id) REFERENCES Etudiant(Id),
    FOREIGN KEY (Groupe_Id) REFERENCES Groupe(Id)
)
""")

# Associe_a (Groupe <-> Projet)
mycursor.execute("""
CREATE TABLE Associe_a (
    Groupe_Id INT,
    Projet_Id INT,
    PRIMARY KEY (Groupe_Id, Projet_Id),
    FOREIGN KEY (Groupe_Id) REFERENCES Groupe(Id),
    FOREIGN KEY (Projet_Id) REFERENCES Projet(Id)
)
""")