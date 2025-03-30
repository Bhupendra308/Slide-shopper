// Define product data with themes and descriptions
const products = {
    ppt1: {
        title: 'PPT Title 1',
        description: 'This is a brief description of PPT 1. Detailed information will be provided upon purchase.',
        theme: 'Business Presentation'
    },
    ppt2: {
        title: 'PPT Title 2',
        description: 'This is a brief description of PPT 2. Detailed information will be provided upon purchase.',
        theme: 'Educational Topic'
    },
    ppt3: {
        title: 'PPT Title 3',
        description: 'This is a brief description of PPT 3. Detailed information will be provided upon purchase.',
        theme: 'Marketing Strategy'
    },
    ppt4: {
        title: 'PPT Title 4',
        description: 'This is a brief description of PPT 4. Detailed information will be provided upon purchase.',
        theme: 'Project Management'
    },
    ppt5: {
        title: 'PPT Title 5',
        description: 'This is a brief description of PPT 5. Detailed information will be provided upon purchase.',
        theme: 'Financial Analysis'
    },
    ppt6: {
        title: 'PPT Title 6',
        description: 'This is a brief description of PPT 6. Detailed information will be provided upon purchase.',
        theme: 'Human Resources'
    },
    ppt7: {
        title: 'PPT Title 7',
        description: 'This is a brief description of PPT 7. Detailed information will be provided upon purchase.',
        theme: 'Product Design'
    },
    ppt8: {
        title: 'PPT Title 8',
        description: 'This is a brief description of PPT 8. Detailed information will be provided upon purchase.',
        theme: 'Market Research'
    },
    ppt9: {
        title: 'PPT Title 9',
        description: 'This is a brief description of PPT 9. Detailed information will be provided upon purchase.',
        theme: 'Sales Strategy'
    },
    ppt10: {
        title: 'PPT Title 10',
        description: 'This is a brief description of PPT 10. Detailed information will be provided upon purchase.',
        theme: 'Customer Service'
    },
    ppt11: {
        title: 'PPT Title 11',
        description: 'This is a brief description of PPT 11. Detailed information will be provided upon purchase.',
        theme: 'Leadership Training'
    },
    ppt12: {
        title: 'PPT Title 12',
        description: 'This is a brief description of PPT 12. Detailed information will be provided upon purchase.',
        theme: 'Innovation Management'
    }
};

// Function to show product details in a modal
function showProductDetails(productId) {
    const modal = document.getElementById('product-details');
    const product = products[productId];
    
    if (product) {
        document.getElementById('product-title').innerText = product.title;
        document.getElementById('product-description').innerText = product.description;
        document.getElementById('product-theme').innerText = 'Theme: ' + product.theme;
        document.getElementById('ppt-id').value = productId; // Set hidden input value
        modal.style.display = 'block';
    } else {
        console.error('Product not found:', productId);
    }
}

// Function to close the product details modal
function closeProductDetails() {
    document.getElementById('product-details').style.display = 'none';
}

// Function to show the purchase form modal
function showPurchaseForm() {
    closeProductDetails();
    document.getElementById('purchase-form').style.display = 'block';
}

// Function to close the purchase form modal
function closePurchaseForm() {
    document.getElementById('purchase-form').style.display = 'none';
}

// Handle form submission
document.getElementById('purchase-form-details').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const pptId = document.getElementById('ppt-id').value;

    fetch('/book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            pptId: pptId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Booking confirmed!');
            closePurchaseForm();
        } else {
            alert('Booking failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
