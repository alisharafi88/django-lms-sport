$(document).ready(function () {
    console.log($('input[name="status"]').attr('name'));
    $('input[name="status"]').change(function () {
        console.log(this.value);
        if (this.value === 'd') {
            $('#buy-dvd-section').show();
        } else {
            $('#buy-dvd-section').hide();
        }
    });
});