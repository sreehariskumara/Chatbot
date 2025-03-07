from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)


openai.api_key = "AIzaSyBHo05xkFbJdmO79HbdG_vOUS2YGOL-gPY"


def load_college_data():
    with open("data/college_data.txt", "r") as file:
        return file.read()

# Endpoint to fetch chatbot response
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    college_data = load_college_data()

    # Send request to Gemini API (replace 'gpt-3.5-turbo' with the appropriate model)
    response = openai.Completion.create(
        model="text-davinci-003",  # Replace with the correct Gemini model
        prompt=f"Use the following college details to answer the question: {college_data}\n\nUser question: {user_message}",
        max_tokens=150
    )
    
    answer = response.choices[0].text.strip()
    return jsonify({'response': answer})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
