document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");

    if (!loginForm) {
        console.error("❌ Form not found in login.js");
        return;
    }

    loginForm.addEventListener("submit", function (event) {
        const college_id_input = document.querySelector('input[name="college_id"]');
        const password_input = document.querySelector('input[name="password"]');

        if (!college_id_input || !password_input) {
            console.error("❌ Input fields not found");
            return;
        }

        const college_id = college_id_input.value.trim();
        const password = password_input.value.trim();

        console.log("📌 Login Attempt - College ID:", college_id, "Password:", password);

        if (!college_id || !password) {
            alert("Please fill in all fields!");
            event.preventDefault(); // Prevent form submission if fields are empty
            return;
        }

       
    });
});
