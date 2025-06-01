from flask import Flask, render_template, request
import sqlite3
import requests

app = Flask(__name__)

# Fetch startup news using NewsAPI
def get_startup_news():
    try:
        api_key = 'b19d46e74c0e484ea07d868c5c1eedf9'  
        url = f'https://newsapi.org/v2/everything?q=startup&language=en&pageSize=3&apiKey={api_key}'
        response = requests.get(url)
        articles = response.json().get('articles', [])
        news = [{'title': a['title'], 'url': a['url']} for a in articles]
        return news
    except Exception:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Connect to SQLite database
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        # Create table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        
        # Insert subscriber data
        c.execute('INSERT INTO subscribers (name, email) VALUES (?, ?)', (name, email))
        
        conn.commit()
        conn.close()
        
        success = True

    news = get_startup_news()
    return render_template('index.html', news_data=news, success=success)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

