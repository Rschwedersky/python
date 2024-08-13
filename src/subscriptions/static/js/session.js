window.addEventListener('DOMContentLoaded', () => {
	window.addEventListener('beforeunload', saveEndOfSession);
	window.addEventListener('click', saveEndOfSession);

	init();

	function init() {
		const sessionCookieExists = Boolean(localStorage.getItem('sectionBeginning'));
		if (sessionCookieExists) {
			checkIfNeedsNewSession();
		} else {
			localStorage.setItem('sectionBeginning', Date.now());
			localStorage.removeItem('sectionEnd');
		}
	}

	function saveEndOfSession() {
		init();
		const now = Date.now();

		localStorage.setItem('sectionEnd', now);
	}

	function checkIfNeedsNewSession() {
		const sessionLastInteraction = localStorage.getItem('sectionEnd');
		const lastInteractionExists = Boolean(sessionLastInteraction);

		if (lastInteractionExists) {
			const now = Date.now();
			const diffTime = Math.abs(now - sessionLastInteraction);
			const diffHours = Number(diffTime / (1000 * 60 * 60));
			const sessionIsExpired = diffHours >= 1;

			if (sessionIsExpired) {
				saveSessionToDatabase();
				createNewSession();
			}
		}
	}

	async function saveSessionToDatabase() {
		const csrftoken = getCookie('csrftoken');

		const sessionStart = Number(localStorage.getItem('sectionBeginning'));
		const sessionEnd = Number(localStorage.getItem('sectionEnd'));

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				session_start: sessionStart,
				session_end: sessionEnd,
			}),
		};

		const response = await fetch('/metrics/login', settings);
	}
	function createNewSession() {
		localStorage.removeItem('sectionBeginning');
	}
});
