from flask import Flask, render_template, request, jsonify
import requests
import datetime
import tensorflow as tf

from clean_text import clean_texts

model = tf.keras.models.load_model('models/cyberbullying-bdlstm.h5')

with open("models/tokenizer.json") as file:
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(file.read())

app = Flask(__name__)

convos = []

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/cyberbully")
def cyberbully():
    messages = clean_texts([request.args.get("msg")], tokenizer)
    return jsonify(dict(score = model.predict(messages).T[0].tolist()[0]))
    
time = lambda: datetime.datetime.now().strftime("%H:%M")

@app.route("/getUserHtml")
def getUser():
    userText = request.args.get('msg')
    return {"user": f"<div class='container darker'><p class='user-msg'>{userText}</p><span class='time-right'>{time()}</span></div>"}

@app.route("/get")
def get():
    userText = request.args.get('msg')
    botText = requests.post("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill", headers={"Authorization": "Bearer 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"}, json={"inputs": {"past_user_inputs": [i[0] for i in convos], "generated_responses": [i[1] for i in convos], "text": userText}, "parameters": {"repetition_penalty": 1.33}}).json()["generated_text"]
    convos.append((userText, botText))
    return {"bot": botText.strip()}
    # return {"user": f"<div class='container darker'><span class='user-msg'>{userText}</span><br><span class='time-right'>{time()}</span></div>", "bot": f"<div class='container'><span>{botText}</span><br><span class='time-left'>{time()}</span></div>"}


# Github webhooking
import git, os

@app.route('/update_server', methods=['POST'])
def webhook():
    repo = git.Repo(os.curdir)
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200
        
if __name__ == "__main__": 
    app.run()
