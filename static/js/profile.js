document.addEventListener("DOMContentLoaded", function () {
    const saveButton = document.getElementById("save-name");
    const logoutButton = document.getElementById("logout");

    // Update Name
    saveButton.addEventListener("click", async function () {
        let newName = document.getElementById("new-name").value.trim();
        if (!newName) {
            alert("Name cannot be empty!");
            return;
        }

        let response = await fetch("/update-profile/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ name: newName }),
        });

        let result = await response.json();
        if (result.success) {
            document.getElementById("profile-name").innerText = newName;
            alert("Name updated successfully!");
        } else {
            alert("Error updating name.");
        }
    });

    // Logout
    logoutButton.addEventListener("click", function () {
        window.location.href = "/logout/";
    });

    // Function to get CSRF token
    function getCSRFToken() {
        return document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
    }
});
