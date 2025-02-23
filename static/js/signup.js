document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");

    signupForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        let fullname = document.querySelector("input[name='name']").value.trim();
        let college_id = document.querySelector("input[name='college_id']").value.trim();
        let email = document.querySelector("input[name='email']").value.trim();
        let phone = document.querySelector("input[name='phone']").value.trim();
        let department = document.querySelector("select[name='department']").value;
        let password = document.querySelector("input[name='password']").value.trim();
        let confirm_password = document.querySelector("input[name='confirm_password']").value.trim();

        // Basic validation
        if (!fullname || !college_id || !email || !phone || !department || !password || !confirm_password) {
            alert("All fields are required!");
            return;
        }

        // Check if phone number is valid (basic check for 10-digit number)
        let phonePattern = /^[0-9]{10}$/;
        if (!phonePattern.test(phone)) {
            alert("Enter a valid 10-digit phone number!");
            return;
        }

        // Check if passwords match
        if (password !== confirm_password) {
            alert("Passwords do not match!");
            return;
        }

        // If all checks pass, submit the form
        signupForm.submit();
    });
});
