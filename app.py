from flask import Flask, request, jsonify, send_file, url_for , render_template
from flask_mail import Mail, Message
import os
import uuid
import requests
from bs4 import BeautifulSoup
import pyttsx3

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

def scrape_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraph_texts = [p.get_text() for p in paragraphs]
        body_text = ' '.join(paragraph_texts)
        return body_text
    else:
        return None
    
def text_to_speech(text, output_file):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 0.9)  
    engine.save_to_file(text, output_file)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        recipient = request.form['recipient']
        message = request.form['message']
        
        # Compose the email
        msg = Message(
            subject="New Contact Form Submission",
            recipients=[os.environ.get('vasanthvnr31@gmail.com')],
            body=f"Name: {name}\nEmail: {email}\nRecipient: {recipient}\nMessage: {message}"
        )
        
        # Send the email
        try:
            mail.send(msg)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('contact.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    url = request.form['websiteLink']
    webpage_content = scrape_webpage(url)
    if webpage_content:
        # Create a unique filename
        audio_filename = f"{uuid.uuid4()}.wav"
        audio_filepath = os.path.join('static', 'audio', audio_filename)
        
        text_to_speech(webpage_content, audio_filepath)
        
        return jsonify({'success': True, 'audio_url': url_for('static', filename=f'audio/{audio_filename}', _external=True)})
    else:
        return jsonify({'success': False, 'error': 'Failed, Try again'})


if __name__ == '__main__':
    if not os.path.exists('static/audio'):
        os.makedirs('static/audio')
    app.run(debug=True)
