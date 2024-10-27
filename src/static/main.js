// function filterScheduledPosts() {
//     const posts = document.querySelectorAll('.post')
//     const selection = document.getElementById('scheduled_post_filter').value
//     posts.forEach(post => {
//         const isRecurring = post.dataset.recurring;
//         // if ((selection == "recurring" & isRecurring == "false") || (selection == "scheduled" & isRecurring == "true")) {
//         if (isRecurring != (selection == "recurring")) {
//             post.style.display = "none"
//         } else {
//             post.style.display = ""
//         }
//     })
// }
// document.addEventListener("DOMContentLoaded", function() {
//     document.getElementById('scheduled_post_filter').addEventListener("change", filterScheduledPosts)
// }) TODO: Future functionality ^^

function deletePost(id) {
    // Construct the endpoint URL with the given id
    const url = `/content-manager/delete/${id}`;

    // Send a DELETE request using Fetch API
    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // If the request was successful, handle success (e.g., refresh the page)
            console.log(`Post with ID ${id} deleted successfully.`);
            window.location.reload();
        } else {
            // If the request was not successful, handle the error
            return response.json().then(errorData => {
                console.error('Error:', errorData);
            });
        }
    })
    .catch(error => {
        console.error('Network error:', error);
    });
}
