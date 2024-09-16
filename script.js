// Function to add degree marks around the radar box
function addDegreeMarks() {
    const radar = document.getElementById('radar-box');
    const radius = 45; // Adjusted radius to bring degrees inward

    for (let i = 0; i < 360; i += 30) {
        // Create and position degree marks
        const mark = document.createElement('div');
        mark.className = 'degree-mark';
        mark.style.transform = `rotate(${i}deg)`;
        radar.appendChild(mark);

        // Create and position degree labels
        const label = document.createElement('div');
        label.className = 'degree-label';
        label.textContent = i + '°';
        const labelAngle = i * Math.PI / 180;
        label.style.left = `${50 + radius * Math.sin(labelAngle)}%`; // Moved inward
        label.style.top = `${50 - radius * Math.cos(labelAngle)}%`; // Moved inward
        radar.appendChild(label);
    }
}

// Function to add direction labels (N, E, S, W) to the radar box
function addDirectionLabels() {
    const radar = document.getElementById('radar-box');
    const directions = { 0: 'N', 90: 'E', 180: 'S', 270: 'W' };
    const radius = 35; // Radius for direction labels

    Object.keys(directions).forEach(degree => {
        // Create and position direction labels
        const label = document.createElement('div');
        label.className = 'degree-label';
        label.textContent = directions[degree];
        const angle = degree * Math.PI / 180;
        label.style.left = `${50 + radius * Math.sin(angle)}%`; // Positioned inward
        label.style.top = `${50 - radius * Math.cos(angle)}%`; // Positioned inward
        radar.appendChild(label);
    });
}

// Function to update the radar line based on the degree input
function updateRadar(degree) {
    const radarLine = document.querySelector('.radar-line');
    radarLine.style.transform = `rotate(${degree}deg)`;
}

// Function to append data (timestamp and direction) to the table
function appendToTable(timestamp, direction) {
    const tableBody = document.getElementById('data-table');
    const directionMap = { 0: 'N', 90: 'E', 180: 'S', 270: 'W' };
    const directionLabel = directionMap[direction] || `${direction}°`;
    const newRow = document.createElement('tr');
    newRow.innerHTML = `<td>${timestamp}</td><td>${directionLabel}</td>`;
    tableBody.appendChild(newRow);
}

// Function to fetch data from the backend and update the radar and table
async function fetchDataAndUpdateRadar() {
    try {
        const response = await fetch('/gunshot-direction');
        const data = await response.json();
        const { timestamp, direction } = data;

        updateRadar(direction);  // Update the radar line
        appendToTable(timestamp, direction);  // Update the table
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Initialize the page by adding degree marks, direction labels, and fetching data
window.onload = function () {
    addDegreeMarks();
    addDirectionLabels();
    fetchDataAndUpdateRadar();
};
