document.addEventListener('DOMContentLoaded', () => {
	const passwordVisibilityIcons = document.querySelectorAll('input[type="password"] + button');
	const allSearchInputsClearButtons = document.querySelectorAll(
		'form input[type="search"] ~ .btn[type="button"]'
	);

	$(function () {
		$('[data-toggle="tooltip"]').tooltip();
	});

	passwordVisibilityIcons.forEach((icon) =>
		icon?.addEventListener('click', togglePasswordVisibility)
	);

	allSearchInputsClearButtons.forEach((button) =>
		button?.addEventListener('click', resetSearchInput)
	);

	function togglePasswordVisibility(event) {
		const button = event.currentTarget;

		const container = event.target.closest('.input-container');
		const icon = button.children[0];

		const input = container.querySelector('input');

		if (input.type === 'password') {
			input.type = 'text';
			icon.classList.replace('fa-eye', 'fa-eye-slash');
		} else {
			input.type = 'password';
			icon.classList.replace('fa-eye-slash', 'fa-eye');
		}
	}

	function resetSearchInput(event) {
		const form = event.target.closest('form');
		const input = form.querySelector('input[type=search]');
		form.reset();

		input.value = '';
	}
});

function replaceWith(elementToReplace, contentToReplace) {
	const parent = elementToReplace.parentNode;
	const content = document.createElement('div');
	content.innerHTML = contentToReplace;
	parent.replaceChild(content.childNodes[0], elementToReplace);
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function capitalize(string) {
	return string[0].toUpperCase() + string.slice(1);
}
