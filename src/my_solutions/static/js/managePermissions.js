document.addEventListener('DOMContentLoaded', () => {
	const tabManagePermission = document.getElementById('manage_permissions');
	if (!tabManagePermission.querySelector('.loading_div')) {
		loadManagePermissionsScript();
	}
});
const loadManagePermissionsScript = () => {
	const allProgressionsRings = document.querySelectorAll('.progress__circular--ring');
	const modalPermission = document.querySelector('.permissions__collaborator-modal');
	const allModalUsers = document.querySelectorAll(
		'.permissions__collaborator-modal .crew__list--item'
	);
	const submitButton = document.querySelector(
		'.permissions__collaborator-modal .permissions__modal--btn'
	);
	const managePermissionContainer = document.querySelector('.manage__permissions-container');

	managePermissionContainer.addEventListener('click', bindCrewListClick);

	allProgressionsRings.forEach((svgCircle) => updateProgressRing(svgCircle));

	const allResetPermissionsBtn = Array.from(document.getElementsByClassName('reset_permissions'));

	const addPermissionToCollaboratorForms = Array.from(
		document.getElementsByClassName('permissions__modal-form')
	);
	const addPermissionToCollaboratorInputs = Array.from(
		document.getElementsByClassName('permissions__modal-form-input')
	);

	addPermissionToCollaboratorForms.forEach((form) =>
		form.addEventListener('submit', handleNewPermissionIntoCollaborator)
	);

	addPermissionToCollaboratorInputs.forEach((input) =>
		input.addEventListener('input', handleInputChange)
	);

	allModalUsers.forEach((single_checkbox) =>
		single_checkbox.addEventListener('change', handleSingleCheckboxChange)
	);

	modalPermission.addEventListener('click', handleClickModal);

	allResetPermissionsBtn.forEach((btn) => btn.addEventListener('click', handleResetPermissions));

	function bindCrewListClick(e) {
		if (e.target.classList.contains('crew__exclude')) {
			let user_id = e.target.closest('.single_permission_box').dataset.user_id;
			let automation_name = e.target
				.closest('.permissions-box__container')
				.querySelector('.btn__purple--permissions').dataset.automation_name;
			submitDeletePermission(automation_name, user_id);
		}
	}

	function handleClickModal(event) {
		const target = event.target;
		const isButtonToSubmitInvite =
			target.classList.contains('permissions__modal--btn') ||
			target.parentElement.classList.contains('permissions__modal--btn');
		const isEmployeeItem =
			target.classList.contains('permissions__modal-email--item') ||
			target.closest('li')?.classList.contains('permissions__modal-email--item');

		if (isButtonToSubmitInvite) {
			handleInviteSubmit(event);
		} else if (isEmployeeItem) {
			handleUserSelection(event);
		}
	}

	function handleInviteSubmit(event) {
		const submitButton =
			event.target.nodeName.toLowerCase() != 'button'
				? event.target.closest('button')
				: event.target;
		replaceWith(submitButton, getLoadingDiv(true, '', ' w-35'));
		const automationName = document.getElementById('permission_automation_name').value;
		const allUsersAdd = getCheckedUsers();
		const allUsersRemove = [];
		const allPermittedUsers = getAllPermittedUsers(
			document.querySelector(`[data-automation_name=${automationName}]`)
		);
		allPermittedUsers.forEach((singleUserPermission) => {
			const index = allUsersAdd.indexOf(singleUserPermission.dataset.user_id);
			if (index !== -1) {
				allUsersAdd.splice(index, 1);
			} else {
				allUsersRemove.push(singleUserPermission.dataset.user_id);
			}
		});
		const csrfmiddlewaretoken = getCSRFauth();
		$.post(
			`/services/manage/permissions`,
			{
				all_users_add: JSON.stringify(allUsersAdd),
				all_users_remove: JSON.stringify(allUsersRemove),
				automation_name: automationName,
				csrfmiddlewaretoken: csrfmiddlewaretoken,
			},
			function (data) {
				if (data.hasOwnProperty('status')) {
					Swal.fire('Oops..', data['msg'], 'error');
				} else {
					updatePermissionsBox(automationName, data);
					document
						.querySelector('.modal__background.modal__background--permissions')
						.click();
					handleRestorePermissionsState();
				}
				replaceWith(
					document.querySelector('#manage_permissions .loading_div'),
					submitButton.outerHTML
				);
			}
		).catch((err) => {
			Swal.fire('Oops..', err.responseJSON.msg, 'error');
			const emailAlreadyExists = Boolean(err.responseJSON.user_repeated_email);
			if (emailAlreadyExists) {
				const repeatedEmail = err.responseJSON.user_repeated_email;
				const collaboratorsList = document.getElementById('permissions-modal-email-list');
				const repeatedEmailElement = collaboratorsList.querySelector(
					`[data-user="${repeatedEmail}"]`
				);
				repeatedEmailElement.remove();
			}
			replaceWith(
				document.querySelector('#manage_permissions .loading_div'),
				submitButton.outerHTML
			);
		});
	}

	function handleResetPermissions(e) {
		let automation_name = e.target
			.closest('.permissions-box__container')
			.querySelector('.btn__purple--permissions').dataset.automation_name;
		submitDeletePermission(automation_name, 0);
	}

	function submitDeletePermission(automationName, userId = 0) {
		let csrfmiddlewaretoken = getCSRFauth();
		$.post(
			'/services/delete/permissions',
			{
				automation_name: automationName,
				user_id: userId,
				csrfmiddlewaretoken: csrfmiddlewaretoken,
			},
			function (data) {
				if (data.hasOwnProperty('status') && data['status'] != 200) {
					Swal.fire('Oops..', data['msg'], 'warning');
				} else {
					let allUsersDiv = `<div class="permission-box__content--collaborator"></div>`;
					if (userId != 0) {
						allUsersDiv = data;
					}
					let permissionBox = document
						.querySelector(`[data-automation_name=${automationName}]`)
						.closest('.permission-box__content');
					permissionBox.querySelector('.permissions__warning--no-permissions')?.remove();
					updatePermissionsBox(automationName, allUsersDiv);
					handleRestorePermissionsState();
				}
			}
		);
	}

	function getCheckedUsers() {
		let allUsers = [];
		const usersWithLicenses = document.querySelectorAll(
			'.permissions__collaborator-modal .permissions__modal-email--active'
		);

		usersWithLicenses.forEach((user) => allUsers.push(user.dataset.user));

		return allUsers;
	}

	function handleUserSelection(event) {
		let targetUser = event.target;

		if (targetUser.tagName != 'li') {
			targetUser = targetUser.closest('li');
		}

		let howManyPermissions = Number(
			document.querySelector('footer .howmany_permissions').textContent
		);
		let allUsersChecked = getCheckedUsers();
		const userIsChecked = targetUser.classList.contains('permissions__modal-email--active');

		if (howManyPermissions > allUsersChecked.length || userIsChecked) {
			targetUser.classList.toggle('permissions__modal-email--active');
			handleSubmitButtonState();
		} else {
			Swal.fire(
				'Oops..',
				`${translate['it_in_only_possible_to_invite'][language]} ${howManyPermissions} ${
					howManyPermissions == 1
						? translate['employee_small'][language]
						: translate['employees'][language]
				}`,
				'warning'
			);
		}
	}

	function handleNewPermissionIntoCollaborator(event) {
		event.preventDefault();

		let howmany_permissions = Number(
			document.querySelector('footer .howmany_permissions').textContent
		);
		let allUsersChecked = getCheckedUsers();
		if (howmany_permissions > allUsersChecked.length) {
			const form = event.target;
			const inputValue = form.elements['collaborator_info'].value;

			if (form.elements['collaborator_info'].checkValidity()) {
				const collaboratorsList = document.getElementById('permissions-modal-email-list');
				const newCollaboratorElement = document.createElement('li');
				newCollaboratorElement.classList.add(
					'permissions__modal-email--item',
					'permissions__modal-email--active',
					'c-pointer'
				);
				newCollaboratorElement.dataset.user = inputValue.trim();
				newCollaboratorElement.innerHTML = `
				<div>
					<span class="border__circle border__circle--permissions">${inputValue.substring(0, 2).toUpperCase()}
					</span>
					<div class="d-flex flex-column">
						<p class="m-0 light-bold topinfo_checkbox">${inputValue}</p>
					</div>
				</div>		
				<span class="color-muted f-size-14">Colaborador</span>
			`;

				collaboratorsList.prepend(newCollaboratorElement);
				submitButton.disabled = false;

				cleanFormAfterSubmit();

				function cleanFormAfterSubmit() {
					const formButton = form.elements['form_collaborator_button'];

					form.reset();
					formButton.disabled = true;
				}
			} else {
				const emailIsPersonal = checkIfEmailIsPersonal(inputValue);
				const msg = `${
					translate[
						emailIsPersonal
							? 'please_enter_profissional_email_address'
							: 'it_is_necessary_to_inform_a_valid_email'
					][language]
				}.`;

				return Swal.fire('Oops..', msg, 'error');
			}
		} else {
			Swal.fire(
				'Oops..',
				`${translate['it_in_only_possible_to_invite'][language]} ${howmany_permissions} ${
					howmany_permissions == 1
						? translate['employee_small'][language]
						: translate['employees'][language]
				}`,
				'warning'
			);
		}
	}

	function updatePermissionsBox(automation_name, new_permission_box) {
		let btn_permission_box = document.querySelector(
			`[data-automation_name=${automation_name}]`
		);
		let permission_box = btn_permission_box.closest('.permissions-box__container');
		let to_replace = permission_box.querySelector('.permission-box__content--collaborator');
		replaceWith(to_replace, new_permission_box);
		let permissions_total = permission_box.querySelector('.permissions_total').innerHTML;
		let permissions_available =
			permissions_total - getAllPermittedUsers(btn_permission_box).length;
		permission_box.querySelector('.progress_permissions_available').innerHTML =
			permissions_available;
		permission_box.querySelector('progress').value = permissions_available;
		permission_box.querySelector('.permissions_available').innerHTML = permissions_available;
		let parent_ring = permission_box.querySelector('.progress__circular--image-enabled');
		let img_nopermissions_available = permission_box.querySelector('.no_permissions_available');
		let ring = permission_box.querySelector('.progress__circular--ring');
		if (permissions_available == 0) {
			// ADD banner all infos transfered, as no licenses available
			let banner = getAllLicensesTransferedBanner();
			let permissionBoxContent = btn_permission_box.closest('.permission-box__content');
			let maxNodes = permissionBoxContent.childNodes.length;
			permissionBoxContent.insertBefore(
				banner,
				permissionBoxContent.childNodes[maxNodes - 2]
			);
			img_nopermissions_available.classList.remove('d-none');
			parent_ring.classList.add('d-none');
		} else {
			img_nopermissions_available.classList.add('d-none');
			parent_ring.classList.remove('d-none');
		}
		ring.dataset.available = permissions_available;
		updateProgressRing(ring);
	}

	function getAllLicensesTransferedBanner() {
		let banner = document.createElement('div');
		banner.innerHTML = `<p class="permissions__warning--no-permissions">
		<strong>${translate['you_have_transferred_all_licenses'][language]}. </strong>
		${translate['to_use_this_service_you_need'][language]}.</p>`;
		return banner.childNodes[0];
	}

	function handleRestorePermissionsState() {
		allResetPermissionsBtn.forEach((buttonsContainer) => {
			const permissionsAvailableSpan = buttonsContainer.previousElementSibling.querySelector(
				'.progress_permissions_available'
			);
			const numberOfPermissionsAvailable = Number(permissionsAvailableSpan.textContent);

			const numberOfPermissionsTotal = Number(
				permissionsAvailableSpan.nextSibling.textContent.replace(/\D/g, '')
			);

			const resetIcon = buttonsContainer.querySelector('.reset__permissions-icon--enabled');
			const resetIconDisabled = buttonsContainer.querySelector(
				'.reset__permissions-icon--disabled'
			);
			const resetText = buttonsContainer.querySelector('span');

			if (numberOfPermissionsAvailable == numberOfPermissionsTotal) {
				resetIcon.classList.add('d-none');
				resetIconDisabled.classList.remove('d-none');
				resetText.classList.remove('c-pointer', 'opacity-hover');
				resetText.classList.add('color-muted--lightest');
			} else {
				resetIcon.classList.remove('d-none');
				resetIconDisabled.classList.add('d-none');
				resetText.classList.remove('color-muted--lightest');
				resetText.classList.add('c-pointer', 'opacity-hover');
			}
		});
	}

	function handleSubmitButtonState() {
		const allUsersWithLicenses = Array.from(
			document.querySelectorAll(
				'.permissions__collaborator-modal .permissions__modal-email--active'
			)
		);
		const initialSelectedUsers = submitButton.dataset.users;

		const newUserWithLicenses = allUsersWithLicenses.filter(
			(user) => !initialSelectedUsers.includes(user.dataset.user)
		);

		if (newUserWithLicenses.length > 0) {
			submitButton.disabled = false;
		} else {
			submitButton.disabled = true;
		}
	}

	function handleInputChange(event) {
		const input = event.target;
		const button = input.nextElementSibling;

		input.checkValidity() ? (button.disabled = false) : (button.disabled = true);
	}
};

function updateProgressRing(svgCircleElement) {
	let circleArea;
	try {
		circleArea = svgCircleElement.getTotalLength();
	} catch {
		const radius = svgCircleElement.r.baseVal.value;
		circleArea = radius * 2 * Math.PI;
	}

	svgCircleElement.style.strokeDasharray = `${circleArea} ${circleArea}`;

	const totalPermissions = svgCircleElement.dataset.total;
	const availablePermissions = svgCircleElement.dataset.available;

	if (availablePermissions == 0) {
		svgCircleElement.style.strokeDashoffset = circleArea;
	} else {
		const percentageCompleted = totalPermissions / availablePermissions;
		const offset = circleArea - circleArea / percentageCompleted;

		svgCircleElement.style.strokeDashoffset = offset;
	}
}
