<div id="top"></div>

<div align="center">
  <h1> Application d'analyse des tweets sur la réforme des retraites en France </h1>
  <p>LPWB - IUT de Lannion - 2022-2023</p>
</div>

***

### Table of Content
1. [Présentation](#presentation)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Fonctionnement du code](#fonctionnement)
5. [Structure du projet](#structure)
6. [Contribution](#contribution)
7. [Contact](#contact)
<p align="right">(<a href="#top">Retour en haut</a>)</p>

***

### Présentation
Cette application web est développée en Python et utilise l'API Twitter pour collecter et analyser des tweets sur la réforme des retraites en France. Elle fournit des statistiques sur le nombre total de tweets analysés et la date et l'heure de la dernière analyse, ainsi qu'une liste de tweets triés par sentiment (positif, neutre, négatif).
<p align="right">(<a href="#top">Retour en haut</a>)</p>

***

### Technologies
Les technologies utilisées pour ce projet sont :

- Python 3.9 pour le code backend
- Flask 2.0.1 pour le framework web
- TextBlob 0.15.3 pour l'analyse de sentiments
- pandas 1.3.1 pour la manipulation de données
- matplotlib 3.4.2 pour la création de graphiques
- WordCloud 1.8.1 pour la création de nuages de mots
<p align="right">(<a href="#top">Retour en haut</a>)</p>

***

### Installation
Pour utiliser l'application, il est nécessaire d'installer les bibliothèques Python utilisées. Pour cela, il est conseillé d'utiliser un environnement virtuel :

```
python3 -m venv venv
source venv/bin/activate
```

Ensuite, il est nécessaire d'installer les bibliothèques à l'aide de la commande suivante :
```pip install -r requirements.txt```

Il est également nécessaire de créer une application sur le site de développeurs Twitter et d'obtenir les clés et les jetons d'accès pour utiliser l'API Twitter.

Une fois les bibliothèques installées et les clés d'API Twitter obtenues, il est possible de lancer l'application en utilisant la commande suivante :
```python app.py```

L'application est accessible à l'adresse http://localhost:5000.
<p align="right">(<a href="#top">Retour en haut</a>)</p> <br>

***

### Fonctionnement du code
Le code de l'application est divisé en plusieurs fonctions qui sont appelées dans les routes Flask pour afficher les résultats sur les pages web.

La fonction get_tweets récupère les tweets sur Twitter pour le mot-clé donné à l'aide de l'API Twitter et effectue une analyse de sentiment pour chaque tweet à l'aide de TextBlob.

La fonction get_analysis_stats permet de récupérer le nombre total de tweets analysés ainsi que la date et l'heure de la dernière analyse à partir du fichier JSON où sont stockés les résultats.

La fonction sentiment_pie_chart crée un graph
<p align="right">(<a href="#top">Retour en haut</a>)</p> <br>
***

### Structure du projet
Le projet est structuré de la manière suivante :

**app.py** : le fichier principal contenant le code de l'application web.
**templates/** : le dossier contenant les fichiers HTML utilisés par l'application.
**static/** : le dossier contenant les fichiers statiques (CSS, JavaScript, etc.) utilisés par l'application.

<p align="right">(<a href="#top">Retour en haut</a>)</p> <br>
***
### Contribution
If you have a suggestion that would make this better, please fork the repository and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<p align="right">(<a href="#top">Retour en haut</a>)</p>

***

### Contact 
Rochat Lise - liserochat@live.fr </br>
Project: [https://github.com/LiseRochat/twitter_app](https://github.com/LiseRochat/twitter_app)
<p align="right">(<a href="#top">Retour en haut</a>)</p>
