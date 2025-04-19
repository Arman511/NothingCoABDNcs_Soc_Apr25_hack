document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form[name="add_tut"]');
    const errorElement = document.querySelector(".error");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {
            course: formData.get("course"),
            tutorial_name: formData.get("tutorial_name"),
            tutorial_description: formData.get("tutorial_description"),
            tutorial_release_date: formData.get("tutorial_release_date"),
            tutorial_due_date: formData.get("tutorial_due_date"),
            tutorial_answer_release_date: formData.get("tutorial_answer_release_date"),
            tutorial_questions: [],
        };

        const questionDivs = document.querySelectorAll(".question");
        questionDivs.forEach((div, index) => {
            const question = {
                custom_id: div.querySelector(`[name^="questions[${index}][custom_id]"]`)?.value || "",
                question_title: div.querySelector(`[name^="questions[${index}][question_title]"]`)?.value || "",
                question_hint: div.querySelector(`[name^="questions[${index}][question_hint]"]`)?.value || "",
                question_answer: div.querySelector(`[name^="questions[${index}][question_answer]"]`)?.value || "",
            };

            data.tutorial_questions.push(question);
        });

        try {
            const response = await fetch("/tutorials/add_tutorial", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (!response.ok) {
                errorElement.textContent = result.error || "Something went wrong!";
                errorElement.classList.remove("error--hidden");
                return;
            }

            // Success
            alert(`Tutorial created! ID: ${result.tutorial_id}`);
            form.reset();
            document.getElementById("questions-section").innerHTML = "";
            questionCount = 0;
        } catch (err) {
            errorElement.textContent = "Request failed.";
            errorElement.classList.remove("error--hidden");
        }
    });
});
