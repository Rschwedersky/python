document.addEventListener('DOMContentLoaded', () => {
	const inputCnpj = document.querySelector('#modalPagarmeInfos .input_cnpj');
	inputCnpj.addEventListener('input', onlyNumbersOnInput);

	const inputTelephone = document.querySelector('#modalPagarmeInfos .input_telephone');
	inputTelephone.addEventListener('input', onlyNumbersOnInput);

	const inputCep = document.querySelector('#modalPagarmeInfos .input_cep');
	inputCep.addEventListener('input', onlyNumbersOnInput);

	const stepCompanyDataInputs = Array.from(
		document.querySelectorAll('#modalPagarmeInfos .step_company_data input')
	);
	stepCompanyDataInputs.forEach((singleInput) =>
		singleInput.addEventListener('keyup', canProceedStepCompanyData)
	);

	const stepCompanyAddressInputs = Array.from(
		document.querySelectorAll('#modalPagarmeInfos .step_company_address input')
	);
	stepCompanyAddressInputs.forEach((singleInput) =>
		singleInput.addEventListener('keyup', canProceedStepCompanyAddress)
	);

	const allStepsHeader = Array.from(document.querySelectorAll('.steps_header p'));
	allStepsHeader.forEach((singleStepHeader) =>
		singleStepHeader.addEventListener('click', goToStep)
	);

	const proceedBtns = Array.from(document.querySelectorAll('#modalPagarmeInfos .proceed'));
	proceedBtns.forEach((singleButton) => singleButton.addEventListener('click', proceedNextStep));

	function onlyNumbersOnInput(e) {
		let i = e.target.value.length;
		let str = e.target.value;
		let wasChar = false;
		if (isNaN(Number(str.charAt(i - 1)))) {
			wasChar = true;
			e.target.value = str.substr(0, i - 1);
		}

		if (e.target.closest('.step_company_data')) {
			canProceedStepCompanyData(e);
		} else if (e.target.closest('.step_company_address')) {
			canProceedStepCompanyAddress(e);
		}

		if (e.target.classList.contains('input_cnpj')) {
			maskCnpjInput(e);
		} else if (e.target.classList.contains('input_telephone')) {
			maskTelephoneInput(e);
		} else if (e.target.classList.contains('input_cep') && !wasChar) {
			maskCepInput(e);
		}
	}

	function maskCnpjInput(e) {
		let noMaskStr = e.target.value.replace(/\D/g, '');
		let length = noMaskStr.length;
		let maskedStr = '';
		for (i = 0; i < noMaskStr.length; i++) {
			maskedStr += noMaskStr[i];
			if ((i === 1 || i === 4) && length !== 2 && length !== 5) maskedStr += '.';
			else if (i === 7 && length !== 8) maskedStr += '/';
			else if (i === 11 && length !== 12) maskedStr += '-';
		}
		if (maskedStr.length > 18) {
			maskedStr = maskedStr.substr(0, 18);
		}
		e.target.value = maskedStr;
	}

	function maskTelephoneInput(e) {
		let noMaskStr = e.target.value.replace(/\D/g, '');
		let length = noMaskStr.length;
		let maskedStr = '(';
		for (i = 0; i < noMaskStr.length; i++) {
			if (i === 2 && length !== 2) maskedStr += ')';
			else if (
				(i === 6 && length <= 10 && length !== 7) ||
				(i === 7 && length >= 11 && length !== 8)
			)
				maskedStr += '-';
			maskedStr += noMaskStr[i];
		}
		if (maskedStr.length > 14) {
			maskedStr = maskedStr.substr(0, 14);
		}
		e.target.value = maskedStr;
	}

	async function maskCepInput(e) {
		let noMaskStr = e.target.value.replace(/\D/g, '');
		let maskedStr = '';
		for (i = 0; i < noMaskStr.length; i++) {
			maskedStr += noMaskStr[i];
			if (i === 4 && length !== 5) maskedStr += '-';
		}
		let transpassedLength = false;
		if (maskedStr.length > 9) {
			maskedStr = maskedStr.substr(0, 9);
			transpassedLength = true;
		}
		e.target.value = maskedStr;
		if (maskedStr.length == 9 && !transpassedLength) {
			// 0-9 only
			Swal.fire({
				title: translate['loading_zip_code_information'][language],
				timer: 1200,
				timerProgressBar: true,
				didOpen: () => {
					Swal.showLoading();
				},
			});
			const settings = {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			};
			const response = await fetch(
				`https://viacep.com.br/ws/${maskedStr.replace(/\D/g, '')}/json/`,
				settings
			);
			const responseJson = await response.json();
			if (responseJson['erro']) {
				Swal.fire(
					'Oops',
					translate['are_you_sure_you_entered_zip_code_correctly'][language]
				);
			} else {
				const stepCompanyAddress = document.querySelector(
					'#modalPagarmeInfos .step_company_address'
				);
				stepCompanyAddress.querySelector('.input_district').value = responseJson.bairro;
				stepCompanyAddress.querySelector('.input_city').value = responseJson.localidade;
				stepCompanyAddress.querySelector('.input_uf').value = responseJson.uf;
				stepCompanyAddress.querySelector('.input_street').value = responseJson.logradouro;
				stepCompanyAddress.querySelector('.input_number').focus();
			}
		}
	}

	function canProceedStepCompanyData(e) {
		const companyData = e.target.closest('.step_company_data');
		let error = false;
		if (companyData.querySelector('.input_company_name').value.length == 0) {
			error = true;
		}
		if (!validateCNPJ(companyData.querySelector('.input_cnpj').value)) {
			error = true;
		}
		if (companyData.querySelector('.input_telephone').value.length < 13) {
			error = true;
		}
		if (!validateEmail(companyData.querySelector('.input_email').value)) {
			error = true;
		}
		companyData.querySelector('.proceed').disabled = error;
	}

	function canProceedStepCompanyAddress(e) {
		const stepCompanyAddress = e.target.closest('.step_company_address');
		let error = false;
		if (stepCompanyAddress.querySelector('.input_cep').value.length < 9) {
			error = true;
		}
		if (stepCompanyAddress.querySelector('.input_street').value.length < 3) {
			error = true;
		}
		if (stepCompanyAddress.querySelector('.input_number').value.length == 0) {
			error = true;
		}
		if (stepCompanyAddress.querySelector('.input_district').value.length == 0) {
			error = true;
		}
		if (stepCompanyAddress.querySelector('.input_city').value.length == 0) {
			error = true;
		}
		if (stepCompanyAddress.querySelector('.input_uf').value.length == 0) {
			error = true;
		}
		stepCompanyAddress.querySelector('.proceed').disabled = error;
	}

	function goToStep(e) {
		if (e.target.classList.contains('company_data')) {
			document
				.querySelector('#modalPagarmeInfos .step_company_data')
				.classList.remove('d-none');
			document
				.querySelector('#modalPagarmeInfos .step_company_address')
				.classList.add('d-none');
		}
	}

	function proceedNextStep(e) {
		e.preventDefault();
		const stepCompanyData = e.target.closest('.step_company_data');
		if (stepCompanyData) {
			stepCompanyData.classList.add('d-none');
			document
				.querySelector('#modalPagarmeInfos .step_company_address')
				.classList.remove('d-none');
		}
	}

	const validateCNPJ = (cnpj) => {
		cnpj = cnpj.replace(/[^\d]+/g, '');

		if (cnpj == '') return false;

		if (cnpj.length != 14) return false;

		// Elimina CNPJs invalidos conhecidos
		if (
			cnpj == '00000000000000' ||
			cnpj == '11111111111111' ||
			cnpj == '22222222222222' ||
			cnpj == '33333333333333' ||
			cnpj == '44444444444444' ||
			cnpj == '55555555555555' ||
			cnpj == '66666666666666' ||
			cnpj == '77777777777777' ||
			cnpj == '88888888888888' ||
			cnpj == '99999999999999'
		)
			return false;

		// Valida DVs
		tamanho = cnpj.length - 2;
		numeros = cnpj.substring(0, tamanho);
		digitos = cnpj.substring(tamanho);
		soma = 0;
		pos = tamanho - 7;
		for (i = tamanho; i >= 1; i--) {
			soma += numeros.charAt(tamanho - i) * pos--;
			if (pos < 2) pos = 9;
		}
		resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
		if (resultado != digitos.charAt(0)) return false;

		tamanho = tamanho + 1;
		numeros = cnpj.substring(0, tamanho);
		soma = 0;
		pos = tamanho - 7;
		for (i = tamanho; i >= 1; i--) {
			soma += numeros.charAt(tamanho - i) * pos--;
			if (pos < 2) pos = 9;
		}
		resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
		if (resultado != digitos.charAt(1)) return false;

		return true;
	};
});

function validateEmail(email) {
	const re =
		/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	return re.test(String(email).toLowerCase());
}
