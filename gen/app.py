from flask import Flask, request, jsonify
import subprocess
import traceback
from chatbot import chat_with_user

PREVIOUS_SONG_PATH = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the music generation API'}), 200


@app.route('/generate-music', methods=['POST'])
def generate_music():
    try:
        data = request.get_json()
        if not data or 'mood' not in data:
            return jsonify({'error': 'Mood is required'}), 400

        mood = data.get('mood', 'happy')
        topic = data.get('topic', 'sunshine')  # Default topic is sunshine

        command = f'python main.py "{mood}" "{topic}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({'message': 'Music generation started successfully!', 'mood': mood, 'topic': topic}), 200
        else:
            return jsonify({'error': f'Subprocess failed: {result.stderr}'}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        conversation_state = data.get("conversation_state", {})

        if not isinstance(conversation_state, dict):
            conversation_state = {}

        responses, updated_state = chat_with_user(
            user_message=user_message,
            conversation_state=conversation_state,
            previous_song_path=PREVIOUS_SONG_PATH
        )

        final_topic = updated_state.get("final_topic", "sunshine")  # Default to sunshine
        final_mood = updated_state.get("final_mood", "")

        return jsonify({
            "responses": responses,
            "conversation_state": updated_state,
            "final_topic": final_topic,
            "final_mood": final_mood
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
