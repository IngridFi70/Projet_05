# Projet de Migration de Données Médicales vers MongoDB

## Description

Ce projet a pour objectif de migrer des données médicales depuis un fichier CSV vers une base de données MongoDB. Le processus est automatisé à l'aide de scripts Python et utilise la conteneurisation via Docker pour garantir la portabilité et la scalabilité de l'application.

## Technologies Utilisées

- **Python** : Langage de programmation utilisé pour le script de migration.
- **Pandas** : Bibliothèque pour la manipulation et l'analyse des données.
- **Pymongo** : Bibliothèque pour interagir avec MongoDB.
- **MongoDB** : Base de données utilisée pour stocker les données médicales.
- **Docker** : Outil de conteneurisation pour déployer l'application.
- **dotenv** : Pour gérer les variables d'environnement.

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/IngridFi70/Projet_05.git
   cd Projet_05/migration
   
2. Assurez-vous d'avoir Python installé sur votre machine. Vous pouvez utiliser un environnement virtuel si nécessaire :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`

3. Installez les dépendances nécessaires :

    ```bash
    pip install -r requirements.txt

4. Créez un fichier .env pour stocker vos informations de connexion MongoDB :

    ```bash
    MONGO_INITDB_ROOT_USERNAME=your_username
    MONGO_INITDB_ROOT_PASSWORD=your_password

## Utilisation

1. Assurez-vous que Docker est installé et en cours d'exécution.

2. Lancez les services Docker nécessaires (MongoDB) :

    ```bash
    docker-compose up -d


3. Exécutez le script de migration :

    ```bash
    python main.py

## Structure du Projet

- **main.py** : Script principal pour la migration des données.
- **requirements.txt** : Liste des dépendances nécessaires pour le projet.
- **docker-compose.yml** : Fichier de configuration pour les services Docker.
- **.env** : Fichier pour stocker les variables d'environnement.

## Contribuer
Les contributions sont les bienvenues ! Si vous souhaitez contribuer, merci de créer une issue ou une demande de tirage.

## License
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.

## Contact
Pour toute question concernant le projet, n'hésitez pas à me contacter via GitHub.
