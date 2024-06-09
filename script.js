var audioPlayer = document.getElementById("audioPlayer");

function synthesizeAudio() {
    var websiteLink = document.getElementById("websiteLink").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/synthesize", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    var audioBlob = new Blob([xhr.response], { type: 'audio/wav' });
                    var audioUrl = URL.createObjectURL(audioBlob);
                    var audioPlayer = document.getElementById('audioPlayer'); // Make sure you have an audio element with this ID
                    audioPlayer.src = audioUrl;
                    audioPlayer.load(); // Load the new audio file
                    alert("Audio generated successfully!");
    
                    // Add event listener to play the audio when the play button is clicked
                    var playButton = document.getElementById('playButton'); // Make sure you have a button with this ID
                    playButton.addEventListener('click', function() {
                        audioPlayer.play();
                    });
                } else {
                    alert("Failed to generate audio. Please check the URL and try again.");
                }
            } else {
                alert("Error occurred while processing the request.");
            }
        }
    };
    xhr.send("websiteLink=" + encodeURIComponent(websiteLink));
}
