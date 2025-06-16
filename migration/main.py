import logging
import pandas as pd
import pymongo
import os
from dotenv import load_dotenv, find_dotenv

# Configurer le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Début du script")

try:
    # Chargement des données
    data0 = pd.read_csv('/app/data/healthcare_dataset.csv')
    logging.info("Données chargées avec succès")
    
    # Normalisation des noms et suppression des doublons
    data0['Name'] = data0['Name'].astype(str).str.lower()
    data1 = data0.drop_duplicates()
    logging.info(f"Nombre de doublons supprimés (avant): {len(data0)}, (après): {len(data1)}")

    # Suppression des doublons selon plusieurs critères
    criteria = ['Name', 'Gender', 'Blood Type', 'Date of Admission', 
                'Hospital', 'Billing Amount', 'Room Number', 'Discharge Date']
    data2 = data1.drop_duplicates(criteria)
    logging.info(f"Nombre de doublons après suppression selon les critères spécifiés : {len(data1)} -> {len(data2)}")

    # Charger les variables d'environnement
    load_dotenv(find_dotenv())
    usr = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    pwd = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    
    # Connection à MongoDB
    url = f"mongodb://{usr}:{pwd}@mongo:27017"
    logging.info("Connexion à la base de données MongoDB")
    client = pymongo.MongoClient(url)
    coll = client['healthcare_db']['patients']

    # Insertion des données et vérification
    logging.info("Création du dictionnaire")
    records = data2.to_dict('records')
    logging.info("Vérification du delta entre le dataframe et le dictionnaire.")
    assert len(records) == len(data2), "Il y a un delta entre le dataframe et le dictionnaire!"
    logging.info("La vérification a réussi: le dataframe et le dictionnaire ont la même longueur.")

    
    logging.info("Vérification de la collection")
    donnees_coll = coll.count_documents({})
    logging.info(f"Nombre de documents dans la collection 'patients' avant insertion : {donnees_coll}")

    if donnees_coll > 0:
        coll.drop()
        logging.info("Collection 'patients' existante supprimée")


    logging.info("Insertion des données dans la collection")
    coll.insert_many(records)
    logging.info(f"{len(records)} documents insérés dans la collection 'patients'")

    logging.info("Vérification du delta entre le dictionnaire et la collection.")
    assert len(records) == coll.count_documents({}), "Il y a un delta entre le dictionnaire et la collection!"
    logging.info("La vérification a réussi: le dictionnaire et la collection ont la même longueur.")

except Exception as e:
    logging.error("Une erreur s'est produite : %s", e)

logging.info("Fin du script")