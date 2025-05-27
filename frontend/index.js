const join_buttons= document.querySelectorAll('.join-button');
join_buttons.forEach(button => {
    button.addEventListener('click', function() {
        const role = this.getAttribute('data-role');
        joinAs(role);
    });
});

function joinAs(role) {
    const token = document.getElementById('tokenInput').value.trim();
    const errorDiv = document.getElementById('errorMsg');
    errorDiv.textContent = "";

    if (!token) {
        errorDiv.textContent = "Please enter a token before proceeding.";
        return;
    }

    // Save the token to sessionStorage so the next page can access it
    sessionStorage.setItem("authToken", token);

    // Redirect to appropriate page
    if (role === 'user') {
        location.href = 'user.html';
    } else if (role === 'admin') {
        location.href = 'admin.html';
    }
}