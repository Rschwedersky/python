const roiDashboardController = (() => {
	const allRoiVariables = {
		processes: {},
	};

	const getAllVariables = () => ({ ...allRoiVariables });

	const getRoiVariable = (key) => allRoiVariables[key];

	const getProcessRoiInfo = (process) => allRoiVariables.processes[process];

	const setRoiVariable = (key, value, process = null) => {
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

	const deleteRoiVariable = (key) => delete allRoiVariables[key];

	const getNumberOfProcesses = () => Object.keys(allRoiVariables.processes).length;
	const getOverallRoi = (beautified = false) => {
		if (beautified) {
			const overallRoi = allRoiVariables.todayRoi;

			if (!overallRoi) return null;
			return `${new Intl.NumberFormat(language).format((overallRoi * 100).toFixed(2))}%`;
		} else {
			return allRoiVariables.todayRoi;
		}
	};
	const getInfosByArea = () => {
		const allInfosProcesses = roiDashboardController.getRoiVariable('processes');
		const roiSumByArea = [];
		const areas = new Set();

		if (areas instanceof Set) {
			const allProcesses = roiDashboardController.getRoiVariable('allProcesses');
			allProcesses?.forEach((process) => {
				const processInfo = roiDashboardController.getProcessRoiInfo(process);
				areas.add(processInfo.area);
			});
		}

		areas.forEach((area) => {
			let processes = 0;
			let thisAreaInvestment = 0;
			let thisAreaProfit = 0;
			const thisAreaStatus = {
				Faulted: 0,
				Successful: 0,
			};
			const informationByArea = Object.entries(allInfosProcesses).filter(
				([processName, processInfo]) => processInfo.area == area
			);

			if (!informationByArea.length) return;

			informationByArea.forEach(([processName, processInfo]) => {
				const thisProcessStatusRecord =
					dashboardController.getProcessInfo(processName).statusByDay || [];

				Object.values(thisProcessStatusRecord).forEach((record) => {
					thisAreaStatus.Faulted += record.Faulted;
					thisAreaStatus.Successful += record.Successful;
				});

				thisAreaInvestment += processInfo.investment;
				thisAreaProfit += processInfo.manualProcessCost - processInfo.investment;
				processes++;
			});
			const completionRate =
				1 -
				(thisAreaStatus['Successful'] / thisAreaStatus['Successful'] +
					thisAreaStatus['Faulted']) *
					0.8;

			const thisAreaRoi = thisAreaProfit / (thisAreaInvestment * completionRate);

			roiSumByArea.push({
				processes,
				area,
				roi: thisAreaRoi,
			});
		});
		return roiSumByArea;
	};

	const getDaysUntilPositiveRoi = (beautified = false) => {
		const positiveRoiDay = getRoiVariable('positiveRoiDay');

		if (!positiveRoiDay) return '-';

		const today = new Date();
		const positiveRoiDayObj = getDateObj(positiveRoiDay);
		const diffInMs = positiveRoiDayObj - today;
		const diffInDays = diffInMs / (1000 * 60 * 60 * 24);

		return beautified
			? `${Math.abs(Math.round(diffInDays))} ${translate['days'][language]}`
			: Math.round(diffInDays);
	};

	return {
		getRoiVariable,
		getProcessRoiInfo,
		setRoiVariable,
		getNumberOfProcesses,
		getOverallRoi,
		getAllVariables,
		getDaysUntilPositiveRoi,
		getInfosByArea,
		deleteRoiVariable,
	};
	f;
})();

function plotRoiProcess(sortRule = 'roi_smaller') {
	const plotId = 'roi_process';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				tickformat: ',.0%',
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
		container: '.sideinfos__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	plotSideInfos(plotId);

	const roiProcessPlot = document.getElementById(plotId);
	roiProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'roi_tab');
	});

	function prepareDataForDashboard() {
		const allProcesses = roiDashboardController.getRoiVariable('allProcesses');

		if (!allProcesses) return [];
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];
		const allProcessesData = [];

		allProcesses.forEach((process) => {
			const processInfo = roiDashboardController.getProcessRoiInfo(process);
			const { area, roi } = processInfo;

			allProcessesData.push({
				process,
				roi,
				area,
			});
		});

		if (sortRule == 'roi_smaller') {
			allProcessesData.sort((a, b) => a.roi - b.roi).forEach(addDataToPlotlyArrays);
		} else {
			allProcessesData.sort((a, b) => b.roi - a.roi).forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { process, roi, area } = processObj;

			xCoordinates.push(process);
			yCoordinates.push(roi);

			hoverTexts.push(
				`<b>${process}</b><br><br><span>ROI: <b>${formatNumberToLanguage(
					(roi * 100).toFixed(2)
				)}%</b></span><br><span>${
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
				color: '#11067a',
				width: 1,
			},
			text: yCoordinates.map(
				(item) => `<b>${formatNumberToLanguage((item * 100).toFixed(2))}%</b>`
			),
			textposition: 'auto',
		};

		return [trace];
	}
}
function plotRoiArea(sortRule = 'roi_smaller') {
	const plotId = 'roi_area';

	const dashboardConfig = {
		layout: {
			yaxis: {
				autorange: true,
				tickformat: ',.0%',
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
		container: '.sideinfos__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard();

	makePlot(plotId, dashboardData, dashboardConfig);

	plotSideInfos(plotId);

	const roiProcessPlot = document.getElementById(plotId);
	roiProcessPlot.on('plotly_click', (data) => {
		const type = 'process';
		const processFilter = data.points[0].x;
		const singleFilter = document.querySelector(`.single_filter.${type}`);
		newClickOnChart(type, singleFilter, processFilter, 'roi_tab');
	});

	function prepareDataForDashboard() {
		const infosByArea = roiDashboardController.getInfosByArea();

		if (!infosByArea) return [];
		const xCoordinates = [];
		const yCoordinates = [];
		const hoverTexts = [];

		if (sortRule == 'roi_smaller') {
			infosByArea.sort((a, b) => a.roi - b.roi).forEach(addDataToPlotlyArrays);
		} else {
			infosByArea.sort((a, b) => b.roi - a.roi).forEach(addDataToPlotlyArrays);
		}

		function addDataToPlotlyArrays(processObj) {
			const { processes, roi, area } = processObj;

			xCoordinates.push(area);
			yCoordinates.push(roi);

			hoverTexts.push(
				`<b>${area}</b><br><br><span>ROI: <b>${formatNumberToLanguage(
					(roi * 100).toFixed(2)
				)}%</b></span><br><span>${
					translate['processes'][language]
				}: <b>${processes}</b></span><extra></extra>`
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
			text: yCoordinates.map(
				(item) => `<b>${formatNumberToLanguage((item * 100).toFixed(2))}%</b>`
			),
			textposition: 'auto',
		};

		return [trace];
	}
}

function plotRoiHistory(sortRule = 'roi_month') {
	const plotId = 'roi_history';

	roiDashboardController.deleteRoiVariable('positiveRoiDay');

	const today = new Date().toISOString().replace(/T.*/, ''); // yyyy-mm-dd

	const dashboardConfig = {
		layout: {
			font: {
				color: '#000',
			},
			plot_bgcolor: '#ffffff',
			paper_bgcolor: '#ffffff',
			yaxis: {
				tickprefix: 'R$ ',
				tickformat: ',.2f',
				automargin: true,
			},
			xaxis: { automargin: true },
			separator: getDecimalSeparator(),
			showlegend: false,
			hovermode: 'closest',
			shapes: sortRule
				? [
						{
							type: 'line',
							x0: today,
							y0: 0,
							x1: today,
							y1: 50000,
							line: {
								color: '#aaa',
								width: 3,
							},
						},
				  ]
				: [],
			textposition: 'auto',
		},
		container: '.sideinfos__dashboard',
	};

	if (!sortRule) {
		makePlot(plotId, [], dashboardConfig);
		plotSideInfos(plotId, true);
		return;
	}

	const dashboardData = prepareDataForDashboard(sortRule);

	makePlot(plotId, dashboardData, dashboardConfig);
	plotSideInfos(plotId);

	function prepareDataForDashboard(sortRule) {
		const allProcesses = roiDashboardController.getRoiVariable('allProcesses');
		if (!allProcesses || !allProcesses.length) return [];

		const xCoordinates = [];
		const yCoordinatesOfAutomatedProcesses = [];
		const yCoordinatesOfManualProcesses = [];
		const humanHoverTexts = [];
		const rpaHoverTexts = [];
		const dates = new Set();
		let biggestValue = 0;
		let totalInvestment = 0;
		let totalManualCost = 0;

		allProcesses.forEach((process) => {
			const processInfo = roiDashboardController.getProcessRoiInfo(process);

			if (!allProcesses) return [];
			const { investment, manualProcessCost } = processInfo;

			totalInvestment += investment;
			totalManualCost += manualProcessCost;

			Object.keys(processInfo.dates).forEach((date) => dates.add(date));
		});
		let value = totalManualCost;
		const checkIfMonthChanged = monthCounter();
		let roiIsPositive = totalManualCost > totalInvestment;
		let todayHasPassed = false;
		const sortedDates = Array.from(dates).sort((a, b) => new Date(a) - new Date(b));
		sortedDates.forEach((date, index) => {
			const dateObj = getDateObj(date);
			const isDifferentMonth = checkIfMonthChanged(date);
			const isToday = getDateObj(date).toDateString() === new Date().toDateString();
			const isSameYearAsToday = dateObj.getFullYear() === new Date().getFullYear();
			const isNextYear = dateObj.getFullYear() + 1 == new Date().getFullYear();
			const isNextMonth = dateObj.getMonth() + 1 > new Date().getMonth() + 1;
			const isNextMonthOfNextYear =
				dateObj.getMonth() + 1 > 0 &&
				dateObj.getMonth() + 1 < 12 &&
				new Date().getMonth() + 1 == 12;

			if (isDifferentMonth && index > 0) {
				value += totalManualCost;
			}

			if (isToday || (!todayHasPassed && dateObj > new Date())) {
				setTodayRoi(dateObj, false);
			}

			if ((isSameYearAsToday && isNextMonth) || (isNextYear && isNextMonthOfNextYear)) {
				todayHasPassed = true;
			}

			if (sortRule == 'roi_month') {
				if (isDifferentMonth) {
					const firstDayOfTheMonth = date.replace(/\d{2}$/, '01');
					xCoordinates.push(firstDayOfTheMonth);

					yCoordinatesOfManualProcesses.push(value);
					yCoordinatesOfAutomatedProcesses.push(totalInvestment);

					const fakeProcess = {
						roi: calculateRoi(totalInvestment, value),
						manualProcessCost: value,
						investment: totalInvestment,
					};

					pushDateToHoverTexts(date, fakeProcess);

					if (!roiIsPositive && value > totalInvestment) {
						goBackAndFindPositiveRoiDay(firstDayOfTheMonth);
					}
				}
			} else {
				if (xCoordinates.includes(date)) return;
				xCoordinates.push(date);
				yCoordinatesOfManualProcesses.push(value);
				yCoordinatesOfAutomatedProcesses.push(totalInvestment);

				const fakeProcess = {
					roi: calculateRoi(totalInvestment, value),
					manualProcessCost: value,
					investment: totalInvestment,
				};

				pushDateToHoverTexts(date, fakeProcess);
			}

			checkAndSetBiggestYAxisValue(totalInvestment, value);
		});
		let count = 0;
		if (!roiIsPositive) {
			const lastDate = Array.from(sortedDates).at(-1);
			const lastDateObj = getDateObj(lastDate);
			const currentDate = lastDateObj;

			while (!roiIsPositive || count < 50) {
				const currentDay = currentDate.getDate();
				const date = currentDate.toLocaleDateString('pt-br').split('/').reverse().join('-');
				const dateObj = getDateObj(date);
				const isDifferentMonth = checkIfMonthChanged(date);
				const isToday = dateObj.toDateString() === new Date().toDateString();

				if (isDifferentMonth) {
					value += totalManualCost;
				}

				if (roiIsPositive) {
					count++;
				}

				if (isToday) {
					setTodayRoi(dateObj);
				}

				if (sortRule == 'roi_month') {
					if (isDifferentMonth) {
						const firstDayOfTheMonth = date.replace(/\d{2}$/, '01');
						xCoordinates.push(firstDayOfTheMonth);

						yCoordinatesOfManualProcesses.push(value);
						yCoordinatesOfAutomatedProcesses.push(totalInvestment);

						const fakeProcess = {
							roi: calculateRoi(totalInvestment, value),
							manualProcessCost: value,
							investment: totalInvestment,
						};

						pushDateToHoverTexts(date, fakeProcess);

						if (value > totalInvestment && dashboardConfig.layout.shapes.length < 2) {
							goBackAndFindPositiveRoiDay(date);
						}

						checkAndSetBiggestYAxisValue(totalInvestment, value);
					}
				} else {
					// todo
				}

				currentDate.setDate(currentDay + 1);
			}
		}

		count = 0;
		if (!todayHasPassed) {
			const lastDate = xCoordinates.at(-1);
			const lastDateObj = getDateObj(lastDate);
			const currentDate = lastDateObj;

			while (!todayHasPassed || count < 50) {
				const currentDay = currentDate.getDate();
				const date = currentDate.toLocaleDateString('pt-br').split('/').reverse().join('-');
				const dateObj = getDateObj(date);
				const isDifferentMonth = checkIfMonthChanged(date);
				const isToday = dateObj.toDateString() === new Date().toDateString();

				if (isDifferentMonth) {
					value += totalManualCost;
				}

				if (todayHasPassed) {
					count++;
				}

				if (isToday || (!todayHasPassed && dateObj > new Date())) {
					setTodayRoi(dateObj);
				}

				if (sortRule == 'roi_month') {
					if (isDifferentMonth) {
						const firstDayOfTheMonth = date.replace(/\d{2}$/, '01');
						xCoordinates.push(firstDayOfTheMonth);

						yCoordinatesOfManualProcesses.push(value);
						yCoordinatesOfAutomatedProcesses.push(totalInvestment);

						const fakeProcess = {
							roi: calculateRoi(totalInvestment, value),
							manualProcessCost: value,
							investment: totalInvestment,
						};

						pushDateToHoverTexts(date, fakeProcess);
					}
				}

				checkAndSetBiggestYAxisValue(totalInvestment, value);

				currentDate.setDate(currentDay + 1);
			}
		}

		const rpaTrace = {
			type: 'scatter',
			x: xCoordinates,
			y: yCoordinatesOfAutomatedProcesses,
			hovertemplate: rpaHoverTexts,
			hoverlabel: {
				bgcolor: '#000',
				font: { color: '#fff' },
			},
			line: { color: '#11067a' },
		};

		const humanTrace = {
			type: 'scatter',
			x: xCoordinates,
			y: yCoordinatesOfManualProcesses,
			hovertemplate: humanHoverTexts,
			hoverlabel: {
				bgcolor: '#000',
				font: { color: '#fff' },
			},
			line: { color: '#17EAAC' },
		};

		updateYAxisOfVerticalLines(biggestValue);

		return [rpaTrace, humanTrace];

		function pushDateToHoverTexts(date, process) {
			const dateObj = getDateObj(date);

			const processInfo =
				typeof process == 'string'
					? roiDashboardController.getProcessRoiInfo(process)
					: process;

			const { roi, manualProcessCost, investment } = processInfo;
			const numberOfProcesses = roiDashboardController.getNumberOfProcesses();

			const monthAndYearText = dateObj.toLocaleString(language, {
				month: 'long',
				year: 'numeric',
			});

			const roiBeautified = new Intl.NumberFormat(language).format((roi * 100).toFixed(2));
			const manualProcessCostBeautified = new Intl.NumberFormat(language, {
				style: 'currency',
				currency: 'BRL',
				minimumFractionDigits: 2,
			}).format(manualProcessCost);

			const investmentBeautified = new Intl.NumberFormat(language, {
				style: 'currency',
				currency: 'BRL',
				minimumFractionDigits: 2,
			}).format(investment);

			const numberOfProcessesBeautified = new Intl.NumberFormat(language).format(
				numberOfProcesses
			);

			const hoverTextString = `<b>${capitalize(
				monthAndYearText
			)}</b><br><br>ROI: <b>${roiBeautified}%</b><br>Processos manuais: <b>${manualProcessCostBeautified}</b><br>Processos automatizados: <b>${investmentBeautified}</b><br>Processos: <b>${numberOfProcessesBeautified}</b><extra></extra>`;

			humanHoverTexts.push(hoverTextString);
			rpaHoverTexts.push(hoverTextString);
		}

		function setTodayRoi(dateObj, markTodayAsPassed = true) {
			const numberOfDaysInThisMonth = getMonthNumberOfDays(
				dateObj.getFullYear(),
				dateObj.getMonth() + 1
			);
			const dailyManualCost = totalManualCost / numberOfDaysInThisMonth;
			const manualCostFromDayOneToThisDay = (new Date().getDate() - 1) * dailyManualCost;
			const updatedValue = value + manualCostFromDayOneToThisDay;
			const todayRoi = (updatedValue - totalInvestment) / totalInvestment;
			roiDashboardController.setRoiVariable('todayRoi', todayRoi);

			if (markTodayAsPassed) todayHasPassed = true;
		}

		function goBackAndFindPositiveRoiDay(date) {
			const thisDate = getDateObj(date);
			const numberOfDaysInThisMonth = getMonthNumberOfDays(
				thisDate.getFullYear(),
				thisDate.getMonth() + 1
			);
			const lastManualCost = yCoordinatesOfManualProcesses.at(-2);
			const lastInvestment = yCoordinatesOfAutomatedProcesses.at(-2);

			const manualCostDiff =
				value > lastManualCost ? value - lastManualCost : lastManualCost - value;

			const manualCostByDay = manualCostDiff / numberOfDaysInThisMonth;

			let days = 0;
			let accumulatedManualCost = value;
			const investmentDiff =
				totalInvestment > lastInvestment
					? totalInvestment - lastInvestment
					: lastInvestment - totalInvestment;
			let accumulatedInvestment = totalInvestment;
			const investmentByDay = investmentDiff / numberOfDaysInThisMonth;

			while (accumulatedManualCost > accumulatedInvestment) {
				//Calculating the exact point where the manual cost passes the investment
				if (value > lastManualCost) {
					accumulatedManualCost -= manualCostByDay;
				} else {
					accumulatedManualCost += manualCostByDay;
				}

				if (totalInvestment >= lastInvestment) {
					accumulatedInvestment -= investmentByDay;
				} else {
					accumulatedInvestment += investmentByDay;
				}

				days++;
			}

			const tempDate = getDateObj(date);

			const positiveRoiDay = new Date(thisDate.setDate(tempDate.getDate() - days))
				.toLocaleDateString('pt-BR')
				.split('/')
				.reverse()
				.join('-');

			checkAndCreateDashedLineOnPlot(positiveRoiDay, dashboardConfig);
			roiIsPositive = true;
		}

		function checkAndSetBiggestYAxisValue(investment, manualCost) {
			if (investment > biggestValue) {
				biggestValue = investment;
			}

			if (manualCost > biggestValue) {
				biggestValue = manualCost;
			}
		}
	}

	function getDecimalSeparator() {
		const test = new Intl.NumberFormat(language).format(1981.81);

		if (test.indexOf(',') < test.indexOf('.')) {
			return '.,';
		} else {
			return ',.';
		}
	}

	function updateYAxisOfVerticalLines(value) {
		dashboardConfig.layout.shapes = dashboardConfig.layout.shapes.map((shape) => {
			const copy = { ...shape };
			copy.y1 = value;
			return copy;
		});
	}
}

function plotSideInfos(divId, empty = false) {
	const html = makeSideInfoBox(divId, empty);
	const placeToAppend = document
		.getElementById(divId)
		.closest('.dashboard')
		.querySelector('.sideinfos_mini_tables');

	if (typeof html == 'string') {
		placeToAppend.innerHTML = html;
	} else {
		if (placeToAppend.children.length) {
			Array.from(placeToAppend.children).forEach((el) => el.remove());
		}
		placeToAppend.append(html);
	}

	document.querySelectorAll('.jsNewTooltip').forEach((el) => {
		$(el).tooltip({
			boundary: 'window',
		});
		el.classList.remove('jsNewTooltip');
	});
}

function makeSideInfoBox(plotId, empty) {
	if (plotId == 'roi_history') {
		const infos = {
			numberOfProcesses: {
				value: roiDashboardController.getNumberOfProcesses(),
				label: 'processos',
			},
			overallRoi: {
				value: getRoiEl(roiDashboardController.getOverallRoi()),
				label: 'de ROI',
			},
			prediction: {
				value: roiDashboardController.getDaysUntilPositiveRoi(true),
				label: `${
					roiDashboardController.getOverallRoi() > 0
						? translate['of_positive_roi'][language]
						: translate['until_the_positive_roi'][language]
				} <i class="fas fa-info-circle jsNewTooltip" data-toggle="tooltip" data-html="true" title="Momento que o valor investido na automação passa a ser menor que o do processo manual.<br><br>Indica quando você estará lucrando com a implementação da automação."></i>`,
			},
		};

		const box = document.createElement('article');
		box.classList.add('dashboard-box', 'p-3', 'd-flex', 'flex-column', 'ignore');

		Object.values(infos).forEach((info, index) => {
			const textContainer = document.createElement('div');
			const firstSpan = document.createElement('span');
			const secondSpan = document.createElement('span');

			textContainer.classList.add('d-flex', 'flex-column');

			if (empty) {
				firstSpan.innerHTML = '';
			} else {
				firstSpan.innerHTML = info.value;
			}
			secondSpan.innerHTML = info.label;

			firstSpan.classList.add('font-weight-bold', 'f-size-18');
			secondSpan.classList.add('f-size-14');

			textContainer.append(firstSpan, secondSpan);

			if (index + 1 !== Object.keys(infos).length) {
				const hr = document.createElement('hr');
				hr.classList.add('w-100');
				textContainer.append(hr);
			}

			box.append(textContainer);
		});

		return box;
	} else {
		if (plotId == 'roi_area') {
			const infosByArea = roiDashboardController.getInfosByArea();

			return (
				infosByArea?.reduce((previousHtml, currentProcess) => {
					const headerType = currentProcess.roi > 0 ? 'positive' : 'negative';
					return (previousHtml += `
				<div class="dashboard-box p-3 backcolorfafafa ${headerType}">
					<div class="d-flex align-items-center">
						<span>
							<i class="fas fa-arrow-up"></i>
							<i class="fas fa-arrow-down"></i>
						</span>
						<b class="f-size-22 info mb-0">${formatNumberToLanguage(
							(currentProcess.roi * 100).toFixed(2)
						)} %</b>
					</div>
					<p class="f-size-14 mb-0">${currentProcess.area}</p>
				</div>
			`);
				}, '') || ''
			);
		}

		if (empty) return '';
		const allProcesses = roiDashboardController.getRoiVariable('allProcesses');
		if (!allProcesses) return '';

		return allProcesses.reduce((previousHtml, currentProcess) => {
			const processInfo = roiDashboardController.getProcessRoiInfo(currentProcess);
			const { roi } = processInfo;
			const headerType = roi > 0 ? 'positive' : 'negative';
			return (previousHtml += `
			<div class="dashboard-box p-3 backcolorfafafa ${headerType}">
				<div class="d-flex align-items-center">
					<span>
						<i class="fas fa-arrow-up"></i>
						<i class="fas fa-arrow-down"></i>
					</span>
					<b class="f-size-22 info mb-0">${formatNumberToLanguage((roi * 100).toFixed(2))} %</b>
				</div>
				<p class="f-size-14 mb-0">${currentProcess}</p>
			</div>
		`);
		}, '');
	}

	function getRoiEl(roi) {
		if (!roi) return '';
		const beautifiedRoi = (roi * 100).toFixed(2);
		if (roi > 0) {
			return `<i class="fas fa-arrow-up mr-2"></i><span style="color: #198754">${
				beautifiedRoi || ''
			}%</span>`;
		} else {
			return `<i class="fas fa-arrow-down mr-2"></i><span style="color: #DC3545">${
				beautifiedRoi || ''
			}%</span>`;
		}
	}
}

function updateRoiVariables() {
	const allProcesses = new Set();
	Object.entries(allTabsVariables.allprocesses).forEach(([processName, processInfo]) => {
		const thisProcessBackendInfo = lastDashboardJson['all_processes'][processName];
		if (!thisProcessBackendInfo) return;

		const thisProcessInvestment = thisProcessBackendInfo.investment;
		const thisProcessRoi = thisProcessBackendInfo.roi;
		const thisProcessManualCost = thisProcessBackendInfo['manual_process_cost'];
		const thisProcessMonthlyTasks = thisProcessBackendInfo['monthly_tasks'];
		const thisProcessMinutesInTask = thisProcessBackendInfo['minutes_in_task'];
		const thisProcessAverageHourValue = thisProcessBackendInfo['average_hour_value'];
		const thisProcessDates = processInfo.dates;

		const { area } = allTabsVariables.allprocesses[processName];

		roiDashboardController.setRoiVariable('area', area, processName);
		roiDashboardController.setRoiVariable('roi', thisProcessRoi, processName);
		roiDashboardController.setRoiVariable('monthlyTasks', thisProcessMonthlyTasks, processName);
		roiDashboardController.setRoiVariable(
			'minutesInTask',
			thisProcessMinutesInTask,
			processName
		);
		roiDashboardController.setRoiVariable('investment', thisProcessInvestment, processName);
		roiDashboardController.setRoiVariable(
			'manualProcessCost',
			thisProcessManualCost,
			processName
		);
		roiDashboardController.setRoiVariable(
			'averageHourValue',
			thisProcessAverageHourValue,
			processName
		);
		roiDashboardController.setRoiVariable('dates', thisProcessDates, processName);

		allProcesses.add(processName);
	});
	roiDashboardController.setRoiVariable('allProcesses', Array.from(allProcesses));
}

function calculateRoi(investment, manualProcessCost) {
	return (manualProcessCost - investment) / investment;
}

function makeRoiBoxes() {
	const overallRoiEl = document.querySelector('.roi_investment div .info');
	const overallRoiImg = document.querySelector('.roi_investment div img');
	const numberOfProcessesEl = document.querySelector('.roi_process div .info');
	const numberOfProcessesImg = document.querySelector('.roi_process div img');
	const numberOfAreasEl = document.querySelector('.roi_areas div .info');
	const numberOfAreasImg = document.querySelector('.roi_areas div img');

	overallRoiEl.textContent = roiDashboardController.getOverallRoi(true) || '-';
	numberOfProcessesEl.textContent = roiDashboardController.getNumberOfProcesses() || '0';
	numberOfAreasEl.textContent = JSON.parse(
		document.getElementById('number_of_areas').textContent
	);

	overallRoiImg.classList.remove('d-none');
	numberOfProcessesImg.classList.remove('d-none');
	numberOfAreasImg.classList.remove('d-none');
}

function fireEmptyStateRoiModal() {
	const fakeTriggerEl = document.createElement('button');
	fakeTriggerEl.setAttribute('data-toggle', 'modal');
	fakeTriggerEl.setAttribute('data-target', '#dashboard-modal');
	fakeTriggerEl.setAttribute('data-modal', 'empty-state-roi');

	document.body.append(fakeTriggerEl);
	fakeTriggerEl.click();
	fakeTriggerEl.remove();
}

function getDateObj(date) {
	return new Date(new Date(date).setDate(new Date(date).getDate() + 1));
}

function getMonthNumberOfDays(year, month) {
	return new Date(year, month, 0).getDate();
}

function checkAndCreateDashedLineOnPlot(date, config) {
	const overallRoi = roiDashboardController.getOverallRoi();
	const roiIsPositiveDrawLineBack = overallRoi > 0 && getDateObj(date) < new Date();
	const roiIsNegativeDrawLineAfter = overallRoi < 0 && getDateObj(date) > new Date();

	if (roiIsPositiveDrawLineBack || roiIsNegativeDrawLineAfter || !overallRoi) {
		config.layout.shapes = config.layout.shapes.concat({
			type: 'line',
			x0: `${date} 12:00`,
			y0: 0,
			x1: `${date} 12:00`,
			y1: 50000,
			line: {
				color: '#aaa',
				width: 1,
				dash: 'dash',
			},
		});
		roiDashboardController.setRoiVariable('positiveRoiDay', date);
	}
}
