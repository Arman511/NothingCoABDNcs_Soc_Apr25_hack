document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("updateForm");
    const errorElement = document.querySelector(".error");
    const successElement = document.querySelector(".success");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Get selected courses
        const selectedCourses = Array.from(document.getElementById("courses").selectedOptions).map((option) => option.value);

        if (selectedCourses.length === 0) {
            errorElement.textContent = "Please select at least one course.";
            errorElement.classList.remove("error--hidden");
            successElement.classList.add("success--hidden");
            return;
        }

        // Prepare data to send
        const data = { courses: selectedCourses };

        try {
            const response = await fetch("/student/add_update_courses", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                successElement.textContent = result.message || "Courses updated successfully!";
                successElement.classList.remove("success--hidden");
                errorElement.classList.add("error--hidden");
            } else {
                errorElement.textContent = result.error || "An error occurred.";
                errorElement.classList.remove("error--hidden");
                successElement.classList.add("success--hidden");
            }
        } catch (error) {
            errorElement.textContent = "Failed to update courses. Please try again.";
            errorElement.classList.remove("error--hidden");
            successElement.classList.add("success--hidden");
        }
    });
});
