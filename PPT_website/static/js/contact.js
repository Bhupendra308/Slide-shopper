document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form'); // Use the form ID

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        console.log('Form submitted with data:', data); // Debugging

        try {
            const response = await fetch('/submit_contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            console.log('Fetch response:', response); // Debugging

            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }

            const result = await response.json();
            console.log('Result from server:', result); // Debugging

            if (result.success) {
                alert('Your message has been sent successfully.');
                form.reset();
            } else {
                alert('Failed to send message: ' + (result.message || 'Unknown error.'));
            }
        } catch (error) {
            console.error('Error during form submission:', error);
            alert('An error occurred while sending your message: ' + error.message);
        }
    });
});
