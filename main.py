from flask import Flask, request, jsonify
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Initialize the Gemini API
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set in the environment variables.")
llm = ChatGoogleGenerativeAI(model="gemini-pro")

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text_to_translate = data.get('text')

    if not text_to_translate:
        return jsonify({"error": "Text to translate is required"}), 400

    # Create a prompt for translation
    prompt = f"Translate the following English text to Kannada: {text_to_translate}"

    # Get the translation from the Gemini API
    try:
        result = llm.invoke(prompt)
        return jsonify({"translated_text": result.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
