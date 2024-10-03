$(document).ready(function () {
    $('input[name="status"]').change(function () {
        if (this.value === 'd') {
            $('#buy-dvd-section').show();
            $('#buy-dvd-section input, #buy-dvd-section textarea').attr('required', true);
        } else {
            $('#buy-dvd-section').hide();
            $('#buy-dvd-section input, #buy-dvd-section textarea').attr('required', false);
        }
    }).change();
});