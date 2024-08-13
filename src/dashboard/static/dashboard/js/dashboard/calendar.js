let futureProcesses = {};
let weekProcessesByDay = {};
let everyMinuteProcess = [];
// let calendar = null;

const calendarController = (() => {
	let calendar;

	const makeCalendar = async (events, initialDate = null) => {
		if (!events) {
			events = await getAllCalendarEvents();
		}

		const calendarEl = document.getElementById('calendar_container');
		const initialView = 'timeGridWeek';
		const calendarConfig = {
			headerToolbar: {
				left: 'prev,next today',
				center: 'title',
				right: 'timeGridWeek,timeGridDay fiveMinButton,fifteenMinButton,thirtyMinButton',
			},
			buttonText: {
				today: translate['today'][language],
				week: translate['week'][language],
				day: translate['day'][language],
			},
			customButtons: {
				fiveMinButton: {
					text: '5 min',
					click: (event, htmlEl) => toggleCalendarIncrementPeriod(htmlEl, 5),
				},
				fifteenMinButton: {
					text: '15 min',
					click: (event, htmlEl) => toggleCalendarIncrementPeriod(htmlEl, 15),
				},
				thirtyMinButton: {
					text: '30 min',
					click: (event, htmlEl) => toggleCalendarIncrementPeriod(htmlEl, 30),
				},
			},
			viewDidMount: (info) => {
				const defaultIncrementPeriodBtn = calendarEl.querySelector(
					'.fc-thirtyMinButton-button'
				);
				defaultIncrementPeriodBtn.classList.add('fc-button-active');
			},
			initialView,
			locale: language.toLowerCase(),
			navLinks: true, // can click day/week names to navigate views
			businessHours: true, // display business hours
			allDaySlot: false,
			editable: false,
			selectable: true,
			events: events,
			eventClick: function (info) {
				Swal.fire(translate['please_wait_p'][language], getLoadingDiv());
				openModalDescription(
					info.event.title,
					info.event.extendedProps.description,
					info.event._instance.range.start
				);
			},
		};
		if (initialDate) {
			calendarConfig['initialDate'] = initialDate;
		}

		calendar = new FullCalendar.Calendar(calendarEl, calendarConfig);
		calendar.render();
		loadControlBtnsEvents();
		getWeeksDescription(0, initialView);
	};

	const getCalendarCurrentData = () => (calendar ? calendar.currentData : null);
	const setOption = (identifier, option) =>
		calendar ? calendar.setOption(identifier, option) : null;

	return {
		makeCalendar,
		getCalendarCurrentData,
		setOption,
	};
})();

function toggleCalendarIncrementPeriod(button, period) {
	if (!period || !button) return;
	const container = button.closest('div');

	calendarController.setOption('slotDuration', {
		minute: period,
	});

	Array.from(container.children).forEach((btn) => btn.classList.remove('fc-button-active'));
	button.classList.add('fc-button-active');
}

const loadControlBtnsEvents = () => {
	const calendarControlBtns = Array.from(
		document.querySelectorAll('#calendar_tab .fc-header-toolbar button')
	);
	calendarControlBtns.forEach((singleControlBtn) => {
		singleControlBtn.addEventListener('click', handleNewInterval);
	});
};

const handleNewInterval = (e) => {
	const days = 0;
	const currentData = calendarController.getCalendarCurrentData();
	let periodType = currentData.currentViewType;
	if (e.currentTarget.classList.contains('fc-timeGridWeek-button')) {
		periodType = 'timeGridWeek';
	} else if (e.currentTarget.classList.contains('fc-timeGridDay-button')) {
		periodType = 'timeGridDay';
	}
	getWeeksDescription(days, periodType);
};

const maxTriesOpenModalDescription = 3;
let tryingOpenModalDescription = 0;
const openModalDescription = (title, description, start) => {
	$('.event-title').html(title);
	const dateFormatted = getDateFormatted(updatingCalendarTimeZone(start), 'Y-m-d');
	if (weekProcessesByDay[dateFormatted] && weekProcessesByDay[dateFormatted].length) {
		Swal.close();
		tryingOpenModalDescription = 0;
		let finalDescription = getCalendarProcessDescription(
			title,
			description,
			start,
			dateFormatted
		);
		$('.event-body').html(finalDescription);
		$('#modal-calendar-processes').modal();
	} else {
		setTimeout(() => {
			tryingOpenModalDescription++;
			if (!Swal.getTitle()) {
				Swal.fire(translate['please_wait_p'][language], getLoadingDiv());
			}
			if (tryingOpenModalDescription <= maxTriesOpenModalDescription) {
				openModalDescription(title, description, start);
			} else {
				Swal.fire(
					'Oops..',
					`${translate['an_error_happened'][language]}, ${translate['refresh_the_page_and_try_again'][language]}`,
					'warning'
				);
				tryingOpenModalDescription = 0;
			}
		}, 1000);
	}
};

const updatingCalendarTimeZone = (date, hours = 3) => {
	const updatingToCalendarTimeZone = new Date(date);
	updatingToCalendarTimeZone.setTime(date.getTime() + hours * 60 * 60 * 1000);
	return updatingToCalendarTimeZone;
};

const getCalendarProcessDescription = (title, description, start, dateFormatted) => {
	const now = new Date();
	for (let i = 0; i < weekProcessesByDay[dateFormatted].length; i++) {
		let processStart = weekProcessesByDay[dateFormatted][i].start;
		if (processStart.indexOf('T') === -1) {
			// tem uma confusão sobre a hora do calendário e a hora que vem, especialmente se ela não está no formato com T
			processStart = getDateFormatted(
				updatingCalendarTimeZone(new Date(processStart), -3),
				'Y-m-d H:i:s'
			);
		}
		let startDate = new Date(processStart);
		let endDate = new Date(weekProcessesByDay[dateFormatted][i].end);
		const limitInterval = new Date(start);
		limitInterval.setTime(limitInterval.getTime() + 1 * 60 * 60 * 1000);
		if (
			startDate.valueOf() >= start.valueOf() &&
			startDate.valueOf() < limitInterval.valueOf()
		) {
			const isSameProcess = weekProcessesByDay[dateFormatted][i].title == title;
			if (isSameProcess) {
				// Igualando como tá salvo no calendário em como mostra o modal, por causa da timezone
				if (processStart.indexOf('T') !== -1) {
					startDate = processStart.split('T');
					let startTime = startDate[1].split('.');
					startDate = new Date(`${startDate[0]} ${startTime[0]}`);
				} else {
					// os processos everyminute não vêm com T na data
					startDate = new Date(weekProcessesByDay[dateFormatted][i].start);
				}

				const title = weekProcessesByDay[dateFormatted][i].title;
				let descriptionTitle = weekProcessesByDay[dateFormatted][i].description;
				let endDateFormatted = `${translate['ending_capitalized'][language]}:`;
				const isFutureProcess = startDate.valueOf() >= now.valueOf();

				if (isFutureProcess && allTabsVariables['allprocesses'][title]) {
					if (processStart.indexOf('T') !== -1) {
						endDate = getEndTimeFutureProcess(title, startDate, 'Y-m-dTH:i:s.z').split(
							'T'
						);
						let endTime = endDate[1].split('.');
						endDate = new Date(`${endDate[0]} ${endTime[0]}`);
					} else {
						endDate = new Date(weekProcessesByDay[dateFormatted][i].end);
					}
					const timeProcessTook = getTimeProcessTook(startDate, endDate);
					descriptionTitle = `${translate['it_is_estimated_that_the_process_would_take'][language]} ${timeProcessTook} ${translate['to_be_executed'][language]}`;
					endDateFormatted += getDateFormatted(endDate, 'd/m/Y H:i:s');
				} else if (isFutureProcess && !allTabsVariables['allprocesses'][title]) {
					endDateFormatted = '';
					descriptionTitle = translate['unable_to_calculate_estimate'][language];
				} else {
					endDate = weekProcessesByDay[dateFormatted][i].end.split('T');
					let endTime = endDate[1].split('.');
					endDate = new Date(`${endDate[0]} ${endTime[0]}`);
					endDateFormatted += getDateFormatted(endDate, 'd/m/Y H:i:s');
				}

				description += `<p class="f-size-12">${i + 1}- ${descriptionTitle} </br> ${
					translate['begining_capitalized'][language]
				}: ${getDateFormatted(startDate, 'd/m/Y H:i:s')} </br> ${endDateFormatted}</p>`;
			}
		}
	}
	return description;
};

const getTimeProcessTook = (startDate, endDate) => {
	let totalSeconds = Math.floor((endDate.valueOf() - startDate.valueOf()) / 1000);
	const minutes = (totalSeconds / 60) >> 0;
	const seconds = totalSeconds % 60 >> 0;
	const minutesText =
		minutes == 1 ? translate['minute'][language] : translate['minutes'][language];
	const secondsText =
		seconds == 1 ? translate['second'][language] : translate['seconds'][language];
	let finalText = `${seconds} ${secondsText}`;
	if (minutes > 0) {
		finalText = `${minutes} ${minutesText} ${translate['and'][language]} ${finalText}`;
	}
	return finalText;
};
const getWeeksDescription = async (intervalDays, periodType) => {
	const calendarInterval = getCalendarInterval(intervalDays, periodType);
	const date_from = getDateFormatted(calendarInterval['minDate'], 'Y-m-d');
	const date_to = getDateFormatted(calendarInterval['maxDate'], 'Y-m-d');
	const settings = {
		method: 'GET',
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
		},
	};
	const now = new Date();
	weekProcessesByDay = {};

	if (calendarInterval['maxDate'].valueOf() <= now.valueOf()) {
		let oldCalendarUrl =
			`/api/v1/get/uipathlogs/calendar?` +
			new URLSearchParams({
				date_from,
				date_to,
			});
		weekProcessesByDay = await getCalendarFetch(oldCalendarUrl, settings);
	} else if (
		calendarInterval['minDate'].valueOf() <= now.valueOf() &&
		calendarInterval['maxDate'] >= now.valueOf()
	) {
		let tomorrow = new Date();
		tomorrow.setDate(tomorrow.getDate() + 1);
		tomorrow = getDateFormatted(tomorrow, 'Y-m-d');
		let oldCalendarUrl =
			`/api/v1/get/uipathlogs/calendar?` +
			new URLSearchParams({
				date_from,
				date_to: tomorrow,
			});
		weekProcessesByDay = await getCalendarFetch(oldCalendarUrl, settings);
		let futureCalendarUrl =
			`/api/v1/get/uipathlogs/calendar/future?` +
			new URLSearchParams({
				date_from: tomorrow,
				date_to,
			});
		futureProcesses = await getCalendarFetch(futureCalendarUrl, settings);
		futureProcesses = futureProcesses['data'];
		weekProcessesByDay = {
			...weekProcessesByDay,
			...futureProcesses,
		};
	} else {
		let futureCalendarUrl =
			`/api/v1/get/uipathlogs/calendar/future?` +
			new URLSearchParams({
				date_from,
				date_to,
			});
		weekProcessesByDay = await getCalendarFetch(futureCalendarUrl, settings);
		weekProcessesByDay = mirrorEveryMinuteProcess(
			weekProcessesByDay['data'],
			everyMinuteProcess
		);
		futureProcesses['data'];
	}
	loadTooltips();
};

const getCalendarFetch = async (url, settings) => {
	let allProcessesByDay = {};
	await fetch(url, settings)
		.then(function (response) {
			// The API call was successful!
			return response.json();
		})
		.then(function (json) {
			// This is the HTML from our response as a text string
			if (json['status'] == 200) {
				allProcessesByDay = json['processes_by_day'];
			}
		})
		.catch(function (err) {
			// There was an error
			Swal.fire('Oops..', 'Error', 'warning');
		});
	return allProcessesByDay;
};

const loadTooltips = () => {
	const allEvents = Array.from(document.querySelectorAll('.fc-timegrid-event'));
	allEvents.forEach((singleEvent) => {
		singleEvent.dataset.toggle = 'tooltip';
		const process = singleEvent.querySelector('.fc-event-title').innerHTML;
		const timeSplitted = singleEvent.querySelector('.fc-event-time').innerHTML.split('-'); // 11:00 - 11:33
		const hour = Number(timeSplitted[0].split(':')[0].trim());
		let nextHour = hour === 23 ? `00` : hour + 1;
		if (language == 'en') {
			nextHour = hour === 12 ? `01` : hour + 1;
		}
		singleEvent.dataset.title = `${process} ${translate['was_executed_between'][language]} ${hour} ${translate['and'][language]} ${nextHour}`;
	});
	$('[data-toggle="tooltip"]').tooltip();
};

const getAllCalendarEvents = async (now) => {
	let oldCalendar = getProcessesBasedOnDashboard();
	if (!now) {
		now = new Date();
	}
	const now30 = new Date();
	now30.setDate(now.getDate() + 31);
	let futureCalendar = await updateFutureProcesses(now, now30);
	return oldCalendar.concat(futureCalendar);
};

const updateFutureProcesses = async (minDate, maxDate) => {
	// TODO: pegar um range de futuro pra adicionar ao calendário
	let futureCalendar = [];
	const date_from = getDateFormatted(minDate, 'Y-m-d');
	const date_to = getDateFormatted(maxDate, 'Y-m-d');
	const now = new Date();
	const settings = {
		method: 'GET',
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
		},
	};
	let url =
		`/api/v1/get/uipathlogs/calendar/future?` +
		new URLSearchParams({
			date_from,
			date_to,
		});

	await fetch(url, settings)
		.then(function (response) {
			// The API call was successful!
			return response.json();
		})
		.then(function (json) {
			// This is the HTML from our response as a text string
			if (json['status'] == 200) {
				const format = 'Y-m-d H:i:s';
				$.each(json['processes_by_day']['data'], function (date, allEvents) {
					const dateObj = new Date(`${date} 00:00:00`);
					if (dateObj.valueOf() > now.valueOf() && !futureProcesses[date]) {
						let dateEvents = [];
						allEvents.map((singleEventObj) => {
							let startDateObj = new Date(singleEventObj.start);
							startDateObj = updatingCalendarTimeZone(startDateObj);
							if (allTabsVariables['allprocesses'][singleEventObj.title]) {
								singleEventObj.start = getDateFormatted(startDateObj, format);
								singleEventObj.end = getEndTimeFutureProcess(
									singleEventObj.title,
									startDateObj,
									format
								);
							} else {
								// Some process are scheduled, but are not running for some time, or in this period. they need a special date
								const dates = getActiveDates();
								const dateFrom = new Date(`${dates['date_from']} 00:00:00`);
								const dateTo = new Date(`${dates['date_to']} 00:00:00`);
								singleEventObj.description = `${
									translate['process_did_not_run_between'][language]
								} ${getDateFormatted(dateFrom, 'd/m/Y')} ${
									translate['and'][language]
								} ${getDateFormatted(dateTo, 'd/m/Y')}`;
							}
							dateEvents.push(singleEventObj);
						});
						futureProcesses[date] = dateEvents;
						if (!weekProcessesByDay[date]) {
							weekProcessesByDay[date] = dateEvents;
						}
					}
				});
				everyMinuteProcess = json['processes_by_day']['every_minute'];
				if (everyMinuteProcess.length) {
					futureProcesses = mirrorEveryMinuteProcess(futureProcesses, everyMinuteProcess);
				}
			}
		})
		.catch(function (err) {
			// There was an error
			Swal.fire('Oops..', 'Error', 'warning');
		});
	$.each(futureProcesses, function (date, allEvents) {
		allEvents.map((singleEventObj) => {
			futureCalendar.push(singleEventObj);
		});
	});
	return futureCalendar;
};

const mirrorEveryMinuteProcess = (processes, everyMinuteProcesses) => {
	everyMinuteProcesses.map((process) => {
		if (allTabsVariables['allprocesses'][process['title']]) {
			let now = new Date();
			let futureCalendarEvents = {};
			let totalOccupationInSeconds = 0;
			let qnt = 0;
			$.each(
				allTabsVariables['allprocesses'][process['title']]['dates'],
				function (date, averageHour) {
					let somatoryPerHour = [];
					$.each(averageHour, function (hour, obj) {
						let startDate = new Date(`${date} ${translateHour[hour]}:00:00`);
						if (somatoryPerHour.indexOf(translateHour[hour]) === -1) {
							somatoryPerHour.push(translateHour[hour]);
						}
						startDate.setMonth(startDate.getMonth() + 1);
						const dateAddedMonth = getDateFormatted(startDate, 'Y-m-d');
						if (!futureCalendarEvents[dateAddedMonth]) {
							futureCalendarEvents[dateAddedMonth] = [];
						}
						let newCalendarEvent = {
							title: process['title'],
							start: getDateFormatted(startDate, 'Y-m-d H:i:s'),
							end: '',
							description: '',
							className: 'fc-bg-default estimated-time',
						};
						futureCalendarEvents[dateAddedMonth].push(newCalendarEvent);
						totalOccupationInSeconds += obj['total_occupation_byhour'];
					});
					qnt += somatoryPerHour.length;
				}
			);
			let finalFutureCalendarEvents = [];
			const averageTime = totalOccupationInSeconds / qnt;
			$.each(futureCalendarEvents, function (date, events) {
				events.forEach((event) => {
					const startDate = new Date(event.start);
					let endDate = new Date(event.start);
					endDate.setSeconds(endDate.getSeconds() + averageTime);
					event.end = getDateFormatted(endDate, 'Y-m-d H:i:s');
					if (startDate.valueOf() >= now.valueOf()) {
						if (!processes[date]) {
							processes[date] = [];
						}
						processes[date].push(event);
						finalFutureCalendarEvents.push(event);
					}
				});
			});
		}
	});
	return processes;
};
const getEndTimeFutureProcess = (title, startDateObj, format = null) => {
	let avgProcessTime =
		allTabsVariables['allprocesses'][title]['rpaHours'] /
		allTabsVariables['allprocesses'][title]['qnt'];
	let endDateObj = new Date(startDateObj);
	endDateObj.setSeconds(endDateObj.getSeconds() + avgProcessTime);
	let endDate = endDateObj.toISOString();
	if (format) {
		endDate = getDateFormatted(endDateObj, format);
	}
	return endDate;
};

const translateHour = {
	'12_AM': '00',
	'01_AM': '01',
	'02_AM': '02',
	'03_AM': '03',
	'04_AM': '04',
	'05_AM': '05',
	'06_AM': '06',
	'07_AM': '07',
	'08_AM': '08',
	'09_AM': '09',
	'10_AM': '10',
	'11_AM': '11',
	'12_PM': '12',
	'01_PM': '13',
	'02_PM': '14',
	'03_PM': '15',
	'04_PM': '16',
	'05_PM': '17',
	'06_PM': '18',
	'07_PM': '19',
	'08_PM': '20',
	'09_PM': '21',
	'10_PM': '22',
	'11_PM': '23',
};
const getProcessesBasedOnDashboard = () => {
	let newCalendar = [];
	$.each(lastDashboardJson['dates'], function (date, dateObj) {
		let calendarProcesses = {};
		$.each(dateObj['processes'], function (key, singleProcess) {
			$.each(singleProcess['averageoccupation_byday'], function (hour, averageOccupation) {
				let seconds = Math.floor(averageOccupation['total_occupation_byhour'] % 60);
				if (seconds < 10) {
					seconds = `0${seconds}`;
				}
				let minutes = Math.floor(averageOccupation['total_occupation_byhour'] / 60);
				if (minutes < 10) {
					minutes = `0${minutes}`;
				} else if (minutes > 60) {
					minutes = 60;
				}
				let calProIndex = `${singleProcess['process']}${translateHour[hour]}`;
				if (calProIndex in calendarProcesses) {
					calendarProcesses[calProIndex]['qnt'] += averageOccupation['qnt'];
					calendarProcesses[calProIndex]['obj'][
						'description'
					] = `${translate['with_capitalized'][language]} ${translate['executions'][language]}:`;
				} else {
					calendarProcesses[calProIndex] = {
						qnt: averageOccupation['qnt'],
						obj: {
							title: singleProcess['process'],
							description: `${translate['with_capitalized'][language]} ${averageOccupation['qnt']} ${translate['executions'][language]}:`,
							start: `${dateObj['date']} ${translateHour[hour]}:00:00`,
							end: `${dateObj['date']} ${translateHour[hour]}:${minutes}:${
								seconds.length == 1 ? '0' + seconds : seconds
							}`,
							className: 'fc-bg-default',
						},
					};
				}
			});
		});
		$.each(calendarProcesses, function (index, calendarItem) {
			newCalendar.push(calendarItem['obj']);
		});
	});
	return newCalendar;
};

const getCalendarInterval = (days = 0, periodType = 'timeGridWeek') => {
	const currentData = calendarController.getCalendarCurrentData();
	const dateInterval = updatingCalendarTimeZone(currentData.currentDate);
	dateInterval.setDate(dateInterval.getDate() + days);
	let calendarDates = {
		minDate: dateInterval,
		maxDate: dateInterval,
	};
	if (periodType == 'timeGridWeek') {
		calendarDates = getWeekMaxAndMinDates(dateInterval);
	}
	// new max date because backend only gets inside interval
	const newMaxDate = new Date(calendarDates['maxDate']);
	newMaxDate.setDate(newMaxDate.getDate() + 1);
	calendarDates['maxDate'] = newMaxDate;
	return calendarDates;
};

const getWeekMaxAndMinDates = (date) => {
	const weekDay = date.getDay();
	const lastWeekDay = 6 - weekDay;
	let maxDate = new Date(date);
	maxDate.setDate(maxDate.getDate() + lastWeekDay);
	let minDate = new Date(maxDate);
	minDate.setDate(minDate.getDate() - 6);
	return { minDate, maxDate };
};

const getDateFormatted = (date, format = 'Y-m-d') => {
	let dateFormatted = '';
	let dayFormatted = formatNumber2Digits(date.getDate());
	let monthFormatted = formatNumber2Digits(date.getMonth() + 1);
	if (format == 'Y-m-d') {
		dateFormatted = `${date.getFullYear()}-${monthFormatted}-${dayFormatted}`;
	} else if (format == 'd/m/Y H:i:s') {
		let hoursFormatted = formatNumber2Digits(date.getHours());
		let minutesFormatted = formatNumber2Digits(date.getMinutes());
		let secondsFormatted = formatNumber2Digits(date.getSeconds());
		dateFormatted = `${dayFormatted}/${monthFormatted}/${date.getFullYear()} ${hoursFormatted}:${minutesFormatted}:${secondsFormatted}`;
	} else if (format == 'd/m/Y') {
		dateFormatted = `${dayFormatted}/${monthFormatted}/${date.getFullYear()}`;
	} else if (format == 'Y-m-dTH:i:s.z') {
		let hoursFormatted = formatNumber2Digits(date.getHours());
		let minutesFormatted = formatNumber2Digits(date.getMinutes());
		let secondsFormatted = formatNumber2Digits(date.getSeconds());
		dateFormatted = `${date.getFullYear()}-${monthFormatted}-${dayFormatted}T${hoursFormatted}:${minutesFormatted}:${secondsFormatted}.000Z`;
	} else if (format == 'Y-m-d H:i:s') {
		let hoursFormatted = formatNumber2Digits(date.getHours());
		let minutesFormatted = formatNumber2Digits(date.getMinutes());
		let secondsFormatted = formatNumber2Digits(date.getSeconds());
		dateFormatted = `${date.getFullYear()}-${monthFormatted}-${dayFormatted} ${hoursFormatted}:${minutesFormatted}:${secondsFormatted}`;
	}
	return dateFormatted;
};

const formatNumber2Digits = (number = 0) => {
	return String(number).length == 1 ? `0${number}` : `${number}`;
};
