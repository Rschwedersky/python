document.addEventListener('DOMContentLoaded', () => {
	let handler;
	/**********************  CONSTANTS ********************************/
	const registrationContainer = document.querySelector('.registration__inner-content');
	const addRpaDashboardButtons = Array.from(
		document.getElementsByClassName('btn__purple--registration-rpa')
	);
	const allAddServiceButtons = registrationContainer.querySelectorAll('.btn__add-service');
	const allButtonsToManipulatePermissions = Array.from(
		document.getElementsByClassName('btn__manipulate-permissions--conclude_registry')
	);
	const allButtonsToShowServiceInfo = document.querySelectorAll(
		'.registration__single-service-header img.menu-info'
	);

	const concludeRegistryButton = document.getElementById(
		'registration-choosing-licenses-advance-button'
	);

	function handleLoadingScreenAppearing(action) {
		const container = document.querySelector('.registration__background');
		const loadingScreen = document.querySelector('.jsConcludeRegistryLoading');

		if (action == 'show') {
			handler = runAnimations();
		} else {
			stopAnimations(handler);
		}

		container.classList.toggle('d-none');
		loadingScreen.classList.toggle('d-none');
	}

	/**********************  EXECUTABLE CODE ********************************/
	addRpaDashboardButtons.forEach((button) =>
		button.addEventListener('click', handleAddRpaButtonClick)
	);
	allAddServiceButtons.forEach((button) => button.addEventListener('click', handleAddService));
	allButtonsToManipulatePermissions.forEach((button) =>
		button.addEventListener('click', handlePermissionsManipulation)
	);
	allButtonsToShowServiceInfo.forEach((button) =>
		button.addEventListener('click', showServiceInfo)
	);

	concludeRegistryButton.addEventListener('click', concludeRegistry);

	/**********************  DECLARATIONS ********************************/

	function handleAddRpaButtonClick(event) {
		let targetButton = event.currentTarget;
		let withDashboard = document.getElementById('with_dashboard');

		let numberOfUsedLicenses = countServices();

		if (targetButton.classList.contains('btn__purple--registration-rpa--clicked')) {
			addRpaDashboardButtons.forEach((button) => {
				button.classList.remove('btn__purple--registration-rpa--clicked');
				button.innerHTML = translate['add_to_my_plan'][language];
			});
			withDashboard.value = '0';
			numberOfUsedLicenses--;
		} else {
			addRpaDashboardButtons.forEach((button) => {
				const imageSrc = button.dataset.image;

				button.classList.add('btn__purple--registration-rpa--clicked');
				button.innerHTML = `${translate['added'][language]} <img src=${imageSrc} alt='Check Icon'  class='ml-2'/>`;
			});
			withDashboard.value = '1';
			numberOfUsedLicenses++;
		}

		registrationContainer.dataset.licenses = numberOfUsedLicenses;
		updateAdvanceButtonState();
	}

	function handleAddService(event) {
		let targetButton = event.currentTarget;
		const serviceBox = targetButton.closest('.registration__single-service-box');
		const targetPermissionsSection = serviceBox.querySelector(
			'.registration__single-service-permissions'
		);
		const licensesManipulationBox = targetPermissionsSection.querySelector('div');
		let numberOfUsedLicenses = countServices();

		targetButton.classList.add('d-none');
		licensesManipulationBox.classList.remove('d-none');
		licensesManipulationBox.classList.add('d-flex');

		numberOfUsedLicenses++;

		registrationContainer.dataset.licenses = numberOfUsedLicenses;
		serviceBox.classList.add('service--selected');
		updateAdvanceButtonState();
	}

	function handlePermissionsManipulation(event) {
		const targetButton = event.target;
		const numberOfPermissionsElement = targetButton
			.closest('.registration__single-service-permissions')
			.querySelector('span');

		let usedLicenses = Number(registrationContainer.dataset.licenses);
		let count;

		if (targetButton.dataset.manipulation == 'decrease') {
			const currentNumberOfPermissions = Number(
				targetButton.nextElementSibling.querySelector('.howmany_automations_added')
					.textContent
			);
			count = currentNumberOfPermissions - 1;
			usedLicenses--;
		} else if (targetButton.dataset.manipulation == 'increase') {
			const currentNumberOfPermissions = Number(
				targetButton.previousElementSibling.querySelector('.howmany_automations_added')
					.textContent
			);

			count = currentNumberOfPermissions + 1;
			usedLicenses++;
		}

		if (count != 0) {
			if (count >= 10) {
				numberOfPermissionsElement.innerHTML = `<span class="howmany_automations_added">${count}</span> ${checkNumberAgreement(
					count
				)}`;
			} else {
				numberOfPermissionsElement.innerHTML = `<span class="howmany_automations_added">0${count}</span> ${checkNumberAgreement(
					count
				)}`;
			}
		} else if (count == 0 && targetButton.dataset.manipulation == 'decrease') {
			const serviceBox = targetButton.closest('.registration__single-service-box');
			serviceBox.classList.remove('service--selected');
			cleanServiceBox(serviceBox);
		}

		registrationContainer.dataset.licenses = usedLicenses;
		updateAdvanceButtonState();

		function checkNumberAgreement(number) {
			return number == 1 ? translate['license'][language] : translate['licenses'][language];
		}
	}

	function showServiceInfo(event) {
		const button = event.currentTarget;
		const header = button.closest('header');
		const infoToHide = header.querySelector('div');
		const infoToShow = header.querySelector('.info-text');
		const temporaryHolderForImageSrc = button.src;

		infoToHide.classList.toggle('d-none');
		infoToShow.classList.toggle('d-none');

		button.src = button.dataset.image;
		button.dataset.image = temporaryHolderForImageSrc;
	}

	async function concludeRegistry(event) {
		handleLoadingScreenAppearing('show');
		const withDashboard = document.getElementById('with_dashboard');
		const allAutomationsAdded = document.querySelectorAll('.service--selected');
		const chosenServices = {};

		allAutomationsAdded.forEach((service) => {
			const serviceName = service.dataset.automation_name;

			if (typeof chosenServices[serviceName] == undefined) {
				chosenServices[serviceName] = 0;
			}
			chosenServices[serviceName] = Number(
				service.querySelector('.howmany_automations_added').textContent
			);
		});

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({
				with_dashboard: withDashboard.value,
				automations_allocated: chosenServices,
			}),
		};

		const response = await fetch('/register/conclude/submit', settings);

		if (response.ok) {
			setTimeout(() => (window.location = `/`), 7500);
		} else {
			handleLoadingScreenAppearing('hide');
			Swal.fire('Ooops..', `${translate['an_error_happened'][language]}`, 'error');
		}
	}

	function updateAdvanceButtonState() {
		const advanceButton = document.getElementById(
			'registration-choosing-licenses-advance-button'
		);
		const usedLicenses = countServices();
		const userHasTheMinimalNumberOfLicenses = usedLicenses >= 3;

		advanceButton.disabled = userHasTheMinimalNumberOfLicenses ? false : true;
	}

	function countServices() {
		const numberOfServicesAdded = document.querySelector('.registration__inner-content').dataset
			.licenses;
		return Number(numberOfServicesAdded) >= 0 ? Number(numberOfServicesAdded) : 0;
	}

	function cleanServiceBox(box) {
		const permissionsSection = box.querySelector('.registration__single-service-permissions');
		const addServiceButton = permissionsSection.querySelector('button');
		const licensesManipulationBox = permissionsSection.querySelector('div');
		const numberOfPermissionsElement = permissionsSection.querySelector('span');

		licensesManipulationBox.classList.add('d-none');
		licensesManipulationBox.classList.remove('d-flex');
		addServiceButton.classList.remove('d-none');
		numberOfPermissionsElement.innerHTML = `<span class="howmany_automations_added">01</span> ${translate['license'][language]}`;
	}

	function runAnimations() {
		const handler = setInterval(() => {
			const container = document.querySelector('.jsRegistrationAnimationContainer');
			const children = Array.from(container.children);

			const first = container.querySelector('p:not(.showing)');

			if (!first) {
				children.forEach((child) => child.classList.replace('showing', 'hiding'));
			} else {
				first.classList.add('showing');
				first.classList.remove('hiding');
			}
		}, 2000);

		return handler;
	}
	function stopAnimations(handler) {
		handler = clearInterval(handler);
	}
});

function updateProgressBar(action, decreaseBy) {
	let progress = document.querySelector('progress');

	if (action == 'increase') {
		progress.value++;
	} else if (action == 'decrease' && progress.value > 0 && Boolean(decreaseBy) == true) {
		progress.value = Number(progress.value) - Number(decreaseBy);
	} else if (action == 'decrease' && progress.value > 0) {
		progress.value--;
	}

	progress.closest('div').querySelector('#used-licenses').textContent = progress.value;
}
