from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    style = request.form['style']
    sub_option = request.form['subOption']
    audio_file = request.files['audio']

    input_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(input_path)

    output_filename = f'transformed_{audio_file.filename}'
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # If the output file already exists, create a unique filename
    if os.path.exists(output_path):
        base, ext = os.path.splitext(output_filename)
        output_filename = f"{base}_{int(time.time())}{ext}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Perform accent transfer
    transformed_audio = accent_transfer(input_path, sub_option)
    save_audio(transformed_audio, output_path)

    # Generate spectral images for both original and transformed audio
    original_spectral_image_path = generate_spectral_image(input_path, 'original')
    transformed_spectral_image_path = generate_spectral_image(output_path, 'transformed')

    return jsonify({
        'originalAudioUrl': f'/{UPLOAD_FOLDER}/{audio_file.filename}',
        'transformedAudioUrl': f'/{OUTPUT_FOLDER}/{output_filename}',
        'originalSpectralImageUrl': f'/{original_spectral_image_path}',
        'transformedSpectralImageUrl': f'/{transformed_spectral_image_path}'
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

def generate_spectral_image(audio_path, prefix):
    audio, sr = librosa.load(audio_path, sr=16000)
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel-spectrogram ({prefix})')
    plt.axis('off')

    image_filename = f'spectral_{prefix}_{os.path.basename(audio_path)}.png'
    image_path = os.path.join(OUTPUT_FOLDER, image_filename)
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    return os.path.join(OUTPUT_FOLDER, image_filename)

def accent_transfer(input_audio, target_accent="british"):
    # Placeholder for actual accent transfer logic
    print(f"Transferring accent to: {target_accent}")
    audio, sr = librosa.load(input_audio, sr=16000)
    return audio

def save_audio(audio, output_path, sr=16000):
    sf.write(output_path, audio, sr)

if __name__ == '__main__':
    app.run(debug=True)
