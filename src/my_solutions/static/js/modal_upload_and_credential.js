function canSubmit(formElements) {
	const is_email_valid = isAllEmailsValid();
	const input = formElements.find('input[name=name]');
	const login = formElements.find('input[name=login]');
	const pass = formElements.find('input[name=pass]');
	const file_format = formElements.find('input[name=file_format]:checked');
	const fileIsValid = formElements.find('input[name=file-input]')[0].files.length > 0;
	let cansubmit = false;
	if (
		login.val().length > 2 &&
		pass.val().length > 2 &&
		input.val().length > 0 &&
		fileIsValid &&
		is_email_valid &&
		file_format.val() != '' &&
		file_format.val() != undefined
	) {
		cansubmit = true;
	}
	return cansubmit;
}

function submitAutomation(formElements) {
	const emails_to_send_results = getAllEmailsToSendResults();
	const name_input = formElements.find('input[name=name]');
	const login = formElements.find('input[name=login]');
	const pass = formElements.find('input[name=pass]');
	const file_format = formElements.find('input[name=file_format]:checked');
	const fileIsValid =
		formElements.find('input[name=file-input]')[0].files.length > 0 ||
		formElements.find('input[name=file-input]')[0].classList.contains('js-fake');

	const cansubmit = canSubmit(formElements);
	const action_type = $('#modalExemplo form input[name=action_type]').val();

	if (cansubmit && action_type == 'edit' && !fileIsValid) {
		const btn = $('#modalExemplo .modal-footer .btn-advance.submit');
		btn.replaceWith(getLoadingDiv(true, ' small'));

		submitForm();
	} else if (cansubmit) {
		$('#modalExemplo .modal-footer .btn-advance.submit').replaceWith(
			getLoadingDiv(true, ' small')
		);
		submitForm();
	} else {
		Swal.fire('Oops..', translate['it_is_not_possible_to_save_usage'][language], 'error');
	}
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
		input_file: formElements['file-input'].files[0],
	};

	content['extra_info'] = '';

	const formData = new FormData();

	Object.entries(content).forEach(([key, value]) => formData.append(key, value));

	return formData;
}

function updateFormInfos(formElements, automation) {
	formElements.find('input[name=name]').val(automation.find('.box_header p').html());
	addFakeFileUpload(automation.find('.automation_upload').val());
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
	formElements.find('input[name=email_to_send_results]').val();
	fillAllEmails(automation.find('.automation_email').val());
}

function updateOnCalendar(dateTarget, date) {
	var dateInputEvent = new CustomEvent('changeDateInputCalendar', {
		detail: {
			input: dateTarget,
			newDate: date,
		},
	});
	// Dispatch/Trigger/Fire the event
	document.dispatchEvent(dateInputEvent);
}

function updateAutomationInfos(data) {
	let automation = $(`.automation[data-id=${data.id}]`);
	automation.find(`.box_header > p`).html(data.name);
	automation.find(`.automation_file_format`).val(data.file_format);
	automation.find(`.automation_email`).val(data.email_to_send_results);
	automation.find(`.automation_upload`).val(data.input_path);
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
