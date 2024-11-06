from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
CORS(app)

# Define the API key
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')
    
    if not text or not target_language:
        return jsonify({'error': 'Invalid input'}), 400

    prompt = f"Translate the following text to {target_language}: {text}"
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        translated_text = response.text
        return jsonify({'translated_text': translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)