document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".login_form");
    const errorElement = document.querySelector(".error");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/student/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: email, password: password }),
            });

            if (response.ok) {
                window.location.href = "/student/dashboard";
            } else {
                const errorData = await response.json();
                errorElement.textContent = errorData.error || "Login failed";
                errorElement.classList.remove("error--hidden");
            }
        } catch (error) {
            errorElement.textContent = "An error occurred. Please try again.";
            errorElement.classList.remove("error--hidden");
        }
    });
});
