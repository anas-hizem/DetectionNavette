# Projet de Détection de Panneaux et Suivi de Personnes

Ce projet utilise les modèles YOLO (You Only Look Once) pour la détection d'objets et SORT (Simple Online and Realtime Tracking) pour le suivi des personnes en temps réel. Il est conçu pour analyser les vidéos et détecter des panneaux spécifiques et des personnes, tout en suivant leurs mouvements à travers les images.

## Table des Matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Structure du Projet](#structure-du-projet)
4. [Détails des Fichiers](#détails-des-fichiers)


## Installation
1. **Créer un environnement virtuel :**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
```
2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

3.  **Télécharger le modèle pré-entraîné :**

Vous devez obtenir le modèle pré-entraîné hamdi_bechir.pt pour YOLO. Placez-le dans le répertoire approprié (/home/anas/DetectionNavette/ dans le script).

## Utilisation

```bash
python PanelDetection.py
```

Par défaut, le script utilise une vidéo locale (test3.mp4). Vous pouvez modifier le chemin dans le script pour utiliser un flux vidéo en direct.

## Structure du Projet

- **PanelDetection.py** : Le script principal qui gère la capture vidéo, la détection d'objets, et l'affichage des résultats.
- **utils_prin.py** : Contient des fonctions utilitaires pour l'initialisation du modèle, le suivi, le traitement des résultats, et l'affichage des résultats.
- **sort.py** : Implémentation de SORT pour le suivi en temps réel des objets détectés.













  
