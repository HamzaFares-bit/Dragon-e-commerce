🛍 E-commerce Video Shopping Platform

Une plateforme e-commerce moderne qui permet aux utilisateurs de découvrir et acheter des produits via des vidéos Instagram intégrées.

 ✨ Fonctionnalités

 🎥 Système de Vidéos
- Intégration de vidéos Instagram
- Navigation entre vidéos par magasin
- Interface utilisateur moderne et responsive

  🛒 Système de Panier
- Ajout/suppression de produits
- Gestion des stocks en temps réel
- Notifications interactives
- Calcul automatique des totaux

  💳 Système de Paiement
- Interface de paiement sécurisée
- Validation en temps réel des cartes
- Simulation de traitement de paiement
- Génération de factures

 👤 Gestion des Utilisateurs
- Inscription et connexion
- Base de données MySQL
- Hachage sécurisé des mots de passe

 📱 Interface Moderne
- Design responsive
- Animations fluides
- Notifications en temps réel
- Interface utilisateur intuitive

 🚀 Installation

  Prérequis
- Python 3.8+
- MySQL 8.0+
- pip

  Étapes d’installation

1.	Cloner le projet
Git clone <url-du-repo>
CProjectStageHamzaFares

2.	Installer les dépendances

Pip install -r requirements.txt

3.	Configurer la base de données
CREATE DATABASE gestion_utilisateur ;
USE gestion_utilisateur ;

CREATE TABLE utilisateurs (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Mot_de_passe VARCHAR(255) NOT NULL,
    Date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ;

4.	Configurer l’application
 le fichier config.py selon mes paramètres :
DATABASE_CONFIG = {
    ‘host’ : ‘localhost’,
    ‘user’ : ‘votre_utilisateur’,
    ‘password’ : ‘mon_mot_de_passe’,
    ‘database’ : ‘gestion_utilisateur’
}

5.	Lancer l’application
bash
Python app.py


  📁 Structure du Projet

ProjectStageHamzaFares/
├── app.py                 # Application Flask principale
├── config.py              # Configuration de l’application
├── requirements.txt       # Dépendances Python
├── static/               # Fichiers statiques
│   └── images/          # Images et vidéos
├── templates/            # Templates HTML
│   ├── index.html       # Page d’accueil
│   ├── index1.html      # Page après connexion
│   ├── video.html       # Page de lecture vidéo
│   ├── paiement.html    # Page de paiement
│   └── facture.html     # Page de facture
└── Info_Utile/          # Informations utiles

 🎯 Utilisation

  1. Inscription/Connexion
- Accédez à la page d’accueil
- Créez un compte ou connectez-vous

  2. Navigation dans les Vidéos
- Parcourez les vidéos disponibles
- Cliquez sur une vidéo pour la regarder
- Découvrez les produits associés

 3. Ajout au Panier
- Sélectionnez un produit
- Choisissez marque, couleur et taille
- Vérifiez la disponibilité en stock
- Ajoutez au panier

 4. Paiement
- Remplissez les informations de paiement
- Validez la commande
- Recevez votre facture

  🔧 Configuration

  Variables d’environnement
bash
Export SECRET_KEY= »votre_clé_secrète »
Export DB_HOST= »localhost »
Export DB_USER= »root »
Export DB_PASSWORD= »mon_mot_de_passe »
Export DB_NAME= »gestion_utilisateur »

  Configuration des paiements 
 config.py pour personnaliser :
- Taux de TVA
- Frais de livraison
- Seuil de livraison gratuite
- Cartes supportées

 🛡 Sécurité

- Mots de passe hachés avec SHA-256
- Validation côté client et serveur
- Protection contre les injections SQL
- Sessions sécurisées
- Validation des données de paiement

📱 Responsive Design

L’application est entièrement responsive et s’adapte à :
- Ordinateurs de bureau
- Tablettes
- Smartphones

 🔄 API Endpoints

 Authentification
- POST /inscription - Inscription utilisateur
- POST /connexion - Connexion utilisateur

 E-commerce
- GET /video.html - Page de vidéo avec produits
- GET /paiement - Page de paiement
- POST /api/process-payment - Traitement du paiement
- GET /facture - Génération de facture

 Problèmes courants

1. Erreur de connexion MySQL
   - Vérifiez les paramètres dans config.py
   - Assurez-vous que MySQL est démarré

2. Module non trouvé
   - Installez les dépendances : pip install -r requirements.txt

3. Erreur de port
   - Changez le port dans app.py ou arrêtez le processus qui utilise le port 5000

 👨‍💻 Auteur

Hamza Fares - Développeur Full Stack
