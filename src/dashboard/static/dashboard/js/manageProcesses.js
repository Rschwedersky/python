/***************************************************** EXECUTABLE CODE */

$(document).ready(function () {
	//forcing loose focus on hide modal
	$('body').on('hidden.bs.modal', '.modal', function () {
		$('.btn').blur();
	});
});

/***************************************************** DECLARATIONS */

function validateInput(input, text_error) {
	let res = { error: false, val: input.val() };
	if (input.val().length < 1) {
		res.error = true;
		input.closest('.form_input').find('.text_error').html(text_error);
	} else {
		input.closest('.form_input').find('.text_error').html('');
	}
	return res;
}

function getRandomId() {
	return Math.floor(1000000000000000 + Math.random() * 9000000000000000)
		.toString(36)
		.substring(0, 10);
}

const updateJsAfterContentIsShown = () => {
	loadSubProcesses();
	runMultiStepJs();

	const form = document.querySelector('#process-modal form');
	form.addEventListener('submit', saveProcessEdit);
	form.addEventListener('change', checkCalculatorBtn);

	const allCurrencyInputs = form.querySelectorAll('.input__money');
	allCurrencyInputs.forEach((input) => input.addEventListener('keyup', autoFormatCurrencyInput));

	const openCalculatorBtn = document.getElementById('open-calculator');
	const exitCalculatorBtn = document.getElementById('back-calculator');
	const gridWrapper = document.getElementById('calculator-wrapper');
	const calculatorColumnInput = document.getElementById('number-of-columns-calculator');
	const calculatorInputsContainer = document.getElementById('calculator-input-container');
	const useCalculatorValueBtn = document.getElementById('use-calculator-value');
	const valuedToBeUsedInput = document.getElementById('calculator-total-value');

	openCalculatorBtn.addEventListener('click', openCalculator);

	exitCalculatorBtn.addEventListener('click', closeCalculator);

	calculatorInputsContainer.addEventListener('input', formatCalculatorInputs);

	gridWrapper.addEventListener('change', calculateAverageHourValue);

	calculatorColumnInput.addEventListener('change', resizeCalculatorColumns);

	useCalculatorValueBtn.addEventListener('click', useCalculatorValue);

	function openCalculator(event) {
		const { target } = event;
		const container = target.closest('.jsContainer');
		const calculatorContainer = container.nextElementSibling;
		const stepper = target.closest('.modal-dialog').querySelector('.jsStepper');

		container.classList.add('d-none');
		stepper.classList.add('d-none');
		calculatorContainer.classList.remove('d-none');
	}

	function closeCalculator(event) {
		const { target } = event;
		const container = target.closest('.jsContainer');
		const calculatorContainer = container.previousElementSibling;
		const stepper = target.closest('.modal-dialog').querySelector('.jsStepper');

		container.classList.add('d-none');
		stepper.classList.remove('d-none');
		calculatorContainer.classList.remove('d-none');
	}

	function checkCalculatorBtn(event) {
		const { target } = event;
		const quantityOfMonthlyTasksInput = document.getElementById('quantity-of-monthly-tasks');
		const minutesPerTaskInput = document.getElementById('processStep2AverageTimeSpent');
		const calculatorInputs = [quantityOfMonthlyTasksInput, minutesPerTaskInput];

		if (!calculatorInputs.includes(target)) return;

		if (calculatorInputs.every((input) => input.value.trim())) {
			openCalculatorBtn.disabled = false;
		} else {
			openCalculatorBtn.disabled = true;
		}
	}

	function resetCalculatorMonthlyValueInput() {
		valuedToBeUsedInput.value = '';
		useCalculatorValueBtn.disabled = true;
	}

	function formatCalculatorInputs(event) {
		const { target } = event;

		if (target.classList.contains('jsCurrencyInput')) {
			autoFormatCurrencyInput(event);
		} else if (target.classList.contains('jsPercentageInput')) {
			autoFormatPercentageInput(target);
		} else {
			return;
		}
	}

	function calculateAverageHourValue(event) {
		const wrapper = event.currentTarget;
		const children = Array.from(wrapper.children).slice(1);

		const { totalValue, totalDedication } = children.reduce(
			(prevInfo, currChild) => {
				const childrenInputs = Array.from(currChild.children);
				const thisQntOfCollaborators = Number(childrenInputs.at(0).value) || 0;
				const thisSalaryInString = childrenInputs.at(1).value.replace(/[^\d,.]/g, '');
				const thisSalary =
					thisSalaryInString.indexOf(',') < thisSalaryInString.indexOf('.')
						? Number(thisSalaryInString.replaceAll(',', ''))
						: Number(thisSalaryInString.replaceAll('.', '').replaceAll(',', '.'));
				const thisDedication =
					Number(childrenInputs.at(2).value.replace(/[^\d]/g, '')) / 100 || 0;

				const thisValue = thisQntOfCollaborators * thisSalary * thisDedication;

				return {
					totalValue: (prevInfo.totalValue += thisValue),
					totalDedication: (prevInfo.totalDedication += thisDedication),
				};
			},
			{
				totalValue: 0,
				totalDedication: 0,
			}
		);
		const monthlyTasks = Number(document.getElementById('quantity-of-monthly-tasks').value);

		const hoursInTask =
			Number(
				document.getElementById('processStep2AverageTimeSpent').value.replace(/[^\d]/g, '')
			) / 60;

		const monthlyHoursWorked = monthlyTasks * hoursInTask;

		const valueToBeUsed = ((totalValue * totalDedication) / monthlyHoursWorked) * 1.5;

		if (valueToBeUsed) {
			valuedToBeUsedInput.value = new Intl.NumberFormat(language, {
				style: 'currency',
				currency: 'BRL',
				minimumFractionDigits: 2,
			}).format(valueToBeUsed);
			useCalculatorValueBtn.disabled = false;
		}
	}

	function resizeCalculatorColumns(event) {
		const target = event.target;
		const value = Number(target.value);

		if (!value) return;

		const gridWrapper = target.closest('.jsContainer')?.querySelector('.jsGridWrapper');
		const currentCount = Number(gridWrapper.getAttribute('data-columns')) || 1;

		gridWrapper.style.gridTemplateColumns = `repeat(${value + 1 || 2}, 1fr)`;

		if (value == currentCount) {
			return;
		} else if (value < currentCount) {
			let counter = currentCount;
			while (value < counter) {
				const lastChild = Array.from(gridWrapper.children).at(-1);
				lastChild.remove();
				counter--;
			}
		} else {
			const lastChild = Array.from(gridWrapper.children).at(-1);
			const copy = lastChild.cloneNode(true);
			copy.querySelectorAll('input').forEach(
				(input) => (input.value = input.getAttribute('value'))
			);
			gridWrapper.append(copy);
			resetCalculatorMonthlyValueInput();
		}

		gridWrapper.setAttribute('data-columns', value);
	}

	function useCalculatorValue(event) {
		const { target } = event;
		const value = target.previousElementSibling?.value;

		if (!value) return;
		const averageHourInput = document.getElementById('process-average-hour-value');

		averageHourInput.value = value;
		exitCalculatorBtn.click();
	}

	const registeredProcessesArea = document.getElementById('processes_registered');

	const confirmationModalButton = document.querySelector('#confirmation-modal button.jsSubmit');
	registeredProcessesArea?.addEventListener('click', handleCrewPopupMenu);

	confirmationModalButton.addEventListener('click', deleteSubprocess);

	function handleCrewPopupMenu(event) {
		const targetMenu = event.target.closest('button');

		if (!targetMenu) return;

		if (!targetMenu.classList.contains('jsPopover')) return;

		const targetPopup = targetMenu.parentNode.querySelector('.crew__popup-menu-container');
		const allPopups = Array.from(document.getElementsByClassName('crew__popup-menu-container'));

		allPopups.forEach((popup) => popup.classList.remove('crew__popup-menu-container--show'));

		targetPopup.classList.toggle('crew__popup-menu-container--show');
	}

	const processName = document.getElementById('processStep1Nickname');
	processName.addEventListener('input', handleProcessName);
	function handleProcessName(e) {
		allowProcessModalNextStep1(e.currentTarget.value);
	}

	function allowProcessModalNextStep1(value) {
		document.querySelector('#step-1 .btn-advance').disabled = value.length < 3;
	}

	$('#process-modal').on('show.bs.modal', (event) => {
		fillProcessModalWithNecessaryInfo(event);
		document.querySelector('html').style.overflow = 'hidden';
	});
	$('.modal').on('hidden.bs.modal', () => (document.querySelector('html').style.overflow = ''));
	$('#confirmation-modal').on('show.bs.modal', (event) => {
		const button = event.relatedTarget;
		const modalButton = event.target.querySelector('button.jsSubmit');

		modalButton.setAttribute('data-process', button.getAttribute('data-id'));
	});

	$(function () {
		$('[data-toggle="tooltip"]').tooltip();
	});

	loadOpenDashboardBtn(document.querySelector('.open_dashboard'));
	function loadOpenDashboardBtn(openDashboardBtn) {
		openDashboardBtn?.addEventListener('click', handleClickGoToDashboard);
		function handleClickGoToDashboard() {
			const targetSingleMenu = document.querySelectorAll('#menu .single_menu')[0];
			const tab = document.getElementById(targetSingleMenu.dataset.idtab);
			if (tab) {
				openTab(targetSingleMenu, tab);
			}
		}
	}

	function setMinutesSuffix(event) {
		const input = event.currentTarget;
		const inputValue = input.value;
		const inputValueWithOnlyDigits = Number(inputValue.replace(/[^\d]/g, ''));

		input.value = `${inputValueWithOnlyDigits} ${
			translate[inputValueWithOnlyDigits == 1 ? 'minute' : 'minutes'][language]
		}`;
	}

	function setHoursSuffix(event) {
		const input = event.currentTarget;
		const inputValue = input.value;
		const inputValueWithOnlyDigits = Number(inputValue.replace(/[^\d]/g, ''));
		input.value = `${inputValueWithOnlyDigits} ${
			translate[inputValueWithOnlyDigits == 1 ? 'hour' : 'hours_capital'][language]
		}`;
	}

	function loadSubProcesses() {
		// subprocesses fake select
		const subProcessesFakeSelect = Array.from(
			document.querySelectorAll('#process-modal .fake_select')
		);
		subProcessesFakeSelect.forEach((fakeSelect) => {
			fakeSelect.addEventListener('click', handleSubProcessesSelectDropdownClick);
		});

		function handleSubProcessesSelectDropdownClick(event) {
			event.preventDefault();
			const target = event.currentTarget;
			const singleFilter = target.closest('.single_filter');
			if (!target.classList.contains('active')) {
				target.classList.add('active');
				singleFilter.classList.add('active');
			} else {
				target.classList.remove('active');
				singleFilter.classList.remove('active');
				addSubProcessesSelected(singleFilter);
			}
		}
	}

	function fillProcessModalWithNecessaryInfo(event) {
		const modal = event.target;
		const targetButton = event.relatedTarget;
		const subtitleText = modal.querySelector('.subtitle_modal');
		if (targetButton.value === 'new') {
			resetProcessModalConfig(targetButton);
			subtitleText.classList.add('d-none');
			modal.querySelector('.modal-header div strong').innerHTML =
				translate['register_process'][language];
			// get all subprocesses
		} else {
			restoreMultiStep();
			subtitleText.classList.remove('d-none');
			const table = targetButton.closest('table');
			const form = modal.querySelector('form');
			table.id = getRandomId();
			modal.dataset.row = table.id;
			form.dataset.process = targetButton.dataset.processid;

			// step1 infos
			modal.querySelector('.modal-header div strong').innerHTML =
				translate['edit_process'][language];
			const modalHeading = modal.querySelector('header h5');
			modalHeading.textContent = targetButton.dataset.name;

			allowProcessModalNextStep1(targetButton.dataset.name);
			const fillNicknameValue = getDesiredElementsAndDoMore(
				targetButton.dataset.name,
				'processStep1Nickname'
			);
			fillNicknameValue(fillInputValueIfItExists);

			const fillAreaValue = getDesiredElementsAndDoMore(
				targetButton.dataset.areaid,
				'processStep1Area'
			);
			fillAreaValue(fillInputValueIfItExists);
			const fillProjectCostValue = getDesiredElementsAndDoMore(
				targetButton.dataset.projectcost,
				'processStep1Cost'
			);
			fillProjectCostValue([fillInputValueIfItExists, autoFormatCurrencyInput]);
			// step1 infos

			// step2 infos
			setAppropriateSubprocesses(targetButton.closest('.table'));
			// step2 infos

			// step3 infos

			const fillQtyOfMensalTasks = getDesiredElementsAndDoMore(
				targetButton.getAttribute('data-monthlytasks'),
				'quantity-of-monthly-tasks'
			);
			fillQtyOfMensalTasks(fillInputValueIfItExists);

			const fillAverageTimeSpent = getDesiredElementsAndDoMore(
				targetButton.getAttribute('data-durationtime'),
				'processStep2AverageTimeSpent'
			);
			fillAverageTimeSpent(setAverageSpentTimeValue);

			const fillAverageHourValue = getDesiredElementsAndDoMore(
				targetButton.getAttribute('data-averagehourvalue'),
				'process-average-hour-value'
			);
			fillAverageHourValue([fillInputValueIfItExists, autoFormatCurrencyInput]);
			// step3 infos

			resetCalculator(targetButton);
		}

		//Higher order function

		function fillInputValueIfItExists(htmlElement, value) {
			const condition = Number.isNaN(Number(value)) ? value : Number(value);

			if (condition) {
				htmlElement.value = value;
			} else {
				htmlElement.value = '';
			}
		}

		function setAverageSpentTimeValue(htmlElement, value) {
			if (value) {
				htmlElement.value = `${Math.round(value)} ${
					translate[Math.round(value) == 1 ? 'minute' : 'minutes'][language]
				}`;
			}
		}
		function setHoursByDay(htmlElement, value) {
			if (value) {
				htmlElement.value = `${Math.round(value)} ${
					translate[Math.round(value) == 1 ? 'hour' : 'hours_capital'][language]
				}`;
			}
		}
	}

	function resetCalculator(targetButton) {
		if (
			Number(targetButton?.getAttribute('data-monthlytasks')) &&
			Number(targetButton?.getAttribute('data-durationtime'))
		) {
			openCalculatorBtn.disabled = false;
		} else {
			openCalculatorBtn.disabled = true;
		}

		exitCalculatorBtn.click();

		calculatorColumnInput.value = '1';
		calculatorColumnInput.dispatchEvent(new Event('change'));

		calculatorInputsContainer
			.querySelectorAll('input')
			.forEach((input) => (input.value = input.getAttribute('value')));
	}

	function getDesiredElementsAndDoMore(value, formElementId) {
		const htmlElement = form.elements[formElementId];

		// Returns a function with access to desired variables via closure
		return (callbacks) =>
			Array.isArray(callbacks)
				? callbacks.forEach((callback) => callback(htmlElement, value))
				: callbacks(htmlElement, value);
	}

	function setAppropriateSubprocesses(tableElement) {
		const singleFilter = document.querySelector('#step-2 .single_filter.subprocesses');

		const subProcessesNames = [];
		if (tableElement) {
			registeredSubprocesses = tableElement.querySelectorAll('.subprocesses_table tbody td');
			registeredSubprocesses.forEach((subprocess) => {
				subProcessesNames.push({
					name: subprocess.querySelector('.subprocess_name span').textContent.trim(),
					checked: true,
				});
			});
		}

		const notRegisteredSubprocesses = Array.from(
			document.querySelectorAll('#processes_not_registered .subprocesses_table tbody td')
		);
		notRegisteredSubprocesses.forEach((subprocess) => {
			subProcessesNames.push({
				name: subprocess.querySelector('.subprocess_name span').textContent.trim(),
				checked: false,
			});
		});

		const labelType = 'subprocesses';
		let allCheckBoxes = '';
		subProcessesNames.forEach((subprocess, index) => {
			allCheckBoxes += `
				<label for="${labelType}${index}" class="single_checkbox d-flex justify-content-start align-items-center mb-0">
					<input type="checkbox" id="${labelType}${index}" name="status" value="${subprocess.name}"${
				subprocess.checked ? ' checked' : ''
			}>
					<span class="checkmark mr-1"></span>
					<p class="f-size-12 color-muted limitoneline mb-0">${subprocess.name}</p>
				</label>
			`;
		});
		singleFilter.querySelector('.all_single_filters').innerHTML = allCheckBoxes;

		addSubProcessesSelected(singleFilter);
	}

	function autoFormatCurrencyInput(event) {
		const targetInput = event.target || event;
		const inputValue = targetInput.value;

		const valueWithOnlyDigits =
			event instanceof Event ? Number(inputValue.replace(/[^\d]/g, '')) : Number(inputValue);

		if (event instanceof Event) {
			targetInput.value = valueWithOnlyDigits
				? new Intl.NumberFormat(language, {
						style: 'currency',
						currency: 'BRL',
						minimumFractionDigits: 2,
				  }).format(parseFloat(valueWithOnlyDigits) / 100)
				: '';
		} else {
			targetInput.value = valueWithOnlyDigits
				? new Intl.NumberFormat(language, {
						style: 'currency',
						currency: 'BRL',
						minimumFractionDigits: 2,
				  }).format(parseFloat(valueWithOnlyDigits))
				: '';
		}
	}

	function autoFormatPercentageInput(event) {
		const targetInput = event.currentTarget || event;
		const inputValue = targetInput.value;
		const valueWithOnlyDigits = inputValue.replace(/[^\d,.]/g, '');
		targetInput.value = `${valueWithOnlyDigits || 0}%`;
	}

	function resetProcessModalConfig(targetButton) {
		const modal = document.querySelector('#process-modal');
		const form = modal.querySelector('form');
		const rowBeingEdited = document.getElementById(modal.dataset.row);
		if (rowBeingEdited) rowBeingEdited.id = '';
		modal.querySelector('.modal-title').innerHTML = '';

		setAppropriateSubprocesses();
		restoreMultiStep();
		form.reset();
		allowProcessModalNextStep1(document.querySelector('#step-1 #processStep1Nickname').value);
		resetCalculator(targetButton);
	}

	async function saveProcessEdit(event) {
		event.preventDefault();
		const form = event.currentTarget;
		const submitButton = form.querySelector('button[type="submit"]');

		const { date_from, date_to } = getActiveDates();
		replaceWith(submitButton, getLoadingDiv());
		const loading = form.querySelector('.loading_div');
		const {
			processId,
			processNickname,
			processArea,
			costOfRpaProject,
			quantityOfMonthlyTasks,
			averageHourValue,
			averageTimeSpent,
			subProcessesNames,
		} = getProcessNecessaryInfo(form);
		if (subProcessesNames.length && processNickname.length) {
			const settings = {
				method: 'POST',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
				},
				body: JSON.stringify({
					process_name: processNickname,
					area: processArea,
					project_cost: costOfRpaProject,
					quantity_of_monthly_tasks: quantityOfMonthlyTasks,
					average_time_spent: averageTimeSpent,
					average_hour_value: averageHourValue,
					subprocesses: subProcessesNames,
					date_from,
					date_to,
				}),
			};
			const response = await fetch(`/post/process/${processId}`, settings);
			const convertedResponse = await response.text();
			let feedbackModal = 'negative_modal';
			let feedbackTitle =
				translate['it_was_not_possible_to_register_your_process_try_again'][language];
			if (response.ok == true) {
				if (!processId) {
					const processesRegistered = document.querySelector('#processes_registered');
					const emptyState = processesRegistered.querySelector('.empty_data');
					const emptyStateIsShowing = !emptyState.classList.contains('d-none');

					const parser = new DOMParser();
					const htmlDoc = parser.parseFromString(convertedResponse, 'text/html');
					const tableHtml = htmlDoc.querySelector('table');

					if (emptyStateIsShowing) {
						emptyState.classList.add('d-none');

						processesRegistered.prepend(tableHtml);
						const roiTab = document.getElementById('roi_tab');
						roiTab.classList.remove('jsNotAllowed');
					} else {
						processesRegistered.append(tableHtml);
					}
					feedbackTitle = translate['process_registered_successfully'][language];
				} else {
					replaceUpdatedProcessRow(convertedResponse);
					feedbackTitle = translate['process_edited_successfully'][language];
				}
				updateNotRegisteredSubProcessesTable(subProcessesNames);
				feedbackModal = 'positive_modal';
				replaceWith(loading, submitButton.outerHTML);
				$('#process-modal').modal('hide');
				getNewDashboardJson();
				showFeedbackModal(feedbackModal, feedbackTitle);
				makeNonActiveTabsRefreshable();
			}
		} else {
			replaceWith(loading, submitButton.outerHTML);
			if (!processNickname.length) {
				Swal.fire(
					'Oops..',
					translate['necessary_define_process_name'][language],
					'warning'
				);
			} else {
				Swal.fire('Oops..', translate['no_subprocess_registered'][language], 'warning');
			}
		}
		function updateNotRegisteredSubProcessesTable(subProcessesArray) {
			const divNotRegisteredSubprocesses = document.querySelector(
				'#processes_not_registered'
			);
			const notRegisteredSubprocesses = Array.from(
				divNotRegisteredSubprocesses.querySelectorAll('.subprocesses_table tbody td')
			);
			notRegisteredSubprocesses.forEach((subprocess) => {
				const name = subprocess.querySelector('.subprocess_name span').textContent.trim();
				if (subProcessesArray.indexOf(name) !== -1) {
					subprocess.closest('tr').remove();
				}
			});

			const remainingNotRegisteredSubProcesses = Array.from(
				document.querySelectorAll('#processes_not_registered .subprocesses_table tbody td')
			);
			if (!remainingNotRegisteredSubProcesses.length) {
				const emptyData = addSubProcessesNotRegisteredEmptyData();
				const notRegisteredTable = divNotRegisteredSubprocesses.querySelector('table');

				notRegisteredTable.classList.add('d-none');
				divNotRegisteredSubprocesses.append(emptyData);

				document.querySelector('.btn__new-process').disabled = true;
				loadOpenDashboardBtn(document.querySelector('.open_dashboard'));
			}
		}
	}

	function showFeedbackModal(feedbackModalString, feedbackTitle) {
		const feedbackModal = $(`#${feedbackModalString}`);
		feedbackModal.find('.modal-header h5').html(feedbackTitle);
		feedbackModal.modal('show');
		setTimeout(() => {
			feedbackModal.modal('hide');
		}, 1500);
	}

	function getProcessNecessaryInfo(form) {
		const processId = Number(form.dataset.process) || 0;
		const processNickname = form.elements.processStep1Nickname.value;
		const processArea = Number(form.elements.processStep1Area.value);
		const costOfRpaProject = fromCurrencyToNumber(form.elements.processStep1Cost.value);
		const quantityOfMonthlyTasks = Number(
			form.elements.quantityOfMonthlyTasks.value.replace(/[^\d]/g, '')
		);
		const averageTimeSpent = Number(
			form.elements.processStep2AverageTimeSpent.value.replace(/[^\d]/g, '')
		);

		const averageHourValue = cleanDecimalNumber(form.elements.averageHourValue.value);

		const subProcessesInput = Array.from(
			form.querySelectorAll('.single_filter.subprocesses label input[type=checkbox]:checked')
		);
		const subProcessesNames = [];
		subProcessesInput.forEach((singleSubProcess) => {
			subProcessesNames.push(singleSubProcess.value);
		});

		return {
			processId,
			processNickname,
			processArea,
			costOfRpaProject,
			quantityOfMonthlyTasks,
			averageTimeSpent,
			averageHourValue,
			subProcessesNames,
		};
	}

	function replaceUpdatedProcessRow(data) {
		const targetRow = document.getElementById(
			document.getElementById('process-modal').dataset.row
		);
		if (targetRow) {
			const oldSubProcesses = Array.from(
				targetRow.querySelectorAll('.subprocesses_table tbody tr')
			);
			let oldSubProcessesNames = {};
			oldSubProcesses.forEach((subProcessLine) => {
				oldSubProcessesNames[
					subProcessLine.querySelector('.subprocess_name span').innerHTML.trim()
				] = subProcessLine;
			});
			targetRow.innerHTML = data;

			const newSubProcesses = Array.from(
				targetRow.querySelectorAll('.subprocesses_table tbody tr')
			);
			newSubProcesses.forEach((subProcessLine) => {
				const name = subProcessLine.querySelector('.subprocess_name span').innerHTML.trim();
				if (oldSubProcessesNames[name]) {
					delete oldSubProcessesNames[name];
				}
			});
			if (Object.keys(oldSubProcessesNames).length) {
				const subProcessesNotRegistered = document.querySelector(
					'#processes_not_registered'
				);
				if (subProcessesNotRegistered.querySelector('.empty_data')) {
					subProcessesNotRegistered.innerHTML =
						targetRow.querySelector('.subprocesses_table').outerHTML;
					subProcessesNotRegistered.querySelector('.subprocesses_table tbody').innerHTML =
						'';
					document.querySelector('.btn__new-process').disabled = false;
				}
				Object.keys(oldSubProcessesNames).forEach((name) => {
					subProcessesNotRegistered
						.querySelector('table tbody')
						.insertAdjacentHTML('beforeend', oldSubProcessesNames[name].outerHTML);
				});
			}
		}
	}

	function addSubProcessesNotRegisteredEmptyData() {
		const string = `
			<section class="empty_data d-flex">
				<div class="w-100 h-100 d-flex flex-column justify-content-center align-items-between m-5 py-5 backgroundf7f7f7 text-center">
					<div>
						<strong>${translate['all_sub_processes_were_registered'][language]}.</strong>
						<p>${translate['now_your_dashboard_will_bring'][language]}.</p>
						<button type="button" value="new" class="open_dashboard btn btn_smarthis mt-0">${translate['go_to_dashboard'][language]}</button>
					</div>
				</div>
			</section>
		`;
		const parser = new DOMParser();
		const htmlDoc = parser.parseFromString(string, 'text/html');
		const emptyDataEl = htmlDoc.querySelector('.empty_data');
		return emptyDataEl;
	}

	async function deleteSubprocess(event) {
		const button = event.target;
		const processId = button?.getAttribute('data-process');

		if (!processId) return;

		const settings = {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
		};

		const response = await fetch(`/process/${processId}`, settings);

		const alertEl = document.createElement('span');

		if (response.ok) {
			alertEl.textContent = translate['process_deleted_successfully'][language];
			fireBootstrapAlert(alertEl);

			updateUiAfterProcessDeletion(processId);
		} else {
			alertEl.textContent = translate['error_deleting_process'][language];
			fireBootstrapAlert(alertEl, 'danger');
		}

		function fireBootstrapAlert(children, bsClass = 'success') {
			if (!children) return;

			const alertElement = document.createElement('div');
			const alertId = `alert-${getRandomId()}`;

			styleAlert();

			alertElement.setAttribute('id', alertId);
			alertElement.setAttribute('role', 'alert');
			alertElement.prepend(children);

			document.body.prepend(alertElement);

			setTimeout(() => alertElement.remove(), 2500);

			function styleAlert() {
				alertElement.classList.add('alert', `alert-${bsClass}`, 'position-absolute');
				alertElement.style.top = '16rem';
				alertElement.style.left = '35%';
				alertElement.style.width = '22rem';
				alertElement.style.zIndex = '1000';
			}
		}
	}

	function updateUiAfterProcessDeletion(processId) {
		const table = document
			.querySelector(`[data-id="${processId}"]`)
			?.closest('table.process_table');
		const subProcessTableRows = table.querySelectorAll('table.subprocesses_table tbody tr');
		const isLastTable =
			Array.from(registeredProcessesArea.children).filter((el) => el.tagName === 'TABLE')
				.length === 1;

		table.remove();

		if (isLastTable) {
			// Show empty state
			registeredProcessesArea.querySelector('section').classList.remove('d-none');
			const roiTab = document.getElementById('roi_tab');
			roiTab.classList.add('jsNotAllowed');
		}

		const notRegisteredTable = document.querySelector('#processes_not_registered table');
		const notRegisteredTableBody = notRegisteredTable.querySelector('tbody');

		subProcessTableRows.forEach((row) => {
			notRegisteredTableBody.append(row);
		});

		if (notRegisteredTable.classList.contains('d-none')) {
			const emptyState = notRegisteredTable.nextElementSibling;

			notRegisteredTable.classList.remove('d-none');
			emptyState.classList.replace('d-flex', 'd-none');
			document.querySelector('.btn__new-process').disabled = false;
		}

		makeNonActiveTabsRefreshable();
	}

	function fromCurrencyToNumber(currency) {
		if (currency.replaceAll(' ', '')) {
			return Number(
				currency
					.replace(/[^\d.,]/g, '')
					.replace(/,/g, '.')
					.replace(/[.](?=.*[.])/g, '')
			);
		} else {
			return 0;
		}
	}
};

function addSubProcessesSelected(singleFilter) {
	let finalHTMLSelection = '';
	const selectedSubProcesses = Array.from(
		singleFilter.querySelectorAll('input[type=checkbox]:checked')
	);
	selectedSubProcesses.forEach((checkbox, index) => {
		if (checkbox.value !== translate['all_male'][language]) {
			finalHTMLSelection += getSubprocessHtml(index, checkbox.value);
		}
	});
	document.querySelector('.subprocesses_selected').innerHTML = finalHTMLSelection;
	updateResumeChoicesText(singleFilter, selectedSubProcesses.length);
	loadRemoveSubProcessClick();
}

function getSubprocessHtml(index, subProcess) {
	const divClass = index % 2 === 0 ? 'even' : 'odd';
	return `
		<div class="box_subprocess d-flex justify-content-between align-items-center p-2 f-size-14 ${divClass}">
			<span class="subprocess_name">${subProcess}</span>
			<span class="remove_subprocess">&#215;</span>
		</div>
	`;
}

function loadRemoveSubProcessClick() {
	const allRemoveSubprocess = document.querySelectorAll('#process-modal .remove_subprocess');
	allRemoveSubprocess.forEach((removeSubProcess) => {
		removeSubProcess.addEventListener('click', handleRemoveSubProcess);
	});

	function handleRemoveSubProcess(e) {
		const boxSubProcess = e.currentTarget.closest('.box_subprocess');
		const subProcessName = boxSubProcess.querySelector('.subprocess_name').innerHTML;
		const checkbox = document.querySelector(`#process-modal input[value="${subProcessName}"]`);
		if (checkbox) {
			checkbox.checked = false;
			boxSubProcess.remove();
			const singleFilter = document.querySelector('#process-modal #step-2 .single_filter');
			const allCheckboxes = Array.from(
				singleFilter.querySelectorAll('input[type=checkbox]:checked')
			);
			updateResumeChoicesText(singleFilter, allCheckboxes.length);
		}
	}
}

function updateResumeChoicesText(singleFilter, qnt) {
	const resumeChoices = singleFilter.querySelector('.resume_choices_text');
	if (qnt > 0) {
		const selectedText = qnt === 1 ? 'sub_process_selected' : 'sub_processes_selected';
		resumeChoices.innerHTML = `${qnt} ${translate[selectedText][language]}`;
	} else {
		resumeChoices.innerHTML = translate['select'][language];
	}
	document.querySelector('#step-2 .btn-advance').disabled = qnt == 0;
}

function cleanDecimalNumber(number) {
	return Number(
		number
			.replaceAll('.', '')
			.replaceAll(',', '.')
			.replace(/[^\d.]/g, '')
	);
}
