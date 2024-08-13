document.addEventListener('DOMContentLoaded', () => {
	$('#root').on('click', '#areas', function (e) {
		e.preventDefault();
		loadingManageOptions();
		$.get('/areas', function (data) {
			$('#manage_settings_tab > .container').replaceWith(data);
			document
				.querySelector('#edit_area_modal form input[type="text"]')
				.addEventListener('input', handleEditButtonState);
			document
				.querySelector('#new_area_modal form input[type="text"]')
				.addEventListener('input', handleRegisterButtonState);
		});
	});

	$('#root').on('click', '#process', function (e) {
		e.preventDefault();
		getProcess().done(() => updateJsAfterContentIsShown());
	});

	$('#root').on('click', '#process_btn', function (e) {
		getProcess().done(() => updateJsAfterContentIsShown());
		const singleMenu = document.querySelector('.single_menu.config');
		const tab = document.getElementById(singleMenu.dataset.idtab);
		openTab(singleMenu, tab);
	});

	$('#root').on('click', '.back_settings', function (e) {
		e.preventDefault();
		$('#manage_settings_tab').html(
			`<div class="container  h-90 whitebackcolor container__loading d-flex justify-content-center align-items-center">${getLoadingDiv()}</div>`
		);
		updateTableContent();
	});
});

function loadingManageOptions() {
	$('#manage_settings_tab > .container').html(
		`<div class="container__loading d-flex justify-content-center align-items-center my-5">${getLoadingDiv()}</div>`
	);
}

const getProcess = () => {
	loadingManageOptions();
	return $.get('/process', function (data) {
		const settingsContainer = $('#manage_settings_tab > .container');
		if (settingsContainer.length > 0) {
			settingsContainer.replaceWith(data);
		} else {
			const areaContainer = $('#manage_settings_tab > #manage_areas_tab');
			areaContainer.replaceWith(data);
		}
	});
};

function handleRegisterButtonState(event) {
	const target = event.target;
	const oldValue = target.dataset.old;
	const newValue = target.value;

	const submitButton = target.closest('.modal').querySelector('.btn__submit-area');
	if (oldValue == newValue) {
		submitButton.disabled = true;
	} else {
		submitButton.disabled = false;
	}
}

function handleEditButtonState(event) {
	const target = event.target;
	const oldValue = target.dataset.old;
	const newValue = target.value;

	const submitButton = target.closest('.modal').querySelector('.btn__submit-area-edit');
	if (oldValue == newValue) {
		submitButton.disabled = true;
	} else {
		submitButton.disabled = false;
	}
}

function updateTableContent() {
	$.get('/get/settings/tab', function (html) {
		$('#manage_settings_tab').replaceWith(html);
		$('#manage_settings_tab').addClass('active');
	});
}
