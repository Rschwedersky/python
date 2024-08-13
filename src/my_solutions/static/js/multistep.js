document.addEventListener('DOMContentLoaded', runMultiStepJs);

function runMultiStepJs() {
	const allSteps = document.querySelectorAll('.setup-content');
	const modal =
		document.getElementById('modalExemplo') || document.getElementById('process-modal');
	const automationNameInput = document.getElementById('name-automation-input');
	const credentialsInput = Array.from(document.getElementsByClassName('form-credential'));
	const dateFrom = document.querySelector('.uploader-inner .from_date');
	const dateTo = document.querySelector('.uploader-inner .to_date');

	modal?.addEventListener('click', handleEventDelegation);
	automationNameInput?.addEventListener('input', updateAdvanceButtonState);
	credentialsInput?.forEach((input) =>
		input.addEventListener('input', handleCredentialsValidation)
	);

	dateFrom?.addEventListener('change', handleFilterNotesValidation);
	dateTo?.addEventListener('change', handleFilterNotesValidation);

	init();

	function init() {
		const firstStep = document.querySelector('.setup-panel .stepper-item.active');
		if (firstStep) {
			const firstContent = document.querySelector(`.setup-content${firstStep.dataset.href}`);
			firstContent.style.display = '';
		}

		allSteps.forEach((step) => (step.style.display = 'none'));
	}

	function handleEventDelegation(event) {
		if (
			event.target.classList.contains('nextBtn') ||
			event.target.closest('button')?.classList.contains('nextBtn')
		) {
			handleModalAdvance();
		} else if (event.target.classList.contains('prevBtn')) {
			handleModalReturn();
		}
	}

	function updateAdvanceButtonState(event) {
		const activeNav = document.querySelector('.setup-panel .active');
		const activePage = document.querySelector(`.setup-content${activeNav.dataset.href}`);
		let button = activePage.querySelector('.nextBtn');

		if (activeNav.dataset.href == '#step-1') {
			button.disabled = Boolean(automationNameInput.value) ? false : true;
		}
	}

	function handleModalAdvance() {
		const wrapper = document.querySelector('.setup-panel');
		const activeNav = wrapper.querySelector('.active');
		const activePage = document.querySelector(`.setup-content${activeNav.dataset.href}`);
		const nextNav = activeNav.nextElementSibling;
		const nextPage = document.querySelector(`.setup-content${nextNav.dataset.href}`);
		let error = 0;

		if (Boolean(nextPage.querySelector('#all_emails'))) {
			const emailsContainer = nextPage.querySelector('#all_emails');
			const excelButton = nextPage.querySelector('#excel_button');
			const csvButton = nextPage.querySelector('#csv_button');
			const saveButton = nextPage.querySelector('button.submit');

			const isFormatChecked =
				excelButton.classList.contains('active') || csvButton.classList.contains('active')
					? true
					: false;
			if (emailsContainer.children.length > 0 && isFormatChecked) {
				saveButton.disabled = false;
			} else {
				saveButton.disabled = true;
			}
		}

		/* CHECKING IF ALL INPUTS AND TEXTAREA IN THE CURRENT PAGE ARE FILLED. IF NOT : ADD ERROR CLASS ON INPUT AND INCREMENT ERROR COUNTER */

		if (activeNav.dataset.href == '#step-2' && activePage.querySelector('.file-container')) {
			const fileIsValid = activePage.querySelector('input[name=file-input]').files.length > 0;
			if (
				!fileIsValid &&
				document.querySelector('#modalExemplo form input[name=action_type]').value !==
					'edit'
			) {
				error++;
			}
		}

		/* IF ERROR COUNTER == 0 (ie. NENHUM ERRO ENCONTRADO)
                => PROSSEGUIR PARA A PRÓXIMA ETAPA
        */
		if (error == 0) {
			activePage.style.display = 'none';
			nextPage.style.display = '';

			activeNav.classList.add('completed');
			activeNav.classList.remove('active');
			nextNav.classList.add('active');
		}
	}

	function handleModalReturn() {
		const wrapper = document.querySelector('.setup-panel');
		const activeNav = wrapper.querySelector('.active');
		const activePage = document.querySelector(`.setup-content${activeNav.dataset.href}`);
		const prevNav = activeNav.previousElementSibling;
		const prevPage = document.querySelector(`.setup-content${prevNav.dataset.href}`);

		activePage.style.display = 'none';
		prevPage.style.display = '';

		prevNav.classList.remove('completed');
		prevNav.classList.add('active');
		activeNav.classList.remove('active');
	}

	function handleCredentialsValidation(event) {
		const advanceButton = event.target
			.closest('.setup-content')
			.querySelector('button.nextBtn');
		let canAdvance = true;
		credentialsInput.forEach((input) => {
			if (Boolean(input.value) == false || input.value.length <= 2) {
				canAdvance = false;
			}
		});

		advanceButton.disabled = !canAdvance;
	}

	function handleFilterNotesValidation(event) {
		let dateTarget = event.target;
		let isvalid_date = new Date(dateTarget.value);
		let final = { date_to: '', date_from: '' };

		let canAdvance = true;
		const advanceButton = dateTarget.closest('.setup-content').querySelector('button.nextBtn');

		if (dateTarget.classList.contains('to_date')) {
			let date_from = dateTarget.closest('.uploader-inner').querySelector('.from_date').value;
			final['date_from'] = date_from;
			let old_datefrom = new Date(date_from);
			if (old_datefrom.getTime() - isvalid_date.getTime() > 0) {
				Swal.fire(
					'Oops..',
					translate['the_end_date_needs_to_be_grater_than_start_date'][language],
					'warning'
				);
				let oneMonth = new Date(date_from);
				oneMonth.setDate(oneMonth.getDate() + 30);
				let day =
					oneMonth.getDate().length == 1 ? `0${oneMonth.getDate()}` : oneMonth.getDate();
				let month =
					oneMonth.getMonth().length + 1 == 1
						? `0${oneMonth.getMonth() + 1}`
						: oneMonth.getMonth() + 1;
				final['date_to'] = `${oneMonth.getFullYear()}-${month}-${day}`;
				dateTarget
					.closest('.uploader-inner')
					.querySelector(
						'.from_date'
					).value = `${oneMonth.getFullYear()}-${month}-${day}`;
			} else {
				final['date_to'] = dateTarget.value;
			}
		} else {
			let date_to = dateTarget.closest('.uploader-inner').querySelector('.to_date').value;
			final['date_to'] = date_to;
			let old_dateto = new Date(date_to);
			if (isvalid_date.getTime() - old_dateto.getTime() > 0) {
				Swal.fire(
					'Oops..',
					translate['the_start_date_needs_to_be_less_than_end_date'][language],
					'warning'
				);
				let oneMonth = new Date(date_to);
				oneMonth.setDate(oneMonth.getDate() - 30);
				let day =
					oneMonth.getDate().length == 1 ? `0${oneMonth.getDate()}` : oneMonth.getDate();
				let month =
					oneMonth.getMonth().length + 1 == 1
						? `0${oneMonth.getMonth() + 1}`
						: oneMonth.getMonth() + 1;
				final['date_from'] = `${oneMonth.getFullYear()}-${month}-${day}`;

				dateTarget
					.closest('.uploader-inner')
					.querySelector('.to_date').value = `${oneMonth.getFullYear()}-${month}-${day}`;
			} else {
				final['date_from'] = dateTarget.value;
			}
		}

		document.getElementById('periodo').value = `${final['date_from']}|${final['date_to']}`;

		advanceButton.disabled = !canAdvance;
	}
}

function getCurrentPageId() {
	const allSteps = Array.from(document.getElementsByClassName('setup-content'));
	const [currentStep] = allSteps.filter((step) => step.style.display != 'none');
	return currentStep.id;
}

function resetAutomationModal() {
	const modal = document.getElementById('modalExemplo');
	const allForms = Array.from(modal.querySelectorAll('form'));
	const allEmails = modal.querySelector('#all_emails');
	const excelButton = modal.querySelector('#excel_button');
	const csvButton = modal.querySelector('#csv_button');
	const allAdvanceButtons = Array.from(
		document.getElementById('modalExemplo').querySelectorAll('.btn-advance')
	);
	const submitButton = modal.querySelector('.btn-advance.submit');

	$('#modalExemplo').modal('hide');
	restoreMultiStep();
	allAdvanceButtons.forEach((button) => (button.disabled = true));
	allForms.forEach((form) => form.reset());
	allEmails.innerHTML = '';
	excelButton.classList.remove('active');
	csvButton.classList.remove('active');
	submitButton.textContent = translate['save_model'][language];
}

function restoreMultiStep() {
	const stepperContainer = document.querySelector('.setup-panel');
	const allNavSteps = Array.from(document.getElementsByClassName('stepper-item'));
	const firstNavStep = stepperContainer.querySelector('[data-href="#step-1"]');
	const allContentSteps = document.querySelectorAll('.setup-content');
	const firstContent = document.querySelector(`.setup-content${firstNavStep.dataset.href}`);

	allNavSteps.forEach((step) => step.classList.remove('completed', 'active'));
	firstNavStep.classList.add('active');

	allContentSteps.forEach((step) => {
		step.style.display = 'none';

		if (step.querySelector('.file-container')) {
			step.querySelector('.file-container').classList.remove('with-file');
		}
	});
	firstContent.style.display = '';
}

function checkIfUtilizationCanBeCreated() {
	const modal = document.getElementById('modalExemplo');
	const formatContainer = modal.querySelector('.excelorcsv');
	const emailsContainer = modal.querySelector('#all_emails');
	const submitButton = emailsContainer.closest('.setup-content').querySelector('.submit');

	let isFormatSelected = Boolean(formatContainer.querySelector('.active'));
	let isThereAnyEmail = emailsContainer.children.length > 0;

	if (isFormatSelected && isThereAnyEmail) {
		submitButton.disabled = false;
	} else {
		submitButton.disabled = true;
	}
}

function getDateFormat(dateString, needReverse = false) {
	let dateSplitted = dateString.split('/');
	let day = dateSplitted[0];
	let month = dateSplitted[1];
	let year = dateSplitted[2];
	if (dateSplitted.length < 2) {
		dateSplitted = dateString.split('-');
		day = dateSplitted[0];
		month = dateSplitted[1];
		year = dateSplitted[2];
	}

	return !needReverse ? `${year}-${month}-${day}` : `${day}-${month}-${year}`;
}
