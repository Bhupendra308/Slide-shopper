// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {

    // Smooth scroll for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Bootstrap tooltip activation
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form Validation (Bootstrap)
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Alert for demo buttons (Optional)
    const demoBtns = document.querySelectorAll(".btn-demo");
    demoBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            alert("🚧 Demo feature – not yet implemented!");
        });
    });

    // Auto-dismiss Bootstrap alerts after 4s
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });
});

function togglePassword(inputId, iconId) {
    const password = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (password.type === "password") {
        password.type = "text";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    } else {
        password.type = "password";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    }
}
