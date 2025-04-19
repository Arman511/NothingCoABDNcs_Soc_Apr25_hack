document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".login_form");
    const errorElement = document.querySelector(".error");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.querySelector("#email").value;
        const password = document.querySelector("#password").value;

        try {
            const response = await fetch("/professor/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: email, password: password }),
            });

            if (response.ok) {
                window.location.href = "/professor/dashboard";
            } else {
                const errorData = await response.json();
                errorElement.textContent = errorData.error || "An error occurred.";
                errorElement.classList.remove("error--hidden");
            }
        } catch (error) {
            errorElement.textContent = "Failed to connect to the server.";
            errorElement.classList.remove("error--hidden");
        }
    });
});
