from flask import Flask, render_template, jsonify, request
import requests
import json
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import io
import base64
import os
import datetime

# Téléchargement des stopwords (mots courants à exclure)
nltk.download('stopwords')

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour récupérer les tweets à partir de l'API Twitter
def get_tweets():
    # Clé d'authentification de l'API Twitter
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAJkflgEAAAAAU%2BU2a6g1QB3TqrtoXq4TSkQleP8%3D1km58lp4uNyOTu62TZUdJGAqcqf1xjyZk8TLyuYZgeQj2JNWEH"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2FilteredStreamPython"
    }

    # URL de l'API pour récupérer les tweets avec certains critères de recherche
    url = "https://api.twitter.com/2/tweets/search/recent?query=réforme%20des%20retraites%20-is:retweet&max_results=100&expansions=author_id,referenced_tweets.id&tweet.fields=created_at,text,public_metrics,entities,geo&user.fields=username"

    # Liste pour stocker tous les tweets récupérés
    all_tweets = []
    next_token = None

    # Boucle pour récupérer plusieurs pages de résultats (jusqu'à 500 tweets au maximum)
    while len(all_tweets) < 500:
        if next_token:
            request_url = f"{url}&pagination_token={next_token}"
        else:
            request_url = url

        # Envoi de la requête à l'API Twitter
        response = requests.get(request_url, headers=headers)

        # Vérification de la réponse
        if response.status_code != 200:
            raise Exception(f"Error getting tweets: {response.status_code}")

        # Conversion de la réponse en JSON
        data = response.json()

        # Extraction des textes des tweets et ajout à la liste de tous les tweets
        tweets = [tweet['text'] for tweet in data['data']]
        all_tweets.extend(tweets)

        # Récupération du jeton de pagination pour la prochaine page de résultats
        if 'meta' in data and 'next_token' in data['meta']:
            next_token = data['meta']['next_token']
        else:
            break

    # Analyse de sentiment pour tous les tweets récupérés
    sentiment_data = analyze_sentiments(all_tweets[:500])

    # Enregistrement des résultats dans un fichier JSON
    with open('tweets.json', 'w', encoding='utf-8') as f:
        json.dump(sentiment_data, f, ensure_ascii=False, indent=4)

    # Renvoi des résultats de l'analyse de sentiment
    return sentiment_data


# Fonction pour récupérer les statistiques d'analyse à partir du fichier 'tweets.json'
def get_analysis_stats():
    # Récupération de la date et de l'heure de la dernière analyse
    last_analysis_time = os.path.getmtime('tweets.json')
    last_analysis_date = datetime.datetime.fromtimestamp(last_analysis_time).strftime('%d/%m/%Y')
    last_analysis_time = datetime.datetime.fromtimestamp(last_analysis_time).strftime('%H:%M:%S')
    
    # Chargement des données d'analyse à partir du fichier 'tweets.json'
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)
        
    # Calcul du nombre total de tweets analysés
    total_tweets = len(sentiment_data)
    
    # Retourne le nombre total de tweets, la date et l'heure de la dernière analyse
    return total_tweets, last_analysis_date, last_analysis_time


def analyze_sentiments(tweets):
    sentiment_data = []
    for tweet in tweets:
        # Analyse de sentiment avec TextBlob
        analysis = TextBlob(tweet)
        # Classification en fonction de la polarité de l'analyse
        if analysis.sentiment.polarity > 0:
            sentiment = 'positif'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutre'
        else:
            sentiment = 'négatif'

        # Stockage du texte du tweet et de son sentiment associé dans un dictionnaire
        sentiment_data.append({'tweet': tweet, 'sentiment': sentiment})

    # Retourne la liste de tous les tweets avec leur sentiment associé
    return sentiment_data


def sentiment_pie_chart(sentiment_data):
    # Création d'un dataframe à partir des données de sentiment
    df = pd.DataFrame(sentiment_data)
    # Comptage du nombre de tweets pour chaque sentiment (positif, neutre, négatif)
    counts = df['sentiment'].value_counts()

    # Création d'un graphique en forme de camembert avec les pourcentages
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
    plt.title('Répartition des sentiments')

    # Conversion de l'image du graphique en format PNG
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encodage de l'image en base64 pour pouvoir l'afficher dans une page web
    return base64.b64encode(img.read()).decode()


def create_wordcloud(sentiment_data, sentiment):
    # Filtrer les données de sentiment en fonction du sentiment choisi
    filtered_data = [data for data in sentiment_data if data['sentiment'] == sentiment]
    # Concaténer tous les textes des tweets filtrés
    words = ' '.join([data['tweet'] for data in filtered_data])
    # Charger les stopwords en français depuis la bibliothèque NLTK
    stopwords_fr = set(stopwords.words('french'))
    # Générer le nuage de mots à partir des mots filtrés, en excluant les stopwords
    wordcloud = WordCloud(stopwords=stopwords_fr, background_color='white', width=800, height=800).generate(words)

    # Convertir le nuage de mots en image PNG et l'enregistrer dans un buffer
    img = io.BytesIO()
    wordcloud.to_image().save(img, 'PNG')
    img.seek(0)
    # Convertir l'image PNG en base64 pour pouvoir l'afficher dans une page web
    return base64.b64encode(img.read()).decode()


@app.route('/')
def home():
    # Ouverture du fichier tweets.json pour récupérer les données
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    # Création d'une liste de dictionnaires contenant les tweets et leur sentiment
    tweets = [{'tweet': data['tweet'], 'sentiment': data['sentiment']} for data in sentiment_data]

    # Appel à la fonction get_analysis_stats() pour récupérer le nombre total de tweets et la date/heure de la dernière analyse
    total_tweets, last_analysis_date, last_analysis_time = get_analysis_stats()

    # Renvoi de la page HTML home.html avec les données récupérées
    return render_template('home.html', tweets=tweets, total_tweets=total_tweets, last_analysis_date=last_analysis_date, last_analysis_time=last_analysis_time)


@app.route('/sentiments')
def sentiments():
    # Appel à la fonction get_tweets() pour récupérer les tweets et leur analyse de sentiment
    sentiment_data = get_tweets()

    # Création d'un graphique en camembert pour représenter la répartition des sentiments
    pie_chart = sentiment_pie_chart(sentiment_data)

    # Calcul du nombre de tweets pour chaque sentiment et stockage dans un dictionnaire
    sentiment_counts = {
        'positif': len([data for data in sentiment_data if data['sentiment'] == 'positif']),
        'neutre': len([data for data in sentiment_data if data['sentiment'] == 'neutre']),
        'negatif': len([data for data in sentiment_data if data['sentiment'] == 'négatif'])
    }

    # Renvoi de la page HTML sentiments.html avec le graphique et les statistiques de répartition des sentiments
    return render_template('sentiments.html', pie_chart=pie_chart, sentiment_counts=sentiment_counts)


@app.route('/tweets/<sentiment>')
def tweets(sentiment):
    # Ouverture du fichier tweets.json pour récupérer les données
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    # Création d'une liste contenant les tweets pour le sentiment sélectionné
    filtered_tweets = [data['tweet'] for data in sentiment_data if data['sentiment'] == sentiment]

    # Renvoi de la page HTML tweets.html avec les tweets pour le sentiment sélectionné
    return render_template('tweets.html', sentiment=sentiment, tweets=filtered_tweets)


@app.route('/wordcloud/<sentiment>')
def wordcloud(sentiment):
    # Ouverture du fichier tweets.json pour récupérer les données
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    # Création d'un nuage de mots pour le sentiment sélectionné
    wc = create_wordcloud(sentiment_data, sentiment)

    # Renvoi de la page HTML wordcloud.html avec le nuage de mots pour le sentiment sélectionné
    return render_template('wordcloud.html', sentiment=sentiment, wordcloud=wc)


if __name__ == '__main__':
    app.run(debug=True)
