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

    # Création du dataframe Patients
    patients = data2[['Name',
                   'Gender', 
                   'Blood Type', 
                   'Medical Condition']]

    patients2 = patients.drop_duplicates()
    patients2['Unique_Key'] = patients2['Name'] + '_' + patients2['Gender'] + '_' + patients2['Blood Type'] + '_' + patients2['Medical Condition']
    

    #Génération de l' ID unique par patient
    patients2['ID patient'] = range(1, len(patients2) + 1)
    patients2.head()
    patients2.head()
    data2['Unique_Key'] = data2['Name'] + '_' + data2['Gender'] + '_' + data2['Blood Type'] + '_' + data2['Medical Condition']
    
    # Merge pour ajouter l'ID patient à data2
    data2 = data2.merge(patients2[['Unique_Key', 'ID patient']], 
                                        on='Unique_Key', 
                                        how='left')
    
    # Suppression de la colonne 'Unique_Key' après la fusion
    data2.drop(columns=['Unique_Key'], inplace=True)
    patients2.drop(columns=['Unique_Key'], inplace=True)
    
    #Génération de l'ID unique par admission
    data2['ID admission'] = range(1, len(data2) + 1)
    
    # Création du dataframe Admissions
    admissions=data2[['ID admission','ID patient', 'Age',
        'Date of Admission', 'Doctor', 'Hospital', 
        'Room Number', 'Admission Type', 'Discharge Date',
        'Medication', 'Test Results' ]]
    
    # Création du dataframe Facturation
    facturation=data2[['ID admission', 'Insurance Provider',
        'Billing Amount' ]]
    facturation.head()

    # Charger les variables d'environnement
    load_dotenv(find_dotenv())
    usr = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    pw = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    db = os.getenv("MONGO_INITDB_DATABASE")
    
    # Connection à MongoDB
    url = f"mongodb://{usr}:{pw}@mongo:27017"
    logging.info("Connexion à la base de données MongoDB")
    client = pymongo.MongoClient(url)
    coll1 = client[db]['coll_patients']
    coll2 = client[db]['coll_admissions']
    coll3 = client[db]['coll_facturation']

    # création des utilisateurs (administrateur, utilisateur actif, consultant)
    logging.info("Création de l'administrateur de la base : %s", os.getenv("MONGO_INITDB_DATABASE"))
    adminName= os.getenv("ADMIN_NAME")
    adminMDP= os.getenv("ADMIN_MDP")

    try:
        client[db].command(
            'createUser', adminName, 
            pwd=adminMDP,
        roles=[{
                    'role': "dbAdmin",
                    'db': os.getenv("MONGO_INITDB_DATABASE")
                }])
    except Exception as e:
        logging.error("Erreur en créant le user : %s", e)
        
    logging.info("Création de l'utilisateur actif (writer) de la base : %s", os.getenv("MONGO_INITDB_DATABASE"))
    userRWName= os.getenv("USER_RW_NAME")
    userRWMDP= os.getenv("USER_RW_MDP")

    try:
        client[db].command(
            'createUser', userRWName, 
            pwd=userRWMDP,
        roles=[{
                    'role': "readWrite",
                    'db': os.getenv("MONGO_INITDB_DATABASE")
                }])
    except Exception as e:
        logging.error("Erreur en créant le user : %s", e)

    logging.info("Création de l'utilisateur consultant (reader) de la base : %s", os.getenv("MONGO_INITDB_DATABASE"))
    userRName= os.getenv("USER_R_NAME")
    userRMDP= os.getenv("USER_R_MDP")

    try:
        client[db].command(
            'createUser', userRName, 
            pwd=userRMDP,
        roles=[{
                    'role': "read",
                    'db': os.getenv("MONGO_INITDB_DATABASE")
                }])
    except Exception as e:
        logging.error("Erreur en créant le user : %s", e)
    

    # Insertion des données Admissions et vérification
    logging.info("Création du dictionnaire admissions")
    records_adm = admissions.to_dict('records')
    logging.info("Vérification du delta entre le dataframe et le dictionnaire.")
    assert len(records_adm) == len(admissions), "Il y a un delta entre le dataframe et le dictionnaire!"
    logging.info("La vérification a réussi: le dataframe et le dictionnaire ont la même longueur.")

    # Insertion des données Patients et vérification
    logging.info("Création du dictionnaire patients")
    records_pat = patients2.to_dict('records')
    logging.info("Vérification du delta entre le dataframe et le dictionnaire.")
    assert len(records_pat) == len(patients2), "Il y a un delta entre le dataframe et le dictionnaire!"
    logging.info("La vérification a réussi: le dataframe et le dictionnaire ont la même longueur.")

    # Insertion des données Facturation et vérification
    logging.info("Création du dictionnaire facturation")
    records_fac = facturation.to_dict('records')
    logging.info("Vérification du delta entre le dataframe et le dictionnaire.")
    assert len(records_fac) == len(facturation), "Il y a un delta entre le dataframe et le dictionnaire!"
    logging.info("La vérification a réussi: le dataframe et le dictionnaire ont la même longueur.")

    
    logging.info("Vérification des collections")
    donnees_coll1 = coll1.count_documents({})
    logging.info(f"Nombre de documents dans la collection 'coll_patients' avant insertion : {donnees_coll1}")

    if donnees_coll1 > 0:
        coll1.drop()
        logging.info("Collection 'coll_patients' existante supprimée")

    donnees_coll2 = coll2.count_documents({})
    logging.info(f"Nombre de documents dans la collection 'coll_admissions' avant insertion : {donnees_coll2}")

    if donnees_coll2 > 0:
        coll2.drop()
        logging.info("Collection 'coll_admissions' existante supprimée")

    donnees_coll3 = coll3.count_documents({})
    logging.info(f"Nombre de documents dans la collection 'coll_facturation' avant insertion : {donnees_coll2}")

    if donnees_coll3 > 0:
        coll3.drop()
        logging.info("Collection 'coll_facturation' existante supprimée")


    logging.info("Insertion des données dans les collections")
    coll1.insert_many(records_pat)
    logging.info(f"{len(records_pat)} documents insérés dans la collection 'coll_patients'")

    logging.info("Vérification du delta entre le dictionnaire et la collection.")
    assert len(records_pat) == coll1.count_documents({}), "Il y a un delta entre le dictionnaire et la collection!"
    logging.info("La vérification a réussi: le dictionnaire et la collection ont la même longueur.")

    coll2.insert_many(records_adm)
    logging.info(f"{len(records_adm)} documents insérés dans la collection 'coll_admissions'")

    logging.info("Vérification du delta entre le dictionnaire et la collection.")
    assert len(records_adm) == coll2.count_documents({}), "Il y a un delta entre le dictionnaire et la collection!"
    logging.info("La vérification a réussi: le dictionnaire et la collection ont la même longueur.")

    coll3.insert_many(records_fac)
    logging.info(f"{len(records_fac)} documents insérés dans la collection 'coll_facturation'")

    logging.info("Vérification du delta entre le dictionnaire et la collection.")
    assert len(records_fac) == coll3.count_documents({}), "Il y a un delta entre le dictionnaire et la collection!"
    logging.info("La vérification a réussi: le dictionnaire et la collection ont la même longueur.")

except Exception as e:
    logging.error("Une erreur s'est produite : %s", e)

logging.info("Fin du script")
exit(0)
