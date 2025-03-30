document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const loginToggle = document.getElementById('loginToggle');
    const signupToggle = document.getElementById('signupToggle');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const switchToLogin = document.getElementById('switchToLogin');

    // Toggle between forms
    loginToggle.addEventListener('click', function() {
        this.classList.add('active');
        signupToggle.classList.remove('active');
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
    });

    signupToggle.addEventListener('click', function() {
        this.classList.add('active');
        loginToggle.classList.remove('active');
        signupForm.classList.add('active');
        loginForm.classList.remove('active');
    });

    switchToLogin.addEventListener('click', function(e) {
        e.preventDefault();
        loginToggle.click();
    });

    // Toggle password visibility
    window.togglePassword = function(inputId) {
        const input = document.getElementById(inputId);
        const icon = input.nextElementSibling.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    };

    // Form validation and submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        // Basic validation
        if (!email || !password) {
            alert('Please fill in all fields');
            return;
        }
        
        // Here you would typically make an API call
        console.log('Login submitted:', { email, password });
        alert('Login successful! (This is a demo)');
    });

    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirm').value;
        
        // Validation
        if (!name || !email || !password || !confirmPassword) {
            alert('Please fill in all fields');
            return;
        }
        
        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }
        
        if (!document.querySelector('#signupForm input[type="checkbox"]').checked) {
            alert('You must agree to the terms');
            return;
        }
        
        // Here you would typically make an API call
        console.log('Signup submitted:', { name, email, password });
        alert('Account created successfully! (This is a demo)');
    });
});