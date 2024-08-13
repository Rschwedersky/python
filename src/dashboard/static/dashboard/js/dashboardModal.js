document.addEventListener('DOMContentLoaded', () => {
	const modal = document.getElementById('dashboard-modal');

	$(modal).on('show.bs.modal', handleBootstrapModal);

	function handleBootstrapModal(event) {
		const button = event.relatedTarget;
		const modal = event.currentTarget;
		const modalDialog = modal.querySelector('.modal-dialog');
		const modalFooter = modal.querySelector('.modal-footer');
		const modalCancelBtn = modalFooter.querySelector('.jsCancelBtn');
		const modalAdvanceBtn = modalFooter.querySelector('.jsAdvanceBtn');

		const action = button.getAttribute('data-modal');
		const config = {
			containerClasses: [],
			footerClasses: [],
			advanceBtnClasses: [],
			cancelBtnClasses: [],
		};
		const isReturning = button === modalCancelBtn;

		switch (action) {
			case 'how-it-works-roi':
				config.modalTitle = 'Retorno por Investimento (ROI)';
				config.advanceBtnClasses.push('mx-auto', 'w-25');
				config.advanceBtnText = 'OK';
				config.advanceBtnDisabled = false;
				config.advanceBtnDismiss = true;
				config.modalSize = 'lg';
				break;
			case 'empty-state-roi':
				config.modalTitle = 'Retorno por Investimento (ROI)';
				config.advanceBtnClasses.push('jsProcessBtn');
				config.advanceBtnText = 'Ir para Processos';
				config.cancelBtnText = 'Continuar no ROI';
				config.cancelBtnClasses.push('secondary');
				config.footerClasses.push('justify-content-around');
				config.advanceBtnDisabled = false;
				config.advanceBtnClickHandler = showManageProcessesTab;
				break;
			case 'history-roi':
				config.modalTitle = 'Histórico de ROI';
				config.advanceBtnClasses.push('mx-auto', 'w-25');
				config.advanceBtnText = 'OK';
				config.advanceBtnDisabled = false;
				config.advanceBtnDismiss = true;
				break;
			case 'how-it-works-rpa':
				config.modalTitle = `${translate['rpa_runtime'][language]}`;
				config.advanceBtnClasses.push('mx-auto', 'w-25');
				config.advanceBtnText = 'OK';
				config.advanceBtnDisabled = false;
				config.advanceBtnDismiss = true;
				break;
			case 'robots_tab_modal':
				config.modalTitle = 'Ocupação e execuções';
				config.advanceBtnClasses.push('mx-auto', 'w-25');
				config.advanceBtnText = 'OK';
				config.advanceBtnDisabled = false;
				config.advanceBtnDismiss = true;
				break;
			case 'hours-returned':
				config.modalTitle = 'Horas Retornadas';
				config.advanceBtnClasses.push('mx-auto', 'w-25');
				config.advanceBtnText = 'OK';
				config.advanceBtnDisabled = false;
				config.advanceBtnDismiss = true;
				config.modalSize = 'lg';
				break;
			default:
				break;
		}

		const modalTitle = modal.querySelector('.modal-title');
		const allModalBodyOptions = Array.from(modal.querySelector('.modal-body').children);

		const desiredModalBody = modal.querySelector(
			`[data-identifier="${config.modalBody || action}"]`
		);

		modalTitle.textContent = config.modalTitle || '';

		if (config.cancelBtnText) {
			modalCancelBtn.textContent = config.cancelBtnText || '';
			modalCancelBtn.classList.remove('d-none');
		} else {
			modalCancelBtn.classList.add('d-none');
		}

		modalAdvanceBtn.textContent = config.advanceBtnText || '';

		modalAdvanceBtn.disabled = config.advanceBtnDisabled === false ? false : true;

		config.containerClasses.forEach((className) => desiredModalBody.classList.add(className));

		config.advanceBtnClasses.forEach((className) => modalAdvanceBtn.classList.add(className));

		config.cancelBtnClasses.forEach((className) => modalCancelBtn.classList.add(className));

		config.footerClasses.forEach((className) => modalFooter.classList.add(className));

		if (!config.advanceBtnClasses.includes('right-arrow')) {
			modalAdvanceBtn.classList.remove('right-arrow');
		}

		if (config.advanceBtnDismiss) {
			modalAdvanceBtn.setAttribute('data-dismiss', 'modal');
		} else {
			modalAdvanceBtn.removeAttribute('data-dismiss');
		}

		if (config.advanceBtnClickHandler) {
			modalAdvanceBtn.addEventListener('click', config.advanceBtnClickHandler);
		}

		if (!isReturning) desiredModalBody.querySelectorAll('form').forEach((form) => form.reset());

		if (config.modalSize) {
			modalDialog.classList.add(`modal-${config.modalSize}`);
		} else {
			modalDialog.classList.remove('modal-sm', 'modal-lg', 'modal-xl');
		}

		allModalBodyOptions.forEach((bodyOption) => {
			if (bodyOption == desiredModalBody) {
				bodyOption.classList.remove('d-none');
			} else if (bodyOption.classList.contains('modal-stepper-container')) {
				return;
			} else {
				bodyOption.classList.add('d-none');
			}
		});
	}

	function showManageProcessesTab(event) {
		const { target } = event;
		getProcess().done(() => updateJsAfterContentIsShown());
		const singleMenu = document.querySelector('.single_menu.config');
		const tab = document.getElementById(singleMenu.dataset.idtab);
		openTab(singleMenu, tab);
		target.removeEventListener('click', showManageProcessesTab);
		$(modal).modal('hide');
	}
});
