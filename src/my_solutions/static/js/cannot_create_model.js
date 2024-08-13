document.addEventListener('DOMContentLoaded', () => {
	const btnAccessCreateModel = document.querySelector(
		'#modal_request_create_model .btn_cannot_create_model_access'
	);

	btnAccessCreateModel.addEventListener('click', handleModalCreation);

	function handleModalCreation(event) {
		event.preventDefault();
		if (btnAccessCreateModel) {
			$('#modal_request_create_model').modal('hide');
			Swal.fire({
				html: `<div class="loading_div_api d-flex justify-content-center align-items-center "><div class="loader loading_api"></div></div>`,
				showConfirmButton: false,
			});
			setTimeout(function () {
				swal.close();
				$('#request_create_model_success').modal('show');
			}, 2000);
			if (btnAccessCreateModel.disabled == false) {
				btnAccessCreateModel.disabled = true;
				btnAccessCreateModel.innerHTML = `${translate['contact_requested'][language]}`;
			}
			sendEmail();
		}
	}
	async function sendEmail() {
		const csrftoken = getCookie('csrftoken');
		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({}),
		};

		const response = await fetch('/services/request-modal-creation/extrato-bancario', settings);

		return response;
	}
});
