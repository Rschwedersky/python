document.addEventListener('DOMContentLoaded', () => {
	const fileInput = document.getElementById('file-picker');
	if (!fileInput) return;
	const fileContainer = fileInput.closest('.file-container');
	const buttonsToClearInput = document.querySelectorAll('.js-remove-file');
	const dropZone = document.getElementById('drop_zone');

	const csrftoken = getCookie('csrftoken');

	fileInput.addEventListener('change', handleFileInput);

	buttonsToClearInput.forEach((button) => button.addEventListener('click', clearInput));

	dropZone.addEventListener('drop', dropHandler);
	dropZone.addEventListener('dragover', dragOverHandler);

	function handleFileInput(event) {
		const input = event.currentTarget;
		const file = input.files[0];
		checkAndAddFile(file);
	}

	async function checkAndAddFile(file) {
		const stepContainer = document.querySelector(
			document.querySelector('.stepper-item.active').dataset.href
		);
		const uploader = stepContainer.querySelector('.uploader');
		uploader.classList.add('d-none');

		const loading = getLoading(stepContainer, translate['checking_your_input_file'][language]);

		const advanceButton = fileInput.closest('.setup-content')?.querySelector('.nextBtn');

		const dataTransfer = new DataTransfer();

		stepContainer.classList.add('justify-content-center', 'align-items-center');

		const service = stepContainer.closest('#modalExemplo').dataset.automation;

		const fileIsValid = await checkIfFileIsValid(file, service);

		if (fileIsValid) {
			showFileInfo(file);
			if (advanceButton) {
				advanceButton.disabled = false;
			}

			dataTransfer.items.add(file);
		} else {
			if (advanceButton) {
				advanceButton.disabled = true;
			}
		}
		fileInput.files = dataTransfer.files;
		loading.remove();

		uploader.classList.remove('d-none');
		stepContainer.classList.remove('justify-content-center', 'align-items-center');
	}

	async function checkIfFileIsValid(file, service) {
		const formData = new FormData();
		formData.append('file', file);

		formData.append('automation', service);

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
			},
			body: formData,
		};

		let errorExists = false;

		try {
			const response = await fetch('/services/check/file', settings);
			if (!response.ok) {
				const convertedResponse = await response.json();
				const errorMessage =
					convertedResponse['payload']?.replaceAll('\n', '<br>') ||
					translate['unsupported_file'][language];

				throw new Error(`${errorMessage}`);
			}
		} catch (error) {
			const errorMessage =
				error.name != 'Error'
					? `${translate['unsupported_file'][language]}.`
					: `${error.message}.`;

			errorExists = true;

			Swal.fire('Oops..', errorMessage, 'error');
		} finally {
			return errorExists ? false : true;
		}
	}

	function clearInput(event) {
		const target = event.currentTarget;
		const targetInput = target
			.closest('.file-container')
			.querySelector('input:not([type="hidden"])');
		const advanceBtn = target.closest('.setup-content').querySelector('.btn-advance');

		targetInput.files = new DataTransfer().files;
		fileContainer.classList.remove('with-file');
		advanceBtn.disabled = true;
	}

	function dropHandler(event) {
		event.preventDefault();

		let file;
		let moreThanOneFile = false;

		if (event.dataTransfer.items) {
			if (event.dataTransfer.items.length > 1) moreThanOneFile = true;

			file = event.dataTransfer.items[0].getAsFile();
		} else {
			if (event.dataTransfer.files.length > 1) moreThanOneFile = true;
			file = event.dataTransfer.files[0];
		}

		if (moreThanOneFile) {
			return Swal.fire(
				'Oops..',
				translate['only_one_file_can_be_added_at_a_time'][language],
				'error'
			);
		} else if (file.size > 2100000) {
			return Swal.fire(
				'Oops..',
				translate['the_inserted_file_exceeds_the_size_limit'][language],
				'error'
			);
		}

		if (file) {
			checkAndAddFile(file);
		}
	}

	function dragOverHandler(ev) {
		// Prevent default behavior (Prevent file from being opened)
		ev.preventDefault();
	}

	function getLoading(elementToAppend, title) {
		const container = document.createElement('div');
		container.id = 'loading-container';
		container.innerHTML = `<div class="loader"></div>`;
		elementToAppend.appendChild(container);

		if (title) {
			const element = document.createElement('p');
			element.classList.add('mb-4');
			element.textContent = `${title}...`;
			container.prepend(element);
			container.classList.add(
				'd-flex',
				'flex-column',
				'justify-content-center',
				'align-items-center',
				'mx-auto'
			);
		}
		return container;
	}
});

function addFakeFileUpload(name) {
	name_array = name.split('.');

	showFileInfo({ name, size: null });
}

function showFileInfo(file) {
	const fileContainer = document.querySelector('.setup-content .file-container');
	fileContainer.classList.add('with-file');
	const fileNameEl = fileContainer.querySelector('.js-file-name');
	const fileSizeEl = fileContainer.querySelector('.js-file-size');

	fileNameEl.textContent = file.name;
	if (file.size) {
		fileSizeEl.textContent = formatBytes(file.size);
	} else {
		fileContainer.querySelector('input[type="file"]').classList.add('js-fake');
	}

	function formatBytes(bytes, decimals = 2) {
		if (bytes == 0) return '0 Bytes';

		const k = 1024;
		const checkedDecimals = decimals < 0 ? 0 : decimals;
		const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

		const baseOfNumber = Math.floor(Math.log(bytes) / Math.log(k));
		const formattedSize = parseFloat(
			(bytes / Math.pow(k, baseOfNumber)).toFixed(checkedDecimals)
		);
		const readableSize = `${formattedSize} ${sizes[baseOfNumber]}`;

		return readableSize;
	}
}
