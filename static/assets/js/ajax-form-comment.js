document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.reply-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-id');
            document.getElementById('parent_id').value = commentId;
            const formElement = document.querySelector('.postbox__comment-form');
            formElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    const commentForm = document.getElementById('comment-form');
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(commentForm);

        fetch(commentForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Adjust this if your CSRF token field is named differently
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle successful comment submission (e.g., append the new comment to the comment list)
                console.log('Comment added successfully');
            } else {
                // Handle errors
                console.error('Error adding comment:', data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
