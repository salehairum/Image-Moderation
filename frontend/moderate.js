const BASE_URL = window.API_BASE_URL;

const uploadButton = document.querySelector(".upload-button");
uploadButton.addEventListener("click", uploadImage);

async function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const loadingDiv = document.getElementById("loading");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image file first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    loadingDiv.style.display = "block";

    try {
        const token = sessionStorage.getItem("authToken");
        const response = await fetch(BASE_URL + '/moderate', {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            body: formData
        });

        const result = await response.json();
        const resultsDiv = document.getElementById("results");
        const resultBody = document.getElementById("resultBody");

        resultBody.innerHTML = "";

        if (!response.ok || !result.scores) {
            resultBody.innerHTML = `<tr><td colspan="2">Error: ${result.detail || "No scores returned"}</td></tr>`;
        } else {
            const sortedScores = Object.entries(result.scores).sort((a, b) => b[1] - a[1]);

            for (const [label, score] of sortedScores) {
                const row = `<tr><td>${label}</td><td>${(score * 100).toFixed(2)}%</td></tr>`;
                resultBody.innerHTML += row;
            }
        }

        resultsDiv.hidden = false;
        loadingDiv.style.display = "none";


    } catch (error) {
        alert("An error occurred: " + error.message);
    }
}