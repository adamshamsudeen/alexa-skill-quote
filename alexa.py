from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import html
import re

app = Flask(__name__)
ask = Ask(app, "/")

def get_quote():
    r = requests.get("http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1")
    p = r.json()[0]['content'].strip()
    p = html.unescape(p)
    quote = re.sub('<[^<]+?>', '', p)
    guy = r.json()[0]['title'].strip()
    titles = 'This world is amazing'
    return quote, guy  

@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like to here a quote?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    quote, guy = get_quote()
    headline_msg = '{}... This was quoted by {}'.format(quote, guy)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)