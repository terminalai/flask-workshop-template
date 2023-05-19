from flask import Flask, render_template, request, jsonify
import requests
import datetime

import tensorflow as tf

from clean_text import clean_texts

model = tf.keras.models.load_model('models/cyberbullying-bdlstm.h5')

with open("models/tokenizer.json") as file:
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(
        file.read()
    )

stopwords = [i.lower() for i in nltk.corpus.stopwords.words('english') + [chr(i) for i in range(97, 123)]]

app = Flask(__name__)

convos = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cyberbully")
def cyberbully():
    messages = clean_texts(request.args.get("msgs"))
    return jsonify(dict(scores=model.predict(messages).T[0]))
    
time = lambda: datetime.datetime.now().strftime("%H:%M")

@app.route("/get")
def get():
    userText = request.args.get('msg')
    botText = requests.post("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill", headers={"Authorization": "Bearer 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"}, json={"inputs": {"past_user_inputs": [i[0] for i in convos], "generated_responses": [i[1] for i in convos], "text": userText}, "parameters": {"repetition_penalty": 1.33}}).json()["generated_text"]
    convos.append((userText, botText))
    return {"user": f"<div class='container darker'><p>{userText}</p><span class='time-right'>{time()}</span></div>", "bot": f"<div class='container'><p>{botText}</p><span class='time-left'>{time()}</span></div>"}


if __name__ == "__main__": app.run()
