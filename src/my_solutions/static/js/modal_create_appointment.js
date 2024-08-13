document.addEventListener('DOMContentLoaded', () => {
	const modalCreate = document.getElementById('modalcreateappointment');
	const modalConfirm = document.getElementById('modalconfirmschedule');
	modalConfirm.addEventListener('click', handleClickModalConfirm);
	function handleClickModalConfirm(e) {
		const isButtonSubmit =
			e.target.closest('.send_appointment') ||
			e.target.classList.contains('send_appointment');
		if (!e.target.closest('.modal-dialog.content_confirm_appointment') && !isButtonSubmit) {
			showModalCreate();
		}
	}

	$(modalCreate).on('show.bs.modal', handleAppointmentsClicks);
	function handleAppointmentsClicks(e) {
		const targetButton = e.relatedTarget;
		if (targetButton.classList.contains('edit_appointment')) {
			$(targetButton.closest('.modal')).modal('hide');
			showCreateAppointmentModal(
				targetButton.dataset.target,
				targetButton.dataset.id,
				targetButton.dataset.cronexpression,
				targetButton.dataset.executiondate
			);
		} else {
			showCreateAppointmentModal(targetButton.dataset.target, targetButton.dataset.id, '');
		}
	}

	function showCreateAppointmentModal(modalElement, id, cronExpression, executionDate) {
		const createModal = document.querySelector(modalElement);
		let date = getNowMinDate();
		let submitText = translate['create_appointment'][language];
		let submitValue = 'create';
		if (executionDate) {
			date = new Date(`${executionDate} 00:00:00`);
			submitText = translate['edit_appointment'][language];
			submitValue = 'edit';
		}
		const confirmationBtn = createModal.querySelector('.confirm_appointment');
		confirmationBtn.value = submitValue;
		confirmationBtn.textContent = submitText;
		document.querySelector('#modalconfirmschedule .send_appointment').textContent = submitText;
		createModal.querySelector('.appointment_date').value = getDateFormatted(date, 'yyyy-mm-dd');
		let dateString = getDateText(date);
		const recurrence = getRecurrenceFromCron(cronExpression);
		createModal.querySelector('select[name=recurrence]').value = recurrence;
		createModal.querySelector('.date_execution').innerHTML = dateString;
		createModal.querySelector('.date_execution_period').innerHTML = dateString;
		modalConfirm.querySelector('.send_appointment').dataset.id = id;
	}

	function getRecurrenceFromCron(cronExpression) {
		cronArray = cronExpression.split(' ');
		let recurrence = 0;
		if (cronArray.length === 6) {
			recurrence = 0;
		} else if (cronArray[2] !== '*') {
			recurrence = 30;
		} else if (cronArray[4] !== '*') {
			recurrence = 7;
		}
		return recurrence;
	}

	const appointmentDate = modalCreate.querySelector('.appointment_date');
	appointmentDate.addEventListener('change', handleAppointmentChange);
	function handleAppointmentChange(e) {
		const dateObj = isDateValid(e.currentTarget.value);
		if (!dateObj['isValid']) {
			Swal.fire(
				'Oops..',
				translate['the_date_must_be_greater_than_1_days_from_today'][language],
				'warning'
			);
			dateObj['date'] = dateObj['now'];
		}
		e.currentTarget.value = getDateFormatted(dateObj['date'], 'yyyy-mm-dd');
		modalCreate.querySelector('.appointment_date').value = getDateFormatted(
			dateObj['date'],
			'yyyy-mm-dd'
		);
		let dateString = getDateText(dateObj['date']);
		modalCreate.querySelector('.date_execution').innerHTML = dateString;
		modalCreate.querySelector('.date_execution_period').innerHTML = dateString;
	}

	const closeConfirmBtn = modalConfirm.querySelector('.close');
	const cancelAppointmentBtn = document.querySelector('.btn_modal.cancel_confim_appointment');
	cancelAppointmentBtn.addEventListener('click', showModalCreate);
	closeConfirmBtn.addEventListener('click', showModalCreate);
	function showModalCreate() {
		modalCreate.classList.remove('d-none');
	}

	const confirmationBtn = modalCreate.querySelector('.confirm_appointment');
	confirmationBtn.addEventListener('click', handleConfirmationBtn);
	function handleConfirmationBtn(e) {
		modalCreate.classList.add('d-none');
		const recurrence = modalCreate.querySelector('#recurrence')?.value;
		const executionDate = new Date(`${appointmentDate.value} 00:00:00`);
		modalConfirm.querySelector('.execution_time-text').innerHTML =
			getAppointmentConfirmationText(recurrence, executionDate);
	}

	const sendAppointmentBtn = modalConfirm.querySelector('.send_appointment');
	sendAppointmentBtn.addEventListener('click', handleSubmitAppointment);
	function handleSubmitAppointment(e) {
		const recurrence = modalCreate.querySelector('#recurrence')?.value;
		const executionDate = appointmentDate.value;
		const id = e.currentTarget.dataset.id;
		const dateObj = isDateValid(executionDate);
		if (!dateObj['isValid']) {
			Swal.fire(
				'Oops..',
				translate['the_date_must_be_greater_than_1_days_from_today'][language],
				'warning'
			);
		} else {
			const submitBtn = e.currentTarget;
			replaceWith(submitBtn, getLoadingDiv(true, 'small'));
			const loading = document.querySelector('.loading_div');
			const settings = {
				method: 'PUT',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify({
					recurrence,
					executionDate,
					id,
				}),
			};

			fetch(`/schedules/appointment`, settings)
				.then(function (response) {
					// The API call was successful!
					return response.text();
				})
				.then(function (data) {
					replaceWith(loading, submitBtn.outerHTML);
					modalConfirm
						.querySelector('.send_appointment')
						.addEventListener('click', handleSubmitAppointment);
					try {
						const json = JSON.parse(data);
						Swal.fire('Oops..', json.msg, 'warning');
					} catch (err) {
						const successMsg =
							confirmationBtn.value === 'edit'
								? translate['appointment_edited_successfully'][language]
								: translate['appointment_created_successfully'][language];
						Swal.fire(translate['success'][language], successMsg, 'success');
						modalConfirm.querySelector('.close').click();
						modalCreate.querySelector('.close').click();
						const templateElement = document.querySelector(`[data-id="${id}"]`);
						templateElement.outerHTML = data;
					}
				})
				.catch(function (err) {
					replaceWith(loading, submitBtn.outerHTML);
					modalConfirm
						.querySelector('.send_appointment')
						.addEventListener('click', handleSubmitAppointment);
					Swal.fire('Oops..', 'Error', 'error');
				});
		}
	}

	const getNowMinDate = () => {
		const now = new Date();
		now.setDate(now.getDate() + 1);
		return now;
	};

	const getAppointmentConfirmationText = (recurrence = 30, date) => {
		let finalText = translate['your_template_will_be_executed'][language];
		if (recurrence == 30) {
			const day = String(date.getDate()).length == 1 ? `0${date.getDate()}` : date.getDate();
			finalText += ` ${translate['monthly'][language]}, ${
				translate['every_day'][language]
			} ${day}, ${translate['starting_in'][language]} ${getDateText(date)}`;
		} else if (recurrence == 7) {
			const maleWeekDays = {
				'pt-BR': [0, 6],
				es: [4, 6],
			};
			let weekDay = date.getDay();
			let weekDayTranslated = translate[`week_${weekDay}`][language];
			let everyText = translate['every_female'][language];
			if (maleWeekDays[language] && maleWeekDays[language].indexOf(weekDay) !== -1) {
				everyText = translate['every_male'][language];
			}
			finalText += ` ${
				translate['weekly'][language]
			}, ${everyText} <strong>${weekDayTranslated}</strong>, ${
				translate['starting_in'][language]
			} ${getDateText(date)}`;
		} else if (recurrence == 0) {
			finalText += ` ${getDateText(date)} ${translate['without_repeat'][language]}`;
		}
		return finalText;
	};

	const isDateValid = (dateStr) => {
		const now = getNowMinDate();
		const seconds = now.getSeconds();
		const minutes = now.getMinutes();
		const hour = now.getHours() + 1;
		let date = new Date(`${dateStr} ${hour}:${minutes}:${seconds}`);
		return { date, isValid: date.valueOf() > now.valueOf(), now };
	};
});

const getDateFormatted = (date, format = 'yyyy-mm-dd') => {
	const day = String(date.getDate()).length == 1 ? `0${date.getDate()}` : date.getDate();
	let month = date.getMonth() + 1;
	if (format.includes('mm') && String(month).length == 1) {
		month = `0${month}`;
	}
	let dateFormatted = '';
	if (format == 'yyyy-mm-dd') {
		dateFormatted = `${date.getFullYear()}-${month}-${day}`;
	}
	return dateFormatted;
};

const getDateText = (date) => {
	let translatedMonth = `month_${date.getMonth() + 1}`;
	return language == 'en'
		? `${translate[translatedMonth][language]} ${date.getDate()}, ${date.getFullYear()}`
		: `${date.getDate()} ${translate['of'][language]} ${translate[translatedMonth][language]} ${
				translate['of'][language]
		  } ${date.getFullYear()}`;
};
