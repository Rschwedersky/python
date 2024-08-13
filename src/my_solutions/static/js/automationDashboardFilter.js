document.addEventListener('DOMContentLoaded', () => {
	const backOpacity = document.getElementById('back_opacity');
	const allSidebarMenuItems = document.querySelectorAll('#menu .single_menu');
	const filterButton = document.querySelector('#menu .single_menu.filter');
	const filterMenu = document.getElementById('filter_menu');
	const intervalDates = document.querySelector('#filter_menu .custom_period.set_interval');
	const customDates = document.querySelector('#filter_menu .custom_period.set_dates');

	backOpacity.addEventListener('click', (e) => {
		toggleFilter(true, filterButton);
	});
	allSidebarMenuItems.forEach((menuItem) =>
		menuItem.addEventListener('click', handleSideMenuClick)
	);
	filterMenu.addEventListener('click', handleFilterMenuClick);

	intervalDates.addEventListener('click', handleCustomPeriod);
	customDates.addEventListener('click', handleCustomPeriod);

	document.addEventListener('click', delegateEvents);

	function handleCustomPeriod(e) {
		if (!e.currentTarget.classList.contains('active')) {
			document.querySelector('#filter_menu .custom_period.active').classList.remove('active');
			e.currentTarget.classList.add('active');
			const customDates = document.querySelector('#filter_menu .custom_dates');
			if (e.currentTarget.classList.contains('set_dates')) {
				customDates.classList.remove('d-none');
				customDates.classList.add('d-flex');
			} else {
				customDates.classList.add('d-none');
				customDates.classList.remove('d-flex');
			}
		}
	}

	function handleSideMenuClick(event) {
		event.preventDefault();
		const targetSingleMenu = event.currentTarget;
		if (targetSingleMenu.classList.contains('filter')) {
			toggleFilter(targetSingleMenu.classList.contains('active'), targetSingleMenu);
		} else if (!targetSingleMenu.classList.contains('active')) {
			if (filterButton.classList.contains('active')) {
				toggleFilter(true, filterButton);
			}
			const targetTab = document.getElementById(targetSingleMenu.dataset.idtab);
			if (targetTab) {
				openTab(targetSingleMenu, targetTab);
			}
		}
	}

	function toggleFilter(isOpened = false, filterOnMenu) {
		if (isOpened) {
			backOpacity.classList.remove('active');
			document.getElementById('filter_menu').classList.remove('active');
			filterOnMenu.classList.remove('active');
		} else {
			backOpacity.classList.add('active');
			document.getElementById('filter_menu').classList.add('active');
			filterOnMenu.classList.add('active');
		}
	}

	function handleApplyFilters(e) {
		const button = e.target;
		replaceWith(button, getLoadingDiv());

		const { dateFrom, dateTo } = getDateRange();
		const allData = controller.getAllData();
		const result = getDataWithFilteredDate(allData, dateFrom, dateTo);
		const { services, models, status } = getSelectedFilters();

		const finalData = getFinalData();

		const customEvent = new CustomEvent('filterApplied', {
			detail: finalData,
		});

		document.dispatchEvent(customEvent);

		replaceWith(document.querySelector('.loading_div'), button.outerHTML);

		toggleFilter(true, filterButton);

		function getFinalData() {
			const finalData = {};
			Object.entries(result).forEach(([key, value]) => {
				value.forEach((item) => {
					if (
						services.includes(item.automation_name) &&
						models.includes(item.schedule_name) &&
						status.includes(item.task_status)
					) {
						if (!finalData[key]) {
							finalData[key] = [];
						}
						finalData[key].push(item);
					}
				});
			});
			return finalData;
		}
	}

	function getSelectedFilters() {
		const servicesSet = new Set();
		const modelsSet = new Set();
		const statusSet = new Set();

		const checked = Array.from(filterMenu.querySelectorAll('.all_filters input:checked'));

		checked.forEach((input) => {
			if (input.value === 'Todos') return;

			const value = input
				.closest('label')
				?.querySelector('.limitoneline')
				?.textContent?.trim();

			if (!value) return;

			if (input.name === 'services') {
				servicesSet.add(value);
			} else if (input.name === 'model') {
				modelsSet.add(value);
			} else if (input.name === 'status') {
				statusSet.add(value);
			} else {
				return;
			}
		});

		const services = Array.from(servicesSet);
		const models = Array.from(modelsSet);
		const status = Array.from(statusSet);

		return { services, models, status };
	}

	function getDataWithFilteredDate(data, dateFrom, dateTo) {
		return filterObjectWithKeys(data, (date) => {
			const dateInCorrectFormat = new Date(date);
			const dateFromInCorrectFormat = new Date(dateFrom);
			const dateToInCorrectFormat = new Date(dateTo);

			return (
				dateInCorrectFormat >= dateFromInCorrectFormat &&
				dateInCorrectFormat <= dateToInCorrectFormat
			);
		});
	}

	function filterObjectWithKeys(obj, predicate) {
		return Object.keys(obj)
			.filter((key) => predicate(key))
			.reduce((res, key) => ((res[key] = obj[key]), res), {});
	}

	function getDateRange() {
		let dateFrom, dateTo;

		const isCustomPeriod = document
			.querySelector('#filter_menu .custom_period.set_dates')
			.classList.contains('active');

		if (isCustomPeriod) {
			dateFrom = formatDate(document.querySelector('#filter_menu .from_datetime').value);
			dateTo = formatDate(document.querySelector('#filter_menu .to_datetime').value);
		} else {
			const interval = Number(
				document.querySelector('#filter_menu .custom_period.set_interval').value
			);

			const now = new Date();
			const intervalDate = new Date(new Date().setDate(now.getDate() - interval));

			dateFrom = formatDate(intervalDate.toLocaleDateString('pt-BR'));

			dateTo = formatDate(now.toLocaleDateString('pt-BR'));
		}

		if (!dateFrom || !dateTo) return;

		return { dateFrom, dateTo };

		function formatDate(date) {
			try {
				const splitted = date.split('/');
				const updatedDate = `${splitted[2]}-${splitted[1]}-${splitted[0]}`;
				return updatedDate;
			} catch (error) {
				return false;
			}
		}
	}

	function handleFilterMenuClick(event) {
		const target = event.target;
		if (target.classList.contains('clean')) {
			handleClearSingleFilter(target);
		} else if (target.classList.contains('apply_filters')) {
			handleApplyFilters(event);
		} else if (target.value === 'Todos') {
			const container = target.closest('.options');
			checkAllFilters(container);
		}
	}

	function handleClearSingleFilter(cleanBtn) {
		const singleFilter = cleanBtn.closest('.single_filter');
		clearSingleFilter(singleFilter);
	}

	function checkAllFilters(section) {
		const thisSectionFilters = section.querySelectorAll('input:not(:checked)');

		thisSectionFilters.forEach((filter) => (filter.checked = true));
	}

	function clearSingleFilter(singleFilter) {
		const allSelected = Array.from(singleFilter.querySelectorAll('.options input:checked'));
		allSelected.map((selected) => {
			selected.checked = false;
		});

		singleFilter.querySelector('.selected_text p').innerHTML = translate['all_male'][language];
	}

	function delegateEvents(event) {
		const openedSingleFilter = document.querySelector('.single_filter.active');
		if (openedSingleFilter) {
			const clickInsideFilter =
				event.target.classList.contains('single_filter') ||
				event.target.closest('.single_filter');
			if (!clickInsideFilter) {
				if (openedSingleFilter.classList.contains('subprocesses')) {
					addSubProcessesSelected(openedSingleFilter);
				}
				openedSingleFilter.classList.remove('active');
				openedSingleFilter.querySelector('.fake_select').classList.remove('active');
			}
		}
	}

	function openTab(targetSingleMenu, targetTab) {
		document.querySelector('#root #menu .single_menu.active').classList.remove('active');
		document.querySelector('.dashboard_tab').classList.remove('active');
		targetSingleMenu.classList.add('active');
		targetTab.classList.add('active');
	}
});
