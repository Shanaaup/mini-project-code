<!DOCTYPE html>
<html lang="en">
<head>
<!-- Define character encoding to UTF-8 for proper text rendering -->
<meta charset="UTF-8">

<!-- Title of the webpage that will appear in the browser tab -->
<title>Cancer Gene Prediction Tool</title>

<!-- Load the Chart.js library from a CDN for creating charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
/* General body styles */
body {
font-family: Arial, sans-serif; /* Font style for the page */
margin: 40px; /* Set margin around the body */
background-color: #f3f3f3; /* Light gray background */
text-align: center; /* Center text */
}

/* Container to hold the form and results */
.container {
max-width: 600px; /* Max width of the container */
margin: 20px auto; /* Center align the container with a margin */
background: #fff; /* White background */
padding: 20px; /* Padding inside the container */
border-radius: 10px; /* Rounded corners */
box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Shadow effect */
text-align: left; /* Align text to the left inside the container */
}

/* Style for form inputs and buttons */
input, button {
width: 100%; /* Make inputs and buttons fill the width of the container */
padding: 10px; /* Add padding inside inputs and buttons */
margin: 10px 0; /* Add margin between inputs/buttons */
font-size: 16px; /* Font size for inputs and buttons */
}

/* Style for button */
button {
background-color: #4CAF50; /* Green background color */
color: white; /* White text color */
border: none; /* Remove border */
cursor: pointer; /* Change cursor to pointer on hover */
}

/* Style for button hover effect */
button:hover {
background-color: #45a049; /* Darker green background on hover */
}

/* Style for the result section */
#result {
margin-top: 15px; /* Space above the result */
font-weight: bold; /* Bold font for result text */
}

/* Style for loading text */
#loading {
display: none; /* Hide loading text by default */
font-size: 14px; /* Set font size */
color: blue; /* Blue text color */
}

/* Style for charts section */
#charts {
margin-top: 30px; /* Space above the charts section */
}

/* Style for images */
img {
max-width: 100%; /* Ensure image is responsive */
height: auto; /* Keep image aspect ratio intact */
border-radius: 10px; /* Rounded corners for images */
}
</style>
</head>
<body>

<!-- Container for the entire form and results -->
<div class="container">
<!-- Header for the tool -->
<h2>Cancer Gene Prediction Tool</h2>

<!-- Form to take gene input and expression status -->
<form id="searchForm">
<!-- Input field for gene symbol -->
<input
type="text"
id="geneInput"
name="gene"
placeholder="Enter Gene Symbol (e.g., TP53)"
required
>

<!-- Input field for expression status -->
<input
type="text"
id="expressionStatus"
name="expression_status"
placeholder="Enter Expression Status (Up/Down/Unknown)"
>

<!-- Submit button to trigger search -->
<button type="submit">Search</button>
</form>

<!-- Loading text shown while processing -->
<p id="loading">Processing... Please wait.</p>

<!-- Area to display the result of the prediction -->
<div id="result"></div>

<!-- Visualization charts section -->
<div id="charts">
<h3>Feature Importance</h3>
<!-- Static image for feature importance -->
<img src="{{ url_for('static', filename='feature_importance.png') }}" alt="Feature Importance">

<h3>Top Predictions</h3>
<!-- Dynamic chart for displaying top predictions -->
<canvas id="predictionChart" width="400" height="200"></canvas>
</div>
</div>

<script>
// Event listener for the form submission
document.getElementById('searchForm').addEventListener('submit', function (event) {
event.preventDefault(); // Prevent default form submission (page reload)

// Get the gene input and expression status values from the form
const gene = document.getElementById('geneInput').value.trim();
const expressionStatus = document.getElementById('expressionStatus').value.trim() || 'Unknown';
const resultDiv = document.getElementById('result');
const loadingText = document.getElementById('loading');

// Clear previous result
resultDiv.innerHTML = '';

// If no gene is entered, show an error message
if (!gene) {
resultDiv.innerHTML = `<p style="color: red;">Please enter a gene symbol.</p>`;
return;
}

// Show the loading text while processing the request
loadingText.style.display = 'block';

// Make a POST request to the /predict endpoint with the gene and expression status
fetch('/predict', {
method: 'POST', // Use POST method
headers: { 'Content-Type': 'application/json' }, // Set content type to JSON
body: JSON.stringify({ gene_symbol: gene, expression_status: expressionStatus }) // Send gene data as JSON
})
.then(response => response.json()) // Parse the JSON response
.then(data => {
// Hide the loading text once data is received
loadingText.style.display = 'none';

// If there's an error in the response, display the error
if (data.error) {
resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
return;
}

// Extract the top predictions from the response
const topPredictions = data.top_predictions || {}; // Ensure top_predictions is an object
const predictionsList = Object.entries(topPredictions).map(
([type, prob]) => `<li>${type}: ${(prob * 100).toFixed(2)}%</li>`
).join('') || "<li>No predictions available</li>";

// Display the predicted cancer type, probability, and top predictions
resultDiv.innerHTML = `
<p>Predicted Cancer Type: <strong>${data.predicted_cancer_type}</strong></p>
<p>Probability: <strong>${(data.probability * 100).toFixed(2)}%</strong></p>
<p>Top Predictions:</p>
<ul>${predictionsList}</ul>
`;

// Update the prediction chart with the top predictions data
updatePredictionChart(data.top_predictions);
})
.catch(error => {
// Hide loading text and display an error message if the fetch request fails
loadingText.style.display = 'none';
resultDiv.innerHTML = `<p style="color: red;">Error connecting to the server.</p>`;
console.error('Error:', error);
});
});

// Function to update the prediction chart with data
function updatePredictionChart(predictions) {
const ctx = document.getElementById('predictionChart').getContext('2d'); // Get canvas context for chart
const labels = Object.keys(predictions); // Get the cancer types (labels)
const values = Object.values(predictions).map(v => v * 100); // Get the probabilities (convert to percentages)

// Create a new bar chart using Chart.js
new Chart(ctx, {
type: 'bar', // Define chart type as 'bar'
data: {
labels: labels, // Use cancer types as labels
datasets: [{
label: 'Prediction Probability (%)', // Label for the dataset
data: values, // Use probabilities as data
backgroundColor: 'blue' // Set color for the bars
}]
},
options: {
responsive: true, // Make chart responsive to screen size
scales: {
y: {
beginAtZero: true // Set y-axis to start from zero
}
}
}
});
}
</script>
</body>
</html>
