document.addEventListener('DOMContentLoaded', () => {
	const alertEl = document.createElement('span');
	const points = [15, 30, 40];

	const confirmEmail = document.getElementById('confirm_email')?.textContent
		? JSON.parse(document.getElementById('confirm_email').textContent)
		: null;

	const useService = document.getElementById('use_service')?.textContent
		? JSON.parse(document.getElementById('use_service').textContent)
		: null;

	const userAddedService = document.getElementById('new_service')?.textContent
		? JSON.parse(document.getElementById('new_service').textContent)
		: null;

	const inviteCrew = document.getElementById('invite_crew')?.textContent
		? JSON.parse(document.getElementById('invite_crew').textContent)
		: null;

	if (confirmEmail) {
		alertEl.textContent = `Parabéns, você ganhou +${points[0]} pontos!`;
		fireBootstrapAlert(alertEl);
	}

	if (userAddedService) {
		alertEl.textContent = `Parabéns, você ganhou +${points[1]} pontos!`;
		fireBootstrapAlert(alertEl);
	}

	if (useService) {
		alertEl.textContent = `Parabéns, você ganhou +${points[1]} pontos!`;
		fireBootstrapAlert(alertEl);
	}

	if (inviteCrew) {
		alertEl.textContent = `Parabéns, você ganhou +${points[0]} pontos!`;
		fireBootstrapAlert(alertEl);
	}

	function getRandomId() {
		return Math.floor(1000000000000000 + Math.random() * 9000000000000000)
			.toString(36)
			.substring(0, 10);
	}

	function fireBootstrapAlert(children) {
		if (!children) return;

		const alertElement = document.createElement('div');
		const alertId = `alert-${getRandomId()}`;

		styleAlert();

		alertElement.setAttribute('id', alertId);
		alertElement.setAttribute('role', 'alert');
		alertElement.prepend(children);

		document.body.prepend(alertElement);

		setTimeout(() => alertElement.remove(), 2500);

		function styleAlert() {
			alertElement.classList.add('alert', 'position-absolute');
			alertElement.style.top = '16rem';
			alertElement.style.left = '35%';
			alertElement.style.width = '22rem';
			alertElement.style.zIndex = '1000';
			alertElement.style.background = '#3C3E3E';
			alertElement.style.color = '#F7F7F7';
		}
	}
});
