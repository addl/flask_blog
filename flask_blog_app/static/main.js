$(document).ready(function() {
    $("#subscriptionForm").submit(function(e) {
        e.preventDefault();
        $.ajax({
            method: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize()
        }).done(function( msg ) {
            $('#subscriptionForm .feedback').toggleClass('active');
        });
    });
});