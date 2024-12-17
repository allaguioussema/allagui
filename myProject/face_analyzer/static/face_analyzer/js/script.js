// Dark mode functionality
const darkModeToggle = document.getElementById('darkModeToggle');
const html = document.documentElement;

// Check for saved dark mode preference
if (localStorage.getItem('darkMode') === 'enabled') {
    html.classList.add('dark');
    darkModeToggle.textContent = 'Dark Mode: On';
}

darkModeToggle.addEventListener('click', () => {
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('darkMode', 'disabled');
        darkModeToggle.textContent = 'Dark Mode: Off';
    } else {
        html.classList.add('dark');
        localStorage.setItem('darkMode', 'enabled');
        darkModeToggle.textContent = 'Dark Mode: On';
    }
});

// Detection toggles
let detectionStates = {
    emotion: true,
    gender: true,
    age: true
};

function toggleDetection(type) {
    const button = document.getElementById(`${type}Toggle`);
    detectionStates[type] = !detectionStates[type];
    button.classList.toggle('bg-primary-500');
    button.classList.toggle('bg-gray-300');
}

// Video handling
let stream = null;
const video = document.getElementById('videoElement');
const toggleBtn = document.getElementById('toggleVideo');

async function startVideo() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        toggleBtn.textContent = 'Stop Camera';
    } catch (err) {
        console.error('Error accessing camera:', err);
    }
}

function stopVideo() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        video.srcObject = null;
        toggleBtn.textContent = 'Start Camera';
    }
}

// Add click handlers to toggle buttons
['emotion', 'gender', 'age'].forEach(type => {
    document.getElementById(`${type}Toggle`).addEventListener('click', () => toggleDetection(type));
});

toggleBtn.addEventListener('click', () => {
    if (stream) {
        stopVideo();
    } else {
        startVideo();
    }
});

// Results display
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    let resultsHTML = '';

    if (data.faces && data.faces.length > 0) {
        data.faces.forEach((face, index) => {
            resultsHTML += `<div class="card mb-4">
                <h3 class="text-lg font-semibold mb-2 dark:text-white">Face ${index + 1}</h3>`;

            if (detectionStates.emotion && face.emotion) {
                resultsHTML += `
                    <div class="mb-2">
                        <p class="text-gray-700 dark:text-gray-300">Emotion: ${face.emotion}</p>
                    </div>`;
            }

            if (detectionStates.age && face.age) {
                resultsHTML += `
                    <div class="mb-2">
                        <p class="text-gray-700 dark:text-gray-300">Age: ${face.age}</p>
                    </div>`;
            }

            if (detectionStates.gender && face.gender) {
                resultsHTML += `
                    <div class="mb-2">
                        <p class="text-gray-700 dark:text-gray-300">Gender: ${face.gender}</p>
                    </div>`;
            }

            resultsHTML += '</div>';
        });
    } else {
        resultsHTML = '<p class="text-gray-600 dark:text-gray-400">No faces detected</p>';
    }

    resultsDiv.innerHTML = resultsHTML;
}

// Start video on page load
startVideo();
