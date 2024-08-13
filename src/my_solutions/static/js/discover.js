document.addEventListener('DOMContentLoaded', () => {
	const csrftoken = getCookie('csrftoken');
	/**********************  TIMER CONTROLLER ********************************/
	let timerHandler;
	let confirmationModalTimerHandler;
	/**********************  STATE ********************************/
	let modalHeadingText;
	let currentUpgradeStep = 1;
	let currentSwitchStep = 1;
	let forbidToCloseModal = false;
	/**********************  CONSTANTS WITH EVENT LISTENERS ********************************/
	const discoverModalMessage = document.getElementById('discover-suggestion-message');
	const allButtonsWithAnimation = Array.from(
		document.getElementsByClassName('button__primary-color--discover-soon')
	);
	const discoverModalOptionBoxes = Array.from(
		document.getElementsByClassName('discover__modal--options-box')
	);
	let allModalStepButtons = Array.from(document.getElementsByClassName('modal__step'));
	const allConfirmationModalStepButtons = Array.from(
		document.getElementsByClassName('confirmation-modal__step')
	);
	const closeDiscoverModalsButtons = Array.from(
		document.getElementsByClassName('discover__modal-close')
	);
	const allPlanBoxes = Array.from(document.getElementsByClassName('discover__plan-box'));
	const confirmationModalCloseButtons = Array.from(
		document.getElementsByClassName('discover__confirmation-modal-close')
	);
	const advanceButtonConfirmationModalSwitch = document.getElementById(
		'advance-button-discover-confirmation-modal-switch'
	);

	const allButtonsToAddService = Array.from(
		document.getElementsByClassName('discover__add-service')
	);

	const allButtonsThatManipulateLicenses = Array.from(
		document.getElementsByClassName('btn__manipulate-permissions--discover')
	);

	/**********************  CONSTANTS ********************************/

	const allDiscoverServiceBoxes = Array.from(
		document.getElementsByClassName('discover__service-box--more')
	);

	const modalHeading = document.getElementById('discover-hire-service-modal-heading');
	const okButtonConfirmationModal = document.getElementById('ok-button-discover-modal-success');
	const underMaintenanceButton = document.querySelectorAll('.permissions-text--inactive button');

	/**********************  EXECUTABLE CODE ********************************/

	allDiscoverServiceBoxes.forEach(addPermissionsAvailableBadge);
	allDiscoverServiceBoxes.forEach((box) => box.addEventListener('click', handleServiceBoxClick));

	// discoverModalMessage.addEventListener('input', handleTextAreaChange);

	allButtonsWithAnimation.forEach((button) =>
		button.addEventListener('click', handleFutureServiceInterest, false)
	);

	discoverModalOptionBoxes.forEach((box) => box.addEventListener('click', handleBoxClick));

	allModalStepButtons.forEach((button) => button.addEventListener('click', handleModalSteps));

	allConfirmationModalStepButtons.forEach((button) =>
		button.addEventListener('click', handleConfirmationModalSteps)
	);

	closeDiscoverModalsButtons.forEach((closeBtn) =>
		closeBtn.addEventListener('click', handleDiscoverModalReset)
	);

	// allPlanBoxes.forEach((box) => box.addEventListener('click', handleSelectedPlan));

	confirmationModalCloseButtons.forEach((button) =>
		button.addEventListener('click', cleanConfirmationModals)
	);

	advanceButtonConfirmationModalSwitch.addEventListener(
		'click',
		savePermissionsChangesToDatabase
	);

	allButtonsToAddService.forEach((button) =>
		button.addEventListener('click', addServiceFromDiscover)
	);

	allButtonsThatManipulateLicenses.forEach((button) =>
		button.addEventListener('click', handleLicensesManipulation)
	);

	underMaintenanceButton.forEach((button) =>
		button.addEventListener('click', warnUserWhenServiceIsFixed)
	);

	/**********************  EVENT DELEGATIONS ******************************/
	const discoverModalBackground = document.querySelector('.modal__background--discover');
	discoverModalBackground.addEventListener('click', handleDiscoverModalEventsDelegation);

	function handleDiscoverModalEventsDelegation(event) {
		if (
			event.target.id == 'discover-switch-service-dropdown' ||
			Boolean(event.target.closest('#discover-switch-service-dropdown')) == true
		) {
			handleDropdownSelectedService(event);
		}
	}

	function handleSinglePermissionExchangeDelegation(event) {
		if (
			event.target.classList.contains('discover__button-switch') ||
			event.target.closest('button')?.classList.contains('discover__button-switch')
		) {
			handlePermissionsExchange(event);
		}
	}

	/**********************  DECLARATIONS ********************************/

	function addPermissionsAvailableBadge(box) {
		const availablePermissionsData = box.nextElementSibling;
		let numberOfAvailablePermissions = availablePermissionsData?.dataset.available;

		let serviceIsInactive = Boolean(box.querySelector('[data-inactive="True"]'));
		badgeContainer = document.createElement('div');
		badgeContainer.classList.add('position-relative', 'w-100');

		if (serviceIsInactive) {
			badgeContainer.classList.add('opacity-50');
		}
		const badge = document.createElement('span');

		badge.classList.add('discover__badge', 'discover__badge--permission-available');

		if (
			availablePermissionsData?.tagName != 'INPUT' ||
			Boolean(numberOfAvailablePermissions) == false
		) {
			numberOfAvailablePermissions = 0;
		}

		badge.textContent = `${numberOfAvailablePermissions} ${checkNumberAgreement(
			numberOfAvailablePermissions,
			'available'
		)}`;
		badgeContainer.appendChild(badge);
		box.prepend(badgeContainer);

		if (numberOfAvailablePermissions == 0) {
			badgeContainer.style.visibility = 'hidden';
		}
	}

	function checkTotalNumberOfServiceSchedules(service) {
		const collaboratorsAllocatedToThisService = Array.from(
			service.nextElementSibling.children
		).filter(
			(button) =>
				button.classList.contains('discover__switch-service-select--selected') == false
		);
		const scheduleSpan = service.querySelector('span');

		let totalNumberOfSchedules = 0;
		if (Boolean(scheduleSpan) == true) {
			collaboratorsAllocatedToThisService.forEach(
				(collaborator) =>
					(totalNumberOfSchedules +=
						(collaborator.dataset.schedules &&
							Number(collaborator.dataset.schedules)) ||
						0)
			);

			if (totalNumberOfSchedules == 1) {
				scheduleSpan.textContent = `${totalNumberOfSchedules} ${translate['model_configured'][language]}`;
			} else {
				scheduleSpan.textContent = `${totalNumberOfSchedules} ${translate['models_configured'][language]}`;
			}
		}
	}

	function handleServiceBoxClick(event) {
		const target = event.target;

		const targetIsNotButton = target.tagName != 'button';
		const targetIsNotInsideButton = Boolean(target.closest('button')) == false;
		const boxIsNotDisabled =
			target.closest('.discover__service-box')?.classList.contains('no-pointer-events') ==
			false;
		const targetIsNotInsideInactiveBox =
			Boolean(target.closest('.permissions-text--inactive')) == false;

		if (
			targetIsNotButton &&
			targetIsNotInsideButton &&
			boxIsNotDisabled &&
			targetIsNotInsideInactiveBox
		) {
			const box = target.closest('.discover__service-box--more');
			if (Boolean(box)) {
				const whereToGo = box.querySelector('a').href;
				window.open(whereToGo, '_top');
			}
		}
	}

	function handleTextAreaChange(event) {
		const targetTextArea = event.target;
		const whichButtonToManipulate = document.getElementById(targetTextArea.dataset.button);
		const infoTextToManipulate = targetTextArea.closest('form').querySelector('p');

		if (Boolean(targetTextArea.value) == true) {
			whichButtonToManipulate.disabled = false;
			infoTextToManipulate.style.display = 'none';
		} else {
			whichButtonToManipulate.disabled = true;
			infoTextToManipulate.style.display = 'block';
		}
	}

	async function handleFutureServiceInterest(event) {
		let targetButton = event.currentTarget;

		const buttonText = targetButton.querySelector('span');
		const buttonSpinner = targetButton.querySelector('div');
		const automationName = targetButton.closest('.discover__service-box--soon').dataset
			.automation;

		buttonText.style.display = 'none';
		buttonSpinner.style.display = 'block';

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				automation_name: automationName,
				interested: targetButton.classList.contains('button__primary-color--clicked')
					? 0
					: 1,
			}),
		};

		const response = await fetch('/discover/future_service', settings);

		if (
			targetButton.classList.contains('button__primary-color--clicked') &&
			response.ok == true
		) {
			buttonText.textContent = translate['warn_me'][language];
			targetButton.classList.remove('button__primary-color--clicked');
		} else if (
			targetButton.classList.contains('button__primary-color--clicked') == false &&
			response.ok == true
		) {
			buttonText.textContent = translate['you_will_receive_news'][language];
			targetButton.classList.add('button__primary-color--clicked');
		}

		buttonSpinner.style.display = '';
		buttonText.style.display = '';
	}

	function handleBoxClick(event) {
		let targetBox = event.target;
		if (targetBox.tagName != 'section') {
			targetBox = targetBox.closest('section');
		}

		const advanceButton = targetBox
			.closest('.modal__tab')
			.querySelector('[data-step="advance"]');
		const oldActive = document.querySelector('.discover__modal--options-box--clicked');

		removeOldActive(
			discoverModalOptionBoxes,
			'discover__modal--options-box--clicked',
			targetBox
		);

		targetBox.classList.toggle('discover__modal--options-box--clicked');

		if (advanceButton.disabled == false) {
			if (Boolean(oldActive) == true && oldActive == targetBox) {
				advanceButton.disabled = true;
			}
		} else {
			advanceButton.disabled = false;
		}
	}

	async function handleModalSteps(event) {
		const targetButton = event.target;
		const whichSelectedOption = document.querySelector('.discover__modal--options-box--clicked')
			.dataset.option;
		const allSteps = Array.from(document.getElementsByClassName('modal__tab'));

		if (modalHeading.textContent.includes(translate['to_your_plan'][language])) {
			modalHeadingText = modalHeading.innerHTML;
		}

		if (whichSelectedOption == 'upgrade') {
			const allUpgradeSteps = allSteps.filter(
				(step) => step.classList.contains('modal__tab--switch') == false
			);
			if (targetButton.dataset.step == 'return') {
				currentUpgradeStep = 2;

				allUpgradeSteps[currentUpgradeStep].classList.remove('d-flex');
				allUpgradeSteps[currentUpgradeStep].classList.add('d-none');

				allUpgradeSteps[0].classList.remove('d-none');
				allUpgradeSteps[0].classList.add('d-flex', 'flex-column');

				currentUpgradeStep--;

				handleModalBackwardSteps();
			} else {
				allUpgradeSteps[currentUpgradeStep - 1].classList.remove('d-flex');
				allUpgradeSteps[currentUpgradeStep - 1].classList.add('d-none');

				allUpgradeSteps[currentUpgradeStep].classList.remove('d-none');
				allUpgradeSteps[currentUpgradeStep].classList.add('d-flex', 'flex-column');

				if (currentUpgradeStep == 1) {
					timerHandler = setTimeout(waitAndShowPlans, 2000, event);
				}

				currentUpgradeStep++;
			}
		} else {
			const allSwitchPermissionsSteps = allSteps.filter(
				(step) => step.classList.contains('modal__tab--upgrade') == false
			);

			if (targetButton.dataset.step == 'return') {
				currentSwitchStep = 1;

				allSwitchPermissionsSteps[currentSwitchStep].classList.remove('d-flex');
				allSwitchPermissionsSteps[currentSwitchStep].classList.add('d-none');

				allSwitchPermissionsSteps[0].classList.remove('d-none');
				allSwitchPermissionsSteps[0].classList.add('d-flex', 'flex-column');

				currentSwitchStep--;

				handleModalBackwardSteps();
			} else {
				const modalBackground = targetButton.closest('.modal__background');
				const loadingStep = document.getElementById('discover-modal-loading');
				const loadingSpinner = loadingStep.querySelector(
					'.discover__inner-modal--hire__loading'
				);
				const loadingTextElement = loadingSpinner.querySelector('p');
				const modal = targetButton.closest('.discover__inner-modal--hire');

				if (!modal) return;

				const automationName = modal.dataset.service;

				allSwitchPermissionsSteps[currentSwitchStep - 1].classList.remove('d-flex');
				allSwitchPermissionsSteps[currentSwitchStep - 1].classList.add('d-none');

				showLoading();

				const switchServiceStepContentResponse = await fetch(
					`/discover/services-info/${automationName}`
				);
				const renderedToHTML = await switchServiceStepContentResponse.text();

				const switchServiceStepContainer = allSwitchPermissionsSteps[currentSwitchStep];

				switchServiceStepContainer.innerHTML = renderedToHTML;

				updateModalAfterResponse();
				updateJsAfterResponse();

				const switchServicesModalSubtitle = document.getElementById(
					'discover-modal-switch-services-subtitle'
				);
				let serviceName;

				if (targetButton != advanceButtonConfirmationModalSwitch) {
					serviceName = modalHeading.querySelector('strong').textContent;

					modalHeading.textContent = translate['exchange_service'][language];
					switchServicesModalSubtitle.innerHTML = `${translate['choose_a_service'][language]} <em>${serviceName}</em>`;

					hideTargetServiceInDropdown();
				}

				hideLoading();

				switchServiceStepContainer.classList.remove('d-none');
				switchServiceStepContainer.classList.add('d-flex', 'flex-column');

				currentSwitchStep++;

				function showLoading() {
					forbidToCloseModal = true;
					modalBackground.removeEventListener('click', handleClickOutsideModal);

					loadingSpinner.style.flexGrow = '1';
					loadingTextElement.textContent = `${translate['loading_my_services'][language]}...`;
					loadingStep.classList.remove('d-none');
					loadingStep.classList.add('d-flex');
				}

				function hideLoading() {
					loadingStep.classList.remove('d-flex');
					loadingStep.classList.add('d-none');
					loadingSpinner.style.flexGrow = '';

					loadingTextElement.textContent = `${translate['opening_upgrade_options'][language]}...`;
					modalBackground.addEventListener('click', handleClickOutsideModal);
					forbidToCloseModal = false;
				}

				function updateModalAfterResponse() {
					const newServiceBox = modal.querySelector('.discover__switch-service-new');

					newServiceBox.dataset.service = modal.dataset.service;
				}

				function updateJsAfterResponse() {
					const oldPermissionsBox = document.getElementById(
						'discover-permissions-box-active'
					);
					const newPermissionsBox = document.getElementById(
						'discover-permissions-box-new'
					);
					const allSwitchServicesButtons = Array.from(
						document.getElementsByClassName('discover__button-switch')
					);
					allModalStepButtons = Array.from(
						document.getElementsByClassName('modal__step')
					);
					const allClientServices = Array.from(
						document.getElementsByClassName('discover__switch-service-select')
					);

					oldPermissionsBox.addEventListener(
						'click',
						handleSinglePermissionExchangeDelegation
					);
					newPermissionsBox.addEventListener(
						'click',
						handleSinglePermissionExchangeDelegation
					);

					allSwitchServicesButtons.forEach((button) =>
						button.addEventListener('click', handlePermissionsExchange)
					);

					allModalStepButtons.forEach((button) =>
						button.addEventListener('click', handleModalSteps)
					);

					allClientServices.forEach(checkTotalNumberOfServiceSchedules);
				}
			}
		}
	}

	function handleConfirmationModalSteps(event) {
		const targetButton = event.target;
		const whichSelectedOption = document.querySelector('.discover__modal--options-box--clicked')
			.dataset.option;

		if (targetButton.classList.contains('confirmation-modal__tab--upgrade')) {
			//Todo: Add logic to upgrade plans confirmation modals
			// event.stopPropagation();
			// setUpCloseModalButton(targetButton);
		} else {
			const switchPermissionsConfirmationSteps = Array.from(
				document.getElementsByClassName('confirmation-modal__tab--switch')
			);
			const footer = event.target.closest('footer');
			const isShowcase =
				document.querySelector('.discover__inner-modal--hire').dataset.showcase == 'true';

			switchPermissionsConfirmationSteps[0].classList.remove('d-flex');
			switchPermissionsConfirmationSteps[0].classList.add('d-none');

			switchPermissionsConfirmationSteps[1].classList.add('d-flex', 'flex-column');
			switchPermissionsConfirmationSteps[1].classList.remove('d-none');

			confirmationModalTimerHandler = setTimeout(waitAndConfirmChanges, 2000);
			footer.style.visibility = 'hidden';

			function waitAndConfirmChanges() {
				const cancelButton = advanceButtonConfirmationModalSwitch.previousElementSibling;
				const xButton = footer
					.closest('.discover__confirmation-modal--switch')
					.querySelector('img.discover__confirmation-modal-close');
				const advanceButton = document.getElementById(
					'discover-modal-no-permissions-advance-button'
				);

				advanceButtonConfirmationModalSwitch.textContent = 'OK';
				advanceButtonConfirmationModalSwitch.dataset.close = '.modal__background';
				advanceButtonConfirmationModalSwitch.classList.add(
					'modal__close',
					'discover__modal-close'
				);

				advanceButtonConfirmationModalSwitch.addEventListener('click', reloadPage);
				advanceButtonConfirmationModalSwitch.removeEventListener('click', handleModalSteps);
				advanceButton.removeEventListener('click', checkWhichConfirmationMessage);

				xButton.style.display = 'none';
				cancelButton.style.display = 'none';
				footer.style.visibility = '';

				switchPermissionsConfirmationSteps[1].classList.remove('d-flex');
				switchPermissionsConfirmationSteps[1].classList.add('d-none');

				if (isShowcase) {
					const feedbackModalContent =
						switchPermissionsConfirmationSteps[2].querySelector('.jsShowcase');
					feedbackModalContent.innerHTML = `<p class="m-0"><strong>Serviço solicitado sucesso!</strong></p><p>Nossa equipe irá entrar em contato em até 24h. Em breve você poderá utilizá-lo.</p>`;
				}

				switchPermissionsConfirmationSteps[2].classList.add('d-flex', 'gap-16');
				switchPermissionsConfirmationSteps[2].classList.remove('d-none');
			}
		}
	}

	function handleDiscoverModalReset(event) {
		const target = event.target;
		if (target.textContent != translate['confirm'][language]) {
			event.stopPropagation();
		}

		if (target.classList.contains('discover__modal-close') && !forbidToCloseModal) {
			const allModalBackgrounds = Array.from(
				document.getElementsByClassName('modal__background')
			);
			allModalBackgrounds.forEach((modal) => (modal.style.display = ''));

			clearTimeout(timerHandler);
			clearTimeout(confirmationModalTimerHandler);

			const stepsToHide = Array.from(
				document.getElementsByClassName('discover__inner-modal-close')
			);
			const stepsToShow = Array.from(
				document.getElementsByClassName('discover__inner-modal-show')
			);

			stepsToHide.forEach((step) => {
				step.classList.remove('d-flex', 'flex-column');
				step.classList.add('d-none');
			});
			stepsToShow.forEach((step) => {
				step.classList.remove('d-none');
				step.classList.add('d-flex', 'flex-column');
			});

			resetConfirmationModalFooter();

			currentSwitchStep = 1;
			currentUpgradeStep = 1;

			removeOldActive(discoverModalOptionBoxes, 'discover__modal--options-box--clicked');

			// removeOldActive(allPlanBoxes, 'discover__plan-box--selected');

			// resetPlans();

			handleSwitchServiceReset();

			modalHeading.innerHTML = modalHeadingText;

			document.querySelector('html').style.overflowY = '';
		}
	}

	function handleSelectedPlan(event) {
		let targetPlan = event.target;
		if (targetPlan.classList.contains('discover__plan-box') == false) {
			targetPlan = targetPlan.closest('.discover__plan-box');
		}

		removeOldActive(allPlanBoxes, 'discover__plan-box--selected', targetPlan);
		targetPlan.classList.toggle('discover__plan-box--selected');
		handleButtonState();

		function handleButtonState() {
			const saveButton = document.getElementById(
				'discover-modal-no-permissions-advance-button'
			);
			const isAnyBoxSelected = Boolean(
				document.querySelector('.discover__plan-box--selected')
			);
			if (targetPlan.dataset.selected != 'true' && isAnyBoxSelected == true) {
				saveButton.disabled = false;
			} else {
				saveButton.disabled = true;
			}
		}
	}

	function handleDropdownSelectedService(event) {
		let targetService = event.target;
		if (targetService.tagName != 'button') {
			targetService = targetService.closest('button');
		}

		const targetButtonContent = targetService.innerHTML;
		const targetLocation = document.getElementById('discover-dropdown-selected-placeholder');
		const selectedButton = targetLocation.closest('button');

		targetLocation.innerHTML = targetButtonContent;

		selectedButton.dataset.service = targetService.dataset.service;
		removeOldPermissionBoxes();
		showPermissionsContent(targetService);

		targetService.style.display = 'none';

		if (Boolean(selectedButton.dataset.previous) == true) {
			const previousElement = document.getElementById(selectedButton.dataset.previous);
			previousElement.style.display = '';
		}
		targetService.id = '_' + Math.random().toString(36).substr(2, 9);
		selectedButton.dataset.previous = targetService.id;

		handleSwitchServiceButtonState('discover__button-switch--trade');
		createInvisibleBoxes();

		function removeOldPermissionBoxes() {
			const oldPermissionsBox = document.getElementById('discover-permissions-box-active');
			const allChildren = Array.from(oldPermissionsBox.children);

			allChildren
				.filter((child) => child.classList.contains('discover__switch-collaborator-box'))
				.forEach((child) => child.remove());
		}
	}

	function handlePermissionsExchange(event) {
		let targetButton = event.target;
		if (targetButton.tagName != 'button') {
			targetButton = targetButton.closest('button');
		}
		const buttonType = targetButton.dataset.switch;
		const numberOfNewServicePermissions = getTotalNumberOfPermissions()[1];
		const numberOfActiveServicePermissions = getTotalNumberOfPermissions()[0];
		const activeAllPermissionsHeader = document.getElementById(
			'discover-permission-text-active'
		);
		const newAllPermissionsHeader = document.getElementById('discover-permission-text-new');

		if (targetButton.classList.contains('discover__button-switch--trade')) {
			const allCollaboratorsBoxes = Array.from(
				document.getElementsByClassName('discover__switch-collaborator-box')
			);

			if (buttonType == 'all') {
				allCollaboratorsBoxes.forEach(tradePermission);

				newAllPermissionsHeader.textContent = `${numberOfNewServicePermissions} ${checkNumberAgreement(
					numberOfNewServicePermissions
				)}`;

				activeAllPermissionsHeader.textContent = `${numberOfActiveServicePermissions} ${checkNumberAgreement(
					numberOfActiveServicePermissions
				)}`;
			} else {
				const thisServiceBox = targetButton.closest('.discover__switch-collaborator-box');
				tradePermission(thisServiceBox, 'single');
			}
		} else {
			const allPermissionsBoxes = Array.from(
				document.getElementsByClassName('discover__switch-permission-box')
			);
			if (buttonType == 'all') {
				allPermissionsBoxes.forEach(handleReturnPermission);

				activeAllPermissionsHeader.textContent = `${numberOfActiveServicePermissions} ${checkNumberAgreement(
					numberOfActiveServicePermissions
				)}`;

				newAllPermissionsHeader.textContent = `${numberOfNewServicePermissions} ${checkNumberAgreement(
					numberOfNewServicePermissions
				)}`;
			} else {
				const thisServiceBox = targetButton.closest('.discover__switch-permission-box');
				handleReturnPermission(thisServiceBox, 'single');
			}
		}
		getTotalNumberOfPermissions(true);
		handleSwitchServiceButtonState('discover__button-switch');
		checkNewPermissionsSize();
	}

	function tradePermission(box, type = 'all') {
		const boxSpan = box.querySelector('span');
		const numberOfPermissions = returnOnlyNumbersFromString(boxSpan.textContent);
		if (numberOfPermissions > 0) {
			updatePermissionsBox(box, type);
			showDuplicatedElement(box);
		}
	}

	function handleReturnPermission(box, type = 'all') {
		const thisBoxSpan = box.querySelector('span');
		const thisNumberOfPermissions = returnOnlyNumbersFromString(thisBoxSpan.textContent);

		if (thisNumberOfPermissions > 0) {
			updatePermissionsBox(box, type);

			const thisUpdatedNumberOfPermissions = returnOnlyNumbersFromString(
				thisBoxSpan.textContent
			);

			if (thisUpdatedNumberOfPermissions == 0) {
				box.style.visibility = 'hidden';
			}
		}
	}

	function cleanConfirmationModals() {
		const confirmationModalStepsToHide = document.querySelectorAll(
			'.discover__confirmation-modal .discover__inner-modal-close'
		);

		const confirmationModalStepsToShow = Array.from(
			document.querySelectorAll('.discover__confirmation-modal .discover__inner-modal-show')
		);

		confirmationModalStepsToHide.forEach((step) => (step.style.display = 'none'));
		confirmationModalStepsToShow.forEach((step) => (step.style.display = 'flex'));

		resetConfirmationModalFooter();
	}

	async function savePermissionsChangesToDatabase() {
		const targetService = document
			.getElementById('discover-switch-new-service-text')
			.closest('.discover__switch-service-new').dataset.service;
		const sourceService = document.querySelector('.discover__switch-service-select--selected')
			.dataset.service;
		const newAllPermissionsHeader = document.getElementById('discover-permission-text-new');

		const totalOfNewPermissions = returnOnlyNumbersFromString(
			newAllPermissionsHeader.textContent
		);
		const usersToRemove = getUsersToRemovePermissions();

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				automation_name: targetService,
				automation_to_remove_permissions: sourceService,
				all_users_remove: usersToRemove,
				number_of_permissions_to_add: totalOfNewPermissions,
				page: 'discover',
			}),
		};

		const response = await fetch('/services/manage/permissions', settings);

		if (response.ok != true) {
			showErrorMessage();
		}

		advanceButtonConfirmationModalSwitch.removeEventListener(
			'click',
			savePermissionsChangesToDatabase
		);

		function getUsersToRemovePermissions() {
			const oldPermissionsBox = document.getElementById('discover-permissions-box-active');

			const allUsers = Array.from(oldPermissionsBox.children).filter(removeUnwantedChildren);
			const usersToRemove = [];
			allUsers.forEach((user) => usersToRemove.push(Number(user.dataset.user)));
			return usersToRemove;

			function removeUnwantedChildren(child) {
				if (
					child.classList.contains('discover__empty-collaborators') ||
					child.dataset.admin == 'true'
				) {
					return false;
				} else {
					const numberOfPermissionsSpan = child.querySelector('span');
					const numberOfPermissions = returnOnlyNumbersFromString(
						numberOfPermissionsSpan.textContent
					);

					if (numberOfPermissions > 0) {
						return false;
					} else {
						return true;
					}
				}
			}
		}
	}

	/**********************  HELPER DECLARATIONS ****************************/
	function removeOldActive(listToIterate, classToRemove, clickedItem) {
		listToIterate.forEach((item) => {
			if (Boolean(clickedItem) == true) {
				item != clickedItem && item.classList.remove(classToRemove);
			} else {
				item.classList.remove(classToRemove);
			}
		});
	}

	function handleModalBackwardSteps() {
		handleSwitchServiceReset();
		// resetPlans();
		currentUpgradeStep = 1;
		currentSwitchStep = 1;

		modalHeading.innerHTML = modalHeadingText;
	}

	function setUpCloseModalButton(advanceButton) {
		const cancelButton = advanceButton.previousElementSibling;

		advanceButton.textContent = 'Confirmar';
		advanceButton.classList.add('discover__modal-close');
		advanceButton.removeEventListener('click', handleModalSteps);
		advanceButton.addEventListener('click', handleDiscoverModalReset);
		advanceButton.dataset.close = '.modal__background--discover';

		cancelButton.classList.remove('visibility-hidden');
	}

	function waitAndShowPlans(event) {
		modalHeading.textContent = translate['change_of_plan'][language];

		handleModalSteps(event);
	}

	function resetConfirmationModalFooter() {
		const cancelPlanChangeConfirmationButton = okButtonConfirmationModal.previousElementSibling;
		const cancelPermissionsSwitchButton =
			advanceButtonConfirmationModalSwitch.previousElementSibling;
		const xButton = advanceButtonConfirmationModalSwitch
			.closest('.discover__confirmation-modal--switch')
			.querySelector('img.discover__confirmation-modal-close');

		okButtonConfirmationModal.textContent = 'OK';
		okButtonConfirmationModal.addEventListener('click', handleModalSteps);
		okButtonConfirmationModal.classList.remove('discover__modal-close');
		okButtonConfirmationModal.removeEventListener('click', handleDiscoverModalReset);

		cancelPlanChangeConfirmationButton.classList.add('visibility-hidden');

		advanceButtonConfirmationModalSwitch.textContent = 'Confirmar';
		advanceButtonConfirmationModalSwitch.classList.remove(
			'modal__close',
			'discover__modal-close'
		);
		advanceButtonConfirmationModalSwitch.removeEventListener('click', handleDiscoverModalReset);
		advanceButtonConfirmationModalSwitch.addEventListener('click', handleModalSteps);
		advanceButtonConfirmationModalSwitch.addEventListener(
			'click',
			savePermissionsChangesToDatabase
		);

		cancelPermissionsSwitchButton.style.display = '';
		xButton.style.display = '';
	}

	function resetPlans() {
		const purchasedPlan = document.querySelector("[data-selected='true']");
		purchasedPlan.classList.add('discover__plan-box--selected');
	}

	function handleSwitchServiceReset() {
		const confirmationModalImage = document.getElementById(
			'discover-confirmation-modal-switch-image'
		);
		const confirmationModalHeading = document.getElementById(
			'discover-confirmation-modal-switch-heading'
		);
		const confirmationModalBody = document.getElementById(
			'discover-confirmation-modal-switch-body'
		);

		const successImageSrc = confirmationModalImage.src.replace('error_red', 'check_green');

		confirmationModalImage.src = successImageSrc;
		confirmationModalHeading.textContent = `${translate['exchange_confirmed'][language]}!`;
		confirmationModalBody.textContent = `${translate['soon_you_will_be_able_access_service'][language]}!`;
	}

	function showPermissionsContent(service) {
		const oldPermissionsBox = document.getElementById('discover-permissions-box-active');

		const permissionsHeader = oldPermissionsBox.previousElementSibling;
		const permissionsSpan = permissionsHeader.querySelector('span');
		const thisServiceNumberOfPermissions = Number(service.dataset.permissions);
		permissionsSpan.textContent = `${thisServiceNumberOfPermissions} ${checkNumberAgreement(
			thisServiceNumberOfPermissions
		)}`;
		const totalNumberOfPermissions = service.dataset.permissions;

		let listOfCollaborators = Array.from(service.nextElementSibling.children);
		if (listOfCollaborators.length < totalNumberOfPermissions) {
			const collaboratorsListContainer = service.nextElementSibling;
			const adminInfo = collaboratorsListContainer.nextElementSibling;
			adminInfo.dataset.admin = true;
			collaboratorsListContainer.prepend(adminInfo);
			listOfCollaborators = Array.from(service.nextElementSibling.children);
		}

		addCollaboratorBoxes();

		if (listOfCollaborators.length > 0) {
			oldPermissionsBox.classList.remove('discover__switch-service-box--empty');
			oldPermissionsBox.classList.add('discover__switch-service-box--occupied');
		} else {
			oldPermissionsBox.classList.add('discover__switch-service-box--empty');
			oldPermissionsBox.classList.remove('discover__switch-service-box--occupied');
		}

		function addCollaboratorBoxes() {
			const fragment = new DocumentFragment();

			listOfCollaborators.forEach(addBoxContent);
			oldPermissionsBox.appendChild(fragment);

			function addBoxContent(collaborator) {
				const newCollaboratorBox = document.createElement('section');
				const newNameContainer = document.createElement('div');
				const newPermissionsContainer = document.createElement('div');
				const newButton = document.createElement('button');

				newNameContainer.innerHTML = `<p class="m-0" data-name='true'>${
					collaborator.dataset.name
				} ${
					collaborator.dataset.admin == 'true'
						? `<em class="f-size-14">(${translate['administrator'][language]})</em>`
						: ''
				}</p>
				<p class="m-0 f-size-14 color-muted">${
					collaborator.dataset.schedules || 0
				} modelos configurados</p>`;
				newPermissionsContainer.innerHTML = `<img src="${
					collaborator.dataset.ticket
				}" alt="Gray Ticket"><span>${checkNumberOfPermissions()}</span>`;
				newButton.innerHTML = `<img src="${collaborator.dataset.arrow}" alt="Double arrow right"><img src="${collaborator.dataset.hover}" alt="Double arrow right hover">Trocar 1`;

				newCollaboratorBox.classList.add('discover__switch-collaborator-box');
				newNameContainer.classList.add('d-flex', 'flex-column', 'justify-content-center');
				newPermissionsContainer.classList.add('d-flex', 'align-items-center', 'gap-10');
				newButton.classList.add(
					'btn__purple',
					'f-size-14',
					'py-2',
					'px-3',
					'gap-10',
					'justify-self-end',
					'no-uppercase',
					'discover__button-switch',
					'discover__button-switch--trade'
				);
				newButton.dataset.switch = 'single';

				if (collaborator.dataset.admin == 'true') {
					newCollaboratorBox.dataset.admin = 'true';
				}

				newCollaboratorBox.dataset.user = collaborator.dataset.user;
				newCollaboratorBox.appendChild(newNameContainer);
				newCollaboratorBox.appendChild(newPermissionsContainer);
				newCollaboratorBox.appendChild(newButton);

				fragment.appendChild(newCollaboratorBox);

				function checkNumberOfPermissions() {
					if (collaborator.dataset.admin == 'true') {
						const permissionsTotal = collaborator.dataset.permissions;
						return `${permissionsTotal} ${checkNumberAgreement(permissionsTotal)}`;
					} else {
						return `1 ${translate['license'][language]}`;
					}
				}
			}
		}
	}

	function returnOnlyNumbersFromString(string) {
		return Number(string.replace(/\D/g, ''));
	}

	function checkNumberAgreement(number, extraWord) {
		if (Boolean(extraWord) == true) {
			if (extraWord == 'available')
				return number == 1
					? translate['license_available'][language]
					: translate['licenses_available'][language];
		} else {
			return number == 1 ? translate['license'][language] : translate['licenses'][language];
		}
	}

	function handleSwitchServiceButtonState(buttonsList) {
		const buttonsArray = Array.from(document.getElementsByClassName(buttonsList));
		buttonsArray.forEach((button) => {
			const buttonIcon = button.querySelector('img');
			const numberOfPermissionsText =
				button.previousElementSibling.querySelector('span').textContent;

			const numberOfPermissions = returnOnlyNumbersFromString(numberOfPermissionsText);
			if (numberOfPermissions > 0) {
				button.disabled = false;
				buttonIcon.src.includes('right')
					? (buttonIcon.src = '/static/img/double-arrow-right.svg')
					: (buttonIcon.src = '/static/img/double-arrow-left.svg');
			} else {
				button.disabled = true;
				buttonIcon.src.includes('right')
					? (buttonIcon.src = '/static/img/double-arrow-right-disabled.svg')
					: (buttonIcon.src = '/static/img/double-arrow-left-disabled.svg');
			}
		});

		checkSaveButtonState();

		function checkSaveButtonState() {
			const saveButton = document.getElementById(
				'discover-modal-no-permissions-advance-button'
			);

			const newPermissionsBoxes = Array.from(
				document.getElementsByClassName('discover__switch-permission-box')
			);

			const boxesAppearing = newPermissionsBoxes.filter(
				(box) => box.style.visibility != 'hidden'
			);

			if (boxesAppearing.length > 0) {
				saveButton.disabled = false;
				saveButton.addEventListener('click', handleSwitchServicesConfirmationModalFooter);
				// saveButton.addEventListener('click', checkWhichConfirmationMessage);
				checkWhichConfirmationMessage();
			} else {
				saveButton.disabled = true;
				saveButton.removeEventListener(
					'click',
					handleSwitchServicesConfirmationModalFooter
				);
			}

			function handleSwitchServicesConfirmationModalFooter() {
				okButtonConfirmationModal.textContent = 'Confirmar';
				okButtonConfirmationModal.dataset.show = '#discover-confirmation-modal-loading';
				okButtonConfirmationModal.dataset.hide = '#discover-confirmation-modal-step1';
				okButtonConfirmationModal.dataset.next = '#discover-confirmation-modal-step2';
			}
		}
	}

	function checkWhichConfirmationMessage() {
		const oldPermissionsBox = document.getElementById('discover-permissions-box-active');
		const activeAllPermissionsHeader = document.getElementById(
			'discover-permission-text-active'
		);
		const permissionsLeft = returnOnlyNumbersFromString(activeAllPermissionsHeader.textContent);
		const confirmationMessagePlaceholder = document.getElementById(
			'discover-confirmation-modal-message'
		);

		if (permissionsLeft == 0) {
			const nameOfTheService = document
				.getElementById('discover-dropdown-selected-placeholder')
				.querySelector('p').textContent;

			confirmationMessagePlaceholder.innerHTML = `${translate['when_confirmed_action_cant_be_undone_part_4'][language]} <strong>${nameOfTheService}</strong> ${translate['when_confirmed_action_cant_be_undone_part_5'][language]}.`;
		} else {
			const collaboratorsNames = [];
			const emptyPermissionsBoxes = Array.from(oldPermissionsBox.children).filter(
				(child) =>
					child.classList.contains('discover__empty-collaborators') == false &&
					child.dataset.admin != 'true'
			);

			emptyPermissionsBoxes.forEach(getCollaboratorsNames);

			if (collaboratorsNames.length >= 1) {
				confirmationMessagePlaceholder.innerHTML = `${
					translate['when_confirmed_action_cant_be_undone'][language]
				} ${getCollaboratorsTextAgreement()} ${
					translate['when_confirmed_action_cant_be_undone_part_2'][language]
				}.`;
			} else {
				confirmationMessagePlaceholder.textContent = `${translate['when_confirmed_action_cant_be_undone_part_3'][language]}.`;
			}

			function getCollaboratorsNames(child) {
				const numberOfPermissions = returnOnlyNumbersFromString(
					child.querySelector('span').textContent
				);

				if (numberOfPermissions == 0) {
					const collaboratorName = child.querySelector('[data-name="true"]').textContent;
					collaboratorsNames.push(collaboratorName);
				}
			}

			function getCollaboratorsTextAgreement() {
				if (collaboratorsNames.length == 1) {
					return `${
						translate['and_the_collaborator'][language]
					} <strong>${collaboratorsNames.join()}</strong> ${
						translate['will_lose'][language]
					}`;
				} else if (collaboratorsNames.length > 1) {
					return `${
						translate['and_the_collaborators'][language]
					} <strong>${collaboratorsNames.join(', ')}</strong> ${
						translate['will_lose_plural'][language]
					}`;
				}
			}
		}
	}

	function checkNewPermissionsSize() {
		const newPermissionsBox = document.getElementById('discover-permissions-box-new');

		const allChildren = newPermissionsBox.children;
		const visibleChildren = Array.from(allChildren).filter(
			(child) => child.style.visibility != 'hidden'
		);
		if (visibleChildren.length >= 2) {
			newPermissionsBox.style.overflowY = '';
		} else {
			newPermissionsBox.style.overflowY = '';
		}
	}

	function showDuplicatedElement(box) {
		const newPermissionsBox = document.getElementById('discover-permissions-box-new');

		const connectedElement = newPermissionsBox.querySelector(`[data-connection='${box.id}']`);
		connectedElement.style.visibility = '';
	}

	function createInvisibleBoxes() {
		const allCollaboratorsBoxes = Array.from(
			document.getElementsByClassName('discover__switch-collaborator-box')
		);

		allCollaboratorsBoxes.forEach(createDuplicateBox);

		function createDuplicateBox(box) {
			const newBox = document.createElement('section');
			const permissionContainer = document.createElement('div');
			const ticketIcon = document.createElement('img');
			const arrowIcon = document.createElement('img');
			const permissionText = document.createElement('span');
			const button = document.createElement('button');

			addClassToElements();
			setElementsInitialAttributes();
			setElementsConnection();
			insertElementsIntoDom();

			/***** Declarations */

			function addClassToElements() {
				newBox.classList.add('discover__switch-permission-box');
				permissionContainer.classList.add('d-flex', 'align-items-center', 'gap-10');
				button.classList.add(
					'button__light-gray',
					'f-size-14',
					'py-2',
					'px-3',
					'gap-10',
					'no-uppercase',
					'discover__button-switch',
					'discover__button-switch--return'
				);
			}

			function setElementsInitialAttributes() {
				ticketIcon.src = box.querySelector('img').src;

				button.innerHTML =
					"<img src='/static/img/double-arrow-left.svg' alt='Double arrow left'>Devolver 1";
			}

			function setElementsConnection() {
				box.id = '_' + Math.random().toString(36).substr(2, 9);
				newBox.dataset.connection = box.id;
			}

			function insertElementsIntoDom() {
				const newPermissionsBox = document.getElementById('discover-permissions-box-new');

				permissionContainer.appendChild(ticketIcon);
				permissionContainer.appendChild(permissionText);
				button.appendChild(arrowIcon);
				newBox.appendChild(permissionContainer);
				newBox.appendChild(button);

				newBox.style.visibility = 'hidden';
				newPermissionsBox.style.overflowY = 'hidden';
				newPermissionsBox.appendChild(newBox);
			}
		}
	}

	function showErrorMessage() {
		const confirmationModalImage = document.getElementById(
			'discover-confirmation-modal-switch-image'
		);
		const confirmationModalHeading = document.getElementById(
			'discover-confirmation-modal-switch-heading'
		);
		const confirmationModalBody = document.getElementById(
			'discover-confirmation-modal-switch-body'
		);
		const errorImageSrc = confirmationModalImage.src.replace('check_green', 'error_red');

		confirmationModalImage.src = errorImageSrc;

		confirmationModalHeading.textContent = `${translate['unable_complete_service_exchange'][language]}!`;
		confirmationModalBody.textContent = `${translate['please_try_again_later'][language]}!`;
	}

	function getTotalNumberOfPermissions(updateHeader = false) {
		const bothHeaders = Array.from(
			document.getElementsByClassName('discover__switch-service-permission')
		);
		const totalPermissions = [];

		bothHeaders.forEach((header) => {
			const headerSpan = header.querySelector('span');
			const targetBox = header.nextElementSibling;
			const allChildren = Array.from(targetBox.children);
			let count = 0;
			allChildren.forEach((child) => {
				if (child.classList.contains('discover__empty-collaborators') == false) {
					const permissionSpan = child.querySelector('span');
					const numberOfPermissions = returnOnlyNumbersFromString(
						permissionSpan.textContent
					);

					if (child.style.visibility != 'hidden') {
						count += numberOfPermissions;
					}
				}
			});

			totalPermissions.push(count);

			if (updateHeader == true) {
				headerSpan.textContent = `${count} ${checkNumberAgreement(count)}`;
			}
		});

		return totalPermissions;
	}

	function updatePermissionsBox(subtractedBox, type = 'all') {
		if (type == 0) {
			type = 'all';
		}

		const subtractedBoxSpan = subtractedBox.querySelector('span');
		const subtractedBoxNumber = returnOnlyNumbersFromString(subtractedBoxSpan.textContent);
		const subtractedBoxNewNumber = subtractedBoxNumber >= 1 ? subtractedBoxNumber - 1 : 0;

		let otherBox;

		if (subtractedBox.classList.contains('discover__switch-permission-box')) {
			otherBox = document.getElementById(subtractedBox.dataset.connection);
		} else {
			const newPermissionsBox = document.getElementById('discover-permissions-box-new');

			otherBox = newPermissionsBox.querySelector(`[data-connection="${subtractedBox.id}"]`);
		}

		const otherBoxSpan = otherBox.querySelector('span');
		const otherBoxNumber = returnOnlyNumbersFromString(otherBoxSpan.textContent);

		if (subtractedBoxNumber > 1 && type == 'all') {
			const otherBoxNewNumber = otherBoxNumber + subtractedBoxNumber;
			subtractedBoxSpan.textContent = `0 ${checkNumberAgreement(0)}`;
			otherBoxSpan.textContent = `${otherBoxNewNumber} ${checkNumberAgreement(
				otherBoxNewNumber
			)}`;
		} else {
			const otherBoxNewNumber = otherBoxNumber + 1;

			subtractedBoxSpan.textContent = `${subtractedBoxNewNumber} ${checkNumberAgreement(
				subtractedBoxNewNumber
			)}`;

			otherBoxSpan.textContent = `${otherBoxNewNumber} ${checkNumberAgreement(
				otherBoxNewNumber
			)}`;
		}
	}

	function hideTargetServiceInDropdown() {
		dropdownContent = document.getElementById('discover-switch-service-dropdown');
		const targetServiceName = document.querySelector('.discover__switch-service-new').dataset
			.service;
		const targetServiceDropdownItem = dropdownContent.querySelector(
			`[data-service='${targetServiceName}']`
		);

		if (
			Boolean(targetServiceDropdownItem) == true &&
			targetServiceDropdownItem.style.display != 'none'
		) {
			targetServiceDropdownItem.style.display = 'none';
		}
	}

	async function addServiceFromDiscover(event) {
		const modal = event.target.closest('.discover__inner-modal--add-service');

		const allModalScreens = modal.querySelectorAll('.discover__inner-modal--section');
		const contentScreen = allModalScreens[0];
		const loadingScreen = allModalScreens[1];
		const feedbackScreen = allModalScreens[2];

		const modalFooter = modal.querySelector('footer');
		const cancelButton = modalFooter.querySelectorAll('button')[0];
		const confirmButton = modalFooter.querySelectorAll('button')[1];

		contentScreen.classList.add('d-none');
		loadingScreen.classList.remove('d-none');

		const service = modal.dataset.service;
		const quantity = Number(modal.querySelector('.services-count').textContent);
		const isShowcase = modal.dataset.showcase == 'true';

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				service,
				quantity,
			}),
		};
		const response = await fetch('/discover/add', settings);

		confirmButton.removeEventListener('click', addServiceFromDiscover);
		if (response.ok != true) {
			const convertedResponse = await response.json();

			const errorModal = feedbackScreen;
			const modalIcon = errorModal.querySelector('img');
			const errorImageSrc = modalIcon.src.replace('check_green', 'error_red');
			const modalHeading = errorModal.querySelector('p >  strong');
			const modalText = errorModal.querySelectorAll('p')[1];

			const errorMessageWasSent = Boolean(convertedResponse['error']);

			modalIcon.src = errorImageSrc;
			modalHeading.textContent = translate['unable_add_service'][language];

			if (errorMessageWasSent) {
				modalText.textContent = convertedResponse['error'];
			} else {
				modalText.textContent = translate['unable_add_service_text'][language];
			}
		}
		confirmButton.addEventListener('click', reloadPage);
		cancelButton.style.visibility = 'hidden';
		confirmButton.textContent = 'OK';

		if (isShowcase) {
			const feedbackModalContent = feedbackScreen.querySelector('.jsShowcase');
			feedbackModalContent.innerHTML = `<p class="m-0"><strong>Serviço solicitado sucesso!</strong></p><p>Nossa equipe irá entrar em contato em até 24h. Em breve você poderá utilizá-lo.</p>`;
		}

		loadingScreen.classList.add('d-none');
		feedbackScreen.classList.remove('d-none');
		feedbackScreen.classList.add('d-flex');
	}

	function handleLicensesManipulation(event) {
		const targetButton = event.target;
		const buttonsContainer = targetButton.closest('.discover__modal-success-btn-container');
		const currentClientPlan = buttonsContainer.dataset.plan;
		const clientIsInTrial = currentClientPlan.includes('trial');

		const numberOfPermissionsElement = buttonsContainer.querySelector('span');

		let count;

		const limit = Number(
			event.target.closest('.discover__modal-success-btn-container').dataset.limit
		);

		if (targetButton.dataset.manipulation == 'decrease') {
			const currentNumberOfPermissions = Number(
				targetButton.nextElementSibling.querySelector('.services-count').textContent
			);
			count = currentNumberOfPermissions - 1;
		} else if (targetButton.dataset.manipulation == 'increase') {
			const currentNumberOfPermissions = Number(
				targetButton.previousElementSibling.querySelector('.services-count').textContent
			);

			if (currentNumberOfPermissions < limit || clientIsInTrial) {
				count = currentNumberOfPermissions + 1;
			} else {
				const errorMessage = `${translate['you_have_reached_limit_available_licenses'][language]}: <strong>${limit}</strong>`;
				return Swal.fire('Oops..', errorMessage, 'error');
			}
		}

		checkIfButtonIsDisabled(targetButton, limit, clientIsInTrial);

		if (count != 0) {
			if (count >= 10) {
				numberOfPermissionsElement.innerHTML = `<span class="services-count">${count}</span> ${checkNumberAgreement(
					count
				)}`;
			} else {
				numberOfPermissionsElement.innerHTML = `<span class="services-count">0${count}</span> ${checkNumberAgreement(
					count
				)}`;
			}
		}

		function checkIfButtonIsDisabled(button, limit, clientIsInTrial = false) {
			const increaseButton =
				button.dataset.manipulation == 'increase'
					? button
					: button.parentElement.querySelector("[data-manipulation='increase' ]");
			const decreaseButton =
				button.dataset.manipulation == 'decrease'
					? button
					: button.parentElement.querySelector("[data-manipulation='decrease' ]");

			if (count == 1) {
				decreaseButton.disabled = true;
				if (count < limit) {
					increaseButton.disabled = false;
				} else {
					increaseButton.disabled = true;
				}
			} else if (count == limit && clientIsInTrial) {
				increaseButton.disabled = true;
				decreaseButton.disabled = false;
			} else {
				decreaseButton.disabled = false;
				increaseButton.disabled = false;
			}
		}
	}

	async function warnUserWhenServiceIsFixed(event) {
		const targetButton = event.currentTarget;

		const automationName = targetButton.closest('.discover__service-box').dataset.service;
		const oldInnerHtml = targetButton.innerHTML;

		targetButton.innerHTML =
			"<div class='spinner-border text-dark spinner-border-sm' role='status'><span class='sr-only'>Loading...</span></div>";
		targetButton.classList.add('w-80', 'justify-content-center');

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				automation: automationName,
			}),
		};

		const response = await fetch('discover/interested_maintenance', settings);

		targetButton.classList.remove('w-80', 'justify-content-center');

		if (response.ok == true && response.redirected == false) {
			const buttonIsAlreadyClicked = Number(targetButton.dataset.clicked) == 1;

			if (buttonIsAlreadyClicked) {
				targetButton.innerHTML = translate['notify_me_when_available'][language];

				targetButton.dataset.clicked = 0;
			} else {
				targetButton.innerHTML = `<img src=${targetButton.dataset.image} alt='Check mark Icon'/> ${translate['you_will_be_notified'][language]}`;

				targetButton.dataset.clicked = 1;
			}
			targetButton.classList.toggle('gap-5');
		} else {
			targetButton.innerHTML = oldInnerHtml;
			const convertedResponse = await response.json();

			const errorMessage =
				convertedResponse['error'] || translate['error_saving_interest'][language];

			Swal.fire('Oops..', errorMessage, 'error');
		}
	}
});

function removeOpenModalAttributes(button) {
	button.classList.remove('modal__open-button');
	delete button.dataset.background;
	delete button.dataset.close;
	delete button.dataset.modal;
}

function reloadPage() {
	location.assign(location);
}
