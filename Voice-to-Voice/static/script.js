let mediaRecorder;
let audioChunks = [];

document.addEventListener('DOMContentLoaded', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            voicePrompt("Welcome user. Please select a voice style from the dropdown below.");
        })
        .catch(error => {
            alert("Microphone access is required for this application.");
        });
});

window.onload = function() {
    // Request microphone permission when the page loads
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            // Prepare to record audio
            mediaRecorder = new MediaRecorder(stream);
            // Play the welcome message
            voicePrompt("Welcome user. Please select a voice style from the dropdown below.");
        })
        .catch(error => {
            alert("Microphone access is required for this application.");
        });
};

function updateSubOptions() {
    const style = document.getElementById('style').value;
    const subOptionsDiv = document.getElementById('subOptions');
    let subOptionsHTML = '';

    if (style === 'accent') {
        subOptionsHTML = `
            <label for="subOption">Choose Accent:</label>
            <select id="subOption" name="subOption">
                <option value="">-select-</option>
                <option value="british">British</option>
                <option value="american">American</option>
                <option value="australian">Australian</option>
            </select>
        `;
    } else if (style === 'tone') {
        subOptionsHTML = `
            <label for="subOption">Choose Tone:</label>
            <select id="subOption" name="subOption">
                <option value="">-select-</option>
                <option value="calm">Calm</option>
                <option value="excited">Excited</option>
                <option value="formal">Formal</option>
            </select>
        `;
    }

    subOptionsDiv.innerHTML = subOptionsHTML;
}

function startRecording() {
    if (mediaRecorder) {
        mediaRecorder.start();
        document.getElementById('recordingStatus').innerText = "Recording... Your voice is being captured.";
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
    } else {
        alert("Microphone access was not granted. Please refresh and allow access.");
    }
}

function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
        document.getElementById('recordingStatus').innerText = "Recording stopped. Processing your voice.";
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            submitVoice(audioBlob);
        };
    }
}

function submitVoice(audioBlob) {
    const style = document.getElementById('style').value;
    const subOption = document.getElementById('subOption').value;

    if (!style || !subOption) {
        alert("Please select both a style and a sub-option.");
        return;
    }

    const formData = new FormData();
    formData.append('style', style);
    formData.append('subOption', subOption);
    formData.append('audio', audioBlob);

    fetch('/transform', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('outputAudio').src = data.transformedVoiceUrl;
    });
}

function voicePrompt(message) {
    const speech = new SpeechSynthesisUtterance(message);
    speech.lang = 'en-US';
    window.speechSynthesis.speak(speech);
}
