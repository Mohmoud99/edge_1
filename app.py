from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import uuid
import os

app = Flask(__name__)

# الصفحة الرئيسية
@app.route("/")
def home():
    return "The server is running"

# تحويل النص إلى صوت MP3
@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]

    output_file = f"{uuid.uuid4()}.mp3"

    async def generate():
        communicate = edge_tts.Communicate(text, "ar-SA-HamedNeural")
        await communicate.save(output_file)

    asyncio.run(generate())

    return send_file(output_file, mimetype="audio/mpeg", as_attachment=True)

# تشغيل السيرفر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)