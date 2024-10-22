document.addEventListener('DOMContentLoaded', function() {
    // Flash message fade out
    var flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 600);
        }, 3000);
    });

    // Form validation
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            var inputs = form.querySelectorAll('input[required], select[required]');
            var isValid = true;
            inputs.forEach(function(input) {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });
            if (!isValid) {
                event.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Interactive tables
    var tables = document.querySelectorAll('table');
    tables.forEach(function(table) {
        table.addEventListener('mouseover', function(e) {
            if (e.target.tagName === 'TD') {
                e.target.parentElement.classList.add('highlight');
            }
        });
        table.addEventListener('mouseout', function(e) {
            if (e.target.tagName === 'TD') {
                e.target.parentElement.classList.remove('highlight');
            }
        });
    });
});