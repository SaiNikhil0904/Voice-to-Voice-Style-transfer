from flask import Flask, request, jsonify, render_template
import openai
import os
from werkzeug.utils import secure_filename
import tempfile
import shutil

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'your_openai_key'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform_voice():
    style = request.form['style']
    sub_option = request.form['subOption']
    audio_file = request.files['audio']

    # Save the uploaded audio file
    filename = secure_filename(audio_file.filename)
    audio_path = os.path.join(UPLOAD_FOLDER, filename)
    audio_file.save(audio_path)

    # Call OpenAI to transform the voice in real-time
    transformed_voice_url = openai_transform(style, sub_option, audio_path)

    # Return the transformed voice URL
    return jsonify({'transformedVoiceUrl': transformed_voice_url})

def openai_transform(style, sub_option, audio_path):
    """
    Transforms the voice by applying speech-to-text and text-to-speech conversion.
    This uses OpenAI's Whisper API (for STT) and GPT or another language model
    for transformation, followed by a TTS API.
    """

    # Step 1: Speech-to-text conversion using OpenAI's Whisper API
    with open(audio_path, 'rb') as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
        original_text = response['text']

    # Step 2: Transform the text based on selected style (accent/tone)
    transformed_text = apply_voice_style(style, sub_option, original_text)

    # Step 3: Text-to-speech synthesis using OpenAI's text-to-speech engine
    transformed_audio_path = synthesize_speech(transformed_text)

    return transformed_audio_path

def apply_voice_style(style, sub_option, original_text):
    """
    Apply transformations to the original text based on the selected voice style and sub-option.
    For accents, you can simulate this by using specific phrasing or words common to the region.
    For tone, modify the formality or emotional tone of the text.
    """
    if style == 'accent':
        prompt = f"Change the accent of this text to {sub_option}: {original_text}"
    elif style == 'tone':
        prompt = f"Change the tone of this text to be more {sub_option}: {original_text}"
    else:
        prompt = original_text

    # Use OpenAI's GPT model to apply the transformation
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    return response['choices'][0]['text']

def synthesize_speech(text):
    """
    Use text-to-speech to convert the transformed text into speech.
    """
    response = openai.TextToSpeech.create(
        model="text-to-speech-001",  # Placeholder model
        text=text,
        voice="your_desired_voice",  # Placeholder voice parameter
    )

    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(response['audio'])

    # Move the temporary audio file to the static folder for serving
    transformed_audio_path = os.path.join('static', os.path.basename(temp_audio_file.name))
    shutil.move(temp_audio_file.name, transformed_audio_path)

    return transformed_audio_path

if __name__ == '__main__':
    app.run(debug=True)