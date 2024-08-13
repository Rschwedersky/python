document.addEventListener('DOMContentLoaded', () => {
	const allPlans = Array.from(document.querySelectorAll('.single__plan-box .top_infos'));
	const oldSelectedPlan = document.querySelector('.single__plan-box[data-selected="true"]');
	const oldPriceElement = oldSelectedPlan?.querySelector('.single__plan-box--price strong');
	const oldPrice = getPrice(oldPriceElement?.textContent);

	const periodPayments = Array.from(
		document.querySelectorAll('.modal__plans .trial-plan-choice-buttons')
	);
	const allPlansPlusSwitch = Array.from(
		document.querySelectorAll('.plans__modal--footer .custom__switch input')
	);

	allPlans.forEach((singlePlan) => {
		singlePlan.addEventListener('click', handlePlanClick);
	});
	periodPayments.forEach((period) => {
		period.addEventListener('click', handlePeriodClick);
	});
	allPlansPlusSwitch.forEach((singlePlanPlusSwitch) => {
		singlePlanPlusSwitch.addEventListener('change', handleExtraQueries);
	});

	function handlePlanClick(e) {
		e.preventDefault();
		document
			.querySelector('.single__plan-box.single__plan-box--selected')
			?.classList.remove('single__plan-box--selected');
		e.currentTarget.closest('.single__plan-box').classList.add('single__plan-box--selected');

		shouldDisableChange();
	}

	function handlePeriodClick(event) {
		event.preventDefault();

		const newActive = event.currentTarget;
		const oldActive = document.querySelector('.modal__plans .trial-plan-choice-buttons.active');
		const clickedTheSameButton = newActive.classList.contains('active');

		if (!clickedTheSameButton) {
			oldActive.classList.remove('active');
			newActive.classList.add('active');

			updatePlanValues(newActive.dataset.period);

			allPlansPlusSwitch.forEach((switchInput) => {
				const currentPlanBox = switchInput.closest('.single__plan-box');
				const isInputChecked = switchInput.checked;
				const isGoingToCurrentPlan =
					switchInput.dataset.selected &&
					switchInput.dataset.period.includes(newActive.dataset.period);

				if (!isInputChecked && !isGoingToCurrentPlan) return;

				if (isGoingToCurrentPlan) {
					switchInput.checked = true;
					currentPlanBox.classList.add('single__plan-box--selected');
				} else {
					switchInput.checked = false;
				}
			});
			shouldDisableChange();
		}
	}

	function handleExtraQueries(event) {
		const targetInput = event.target;
		const targetPlan = targetInput.closest('.single__plan-box');
		const currentPriceElement = targetPlan.querySelector('.single__plan-box--price strong');
		const currentPrice = getPrice(currentPriceElement.textContent);
		const extraPriceElement = targetPlan.querySelector(
			'.plans__modal--footer .extra-queries-price'
		);
		const extraPrice = getPrice(extraPriceElement.textContent);
		const currentPeriod = getCurrentPeriod(targetInput);
		const isAnualPeriod = currentPeriod == 'year';
		const queriesAreBeingAdded = targetInput.checked;
		let finalPrice = null;

		if (isAnualPeriod) {
			const anualExtraPriceWithDiscount = extraPrice * 10;
			if (queriesAreBeingAdded) {
				finalPrice = currentPrice + anualExtraPriceWithDiscount;
			} else {
				finalPrice = currentPrice - anualExtraPriceWithDiscount;
			}
		} else {
			if (queriesAreBeingAdded) {
				finalPrice = currentPrice + extraPrice;
			} else {
				finalPrice = currentPrice - extraPrice;
			}
		}

		currentPriceElement.textContent = finalPrice;
		if (targetPlan.classList.contains('single__plan-box--selected')) {
			shouldDisableChange();
		}
	}

	function updatePlanValues(period) {
		const allPlansValues = Array.from(
			document.querySelectorAll('.modal__plans .single__plan-box--price')
		);

		allPlansValues.forEach((planValue) => {
			const priceElement = planValue.querySelector('strong');
			const periodElement = planValue.querySelector('span');

			priceElement.textContent =
				period == 'month'
					? planValue.dataset.monthly_price
					: planValue.dataset.yearly_price;

			periodElement.textContent = `/ ${translate[period][language].toLowerCase()}`;
		});
	}

	function getSelectedValues() {
		const selectedPlan = document.querySelector('.single__plan-box--selected');
		let selectedExtraQueries = false;
		if (selectedPlan) {
			selectedExtraQueries = selectedPlan.querySelector('.custom__switch input')?.checked;
		}
		return { selectedPlan, selectedExtraQueries };
	}

	function shouldDisableChange() {
		const onlyUpgrade = true;
		const submitButton = document.querySelector('.update_plan button.btn__purple');
		const { selectedPlan } = getSelectedValues();
		if (onlyUpgrade && selectedPlan && isPlanUpgrade(selectedPlan)) {
			submitButton.disabled = false;
			updateHrefChangePlan();
		} else {
			submitButton.disabled = true;
		}
	}

	function isPlanUpgrade(selectedPlan) {
		const currentPriceElement = selectedPlan.querySelector('.single__plan-box--price strong');
		let currentPrice = 0;
		if (selectedPlan.dataset.value != 'business') {
			currentPrice = getPrice(currentPriceElement.textContent);
		} else {
			currentPrice = oldPrice + 1;
		}
		return currentPrice > oldPrice;
	}

	function getPrice(price) {
		return price ? Number(price.replace(',', '.')) : 0;
	}

	function updateHrefChangePlan() {
		const { selectedPlan, selectedExtraQueries, selectedPeriod } = getSelectedValues();
		let plus = '';
		if (selectedExtraQueries) {
			plus = '/plus';
		}
		let translatePeriod = { month: 'monthly', year: 'yearly' };

		const href = `/update/plan/${selectedPlan.dataset.value}/${
			translatePeriod[getCurrentPeriod(selectedPlan)]
		}${plus}`;
		document.querySelector('.update_plan').href = href;
	}

	function getCurrentPeriod(targetElement) {
		const container = targetElement.closest('.modal__plans');
		const period = container.querySelector('.trial-plan-choice-buttons.active').dataset.period;
		return period;
	}
});
