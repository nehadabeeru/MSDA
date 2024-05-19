from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model_path = './model'
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token

@app.route('/')
def home():
    return render_template('chat.html')  # Ensure there's a basic route to load the form

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Handling JSON data from AJAX
        data = request.get_json()
        message = data['msg']
        inputs = tokenizer.encode(message, return_tensors='pt')
        outputs = model.generate(inputs, max_length=512)
        predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({'response': predicted_text})  # Respond with JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
