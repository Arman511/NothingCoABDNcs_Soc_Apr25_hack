document.getElementById("submit").addEventListener("click", async () => {
    const ratings = {};
    const comments = {};
    const uuid = document.getElementById("uuid").getAttribute("data-id");
    const errorElement = document.querySelector(".error");
    const successElement = document.querySelector(".success");

    // Collect ratings from the dropdowns
    document.querySelectorAll("select[name^='rating_']").forEach((select) => {
        const questionId = select.name.replace("rating_", "");
        const rating = select.value;
        ratings[questionId] = parseInt(rating, 10);
        comments[questionId] = document.querySelector(`textarea[name='comment_${questionId}']`).value;
    });

    // Send the ratings to the server
    try {
        const response = await fetch(`/tutorials/update_record?uuid=${uuid}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ratings, comments }),
        });

        const result = await response.json();

        if (response.ok) {
            successElement.textContent = result.message;
            successElement.classList.remove("success--hidden");
            errorElement.classList.add("error--hidden");
        } else {
            throw new Error(result.error || "Failed to update ratings.");
        }
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove("error--hidden");
        successElement.classList.add("success--hidden");
    }
});
