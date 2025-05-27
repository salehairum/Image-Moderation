const join_buttons = document.querySelectorAll('.join-button');
join_buttons.forEach(button => {
    button.addEventListener('click', function () {
        const role = this.getAttribute('data-role');
        joinAs(role);
    });
});

async function joinAs(role) {
    const token = document.getElementById('tokenInput').value.trim();
    const errorDiv = document.getElementById('errorMsg');
    errorDiv.textContent = "";

    if (!token) {
        errorDiv.textContent = "Please enter a token before proceeding.";
        return;
    }

    try {
        const response = await fetch('http://localhost:7000/login/verify-token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token: token,
                isAdmin: role === 'admin'
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            errorDiv.textContent = errorData.detail || "Token verification failed.";
            return;
        }

        // If verification successful, save to storage
        sessionStorage.setItem("authToken", token);

        if (role === 'user') {
            location.href = 'moderate.html';
        } else if (role === 'admin') {
            location.href = 'admin.html';
        }

    } catch (error) {
        errorDiv.textContent = "Error connecting to server.";
        console.error(error);
    }
}