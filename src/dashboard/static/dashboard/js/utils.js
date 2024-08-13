document.addEventListener('DOMContentLoaded', () => {
	/**********************  CONSTANTS ********************************/

	// Modal

	loadAllModalEvents();
	const settingsModalBackground = document.getElementById('modalsettings');
	const modalEventDelegator = document.querySelector('.modal__background--discover');
	const plansSwitchButtons = Array.from(document.getElementsByClassName('plan__switch'));
	// Filter
	loadAllFilterBtns();
	// Dropdowns
	loadAllDropdownArrows();
	// Permissions
	const allButtonsToManipulatePermissions = Array.from(
		document.getElementsByClassName('btn__manipulate-permissions')
	);

	/**********************  EXECUTABLE CODE ************************/
	document.addEventListener('click', handleDocumentOutsideClick);

	settingsModalBackground?.addEventListener('click', handleClickOutsideModal);

	plansSwitchButtons.forEach((slider) =>
		slider.addEventListener('click', handlePlanSwitchButton)
	);

	modalEventDelegator?.addEventListener('click', handleDiscoverModalEventsDelegation);

	document.addEventListener('click', (event) => {
		if (event.target.classList.contains('btn__pill--dashboard-processes')) {
			handleFilters(event);
		}
	});

	$('.modal').on('hidden.bs.modal', () => (document.querySelector('html').style.overflow = ''));
	$('.modal').on(
		'show.bs.modal',
		() => (document.querySelector('html').style.overflow = 'hidden')
	);

	checkAndOpenModalWithUrlInfo();

	/**********************  DECLARATIONS ****************************/

	function handleDocumentOutsideClick(event) {
		const clickTarget = event.target;
		const openPopup = document.querySelector('.crew__popup-menu-container--show');
		const settingsModal = document.getElementById('modalsettings');
		const discoverModal = document.querySelector('.modal__background--discover');

		if (
			openPopup &&
			clickTarget.closest('div') !== null &&
			!clickTarget.closest('div').className.includes('crew__popup-menu')
		) {
			openPopup.classList.toggle('crew__popup-menu-container--show');
		} else if (Boolean(settingsModal) == true && settingsModal.style.display == 'block') {
			const languageDropdown = document.getElementById('language-dropdown-menu');
			const isLanguageDropdownOpen = languageDropdown?.dataset.showing;
			const selectedLanguage = document.getElementById('selected-language-dropdown');
			const isClickOutsideLanguageContainer =
				clickTarget.closest('div') !== null &&
				!clickTarget.closest('div').classList.contains('language__dropdown-menu') &&
				clickTarget.id != selectedLanguage?.id &&
				clickTarget.closest('button')?.id != 'selected-language-dropdown';

			if (isLanguageDropdownOpen == 'true' && isClickOutsideLanguageContainer) {
				languageDropdown.style.display = 'none';
			}
		} else if (discoverModal?.style.display == 'flex') {
			const arrowDropdownButton = document.getElementById('open-hired-services');
			const discoverServicesDropdown = document.getElementById(
				'discover-switch-service-dropdown'
			);
			let isServicesDropdownOpen = discoverServicesDropdown?.dataset.showing;

			const isClickOutsideServicesDropdown = clickTarget.closest('div') !== null;

			if (isServicesDropdownOpen == 'true' && isClickOutsideServicesDropdown) {
				const srcNow = arrowDropdownButton.src;

				discoverServicesDropdown.style.display = 'none';
				arrowDropdownButton.src = arrowDropdownButton.dataset.image;
				arrowDropdownButton.dataset.image = srcNow;
				discoverServicesDropdown.dataset.showing = false;
			}
		}
	}

	/**********************  HELPER DECLARATIONS ****************************/
	function handlePlanSwitchButton(event) {
		event.preventDefault();

		let targetSwitch = event.target;
		if (targetSwitch.tagName != 'LABEL') {
			targetSwitch = targetSwitch.closest('label');
		}

		const input = targetSwitch.querySelector('input');
		isInputChecked = input.checked;
		isInputChecked ? (input.checked = false) : (input.checked = true);

		const pricePlaceholder = targetSwitch
			.closest('.single__plan-box')
			.querySelector('.single__plan-box--price');
		const price = pricePlaceholder.querySelector('strong');
		const oldPrice = price.textContent;

		const anualPrice = targetSwitch
			.closest('.single__plan-box')
			.querySelector('.single__plan-box--anual-price');
		const oldAnualPrice = anualPrice.textContent;

		price.textContent = pricePlaceholder.dataset.price;
		pricePlaceholder.dataset.price = oldPrice;

		anualPrice.textContent = anualPrice.dataset.price;
		anualPrice.dataset.price = oldAnualPrice;

		const registrationPlanContainer = targetSwitch.closest('.plans');

		if (
			input.checked == true &&
			Boolean(registrationPlanContainer) == true &&
			registrationPlanContainer.dataset.value != 'business'
		) {
			const oldDataValue = registrationPlanContainer.dataset.value;
			registrationPlanContainer.dataset.value = `${oldDataValue}_plus`;
		} else if (
			input.checked == false &&
			Boolean(registrationPlanContainer) == true &&
			registrationPlanContainer.dataset.value != 'business'
		) {
			const newDatasetValue = registrationPlanContainer.dataset.value.replace('_plus', '');
			registrationPlanContainer.dataset.value = newDatasetValue;
		}
	}

	/**********************  EVENT DELEGATIONS ****************************/

	function handleDiscoverModalEventsDelegation(event) {
		const target = event.target;

		if (target.classList.contains('modal__open-button')) {
			handleModalOpen(event);
		} else if (target.id == 'ok-button-discover-modal-success') {
			handleModalClose(event);
			target.dataset.close = '';
		} else if (target.classList.contains('arrow__button--dropdown')) {
			handleBoxDropdown(event);
		} else {
			handleDocumentOutsideClick(event);
		}
	}

	function checkAndOpenModalWithUrlInfo() {
		const modal = new URL(window.location.href).searchParams.get('modal');

		if (!modal) return;

		const modalId = JSON.parse(modal);

		$(`#${modalId}`).modal('show');
	}
});

const handleClickOutsideModal = (event) => {
	const html = document.querySelector('html');
	let targetModalBackground = event.target;
	if (targetModalBackground.classList.contains('modal__background')) {
		html.style.overflow = '';
		targetModalBackground.style.display = 'none';

		if (targetModalBackground.id == 'modalsettings') {
			resetSettingsModal();
		}
	}
};

function getAllPermittedUsers(btn) {
	let permissions_box = btn.closest('.permissions-box__container');
	let allPermitted = permissions_box.querySelectorAll(
		'.permission-box__content--collaborator .single_permission_box'
	);
	return allPermitted;
}

function resetSettingsModal() {
	const modal = document.getElementById('modalsettings');
	const allNavButtons = Array.from(document.getElementsByClassName('tab-button'));
	const oldActiveContent = Array.from(
		document.getElementsByClassName('active-settings__content')
	);
	const submitButton = modal.querySelector('#modalsettings .submit_profile');

	allNavButtons.forEach((button) => button.classList.remove('tab-button--active'));

	oldActiveContent.forEach((content) => content.classList.remove('active-settings__content'));
	document.getElementById('profile-content').classList.add('active-settings__content');

	submitButton.disabled = true;

	cleanProfileTab();
	cleanSettingsCrewForm();

	function cleanProfileTab() {
		const profileNavButton = modal.querySelector('#profile');

		const profileForm = document.getElementById('settings-profile-form');

		const passwordScreen = document.getElementById('new-password-screen');
		const passwordForm = modal.querySelector('.profile__change-password--form');
		const allSuccessPasswordFeedbacks = Array.from(
			document.getElementsByClassName('profile-password--success')
		);
		const allErrorPasswordFeedbacks = Array.from(
			document.getElementsByClassName('profile-password--error')
		);

		const openInputs = Array.from(
			document.getElementsByClassName('settings__edit-container')
		).filter((item) => item.dataset.open == 'true');
		openInputs.forEach((input) => {
			const cancelIcon = input.querySelector('.settings__clear--icon');
			const oldPTagHtml = input.querySelector('input').value.trim();

			input.style.display = 'none';

			input.dataset.open = false;

			const targetTagP = document.getElementById(cancelIcon.dataset.paragraph);

			targetTagP.style.display = 'flex';
			targetTagP.querySelector('span').innerHTML = oldPTagHtml;
		});

		profileNavButton.classList.add('tab-button--active');

		profileForm.style.display = '';

		passwordScreen.style.display = '';

		passwordForm.reset();

		allSuccessPasswordFeedbacks.forEach((item) => (item.style.display = ''));
		allErrorPasswordFeedbacks.forEach((item) => (item.style.display = ''));
	}

	function cleanSettingsCrewForm() {
		const crewForm = document.getElementById('crew-list-settings').closest('form');
		const excludeAllCrewButton = document.getElementById('crew-remove-selected');
		const excludeAllCrewButtonIcon = excludeAllCrewButton.querySelector('img');

		crewForm.reset();
		excludeAllCrewButton.disabled = true;
		excludeAllCrewButtonIcon.src = excludeAllCrewButtonIcon.dataset.disabled;
	}
}

function checkIfEmailIsPersonal(email) {
	const checkIfItIsBusinessEmail = (domain) => !email.includes(domain);
	const forbiddenDomains = [
		'gmail',
		'yahoo',
		'hotmail',
		'aol',
		'live',
		'outlook',
		'protonmail',
		'dukeoo',
	];

	return !forbiddenDomains.every(checkIfItIsBusinessEmail);
}

const loadAllDropdownArrows = () => {
	const allDropdownArrows = Array.from(
		document.getElementsByClassName('arrow__button--dropdown')
	);
	allDropdownArrows.forEach((dropdownBtn) =>
		dropdownBtn.addEventListener('click', handleBoxDropdown)
	);
};

const handleBoxDropdown = (event) => {
	const targetButton = event.target;

	if (targetButton.dataset.select == 'true') {
		event.stopPropagation();
		const discoverDropdownContent = document.getElementById('discover-switch-service-dropdown');

		changeDropdownVisibility(discoverDropdownContent, 'flex');

		discoverDropdownContent.dataset.showing == 'false' ||
		!discoverDropdownContent.dataset.showing
			? (discoverDropdownContent.dataset.showing = 'true')
			: (discoverDropdownContent.dataset.showing = 'false');
	} else {
		const targetDropdownContent = targetButton.closest('header').nextElementSibling;

		if (targetDropdownContent.classList.contains('service__dropdown-info')) {
			changeDropdownVisibility(targetDropdownContent, 'flex');
		} else if (targetDropdownContent.classList.contains('permission-box__content')) {
			changeDropdownVisibility(targetDropdownContent, 'block');
		} else if (targetDropdownContent.classList.contains('help--center-box__content')) {
			changeDropdownVisibility(targetDropdownContent, 'block');
		} else if (targetDropdownContent.classList.contains('standard--center-box__content')) {
			changeDropdownVisibility(targetDropdownContent, 'none');
			if (document.querySelector('.standard--center-box__content').style.display === 'none') {
				document.querySelector('.standard--min-box__content').style.display = 'block';
			} else {
				document.querySelector('.standard--min-box__content').style.display = 'none';
			}
		} else if (targetDropdownContent.classList.contains('schedule_edit_box__content')) {
			changeDropdownVisibility(targetDropdownContent, 'block');
		}
	}

	function changeDropdownVisibility(element, display) {
		if (element.style.display == display) {
			element.style.display = '';
		} else {
			element.style.display = display;
		}
		const srcNow = targetButton.dataset.image;
		targetButton.dataset.image = targetButton.src;
		targetButton.src = srcNow;
	}
};

const loadAllModalEvents = () => {
	const allModalsBackgrounds = Array.from(document.getElementsByClassName('modal__background'));
	allModalsBackgrounds.forEach((modalBackground) =>
		modalBackground.addEventListener('click', handleClickOutsideModal)
	);

	const allButtonsToOpenModal = Array.from(document.getElementsByClassName('modal__open-button'));
	allButtonsToOpenModal.forEach((button) => button.addEventListener('click', handleModalOpen));

	const allButtonsToCloseModal = Array.from(document.getElementsByClassName('modal__close'));
	allButtonsToCloseModal.forEach((button) => button.addEventListener('click', handleModalClose));
};

const handleModalClose = (event) => {
	const targetBtn = event.target;
	const targetModal = document.querySelectorAll(targetBtn.dataset.close);

	targetModal.forEach((modal) => (modal.style.display = ''));
	if (targetBtn.dataset.close?.includes('modalsettings')) {
		resetSettingsModal();
	} else {
		document.querySelector('html').style.overflow = '';
	}
};

const checkNumberAgreement = (number) => {
	return number == 1 ? translate['license'][language] : translate['licenses'][language];
};

const handleModalOpen = (event) => {
	let targetBtn = event.target;
	if (Boolean(targetBtn.dataset.modal) == false) {
		targetBtn = targetBtn.closest('button') || targetBtn.closest('.modal__open-button');
	}
	const innerModalsToClose = targetBtn.dataset.close;
	let targetModal = targetBtn.dataset.modal;
	const targetModalBackground = targetBtn.dataset.background;

	if (targetBtn.classList.contains('btn__purple--permissions')) {
		const permissionsModalHeading = document.getElementById('permissions-modal-heading');
		const form = document.querySelector('.permissions__modal-form');
		const oldActives = document.querySelectorAll(
			'.permissions__modal-email--list .permissions__modal-email--active'
		);

		permissionsModalHeading.innerText = `${targetBtn.dataset.heading} ${targetBtn.dataset.service}`;
		form.reset();
		oldActives.forEach((item) => item.classList.remove('permissions__modal-email--active'));

		document.getElementById('permission_automation_name').value =
			targetBtn.dataset.automation_name;

		let permissions_box = targetBtn.closest('.permissions-box__container');

		let howmany_permissions_available =
			permissions_box.querySelector('.permissions_total').textContent;

		document.querySelector(
			'footer .licenses__limit'
		).innerHTML = `<span class="howmany_permissions">${howmany_permissions_available}</span> ${checkNumberAgreement(
			Number(howmany_permissions_available)
		)}`;

		updateUsersWithPermissionsOnModal();

		function updateUsersWithPermissionsOnModal() {
			let allPermissions = getAllPermittedUsers(targetBtn);
			let all_users_in_permissions = [];
			allPermissions.forEach((single_user_permission) => {
				all_users_in_permissions.push(single_user_permission.dataset.user_id);
			});

			const allClientCollaborators = Array.from(
				document.getElementsByClassName('permissions__modal-email--item')
			);
			const submitButton = document.querySelector(`${targetModal} .permissions__modal--btn`);
			const crewWithLicenses = [];
			allClientCollaborators
				.filter((item) => all_users_in_permissions.includes(item.dataset.user))
				.forEach((collaborator) => {
					collaborator.classList.add('permissions__modal-email--active');
					crewWithLicenses.push(collaborator.dataset.user);
				});
			submitButton.dataset.users = crewWithLicenses;
		}
	} else if (targetBtn.classList.contains('discover__modal--btn-hire')) {
		const modal = document.querySelector(targetModal);

		handleHireServiceModalOpen(targetBtn, modal);
	} else if (targetBtn.classList.contains('crew__edit', 'settings')) {
		// is edit btn, need to update infos
		let user_div = targetBtn.closest('.crew__list--item');
		// let user_id = targetBtn.closest('[data-user_id]').dataset.user_id;
		let name = user_div.querySelector('.topinfo_checkbox').innerHTML;
		let email = user_div.querySelector('.bottominfo_checkbox').innerHTML;
		let services_json = {};
		let services_string = user_div.querySelector('.services_by_user');
		if (services_string !== null) {
			services_json = JSON.parse(services_string.value);
		}
		updateUsersOnEditModal(name, email, services_json);

		function updateUsersOnEditModal(name, email, services_json) {
			let crew_modal = document.getElementById('crew-edit-modal');
			crew_modal.querySelector('#p-crew-name').innerHTML = name;
			crew_modal.querySelector('#p-crew-email').innerHTML = email;
			let services_to_update = ``;
			Object.keys(services_json).map((key) => {
				services_to_update += generateCrewService(
					services_json[key]['display_name'],
					services_json[key]['howmany_models_configured']
				);
			});
			crew_modal.querySelector('.services_crew_modal').innerHTML = services_to_update;
		}

		function generateCrewService(title, display_name, howmany_models_configured) {
			return `
				<div class="service__dropdown service__dropdown--crew">
					<div class="d-flex">
						<img
							src="static/dashboard/img/services-icon.svg"
							alt="Services icon"
						/>

						<div class="d-flex flex-column margin-left-15">
							<p class="f-size-14 m-0">
								${display_name}
							</p>
							<p class="f-size-12 m-0 color-muted">
								${howmany_models_configured} ${
				howmany_models_configured == 1
					? translate['model_configured'][language]
					: translate['models_configured'][language]
			}
							</p>
						</div>
					</div>
				</div>
			`;
		}
	} else if (
		targetBtn.classList.contains('crew__exclude--settings') ||
		targetBtn.closest('button')?.classList.contains('crew__exclude--settings')
	) {
		const modalHeader = document.querySelector(`${targetModal} header span`);
		const modalText = document.querySelector(`${targetModal} .crew__modal--text`);
		let datasetTarget = targetBtn.classList.contains('crew__exclude--settings')
			? targetBtn
			: targetBtn.closest('button');

		const whichExcludeType = datasetTarget.dataset.exclude;
		const buttonToExcludeCrew = document
			.querySelector(targetModal)
			.querySelector('.crew__modal--btn');

		modalText.previousElementSibling.style.display = '';
		modalText.classList.remove('d-flex', 'align-items-center', 'gap-16');

		if (whichExcludeType == 'single') {
			const collaboratorName = targetBtn
				.closest('li')
				.querySelector('.topinfo_checkbox').textContent;
			modalHeader.textContent = `${translate['exclude'][language]} ${collaboratorName}?`;
			modalText.innerHTML = `${translate['do_you_want_to_exclude_collaborator_1'][language]} ${collaboratorName} ${translate['do_you_want_to_exclude_collaborator_2'][language]} <strong>${translate['do_you_want_to_exclude_collaborator_3'][language]}</strong> ${translate['do_you_want_to_exclude_collaborator_4'][language]}.`;
			buttonToExcludeCrew.textContent = translate['delete_collaborator'][language];
			buttonToExcludeCrew.dataset.user = datasetTarget.closest(
				'.crew__popup-menu-container'
			).dataset.user_id;
			document.querySelector(targetModal).dataset.user = collaboratorName;
		} else {
			const checkedCollaborators = Array.from(
				targetBtn.nextElementSibling.querySelector('#crew-list-settings').children
			).filter((child) => child.querySelector('input[type=checkbox]').checked);
			const numberOfCollaboratorsToExclude = checkedCollaborators.length;

			if (numberOfCollaboratorsToExclude == 1) {
				const whichCollaborator =
					checkedCollaborators[0].querySelector('.topinfo_checkbox').textContent;

				modalHeader.textContent = `${translate['exclude'][language]} ${whichCollaborator}?`;
				modalText.innerHTML = `${translate['do_you_want_to_exclude_collaborator_1'][language]} ${whichCollaborator} ${translate['do_you_want_to_exclude_collaborator_2'][language]} <strong>${translate['do_you_want_to_exclude_collaborator_3'][language]}</strong> ${translate['do_you_want_to_exclude_collaborator_4'][language]}.`;
			} else {
				modalHeader.textContent = `${translate['exclude'][language]} ${translate['employees_capitalized'][language]}?`;
				modalText.textContent = translate['confirm_exclude_settings_crew'][language];
				buttonToExcludeCrew.textContent = translate['delete_collaborator_plural'][language];
			}
		}

		buttonToExcludeCrew.dataset.exclude = whichExcludeType;
	} else if (targetBtn.classList.contains('discover__add-service-modal')) {
		const modal = document.querySelector(targetModal);
		if (modal.querySelector('#discover-heading')) {
			const card = targetBtn.closest('.discover__service-box');
			const service = targetBtn.dataset.service || card.dataset.service;
			const heading =
				card?.querySelector('p').textContent ||
				document.querySelector('.discover-service__header h1').textContent;
			const modalHeadingPlaceholder = modal.querySelector('#discover-heading');
			const isShowcase = card.dataset.showcase == 'true';
			modalHeadingPlaceholder.textContent = ` ${heading} `;
			modal.dataset.service = service;
			modal.dataset.showcase = isShowcase ? 'true' : 'false';

			cleanAddServiceModal();
		}
		function cleanAddServiceModal() {
			const buttonsContainer = modal.querySelector('.discover__modal-success-btn-container');
			const subtractButton = buttonsContainer.querySelector('[data-manipulation="decrease"]');
			const increaseButton = buttonsContainer.querySelector('[data-manipulation="increase"]');
			const numberOfLicensesElement = subtractButton.nextElementSibling;

			const licensesLimit = Number(
				buttonsContainer.closest('.discover__modal-success-btn-container').dataset.limit
			);

			subtractButton.disabled = true;

			if (licensesLimit > 1) {
				increaseButton.disabled = false;
			} else {
				increaseButton.disabled = true;
			}

			numberOfLicensesElement.innerHTML = `<span class="services-count">01</span> ${translate['license'][language]} `;
		}
	}

	if (Boolean(innerModalsToClose) == true) {
		closeAllOtherModals(innerModalsToClose);
	}
	onModalOpen(targetModalBackground, targetModal);

	function onModalOpen(backgroundModal, targetModal) {
		const modalBackground = document.querySelector(backgroundModal);
		const modalToOpen = document.querySelector(targetModal);

		modalBackground.style.display = 'flex';

		if (modalToOpen.classList.contains('discover__inner-modal--hire')) {
			modalToOpen.style.display = 'grid';
		} else {
			modalToOpen.style.display = 'flex';
			modalToOpen.style.flexDirection = 'column';
		}

		document.querySelector('html').style.overflow = 'hidden';
	}

	function closeAllOtherModals(modals) {
		const allModals = Array.from(document.querySelectorAll(modals));

		allModals.forEach((modal) => (modal.style.display = ''));
	}
};

const loadAllFilterBtns = () => {
	const allFilterButtons = Array.from(document.getElementsByClassName('btn__pill'));
	allFilterButtons.forEach((filterButton) =>
		filterButton.addEventListener('click', handleFilters)
	);
};

const handleFilters = (event) => {
	const targetButton = event.target.closest('.btn__pill');
	const whichFilterButtonsGroup = Array.from(
		document.getElementsByClassName(targetButton.dataset.class)
	);
	const whichElementsToQuery = Array.from(
		document.getElementsByClassName(targetButton.dataset.query)
	);

	handleActiveState(whichFilterButtonsGroup);
	handleFilterQuery(whichElementsToQuery);

	function handleActiveState(filterButtonsGroup) {
		filterButtonsGroup.forEach((btn) => btn.classList.remove('btn__pill--active'));
		targetButton.classList.add('btn__pill--active');
	}

	function handleFilterQuery(targetElementsClass) {
		const isDashboardProcessesFilters = targetButton.classList.contains(
			'btn__pill--dashboard-processes'
		);

		const targetDataset = targetButton.dataset.type;

		if (isDashboardProcessesFilters) {
			queryDashboardProcessesFilters();
		} else {
			queryRegularFilters();
		}
		function queryRegularFilters() {
			targetElementsClass.forEach((element) => {
				if (targetButton.dataset.tohide) {
					const parent = element.closest(`.${targetButton.dataset.tohide}`);
					if (targetDataset == 'allFilters') {
						parent.style.display = '';
					} else if (element.dataset.type != targetDataset) {
						parent.style.display = 'none';
					} else {
						parent.style.display = '';
					}
				} else {
					if (targetDataset == 'allFilters') {
						element.style.display = '';
					} else if (element.dataset.type != targetDataset) {
						element.style.display = 'none';
					} else {
						element.style.display = '';
					}
				}
			});
		}

		function queryDashboardProcessesFilters() {
			const trimmedTargetButtonText = targetButton.textContent.trim();

			// Query for completed processes
			if (trimmedTargetButtonText == translate['data_complete'][language]) {
				targetElementsClass.forEach((element) => {
					if (targetButton.dataset.tohide) {
						const completed = element
							.querySelector('[data-completed')
							?.getAttribute('data-completed');

						if (completed == 'True') {
							element.style.display = '';
						} else {
							element.style.display = 'none';
						}
					} else {
						if (element.dataset.completed == 'True') {
							element.style.display = '';
						} else {
							element.style.display = 'none';
						}
					}
				});
				// Query for not completed processes
			} else if (trimmedTargetButtonText == translate['incomplete_data'][language]) {
				targetElementsClass.forEach((element) => {
					if (targetButton.dataset.tohide) {
						const completed = element
							.querySelector('[data-completed')
							?.getAttribute('data-completed');
						if (completed == 'False') {
							element.style.display = '';
						} else {
							element.style.display = 'none';
						}
					} else {
						if (element.dataset.completed == 'False') {
							element.style.display = '';
						} else {
							element.style.display = 'none';
						}
					}
				});
			} else {
				// Query for processes areas
				queryRegularFilters();
			}
		}
	}
};

const loadSingleTabScripts = (table = '') => {
	if (table == 'manage_permissions') {
		loadManagePermissionsScript();
		loadAllDropdownArrows();
		loadAllModalEvents();
		loadAllFilterBtns();
		loadCrewPopManagePermission();
	} else if (table == 'processes_history') {
		loadAllModalEvents();
		loadAllFilterBtns();
	} else if (table == 'my_services') {
		loadAllFilterBtns();
	}
};

const handleHireServiceModalOpen = (clickedButton, targetModal) => {
	if (clickedButton.dataset.admin == 'True') {
		const serviceBox = clickedButton.closest('.discover__service-box');
		const serviceName = serviceBox?.querySelector('p').innerText;
		const advanceButton = targetModal.querySelector('button[data-step="advance"]');
		const isShowcase = serviceBox?.dataset.showcase == 'true';

		targetModal.dataset.service = serviceBox
			? serviceBox.dataset.service
			: clickedButton.dataset.service;

		advanceButton.disabled = true;

		if (serviceBox) {
			const headingPlaceholder = Array.from(
				document.getElementsByClassName('discover__inner-modal--heading')
			);

			targetModal.dataset.showcase = isShowcase;

			headingPlaceholder.forEach(
				(heading) =>
					(heading.innerHTML = `${translate['add'][language]} <strong>${serviceName}</strong> ${translate['to_your_plan'][language]}?`)
			);
		}
	}
};
