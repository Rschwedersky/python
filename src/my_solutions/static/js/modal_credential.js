function canSubmit(formElements) {
	let input = formElements.find('input[name=name]');
	let login = formElements.find('input[name=login]');
	let pass = formElements.find('input[name=pass]');
	let is_email_valid = isAllEmailsValid();
	let file_format = formElements.find('input[name=file_format]:checked');
	let cansubmit = false;
	if (
		login.val().length > 2 &&
		pass.val().length > 2 &&
		input.val().length > 0 &&
		is_email_valid &&
		file_format.val() != '' &&
		file_format.val() != undefined
	) {
		cansubmit = true;
	}
	return cansubmit;
}

function getModelFormBodyParams(formElements) {
	const content = {
		name: formElements.name.value,
		login: formElements.login.value,
		pass: formElements.pass.value,
		automation: formElements.automation.value,
		action_type: formElements['action_type'].value,
		email_to_send_results: getAllEmailsToSendResults(),
		file_format: formElements['file_format'].value,
	};

	content['extra_info'] = '';
	content['link_results'] = '';

	const filter_notes = document.getElementById('filter_notes');
	if (filter_notes) {
		content['filter_notes'] = 'periodo';
		content['extra_info'] = formElements.periodo?.value;
	}

	if (formElements.link_results) {
		content['link_results'] = formElements.link_results?.value;
	}

	const formData = new FormData();

	Object.entries(content).forEach(([key, value]) => formData.append(key, value));

	return formData;
}

function submitAutomation(formElements) {
	let cansubmit = canSubmit(formElements);
	if (cansubmit) {
		const btn = $('#modalExemplo .modal-footer .btn-advance.submit');
		btn.replaceWith(getLoadingDiv(true, ' small'));
		submitForm();
	} else {
		Swal.fire('Oops..', translate['it_is_not_possible_to_save_usage'][language], 'error');
	}
}

function updateFormInfos(formElements, automation) {
	if (
		automation.find(`.automation_extra_info`).length > 0 &&
		automation.find(`.automation_extra_info`).val() != ''
	) {
		updateDatesFilterNotes(automation.find(`.automation_extra_info`).val());
	}
	formElements.find('input[name=name]').val(automation.find('.box_header p').html());
	let radio_inputs = document.getElementsByName('file_format');
	for (var i = 0; i < radio_inputs.length; i++) {
		radio_inputs[i].checked =
			radio_inputs[i].value == automation.find('.automation_file_format').val()
				? true
				: false;
	}
	let btn =
		automation.find('.automation_file_format').val() == 'csv' ? 'csv_button' : 'excel_button';
	$('#modalExemplo form .formato-group .btn.active').removeClass('active');
	formElements.find(`#${btn}`).addClass('active');
	formElements.find('input[name=email_to_send_results]').val('');
	fillAllEmails(automation.find('.automation_email').val());
}

function updateAutomationInfos(data) {
	let automation = $(`.automation[data-id=${data.id}]`);
	automation.find(`.box_header > p`).html(data.name);
	automation.find(`.automation_file_format`).val(data.file_format);
	automation.find(`.automation_email`).val(data.email_to_send_results);
	if (automation.find(`.automation_extra_info`).length > 0 && data.hasOwnProperty('extra_info')) {
		automation.find(`.automation_extra_info`).val(data.extra_info);
	} else if (data.hasOwnProperty('extra_info')) {
		automation.append(
			`<input type="hidden" class="automation_extra_info" value="${data.extra_info}" />`
		);
	} else if (
		!data.hasOwnProperty('extra_info') &&
		automation.find(`.automation_extra_info`).length > 0
	) {
		automation.find(`.automation_extra_info`).val('');
	}
	updateTemplateCron(automation[0], data.name);
}

function updateDatesFilterNotes(dateString) {
	document.getElementById('periodo').value = dateString;
	let dateToAndFrom = dateString.split('|');

	let date_from = new Date(`${dateToAndFrom[0]} 00:00`);
	let dateFromTarget = document.querySelector('.uploader-inner .from_date');
	// updateOnCalendar(dateFromTarget, date_from);
	let day =
		String(date_from.getDate()).length == 1 ? `0${date_from.getDate()}` : date_from.getDate();
	let month =
		String(date_from.getMonth() + 1).length == 1
			? `0${date_from.getMonth() + 1}`
			: date_from.getMonth() + 1;
	dateFromTarget.value = `${date_from.getFullYear()}-${month}-${day}`;

	let date_to = new Date(`${dateToAndFrom[1]} 00:00`);
	let dateToTarget = document.querySelector('.uploader-inner .to_date');
	// updateOnCalendar(dateToTarget, date_to);
	day = String(date_to.getDate()).length == 1 ? `0${date_to.getDate()}` : date_to.getDate();
	month =
		String(date_to.getMonth() + 1).length == 1
			? `0${date_to.getMonth() + 1}`
			: date_to.getMonth() + 1;
	dateToTarget.value = `${date_to.getFullYear()}-${month}-${day}`;
}
