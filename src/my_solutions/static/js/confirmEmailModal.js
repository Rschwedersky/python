document.addEventListener('DOMContentLoaded', () => {
	const resendEmail = document.querySelector('#onboarding__modal_1 .resend_email');

	resendEmail?.addEventListener('click', (event) => {
		sendVerificationEmailAgain(event, false);
	});

	async function sendVerificationEmailAgain() {
		if (resendEmail) {
			$('#onboarding__modal_1').modal('hide');
			Swal.fire({
				title: `<h5 class="modal-title"><strong>Confirme seu e-mail</strong></h5>`,
				html: `<div class="loading_div_api d-flex justify-content-center align-items-center "><div class="loader loading_api"></div></div>`,
				showConfirmButton: false,
			});
			setTimeout(function () {
				swal.close();
				$('#modal__confirm_email').modal('show');
			}, 2000);
		}

		try {
			const response = await sendEmailAgain();
		} catch (error) {
			Swal.fire('Oops..', 'error');
		} finally {
			$('#onboarding__modal_1').modal('hide');
		}
	}

	async function sendEmailAgain() {
		const csrftoken = getCookie('csrftoken');
		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({}),
		};

		const response = await fetch('/accounts/send-email-confirmation', settings);
		if (!response.ok) return Promise.reject(response);

		return response;
	}
});
