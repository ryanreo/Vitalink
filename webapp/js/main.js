// Modal functionality
function openLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function closeLogin() {
    document.getElementById('loginModal').style.display = 'none';
}

function openSignup() {
    document.getElementById('signupModal').style.display = 'block';
}

function closeSignup() {
    document.getElementById('signupModal').style.display = 'none';
}

function scrollToFeatures() {
    document.getElementById('features').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

// Close modals when clicking outside
window.onclick = function(event) {
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    
    if (event.target === loginModal) {
        closeLogin();
    }
    if (event.target === signupModal) {
        closeSignup();
    }
}

// Form submissions
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    // Add login logic here
    console.log('Login form submitted');
});

document.getElementById('signupForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    // Add signup logic here
    console.log('Signup form submitted');
});

// Check backend connection
fetch('http://localhost:5000/api/health')
    .then(response => response.json())
    .then(data => console.log('Backend status:', data))
    .catch(error => console.error('Backend connection failed:', error));