document.addEventListener('DOMContentLoaded', () => {
	const visibilityIcon = document.getElementById('view_password');

	visibilityIcon.addEventListener('click', togglePasswordVisibility);

	function togglePasswordVisibility(event) {
		const icon = event.currentTarget;
		const input = icon.closest('div')?.querySelector('input');
		if (!input) return;

		if (input.type === 'password') {
			input.type = 'text';
			icon.src = icon.src.replace('on', 'off');
		} else {
			input.type = 'password';
			icon.src = icon.src.replace('off', 'on');
		}
	}
});
