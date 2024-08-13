document.addEventListener('DOMContentLoaded', () => {
	const body = document.querySelector('body');

	body.addEventListener('click', handleBodyClick);
	body.addEventListener('keyup', handleBodyKeyup);
	document.addEventListener('changeDateInputCalendar', handleInputChanged);

	function handleBodyClick(e) {
		if (e.target.closest('.input_date') !== null) {
			handleClickDate(e);
		} else if (e.target.classList.contains('single_day')) {
			handleClickCalendar(e);
		} else if (e.target.classList.contains('prev') || e.target.classList.contains('next')) {
			if (e.target.closest('.month') !== null) {
				newMonth(e);
			} else if (e.target.closest('.year') !== null) {
				newYear(e);
			}
		} else if (e.target.classList.contains('close_icon')) {
			hideCalendar(e.target.closest('.date_calendar'));
		}

		let hasOpenedCalendar = document.querySelector('.date_calendar.opened');

		if (
			hasOpenedCalendar &&
			e.target.closest('.input_date') == null &&
			e.target.closest('.calendar') == null
		) {
			updateDateInput(hasOpenedCalendar);
			hasOpenedCalendar.classList.remove('opened');
		}
	}

	function handleBodyKeyup(e) {
		if (e.target.closest('.input_date') !== null) {
			handleKeyDate(e);
		}
	}

	function handleInputChanged(e) {
		let dateCalendar = e.detail.input.closest('.date_calendar');
		let day =
			e.detail.newDate.getDate().length == 1
				? `0${e.detail.newDate.getDate()}`
				: e.detail.newDate.getDate();
		let month =
			e.detail.newDate.getMonth().length + 1 == 1
				? `0${e.detail.newDate.getMonth() + 1}`
				: e.detail.newDate.getMonth() + 1;
		dateCalendar.querySelector(
			'.input_date input'
		).value = `${day}/${month}/${e.detail.newDate.getFullYear()}`;
		updateCalendarFromInput(e.detail.input);
	}

	function handleClickCalendar(e) {
		let singleDay = e.target;
		if (!singleDay.classList.contains('active')) {
			let calendar = singleDay.closest('.calendar');
			calendar.querySelector('.single_day.active').classList.remove('active');
			singleDay.classList.add('active');
			calendar.querySelector('.active_date_infos .day .value').innerHTML =
				singleDay.innerHTML;
			updateDateInput(calendar.closest('.date_calendar'));
		}
	}

	function newMonth(e) {
		let activeDateInfos = e.target.closest('.active_date_infos');
		let maxMonth = activeDateInfos.querySelectorAll('.all_months .value').length;
		let oldActiveMonth = activeDateInfos.querySelector('.all_months .value.active');
		let oldActiveIndex = Number(oldActiveMonth.dataset.number_translation);
		let newMonth = (oldActiveIndex - 1) % maxMonth;
		if (e.target.classList.contains('next')) {
			newMonth = (oldActiveIndex + 1) % maxMonth;
		}

		if (newMonth == 0) {
			newMonth = maxMonth;
		}
		oldActiveMonth.classList.remove('active');
		activeDateInfos
			.querySelector(`[data-number_translation~="${newMonth}"]`)
			.classList.add('active');
		updateDateInput(activeDateInfos.closest('.date_calendar'));
		fillInputDate(activeDateInfos.closest('.date_calendar').querySelector('input'));
	}

	function newYear(e) {
		let activeDateInfos = e.target.closest('.active_date_infos');
		let allYears = Array.from(activeDateInfos.querySelectorAll('.all_years .value'));
		let maxIndexYear = allYears.length;
		let oldActiveYear = activeDateInfos.querySelector('.all_years .value.active');
		let oldActiveIndex = allYears.indexOf(oldActiveYear);
		let newYearIndex = (oldActiveIndex - 1) % maxIndexYear;
		if (e.target.classList.contains('next')) {
			newYearIndex = (oldActiveIndex + 1) % maxIndexYear;
		}

		if (newYearIndex < 0) {
			newYearIndex = maxIndexYear - 1;
		}

		oldActiveYear.classList.remove('active');
		allYears[newYearIndex].classList.add('active');
		updateDateInput(activeDateInfos.closest('.date_calendar'));
		fillInputDate(activeDateInfos.closest('.date_calendar').querySelector('input'));
	}

	function handleKeyDate(e) {
		if (/[^\d/]/g.test(e.target.value)) {
			e.target.value = e.target.value.replace(/[^\d/]/g, '');
		}

		if (e.target.value.length == 10) {
			updateCalendarFromInput(e.target);
		}
	}

	function handleClickDate(e) {
		let dateCalendar = e.target.closest('.date_calendar');
		fillInputDate(dateCalendar.querySelector('input'));
		if (dateCalendar.classList.contains('opened')) {
			hideCalendar(dateCalendar);
		} else {
			document.querySelectorAll('.date_calendar.opened').forEach((calendar) => {
				calendar.classList.remove('opened');
			});
			dateCalendar.classList.add('opened');
		}
	}

	function hideCalendar(dateCalendar) {
		dateCalendar.classList.remove('opened');
	}

	function fillInputDate(input) {
		let completeDate = input.value.split('/');
		let lastDay = new Date(completeDate[2], Number(completeDate[1]), 0).getDate();
		let firstDayWeek = new Date(completeDate[2], Number(completeDate[1]) - 1, 1).getDay();
		let activeDate = completeDate[0];
		if (completeDate.length < 2) {
			completeDate = input.value.split('-');
			lastDay = new Date(completeDate[0], Number(completeDate[1]) - 1, 0).getDate();
			firstDayWeek = new Date(completeDate[0], Number(completeDate[1]) - 1, 1).getDay();
			activeDate = completeDate[2];
		}
		input
			.closest('.date_calendar')
			.querySelector('.month_dates .single_day.active')
			?.classList.remove('active');
		let calendar = input.closest('.date_calendar').querySelector('.calendar .month_dates');
		let count = 1;
		for (let line = 1; line <= 6; line++) {
			let chosenLine = calendar.querySelector(`.line${line}`);
			for (let column = 1; column <= 7; column++) {
				// como o primeiro lugar é 2, se for segunda, ao invés de 0 vai ser 2
				let matrixPosition = line + column;
				let dayLocation = chosenLine.querySelector(`.column${column}`);
				if (
					(line == 1 && firstDayWeek + 2 <= matrixPosition) ||
					(line != 1 && count <= lastDay)
				) {
					dayLocation.innerHTML = count;
					if (Number(activeDate) == count) {
						dayLocation.classList.add('active');
					} else {
						dayLocation.classList.remove('active');
					}
					count++;
				} else {
					dayLocation.innerHTML = ' ';
				}
			}
		}
	}

	function updateDateInput(dateCalendar) {
		let day = dateCalendar.querySelector('.active_date_infos .day .value').innerHTML;
		let monthElement = dateCalendar.querySelector(
			'.active_date_infos .all_months .value.active'
		);
		let month = monthElement.dataset.number_translation;
		let year = dateCalendar.querySelector(
			'.active_date_infos .all_years .value.active'
		).innerHTML;

		if (day.length == 1) {
			day = `0${day}`;
		}

		if (month.length == 1) {
			month = `0${month}`;
		}

		dateCalendar.querySelector('.input_date input').value = `${day}/${month}/${year}`;
		updateResumedYearMonth(dateCalendar, `${monthElement.innerHTML} ${year}`);
		// Create the event
		var dateEvent = new CustomEvent('changeDate', {
			detail: {
				inputTarget: dateCalendar.querySelector('input'),
			},
		});
		// Dispatch/Trigger/Fire the event
		document.dispatchEvent(dateEvent);
	}

	function updateCalendarFromInput(input) {
		let splittedDate = input.value.split('/');
		let dateCalendar = input.closest('.date_calendar');

		dateCalendar
			.querySelector('.active_date_infos .all_months .value.active')
			.classList.remove('active');
		let activeMonthElement = dateCalendar.querySelector(
			`.active_date_infos .all_months [data-number_translation~="${Number(splittedDate[1])}"]`
		);
		activeMonthElement.classList.add('active');

		dateCalendar
			.querySelector('.active_date_infos .all_years .value.active')
			?.classList.remove('active');
		dateCalendar
			.querySelector(
				`.active_date_infos .all_years [data-number_translation~="${splittedDate[2]}"]`
			)
			?.classList.add('active');

		monthYear = `${activeMonthElement.innerHTML} ${splittedDate[2]}`;
		updateResumedYearMonth(dateCalendar, monthYear);

		dateCalendar.querySelector('.active_date_infos .day .value').innerHTML = splittedDate[0];
		fillInputDate(input);
		dateCalendar.querySelector('.month_dates .single_day.active').classList.remove('active');
		dateCalendar.querySelectorAll('.month_dates .single_day').forEach((singleDay) => {
			if (Number(singleDay.innerHTML) == Number(splittedDate[0])) {
				singleDay.classList.add('active');
			} else {
				singleDay.classList.remove('active');
			}
		});
	}

	function updateResumedYearMonth(dateCalendar, value) {
		dateCalendar.querySelector('.year_month').innerHTML = value;
	}
});
