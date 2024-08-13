document.addEventListener('DOMContentLoaded', () => {
	/**********************  CONSTANTS ********************************/
	// Used in more than in one tab
	const settingsTabs = Array.from(document.getElementsByClassName('tab-button'));
	const allSchedulesContainer = Array.from(document.getElementsByClassName('allschedules'));
	loadCrewPopManagePermission();

	// Advanced
	const selectedLanguage = document.getElementById('selected-language-dropdown');
	const backToAdvancedButton = Array.from(document.getElementsByClassName('advanced__back-btn'));
	const advancedSettingsBox = Array.from(document.getElementsByClassName('advanced__box'));

	// Delete collaborator
	const deleteCollaboratorButton = document.getElementById('settings-delete-collaborator-button');

	/**********************  EXECUTABLE CODE ********************************/

	settingsTabs.forEach((tab) => tab.addEventListener('click', handleActiveTab));
	// selectedLanguage.addEventListener('click', handleSelectedLanguage);
	advancedSettingsBox.forEach((box) =>
		box.addEventListener('click', handleAdvancedSettingsRoute)
	);
	backToAdvancedButton.forEach((button) =>
		button.addEventListener('click', handleAdvancedSettingsRoute)
	);
	allSchedulesContainer.forEach((container) =>
		container.addEventListener('click', bindCrewPopupClick)
	);
	deleteCollaboratorButton.addEventListener('click', handleCollaboratorExclusion);

	/**********************  DECLARATIONS ********************************/
	function handleActiveTab(event) {
		let clickedTab = event.currentTarget;
		let clickedTabId = clickedTab.id;
		for (let tab of settingsTabs) {
			tab.classList.remove('tab-button--active');
		}
		clickedTab.classList.add('tab-button--active');
		handleShownContent(clickedTabId);
		function handleShownContent(activeTabId) {
			const oldContent = Array.from(
				document.getElementsByClassName('active-settings__content')
			);
			oldContent.forEach((content) => content.classList.remove('active-settings__content'));
			document
				.getElementById(`${activeTabId}-content`)
				.classList.add('active-settings__content');
		}
	}
	function handleSelectedLanguage() {
		const languageDropdown = document.getElementById('language-dropdown-menu');
		if (languageDropdown.style.display == 'block') {
			languageDropdown.style.display = '';
			languageDropdown.dataset.showing = 'false';
		} else {
			languageDropdown.style.display = 'block';
			languageDropdown.dataset.showing = 'true';
		}
	}
	function handleAdvancedSettingsRoute(event) {
		event.target.className.includes('advanced__back-btn')
			? handleBackButton(event)
			: goToSetting(event);
		function handleBackButton(event) {
			const whichBackBtn = event.target;
			const backTo = whichBackBtn.dataset.back;
			const containerToHide = document.getElementById(backTo);
			const advancedContainer = document.getElementById('advanced-settings-container');
			containerToHide.style.display = '';
			advancedContainer.style.display = '';
		}
		function goToSetting(event) {
			let whichSetting = event.target;
			if (!event.target.className.includes('advanced__box')) {
				whichSetting = event.target.closest('div');
			}
			const whereTo = document.getElementById(whichSetting.dataset.setting);
			const advancedContainer = document.getElementById('advanced-settings-container');
			advancedContainer.style.display = 'none';
			whereTo.style.display = 'block';
		}
	}
	async function handleCollaboratorExclusion(event) {
		const target = event.target;
		const modal = target.closest('#crew-exclude-modal');
		const modalText = modal.querySelector('.crew__modal--text');
		const modalFooter = modal.querySelector('footer');
		const excludeButton = modalFooter.querySelector('#settings-delete-collaborator-button');
		updateModalStyle();
		showLoading();
		delete target.dataset.dismiss;
		const collaboratorsToRemove = [];
		const whichTypeOfExclusion = event.target.dataset.exclude;
		if (whichTypeOfExclusion == 'single') {
			collaboratorsToRemove.push(Number(target.dataset.user));
		} else {
			const usersListContainer = document.getElementById('crew-list-settings');
			const allUsers = Array.from(usersListContainer.children);
			allUsers.forEach((user) => {
				const input = user.querySelector('input[type=checkbox]');
				if (input.checked == true) {
					collaboratorsToRemove.push(Number(input.value));
				}
			});
		}
		const exclusionRequestState = await deleteUsersFromDatabase(collaboratorsToRemove);
		handleMessageAfterExclusion(exclusionRequestState);
		function updateModalStyle() {
			const modalHeader = modal.querySelector('header');
			modalHeader.style.display = 'none';
			modalText.classList.add(
				'd-flex',
				'flex-column',
				'justify-content-center',
				'align-items-center',
				'gap-16'
			);
			modalFooter.style.visibility = 'hidden';
			modalFooter.querySelector('.button__link').style.display = 'none';
			excludeButton.style.padding = '0.7rem 3rem';
			excludeButton.textContent = 'OK';
			excludeButton.addEventListener('click', handlePageReload);
			modalFooter.style.justifyContent = 'flex-end';
		}
		function showLoading() {
			document
				.querySelector('.modal__background--settings')
				.removeEventListener('click', handleClickOutsideModal);
			document
				.getElementById('modalsettings')
				.removeEventListener('click', handleClickOutsideModal);
			modalText.innerHTML = `
					<p class="f-size-20">${translate['finalizing_request'][language]}...</p>
					<div class="spinner-border text-secondary" role="status" style="width: 3rem; height: 3rem;">
						<span class="sr-only">Loading...</span>
					</div>`;
		}
		function handleMessageAfterExclusion(wasExclusionSuccessful) {
			setTimeout(() => {
				modalText.classList.remove('flex-column', 'justify-content-center');
				modalFooter.style.visibility = '';
				showStatusMessage(wasExclusionSuccessful);
			}, 2000);
			function showStatusMessage(status) {
				let imageIcon;
				let heading;
				let message;
				document
					.querySelector('.modal__background--settings')
					.addEventListener('click', handleClickOutsideModal);
				document
					.getElementById('modalsettings')
					.addEventListener('click', handleClickOutsideModal);
				if (status === true) {
					const checkedCollaborators = Array.from(
						document.getElementById('crew-list-settings').children
					).filter((child) => child.querySelector('input[type=checkbox]').checked);
					const howManyCollaboratorsToDelete = checkedCollaborators.length;
					imageIcon = modal.dataset.success;
					if (excludeButton.dataset.exclude == 'single') {
						heading = 'collaborator_successfully_deleted';
						message = `${modal.dataset.user} ${translate['collaborator_lost_access'][language]}`;
					} else if (howManyCollaboratorsToDelete == 1) {
						const whichCollaborator =
							checkedCollaborators[0].querySelector('.topinfo_checkbox').textContent;
						heading = 'collaborator_successfully_deleted';
						message = `${whichCollaborator} ${translate['collaborator_lost_access'][language]}`;
					} else {
						heading = 'collaborator_successfully_deleted_plural';
						message = translate['collaborator_lost_access_plural'][language];
					}
				} else {
					imageIcon = modal.dataset.error;
					heading = 'collaborator_not_deleted';
					message = translate['please_try_again_later'][language];
				}
				modalText.innerHTML = `
							<img src='${imageIcon}' alt='Success Icon'/>
							<div class='d-flex flex-column gap-16'>
								<div class='d-inline-block'>
									<p>${translate[heading][language]}</p>
									<div class="green__underlined green__underlined--discover-modal w-100"></div>
								</div>
								<span>${message}</span>
							</div>`;
			}
		}
	}
	function handlePageReload() {
		const settingsConfirmationModalExcludeBtn = document.getElementById(
			'settings-delete-collaborator-button'
		);
		settingsConfirmationModalExcludeBtn.dataset.dismiss = 'modal';
		location.assign(location);
	}
});

async function deleteUsersFromDatabase(usersToRemove) {
	const csrftoken = getCookie('csrftoken');

	const settings = {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			all_users_remove: usersToRemove,
		}),
	};
	const response = await fetch('/accounts/user/exclude', settings);

	if (response.ok == true) {
		const convertedResponse = await response.json();
		return true;
	} else {
		return false;
	}
}

const loadCrewPopManagePermission = () => {
	const managePermissionContainer = document.querySelector('.manage__permissions-container');
	managePermissionContainer?.addEventListener('click', bindCrewPopupClick);
};

const bindCrewPopupClick = (event) => {
	if (event.target.classList.contains('crew__popup-menu--icon')) {
		handleCrewPopupMenu(event);
	}
};

const handleCrewPopupMenu = (event) => {
	const targetMenu = event.target;
	const targetPopup = targetMenu.parentNode.querySelector('.crew__popup-menu-container');
	const allPopups = Array.from(document.getElementsByClassName('crew__popup-menu-container'));

	allPopups.forEach((popup) => popup.classList.remove('crew__popup-menu-container--show'));

	targetPopup.classList.toggle('crew__popup-menu-container--show');
};
