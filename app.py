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


nltk.download('stopwords')

app = Flask(__name__)

def get_tweets():
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAJkflgEAAAAAU%2BU2a6g1QB3TqrtoXq4TSkQleP8%3D1km58lp4uNyOTu62TZUdJGAqcqf1xjyZk8TLyuYZgeQj2JNWEH"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2FilteredStreamPython"
    }

    url = "https://api.twitter.com/2/tweets/search/recent?query=réforme%20des%20retraites%20-is:retweet&max_results=100&expansions=author_id,referenced_tweets.id&tweet.fields=created_at,text,public_metrics,entities,geo&user.fields=username"

    all_tweets = []
    next_token = None

    while len(all_tweets) < 500:
        if next_token:
            request_url = f"{url}&pagination_token={next_token}"
        else:
            request_url = url

        response = requests.get(request_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error getting tweets: {response.status_code}")

        data = response.json()
        tweets = [tweet['text'] for tweet in data['data']]
        all_tweets.extend(tweets)

        if 'meta' in data and 'next_token' in data['meta']:
            next_token = data['meta']['next_token']
        else:
            break

    sentiment_data = analyze_sentiments(all_tweets[:500])

    with open('tweets.json', 'w', encoding='utf-8') as f:
        json.dump(sentiment_data, f, ensure_ascii=False, indent=4)

    return sentiment_data


def get_analysis_stats():
    last_analysis_time = os.path.getmtime('tweets.json')
    last_analysis_date = datetime.datetime.fromtimestamp(last_analysis_time).strftime('%d/%m/%Y')
    last_analysis_time = datetime.datetime.fromtimestamp(last_analysis_time).strftime('%H:%M:%S')
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)
    total_tweets = len(sentiment_data)
    return total_tweets, last_analysis_date, last_analysis_time

def analyze_sentiments(tweets):
    sentiment_data = []
    for tweet in tweets:
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            sentiment = 'positif'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutre'
        else:
            sentiment = 'négatif'

        sentiment_data.append({'tweet': tweet, 'sentiment': sentiment})

    return sentiment_data

def sentiment_pie_chart(sentiment_data):
    df = pd.DataFrame(sentiment_data)
    counts = df['sentiment'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
    plt.title('Répartition des sentiments')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

def create_wordcloud(sentiment_data, sentiment):
    filtered_data = [data for data in sentiment_data if data['sentiment'] == sentiment]
    words = ' '.join([data['tweet'] for data in filtered_data])
    stopwords_fr = set(stopwords.words('french'))
    wordcloud = WordCloud(stopwords=stopwords_fr, background_color='white', width=800, height=800).generate(words)

    img = io.BytesIO()
    wordcloud.to_image().save(img, 'PNG')
    img.seek(0)
    return base64.b64encode(img.read()).decode()

@app.route('/')
def home():
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    tweets = [{'tweet': data['tweet'], 'sentiment': data['sentiment']} for data in sentiment_data]

    total_tweets, last_analysis_date, last_analysis_time = get_analysis_stats()

    return render_template('home.html', tweets=tweets, total_tweets=total_tweets, last_analysis_date=last_analysis_date, last_analysis_time=last_analysis_time)



@app.route('/sentiments')
def sentiments():
    sentiment_data = get_tweets()
    pie_chart = sentiment_pie_chart(sentiment_data)
    
    sentiment_counts = {
        'positif': len([data for data in sentiment_data if data['sentiment'] == 'positif']),
        'neutre': len([data for data in sentiment_data if data['sentiment'] == 'neutre']),
        'negatif': len([data for data in sentiment_data if data['sentiment'] == 'négatif'])
    }

    return render_template('sentiments.html', pie_chart=pie_chart, sentiment_counts=sentiment_counts)

@app.route('/tweets/<sentiment>')
def tweets(sentiment):
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    filtered_tweets = [data['tweet'] for data in sentiment_data if data['sentiment'] == sentiment]
    return render_template('tweets.html', sentiment=sentiment, tweets=filtered_tweets)

@app.route('/wordcloud/<sentiment>')
def wordcloud(sentiment):
    with open('tweets.json', 'r', encoding='utf-8') as f:
        sentiment_data = json.load(f)

    wc = create_wordcloud(sentiment_data, sentiment)
    return render_template('wordcloud.html', sentiment=sentiment, wordcloud=wc)


if __name__ == '__main__':
    app.run(debug=True)
