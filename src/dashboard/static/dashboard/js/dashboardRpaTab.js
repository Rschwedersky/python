const rpaDashboardController = (() => {
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

	const getInfosByArea = () => {
		const allInfosProcesses = rpaDashboardController.getVariable('processes');
		const rpaSumByArea = [];
		const areas = rpaDashboardController.getVariable('allAreas');

		areas.forEach((area) => {
			let rpaSum = 0;
			let processes = 0;
			const informationByArea = Object.values(allInfosProcesses).filter(
				(x) => x.area == area
			);
			informationByArea.forEach((process) => {
				rpaSum += process.rpa;
				processes++;
			});
			rpaSumByArea.push({
				processes,
				rpaSum,
				area,
			});
		});
		return rpaSumByArea;
	};

	return {
		getVariable,
		getProcessInfo,
		setVariable,
		getNumberOfProcesses,
		getAllVariables,
		getInfosByArea,
	};
})();

function plotRpaProcess(sortRule = 'smaller') {
	const plotId = 'rpa_process';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				ticksuffix: 'h',
				automargin: true,
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

	plotGraphTableRpa('rpa-processes-table');

	const roiProcessPlot = document.getElementById(plotId);
	roiProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'roi_tab');
	});

	function prepareDataForDashboard() {
		const allProcesses = rpaDashboardController.getVariable('allProcesses');

		if (!allProcesses) return [];
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];
		const allProcessesData = [];

		allProcesses.forEach((process) => {
			const processInfo = rpaDashboardController.getProcessInfo(process);

			const { area, rpa } = processInfo;

			const allProcessesRpa = rpaDashboardController.getVariable('totalRpa');
			const totalPercentage = (rpa * 100) / allProcessesRpa;
			rpaDashboardController.setVariable('returnPercentage', totalPercentage, process);

			allProcessesData.push({
				process,
				area,
				rpa,
				totalPercentage,
			});
		});

		rpaDashboardController.setVariable('processesInfo', allProcessesData);

		if (sortRule == 'smaller') {
			allProcessesData.sort((a, b) => a.rpa - b.rpa).forEach(addDataToPlotlyArrays);
		} else {
			allProcessesData.sort((a, b) => b.rpa - a.rpa).forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { process, rpa, area, totalPercentage } = processObj;

			xCoordinates.push(process);
			yCoordinates.push(rpa);

			hoverTexts.push(
				`<b>${process}</b><br><br><span>${
					translate['rpa_runtime'][language]
				}: <b>${formatNumberToLanguage(Math.round(rpa))}h (${formatNumberToLanguage(
					totalPercentage.toFixed(2)
				)}%)</b></span><br><span>${
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
				color: '#11067A',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}
function plotRpaArea(sortRule = 'smaller') {
	const plotId = 'rpa_area';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				ticksuffix: 'h',
				automargin: true,
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

	plotGraphTableRpa('rpa-areas-table');

	const rpaProcessPlot = document.getElementById(plotId);
	rpaProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'rpa_tab');
	});

	function prepareDataForDashboard() {
		const allInfosProcesses = rpaDashboardController.getVariable('processes');
		const rpaArea = [];
		const areas = new Set();
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];

		if (areas instanceof Set) {
			const allProcesses = rpaDashboardController.getVariable('allProcesses');
			allProcesses?.forEach((process) => {
				const processInfo = rpaDashboardController.getProcessInfo(process);
				areas.add(processInfo.area);
			});
		}

		areas.forEach((area) => {
			let processes = 0;
			let thisAreaRpa = 0;

			const informationByArea = Object.entries(allInfosProcesses).filter(
				([processName, processInfo]) => processInfo.area == area
			);

			if (!informationByArea.length) return;

			informationByArea.forEach(([processName, processInfo]) => {
				thisAreaRpa += processInfo.rpa;
				processes++;
			});
			const totalRpa = rpaDashboardController.getVariable('totalRpa');

			const returnPercentage = (thisAreaRpa * 100) / totalRpa;
			rpaArea.push({
				processes,
				area,
				rpa: thisAreaRpa,
				returnPercentage,
			});
		});

		rpaDashboardController.setVariable('areasInfo', rpaArea);

		if (sortRule == 'smaller') {
			rpaArea.sort((a, b) => a.rpa - b.rpa).forEach(addDataToPlotlyArrays);
		} else {
			rpaArea.sort((a, b) => b.rpa - a.rpa).forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { process, rpa, area } = processObj;
			const allProcessesRpa = rpaDashboardController.getVariable('totalRpa');
			const totalPercentage = (rpa * 100) / allProcessesRpa;
			rpaDashboardController.setVariable('returnPercentage', totalPercentage, process);
			const numberOfProcesses = rpaDashboardController.getNumberOfProcesses();

			xCoordinates.push(area);
			yCoordinates.push(rpa);

			hoverTexts.push(
				`<b>${area}</b><br><br><span>${
					translate['rpa_runtime'][language]
				}: <b>${formatNumberToLanguage(Math.round(rpa))}h (${formatNumberToLanguage(
					totalPercentage.toFixed(2)
				)}%)</b></span><br><span>${
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
				color: '#3424C4',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}

function plotRpaHistory(sortRule = 'month') {
	const plotId = 'rpa-history';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				ticksuffix: 'h',
				automargin: true,
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
			let rpaInThisDay = 0;
			let numberOfProcesses = 0;
			const robots = new Set();

			Object.values(dateInfo.processes).forEach((process) => {
				rpaInThisDay += process.time;
				numberOfProcesses++;
				robots.add(process.robot);
			});
			const data = {
				rpaInThisDay,
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
				.sort((a, b) => a.rpa - b.rpa)
				.filter(differentMonths)
				.forEach(addDataToPlotlyArrays);
		} else {
			allProcessesData.sort((a, b) => b.rpa - a.rpa).forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { rpaInThisDay, numberOfProcesses, numberOfRobots, date } = processObj;
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

				const { rpa, numberOfProcesses, numberOfRobots } = thisMonthData.reduce(
					(prevCount, currentProcess) => {
						return {
							rpa: prevCount.rpa + currentProcess.rpaInThisDay,
							numberOfProcesses:
								prevCount.numberOfProcesses + currentProcess.numberOfProcesses,
							numberOfRobots:
								prevCount.numberOfRobots + currentProcess.numberOfRobots,
						};
					},
					{
						rpa: 0,
						numberOfProcesses: 0,
						numberOfRobots: 0,
					}
				);

				yCoordinates.push(rpa);

				hoverTexts.push(
					`<b>${capitalize(monthText)}</b><br><br><span>${
						translate['rpa_runtime'][language]
					}: <b>${formatNumberToLanguage(Math.round(rpa))}h</b></span><br><span>${
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
				yCoordinates.push(rpaInThisDay);

				hoverTexts.push(
					`<b>${dayText}</b><br><br><span>${
						translate['rpa_runtime'][language]
					}: <b>${formatNumberToLanguage(
						Math.round(rpaInThisDay)
					)}h</b></span><br><span>Processos: <b>${numberOfProcesses}</b></span></span><br><span>${
						translate['processes_capital_plural'][language]
					}: <b>${numberOfRobots}</b></span><extra></extra>`
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
				color: '#11067A',
				width: 1,
			},
			text: yCoordinates.map((item) => `<b>${formatNumberToLanguage(Math.round(item))}h</b>`),
			textposition: 'auto',
		};

		return [trace];
	}
}

function plotGraphTableRpa(tableId) {
	const infoTable = document.getElementById(tableId);
	const tableBody = infoTable.querySelector('tbody');
	tableBody.innerHTML = '';

	if (tableId === 'rpa-processes-table') {
		const processes = rpaDashboardController.getVariable('processesInfo');
		processes.forEach((processInfo) => {
			const { rpa, totalPercentage, process } = processInfo;
			const tableRow = document.createElement('tr');
			const gainElement = document.createElement('td');
			const nameElement = document.createElement('td');

			gainElement.textContent = `${formatNumberToLanguage(
				Math.round(rpa)
			)}h (${formatNumberToLanguage(totalPercentage.toFixed(2))}%)`;
			gainElement.classList.add('font-weight-bold');
			nameElement.classList.add('font-weight-bold');

			nameElement.textContent = process;
			tableRow.appendChild(gainElement);
			tableRow.appendChild(nameElement);
			tableBody.appendChild(tableRow);
		});
	} else {
		const areas = rpaDashboardController.getVariable('areasInfo');

		areas.forEach((areaInfo) => {
			const { rpa, returnPercentage, area } = areaInfo;
			const tableRow = document.createElement('tr');
			const gainElement = document.createElement('td');
			const nameElement = document.createElement('td');

			gainElement.textContent = `${formatNumberToLanguage(
				Math.round(rpa)
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

function updateRpaVariables() {
	const allProcesses = new Set();
	const allAreas = new Set();
	let totalRpa = 0;
	Object.entries(allTabsVariables.allprocesses).forEach(([processName, processInfo]) => {
		const thisProcessBackendInfo = lastDashboardJson['all_processes'][processName];
		if (!thisProcessBackendInfo) return;

		const thisProcessRpaValue = processInfo.rpaHours;
		const thisProcessDates = processInfo.dates;
		totalRpa += processInfo.rpaHours;

		const { area } = allTabsVariables.allprocesses[processName];

		rpaDashboardController.setVariable('area', area, processName);
		rpaDashboardController.setVariable('rpa', thisProcessRpaValue, processName);
		rpaDashboardController.setVariable('dates', thisProcessDates, processName);

		allProcesses.add(processName);
		allAreas.add(area);
	});
	rpaDashboardController.setVariable('allProcesses', Array.from(allProcesses));
	rpaDashboardController.setVariable('allAreas', Array.from(allAreas));
	rpaDashboardController.setVariable('totalRpa', totalRpa);
}

function makeRpaBoxes() {
	const totalRpaEl = document.querySelector('.jsTotalRpa div .info');
	const totalRpaImg = document.querySelector('.jsTotalRpa div img');
	const numberOfProcessesEl = document.querySelector('.jsTotalRpaProcesses div .info');
	const numberOfProcessesImg = document.querySelector('.jsTotalRpaProcesses div img');
	const numberOfAreasEl = document.querySelector('.jsTotalRpaAreas div .info');
	const numberOfAreasImg = document.querySelector('.jsTotalRpaAreas div img');

	const totalRpa = rpaDashboardController.getVariable('totalRpa');

	totalRpaEl.textContent = totalRpa
		? `${new Intl.NumberFormat(language).format(Math.round(totalRpa))}h`
		: '-';
	numberOfProcessesEl.textContent = rpaDashboardController.getNumberOfProcesses() || '0';
	numberOfAreasEl.textContent = JSON.parse(
		document.getElementById('number_of_areas').textContent
	);

	totalRpaImg.classList.remove('d-none');
	numberOfProcessesImg.classList.remove('d-none');
	numberOfAreasImg.classList.remove('d-none');
}
