from flask import Flask, request, Response, jsonify
import edge_tts
import asyncio
import tempfile
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return {"status": "ok"}, 200


def generate_audio(text):
    async def run():
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp_path = tmp_file.name
        tmp_file.close()

        communicate = edge_tts.Communicate(text, "ar-SA-HamedNeural")
        await communicate.save(tmp_path)

        return tmp_path

    return asyncio.run(run())


@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "status": "error",
            "message": "text is required"
        }), 400

    text = data["text"]

    try:
        file_path = generate_audio(text)

        def stream():
            with open(file_path, "rb") as f:
                yield from f
            os.remove(file_path)

        return Response(stream(), mimetype="audio/mpeg", status=200)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
app = app