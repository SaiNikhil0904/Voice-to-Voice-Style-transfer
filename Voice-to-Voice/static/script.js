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

document.getElementById('transformButton').onclick = function() {
    const formData = new FormData(document.getElementById('voiceForm'));

    fetch('/transform', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('originalAudio').src = data.originalAudioUrl;
        document.getElementById('transformedAudio').src = data.transformedAudioUrl;
        document.getElementById('originalSpectralImage').src = data.originalSpectralImageUrl;
        document.getElementById('transformedSpectralImage').src = data.transformedSpectralImageUrl;

        document.getElementById('results').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
};