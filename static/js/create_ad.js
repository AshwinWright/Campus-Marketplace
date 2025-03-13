document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded!");  // Debug message

    document.getElementById("productForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        console.log("Form submitted!");  // Debug message

        let formData = new FormData(this);

        // Get CSRF token from the hidden input field in the form
        let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        try {
            let response = await fetch("/post_ad/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken  // Include CSRF token in request header
                }
            });

            console.log("Response received:", response.status);  // Debug log

            if (response.status === 403) {
                let result = await response.json();
                alert(result.error + "\nClick here to login: " + window.location.origin + result.login_url);
                return;
            }

            let result = await response.json();
            alert(result.message);
            window.location.href = "/"; // Redirect to homepage
        } catch (error) {
            console.error("Error submitting form:", error);
            alert("An error occurred. Please try again.");
        }
    });
});
