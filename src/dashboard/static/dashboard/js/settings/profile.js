document.addEventListener('DOMContentLoaded', () => {
	const settingsModal = document.getElementById('modalsettings');
	const cancelIcons = Array.from(document.getElementsByClassName('settings__clear--icon'));
	const editProfileName = document.getElementById('input-profile-name');
	const editProfileEmail = document.getElementById('input-profile-email');
	const editProfilePhone = document.getElementById('input-profile-phone');
	const editProfileDepartment = document.getElementById('input-profile-department');
	const newPassword = document.getElementById('profile-new-password');

	settingsModal.addEventListener('click', handleSettingsModalDelegation);
	cancelIcons.forEach((cancelIcon) => cancelIcon.addEventListener('click', handleCancelEdit));

	editProfileName.addEventListener('input', handleEditProfileButtonState);
	editProfileEmail.addEventListener('input', handleEditProfileButtonState);
	editProfilePhone.addEventListener('input', handleEditProfileButtonState);
	editProfileDepartment.addEventListener('input', handleEditProfileButtonState);

	function handleSettingsModalDelegation(event) {
		const target = event.target;
		if (target.classList.contains('settings__edit--icon')) {
			handleInputEdit(event);
		} else if (target.classList.contains('submit_profile')) {
			handleSubmitProfile();
		}
	}

	function handleInputEdit(event) {
		const targetIcon = event.target;
		const closestTagP = targetIcon.closest('p');
		const pTagTextContent = closestTagP.innerText;
		const pTagHtml = closestTagP.innerHTML;

		const targetInputContainer = document.getElementById(targetIcon.dataset.container);
		const targetInput = document.getElementById(targetIcon.dataset.input);

		targetInputContainer.dataset.open = true;
		closestTagP.style.display = 'none';

		targetInput.setAttribute('placeholder', pTagTextContent);
		targetInput.dataset.html = pTagHtml;

		targetInputContainer.style.display = 'block';
	}

	function handleCancelEdit(event) {
		const targetIcon = event.target;
		const closestDivContainer = targetIcon.closest('div');
		closestDivContainer.style.display = 'none';
		closestDivContainer.dataset.open = false;
		const targetTagP = document.getElementById(targetIcon.dataset.paragraph);
		targetTagP.style.display = 'flex';
	}

	function handleEditProfileButtonState() {
		const submitButton = document.querySelector('#modalsettings .submit_profile');
		const nameChanged =
			Boolean(editProfileName.value) &&
			editProfileName.value.trim() != editProfileName.dataset.old.trim();
		const emailChanged =
			Boolean(editProfileEmail.value) &&
			editProfileEmail.value.trim() != editProfileEmail.dataset.old.trim();
		const phoneChanged =
			Boolean(editProfilePhone.value) &&
			editProfilePhone.value.trim() != editProfilePhone.dataset.old.trim();
		const departmentChanged =
			Boolean(editProfileDepartment.value) &&
			editProfileDepartment.value.trim() != editProfileDepartment.dataset.old.trim();
		if (nameChanged || emailChanged || departmentChanged || phoneChanged) {
			submitButton.disabled = false;
			editProfileName.dataset.old;
		} else {
			submitButton.disabled = true;
		}
	}

	async function handleSubmitProfile(e) {
		let settingsModal = document.getElementById('modalsettings');
		let btn_submit = document.querySelector('.submit_profile');
		replaceWith(btn_submit, getLoadingDiv(true, ' small'));
		let old_password = document.getElementById('profile-old-password').value;
		let new_password = newPassword.value;
		let loading = settingsModal.querySelector('.loading_div');
		let email = editProfileEmail.value.trim();

		if (email) {
			if (!editProfileEmail.checkValidity()) {
				// const emailIsPersonal = checkIfEmailIsPersonal(email);
				const msg = `${translate['it_is_necessary_to_inform_a_valid_email'][language]}.`;
				return (
					Swal.fire('Oops..', msg, 'error'), replaceWith(loading, btn_submit.outerHTML)
				);
			}
		}

		const csrftoken = getCookie('csrftoken');
		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				user: editProfileName.value.trim(),
				email: editProfileEmail.value.trim(),
				department: editProfileDepartment.value.trim(),
				phone: editProfilePhone.value.trim(),
				new_password: new_password,
				old_password: old_password,
			}),
		};

		const response = await fetch('/accounts/user/edit_profile_user', settings);
		replaceWith(loading, btn_submit.outerHTML);
		if (response.ok == true) {
			let email_banner = document.querySelector('.email_banner');
			let modal_emailverification = document.querySelector(
				'#onboarding__modal_1 .email_banner'
			);
			let email_confirm_email = document.querySelector('#modal__confirm_email .email_banner');

			const dropdownName = document.getElementById('dropdown01');
			Swal.fire(
				translate['success'][language],
				translate['your_profile_has_been_updated'][language],
				'success'
			);
			$('#modalsettings').modal('hide');
			resetSettingsModal();
			if (editProfileName.value.trim()) {
				dropdownName.innerHTML = `<i class="mr-1"></i>${editProfileName.value.trim()}`;
			}
			if (editProfileEmail.value.trim() && email_confirm_email) {
				email_banner.innerHTML = `<strong class="email_banner">&nbsp;${editProfileEmail.value.trim()}</strong>`;
				modal_emailverification.innerHTML = `<strong class="email_banner">&nbsp;${editProfileEmail.value.trim()}</strong>`;
				email_confirm_email.innerHTML = `<strong class="email_banner">&nbsp;${editProfileEmail.value.trim()}</strong>`;
			}
			return true;
		} else {
			const convertedResponse = await response.json();
			Swal.fire('Oops..', convertedResponse['msg'], 'error');
			document
				.querySelector('.submit_profile')
				.addEventListener('click', handleSubmitProfile);
			return false;
		}
	}
});
