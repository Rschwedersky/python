document.addEventListener('DOMContentLoaded', function () {
	const gotoMyservices = document.querySelector('.noservices .goto_myservices');

	gotoMyservices?.addEventListener('click', handleGotoMyservicesClick);

	function handleGotoMyservicesClick(e) {
		e.preventDefault();

		const newTab = 'my_services';
		document.querySelector('.single_tab_header.active').classList.remove('active');
		document.querySelector('#all_schedules').classList.add('d-none');
		document.querySelector(`.single_tab_header[data-href=${newTab}]`).classList.add('active');
		document.querySelector(`#${newTab}`).classList.remove('d-none');
	}
});
