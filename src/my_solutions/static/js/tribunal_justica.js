$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('#register_email').submit(function(e) {
        e.preventDefault();
        let $this = $(this);
        let error = [];
        error.push(validateInput($this, 'login', 'É necessário informar o login'));
        error.push(validateInput($this, 'password', 'É necessário informar o password'));
        error.push(validateInput($this, 'email', 'É necessário informar o email'));
        error = error.filter(function(val) { return val; });
        if(error.length == 0) {
            $.post($this.attr('action'), $this.serialize(), function(data) {
                $('#tribunal_justica_content').html(data);
                $('[data-toggle="tooltip"]').tooltip();
            })
        }
    });
});

function validateInput($this, inputname, text) {
    let error = false
    let input = $this.find(`input[name=${inputname}]`);
    if(input.val().length < 2) {
        input.parent().find('.text_error').html(text);
        error = true;
    }
    return error;
}