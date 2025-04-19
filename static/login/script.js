document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector(".login_form");
    const errorElement = document.querySelector(".error");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const isProf = document.getElementById("isProf").checked;

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    isProf: isProf,
                    username: email,
                    password: password,
                }),
            });

            if (response.ok) {
                let data = await response.json();

                window.location.href = data.message;
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
