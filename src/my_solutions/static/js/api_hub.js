document.addEventListener('DOMContentLoaded', () => {
	const buttonReceiveAccess = document.querySelector(
		'#api_go_documentation .button__receive_access'
	);

	buttonReceiveAccess.addEventListener('click', handleAcessClick);

	function handleAcessClick(event) {
		event.preventDefault();
		if (buttonReceiveAccess) {
			$('#api_go_documentation').modal('hide');
			Swal.fire({
				html: `<div class="loading_div_api d-flex justify-content-center align-items-center "><div class="loader loading_api"></div></div>`,
				showConfirmButton: false,
			});
			setTimeout(function () {
				swal.close();
				$('#api_request').modal('show');
			}, 2000);
			if (buttonReceiveAccess.disabled == false) {
				buttonReceiveAccess.disabled = true;
				buttonReceiveAccess.innerHTML = `Acesso Solicitado`;
			}
			sendEmail();
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

			const response = await fetch('api-hub/request/email', settings);

			return response;
		}
	}
});
