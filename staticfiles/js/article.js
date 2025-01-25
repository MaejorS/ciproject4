document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".delete-post-button"); // Buttons that trigger the modal
    const deleteConfirm = document.getElementById("deleteConfirm"); // "Delete" button in the modal

    // Loop through all delete buttons and add event listeners
    deleteButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            const deleteUrl = button.getAttribute("data-url"); // URL passed from the button's data-url attribute
            deleteConfirm.href = deleteUrl; // Set the href of the modal "Delete" button
        });
    });
});