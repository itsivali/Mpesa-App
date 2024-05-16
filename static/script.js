document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('paymentForm');
    const phoneInput = document.getElementById('phone');
    const amountInput = document.getElementById('amount');
    const spinner = document.getElementById('spinner');

    form.addEventListener('submit', function(event) {
        // Prevent form submission until validation
        event.preventDefault();

        // Clear previous validation messages
        phoneInput.classList.remove('is-invalid');
        amountInput.classList.remove('is-invalid');

        let isValid = true;

        // Validate phone number (must be in the format of 254XXXXXXXXX)
        const phonePattern = /^254\d{9}$/;
        if (!phonePattern.test(phoneInput.value)) {
            phoneInput.classList.add('is-invalid');
            isValid = false;
        }

        // Validate amount (must be a positive number)
        const amount = parseFloat(amountInput.value);
        if (isNaN(amount) || amount <= 0) {
            amountInput.classList.add('is-invalid');
            isValid = false;
        }

        if (isValid) {
            // Show the spinner
            spinner.style.display = 'block';

            // Submit the form
            form.submit();
        }
    });
});
