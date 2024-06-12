from flask import Flask, request, redirect, render_template
from hashlib import md5
import json
import os
import string
import random

app = Flask(__name__)

# Load URL mappings from file or create empty dictionary
url_mapping_file = 'urls.json'
if os.path.exists(url_mapping_file):
    with open(url_mapping_file, 'r') as file:
        url_mapping = json.load(file)
else:
    url_mapping = {}

# Function to generate a short code
def generate_short_code(length=5):
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(length))
    return short_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url_code = generate_short_code()

    # Ensure the short code is unique
    while short_url_code in url_mapping:
        short_url_code = generate_short_code()

    url_mapping[short_url_code] = original_url

    # Save the URL mappings to file
    with open(url_mapping_file, 'w') as file:
        json.dump(url_mapping, file)

    short_url = f"http://127.0.0.1:5000/{short_url_code}"
    return render_template('index.html', short_url=short_url)

@app.route('/<short_url_code>')
def redirect_to_url(short_url_code):
    original_url = url_mapping.get(short_url_code)
    if original_url:
        return redirect(original_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
