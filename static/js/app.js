// MATERIAL DESIGN INIT
$( document ).ready(function() {
    $.material.init()
});

$(document).ready(function(){
	$('#trigger-inscricao').click(function(event){
		event.preventDefault();
		$('#conteudo').children().hide();
		$('#inscricao').show('fast');
	})
});

$(document).ready(function(){
	$('#trigger-edicao').click(function(event){
		event.preventDefault();
		$('#conteudo').children().hide();
		$('#login').show('fast');
	})
});

$(document).ready(function(){
	$('.enviar-formulario').click(function(event){
		event.preventDefault();
		form = $(this).parent().parent().parent();
		if($('#nome').val() == '' || $('#cpf').val() == '' || $('#data-nascimento').val() == '' || $('#email').val() == '' || $('#curso').val() == ''  || $('#historico').val() == '' || $('#curriculum').val() == '' || $('#foto').val() == ''){
			alert('Existem campos obrigatorios nao preenchidos');
			return false;
		}
		form.submit();
	});
})
