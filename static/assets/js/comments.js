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
});
