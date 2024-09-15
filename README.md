# Voice to Voice Style Transfer

Transform your voice with different styles and accents in real-time. This project allows users to modify their voice recordings using various styles (e.g., accents, tones) with the help of OpenAI's API. It provides a simple and interactive web interface for capturing, processing, and playing back transformed audio.

## Overview
The Voice Style Transfer project uses the microphone to capture the user's voice in real-time, and then transforms the audio using OpenAI. Users can select from different voice styles such as accents (British, American, Australian) and tones (Calm, Excited, Formal) to modify their recorded voice. The transformed audio is then played back to the user.

## Key Features
- Real-time voice recording and transformation.
- Various voice style options including accents and tones.
- Simple and interactive web interface.
- Uses OpenAI's API for voice transformation.
- Provides audio instructions to guide users through the interface.

## Installation

### 1. Clone the Repository
First, clone the repository to your local machine using:
```bash
git clone https://github.com/yourusername/voice-style-transfer.git
cd voice-style-transfer
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to manage project dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install the necessary Python libraries by running:

```bash
pip install -r requirements.txt
```

### 4. Set Up OpenAI API Key
You need to provide your OpenAI API key in app.py. Replace YOUR_OPENAI_API_KEY with your actual key:

```openai.api_key = 'YOUR_OPENAI_API_KEY'```

## How to Use
### 1. Start the Flask Server: Run the server to launch the application:
```python app.py ```

### 2. Open the Application: In your web browser, go to ```http://127.0.0.1:5000```.

### 3. *Microphone Access:* Allow the application to access your microphone when prompted.

### 4. *Select Voice Style:* Choose a voice style (Accent or Tone) from the dropdown menu. An audio prompt will guide you through the process.

### 5. *Record Your Voice:* Click "Start Recording" to record your voice. Click "Stop Recording" once finished.

### 6. *Transformation:* The recorded audio will be processed, and the transformed audio will be played back in the output section.

## Important Files
- **`app.py`**: Main Flask application handling backend logic, including audio processing using OpenAI.
- **`templates/index.html`**: HTML file for the frontend user interface.
- **`static/styles.css`**: CSS file for styling the web interface.
- **`static/script.js`**: JavaScript file managing user interactions, recording, and server communication.
- **`requirements.txt`**: Lists all the Python dependencies required for the project.
- **`uploads/`**: Directory for storing uploaded audio files.
- **`static/transformed_voice.mp3`**: File where the transformed audio is saved and played.

## Future Improvements
- Integrate actual OpenAI API calls for more advanced voice transformation.
- Optimize real-time processing speed.
- Add more voice styles and transformation options.
- Implement better error handling and user feedback mechanisms.


