$(document).ready(function () {
	const allSingleTabHeader = Array.from(
		document.querySelectorAll('#services .tab_header .single_tab_header')
	);

	allSingleTabHeader.forEach((singleTabHeader) => {
		singleTabHeader.addEventListener('click', handleClickTabHeader);
	});

	async function handleClickTabHeader(e) {
		e.preventDefault();
		let $this = e.currentTarget;
		if (!$this.classList.contains('active')) {
			let old_tab = document.querySelector('.single_tab_header.active');
			old_tab.classList.remove('active');
			document.getElementById(old_tab.dataset.href).classList.add('d-none');
			$this.classList.add('active');
			let newTab = document.getElementById($this.dataset.href);
			newTab.classList.remove('d-none');
			if (newTab.querySelector('.loading_div')) {
				const settings = {
					method: 'GET',
					headers: {
						'X-CSRFToken': getCookie('csrftoken'),
					},
				};
				fetch(`/services/singletab/${$this.dataset.href}`, settings)
					.then(function (response) {
						// The API call was successful!
						return response.text();
					})
					.then(function (html) {
						// This is the HTML from our response as a text string
						newTab.querySelector('.py-5').innerHTML = html;
						loadSingleTabScripts($this.dataset.href);
					})
					.catch(function (err) {
						// There was an error
						Swal.fire('Oops..', 'Error', 'warning');
					});
			}
		}
	}
});
