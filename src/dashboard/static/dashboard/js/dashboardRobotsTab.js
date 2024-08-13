const robotsDashboardController = (() => {
	const allRobotVariables = {
		robots: {},
	};

	const getAllVariables = () => ({ ...allRobotVariables });

	const getRobotVariable = (key) => allRobotVariables[key];

	const setRobotVariable = (key, value, robot = null) => {
		if (robot) {
			if (!(robot in allRobotVariables.robots)) {
				allRobotVariables.robots[robot] = {};
			}

			const thisRobotInfo = allRobotVariables.robots[robot];

			thisRobotInfo[key] = value;
		} else {
			allRobotVariables[key] = value;
		}
	};

	const getDailyInfo = (withRobots = false) => {
		const data = {};
		const lastDateGlobalFilter = globalFilter.date?.at(-1)?.replaceAll('_', '-');
		const lastDateMidnight = new Date(`${lastDateGlobalFilter} 00:00`);
		const lastDateBeautified = `${lastDateMidnight.getFullYear()}-${
			lastDateMidnight.getMonth() + 1
		}-${lastDateMidnight.getDate()}`;
		const robots = new Set();
		let totalOccupation = 0;

		Object.entries(allTabsVariables['occupationby_robot']).forEach(([robot, robotHours]) => {
			Object.entries(robotHours).forEach(([hour, hourInfo]) => {
				const quantityOfRobotsInTheHour = hourInfo.qnt;
				const averageOccupationInThisHour =
					quantityOfRobotsInTheHour > 0
						? hourInfo['total_occupation_byhour'] / quantityOfRobotsInTheHour
						: hourInfo['total_occupation_byhour'];
				const hourInNumber = Number(hour.split('_').at(0));
				const hourIn24hoursFormat = hour.includes('PM')
					? hourInNumber == 12
						? hourInNumber
						: hourInNumber + 12
					: hourInNumber == 12
					? 0
					: hourInNumber;

				if (withRobots) {
					if (!data[robot]) data[robot] = {};

					if (!data[robot][`${lastDateBeautified} ${hourIn24hoursFormat}:00`]) {
						data[robot][`${lastDateBeautified} ${hourIn24hoursFormat}:00`] = {
							averageOccupation: 0,
							hourDisplayFormat: hour,
						};
					}

					data[robot][
						`${lastDateBeautified} ${hourIn24hoursFormat}:00`
					].averageOccupation += averageOccupationInThisHour;
				} else {
					if (!data[`${lastDateBeautified} ${hourIn24hoursFormat}:00`]) {
						data[`${lastDateBeautified} ${hourIn24hoursFormat}:00`] = {
							averageOccupation: 0,
							hourDisplayFormat: hour,
						};
					}

					data[`${lastDateBeautified} ${hourIn24hoursFormat}:00`].averageOccupation +=
						averageOccupationInThisHour;
				}

				totalOccupation += averageOccupationInThisHour;
			});

			robots.add(robot);
		});
		setRobotVariable('totalOccupation', totalOccupation);

		setRobotVariable('allRobots', Array.from(robots));

		return data;
	};

	const getWeekInfo = () => {
		const variablesByTime = {};
		let count = 0;
		let weekCount = 0;

		Object.entries(allTabsVariables['robots_bydate']).forEach(([date, dateInfo]) => {
			if (count === 0) {
				variablesByTime[weekCount] = {
					date: dateInfo['date'],
					robots: { ...dateInfo.robots },
				};
			}

			Object.entries(dateInfo.robots).forEach(([robot, robotInfo]) => {
				const robotIsInWeekData = robot in variablesByTime[weekCount]['robots'];

				if (robotIsInWeekData) {
					variablesByTime[weekCount]['robots'][robot]['time_in_seconds'] += Number(
						robotInfo['time_in_seconds']
					);
				} else {
					variablesByTime[weekCount]['robots'][robot] = { time_in_seconds: 0 };
					variablesByTime[weekCount]['robots'][robot]['time_in_seconds'] = Number(
						robotInfo['time_in_seconds']
					);
				}
			});
			count++;
			const dateObj = getDate(dateInfo['date']);
			if (dateObj.getDay() == 6) {
				weekCount++;
				count = 0;
			}
		});

		return variablesByTime;
	};

	const getMonthlyInfo = () => {
		const variablesByTime = {};
		let count = 0;
		let monthCount = 0;

		Object.entries(allTabsVariables['robots_bydate']).forEach(([date, dateInfo]) => {
			if (count === 0) {
				variablesByTime[monthCount] = {
					date: dateInfo['date'],
					robots: { ...dateInfo.robots },
				};
			}

			Object.entries(dateInfo.robots).forEach(([robot, robotInfo]) => {
				const robotIsInWeekData = robot in variablesByTime[monthCount]['robots'];

				if (robotIsInWeekData) {
					variablesByTime[monthCount]['robots'][robot]['time_in_seconds'] += Number(
						robotInfo['time_in_seconds']
					);
				} else {
					variablesByTime[monthCount]['robots'][robot] = { time_in_seconds: 0 };
					variablesByTime[monthCount]['robots'][robot]['time_in_seconds'] = Number(
						robotInfo['time_in_seconds']
					);
				}
			});
			count++;
			const dateObj = getDate(dateInfo['date']);
			if (dateObj.getDate() == 1) {
				monthCount++;
				count = 0;
			}
		});

		return variablesByTime;
	};
	return {
		getAllVariables,
		getRobotVariable,
		setRobotVariable,
		getDailyInfo,
		getWeekInfo,
		getMonthlyInfo,
	};
})();

function plotAverageOccupationProcesses(sortRule = 'general') {
	const plotId = 'average_occupation_byhour';

	const lastDateGlobalFilter = globalFilter.date?.at(-1)?.replaceAll('_', '-');
	const lastDate = getDate(lastDateGlobalFilter)
		.toLocaleDateString('pt-br')
		.split('/')
		.reverse()
		.join('-');

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				ticksuffix: ' min',
				automargin: true,
			},
			xaxis: {
				linecolor: '#ccc',
				linewidth: 0,
				automargin: true,
				autorange: true,
				type: 'date',
				range: [lastDate, `${lastDate} 23:00`],
			},
			hovermode: 'closest',
			barmode: 'group',
			showlegend: false,
			shapes: [
				{
					type: 'line',
					xref: 'paper',
					x0: 0,
					y0: 60,
					x1: 24,
					y1: 60,
					line: {
						color: '#01ffa9',
						width: 3,
					},
				},
			],
			annotations: [
				{
					showarrow: false,
					text: translate['maximum_occupancy'][language],
					align: 'right',
					x: 0,
					xanchor: 'left',
					y: 60,
					yanchor: 'bottom',
					xref: 'paper',
				},
			],
		},
		container: '.single__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	function prepareDataForDashboard() {
		if (sortRule === 'general') {
			const infoByHour = robotsDashboardController.getDailyInfo();
			const xCoordinates = [];
			const yCoordinates = [];
			const hoverTexts = [];

			Object.entries(infoByHour).forEach(([hour, hourData]) => {
				const { hourDisplayFormat, averageOccupation } = hourData;
				xCoordinates.push(hour);
				yCoordinates.push(averageOccupation / 60);

				const hourBeautified = hourDisplayFormat.replace('_', '');
				const minutes = Math.floor(averageOccupation / 60);
				const seconds = Math.round(averageOccupation - minutes * 60);
				const text = `${minutes}${translate['minutes_minified'][language]} ${translate['and'][language]} ${seconds} ${translate['seconds'][language]}`;

				const percentage = (averageOccupation * 100) / 3600;

				hoverTexts.push(
					`<b>${hourBeautified}</b><br><br><span>${
						translate['rate'][language]
					}: <b>${formatNumberToLanguage(Math.round(percentage))}%</b></span><br><span>${
						translate['occupation'][language]
					}: <b>${text}</b></span><extra></extra>`
				);
			});

			const trace = {
				type: 'scatter',
				fill: 'tozeroy',
				fillcolor: '#11067a1a',
				x: xCoordinates,
				y: yCoordinates,
				hovertemplate: hoverTexts,
				hoverlabel: {
					bgcolor: '#000',
					font: { color: '#fff' },
				},
				marker: {
					color: '#11067a',
					width: 1,
				},
				text: yCoordinates.map(
					(item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`
				),
				textposition: 'auto',
				mode: 'lines',
			};

			return [trace];
		} else {
			const infoByHour = robotsDashboardController.getDailyInfo(true);
			const traces = [];
			const colors = ['#11067a', '#c8c1ff', '#7768ff'];
			let count = 0;
			Object.entries(infoByHour).forEach(([robot, robotInfo]) => {
				const xCoordinates = [];
				const yCoordinates = [];
				const hoverTexts = [];

				Object.entries(robotInfo).forEach(([hour, hourData]) => {
					const { hourDisplayFormat, averageOccupation } = hourData;
					xCoordinates.push(hour);
					yCoordinates.push(averageOccupation / 60);

					const hourBeautified = hourDisplayFormat.replace('_', '');
					const minutes = Math.floor(averageOccupation / 60);
					const seconds = Math.round(averageOccupation - minutes * 60);
					const text = `${minutes}${translate['minutes_minified'][language]} ${translate['and'][language]} ${seconds} ${translate['seconds'][language]}`;

					const percentage = (averageOccupation * 100) / 3600;

					hoverTexts.push(
						`<b>${robot}</b><br><br><span>Horário: <b>${hourBeautified}</b></span><br><span>${
							translate['rate'][language]
						}: <b>${formatNumberToLanguage(
							Math.round(percentage)
						)}%</b></span><br><span>${
							translate['occupation'][language]
						}: <b>${text}</b></span><extra></extra>`
					);
				});
				const index = count % colors.length;
				count++;

				const trace = {
					type: 'scatter',
					x: xCoordinates,
					y: yCoordinates,
					hovertemplate: hoverTexts,
					hoverlabel: {
						bgcolor: '#000',
						font: { color: '#fff' },
					},
					marker: {
						color: colors[index],
						width: 1,
					},
					text: yCoordinates.map(
						(item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`
					),
					textposition: 'auto',
				};

				traces.push(trace);
			});

			return traces;
		}
	}
}

function plotStatusProcesses() {
	const plotId = 'process_bystatus';
	const infosToAdd = [];
	const totalNumberOfProcesses = dashboardController.getVariable('totalNumberOfProcesses');
	const allStatus = dashboardController.getVariable('totalStatus');
	let percentageSuccess = 0;

	Object.entries(allStatus).forEach(([status, numberOfProcessesWithThisStatus]) => {
		if (status == 'Successful') {
			percentageSuccess = (
				(allStatus.Successful * 100) /
				(allStatus.Successful + allStatus.Faulted + allStatus.Stopped)
			).toFixed(2);

			infosToAdd[0] = {
				qnt: numberOfProcessesWithThisStatus,
				text: translate['completed'][language],
			};
		} else if (status == 'Faulted') {
			infosToAdd[1] = {
				qnt: numberOfProcessesWithThisStatus,
				text: translate['faulted'][language],
			};
		} else {
			infosToAdd[2] = {
				qnt: numberOfProcessesWithThisStatus,
				text: translate['paused_stopped'][language],
			};
		}
	});

	const plotNumberEl = document.querySelector(`#${plotId} .half_donut_infos .percentage strong`);
	const boxesContainer = document.querySelector(`#${plotId} .infos_content`);
	boxesContainer.innerHTML = '';

	plotNumberEl.textContent = Number(percentageSuccess)
		? `${formatNumberToLanguage(percentageSuccess)}%`
		: '-';

	infosToAdd.forEach((item) => {
		const box = document.createElement('div');
		const boldEl = document.createElement('b');
		const textEl = document.createElement('p');

		box.classList.add('dashboard_small_box_info');
		boldEl.classList.add('f-size-22');
		textEl.classList.add('f-size-16');

		boldEl.textContent = formatNumberToLanguage(item.qnt);
		textEl.textContent = item.text;

		box.append(boldEl, textEl);

		boxesContainer.append(box);
	});

	document.querySelector(`#${plotId} .status_infos p b`).textContent =
		formatNumberToLanguage(totalNumberOfProcesses);
	document.documentElement.style.setProperty(
		'--status-circle-progress',
		Number(percentageSuccess) ? `${180 - 180 * (percentageSuccess / 100)}deg` : '180deg'
	);
}

function plotRobotOccupancyRate(sortRule = 'day') {
	const plotId = 'houriddleness_byday';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				automargin: true,
			},
			xaxis: {
				linecolor: '#ccc',
				linewidth: 0,
				automargin: true,
				autorange: true,
			},
			hovermode: 'closest',
			barmode: 'stack',
			autosize: false,
		},
		container: '.single__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	const plotEl = document.getElementById(plotId);
	plotEl.on('plotly_click', handlePlotClick);

	function prepareDataForDashboard() {
		const xCoordinates = [];
		const yCoordinates = robotsDashboardController.getRobotVariable('allRobots');
		const zCoordinates = [];
		const hoverTexts = [];
		let count = 0;

		yCoordinates.forEach((robot, index) => {
			zCoordinates[index] = [];
			hoverTexts[index] = [];
		});

		if (sortRule === 'hour') {
			Object.entries(allTabsVariables['robots_bydate']).forEach(([date, dateInfo]) => {
				const dateInCorrectFormat = date.replaceAll('_', '-');
				for (let hour = 0; hour < 24; hour++) {
					const hourWithZeroToTheLeft = String(hour).padStart(2, '0');

					xCoordinates.push(`${dateInCorrectFormat} ${hourWithZeroToTheLeft}:00`);

					zCoordinates.forEach((value) => {
						value[count] = [];
					});

					const hourWithAmOrPm = getHourWithPmAmFromNumber(hour);

					Object.entries(dateInfo.robots).forEach(([robot, robotInfo]) => {
						const indexOfRobot = yCoordinates.indexOf(robot);

						if (indexOfRobot === -1) return;

						const minutes =
							robotInfo['occupation_by_hour'][hourWithAmOrPm][
								'total_occupation_byhour'
							] / 60;
						zCoordinates[indexOfRobot][count] = Math.round(minutes * 10) / 10;
						const occupancyRate = Math.round((minutes / 60) * 1000) / 10;

						const dateBeautified = getDate(dateInCorrectFormat).toLocaleString(
							language,
							{
								day: 'numeric',
								month: 'long',
								year: 'numeric',
							}
						);
						const firstInfoText = `${hourWithAmOrPm.replaceAll(
							'_',
							''
						)} - ${dateBeautified} `;

						hoverTexts[indexOfRobot][
							count
						] = `<b>${firstInfoText}</b><br><br>${translate['robot'][language]}: ${yCoordinates[indexOfRobot]} <br>${translate['rate'][language]}: ${occupancyRate}% <br> ${translate['occupation'][language]}: ${zCoordinates[indexOfRobot][count]}min`;
					});

					count++;
				}
			});
		} else if (sortRule === 'day') {
			Object.entries(allTabsVariables['robots_bydate']).forEach(([date, dateInfo]) => {
				const dateInCorrectFormat = date.replaceAll('_', '-');
				xCoordinates.push(dateInCorrectFormat);

				zCoordinates.forEach((value) => {
					value[count] = [];
				});

				Object.entries(dateInfo.robots).forEach(([robot, robotInfo]) => {
					const indexOfRobot = yCoordinates.indexOf(robot);

					if (indexOfRobot === -1) return;

					const hours = robotInfo['time_in_seconds'] / 3600;

					const minutes = Math.floor((robotInfo['time_in_seconds'] % 3600) / 60);

					const occupancyRate = Math.round((hours / 24) * 1 * 1000) / 10;

					zCoordinates[indexOfRobot][count] = Math.round(minutes * 10) / 10;

					const dateBeautified = getDate(dateInCorrectFormat).toLocaleString(language, {
						day: 'numeric',
						month: 'long',
						year: 'numeric',
					});

					hoverTexts[indexOfRobot][
						count
					] = `<b>${dateBeautified}</b><br><br>${translate['robot'][language]}: ${yCoordinates[indexOfRobot]} <br>${translate['rate'][language]}: ${occupancyRate}% <br> ${translate['occupation'][language]}: ${zCoordinates[indexOfRobot][count]}min`;
				});

				count++;
			});
		} else if (sortRule == 'week') {
			const weekData = robotsDashboardController.getWeekInfo();

			Object.entries(weekData).forEach(([index, weekInfo]) => {
				const date = weekInfo.date;
				xCoordinates.push(date);

				zCoordinates.forEach((value) => {
					value[count] = [];
				});

				Object.entries(weekInfo.robots).forEach(([robot, robotInfo]) => {
					const indexOfRobot = yCoordinates.indexOf(robot);

					if (indexOfRobot === -1) return;

					const hours = robotInfo['time_in_seconds'] / 3600;

					const minutes = Math.floor((robotInfo['time_in_seconds'] % 3600) / 60);

					const occupancyRate = Math.round((hours / 24) * 1 * 1000) / 10;

					zCoordinates[indexOfRobot][count] = Math.round(minutes * 10) / 10;

					const lastWeekDay = getLastDayOfWeek(date);
					const firstInfoText = `${getDate(date).getDate()} ${
						translate['to'][language]
					} ${getDate(lastWeekDay).toLocaleString(language, {
						day: 'numeric',
						month: 'long',
						year: 'numeric',
					})}`;

					hoverTexts[indexOfRobot][
						count
					] = `<b>${firstInfoText}</b><br><br>${translate['robot'][language]}: ${yCoordinates[indexOfRobot]} <br>${translate['rate'][language]}: ${occupancyRate}% <br> ${translate['occupation'][language]}: ${zCoordinates[indexOfRobot][count]}min`;
				});

				count++;
			});
		} else if (sortRule == 'month') {
			const monthData = robotsDashboardController.getMonthlyInfo();

			Object.entries(monthData).forEach(([index, monthInfo]) => {
				const date = monthInfo.date;
				xCoordinates.push(date);

				zCoordinates.forEach((value) => {
					value[count] = [];
				});

				Object.entries(monthInfo.robots).forEach(([robot, robotInfo]) => {
					const indexOfRobot = yCoordinates.indexOf(robot);

					if (indexOfRobot === -1) return;

					const hours = robotInfo['time_in_seconds'] / 3600;

					const minutes = Math.floor((robotInfo['time_in_seconds'] % 3600) / 60);

					const occupancyRate = Math.round((hours / 24) * 1 * 1000) / 10;

					zCoordinates[indexOfRobot][count] = Math.round(minutes * 10) / 10;

					const lastWeekDay = getLastDayOfWeek(date);
					const beautifiedMonth = capitalize(
						getDate(lastWeekDay).toLocaleString(language, {
							month: 'long',
							year: 'numeric',
						})
					);

					hoverTexts[indexOfRobot][
						count
					] = `<b>${beautifiedMonth}</b><br><br>${translate['robot'][language]}: ${yCoordinates[indexOfRobot]} <br>${translate['rate'][language]}: ${occupancyRate}% <br> ${translate['occupation'][language]}: ${zCoordinates[indexOfRobot][count]}min`;
				});

				count++;
			});
		}

		const colorScale = [
			[0, '#92f3d7'],
			[1, '#13087b'],
		];

		const trace = {
			z: zCoordinates,
			x: xCoordinates,
			y: yCoordinates,
			type: 'heatmap',
			hoverongaps: false,
			colorscale: colorScale,
			colorbar: {
				outlinecolor: '#ffffff',
			},
			text: hoverTexts,
			hoverinfo: 'text',
			hoverlabel: {
				bgcolor: '#000',
				font: { color: '#fff' },
			},
		};

		return [trace];
	}

	function handlePlotClick(data) {
		const type = 'robot';
		const clickedFilter = data.points[0].y;
		// data.points[0].y = "AZBR-RPA-DESK1"
		// data.points[0].x = '2020-04-27'
		// data.points[0].z = 29.2
		if (sortRule == 'week') {
			let lastWeekDay = getLastDayOfWeekFromDay(data.points[0].x);
			let weekClicked = getRangeDates(
				`${data.points[0].x} 00:00`,
				new Date(
					`${lastWeekDay['year']}-${lastWeekDay['month']}-${lastWeekDay['day']} 00:00:00`
				)
			);
			newClickOnChartWithoutCheckBox(
				'date',
				weekClicked,
				'robots_tab',
				{ type, clickedFilter },
				true
			);
			selectOrderRobot.value = 'day';
			selectOrderRobot.dataset.selected = 'day';
		} else if (sortRule == 'month') {
			let lastMonthDay = getLastDayOfMonth(data.points[0].x);
			let monthClicked = getRangeDates(
				`${data.points[0].x} 00:00`,
				new Date(
					`${lastMonthDay['year']}-${lastMonthDay['month']}-${lastMonthDay['day']} 00:00:00`
				)
			);
			newClickOnChartWithoutCheckBox('date', monthClicked, 'robots_tab', {
				type,
				clickedFilter,
			});
			selectOrderRobot.value = 'day';
			selectOrderRobot.dataset.selected = 'day';
		} else if (sortRule == 'hour') {
			let dateClicked = data.points[0].x.replaceAll('-', '_');
			newClickOnChartDateHour([dateClicked], 'robots_tab', {
				type,
				clickedFilter,
			});
		} else {
			let dateClicked = data.points[0].x.replaceAll('-', '_');
			// algumas situações representam voltar ao estado inicial do filtro
			if (globalFilter['date'].length == 7 || globalFilter['date'].length == 30) {
				// era 7 e agora está por dia, melhor voltar ao range de todas as datas
				dateClicked = dateClicked.split(' ')[0];
			}
			newClickOnChartWithoutCheckBox('date', [dateClicked], 'robots_tab', {
				type,
				clickedFilter,
			});
		}
	}
}

function getHourWithPmAmFromNumber(number) {
	const hourWithZeroToTheLeft = String(number).padStart(2, '0');
	let hourIndexTranslate = '';
	if (number > 11) {
		const foreignHour = number == 12 ? 12 : number - 12;
		const foreignHourWithZeroToTheLeft = String(foreignHour).padStart(2, '0');
		hourIndexTranslate = `${foreignHourWithZeroToTheLeft}_PM`;
	} else {
		const hour = number == 0 ? 12 : hourWithZeroToTheLeft;
		hourIndexTranslate = `${hour}_AM`;
	}
	return hourIndexTranslate;
}

function updateRobotsVariables() {
	const allRobots = new Set();
	const allProcesses = new Set();
	allTabsVariables.all_robots.forEach((robotName) => {
		allRobots.add(robotName);
	});
	Object.entries(allTabsVariables.allprocesses).forEach((processName) => {
		allProcesses.add(processName);
	});
	robotsDashboardController.setRobotVariable('allProcesses', Array.from(allProcesses));
	robotsDashboardController.setRobotVariable('allRobots', Array.from(allRobots));
}

function makeRobotsBoxes() {
	const overallRobotsEl = document.querySelector('.occupation div .info');
	const overallRobotsImg = document.querySelector('.occupation div img');
	const robotsEl = document.querySelector('.robots div .info');
	const robotsImg = document.querySelector('.robots div img');
	const numberOfProcesses = document.querySelector('.robot_process div .info');
	const numberOfProcessesImg = document.querySelector('.robot_process div img');
	const totalOccupation = robotsDashboardController.getRobotVariable('totalOccupation');
	const averageOccupation = (totalOccupation * 100) / 86400;

	overallRobotsEl.textContent = averageOccupation
		? `${new Intl.NumberFormat(language).format(averageOccupation.toFixed(2))}%`
		: '-';

	numberOfProcesses.textContent =
		robotsDashboardController.getRobotVariable('allProcesses').length || '-';

	robotsEl.textContent = robotsDashboardController.getRobotVariable('allRobots').length || '-';

	robotsImg.classList.remove('d-none');
	numberOfProcessesImg.classList.remove('d-none');
	overallRobotsImg.classList.remove('d-none');
}

function getLastDayOfWeek(date) {
	const dateObj = getDate(date); // get current date
	const start = dateObj.getDate() - dateObj.getDay(); // First day is the day of the month - the day of the week
	const end = start + 6; // last day is the first day + 6

	const lastDay = getDate(dateObj.setDate(end))
		.toLocaleDateString('pt-br')
		.split('/')
		.reverse()
		.join('-');

	return lastDay;
}
