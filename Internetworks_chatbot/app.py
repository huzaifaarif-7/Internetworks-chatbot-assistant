from flask import Flask, request, jsonify, render_template, Response
import json
import os
from dotenv import load_dotenv

from internetworks import chat_with_bot, stream_chat_with_bot


load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    calendly_url = os.getenv("CALENDLY_URL", "https://calendly.com/muizznaveed-internetworks/30min")
    return render_template("index.html", calendly_url=calendly_url)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_response = chat_with_bot(user_message)
    return jsonify({"response": bot_response})

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    user_message = request.json.get("message")

    def generate():
        for chunk in stream_chat_with_bot(user_message):
            yield f"data: {json.dumps(chunk)}\n\n"

    return Response(generate(), mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache',
                           'Connection': 'keep-alive',
                           'Access-Control-Allow-Origin': '*'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



