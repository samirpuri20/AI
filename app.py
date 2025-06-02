from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>LLaMA3 Chatbot</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; }
        #chatbox { border: 1px solid #ccc; padding: 10px; min-height: 300px; margin-bottom: 10px; overflow-y: auto; }
        .user { font-weight: bold; color: blue; }
        .bot { font-weight: bold; color: green; }
    </style>
</head>
<body>
    <h1>Chat with LLaMA 3</h1>
    <div id="chatbox"></div>
    <input id="message" autocomplete="off" placeholder="Type a message..." style="width: 80%;">
    <button onclick="sendMessage()">Send</button>

<script>
    async function sendMessage() {
        const msgInput = document.getElementById('message');
        const msg = msgInput.value;
        if (!msg.trim()) return;

        const chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += `<div class="user">You: ${msg}</div>`;
        msgInput.value = '';
        chatbox.scrollTop = chatbox.scrollHeight;

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });

        const data = await response.json();
        chatbox.innerHTML += `<div class="bot">Bot: ${data.response}</div>`;
        chatbox.scrollTop = chatbox.scrollHeight;
    }
</script>
</body>
</html>
"""

OLLAMA_API_URL = "http://localhost:11434/api/chat"

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').lower()

    # Custom info about Samir Puri
    if "samir puri" in user_message or "samir" in user_message:
        reply = ("Samir Puri is the developer of this AI agent. "
                 "He is originally from Nepal, specifically Chitwan Bharatpur, "
                 "and is currently living in Sydney.")
        return jsonify({"response": reply})

    # Otherwise, send to Ollama
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_API_URL, json=payload)
        r.raise_for_status()
        response_json = r.json()
        reply = response_json.get('message', {}).get('content', "Sorry, no response")
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)