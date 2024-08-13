document.addEventListener('DOMContentLoaded', () => {
	const toggleVisibilityIcons = Array.from(
		document.getElementsByClassName('toggle__visibility--icon')
	);
	const newPassword = document.getElementById('profile-new-password');
	const newPasswordConfirmation = document.getElementById('profile-repeat-new-password');
	const linkToPasswordScreen = document.getElementById('link-change-password');
	const backToProfileScreen = document.getElementById('back-to-profile');

	newPasswordConfirmation.addEventListener('input', checkSamePasswords);
	newPassword.addEventListener('input', checkSamePasswords);

	toggleVisibilityIcons.forEach((visibilityIcon) =>
		visibilityIcon.addEventListener('click', handlePasswordVisibility)
	);
	linkToPasswordScreen.addEventListener('click', handlePasswordScreenRoutes);
	backToProfileScreen.addEventListener('click', handlePasswordScreenRoutes);

	function handlePasswordVisibility(event) {
		const whichIcon = event.target;
		const whichPassword = document.getElementById(whichIcon.dataset.password);
		if (whichPassword.type == 'password') {
			const updatedIcon = whichIcon.src.replace('visibility', 'visibility_hidden');
			whichIcon.src = updatedIcon;
			whichPassword.type = 'text';
		} else {
			const updatedIcon = whichIcon.src.replace('visibility_hidden', 'visibility');
			whichIcon.src = updatedIcon;
			whichPassword.type = 'password';
		}
	}

	function checkSamePasswords(event) {
		const newPasswordValue = newPassword.value;
		const confirmNewPasswordValue = newPasswordConfirmation.value;
		const passwordIsStrong = newPassword.checkValidity();
		const isEqual = document.getElementById('password-is-equal');
		const isDifferent = document.getElementById('password-is-different');
		const submitButton = document.querySelector('#modalsettings .submit_profile');
		resetFeedback();
		if (newPasswordValue === confirmNewPasswordValue) {
			isEqual.style.display = 'flex';
			submitButton.disabled =
				document.querySelector('.profile__change-password--input').value.length > 0 &&
				passwordIsStrong
					? false
					: true;
		} else {
			isDifferent.style.display = 'flex';
			submitButton.disabled = true;
		}
		function resetFeedback() {
			isEqual.style.display = 'none';
			isDifferent.style.display = 'none';
		}
	}

	function handlePasswordScreenRoutes() {
		const profileForm = document.getElementById('settings-profile-form');
		const passwordScreen = document.getElementById('new-password-screen');
		if (profileForm.style.display == 'none' && passwordScreen.style.display == 'block') {
			profileForm.style.display = '';
			passwordScreen.style.display = '';
		} else {
			profileForm.style.display = 'none';
			passwordScreen.style.display = 'block';
		}
	}
});
