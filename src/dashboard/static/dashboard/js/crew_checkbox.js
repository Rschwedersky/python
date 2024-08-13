document.addEventListener('DOMContentLoaded', () => {
	const settingsCrewList = document.getElementById('crew-list-settings');

	settingsCrewList.addEventListener('click', handleDisabledButton);

	function handleDisabledButton(event) {
		event.preventDefault();
		const target = event.target;

		if (
			target.classList.contains('crew__list--item') ||
			target.closest('li').classList.contains('crew__list--item')
		) {
			if (
				target.classList.contains('crew__popup-menu--icon') == false &&
				target.closest('div')?.classList.contains('crew__popup-menu-container') == false
			) {
				const removeSelectedBtn = document.getElementById('crew-remove-selected');
				const removeSelectedIcon = document.getElementById('crew-remove-selected-icon');
				const allCrewItems = Array.from(
					document.getElementsByClassName('crew__list--item')
				);
				let checkbox;

				if (target.classList.contains('crew__list--item')) {
					checkbox = target.querySelector('input[type=checkbox]');
				} else {
					checkbox = target.closest('li').querySelector('input[type=checkbox]');
				}

				checkbox.checked == true ? (checkbox.checked = false) : (checkbox.checked = true);

				let isDisabled = true;

				allCrewItems.forEach((item) => {
					const itemCheckbox = item.querySelector('input[type=checkbox]');

					if (itemCheckbox.checked == true) {
						removeSelectedBtn.disabled = false;
						removeSelectedIcon.src = removeSelectedIcon.dataset.enabled;
						isDisabled = false;
					}
				});

				if (isDisabled == true) {
					removeSelectedBtn.disabled = true;
					removeSelectedIcon.src = removeSelectedIcon.dataset.disabled;
				}
			} else if (target.classList.contains('crew__popup-menu--icon')) {
				handleCrewPopupMenu(event);
			}
		}
	}

	function handleCrewPopupMenu(event) {
		const targetMenu = event.target;
		const targetPopup = targetMenu.parentNode.querySelector('.crew__popup-menu-container');
		const allPopups = Array.from(document.getElementsByClassName('crew__popup-menu-container'));

		allPopups.forEach((popup) => popup.classList.remove('crew__popup-menu-container--show'));

		targetPopup.classList.toggle('crew__popup-menu-container--show');
	}
});
