document.addEventListener('DOMContentLoaded', () => {
	if (!document.getElementById('root')) return;
	const backOpacity = document.getElementById('back_opacity');
	const allSingleMenu = document.querySelectorAll('#menu .single_menu');
	const filterButton = document.querySelector('#menu .single_menu.filter');
	const filterMenu = document.getElementById('filter_menu');
	document.addEventListener('changeDate', handleFilterDateChange);

	backOpacity.addEventListener('click', (e) => {
		toggleFilter(true, filterButton);
	});
	allSingleMenu.forEach((singleMenu) =>
		singleMenu.addEventListener('click', handleSideMenuClick)
	);
	filterMenu.addEventListener('change', handleFilterMenuChange);
	filterMenu.addEventListener('click', handleFilterMenuClick);

	document.addEventListener('click', handleAnyClick);

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

	function handleFilterMenuChange(e) {
		if (e.target.type == 'checkbox') {
			handleFiltersChange(e.target);
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
		replaceWith(e.target, getLoadingDiv());

		const rangeDate = getActiveDates();
		const dateFrom = rangeDate['date_from'];
		const dateTo = rangeDate['date_to'];

		const allDates = Object.keys(lastDashboardJson['dates']);
		if (!allDates.length) {
			getNewDashboardJson();
		} else {
			const limitDateFrom = allDates[0].replaceAll('_', '-');
			const limitDateTo = allDates[allDates.length - 1].replaceAll('_', '-');
			if (limitDateFrom == dateFrom && limitDateTo == dateTo) {
				const activeMenu = document.querySelector('#menu .single_menu.active');
				plotOnTab(lastDashboardJson, activeMenu.dataset.idtab);
			} else {
				getNewDashboardJson();
			}
		}
	}

	function handleFilterMenuClick(event) {
		const target = event.target;
		if (target.classList.contains('jsCleanSingleFilter')) {
			handleClearSingleFilter(target);
		} else if (target.classList.contains('jsCleanAllFilters')) {
			const allClearButtons = document.querySelectorAll('#filter_menu .jsCleanSingleFilter');

			allClearButtons.forEach((cleanBtn, index) =>
				index > 0
					? handleClearSingleFilter(cleanBtn, false)
					: handleClearSingleFilter(cleanBtn)
			);
			makeNonActiveTabsRefreshable();
		} else if (target.classList.contains('apply_filters')) {
			handleApplyFilters(event);
			makeNonActiveTabsRefreshable();
		}
	}

	function handleClearSingleFilter(cleanBtn, plot = true) {
		const singleFilter = cleanBtn.closest('.single_filter');
		clearSingleFilter(singleFilter);
		const activeMenu = document.querySelector('#menu .single_menu.active');

		if (plot) {
			plotOnTab(lastDashboardJson, activeMenu.dataset.idtab);
		}
	}

	function clearSingleFilter(singleFilter) {
		let type = singleFilter.querySelector('.filters').dataset.type;
		let allSelected = Array.from(singleFilter.querySelectorAll('.options input:checked'));
		allSelected.map((val, i) => {
			let index = globalFilter[type].indexOf(val.value);
			globalFilter[type].splice(index, 1);
			val.checked = false;
		});
		singleFilter.querySelector('.selected_text p').innerHTML = 'Todos';
	}

	function handleFiltersChange(input) {
		if (input.checked) {
			if (input.value == 'all_filters') {
				const allFilters = input.closest('.options').querySelectorAll('input');
				addAllFiltersToGlobalFilter(allFilters, input.name, input.checked);
			} else {
				addFilterToGlobalFilter(input);
			}
		} else {
			if (input.value == 'all_filters') {
				const allFilters = input
					.closest('.options')
					.querySelectorAll('.all_single_filters input');
				removeAllFiltersFromGlobalFilter(allFilters, input.checked);
			} else {
				removeFilterFromGlobalFilter(input);
			}
		}
		handleMarkedCheckboxCount(input);
	}

	function handleFilterDateChange(e) {
		let dateTarget = e.detail.inputTarget;
		let isvalid_date = new Date(getDateFormat(dateTarget.value));

		let rangeDate = getActiveDates();

		if (dateTarget.classList.contains('to_datetime')) {
			let old_datefrom = new Date(rangeDate['date_from']);
			if (old_datefrom.getTime() - isvalid_date.getTime() > 0) {
				Swal.fire('Oops..', 'A data final necessita ser maior que a inicial', 'warning');
				let oneMonth = new Date(getDateFormat(rangeDate['date_from'], true));
				oneMonth.setDate(oneMonth.getDate() + 30);
				// Create the event
				var dateInputEvent = new CustomEvent('changeDateInputCalendar', {
					detail: {
						input: dateTarget,
						newDate: oneMonth,
					},
				});
				// Dispatch/Trigger/Fire the event
				document.dispatchEvent(dateInputEvent);
			}
		} else {
			let old_dateto = new Date(rangeDate['date_to']);
			if (isvalid_date.getTime() - old_dateto.getTime() > 0) {
				Swal.fire('Oops..', 'A data inicial necessita ser menor que a final', 'warning');
				let oneMonth = new Date(getDateFormat(rangeDate['date_to'], true));
				oneMonth.setDate(oneMonth.getDate() - 30);
				// Create the event
				var dateInputEvent = new CustomEvent('changeDateInputCalendar', {
					detail: {
						input: dateTarget,
						newDate: oneMonth,
					},
				});
				// Dispatch/Trigger/Fire the event
				document.dispatchEvent(dateInputEvent);
			}
		}
	}

	function handleAnyClick(event) {
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
});

function removeAllFiltersFromGlobalFilter(allFilters, isAllFiltersChecked = false) {
	allFilters.forEach((singleFilter) => {
		singleFilter.checked = isAllFiltersChecked;
		removeFilterFromGlobalFilter(singleFilter);
	});
}

function addAllFiltersToGlobalFilter(allFilters, type, isAllFiltersChecked = true) {
	globalFilter[type] = [];
	allFilters.forEach((singleFilter) => {
		singleFilter.checked = isAllFiltersChecked;
		addFilterToGlobalFilter(singleFilter);
	});
}

function handleMarkedCheckboxCount(input, singleFilterElement = '') {
	if (singleFilterElement == '') {
		singleFilterElement = input.closest('.single_filter');
	}
	let allChecked = singleFilterElement.querySelectorAll('.all_single_filters input:checked');
	let numberOfCheckedInputs = allChecked.length;
	let headerElement = singleFilterElement.querySelector('.selected_text .resume_choices_text');
	let selectedText = '';
	let howmanySelected = '';
	if (
		singleFilterElement.querySelectorAll('.all_single_filters input').length ==
		numberOfCheckedInputs
	) {
		selectedText = singleFilterElement.classList.contains('area')
			? translate['all'][language]
			: translate['all_male'][language];
	} else if (numberOfCheckedInputs == 0) {
		selectedText = 'Nenhum item selecionado';
	} else {
		let resp = addTextWithoutOverflowing(allChecked, headerElement.offsetWidth);
		selectedText = resp['textResult'];
		howmanySelected = resp['howManyOverflowing'];
	}

	headerElement.innerHTML = selectedText;
	singleFilterElement.querySelector('.selected_text .howmany_selected').innerHTML =
		howmanySelected;
}

function addTextWithoutOverflowing(allWords, widthLimit) {
	let textResult = '';
	let arrayTextResult = [];
	let howManyOverflowing = 0;
	for (let index = 0; index < allWords.length; index++) {
		let potencialWidth = getTextWidth(textResult);
		if (potencialWidth <= widthLimit) {
			if (allWords[index].value == '') {
				let text = allWords[index].closest('label').querySelector('p').innerHTML;
				textResult += `${text},`;
				arrayTextResult.push(text);
			} else {
				arrayTextResult.push(allWords[index].value);
				textResult += `${allWords[index].value},`;
			}
		} else {
			howManyOverflowing++;
		}
	}
	howManyOverflowing = howManyOverflowing == 0 ? '' : `+${howManyOverflowing}`;
	textResult = arrayTextResult.join(', ');
	return { textResult, howManyOverflowing };
}

function setRangeDatesOnGlobalFilter() {
	let rangeDate = getActiveDates();
	let date_from = rangeDate['date_from'];
	let date_to = rangeDate['date_to'];
	globalFilter['date'] = getRangeDates(`${date_from} 00:00`, new Date(date_to));
}

function removeFilterFromGlobalFilter(input) {
	let indexof = globalFilter[input.name].indexOf(input.value);
	if (indexof > -1) {
		globalFilter[input.name].splice(indexof, 1);
	}
}

function addFilterToGlobalFilter(input) {
	if (typeof globalFilter[input.name] === 'undefined') {
		globalFilter[input.name] = [];
	}
	globalFilter[input.name].push(input.value);
}

function openTab(targetSingleMenu, targetTab) {
	document.querySelector('#root #menu .single_menu.active').classList.remove('active');
	document.querySelector('#root .dashboard_tab.active').classList.remove('active');
	targetSingleMenu.classList.add('active');
	targetTab.classList.add('active');
	if (!targetSingleMenu.classList.contains('config') && targetTab.classList.contains('virgin')) {
		targetTab.classList.remove('virgin');
		const noPlotTabs = ['calendar_tab'];
		if (noPlotTabs.includes(targetTab.id)) {
			// TODO: chamar calendário
			if (targetTab.id == 'calendar_tab') {
				calendarController.makeCalendar();
			}
		} else if ('dates' in lastDashboardJson) {
			plotOnTab(lastDashboardJson, targetSingleMenu.dataset.idtab);
		}
	}
}
