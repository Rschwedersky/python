function canSubmit(formElements) {
	const is_email_valid = isAllEmailsValid();
	const input = formElements.find('input[name=name]');
	const file_format = formElements.find('input[name=file_format]:checked');
	const fileIsValid =
		formElements.find('input[name=file-input]')[0].files.length > 0 ||
		formElements.find('input[name=file-input]')[0].classList.contains('js-fake');

	let cansubmit = false;
	if (
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
	const cansubmit = canSubmit(formElements);

	if (cansubmit) {
		$('#modalExemplo .modal-footer .btn-advance.submit').replaceWith(
			getLoadingDiv(true, ' small')
		);

		submitForm();
	}
}

function updateFormInfos(formElements, automation) {
	const modelNameEl = formElements.find('input[name=name]');
	modelNameEl.val(automation.find('.box_header p').html());
	modelNameEl.attr('data-old', automation.find('.box_header p').html());
	addFakeFileUpload(automation.find('.automation_upload').val());

	const radioInputs = document.getElementsByName('file_format');
	for (let i = 0; i < radioInputs.length; i++) {
		radioInputs[i].checked =
			radioInputs[i].value == automation.find('.automation_file_format').val() ? true : false;

		radioInputs[i].setAttribute('data-old', automation.find('.automation_file_format').val());
	}
	const btn =
		automation.find('.automation_file_format').val() == 'csv' ? 'csv_button' : 'excel_button';
	$('#modalExemplo form .formato-group .btn.active').removeClass('active');
	formElements.find(`#${btn}`).addClass('active');
	formElements.find('input[name=email_to_send_results]').val();
	fillAllEmails(automation.find('.automation_email').val());

	const hiddenInputWithEmails = document.createElement('input');
	hiddenInputWithEmails.type = 'hidden';
	hiddenInputWithEmails.name = 'old-emails';
	hiddenInputWithEmails.value = automation.find('.automation_email').val();

	document.querySelector('#modalExemplo form').append(hiddenInputWithEmails);
}

function getModelFormBodyParams(formElements, action) {
	const content = {};

	if (action.includes('new')) {
		content.name = formElements.name.value;
		content.automation = formElements.automation.value;
		content['action_type'] = formElements['action_type'].value;
		content['email_to_send_results'] = getAllEmailsToSendResults();
		content['file_format'] = formElements['file_format'].value;
		content['input_file'] = formElements['file-input'].files[0];
	} else {
		const emails = getAllEmailsToSendResults();

		content.name =
			formElements.name.value !== formElements.name.getAttribute('data-old')
				? formElements.name.value
				: '';

		content.automation = '';
		content['action_type'] = formElements['action_type'].value;
		content['email_to_send_results'] =
			emails !== formElements['old-emails'].value ? emails : '';
		content['file_format'] =
			formElements['file_format'].value !==
			formElements['file_format'][0].getAttribute('data-old')
				? formElements['file_format'].value
				: '';

		content['input_file'] = formElements['file-input'].files[0]
			? formElements['file-input'].files[0]
			: null;
	}

	const formData = new FormData();

	Object.entries(content).forEach(([key, value]) => formData.append(key, value));

	return formData;
}

function updateAutomationInfos(data) {
	let automation = $(`.automation[data-id=${data.id}]`);
	automation.find(`.box_header > p`).html(data.name);
	automation.find(`.automation_file_format`).val(data.file_format);
	automation.find(`.automation_email`).val(data.email_to_send_results);
	automation.find(`.automation_upload`).val(data.input_path);
	updateTemplateCron(automation[0], data.name);
}
