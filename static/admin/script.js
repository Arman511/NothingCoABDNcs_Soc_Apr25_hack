document.addEventListener("DOMContentLoaded", () => {
    const addProfForm = document.querySelector(".add_prof");
    const addStuForm = document.querySelector(".add_stu");

    // Handle Add Professor Form Submission
    addProfForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("email_prof").value;
        const password = document.getElementById("password_prof").value;

        try {
            const response = await fetch("/add_professor", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                showError(addProfForm, errorData.error || "Failed to add professor.");
            } else {
                alert("Professor added successfully!");
                addProfForm.reset();
            }
        } catch (error) {
            showError(addProfForm, "An error occurred. Please try again.");
        }
    });

    // Handle Add Student Form Submission
    addStuForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("email_stu").value;
        const password = document.getElementById("password_stu").value;

        try {
            const response = await fetch("/add_student", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                showError(addStuForm, errorData.error || "Failed to add student.");
            } else {
                alert("Student added successfully!");
                addStuForm.reset();
            }
        } catch (error) {
            showError(addStuForm, "An error occurred. Please try again.");
        }
    });

    // Utility function to show error messages
    function showError(form, message) {
        const errorElement = form.querySelector(".error");
        errorElement.textContent = message;
        errorElement.classList.remove("error--hidden");
    }
});
