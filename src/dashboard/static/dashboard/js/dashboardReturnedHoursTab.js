const returnedHoursDashboardController = (() => {
	const allRoiVariables = {
		processes: {},
	};

	const getAllVariables = () => ({ ...allRoiVariables });

	const getVariable = (key) => allRoiVariables[key];

	const getProcessInfo = (process) => allRoiVariables.processes[process];

	const setVariable = (key, value, process = null) => {
		if (process) {
			if (!(process in allRoiVariables.processes)) {
				allRoiVariables.processes[process] = {};
			}

			const thisProcessInfo = allRoiVariables.processes[process];

			thisProcessInfo[key] = value;
		} else {
			allRoiVariables[key] = value;
		}
	};

	const getNumberOfProcesses = () => Object.keys(allRoiVariables.processes).length;

	return {
		getVariable,
		getProcessInfo,
		setVariable,
		getNumberOfProcesses,
		getAllVariables,
	};
})();

function plotReturnedHoursByProcess(sortRule = 'smaller') {
	const plotId = 'returned-hours-process';

	const margin = {
		t: 40,
		b: 100,
		r: 15,
		l: 80,
		pad: 23,
	};

	const dashboardConfig = {
		layout: {
			margin,

			yaxis: {
				autorange: true,
				ticksuffix: 'h',
			},
			xaxis: {
				linecolor: '#ccc',
				linewidth: 0,
				autotick: false,
				automargin: true,
				autorange: true,
			},
			hovermode: 'closest',
			barmode: 'group',
		},
		container: '.table__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	plotGraphTable('returned-hours-processes-table');

	const roiProcessPlot = document.getElementById(plotId);
	roiProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'roi_tab');
	});

	function prepareDataForDashboard() {
		const allProcesses = returnedHoursDashboardController.getVariable('allProcesses');

		if (!allProcesses) return [];
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];
		const allProcessesData = [];

		allProcesses.forEach((process) => {
			const processInfo = returnedHoursDashboardController.getProcessInfo(process);

			const { area, returnInHours } = processInfo;

			const allProcessesReturnInHours =
				returnedHoursDashboardController.getVariable('totalReturnInHours');
			const totalPercentage = (returnInHours * 100) / allProcessesReturnInHours;
			returnedHoursDashboardController.setVariable(
				'returnPercentage',
				totalPercentage,
				process
			);

			allProcessesData.push({
				process,
				area,
				returnInHours,
				totalPercentage,
			});
		});

		returnedHoursDashboardController.setVariable('processesInfo', allProcessesData);

		if (sortRule == 'smaller') {
			allProcessesData
				.sort((a, b) => a.returnInHours - b.returnInHours)
				.forEach(addDataToPlotlyArrays);
		} else {
			allProcessesData
				.sort((a, b) => b.returnInHours - a.returnInHours)
				.forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { process, returnInHours, area, totalPercentage } = processObj;

			xCoordinates.push(process);
			yCoordinates.push(returnInHours);

			hoverTexts.push(
				`<b>${process}</b><br><br><span>${
					translate['returned_hours'][language]
				}: <b>${formatNumberToLanguage(
					Math.round(returnInHours)
				)}h (${formatNumberToLanguage(totalPercentage.toFixed(2))}%)</b></span><br><span>${
					translate['area'][language]
				}: <b>${area}</b></span><extra></extra>`
			);
		}

		const trace = {
			type: 'bar',
			x: xCoordinates,
			y: yCoordinates,
			hovertemplate: hoverTexts,
			hoverlabel: {
				bgcolor: '#000',
				font: { color: '#fff' },
			},
			marker: {
				color: '#17EAAC',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}

function plotReturnedHoursByArea(sortRule = 'smaller') {
	const plotId = 'returned-hours-area';

	const margin = {
		t: 40,
		b: 100,
		r: 15,
		l: 80,
		pad: 23,
	};

	const dashboardConfig = {
		layout: {
			margin,

			yaxis: {
				autorange: true,
				ticksuffix: 'h',
			},
			xaxis: {
				linecolor: '#ccc',
				linewidth: 0,
				autotick: false,
				automargin: true,
				autorange: true,
			},
			hovermode: 'closest',
			barmode: 'group',
		},
		container: '.table__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	plotGraphTable('returned-hours-areas-table');

	const roiProcessPlot = document.getElementById(plotId);
	roiProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'roi_tab');
	});

	function prepareDataForDashboard() {
		const allInfosProcesses = returnedHoursDashboardController.getVariable('processes');
		const returnInHoursByArea = [];
		const areas = new Set();
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];

		if (areas instanceof Set) {
			const allProcesses = returnedHoursDashboardController.getVariable('allProcesses');
			allProcesses?.forEach((process) => {
				const processInfo = returnedHoursDashboardController.getProcessInfo(process);
				areas.add(processInfo.area);
			});
		}

		areas.forEach((area) => {
			let processes = 0;
			let thisAreaReturnInHours = 0;

			const informationByArea = Object.entries(allInfosProcesses).filter(
				([processName, processInfo]) => processInfo.area == area
			);

			if (!informationByArea.length) return;

			informationByArea.forEach(([processName, processInfo]) => {
				thisAreaReturnInHours += processInfo.returnInHours;
				processes++;
			});
			const totalReturnInHours =
				returnedHoursDashboardController.getVariable('totalReturnInHours');

			const returnPercentage = (thisAreaReturnInHours * 100) / totalReturnInHours;
			returnInHoursByArea.push({
				processes,
				area,
				returnInHours: thisAreaReturnInHours,
				returnPercentage,
			});
		});

		returnedHoursDashboardController.setVariable('areasInfo', returnInHoursByArea);

		if (sortRule == 'smaller') {
			returnInHoursByArea
				.sort((a, b) => a.returnInHours - b.returnInHours)
				.forEach(addDataToPlotlyArrays);
		} else {
			returnInHoursByArea
				.sort((a, b) => b.returnInHours - a.returnInHours)
				.forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { process, returnInHours, area } = processObj;
			const allProcessesReturnInHours =
				returnedHoursDashboardController.getVariable('totalReturnInHours');
			const totalPercentage = (returnInHours * 100) / allProcessesReturnInHours;
			returnedHoursDashboardController.setVariable(
				'returnPercentage',
				totalPercentage,
				process
			);
			const numberOfProcesses = returnedHoursDashboardController.getNumberOfProcesses();

			xCoordinates.push(area);
			yCoordinates.push(returnInHours);

			hoverTexts.push(
				`<b>${area}</b><br><br><span>${
					translate['returned_hours'][language]
				}: <b>${formatNumberToLanguage(
					Math.round(returnInHours)
				)}h (${formatNumberToLanguage(totalPercentage.toFixed(2))}%)</b></span><br><span>${
					translate['processes_capital_plural'][language]
				}: <b>${numberOfProcesses}</b></span><extra></extra>`
			);
		}

		const trace = {
			type: 'bar',
			x: xCoordinates,
			y: yCoordinates,
			hovertemplate: hoverTexts,
			hoverlabel: {
				bgcolor: '#000',
				font: { color: '#fff' },
			},
			marker: {
				color: '#17EAAC',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}

function plotReturnedHoursHistory(sortRule = 'month') {
	const plotId = 'hours-returned-history';

	const margin = {
		t: 40,
		b: 100,
		r: 15,
		l: 80,
		pad: 23,
	};

	const dashboardConfig = {
		layout: {
			margin,

			yaxis: {
				autorange: true,
				ticksuffix: 'h',
			},
			hovermode: 'closest',
			barmode: 'group',
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
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];
		const allProcessesData = [];
		const infoByMonth = {};

		Object.entries(lastDashboardJson.dates).forEach(([date, dateInfo]) => {
			const dateInCorrectFormat = date.replaceAll('_', '-');
			const dateObj = getDate(dateInCorrectFormat);
			const month = dateObj.getMonth() + 1;
			let hoursReturnedInThisDay = 0;
			let numberOfProcesses = 0;
			const robots = new Set();

			Object.values(dateInfo.processes).forEach((process) => {
				const processInfo = returnedHoursDashboardController.getProcessInfo(
					process.process
				);
				if (!processInfo) return;
				const { returnInHours } = processInfo;
				hoursReturnedInThisDay += returnInHours;
				numberOfProcesses++;
				robots.add(process.robot);
			});
			const data = {
				hoursReturnedInThisDay,
				numberOfProcesses,
				numberOfRobots: robots.size,
				date: dateInCorrectFormat,
			};

			if (sortRule === 'month') {
				if (!infoByMonth[month]) infoByMonth[month] = [];

				infoByMonth[month].push(data);
			}

			allProcessesData.push(data);
		});
		if (sortRule == 'month') {
			const differentMonths = monthCounter();
			allProcessesData
				.sort((a, b) => a.returnInHours - b.returnInHours)
				.filter(differentMonths)
				.forEach(addDataToPlotlyArrays);
		} else {
			allProcessesData
				.sort((a, b) => b.returnInHours - a.returnInHours)
				.forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { hoursReturnedInThisDay, numberOfProcesses, numberOfRobots, date } = processObj;
			const dateObj = getDate(date);

			if (sortRule === 'month') {
				const firstDayOfTheMonth = date.replace(/\d{2}$/, '01');
				xCoordinates.push(firstDayOfTheMonth);

				const month = dateObj.getMonth() + 1;
				const thisMonthData = infoByMonth[month];
				const monthText = dateObj.toLocaleString(language, {
					month: 'long',
					year: 'numeric',
				});

				const { hoursReturned, numberOfProcesses, numberOfRobots } = thisMonthData.reduce(
					(prevCount, currentProcess) => {
						return {
							hoursReturned:
								prevCount.hoursReturned + currentProcess.hoursReturnedInThisDay,
							numberOfProcesses:
								prevCount.numberOfProcesses + currentProcess.numberOfProcesses,
							numberOfRobots:
								prevCount.numberOfRobots + currentProcess.numberOfRobots,
						};
					},
					{
						hoursReturned: 0,
						numberOfProcesses: 0,
						numberOfRobots: 0,
					}
				);

				yCoordinates.push(hoursReturned);

				hoverTexts.push(
					`<b>${capitalize(monthText)}</b><br><br><span>${
						translate['returned_hours'][language]
					}: <b>${formatNumberToLanguage(
						Math.round(hoursReturned)
					)}h</b></span><br><span>${
						translate['processes_capital_plural'][language]
					}: <b>${numberOfProcesses}</b></span></span><br><span>${
						translate['robots'][language]
					}: <b>${numberOfRobots}</b></span><extra></extra>`
				);
			} else {
				xCoordinates.push(date);
				const dayText = dateObj.toLocaleString(language, {
					day: 'numeric',
					month: 'long',
					year: 'numeric',
				});
				yCoordinates.push(hoursReturnedInThisDay);

				hoverTexts.push(
					`<b>${dayText}</b><br><br><span>Horas Retornadas: <b>${formatNumberToLanguage(
						Math.round(hoursReturnedInThisDay)
					)}h</b></span><br><span>Processos: <b>${numberOfProcesses}</b></span></span><br><span>Robôs: <b>${numberOfRobots}</b></span><extra></extra>`
				);
			}
		}

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
				color: '#17EAAC',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}

function updateReturnedHoursVariables() {
	const allProcesses = new Set();
	let totalReturnInHours = 0;
	Object.entries(allTabsVariables.allprocesses).forEach(([processName, processInfo]) => {
		const thisProcessBackendInfo = lastDashboardJson['all_processes'][processName];
		if (!thisProcessBackendInfo) return;
		const thisProcessStatus = {
			Faulted: 0,
			Successful: 0,
		};

		const thisProcessMonthlyTasks = thisProcessBackendInfo['monthly_tasks'];
		const thisProcessMinutesInTask = thisProcessBackendInfo['minutes_in_task'];

		const thisProcessStatusRecord =
			dashboardController.getProcessInfo(processName).statusByDay || [];

		Object.values(thisProcessStatusRecord).forEach((record) => {
			thisProcessStatus.Faulted += record.Faulted;
			thisProcessStatus.Successful += record.Successful;
		});

		const conclusionRate =
			thisProcessStatus['Successful'] /
			(thisProcessStatus['Successful'] + thisProcessStatus['Faulted']);

		const thisProcessReturnInHours =
			thisProcessMinutesInTask * thisProcessMonthlyTasks * (conclusionRate * 0.8);

		totalReturnInHours += thisProcessReturnInHours;
		const thisProcessDates = processInfo.dates;

		const { area } = allTabsVariables.allprocesses[processName];

		returnedHoursDashboardController.setVariable('area', area, processName);
		returnedHoursDashboardController.setVariable(
			'monthlyTasks',
			thisProcessMonthlyTasks,
			processName
		);
		returnedHoursDashboardController.setVariable(
			'minutesInTask',
			thisProcessMinutesInTask,
			processName
		);
		returnedHoursDashboardController.setVariable(
			'returnInHours',
			thisProcessReturnInHours,
			processName
		);

		returnedHoursDashboardController.setVariable('dates', thisProcessDates, processName);

		allProcesses.add(processName);
	});

	returnedHoursDashboardController.setVariable('allProcesses', Array.from(allProcesses));
	returnedHoursDashboardController.setVariable('totalReturnInHours', totalReturnInHours);
}

function plotGraphTable(tableId) {
	const infoTable = document.getElementById(tableId);
	const tableBody = infoTable.querySelector('tbody');
	tableBody.innerHTML = '';

	if (tableId === 'returned-hours-processes-table') {
		const processes = returnedHoursDashboardController.getVariable('processesInfo');
		processes.forEach((processInfo) => {
			const { returnInHours, totalPercentage, process } = processInfo;
			const tableRow = document.createElement('tr');
			const gainElement = document.createElement('td');
			const nameElement = document.createElement('td');

			gainElement.textContent = `${formatNumberToLanguage(
				Math.round(returnInHours)
			)}h (${formatNumberToLanguage(totalPercentage.toFixed(2))}%)`;
			gainElement.classList.add('font-weight-bold');
			nameElement.classList.add('font-weight-bold');

			nameElement.textContent = process;
			tableRow.appendChild(gainElement);
			tableRow.appendChild(nameElement);
			tableBody.appendChild(tableRow);
		});
	} else {
		const areas = returnedHoursDashboardController.getVariable('areasInfo');

		areas.forEach((areaInfo) => {
			const { returnInHours, returnPercentage, area } = areaInfo;
			const tableRow = document.createElement('tr');
			const gainElement = document.createElement('td');
			const nameElement = document.createElement('td');

			gainElement.textContent = `${formatNumberToLanguage(
				Math.round(returnInHours)
			)}h (${formatNumberToLanguage(returnPercentage.toFixed(2))}%)`;
			gainElement.classList.add('font-weight-bold');
			nameElement.classList.add('font-weight-bold');

			nameElement.textContent = area;
			tableRow.appendChild(gainElement);
			tableRow.appendChild(nameElement);
			tableBody.appendChild(tableRow);
		});
	}
	infoTable.classList.remove('visibility-hidden');
}

function makeReturnedHoursBoxes() {
	const totalHoursReturnedEl = document.querySelector('.jsTotalHoursReturned div .info');
	const totalHoursReturnedImg = document.querySelector('.jsTotalHoursReturned div img');
	const numberOfProcessesEl = document.querySelector('.jsTotalHoursReturnedProcesses div .info');
	const numberOfProcessesImg = document.querySelector('.jsTotalHoursReturnedProcesses div img');
	const numberOfAreasEl = document.querySelector('.jsTotalHoursReturnedAreas div .info');
	const numberOfAreasImg = document.querySelector('.jsTotalHoursReturnedAreas div img');

	const totalHoursReturned = returnedHoursDashboardController.getVariable('totalReturnInHours');

	totalHoursReturnedEl.textContent = totalHoursReturned
		? `${new Intl.NumberFormat(language).format(Math.round(totalHoursReturned))}h`
		: '-';
	numberOfProcessesEl.textContent =
		returnedHoursDashboardController.getNumberOfProcesses() || '0';
	numberOfAreasEl.textContent = JSON.parse(
		document.getElementById('number_of_areas').textContent
	);

	totalHoursReturnedImg.classList.remove('d-none');
	numberOfProcessesImg.classList.remove('d-none');
	numberOfAreasImg.classList.remove('d-none');
}
