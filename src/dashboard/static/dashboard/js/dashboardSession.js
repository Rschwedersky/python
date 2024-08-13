document.addEventListener('DOMContentLoaded', () => {
	initDashboardSession();

	function initDashboardSession() {
		const dashboardHTML = document.getElementById('root');

		if (!dashboardHTML) return;

		dashboardHTML.addEventListener('beforeunload', saveEndOfDashboardSession);
		dashboardHTML.addEventListener('click', saveEndOfDashboardSession);

		const sessionCookieExists = Boolean(localStorage.getItem('dashboardSectionBeginning'));
		if (sessionCookieExists) {
			checkIfNeedsNewDashboardSession();
		} else {
			localStorage.setItem('dashboardSectionBeginning', Date.now());
			localStorage.removeItem('dashboardSectionEnd');
		}
	}

	function saveEndOfDashboardSession() {
		initDashboardSession();
		const now = Date.now();

		localStorage.setItem('dashboardSectionEnd', now);
	}

	function checkIfNeedsNewDashboardSession() {
		const sessionLastInteraction = localStorage.getItem('dashboardSectionEnd');
		const lastInteractionExists = Boolean(sessionLastInteraction);

		if (lastInteractionExists) {
			const now = Date.now();
			const diffTime = Math.abs(now - sessionLastInteraction);
			const diffHours = Number(diffTime / (1000 * 60 * 60));
			const sessionIsExpired = diffHours >= 1;

			if (sessionIsExpired) {
				saveDashboardSessionToDatabase();
				createNewDashboardSession();
			}
		}
	}

	async function saveDashboardSessionToDatabase() {
		const csrftoken = getCookie('csrftoken');

		const sessionStart = Number(localStorage.getItem('dashboardSectionBeginning'));
		const sessionEnd = Number(localStorage.getItem('dashboardSectionEnd'));

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

		const response = await fetch('/metrics/dashboard', settings);
	}
	function createNewDashboardSession() {
		localStorage.removeItem('dashboardSectionBeginning');
	}
});
