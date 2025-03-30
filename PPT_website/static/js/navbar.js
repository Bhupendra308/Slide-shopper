// navbar.js
document.addEventListener("DOMContentLoaded", function() {
    fetch('/navbar') // Adjust this URL to match your Flask route for serving navbar.html
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        })
        .catch(error => console.error('Error loading navbar:', error));
});
