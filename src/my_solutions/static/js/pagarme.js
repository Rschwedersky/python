document.addEventListener('DOMContentLoaded', () => {
	const payButton = document.getElementById('submitEndOfTrialPlanButton');
	const pagarmeEncryptionKey = document.getElementById('pagarmeEncryptionKey').value;
	document.getElementById('pagarmeEncryptionKey').remove();
	const form = document.querySelector('form.js-submit-form');

	addPayEventListener();

	function addPayEventListener() {
		if (payButton.classList.contains('allow-payment')) {
			payButton.addEventListener('click', function (e) {
				e.preventDefault();
				openModalPaymentInfos();
			});
			const checkoutPagarme = document.querySelector(
				'#modalPagarmeInfos .step_company_address .proceed'
			);
			checkoutPagarme.addEventListener('click', function (e) {
				checkoutSubmit(payButton, form, e);
			});
		} else {
			payButton.addEventListener('click', function (e) {
				submitPlanOption(e);
			});
		}
	}

	function openModalPaymentInfos() {
		const modal = document.getElementById('modalPagarmeInfos');
		let bootstrapModal = new bootstrap.Modal(modal);
		bootstrapModal.show();
		document.querySelector('.modal-backdrop').classList.add('harder-opacity');
	}

	function closeModalPaymentInfos() {
		$('#modalPagarmeInfos').modal('hide');
		document.querySelector('.modal-backdrop').remove();
	}

	function checkoutSubmit(payButton, form, event) {
		closeModalPaymentInfos();

		var checkout = new PagarMeCheckout.Checkout({
			encryption_key: pagarmeEncryptionKey,
			success: function (data) {
				submitPaymentInfos(data, event);
			},
			error: function (err) {
				console.log(err);
				Swal.fire('Oops', 'Houve algum erro no pagamento!', 'error');
			},
			close: function () {
				hideLoading(payButton);
			},
		});

		showLoading(payButton);

		const chosenPeriod = getInputChosenPeriod(form);

		const price = getPlanValue(form, chosenPeriod);
		const companyInfosForm = document.querySelector('#modalPagarmeInfos form');

		const inputTelephone = companyInfosForm.querySelector('.input_telephone').value.split(')');
		checkout.open({
			amount: price * 100,
			customerData: 'false',
			createToken: 'false',
			paymentMethods: 'boleto,credit_card',
			customerName: companyInfosForm.querySelector('.input_company_name').value.trim(),
			customerDocumentNumber: companyInfosForm
				.querySelector('.input_cnpj')
				.value.replace(/[^\d]+/g, ''),
			customerEmail: companyInfosForm.querySelector('.input_email').value,
			customerAddressStreet: companyInfosForm.querySelector('.input_street').value,
			customerAddressStreetNumber: companyInfosForm.querySelector('.input_number').value,
			customerAddressComplementary: companyInfosForm.querySelector('.input_complement').value,
			customerAddressNeighborhood: companyInfosForm.querySelector('.input_district').value,
			customerAddressCity: companyInfosForm.querySelector('.input_city').value,
			customerAddressZipcode: companyInfosForm
				.querySelector('.input_cep')
				.value.replace(/[^\d]+/g, ''),
			customerAddressState: companyInfosForm.querySelector('.input_uf').value,
			customerPhoneDdd: inputTelephone[0].replace(/[^\d]+/g, ''),
			customerPhoneNumber: inputTelephone[1].replace(/[^\d]+/g, ''),
		});
	}

	async function submitPaymentInfos(payload, event) {
		payload['plan'] = getAllPlanInfos();
		payload['chosen_period'] = getInputChosenPeriod(form);

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(payload),
		};
		const response = await fetch('/pay/subscription', settings);
		const responseJson = await response.json();
		if (responseJson['status'] == 200) {
			submitPlanOption(event);
		} else {
			hideLoading(payButton);
			Swal.fire('Oops..', responseJson['msg'], 'error');
		}
	}
});

const getAllPlanInfos = () => {
	let plan = getPlan();
	const form = document.querySelector('form.js-submit-form');

	const chosenPeriod = getInputChosenPeriod(form);
	const price = getPlanValue(form, chosenPeriod);

	if (plan != 'business' || price > 0) {
		plan += chosenPeriod == 'yearly' ? `_anual` : `_${chosenPeriod}`;

		let customSwitch = form.querySelector('.custom__switch input:checked');
		if (customSwitch) {
			plan += `_plus`;
		}

		const allCheckboxServices = Array.from(
			form.querySelectorAll('.free-trial__end--plans .single_checkbox input')
		);
		const withDashboard = allCheckboxServices.filter((checkbox) => {
			const container = checkbox.closest('.trial__choose-plan-service-box');
			const service = container.dataset.service;
			return service == 'dashboard';
		});
		if (withDashboard.length > 0) {
			plan += `_with_dashboard`;
		}
	} else {
		plan = form.getElementById('trialPlan').value;
	}

	return plan;
};
