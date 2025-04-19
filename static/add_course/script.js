document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".add_course_form");
    const errorElement = document.querySelector(".error");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Collect form data
        const courseData = {
            course_id: form.course_id.value.trim(),
            course_name: form.course_name.value.trim(),
            description: form.description.value.trim(),
        };

        // Validate form data
        if (!courseData.course_id || !courseData.course_name || !courseData.description) {
            showError("All fields are required.");
            return;
        }

        try {
            // Send POST request to the server
            const response = await fetch("/add_course", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",
                },
                body: JSON.stringify(courseData),
            });

            const result = await response.json();

            if (!response.ok) {
                showError(result.error || "An error occurred while adding the course.");
            } else {
                alert(result.message || "Course added successfully!");
                form.reset();
                errorElement.classList.add("error--hidden");
                errorElement.textContent = "";
            }
        } catch (error) {
            showError("Failed to connect to the server. Please try again later.");
        }
    });

    function showError(message) {
        errorElement.textContent = message;
        errorElement.classList.remove("error--hidden");
    }
});
