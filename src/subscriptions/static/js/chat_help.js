document.addEventListener('DOMContentLoaded', () => {
	const buttonSubmit = document.querySelector('.footer_modal__chat_help .btn__chat_help');
	const formAssunto = document.querySelector('.box_chat__modal-form .text_assunto');
	const formMensagem = document.querySelector('.box_chat__modal-form .text_mensagem');
	window.addEventListener('resize', setChatBoxPosition);

	buttonSubmit.addEventListener('submit', handleSubmitFormHelp);
	formMensagem.addEventListener('input', handleSubmitFormHelp);
	formAssunto.addEventListener('input', handleSubmitFormHelp);
	buttonSubmit.addEventListener('click', hadleButtonSubmit);

	setChatBoxPosition();

	function setChatBoxPosition() {
		const chatBox = document.getElementById('box_chat-help-center');
		const windowWidth = window.innerWidth;
		const containerWidth = document.querySelector('.jsHelpContainer').offsetWidth;
		const margin = (windowWidth - containerWidth) / 2;

		chatBox.style.right = `${margin + 42}px`;
	}

	function handleSubmitFormHelp() {
		buttonSubmit.disabled = !(
			formAssunto.value.trim().length > 2 && formMensagem.value.trim().length
		);
	}

	function hadleButtonSubmit() {
		$.post(
			'help_center/faq_doubts',
			{
				formAssunto: formAssunto.value,
				formMensagem: formMensagem.value,
				csrfmiddlewaretoken: getCSRFauth(),
			},
			function (data) {
				if (data['status'] == 200) {
					Swal.fire({
						title: `<strong class="f-size-18 success-register_area color000000">Mensagem enviada com sucesso<div class="green__underlined green__chat-help"></div></strong>`,
						html:
							`<div class="sub-text_swal_chat color000000"><p class="f-size-16">Em breve, responderemos sua dúvida pelo e-mail cadastrado no Smarthis Hub.</p></div>` +
							'<div class="position_img-chat"><img class="img_check-chat" src=static/dashboard/img/logo-check.png ></div>',
						customClass: {
							popup: 'swal2-popup swal-wide-help_center',
							actions: 'justify-content-end',
							cancelButton: 'btn_chat-help',
							header: 'align-items-start',
						},
						showConfirmButton: false,
						showCloseButton: true,
						showCancelButton: true,
						cancelButtonText: 'OK',
						closeButtonHtml: '<span class="dark-gray__color">&times;</span>',
						buttonsStyling: true,
					});
					$('#form').modal('hide');
					$('.box_chat__modal-form .text_assunto').val('');
					$('.box_chat__modal-form .text_mensagem').val('');
					handleSubmitFormHelp();
				} else {
					Swal.fire('Oops..', data['msg'], 'error');
				}
			}
		);
	}
});
