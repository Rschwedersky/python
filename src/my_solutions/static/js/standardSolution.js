function updateScheduleState(automation) {
	let id = automation.dataset.id;
	$.get(`/api/v1/get_schedule_state/${id}`)
		.then(function (data) {
			let state = data.state;
			update_schedule_display_state(automation, state);
		})
		.catch(function (e) {});
}

function update_schedule_display_state(automation, state) {
	switch (state) {
		case 'RUNNING':
			automation.classList.remove('starting');
			automation.classList.add('executing');
			// automation.find('.running_automation').removeClass('d-none');
			break;

		case 'IDDLE':
			automation.classList.remove('executing', 'starting');
			automation.querySelector('.btn_edit_remove, .iniciar').disabled = false;
			automation.querySelector('.cancel').disabled = true;
			clearInterval(all_intervals[automation.dataset.id]);
			break;

		default:
			break;
	}
}

const all_intervals = {};

$(document).ready(function () {
	$('#manage_appointments').on('show.bs.modal', (event) => fillModalWithInfos(event));

	$('#standard_solution_inner_content').on('click', '#btn_newconfig', function (e) {
		$('#modalExemplo form input[name=action_type]').val('new');
		resetAutomationModal();
		document.getElementById('modalExemplo').dataset.automation = e.target.dataset.automation;
		$('#modalExemplo form').attr('action', `/services/model/new`);
		if ($('#email-setado').val() != null) {
			let $this = $(this);
			addEmail($('#email-setado').val());
			toggleFileFormat($this, 'csv_radio');
			$('#csv_button').addClass('active');
		}
	});

	$('#standard_solution_inner_content').on('click', '.automation .btn_edit', function (e) {
		const allAdvanceButtons = Array.from(
			document.getElementById('modalExemplo').querySelectorAll('.btn-advance')
		);

		resetAutomationModal();
		document.getElementById('modalExemplo').dataset.automation = e.target.dataset.automation;
		allAdvanceButtons
			.filter((button) => button.classList.contains('credentials_advance') == false)
			.forEach((button) => (button.disabled = false));
		$('#modalExemplo form input[name=action_type]').val('edit');
		let $this = $(this);
		$('#modalExemplo .btn-advance.submit').html(translate['edit_model'][language]);
		let formElements = $('#modalExemplo form');
		formElements.attr('action', `/services/model/edit/${$this.data('id')}`);
		updateFormInfos(formElements, $this.closest('.automation'));
	});

	$('#modalExemplo').on('keyup', 'form input[name=name]', function (e) {
		canSubmit($('#modalExemplo form'));
	});

	$('#modalExemplo').on('click', '.modal-footer .btn-advance.submit', function (e) {
		e.preventDefault();
		$('#modalExemplo form').submit();
	});

	$('#modalExemplo').on('submit', 'form', function (e) {
		e.preventDefault();
		let formElements = $(this);
		submitAutomation(formElements);
	});

	//deleting
	$('#standard_solution_inner_content').on('click', '.automation .btn_remove', function (e) {
		let $this = $(this);
		$('#modaldelet .confirm_exclude').data('id', $this.data('id'));
		$('#modaldelet .content_delete .automation_name').html(
			`[ ${$this.closest('.automation').find('.box_header p').html()} ]`
		);
	});

	$('#modaldelet').on('click', '.confirm_exclude', async function (e) {
		const $this = $(this);
		const id = $this.data('id');
		if (typeof id == 'number') {
			$this.replaceWith(getLoadingDiv(true, ' small'));
			const fetchUrl = `/services/model/remove/${id}`;

			const settings = {
				method: 'DELETE',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify({}),
			};

			try {
				const response = await fetch(fetchUrl, settings);
				const convertedResponse = await response.json();

				$('#modaldelet .loading_div').replaceWith($this);

				if (response.status < 300) {
					Swal.fire(translate['success'][language], convertedResponse.msg, 'success');
					$(`.automation[data-id=${id}]`).remove();
				} else {
					Swal.fire('Oops..', convertedResponse.msg, 'error');
				}
			} catch (error) {
				Swal.fire(
					'Oops..',
					translate['unable_to_remove_execution_please_try_again'][language],
					'error'
				);
			} finally {
				$('#modaldelet').modal('hide');
			}
		} else {
			Swal.fire(
				'Oops..',
				'Atualize a página e tente novamente, a utilização informada não está de acordo com nosso sistema',
				'error'
			);
		}
	});

	//CANCEL
	$('#standard_solution_inner_content').on('click', '.automation .btn_cancel', function (e) {
		let $this = $(this);
		$('#modalcancel .confirm_cancel').data('id', $this.data('id'));
		$('#modalcancel .content_cancel .automation_name').html(
			`[ ${$this.closest('.automation').find('.box_header p').html()} ]`
		);
	});

	$('#modalcancel').on('click', '.confirm_cancel', function (e) {
		let $this = $(this);
		let id = $this.data('id');
		let automation = $(`.automation[data-id="${id}"]`);
		if (typeof id == 'number') {
			// let btn = $this;
			$this.replaceWith(getLoadingDiv(true, ' small'));
			let csrfmiddlewaretoken = getCSRFauth();
			$.post(
				`/services/automation/cancel/${id}`,
				{ csrfmiddlewaretoken: csrfmiddlewaretoken },
				function (data) {
					$('#modalcancel .loading_div').replaceWith($this);
					if (data.status == 200) {
						automation.removeClass('starting').removeClass('executing');
						automation.find('.running_automation').addClass('d-none');
						automation.find('.btn_edit_remove, .iniciar').prop('disabled', false);
						automation.find('.cancel').prop('disabled', true);
						Swal.fire(translate['success'][language], data.msg, 'success');
						$(`.automation[data-id=${id}]`);
						$('#modalcancel').modal('hide');
						updateScheduleState(automation[0]);
					} else {
						Swal.fire('Oops..', data.msg, 'error');
					}
				}
			).catch((err) => {
				$('#modalcancel .loading_div').replaceWith($this);
				Swal.fire('Oops..', 'Erro estranho ocorreu', 'error');
			});
		} else {
			Swal.fire(
				'Oops..',
				'Atualize a página e tente novamente, a utilização informada não está de acordo com nosso sistema',
				'error'
			);
		}
	});

	$('.allschedules').on('click', '.automation .cancel', function (e) {
		e.preventDefault();
	});

	const allModelsContainer = document.querySelector('.allschedules');
	allModelsContainer.addEventListener('click', delegateEvents);

	function delegateEvents(event) {
		const target = event.target;
		const isBtnToStartModel = target.closest('.iniciar');

		if (isBtnToStartModel) {
			startModel(event);
		}
	}

	async function startModel(event) {
		const targetButton = event.target;
		const serviceBox = targetButton.closest('.automation');
		const serviceId = serviceBox.getAttribute('data-id');
		const excludeModelBtn = serviceBox.querySelector('.btn_edit_remove');
		const cancelModelBtn = serviceBox.querySelector('.cancel');
		serviceBox.classList.add('starting');

		targetButton.disabled = true;
		excludeModelBtn.disabled = true;
		cancelModelBtn.disabled = false;

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
		};

		const response = await fetch(`/services/automation/start/${serviceId}`, settings);

		if (!response.ok) {
			Swal.fire({
				icon: 'error',
				title: 'Oops...',
				text: 'Erro ao iniciar a automação!',
				confirmButtonText: 'OK',
				confirmButtonColor: 'var(--dark-green)',
			}).then(() => {
				updateScheduleState(serviceBox);
				serviceBox.classList.remove('starting', 'executing');
				serviceBox.querySelector('.running_automation').classList.add('d-none');
				targetButton.disabled = false;
				excludeModelBtn.disabled = false;
				cancelModelBtn.disabled = true;
			});
		}
	}

	$('#csv_button').click(function () {
		let $this = $(this);
		if (!$this.hasClass('active')) {
			toggleFileFormat($this, 'csv_radio');
		} else {
			$this.removeClass('active');
		}
		checkIfUtilizationCanBeCreated();
	});

	$('#excel_button').click(function () {
		let $this = $(this);
		if (!$this.hasClass('active')) {
			toggleFileFormat($this, 'excel_radio');
		} else {
			$this.removeClass('active');
		}
		checkIfUtilizationCanBeCreated();
	});

	//ADDING MUTIPLE EMAILS
	$('#modalExemplo').on('click', '#add-mais', function (e) {
		const $this = $(this);
		const allEmailsToSendResults = $('#modalExemplo input[name=email_to_send_results]').val();
		const limit = 4;
		const emailsAreValid = validateEmail(allEmailsToSendResults);
		const emailsAreRepeated = isEmailAlreadyIncluded(allEmailsToSendResults);
		const errorTag = $this.closest('.forminput').find('.error');
		if (emailsAreValid && $('#all_emails .add-email').length < limit && !emailsAreRepeated) {
			$('#modalExemplo input[name=email_to_send_results]').val('');
			errorTag.html('');
			addEmail(allEmailsToSendResults, limit, true);
			checkIfUtilizationCanBeCreated();
		} else if (!emailsAreValid) {
			errorTag.html('Esse email não é válido');
			// Swal.fire('Oops..', 'Esse email não é válido', 'error');
		} else if (emailsAreRepeated) {
			Swal.fire('Oops..', 'Esse email já foi adicionado', 'error');
			errorTag.html('');
		} else {
			Swal.fire('Oops..', 'Limite de 4 emails por automação atingido', 'error');
			errorTag.html('');
		}
		canSubmit($('#modalExemplo form'));
	});

	$('#modalExemplo').on('click', '#all_emails .remove_email', function (e) {
		e.preventDefault();
		$(this).closest('.add-email').remove();
		toggleAddEmailBtn(4);
		canSubmit($('#modalExemplo form'));
		checkIfUtilizationCanBeCreated();
	});
});

function getAutomationType() {
	return document.getElementById('automation_type').value;
}

function addEmail(email_to_send_results, limit, isNew = false) {
	let conteudo;
	if (email_to_send_results.toLowerCase().includes('uipath') && !isNew) {
		const splittedEmailString = email_to_send_results.split('-');
		const email = splittedEmailString.shift();
		const token = splittedEmailString.join(',');

		conteudo = `<div class="color000000 add-email light-bold col-13 py-1 col d-flex justify-content-between m-1"><p class="limitoneline mb-0" data-token=${token}>${email}</p>`;
	} else {
		conteudo = `<div class="color000000 add-email light-bold col-13 py-1 col d-flex justify-content-between m-1"><p class="limitoneline mb-0">${email_to_send_results}</p> <span class="remove_email color656565 ml-1 c-pointer">X</span></div>`;
	}
	$('#all_emails').append(conteudo);
	toggleAddEmailBtn(limit);
}

function toggleAddEmailBtn(limit) {
	if ($('#all_emails .add-email').length < limit) {
		$('#add-mais').removeClass('disable-button');
	} else if ($('#all_emails .add-email').length == limit) {
		$('#add-mais').addClass('disable-button');
	}
}

//verificar se foi inserido o mesmo email
function isEmailAlreadyIncluded(email_to_send_results) {
	is_included = false;
	$('#all_emails .add-email p').map((index, email) => {
		if (email.textContent == email_to_send_results) {
			is_included = true;
		}
	});
	return is_included;
}

function getAllEmailsToSendResults(return_json = true) {
	let allemails_json = [];
	$('#all_emails .add-email p').map((index, email) => {
		if (email.textContent.toLowerCase().includes('uipath')) {
			allemails_json.push(`${email.textContent}-${email.dataset.token || 'no token'}`);
		} else {
			allemails_json.push(email.textContent);
		}
	});
	return return_json ? JSON.stringify(allemails_json) : allemails_json;
}

function isAllEmailsValid() {
	let all_emails = getAllEmailsToSendResults(false);
	let all_emails_valid = all_emails.length > 0;
	all_emails.forEach((item) => {
		const isUipathConnectionString = item.toLowerCase().includes('uipath');
		if (!isUipathConnectionString && !validateEmail(item)) {
			all_emails_valid = false;
		}
	});
	return all_emails_valid;
}

function fillAllEmails(allemails_json) {
	try {
		const allEmails = JSON.parse(allemails_json);
		allEmails.forEach((item) => {
			addEmail(item, 4);
		});
	} catch (e) {
		addEmail(allemails_json, 4);
	}
}

function toggleFileFormat($this, id_element) {
	$('#modalExemplo form .formato-group .btn.active').removeClass('active');
	$this.addClass('active');
	let radio_inputs = document.getElementsByName('file_format');
	for (var i = 0; i < radio_inputs.length; i++) {
		radio_inputs[i].checked = radio_inputs[i].id == id_element ? true : false;
	}
	canSubmit($('#modalExemplo form'));
}

$(document).ready(function () {
	$('#standard_solution_inner_content').on(
		'click',
		'.tab_header .single_tab_header',
		function (e) {
			let $this = $(this);
			if ($this.data('href') == 'my_services') {
				window.location = '/services';
			} else if (!$this.hasClass('active')) {
				let old_tab = $('.single_tab_header.active');
				old_tab.removeClass('active');
				$(`#${old_tab.data('href')}`).addClass('d-none');
				$this.addClass('active');
				let newTab = document.getElementById($this.data('href'));
				newTab.classList.remove('d-none');
				if (newTab.querySelector('.loading_div')) {
					const settings = {
						method: 'GET',
						headers: {
							'X-CSRFToken': getCookie('csrftoken'),
						},
					};
					fetch(`/services/singletab/${$this.data('href')}`, settings)
						.then(function (response) {
							// The API call was successful!
							return response.text();
						})
						.then(function (html) {
							// This is the HTML from our response as a text string
							newTab.querySelector('.py-5').innerHTML = html;
							loadSingleTabScripts($this.data('href'));
						})
						.catch(function (err) {
							// There was an error
							Swal.fire('Oops..', 'Error', 'warning');
						});
				}
			}
		}
	);
});

async function submitForm() {
	const form = document.querySelector('#modalExemplo form');
	const formElements = form.elements;
	const fetchUrl = form.getAttribute('action');
	const action = form.elements['action_type'].value;
	const settings = {
		method: 'POST',
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
		},
		body: getModelFormBodyParams(formElements, fetchUrl),
	};

	const response = await fetch(fetchUrl, settings);
	const convertedResponse = await response.json();

	if (response.status < 300) {
		Swal.fire(translate['success'][language], convertedResponse.msg, 'success');

		if (action === 'new') {
			const newModelElement = new DOMParser()
				.parseFromString(convertedResponse['model_component'], 'text/html')
				.body.querySelector('*:first-of-type');

			insertNewScheduleIntoDom(newModelElement);
		}
	} else {
		Swal.fire('Oops..', convertedResponse.msg, 'error');
	}

	resetModalFooter();

	if (action == 'edit' && response.status < 300) {
		updateAutomationInfos(convertedResponse.data);
	}

	resetAutomationModal();

	return response.ok;
}

function resetModalFooter() {
	const action = document.querySelector('#modalExemplo form input[name=action_type]')?.value;

	const confirmationButtonText =
		action === 'edit'
			? translate['edit_capital'][language]
			: translate['save_capital'][language];

	$('#modalExemplo .loading_div').replaceWith(
		`<button class="btn__purple py-2 px-3 gap-16 no-uppercase mr-3 btn-advance submit" type="submit">${confirmationButtonText}</button>`
	);
}

function validateEmail(email) {
	const re =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(String(email).toLowerCase());
}

function insertNewScheduleIntoDom(elementInStringFormat) {
	const allSchedulesContainer = document.querySelector('.allschedules');
	const listOfSchedules = Array.from(allSchedulesContainer.querySelectorAll('.automation'));

	if (listOfSchedules.length) {
		const firstScheduleOfList = listOfSchedules.at(0);
		const lastScheduleOfList = listOfSchedules.at(-1);
		const listIsFull = listOfSchedules.length >= 5;

		allSchedulesContainer.prepend(elementInStringFormat);

		if (listIsFull) lastScheduleOfList.remove();
	} else {
		allSchedulesContainer.prepend(elementInStringFormat);
	}
}

const fillModalWithInfos = (event) => {
	const modal = event.target;
	const targetButton = event.relatedTarget;
	const allCrons = Array.from(targetButton.querySelectorAll('.single_cron'));
	let allCronsExpression = '';
	let lastTemplateName = '';
	allCrons.forEach((singleCron) => {
		lastTemplateName = singleCron.dataset.templatename;
		allCronsExpression += newSingleCron(
			singleCron.value,
			singleCron.dataset.fullcrontext,
			singleCron.dataset.templateid,
			singleCron.dataset.cronexpression,
			singleCron.dataset.executiondate,
			singleCron.dataset.templatename
		);
	});
	modal.querySelector('.model_title').innerHTML = lastTemplateName;
	modal.querySelector('.cron_expressions_content').innerHTML = allCronsExpression;
	const allCronBoxesHeader = Array.from(
		document.querySelectorAll('.single_cron_box .single_cron_box_header')
	);
	allCronBoxesHeader.forEach((singleCronBoxHeader) => {
		singleCronBoxHeader.addEventListener('click', function (e) {
			const singleCronBox = e.currentTarget.closest('.single_cron_box');
			const arrow = singleCronBox.querySelector('.arrow');
			if (singleCronBox.classList.contains('active')) {
				singleCronBox.classList.remove('active');
				arrow.classList.remove('up');
				arrow.classList.add('down');
			} else {
				singleCronBox.classList.add('active');
				arrow.classList.remove('down');
				arrow.classList.add('up');
			}
		});
	});
};

const newSingleCron = (cronText, msg, templateId, cronExpression, executionDate, templateName) => {
	return `
		<div class="single_cron_box">
			<div class="single_cron_box_header d-flex justify-content-between align-items-center">
				<p class="mb-0"><img class="mr-2" src="/static/img/img_select_agendamento.png"/> ${cronText}</p>
				<i class="arrow down"></i>
			</div>
			<div class="single_cron_box_content px-4 py-3">
				<p>${msg}</p>
				<div class="d-flex justify-content-start gap-16">
					<button class="edit_appointment btn__basic py-1 px-2 d-flex justify-content-start gap-10" data-toggle="modal" data-target="#modalcreateappointment" data-id="${templateId}" data-cronexpression="${cronExpression}" data-executiondate="${executionDate}">
						<img src="/static/dashboard/img/edit.svg" alt="Icon Edit">
						${translate['edit'][language]}
					</button>
					<button class="remove_appointment btn__basic py-1 px-2 d-flex justify-content-start gap-10" data-toggle="modal" data-target="#modaldeleteappointment" data-id="${templateId}" data-name="${templateName}">
						<img src="/static/dashboard/img/delete_filled.svg" alt="Icon Exclude">
						${translate['exclude'][language]}
					</button>
				</div>
			</div>
		</div>
	`;
};

const updateTemplateCron = (automationElement, newName) => {
	const allCrons = Array.from(automationElement.querySelectorAll('.single_cron'));
	allCrons.forEach((singleCron) => {
		singleCron.dataset.templatename = newName;
	});
};
