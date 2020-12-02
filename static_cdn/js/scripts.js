
//Only for Demo animation Selection

$(window).bind("load", function() {
   $(".light-modal-body #id_email").val('');
});
$(document).ready(function() {
    $('.light-modal-content').not('.no').removeClass().addClass('flipInY light-modal-content animated');

    $(function(){
        setTimeout(function(){
            $('#alertos').slideUp(2000);
        }, 10000);
    });
});


