document.addEventListener('DOMContentLoaded', () => {
	const allPlansPeriodButtons = Array.from(
		document.getElementsByClassName('trial-plan-choice-buttons')
	);
	const allGroupedButtons = document.querySelectorAll('.free-trial__end--plans .button__group');
	const allArithmeticButtons = document.querySelectorAll(
		'.free-trial__end--plans .arithmetic-button'
	);
	const allServicesCheckboxes = document.querySelectorAll(
		'.free-trial__end--plans .single_checkbox'
	);
	const choosePeriodButtons = document.querySelectorAll(
		'.free-trial__end--plans .custom__radio--container input'
	);
	const queriesLimitSwitch = document.querySelector(
		'.free-trial__end--plans .custom__switch input'
	);
	const cnpjInput = document.getElementById('trialCnpj');

	allPlansPeriodButtons.forEach((button) => button.addEventListener('click', togglePlanPeriod));

	allGroupedButtons.forEach((button) => button.addEventListener('click', toggleQueries));

	allArithmeticButtons.forEach((button) =>
		button.addEventListener('click', handleLicenseManipulation)
	);

	allServicesCheckboxes.forEach((checkbox) =>
		checkbox.addEventListener('click', handleServiceClick)
	);

	choosePeriodButtons.forEach((button) => button.addEventListener('click', changePaymentPeriod));

	queriesLimitSwitch?.addEventListener('click', handleQueriesLimit);

	cnpjInput?.addEventListener('input', setSubmitButtonClickable);

	function togglePlanPeriod(event) {
		const targetButton = event.target;
		const otherButton = targetButton.nextElementSibling || targetButton.previousElementSibling;
		const targetPeriod = targetButton.dataset.period;
		const allPlanBoxes = Array.from(document.getElementsByClassName('single__plan-box'));
		const clickedTheSameButton = targetButton.classList.contains('active');

		targetButton.classList.add('active');
		otherButton.classList.remove('active');

		if (!clickedTheSameButton) {
			allPlanBoxes
				.filter((box) => box.querySelector('.single__plan-box--price') !== null)
				.forEach((box) => updateBoxes(box));
		}

		function updateBoxes(box) {
			const boxLink = box.querySelector('a');
			const pricePlaceholder = box.querySelector('.single__plan-box--price');
			const temp = pricePlaceholder.querySelector('strong').textContent;
			const planBox = pricePlaceholder.closest('.single__plan-box');
			let desiredHref;

			if (targetPeriod == 'month') {
				desiredHref = boxLink.href.replace('yearly', 'monthly');

				pricePlaceholder.innerHTML = `R$ <strong class="f-size-26">${pricePlaceholder.dataset.price}</strong><span class='secondary__color'>/${translate['month'][language]}</span>`;
			} else {
				const anualPriceWithoutDiscount = Number(temp.replace(',', '.')) * 12;
				desiredHref = boxLink.href.replace('monthly', 'yearly');

				pricePlaceholder.innerHTML = `
                <span class='d-block'>${translate['from_de'][language]}
                    <span class='color-muted--lightest text-decoration-through'>${anualPriceWithoutDiscount}</span>
                    ${translate['for'][language]}:
                </span>
                1x R$ <strong class="f-size-26">${pricePlaceholder.dataset.price}</strong><span class='secondary__color'>/${translate['year'][language]}</span>`;
			}

			boxLink.href = desiredHref;
			pricePlaceholder.classList.toggle('color-muted--light');
			planBox.classList.toggle('anual');
			pricePlaceholder.dataset.price = temp;
		}
	}

	function toggleQueries(event) {
		const targetButton = event.target;

		allGroupedButtons.forEach((button) => button.classList.remove('active'));
		targetButton.classList.add('active');
	}

	function handleLicenseManipulation(event) {
		const targetButton = event.target;
		if (targetButton.classList.contains('disabled')) {
			return;
		}
		const operation = targetButton.dataset.operation;
		const numberOfLicensesPlaceholder =
			targetButton.nextElementSibling?.querySelector('.licenses-to-add') ||
			targetButton.previousElementSibling?.querySelector('.licenses-to-add');
		let subtractButton;

		const numberOfLicensesInput = document.getElementById('business-number-of-licenses');

		let currentNumberOfLicenses = Number(numberOfLicensesInput.value);
		const numberOfChosenServices = targetButton
			.closest('.free-trial__end--plans')
			.querySelectorAll('input[type="checkbox"]:checked').length;

		if (operation == 'decrease' && currentNumberOfLicenses > 4) {
			subtractButton = targetButton;
			addButton = targetButton.nextElementSibling.nextElementSibling;
			currentNumberOfLicenses--;
		} else if (operation == 'increase') {
			addButton = targetButton;
			subtractButton = targetButton.previousElementSibling.previousElementSibling;
			currentNumberOfLicenses++;
		} else {
			return;
		}
		updateButtonsState();
		updateProgressBar();

		numberOfLicensesInput.value = currentNumberOfLicenses;
		numberOfLicensesPlaceholder.textContent = currentNumberOfLicenses;
		numberOfLicensesPlaceholder.nextSibling.textContent = translate['licenses'][language];

		function updateButtonsState() {
			if (currentNumberOfLicenses > numberOfChosenServices && currentNumberOfLicenses > 4) {
				temp = subtractButton.src.replace('remove-blue-disabled', 'remove-blue');
				subtractButton.src = temp;
				subtractButton.classList.add('opacity-hover', 'c-pointer');
				subtractButton.classList.remove('disabled');
				subtractButton.disabled = false;
			} else {
				temp = subtractButton.src.replace('remove-blue', 'remove-blue-disabled');
				subtractButton.src = temp;
				subtractButton.classList.remove('opacity-hover', 'c-pointer');
				subtractButton.classList.add('disabled');
				subtractButton.disabled = true;
			}
		}

		function updateProgressBar() {
			const progressBar = targetButton
				.closest('.free-trial__end--plans')
				.querySelector('progress');
			const progressSubtitle = progressBar.nextElementSibling;
			const progressSubtitleUsedLicenses = progressSubtitle.querySelector('#used-licenses');
			const progressSubtitleLicensesLimit = progressSubtitle.querySelector('#licenses-limit');

			progressSubtitleUsedLicenses.textContent = numberOfChosenServices;
			progressSubtitleLicensesLimit.textContent = currentNumberOfLicenses;
			progressBar.max = currentNumberOfLicenses;
		}
	}

	function handleServiceClick(event) {
		event.preventDefault();

		const targetCheckbox = event.currentTarget;
		const input = targetCheckbox.querySelector('input');
		const inputIsChecked = input.checked;
		const plan = getPlan();

		const progressBar = targetCheckbox
			.closest('.free-trial__end--plans')
			.querySelector('progress');
		const progressSubtitle = progressBar.nextElementSibling;
		const progressSubtitleUsedLicenses = progressSubtitle.querySelector('#used-licenses');
		let numberOfUsedLicenses = getNumberOfUsedLicenses();

		const userIsInsideLimit = checkLicensesLimit(true);

		if (userIsInsideLimit || inputIsChecked) {
			checkInputAndUpdateProgressBar();
		} else {
			Swal.fire('Oops..', translate['you_have_reached_licenses_limit'][language], 'error');
		}

		function checkInputAndUpdateProgressBar() {
			if (inputIsChecked) {
				input.checked = false;
				progressBar.value -= 1;
				progressSubtitleUsedLicenses.textContent = numberOfUsedLicenses - 1;

				if (plan == 'business') {
					updatesLicenseIncrementer('decrease');
				}
			} else {
				input.checked = true;
				progressBar.value += 1;
				progressSubtitleUsedLicenses.textContent = numberOfUsedLicenses + 1;
				if (plan == 'business') {
					updatesLicenseIncrementer('increase');
				}
			}

			function updatesLicenseIncrementer(action) {
				const licensesLimitPlaceholder = progressSubtitle.querySelector('#licenses-limit');
				const licensesLimit = Number(licensesLimitPlaceholder.textContent);
				const isToIncreaseNumberOfChosenLicenses =
					action == 'increase' && numberOfUsedLicenses == licensesLimit;
				const isToDecreaseModifiedNumberOfLicenses =
					action == 'decrease' && Number(licensesLimitPlaceholder.dataset.modified) == 1;

				if (isToIncreaseNumberOfChosenLicenses || isToDecreaseModifiedNumberOfLicenses) {
					const targetButton = targetCheckbox
						.closest('.free-trial__end--plans')
						.querySelector(`img[data-operation=${action}]`);

					licensesLimitPlaceholder.dataset.modified = action == 'increase' ? 1 : 0;
					targetButton.click();
				}
			}
		}
	}

	function changePaymentPeriod(event) {
		const targetButton = event.currentTarget;

		const currentPeriod = targetButton.closest('div').dataset.previous;
		const targetPeriod = targetButton.value;
		const yearlyPaymentContent = targetButton
			.closest('section')
			.querySelector('[data-period="yearly"]:not(input)');
		const monthlyPaymentContent = targetButton
			.closest('section')
			.querySelector('[data-period="monthly"]:not(input)');

		if (targetPeriod == 'yearly') {
			monthlyPaymentContent.classList.add('d-none');
			yearlyPaymentContent.classList.add('d-flex');
			yearlyPaymentContent.classList.remove('d-none');
		} else {
			yearlyPaymentContent.classList.add('d-none');
			yearlyPaymentContent.classList.remove('d-flex');
			monthlyPaymentContent.classList.remove('d-none');
		}

		const queriesSwitch = targetButton
			.closest('section')
			.querySelector('.custom__switch input');
		if (currentPeriod != targetPeriod && queriesSwitch) {
			handleQueriesLimit(queriesSwitch);
		}

		targetButton.closest('div').dataset.previous = targetPeriod;
	}

	function handleQueriesLimit(event) {
		let targetInput, currentPeriod;
		let clickOnPlusQueries = false;

		if (event instanceof Event) {
			targetInput = event.currentTarget;
			currentPeriod = targetInput
				.closest('section')
				.querySelector('.custom__radio--container input:checked').value;
			clickOnPlusQueries = true;
		} else {
			// Delegation from another function
			targetInput = event;
			currentPeriod = targetInput
				.closest('section')
				.querySelector('.custom__radio--container input:not(:checked)').value;
		}
		// input is checked before js runs
		const inputIsChecked = targetInput.checked;
		const container = targetInput.closest('section');
		const pricePlaceholder = container.querySelector(`span.js-price-${currentPeriod}`);
		const price = Number(pricePlaceholder.dataset.price.replace(',', '.'));
		const priceToAddPlaceholder = container.querySelector(`span.js-extra-price`);
		let priceToAdd = Number(priceToAddPlaceholder.textContent.replace(',', '.'));

		if (currentPeriod == 'monthly') {
			if (!clickOnPlusQueries) {
				priceToAdd = 0;
			}
			pricePlaceholder.textContent = `${!inputIsChecked ? price : price + priceToAdd},00`;
		} else {
			const previousPricePlaceholder = container.querySelector(
				`span.js-previous-price-${currentPeriod}`
			);
			const previousPrice = Number(
				pricePlaceholder.dataset.price_without_discount.replace(',', '.')
			);
			let yearlyPriceToAddWithDiscount = plusToAddYearly(priceToAdd);
			let yearlyPriceToAddWithoutDiscount = priceToAdd * 12;
			if (!clickOnPlusQueries) {
				yearlyPriceToAddWithDiscount = 0;
				yearlyPriceToAddWithoutDiscount = 0;
			}

			pricePlaceholder.textContent = `${
				!inputIsChecked ? price : price + yearlyPriceToAddWithDiscount
			},00`;

			previousPricePlaceholder.textContent = `${
				!inputIsChecked ? previousPrice : previousPrice + yearlyPriceToAddWithoutDiscount
			},00`;
		}
		if (!(event instanceof Event)) {
			targetInput.checked = false;
		}
	}

	function setSubmitButtonClickable(event) {
		const cnpjInput = event.target;
		const submitButton = cnpjInput.closest('form').querySelector('button[type="submit"]');
		submitButton.disabled = !cnpjInput.value || !cnpjInput.checkValidity();
	}
});

const submitPlanOption = (event) => {
	event.preventDefault();

	const form = document.querySelector('.free-trial__end--plans form.js-submit-form');
	const formElements = form.elements;

	let submitButton = formElements.submitEndOfTrialPlanButton;
	showLoading(submitButton);
	let loading = document.querySelector('.loading_div');

	const userIsInsideLimit = checkLicensesLimit(false);

	if (!userIsInsideLimit) {
		const errorMessage = `${translate['you_are_hiring_more_licenses_allowed'][language]}.`;
		Swal.fire('Oops..', errorMessage, 'error');
		hideLoading(submitButton);
		throw new Error(errorMessage);
	}
	let planValue = 0;
	let cleanedCnpj = document
		.querySelector('#modalPagarmeInfos .input_cnpj')
		?.value.replace(/\D/g, '');
	if (cleanedCnpj && cleanedCnpj.length != 14) {
		const errorMessage = translate['invalid_cnpj_please_type_again'][language];
		Swal.fire('Oops..', errorMessage, 'error');
		hideLoading(submitButton);
		throw new Error(errorMessage);
	} else if (cleanedCnpj && cleanedCnpj.length == 14) {
		const chosenPeriod = getInputChosenPeriod(form);
		planValue = getPlanValue(form, chosenPeriod);
	}

	const plan = getPlan();
	const isBusinessPlan = plan == 'business';

	const { chosenServices, lostServices, schedulesToBeDeleted, forbiddenSchedules } =
		getServices();

	let settings;
	const csrftoken = getCookie('csrftoken');

	if (isBusinessPlan) {
		const numberOfQueries = form.querySelector('.button__group.active').dataset.value;
		const numberOfLicenses = Number(
			document.getElementById('business-number-of-licenses').value
		);
		let data = {
			cnpj: cleanedCnpj,
			chosen_services: chosenServices,
			lost_services: lostServices,
			chosen_number_of_queries:
				numberOfQueries == 'unlimited' ? numberOfQueries : Number(numberOfQueries),
			chosen_number_of_licenses: numberOfLicenses,
			chosen_plan: plan,
			schedules_to_be_deleted: schedulesToBeDeleted,
			forbidden_schedules: forbiddenSchedules,
			plan_value: planValue,
		};
		if (planValue > 0) {
			const chosenPeriod = getInputChosenPeriod(form);
			data['chosen_period'] = chosenPeriod;
		}
		settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify(data),
		};
	} else {
		const userChoseExtraQueries = formElements.queries.checked;
		const chosenPeriod = getInputChosenPeriod(form);

		settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				cnpj: cleanedCnpj,
				chosen_services: chosenServices,
				lost_services: lostServices,
				chosen_period: chosenPeriod,
				with_extra_queries: userChoseExtraQueries == true ? 1 : 0,
				chosen_plan: plan,
				schedules_to_be_deleted: schedulesToBeDeleted,
				forbidden_schedules: forbiddenSchedules,
			}),
		};
	}
	concludeChoosePlan(settings);

	async function concludeChoosePlan(settings) {
		const response = await fetch('/trial/choose-plan/conclude', settings);

		if (response.ok == true) {
			window.location = '/trial/choose-plan/feedback';
		} else {
			replaceWith(loading, submitButton.outerHTML);

			const convertedResponse = await response.json();

			const errorMessage =
				convertedResponse['error'] ||
				`${translate['plan_registration_error_msg'][language]} <strong class='d-block'>${translate['hub_contact_email'][language]}</strong>`;

			Swal.fire('Oops..', errorMessage, 'error');
		}
	}

	function getServices() {
		const allCheckboxes = document.querySelectorAll(
			'.free-trial__end--plans .single_checkbox input'
		);

		const chosenServices = [];
		const lostServices = [];
		const schedulesToBeDeleted = [];
		const forbiddenSchedules = {};

		allCheckboxes.forEach((checkbox) => {
			const container = checkbox.closest('.trial__choose-plan-service-box');
			const service = container.dataset.service;
			const userThatUsedThisService = container.querySelector('em')?.dataset.id || null;
			const allSchedulesOfService = container.querySelectorAll('input[type="hidden"]');

			const objectWithServiceInfo = {};

			objectWithServiceInfo[service] = userThatUsedThisService;

			if (checkbox.checked) {
				chosenServices.push(service);
				if (allSchedulesOfService && userThatUsedThisService) {
					allSchedulesOfService.forEach((schedule) => {
						forbiddenSchedules[Number(schedule.value)] = userThatUsedThisService;
					});
				}
			} else {
				lostServices.push(objectWithServiceInfo);
				if (allSchedulesOfService) {
					allSchedulesOfService.forEach((schedule) => {
						schedulesToBeDeleted.push(Number(schedule.value));
					});
				}
			}
		});

		return {
			chosenServices,
			lostServices,
			schedulesToBeDeleted,
			forbiddenSchedules,
		};
	}
};

function checkLicensesLimit(interestedInSmallerThan = true) {
	const container = document.querySelector('.free-trial__end--plans');
	const plan = getPlan();
	const numberOfUsedLicenses = getNumberOfUsedLicenses();
	const licensesLimit = Number(container.dataset.licenses);

	if (interestedInSmallerThan) {
		return plan == 'business' || numberOfUsedLicenses < licensesLimit;
	} else {
		return plan == 'business' || numberOfUsedLicenses <= licensesLimit;
	}
}

function getNumberOfUsedLicenses() {
	const numberOfChosenServices = document.querySelectorAll(
		'.free-trial__end--plans .single_checkbox input[type="checkbox"]:checked'
	).length;

	return numberOfChosenServices;
}

function getPlan() {
	return document.querySelector('.free-trial__end--plans').dataset.plan;
}

const plusToAddYearly = (price) => {
	return price * 10;
};

function showLoading(payButton) {
	let loading = document.querySelector('.loading_div');
	payButton.classList.add('d-none');
	loading.classList.add('d-flex');
	loading.classList.remove('d-none');
}

function hideLoading(payButton) {
	let loading = payButton.closest('div').querySelector('.loading_div');
	payButton.classList.remove('d-none');
	loading.classList.remove('d-flex');
	loading.classList.add('d-none');
}

const getPlanValue = (form, chosenPeriod) => {
	const pricePlaceholder = form.querySelector(`span.js-price-${chosenPeriod}`);
	return Number(pricePlaceholder.textContent.replace(',', '.'));
};

const getInputChosenPeriod = (form) => {
	const inputChosen = form.querySelector('.custom__radio--container input:checked');
	return inputChosen
		? inputChosen.value
		: form.querySelector('.custom__radio--container input').value;
};
