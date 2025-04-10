from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the Gemini API key
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

def load_college_data():
    """Load college data from a text file."""
    try:
        with open("data/college_data.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No college data available."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    college_data = load_college_data()

    # Use Gemini-1.5-Pro-Latest model
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = (
        "You are an AI assistant with deep knowledge in various fields. "
        "Use both your own knowledge and the following college details to answer the question:\n\n"
        f"College Data:\n{college_data}\n\n"
        f"User Question: {user_message}"
        "Respond in a simple, friendly, and helpful tone. If listing items, use plain text dashes (-) or numbered format, and avoid using asterisks or bold text. Only refer to college data if the question is related; otherwise, answer normally like a human."
    )

    try:
        response = model.generate_content([prompt])  # Correct API call
        answer = response.text.strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    return jsonify({'response': answer})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
