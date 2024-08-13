document.addEventListener('DOMContentLoaded', registrationRouter);

function registrationRouter() {
	const allForms = document.querySelectorAll('form');

	allForms.forEach((form) => form.addEventListener('formFirstStepSubmitted', showSecondFormStep));

	function showSecondFormStep(event) {
		const form = event.currentTarget;
		const firstStepContainer = form.closest('.jsRegistrationStep');
		const secondStepContainer = firstStepContainer.nextElementSibling;

		firstStepContainer.classList.add('d-none');
		firstStepContainer.classList.remove('d-flex');
		secondStepContainer.classList.remove('d-none');
	}
}
