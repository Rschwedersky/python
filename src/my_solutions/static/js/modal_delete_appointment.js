document.addEventListener('DOMContentLoaded', () => {
	const jqueryModal = $('#modaldeleteappointment');
	jqueryModal.on('show.bs.modal', fillModalInfos);
	function fillModalInfos(event) {
		const targetButton = event.relatedTarget;
		$(targetButton.closest('.modal')).modal('hide');
		const modal = event.target;
		modal.querySelector('.template_name').textContent = targetButton.dataset.name;
		modal.querySelector('.delete_appointment.btn_smarthis').dataset.templateid =
			targetButton.dataset.id;
	}

	jqueryModal[0].addEventListener('click', handleDeleteClick);
	function handleDeleteClick(event) {
		const isConfirmDeletion =
			event.target.classList.contains('delete_appointment') ||
			event.target.closest('.delete_appointment');
		if (isConfirmDeletion) {
			const btn = event.target.classList.contains('delete_appointment')
				? event.target
				: event.target.closest('.delete_appointment');
			removeAppointment(btn);
		}
	}
	async function removeAppointment(submitBtn) {
		const id = submitBtn.dataset.templateid;
		replaceWith(submitBtn, getLoadingDiv(true, 'small'));
		const loading = document.querySelector('.loading_div');
		const settings = {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
		};
		const response = await fetch(`/schedules/appointment/${id}`, settings);
		const data = await response.text();
		if (response.ok) {
			Swal.fire(
				translate['success'][language],
				translate['appointment_removed_successfully'][language],
				'success'
			);
			const templateElement = document.querySelector(`[data-id="${id}"]`);
			templateElement.outerHTML = data;
			jqueryModal.modal('hide');
		} else {
			const json = JSON.parse(data);
			Swal.fire('Oops..', json.msg, 'error');
		}
		replaceWith(loading, submitBtn.outerHTML);
	}
});
