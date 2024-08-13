document.addEventListener('DOMContentLoaded', () => {
	let isFirstStep = true;

	const allForms = Array.from(document.querySelectorAll('form'));
	const secondStepForm = document.getElementById('second-step-form');
	const phoneInput = secondStepForm.elements.phone;

	allForms.forEach((form) => {
		form.addEventListener('submit', handleFormSubmission);
		form.addEventListener('input', handleFormEventDelegation);
	});

	secondStepForm.addEventListener('change', toggleOtherFieldsVisibility);
	phoneInput.addEventListener('countrychange', handlePhoneInput);

	function handleFormEventDelegation(event) {
		const target = event.target;
		const isInputWithCustomValidity = target.classList.contains('jsCustomValidity');

		if (isInputWithCustomValidity) {
			target.setCustomValidity('');
			target.classList.remove('jsCustomValidity');
		} else {
			return;
		}
	}

	async function handleFormSubmission(event) {
		event.preventDefault();
		const form = event.currentTarget;
		const elements = Array.from(form.elements);

		const { inputsAreValid, errorMessage } = validateInputs(form, elements);

		if (inputsAreValid) {
			if (isFirstStep) {
				const evt = new Event('formFirstStepSubmitted');

				form.dispatchEvent(evt);
				isFirstStep = false;
			} else {
				await submitForm(event);
			}

			form.classList.replace('needs-validation', 'was-validated');
		} else {
			return Swal.fire({
				position: 'top',
				title: 'Erro!',
				text: errorMessage,
				icon: 'error',
				confirmButtonText: 'OK',
			});
		}
	}

	async function submitForm(event) {
		const form = event.currentTarget;

		const button = form.querySelector('button[type="submit"]');
		replaceWith(button, getLoadingDiv());

		const body = getRequestBody();
		const userRole = button.getAttribute('data-admin') === 'true' ? 4 : 1;

		const fieldsWithError = new Set();

		body['user_role'] = userRole;

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify(body),
		};

		try {
			const response = await fetch(location.pathname, settings);

			if (response.ok) {
				startLoadingAnimations();
				window.location =
					button.getAttribute('data-admin') == 'true' ? '/register/conclude' : '/';

				function startLoadingAnimations() {
					const mainContent = document.getElementById('registration');
					const loading = mainContent.nextElementSibling;

					mainContent.classList.add('d-none');
					loading.classList.remove('d-none');
				}
			} else {
				const convertedResponse = await response.json();

				if ('field' in convertedResponse) {
					fieldsWithError.add(convertedResponse.field);
				}

				throw new Error(convertedResponse.msg);
			}
		} catch (error) {
			let errorMsg;

			if (error instanceof SyntaxError) {
				errorMsg = translate['an_error_happened'][language];
			} else {
				errorMsg = error.message || translate['an_error_happened'][language];
			}

			Swal.fire({
				title: 'Erro!',
				text: errorMsg,
				icon: 'error',
				confirmButtonText: 'OK',
			});

			showFirstStepOfTheForm();
			addInvalidClassesToFieldsWithError(Array.from(fieldsWithError));

			function showFirstStepOfTheForm() {
				const firstStep = allForms.at(0)?.closest('.jsRegistrationStep');
				const secondStep = secondStepForm.closest('.jsRegistrationStep');

				if (!firstStep || !secondStep) return;

				secondStep.classList.add('d-none');
				firstStep.classList.replace('d-none', 'd-flex');
				isFirstStep = true;
			}

			function addInvalidClassesToFieldsWithError(fields) {
				allForms.forEach((form) => {
					fields.forEach((field) => {
						if (form.elements[field]) {
							const fieldWithError = form.elements[field];
							fieldWithError.setCustomValidity('Invalid field.');
							fieldWithError.classList.add('jsCustomValidity');
						}
					});
				});
			}
		} finally {
			replaceWith(document.querySelector('.loading_div'), button.outerHTML);
		}
	}

	function getRequestBody() {
		const data = {};
		const elements = new Set();
		allForms.forEach((form) => {
			Array.from(form.elements)
				.filter((el) => el.tagName !== 'BUTTON' || el.id === 'phone')
				.forEach((el) => {
					elements.add(el);
				});
		});

		const elementsArr = removeUnnecessaryElements(Array.from(elements));

		function removeUnnecessaryElements(elementsArr) {
			const copy = [...elementsArr];
			const areaInput = secondStepForm.elements.area;
			const roleInput = secondStepForm.elements.role;

			if (areaInput.value == 'other') {
				copy.splice(copy.indexOf(areaInput), 1);
			} else {
				const otherInput = secondStepForm.elements.otherArea;
				copy.splice(copy.indexOf(otherInput), 1);
			}

			if (roleInput.value == 'other') {
				copy.splice(copy.indexOf(roleInput), 1);
			} else {
				const otherInput = secondStepForm.elements.otherRole;
				copy.splice(copy.indexOf(otherInput), 1);
			}

			return copy;
		}

		elementsArr.forEach((el) => {
			if (el.name.includes('other')) {
				const updatedName = el.name.replace('other', '').toLowerCase();
				data[updatedName] = el.value;
			} else {
				data[el.name] = el.value;
			}
		});

		return data;
	}

	function validateInputs(form, inputs) {
		const response = {
			inputsAreValid: true,
			errorMessage: null,
		};
		const emailInput = document.querySelector('form input[type="email"]');
		inputs.forEach((input) => {
			if (!input.checkValidity()) {
				if (!input.value.trim()) {
					response.inputsAreValid = false;
					response.errorMessage = translate['one_or_more_fields_are_empty'][language];
					return;
				}

				response.inputsAreValid = false;
				if (!response.errorMessage)
					response.errorMessage = translate['one_or_more_fields_are_invalid'][language];
			} else if (input === phoneInput) {
				if (input.value.trim() && !validatePhone()) {
					input.setCustomValidity('Invalid field.');
					response.inputsAreValid = false;
					response.errorMessage = translate['one_or_more_fields_are_invalid'][language];
				}
			}
		});

		form.classList.replace('needs-validation', 'was-validated');

		return response;
	}

	function toggleOtherFieldsVisibility(event) {
		const input = event.target;
		const roleInput = secondStepForm.elements.role;
		const areaInput = secondStepForm.elements.area;

		if (input !== roleInput && input !== areaInput) return;

		const otherRoleInput = secondStepForm.elements.otherRole;
		const otherAreaInput = secondStepForm.elements.otherArea;

		if (roleInput.value === 'other') {
			otherRoleInput.classList.remove('d-none');
			otherRoleInput.required = true;
		} else {
			otherRoleInput.classList.add('d-none');
			otherRoleInput.required = false;
		}

		if (areaInput.value === 'other') {
			otherAreaInput.classList.remove('d-none');
			otherAreaInput.required = true;
		} else {
			otherAreaInput.classList.add('d-none');
			otherAreaInput.required = false;
		}
	}

	const iti = window.intlTelInput(phoneInput, {
		formatOnDisplay: false,
		hiddenInput: 'full_number',
		placeholderNumberType: 'MOBILE',
		allowDropdown: true,
		preferredCountries: ['br'],
		autoHideDialCode: true,
		utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.14/js/utils.js',
	});

	function handlePhoneInput(event) {
		const selectedCountryData = iti.getSelectedCountryData();
		newPlaceholder = intlTelInputUtils.getExampleNumber(
			selectedCountryData.iso2,
			true,
			intlTelInputUtils.numberFormat.INTERNATIONAL
		);
	}

	iti.promise.then(() => {
		const evt = new Event('countrychange');
		phoneInput.dispatchEvent(evt);
	});
	validPhoneInput();

	function validatePhone(phone) {
		if (iti.isValidNumber()) return true;

		return false;
	}

	function validPhoneInput() {
		errorMsg = document.querySelector('#phone-error-msg');

		phoneInput.addEventListener('keyup', formatIntlTelInput);
		phoneInput.addEventListener('change', formatIntlTelInput);
		phoneInput.addEventListener('keyup', reset);

		function formatIntlTelInput() {
			if (typeof intlTelInputUtils !== 'undefined') {
				const currentText = iti.getNumber(intlTelInputUtils.numberFormat.E164);
				if (typeof currentText === 'string') {
					iti.setNumber(currentText);
				}
			}
		}

		phoneInput.addEventListener('keyup', () => {
			reset();
			if (phoneInput.value.trim()) {
				if (iti.isValidNumber()) {
					if (phoneInput.classList.contains('is-invalid')) {
						phoneInput.classList.replace('is-invalid', 'is-valid');
					} else {
						phoneInput.classList.add('is-valid');
					}

					phoneInput.setCustomValidity('');
				} else {
					phoneInput.setCustomValidity('is-invalid');
					if (phoneInput.classList.contains('is-valid')) {
						phoneInput.classList.replace('is-valid', 'is-invalid');
					} else {
						phoneInput.classList.add('is-invalid');
					}

					errorMsg.innerHTML = translate['invalid_cell_phone'][language];

					errorMsg.style.color = 'red';
					errorMsg.style.fontSize = '12px';

					errorMsg.classList.remove('d-none');
				}
			} else {
				phoneInput.classList.remove('is-invalid');
				phoneInput.setCustomValidity('');
			}
		});

		function reset() {
			phoneInput.classList.remove('is-invalid');
			errorMsg.classList.add('d-none');
			errorMsg.innerHTML = '';
		}
	}
});
