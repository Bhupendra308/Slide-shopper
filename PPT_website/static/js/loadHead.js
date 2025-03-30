document.addEventListener("DOMContentLoaded", function() {
    fetch('/head')
        .then(response => response.text())
        .then(data => {
            document.head.innerHTML = data + document.head.innerHTML;
        });
});
