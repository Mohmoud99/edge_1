from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import uuid
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "The server is running"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400

    output_file = f"{uuid.uuid4()}.mp3"

    try:
        async def generate():
            communicate = edge_tts.Communicate(text, "ar-SA-HamedNeural")
            await communicate.save(output_file)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate())
        loop.close()

        return send_file(output_file, mimetype="audio/mpeg", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # تنظيف الملف بعد الإرسال (مهم جدًا في السيرفرات)
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
