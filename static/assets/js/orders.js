$(document).ready(function () {
    function toggleDvdSection() {
        const isDvdSelected = $('input[name="status"]:checked').val() === 'd';
        if (isDvdSelected) {
            $('#buy-dvd-section').show();
            $('#buy-dvd-section input, #buy-dvd-section textarea').attr('required', true);
        } else {
            $('#buy-dvd-section').hide();
            $('#buy-dvd-section input, #buy-dvd-section textarea').attr('required', false);
        }
    }

    $('input[name="status"]').change(toggleDvdSection);

    toggleDvdSection();
});