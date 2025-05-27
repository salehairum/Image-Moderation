async function loadTokens() {
    const token = sessionStorage.getItem("authToken");
    const errorDiv = document.getElementById("errorMsg");

    if (!token) {
        errorDiv.textContent = "No token found. Please login first.";
        return;
    }

    try {
        const response = await fetch("http://localhost:7000/auth/tokens", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if (!response.ok) {
            const errData = await response.json();
            errorDiv.textContent = errData.detail || "Failed to fetch tokens.";
            return;
        }

        const tokens = await response.json();
        const tbody = document.querySelector("#tokenTable tbody");

        tokens.forEach(tok => {
            const row = document.createElement("tr");

            const tokenCell = document.createElement("td");
            tokenCell.textContent = tok.token;
            row.appendChild(tokenCell);

            const isAdminCell = document.createElement("td");
            isAdminCell.textContent = tok.isAdmin ? "Admin" : "User";;
            row.appendChild(isAdminCell);

            const createdAtCell = document.createElement("td");
            createdAtCell.textContent = new Date(tok.createdAt).toLocaleString();
            row.appendChild(createdAtCell);

            tbody.appendChild(row);
        });

    } catch (err) {
        errorDiv.textContent = "Error connecting to server.";
        console.error(err);
    }
}

window.onload = loadTokens;

//add token mechanisms
document.querySelector('.add-button').addEventListener('click', () => {
    document.getElementById('addTokenModal').style.display = 'block';
});

document.querySelector('#cancelAddToken').addEventListener('click', () => {
    document.getElementById('addTokenModal').style.display = 'none';
});

window.addEventListener('click', (event) => {
    const modal = document.getElementById('addTokenModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

document.getElementById('addTokenForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = document.getElementById('newTokenInput').value.trim();
    const isAdmin = document.getElementById('isAdminCheckbox').checked;
    const errorDiv = document.getElementById('errorMsgModal');
    errorDiv.textContent = '';

    if (!token) {
        errorDiv.textContent = 'Token cannot be empty.';
        return;
    }

    try {
        const authToken = sessionStorage.getItem('authToken');
        const response = await fetch('http://localhost:7000/auth/tokens', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + authToken
            },
            body: JSON.stringify({
                token,
                isAdmin
            })
        });

        if (!response.ok) {
            const err = await response.json();
            errorDiv.textContent = err.detail || 'Error creating token.';
            return;
        }

        document.getElementById('addTokenModal').style.display = 'none';
        location.reload();  // Reload to show the new token
    } catch (err) {
        errorDiv.textContent = 'Server error. Try again.';
        console.error(err);
    }
});

//delete token mechanisms
document.querySelector('.delete-button').addEventListener('click', () => {
    document.getElementById('deleteTokenModal').style.display = 'block';
});

document.querySelector('#cancelDeleteToken').addEventListener('click', () => {
    document.getElementById('deleteTokenModal').style.display = 'none';
});

window.addEventListener('click', (event) => {
    const modal = document.getElementById('deleteTokenModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

document.getElementById('deleteTokenForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = document.getElementById('tokenInput').value.trim();
    const errorDiv = document.getElementById('deleteErrorMsgModal');
    errorDiv.textContent = '';

    if (!token) {
        errorDiv.textContent = 'Token cannot be empty.';
        return;
    }

    try {
        const authToken = sessionStorage.getItem('authToken');
        const response = await fetch(`http://localhost:7000/auth/tokens/${token}`, {
            method: "DELETE",
            headers: {
                'Authorization': 'Bearer ' + authToken
            }
        });

        if (!response.ok) {
            const err = await response.json();
            console.log(err.detail)
            errorDiv.textContent = err.detail || 'Error deleting token.';
            return;
        }

        document.getElementById('deleteTokenModal').style.display = 'none';
        location.reload();  // Reload to show the new token
    } catch (err) {
        errorDiv.textContent = 'Server error. Try again.';
        console.error(err);
    }
});

//go to moderate image
document.querySelector('.moderate-button').addEventListener('click', () => {
    const token = sessionStorage.getItem("authToken");
    if (!token) {
        document.getElementById('errorMsg').textContent = "Please login first.";
        return;
    }
    location.href = 'moderate.html';
});