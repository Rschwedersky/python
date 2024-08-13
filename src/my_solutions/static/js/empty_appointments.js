document.addEventListener('DOMContentLoaded', function () {
	document.addEventListener('click', handleGotoMyservicesClick);

	function handleGotoMyservicesClick(e) {
		const isGotoMyservices =
			e.target.closest('.goto_myservices') || e.target.classList.contains('goto_myservices');
		if (isGotoMyservices) {
			const newTab = 'my_services';
			document.querySelector('.single_tab_header.active').classList.remove('active');
			document.querySelector('#all_scheduled_automations')?.classList.add('d-none');
			document
				.querySelector(`.single_tab_header[data-href=${newTab}]`)
				.classList.add('active');
			document.querySelector(`#${newTab}`).classList.remove('d-none');
		}
	}
});
