let taskSocket = null;

connect();

function connect() {
	const protocol = location.protocol.includes('https') ? 'wss://' : 'ws://';
	taskSocket = new WebSocket(`${protocol}${window.location.host}/ws/models/state/`);
	taskSocket.onopen = (event) => {};

	taskSocket.onclose = (event) => {
		setTimeout(() => {
			connect();
		}, 2000);
	};

	taskSocket.onmessage = (event) => {
		const { model_id: modelId, new_state: state, message } = JSON.parse(event.data);

		updateAutomationBox(modelId, Number(state));
	};

	taskSocket.onerror = (err) => {
		taskSocket.close();
	};
}

function updateAutomationBox(modelId, state) {
	const boxes = Array.from(document.querySelectorAll(`.jsRealtime[data-id="${modelId}"]`));

	if (!boxes.length) return;

	let className;

	switch (state) {
		case 3:
			className = 'executing';
			break;
		case 4:
			className = 'error';
			break;
		case 6:
		case 7:
			className = 'success';
			break;
		default:
			return;
	}

	boxes.forEach((box) => {
		box.classList.remove('starting', 'executing', 'error', 'success');
		box.classList.add(className);

		if (box.querySelector('.jsExecutedOnDate')) {
			const now = new Date().toLocaleDateString();
			const executedOnEl = box.querySelector('.jsExecutedOnDate');
			executedOnEl.textContent = now;
		}

		if (className == 'error' || className == 'success') {
			const startAutomationBtn = box.querySelector('.crew__popup-menu button.iniciar');

			if (startAutomationBtn) startAutomationBtn.disabled = false;
		}
	});
}
