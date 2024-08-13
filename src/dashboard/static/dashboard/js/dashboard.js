let lastDashboardJson = {};
let processes_infos = {};
let globalFilter = {};
let allTabsVariables = resetAllTabsVariables();
let needOccupationByHourThroughDay = false;

const dashboardController = (() => {
	const reference = {
		processes: {},
	};

	const getVariable = (key) => reference[key];

	const getProcessInfo = (process) => reference.processes[process];

	const setVariable = (key, value, process = null) => {
		if (process) {
			if (!(process in reference.processes)) {
				reference.processes[process] = {};
			}

			const thisProcessInfo = reference.processes[process];

			thisProcessInfo[key] = value;
		} else {
			reference[key] = value;
		}
	};

	const updateVariable = (key, callback, process = null) => {
		if (process) {
			if (!reference.processes[process]) reference.processes[process] = {};

			const newValue = callback(reference.processes[process][key]);
			reference.processes[process][key] = newValue;
			return reference.processes[process][key];
		} else {
			const newValue = callback(reference[key]);
			reference[key] = newValue;
			return reference[key];
		}
	};

	const getNumberOfProcesses = () => Object.keys(reference.processes).length;
	const getOverallRoi = (beautified = false) => {
		const totalRoi = Object.values(reference.processes).reduce(
			(previousRoi, currentProcess) => previousRoi + currentProcess.roi,
			0
		);

		const numberOfProcesses = getNumberOfProcesses();

		if (beautified) {
			return `${new Intl.NumberFormat(language).format(
				((totalRoi / numberOfProcesses) * 100).toFixed(2)
			)}%`;
		} else {
			return totalRoi / numberOfProcesses;
		}
	};

	return {
		getVariable,
		getProcessInfo,
		setVariable,
		updateVariable,
		getNumberOfProcesses,
		getOverallRoi,
		getAllVariables: () => ({ ...reference }),
	};
})();

/**********************  EXECUTABLE CODE ********************************/

document.addEventListener('DOMContentLoaded', () => {
	if (!document.getElementById('root')) return;
	Plotly.setPlotConfig({ locale: language.toLowerCase() });

	getNewDashboardJson();
	updateProcessesInfos();

	const orderBySelects = Array.from(document.getElementsByClassName('dashboard-select-order-by'));
	const fullScreenButtons = Array.from(document.getElementsByClassName('button__fullscreen'));
	const customPeriodDates = document.querySelector('#filter_menu .custom_period.set_dates');
	const customPeriodInterval = document.querySelector('#filter_menu .custom_period.set_interval');

	orderBySelects.forEach((select) => select.addEventListener('change', handleOrderBySelect));

	fullScreenButtons.forEach((button) => button.addEventListener('click', handleFullScreen));
	document.addEventListener('fullscreenchange', exitFromFullScreenWithEsc);
	document.addEventListener('webkitfullscreenchange', exitFromFullScreenWithEsc);
	document.addEventListener('mozfullscreenchange', exitFromFullScreenWithEsc);
	document.addEventListener('MSFullscreenChange', exitFromFullScreenWithEsc);

	customPeriodDates.addEventListener('click', handleCustomPeriod);
	customPeriodInterval.addEventListener('focus', handleCustomPeriod);
	customPeriodInterval.addEventListener('change', updateDates);

	$('#downloading-plot-modal').on('shown.bs.modal', (event) => {
		downloadPlot(event);
	});

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

	function updateProcessesInfos() {
		let allSettingsSingleProcesses = Array.from(
			document.querySelectorAll('#manage_settings_tab .single_process')
		);
		allSettingsSingleProcesses.forEach((form_process) => {
			let processName = '';
			let allDivInputFormProcesses = form_process.querySelectorAll('.form_input');
			allDivInputFormProcesses.forEach((input_div) => {
				let input = input_div.querySelector('input');
				if (input !== null) {
					let name_index = input.name;
					if (
						name_index == 'process' ||
						(name_index == 'process_translate' && input.value !== '')
					) {
						processName = input.value;
						processes_infos[input.value] = {};
					} else {
						let value = input.value.replaceAll(',', '').match(/\d+(\.\d{1,2})?/);
						processes_infos[processName][name_index] = value !== null ? value[0] : '';
					}
				} else {
					let input = input_div.querySelector('select');
					processes_infos[processName][input.name] =
						input.options[input.selectedIndex].text;
				}
			});
		});
	}

	function handleOrderBySelect(event) {
		const target = event.target;
		const currentTarget = event.currentTarget;
		if (Boolean(target.value) && target.value != currentTarget.dataset.selected) {
			const whichSelect = currentTarget.id;
			const isEmptyRoi = document
				.getElementById('roi_tab')
				.classList.contains('jsNotAllowed');

			switch (whichSelect) {
				case 'all-areas-select-order':
					plotAllAreasGraph(target.value);
					break;
				case 'all-processes-select-order':
					plotAllProcessesGraph(target.value);
					break;
				case 'rpa-execution-history-detail':
					plotRpaHoursByDay(target.value);
					break;
				case 'all-occupation-robot-select-order':
					plotRobotOccupancyRate(target.value);
					break;
				case 'robot-occupation-time-band-select-order':
					const element = document.querySelector(
						'.single__dashboard  .legend_graphic_area'
					);
					if (target.value == 'single') {
						element.style.display = 'none';
					} else {
						element.style.display = 'block';
					}
					plotAverageOccupationProcesses(target.value);
					break;
				case 'returned-hours-process-select':
					plotReturnedHoursByProcess(target.value);
					break;
				case 'returned-hours-areas-select':
					plotReturnedHoursByArea(target.value);
					break;
				case 'hours-returned-history-select':
					plotReturnedHoursHistory(target.value);
					break;
				case 'roi-process-order':
					plotRoiProcess(isEmptyRoi ? null : target.value);
					break;
				case 'roi-area-order':
					plotRoiArea(isEmptyRoi ? null : target.value);
					break;
				case 'roi-history-order':
					plotRoiHistory(isEmptyRoi ? null : target.value);
					break;
				case 'rpa-process-select':
					plotRpaProcess(target.value);
					break;
				case 'rpa-area-select':
					plotRpaArea(target.value);
					break;
				case 'rpa-history-select':
					plotRpaHistory(target.value);
					break;
			}

			currentTarget.dataset.selected = target.value;
		}
	}

	async function handleFullScreen(event) {
		const element = event.target.closest('.full-screen');
		const whichPlotId = event.currentTarget.dataset.plot;
		const whichSortRule = element.querySelector('select').dataset.selected;

		if (document.fullscreenElement) {
			await document.exitFullscreen();
		} else {
			if (element.requestFullscreen) {
				await element.requestFullscreen();
			} else if (element.webkitRequestFullscreen) {
				/* Safari */ cam;
				await element.webkitRequestFullscreen();
			} else if (element.msRequestFullscreen) {
				/* IE11 */
				await element.msRequestFullscreen();
			}
		}

		handlePlotsAfterFullScreen(whichPlotId, whichSortRule);
	}

	function exitFromFullScreenWithEsc(event) {
		const plot = event.target;
		const whichPlotId = plot.querySelector('.button__fullscreen').dataset.plot;
		const whichSortRule = plot.querySelector('select').dataset.selected;
		if (
			!document.fullscreenElement &&
			!document.webkitIsFullScreen &&
			!document.mozFullScreen &&
			!document.msFullscreenElement
		) {
			handlePlotsAfterFullScreen(whichPlotId, whichSortRule);
		}
	}

	function handlePlotsAfterFullScreen(plotId, sortRule) {
		const isEmptyRoi = document.getElementById('roi_tab').classList.contains('jsNotAllowed');
		switch (plotId) {
			case 'all-areas-hours':
				plotAllAreasGraph(sortRule);
				break;
			case 'all-processes-hours':
				plotAllProcessesGraph(sortRule);
				break;
			case 'rpa-execution-history':
				plotRpaHoursByDay(sortRule);
				break;
			case 'houriddleness_byday':
				plotRobotOccupancyRate(sortRule);
				break;
			case 'average_occupation_byhour':
				plotAverageOccupationProcesses(
					document.getElementById('robot-occupation-time-band-select-order').value
				);
				break;
			case 'returned-hours-process':
				plotReturnedHoursByProcess(sortRule);
				break;
			case 'returned-hours-area':
				plotReturnedHoursByArea(sortRule);
				break;
			case 'hours-returned-history':
				plotReturnedHoursHistory(sortRule);
				break;
			case 'rpa_process':
				plotRpaProcess(sortRule);
				break;
			case 'rpa_area':
				plotRpaArea(sortRule);
				break;
			case 'rpa-history':
				plotRpaHistory(sortRule);
				break;
			case 'roi_process':
				plotRoiProcess(isEmptyRoi ? null : sortRule);
				break;
			case 'roi_area':
				plotRoiArea(isEmptyRoi ? null : sortRule);
				break;
			case 'roi_history':
				plotRoiHistory(isEmptyRoi ? null : sortRule);
				break;
		}
	}
});

let locale = {
	moduleType: 'locale',
	name: 'pt-BR',
	dictionary: {
		Autoscale: 'Escala autom\xe1tica',
		'Box Select': 'Sele\xe7\xe3o retangular',
		'Click to enter Colorscale title': 'Clique para editar o t\xedtulo da escala de cor',
		'Click to enter Component A title': 'Clique para editar o t\xedtulo do Componente A',
		'Click to enter Component B title': 'Clique para editar o t\xedtulo do Componente B',
		'Click to enter Component C title': 'Clique para editar o t\xedtulo do Componente C',
		'Click to enter Plot title': 'Clique para editar o t\xedtulo do Gr\xe1fico',
		'Click to enter X axis title': 'Clique para editar o t\xedtulo do eixo X',
		'Click to enter Y axis title': 'Clique para editar o t\xedtulo do eixo Y',
		'Click to enter radial axis title': 'Clique para editar o t\xedtulo do eixo radial',
		'Compare data on hover': 'Comparar dados ao pairar',
		'Double-click on legend to isolate one trace':
			'Duplo clique na legenda para isolar uma s\xe9rie',
		'Double-click to zoom back out': 'Duplo clique para reverter zoom',
		'Download plot as a png': 'Fazer download do gr\xe1fico como imagem (png)',
		'Download plot': 'Fazer download do gr\xe1fico',
		'Edit in Chart Studio': 'Editar no Chart Studio',
		'IE only supports svg.  Changing format to svg.':
			'IE suporta apenas svg. Alterando formato para svg',
		'Lasso Select': 'Sele\xe7\xe3o de la\xe7o',
		'Orbital rotation': 'Rota\xe7\xe3o orbital',
		Pan: 'Mover',
		'Produced with Plotly': 'Criado com o Plotly',
		Reset: 'Restaurar',
		'Reset axes': 'Restaurar eixos',
		'Reset camera to default': 'Restaurar c\xe2mera para padr\xe3o',
		'Reset camera to last save': 'Restaurar c\xe2mera para \xfaltima salva',
		'Reset view': 'Restaurar vis\xe3o',
		'Reset views': 'Restaurar vis\xf5es',
		'Show closest data on hover': 'Exibir dado mais pr\xf3ximo ao pairar',
		'Snapshot succeeded': 'Captura instant\xe2nea completa',
		'Sorry, there was a problem downloading your snapshot!':
			'Desculpe, houve um problema no download de sua captura instant\xe2nea!',
		'Taking snapshot - this may take a few seconds':
			'Efetuando captura instant\xe2nea - isso pode lelet alguns instantes',
		'Toggle Spike Lines': 'Habilitar/desabilitar triangula\xe7\xe3o de linhas',
		'Toggle show closest data on hover':
			'Habilitar/desabilitar exibi\xe7\xe3o de dado mais pr\xf3ximo ao pairar',
		'Turntable rotation': 'Rota\xe7\xe3o de mesa',
		Zoom: 'Zoom',
		'Zoom in': 'Ampliar zoom',
		'Zoom out': 'Reduzir zoom',
		close: 'fechamento',
		high: 'alta',
		'incoming flow count': 'contagem de fluxo de entrada',
		kde: 'kde',
		lat: 'latitude',
		lon: 'longitude',
		low: 'baixa',
		'lower fence': 'limite inferior',
		max: 'm\xe1ximo',
		'mean \xb1 \u03c3': 'm\xe9dia \xb1 \u03c3',
		mean: 'm\xe9dia',
		median: 'mediana',
		min: 'm\xednimo',
		'new text': 'novo texto',
		open: 'abertura',
		'outgoing flow count': 'contagem de fluxo de sa\xedda',
		q1: 'q1',
		q3: 'q3',
		source: 'origem',
		target: 'destino',
		trace: 's\xe9rie',
		'upper fence': 'limite superior',
	},
	format: {
		days: [
			'Domingo',
			'Segunda-feira',
			'Ter\xe7a-feira',
			'Quarta-feira',
			'Quinta-feira',
			'Sexta-feira',
			'S\xe1bado',
		],
		shortDays: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'S\xe1b'],
		months: [
			'Janeiro',
			'Fevereiro',
			'Mar\xe7o',
			'Abril',
			'Maio',
			'Junho',
			'Julho',
			'Agosto',
			'Setembro',
			'Outubro',
			'Novembro',
			'Dezembro',
		],
		shortMonths: [
			'Jan',
			'Fev',
			'Mar',
			'Abr',
			'Mai',
			'Jun',
			'Jul',
			'Ago',
			'Set',
			'Out',
			'Nov',
			'Dez',
		],
		date: '%d/%m/%Y',
	},
};
'undefined' == typeof Plotly
	? ((window.PlotlyLocales = window.PlotlyLocales || []), window.PlotlyLocales.push(locale))
	: Plotly.register(locale);

/** ************************* GENERIC FUNCTIONS ***************************  */

function loadingOnAllTabs() {
	let allSingleChartContent = document.querySelectorAll('.single_chartcontent > div');
	allSingleChartContent.forEach((singleChartContent) => {
		singleChartContent.innerHTML = getLoadingDiv();
	});

	let allHeaderInfos = document.querySelectorAll('.resumed_infos div .d-flex b');
	allHeaderInfos.forEach((headerInfo) => {
		headerInfo.innerHTML = `<div>${getLoadingDiv(false, ' small')}</div>`;
	});

	let allHeaderImgs = document.querySelectorAll('.resumed_infos div .d-flex img');
	allHeaderImgs.forEach((headerImg) => {
		headerImg.classList.add('d-none');
	});
}

async function getNewDashboardJson() {
	loadingOnAllTabs();
	const csrfmiddlewaretoken = getCookie('csrftoken');
	const rangeDate = getActiveDates();
	const date_from = rangeDate['date_from'];
	const date_to = rangeDate['date_to'];

	const settings = {
		method: 'GET',
		headers: {
			'X-CSRFToken': csrfmiddlewaretoken,
			'Content-Type': 'application/json',
		},
	};

	try {
		const response = await fetch(
			`/api/v1/get_uipath_logs/?${new URLSearchParams({
				date_from,
				date_to,
			})}`,
			settings
		);

		if (response.ok) {
			const convertedResponse = await response.json();
			const jsonHasUpdateInfos = 'update_infos' in convertedResponse;
			lastDashboardJson =
				jsonHasUpdateInfos && 'fakejson' in convertedResponse['update_infos']
					? JSON.parse(convertedResponse['update_infos']['fakejson'])
					: convertedResponse;

			if (jsonHasUpdateInfos) {
				updateNewFilters(date_from, date_to);

				if (!lastDashboardJson.dates.length && convertedResponse.dates.length) {
					lastDashboardJson.dates = { ...convertedResponse.dates };
				}
			}

			const activeTab = document.querySelector('#root .dashboard_tab.active').id;

			plotOnTab(lastDashboardJson, activeTab);
			removeAllLoading();
		} else {
			throw new Error('Problem getting data');
		}
	} catch (error) {
		Swal.fire({
			icon: 'error',
			title: translate['an_error_happened'][language],
			text: translate['we_are_having_trouble_fetching_your_data'][language],
			confirmButtonText: 'OK',
		});
	} finally {
		makeNonActiveTabsRefreshable();
		removeAllLoading();
		replaceLoadingOnFilter();
	}
}

function updateNewFilters(date_from, date_to) {
	Object.keys(lastDashboardJson['update_infos'].all_filters).map((filterType) => {
		let lastFiltersTranslated = {};
		let allFiltersChecked = ' checked';
		Array.from(
			document.querySelectorAll(
				`#filter_menu .single_filter.${filterType} input[type=checkbox]`
			)
		).forEach((input) => {
			if (input.checked) {
				lastFiltersTranslated[input.value] = ' checked';
			} else {
				lastFiltersTranslated[input.value] = '';
				allFiltersChecked = '';
			}
		});
		let allSingleFilters = '';
		if (lastDashboardJson['update_infos']['all_filters'][filterType]['inputs'].length > 0) {
			let allValues = translate['all_male'][language];
			if (filterType == 'area') {
				allValues = translate['all'][language];
			}
			if (typeof globalFilter[filterType] === 'undefined') {
				globalFilter[filterType] = [];
			}
			allSingleFilters += `
				<label for="${filterType}-1" class="single_checkbox d-flex justify-content-start align-items-center mb-0"> 
					<input type="checkbox" id="${filterType}-1" name="${filterType}" value="all_filters"${allFiltersChecked}>
					<span class="checkmark mr-1"></span>
					<p class="f-size-12 color-muted limitoneline mb-0">${allValues}</p>
				</label>
				<div class="all_single_filters">`;
		}
		lastDashboardJson['update_infos']['all_filters'][filterType]['inputs'].map(
			(singleFilter, index) => {
				let isChecked = ' checked';
				if (singleFilter in lastFiltersTranslated) {
					isChecked = lastFiltersTranslated[singleFilter];
					if (
						globalFilter[filterType].indexOf(singleFilter) === -1 &&
						isChecked == ' checked'
					) {
						globalFilter[filterType].push(singleFilter);
					}
				} else if (globalFilter[filterType].indexOf(singleFilter) === -1) {
					globalFilter[filterType].push(singleFilter);
				}
				allSingleFilters += `
				<label for="${filterType}${index}" class="single_checkbox d-flex justify-content-start align-items-center mb-0"> 
					<input type="checkbox" id="${filterType}${index}" name="${filterType}" value="${singleFilter}"${isChecked}>
					<span class="checkmark mr-1"></span>
					<p class="f-size-12 color-muted limitoneline mb-0">${singleFilter}</p>
				</label>`;
			}
		);
		if (lastDashboardJson['update_infos']['all_filters'][filterType]['inputs'].length > 0) {
			allSingleFilters += `</div>`;
		}
		document.querySelector(`#filter_menu .single_filter.${filterType} .options`).innerHTML =
			allSingleFilters;
		handleMarkedCheckboxCount(
			'',
			document.querySelector(`#filter_menu .single_filter.${filterType}`)
		);
	});
	globalFilter['date'] = getRangeDates(`${date_from} 00:00`, new Date(`${date_to} 00:00`));
	globalFilter['average_occupation'] = getAllHoursOccupation();
}

function plotOnTab(dashboardJson, tab = 'robots_tab', considerHourOnDate = false) {
	updateTabVariables(dashboardJson, considerHourOnDate);

	const rangeDate = getActiveDates();
	document.querySelectorAll('.jsDashboardTitleAndDateContainer .period').forEach((box) => {
		box.innerHTML = `${translate['between'][language]} ${formatDateToLanguage(
			rangeDate['date_from']
		)} ${translate['and'][language]} ${formatDateToLanguage(rangeDate['date_to'])}`;
	});
	if (tab == 'robots_tab') {
		updateRobotsVariables();
		plotAverageOccupationProcesses();

		plotStatusProcesses();
		plotRobotOccupancyRate();
		replaceLoadingOnFilter();

		makeRobotsBoxes();
	} else if (tab == 'roi_tab') {
		const isEmptyRoi = document.getElementById('roi_tab').classList.contains('jsNotAllowed');
		if (isEmptyRoi) {
			plotRoiProcess(null);
			plotRoiArea(null);
			plotRoiHistory(null);
			makeRoiBoxes(null);
			fireEmptyStateRoiModal();
		} else {
			updateRoiVariables();
			plotRoiProcess();
			plotRoiArea();
			plotRoiHistory();
			makeRoiBoxes();
		}

		replaceLoadingOnFilter();
	} else if (tab == 'calendar_tab') {
		calendarController.makeCalendar();
		replaceLoadingOnFilter();
	} else if (tab == 'hours_returned_tab') {
		updateReturnedHoursVariables();
		plotReturnedHoursByProcess();
		plotReturnedHoursByArea();
		plotReturnedHoursHistory();
		makeReturnedHoursBoxes();
	} else if (tab == 'rpa_tab') {
		updateRpaVariables();
		plotRpaProcess();
		plotRpaArea();
		plotRpaHistory();
		makeRpaBoxes();
	}
}

function replaceLoadingOnFilter() {
	let hasLoading = document.querySelector('#filter_menu .loading_div');
	if (hasLoading) {
		replaceWith(
			hasLoading,
			`<button type="button" class="apply_filters btn_smarthis px-4 py-2 mt-0">${translate['apply_filters'][language]}</button>`
		);
	}
}

function updateTabVariables(dashboardJson, considerHourOnDate = false) {
	allTabsVariables = resetAllTabsVariables();
	allTabsVariables['all_robots'] = dashboardJson['all_robots'];

	const monthlyHoursRPA = {};
	let previous = null;
	let numberOfRpaHoursByMonth = 0;
	let robotsByMonth = new Set();
	const totalStatus = {
		Successful: 0,
		Faulted: 0,
		Stopped: 0,
	};
	let totalNumberOfProcesses = 0;
	$.each(dashboardJson.dates, function (date, allInfosByDay) {
		let isDateOnFilter = false;
		if (globalFilter['date'] !== undefined && globalFilter['date'].length > 0) {
			if (globalFilter['date'].indexOf(date) !== -1) {
				isDateOnFilter = true;
			}
		}
		if (isDateOnFilter) {
			let hours_rpa = 0;
			let qnt_processes = 0;
			allTabsVariables['robots_bydate'][date] = {
				date: allInfosByDay['date'],
				robots: {},
			};

			$.each(allInfosByDay.processes, function (index, singleProcess) {
				let isProcessAllowed = filterHasSingleProcessInfo(singleProcess);

				if (isProcessAllowed.indexOf(false) === -1) {
					// algumas automações não vêm com ocupação do robô, então criamos uma representação "vazia" pra poder manipular logo abaixo
					let hasAverageOccupation = calculateOccupationByProcess(singleProcess, date);

					if (hasAverageOccupation) {
						// caso verdadeiro, o processo pode ser considerado para os gráficos e suas variáveis

						if (
							typeof allTabsVariables['allprocesses'][singleProcess['process']] ===
							'undefined'
						) {
							allTabsVariables['allprocesses'][singleProcess['process']] = {
								rpaHours: 0,
								humanHours: 0,
								qnt: 0,
								area: singleProcess.area,
								dates: {},
							};
						}
						// time is in seconds
						allTabsVariables['allprocesses'][singleProcess['process']]['rpaHours'] +=
							singleProcess.time;
						allTabsVariables['allprocesses'][singleProcess['process']]['humanHours'] +=
							singleProcess.human_time;
						allTabsVariables['allprocesses'][singleProcess['process']]['qnt'] +=
							singleProcess.qnt;
						if (singleProcess['status'] == 'Successful') {
							// dados uteis pra espelhamento de processos every minute futuros
							allTabsVariables['allprocesses'][singleProcess['process']]['dates'][
								allInfosByDay['date']
							] = singleProcess['averageoccupation_byday'];
						}

						if (
							typeof allTabsVariables['all_areas'][singleProcess.area] === 'undefined'
						) {
							allTabsVariables['all_areas'][singleProcess.area] = {
								name: singleProcess.area,
								hours_rpa: 0,
								hours_human: 0,
								processes: [],
							};
						}
						allTabsVariables['all_areas'][singleProcess.area]['hours_rpa'] +=
							singleProcess.time;
						allTabsVariables['all_areas'][singleProcess.area]['hours_human'] +=
							singleProcess.human_time;
						allTabsVariables['all_areas'][singleProcess.area]['processes'].push(
							singleProcess.process
						);

						totalStatus[singleProcess['status']] += singleProcess.qnt;

						dashboardController.updateVariable(
							'statusByDay',
							(oldObj) => {
								if (oldObj) {
									const copy = { ...oldObj };
									if (!copy[date])
										copy[date] = {
											Faulted: 0,
											Stopped: 0,
											Successful: 0,
										};
									copy[date][singleProcess.status] += singleProcess.qnt;
									return copy;
								} else {
									const obj = {};
									obj[date] = {
										Faulted: 0,
										Stopped: 0,
										Successful: 0,
									};
									obj[date][singleProcess.status] += singleProcess.qnt;

									return obj;
								}
							},
							singleProcess.process
						);

						totalNumberOfProcesses += singleProcess.qnt;

						if (singleProcess.human_time > 0) {
							allTabsVariables['total_hours'] += singleProcess.time;
							allTabsVariables['total_hours_human'] += singleProcess.human_time;
						}
						hours_rpa += singleProcess.time;

						numberOfRpaHoursByMonth += singleProcess.time;

						qnt_processes += singleProcess.qnt;
						if (
							typeof allTabsVariables['robots_bydate'][date]['robots'][
								singleProcess['robot']
							] === 'undefined'
						) {
							allTabsVariables['robots_bydate'][date]['robots'][
								singleProcess['robot']
							] = {
								time_in_seconds: 0,
								occupation_by_hour: $.extend(
									true,
									{},
									allTabsVariables['newAverageOccupation']
								),
							};
						}
						allTabsVariables['robots_bydate'][date]['robots'][singleProcess['robot']][
							'time_in_seconds'
						] += singleProcess.time;

						// cálculo especifico pra atualizar as horas do trabalho de cada robô
						calculateOccupationByDayForRobot(singleProcess, date);

						if (singleProcess.robot) {
							robotsByMonth.add(singleProcess.robot);
						}
					}
				}
			});

			if (Boolean(monthlyHoursRPA[allInfosByDay['date'].substring(0, 7)]) == false) {
				if (Boolean(monthlyHoursRPA[previous])) {
					const year = previous.substring(0, 4);
					// Adicionando o "-02" pois sem a data o construtor Date infere que é o dia 1 e retorna o mês anterior. Mais info: https://stackoverflow.com/questions/41432834/wrong-date-with-javascript-function-tolocaledatestring
					const month = firstLetterToUppercase(
						new Date(`${previous}-02`).toLocaleString(language, { month: 'long' })
					);
					const dateText = `${month}${language == 'pt-BR' ? ' de' : ''} ${year}`;
					const hours = (numberOfRpaHoursByMonth / 3600) >> 0;
					const mins = ((numberOfRpaHoursByMonth % 3600) / 60) >> 0;

					allTabsVariables['hoursbyday_rpa']['xMonthlyData'].push(previous);
					allTabsVariables['hoursbyday_rpa']['yMonthlyData'].push(
						Math.round((numberOfRpaHoursByMonth / 3600) * 10) / 10
					);

					allTabsVariables['hoursbyday_rpa']['monthlyTextData'].push(
						`<b style='color:#17EAAC'>${dateText}</b> <br><b>${translate['rpa_runtime'][language]} </b>: ${hours}h ${mins}min <br><b>${translate['processes'][language]}</b>: ${qnt_processes}<br><b>${translate['robots'][language]}</b>: ${robotsByMonth.size}<extra></extra>`
					);
					numberOfRpaHoursByMonth = 0;
					robotsByMonth.clear();
				}

				monthlyHoursRPA[allInfosByDay['date'].substring(0, 7)] = [];
			}
			previous = allInfosByDay['date'].substring(0, 7);

			allTabsVariables['hoursbyday_rpa']['xDailyData'].push(allInfosByDay['date']);
			// hours_rpa in seconds
			allTabsVariables['hoursbyday_rpa']['yDailyData'].push(
				Math.round((hours_rpa / 3600) * 10) / 10
			);

			const thisDay = allInfosByDay['date'].substring(8, 10);
			const thisMonth = firstLetterToUppercase(
				new Date(`${allInfosByDay['date']} 12:30`).toLocaleString(language, {
					month: 'long',
				})
			);
			const thisYear = allInfosByDay['date'].substring(0, 4);
			const dateText =
				language == 'pt-BR'
					? `${thisDay} de ${thisMonth} de ${thisYear}`
					: `${thisMonth} ${thisDay}, ${thisYear}`;

			const numberOfRobots = new Set(
				Object.keys(allTabsVariables['robots_bydate'][date]['robots'])
			).size;

			let hours = (hours_rpa / 3600) >> 0;
			let mins = ((hours_rpa % 3600) / 60) >> 0;

			allTabsVariables['hoursbyday_rpa']['textData'].push(
				`<b style='color:#17EAAC'>${dateText}</b> <br><b>${translate['rpa_runtime'][language]} </b>: ${hours}h ${mins}min <br><b>${translate['processes'][language]}</b>: ${qnt_processes}<br><b>${translate['robots'][language]}</b>: ${numberOfRobots}<extra></extra>`
			);
		}
	});

	dashboardController.setVariable('totalNumberOfProcesses', totalNumberOfProcesses);
	dashboardController.setVariable('totalStatus', totalStatus);

	setOcuppationTimeToMinutes();
	allTabsVariables['total_hours'] = Math.round(allTabsVariables['total_hours'] / 3600);
	allTabsVariables['total_hours_human'] = Math.round(allTabsVariables['total_hours_human'] / 60);
}

function resetAllTabsVariables() {
	total_hours = 0;
	total_hours_human = 0;
	allprocesses = {};
	all_areas = {};
	hoursbyday_rpa = {
		xDailyData: [],
		xMonthlyData: [],
		yDailyData: [],
		yMonthlyData: [],
		textData: [],
		monthlyTextData: [],
	};
	robots_bydate = {};
	occupationby_robot = [];
	all_robots = {};
	newAverageOccupation = {
		'12_AM': { qnt: 0, total_occupation_byhour: 0 },
		'01_AM': { qnt: 0, total_occupation_byhour: 0 },
		'02_AM': { qnt: 0, total_occupation_byhour: 0 },
		'03_AM': { qnt: 0, total_occupation_byhour: 0 },
		'04_AM': { qnt: 0, total_occupation_byhour: 0 },
		'05_AM': { qnt: 0, total_occupation_byhour: 0 },
		'06_AM': { qnt: 0, total_occupation_byhour: 0 },
		'07_AM': { qnt: 0, total_occupation_byhour: 0 },
		'08_AM': { qnt: 0, total_occupation_byhour: 0 },
		'09_AM': { qnt: 0, total_occupation_byhour: 0 },
		'10_AM': { qnt: 0, total_occupation_byhour: 0 },
		'11_AM': { qnt: 0, total_occupation_byhour: 0 },
		'12_PM': { qnt: 0, total_occupation_byhour: 0 },
		'01_PM': { qnt: 0, total_occupation_byhour: 0 },
		'02_PM': { qnt: 0, total_occupation_byhour: 0 },
		'03_PM': { qnt: 0, total_occupation_byhour: 0 },
		'04_PM': { qnt: 0, total_occupation_byhour: 0 },
		'05_PM': { qnt: 0, total_occupation_byhour: 0 },
		'06_PM': { qnt: 0, total_occupation_byhour: 0 },
		'07_PM': { qnt: 0, total_occupation_byhour: 0 },
		'08_PM': { qnt: 0, total_occupation_byhour: 0 },
		'09_PM': { qnt: 0, total_occupation_byhour: 0 },
		'10_PM': { qnt: 0, total_occupation_byhour: 0 },
		'11_PM': { qnt: 0, total_occupation_byhour: 0 },
	};
	averageoccupation_byhour = $.extend(true, {}, newAverageOccupation);

	return {
		total_hours,
		total_hours_human,
		allprocesses,
		all_areas,
		hoursbyday_rpa,
		robots_bydate,
		occupationby_robot,
		newAverageOccupation,
		averageoccupation_byhour,
		all_robots,
	};
}

function filterHasSingleProcessInfo(singleProcess) {
	let isAllowedValue = [];
	if (
		singleProcess['area'] == '' &&
		globalFilter['area'] &&
		globalFilter['area'].indexOf('') === -1 &&
		document.getElementById('area-2') === null
	) {
		// existem processos que não possuem área, ainda.. precisam ser contabilizados, logo adicionar ao globalFilter é a melhor opção
		addEmptyArea();
	}
	$.each(globalFilter, function (type, filters) {
		if (type !== 'date' && type !== 'average_occupation') {
			let exists = false;
			$.each(filters, function (i, filter) {
				if (singleProcess[type] == filter) {
					exists = true;
				}
			});
			isAllowedValue.push(exists);
		} else {
			isAllowedValue.push(true);
		}
	});
	return isAllowedValue;
}

function addEmptyArea() {
	globalFilter['area'].push('');
	let oldHtml = document.querySelector('.single_filter.area .all_single_filters').innerHTML;
	document.querySelector('.single_filter.area .all_single_filters').innerHTML = `
	<label for="area-2" class="single_checkbox d-flex justify-content-start align-items-center mb-0"> 
		<input type="checkbox" id="area-2" name="area" value="" checked="">
		<span class="checkmark mr-1"></span>
		<p class="f-size-12 color-muted limitoneline mb-0">${translate['no_department'][language]}</p>
	</label>${oldHtml}`;
	handleMarkedCheckboxCount('', document.querySelector(`#filter_menu .single_filter.area`));
}

function calculateOccupationByProcess(singleProcess, date = '') {
	if (typeof allTabsVariables['occupationby_robot'][singleProcess['robot']] === 'undefined') {
		allTabsVariables['occupationby_robot'][singleProcess['robot']] = $.extend(
			true,
			{},
			allTabsVariables['newAverageOccupation']
		);
	}
	let hasAverageOccupation = false;
	$.each(singleProcess['averageoccupation_byday'], function (hour, occupation) {
		let isAllowedAverage = false;
		if (globalFilter['average_occupation'].indexOf(hour) !== -1) {
			hasAverageOccupation = true;
			isAllowedAverage = true;
		}

		if (isAllowedAverage) {
			allTabsVariables['occupationby_robot'][singleProcess['robot']][hour]['qnt']++;
			allTabsVariables['occupationby_robot'][singleProcess['robot']][hour][
				'total_occupation_byhour'
			] += occupation['total_occupation_byhour'];
		}
	});
	return hasAverageOccupation;
}

function calculateOccupationByDayForRobot(singleProcess, date) {
	$.each(singleProcess['averageoccupation_byday'], function (hour, occupation) {
		allTabsVariables['robots_bydate'][date]['robots'][singleProcess['robot']][
			'occupation_by_hour'
		][hour]['total_occupation_byhour'] += occupation['total_occupation_byhour'];

		allTabsVariables['robots_bydate'][date]['robots'][singleProcess['robot']][
			'occupation_by_hour'
		][hour]['qnt'] += occupation['qnt'];
	});
}

function setOcuppationTimeToMinutes() {
	Object.keys(allTabsVariables['occupationby_robot']).map(function (robot) {
		Object.keys(allTabsVariables['occupationby_robot'][robot]).map(function (hour) {
			let total_occupation_byhour =
				allTabsVariables['occupationby_robot'][robot][hour]['total_occupation_byhour'] > 0
					? allTabsVariables['occupationby_robot'][robot][hour][
							'total_occupation_byhour'
					  ] /
					  60 /
					  allTabsVariables['occupationby_robot'][robot][hour]['qnt']
					: 0;
			allTabsVariables['averageoccupation_byhour'][hour]['total_occupation_byhour'] +=
				total_occupation_byhour;
			allTabsVariables['averageoccupation_byhour'][hour]['qnt']++;
		});
	});
}

/** ****************** PLOTGRAPHS ********************  */

function makePlot(elementSelector, dashboardData, config) {
	const plot = document.getElementById(elementSelector);

	const dashboardContainer = plot.closest(config.container || '.dashboard');
	const dashboardHeader = dashboardContainer.querySelector('header');
	const width = plot.offsetWidth;
	const height = dashboardContainer.offsetHeight - dashboardHeader.offsetHeight;

	const updatedLayout = { ...config.layout };

	updatedLayout.width = width;
	updatedLayout.height = height;

	Plotly.newPlot(elementSelector, dashboardData, updatedLayout);
}

/** ****************** PLOTGRAPHS ********************  */

async function newClickOnChart(
	type,
	singleFilter,
	selectedFilter,
	tab,
	getPlot = true,
	considerHourOnDate = false
) {
	let allFilters = singleFilter.querySelectorAll(`.options input`);
	if (globalFilter[type].length === 1) {
		// back to everyone
		addAllFiltersToGlobalFilter(allFilters, type);
		handleMarkedCheckboxCount('', singleFilter);
		if (getPlot) {
			plotOnTab(lastDashboardJson, tab, considerHourOnDate);
			makeNonActiveTabsRefreshable();
		}
	} else {
		// only type filters
		async function removeAllFiltersAsync(_callback) {
			removeAllFiltersFromGlobalFilter(allFilters);
		}
		async function keepOnlySelectedFilter() {
			await removeAllFiltersAsync();
			globalFilter[type].push(selectedFilter);
			allFilters.forEach((inputFilter) => {
				if (inputFilter.value == selectedFilter) {
					inputFilter.checked = true;
				}
			});
			handleMarkedCheckboxCount('', singleFilter);
			if (getPlot) {
				plotOnTab(lastDashboardJson, tab, considerHourOnDate);
				makeNonActiveTabsRefreshable();
			}
		}

		keepOnlySelectedFilter();
	}
}

function newClickOnChartWithoutCheckBox(
	type,
	filterValue = [],
	tab,
	updateSingleFilter = {},
	considerHourOnDate = false
) {
	if (globalFilter[type].length === 1) {
		if (type == 'date') {
			setRangeDatesOnGlobalFilter();
			if ('type' in updateSingleFilter) {
				let singleFilter = document.querySelector(
					`.single_filter.${updateSingleFilter['type']}`
				);
				newClickOnChart(
					updateSingleFilter['type'],
					singleFilter,
					updateSingleFilter['clickedFilter'],
					'robots_tab',
					true,
					considerHourOnDate
				);
			} else {
				plotOnTab(lastDashboardJson, tab, considerHourOnDate);
				makeNonActiveTabsRefreshable();
			}
		} else if (type == 'average_occupation') {
			globalFilter['average_occupation'] = getAllHoursOccupation();
			plotOnTab(lastDashboardJson, tab);
			makeNonActiveTabsRefreshable();
		}
	} else {
		async function removeAllFiltersAsync(_callback) {
			globalFilter[type] = [];
		}
		async function keepOnlySelectedFilter() {
			await removeAllFiltersAsync();
			globalFilter[type] = filterValue;
			if ('type' in updateSingleFilter) {
				let singleFilter = document.querySelector(
					`.single_filter.${updateSingleFilter['type']}`
				);
				newClickOnChart(
					updateSingleFilter['type'],
					singleFilter,
					updateSingleFilter['clickedFilter'],
					'robots_tab',
					true,
					considerHourOnDate
				);
			} else {
				plotOnTab(lastDashboardJson, tab);
				makeNonActiveTabsRefreshable();
			}
		}
		keepOnlySelectedFilter();
	}
}

function newClickOnChartDateHour(filterValue = [], tab, updateSingleFilter = {}) {
	if (globalFilter['date'].length === 1) {
		setRangeDatesOnGlobalFilter();
		plotOnTab(lastDashboardJson, tab, true);
		makeNonActiveTabsRefreshable();
	} else {
		let dateHour = filterValue[0].split(' ');
		globalFilter['date'] = [dateHour[0]];
		plotOnTab(lastDashboardJson, tab, true);
		makeNonActiveTabsRefreshable();
	}
}

function formatDateToLanguage(date) {
	const convertedDate = new Date(date);
	return new Intl.DateTimeFormat(language).format(convertedDate);
}

function decimalHoursToMinutes(hours) {
	if (!Number.isInteger(hours)) {
		const splittedHour = String(hours).split('.');
		const hoursPart = splittedHour[0];
		const decimalPart = splittedHour[1];
		const formattedHours = formatNumberToLanguage(hoursPart);
		const convertedToMinutes = (decimalPart / 10) * 60;

		return `${formattedHours}h ${convertedToMinutes}m`;
	} else {
		return `${formatNumberToLanguage(hours)}h`;
	}
}

function removeAllLoading() {
	let allLoaders = document.querySelectorAll('.loader');
	allLoaders.forEach((loader) => {
		loader.parentNode.remove();
	});
}

function makeNonActiveTabsRefreshable() {
	let allTabsNeedingRefresh = document.querySelectorAll(
		'#content .dashboard_tab:not(.active):not(#manage_settings_tab'
	);
	allTabsNeedingRefresh.forEach((tab) => tab.classList.add('virgin'));
}

function getLastDayOfMonth(date) {
	let weekDay = new Date(`${date} 00:00:00`);
	var lastDay = new Date(weekDay.getFullYear(), weekDay.getMonth() + 1, 0);
	let day = String(lastDay.getDate()).length == 1 ? `0${lastDay.getDate()}` : lastDay.getDate();
	let month = lastDay.getMonth() + 1;
	month = String(month).length == 1 ? `0${month}` : month;
	return { day: day, month: month, year: weekDay.getFullYear() };
}

function getLastDayOfWeekFromDay(date) {
	const weekDay = getDate(`${date} 00:00:00`);
	const daysToAdd = 7 - weekDay.getDay();
	weekDay.setDate(weekDay.getDate() + daysToAdd);
	const lastDay =
		String(weekDay.getDate()).length == 1 ? `0${weekDay.getDate()}` : weekDay.getDate();
	let lastMonth = weekDay.getMonth() + 1;
	lastMonth = String(lastMonth).length == 1 ? `0${lastMonth}` : lastMonth;
	return { day: lastDay, month: lastMonth, year: weekDay.getFullYear() };
}

function getRangeDates(startDate, stopDate) {
	let dateArray = new Array();
	let currentDate = new Date(startDate);
	while (currentDate <= stopDate) {
		let objdate = new Date(currentDate);
		let month = `${objdate.getMonth() + 1}`;
		if (month.length == 1) {
			month = `0${month}`;
		}
		let day = `${objdate.getDate()}`;
		if (day.length == 1) {
			day = `0${day}`;
		}
		dateArray.push(`${objdate.getFullYear()}_${month}_${day}`);
		currentDate = addDays(currentDate, 1);
	}
	return dateArray;
}

function getAllHoursOccupation() {
	return [
		'12_AM',
		'01_AM',
		'02_AM',
		'03_AM',
		'04_AM',
		'05_AM',
		'06_AM',
		'07_AM',
		'08_AM',
		'09_AM',
		'10_AM',
		'11_AM',
		'12_PM',
		'01_PM',
		'02_PM',
		'03_PM',
		'04_PM',
		'05_PM',
		'06_PM',
		'07_PM',
		'08_PM',
		'09_PM',
		'10_PM',
		'11_PM',
	];
}

function addDays(olddate, days) {
	let date = new Date(olddate.valueOf());
	date.setDate(date.getDate() + days);
	return date;
}

function plotTableInfoGraph(information, whichTable) {
	const infoTable = document.getElementById(whichTable['infoTable']);
	const tableBody = infoTable.querySelector('tbody');
	tableBody.innerHTML = '';

	Object.entries(information).forEach(([key, value], index) => {
		const tableRow = document.createElement('tr');
		const gainElement = document.createElement('td');
		const nameElement = document.createElement('td');

		const humanHours = value[whichTable['humanHours']];
		const rpaHours = value[whichTable['rpaHours']];
		if (humanHours !== 0 && rpaHours !== 0) {
			gainElement.innerHTML = `<strong>${
				value.gain_in_hours || Math.round(100 - (rpaHours * 100) / humanHours)
			}%</strong>`;
		} else {
			const iconSrc = tableBody.dataset.icon;
			gainElement.innerHTML = `${translate['unavailable'][language]}  <img src='${iconSrc}' alt='Info Icon'</img><span>${translate['dashboard_not_available_hover'][language]}</span>`;
			gainElement.classList.add('dashboard__hover--not-available');
		}

		nameElement.textContent = whichTable['type'] == 'areas' ? value.name : key;
		tableRow.appendChild(gainElement);
		tableRow.appendChild(nameElement);
		tableBody.appendChild(tableRow);
	});

	infoTable.classList.remove('visibility-hidden');
}

function getVerticalPlotWidth(count, width, labelsX = []) {
	if (labelsX.length > 0) {
		hasBigLabel = labelsX.some(function (word) {
			return word.length > 35;
		});
		if (hasBigLabel) {
			width = width * 2.5;
		}
	}
	switch (true) {
		case count < 10:
			return width;
		case count < 50:
			return width * 5;
		case count < 100:
			return width * 10;
		case count < 170:
			return width * 15;
		case count < 230:
			return width * 20;
		case count < 280:
			return width * 25;
		default:
			return width * 40;
	}
}

function getTextWidth(text, font = 'normal 14px Montserrat') {
	// re-use canvas object for better performance
	var canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement('canvas'));
	var context = canvas.getContext('2d');
	context.font = font;
	var metrics = context.measureText(text);
	return metrics.width;
}

function sortCoordinatesArrays(information, compareRule, whichPlot) {
	const sortable = [];
	const sortedInfo = {};
	const deepObjectCopy = JSON.parse(JSON.stringify(information));
	let objKey;

	if (whichPlot == 'roiProcess' || whichPlot == 'roiArea') {
		for (item in deepObjectCopy) {
			deepObjectCopy[item][objKey];
			sortable.push([item, deepObjectCopy[item]]);
		}
		if (compareRule === 'roi_smaller') {
			sortable.sort((a, b) => a[1]['roi'] - b[1]['roi']);
		} else {
			sortable.sort((a, b) => b[1]['roi'] - a[1]['roi']);
		}

		sortable.forEach((item) => (sortedInfo[item[0]] = item[1]));
	} else {
		for (item in deepObjectCopy) {
			if (whichPlot == 'allProcesses') {
				deepObjectCopy[item]['rpaHours'] =
					Math.round((deepObjectCopy[item]['rpaHours'] / 3600) * 10) / 10;
				deepObjectCopy[item]['humanHours'] =
					Math.round((deepObjectCopy[item]['humanHours'] / 60) * 10) / 10;
			}

			if (compareRule == 'returnInHours') {
				const humanHours =
					deepObjectCopy[item][
						whichPlot == 'allProcesses' ? 'humanHours' : 'hours_human'
					];
				const rpaHours =
					deepObjectCopy[item][whichPlot == 'allProcesses' ? 'rpaHours' : 'hours_rpa'];

				if (humanHours != 0 && rpaHours != 0) {
					deepObjectCopy[item]['gain_in_hours'] = Math.round(
						100 - (rpaHours * 100) / humanHours
					);
				} else {
					deepObjectCopy[item]['gain_in_hours'] = 0;
				}
			}
			sortable.push([item, deepObjectCopy[item]]);
		}

		if (compareRule == 'operatorHours') {
			objKey = whichPlot == 'allProcesses' ? 'humanHours' : 'hours_human';
		} else if (compareRule == 'rpaHours') {
			objKey = whichPlot == 'allProcesses' ? 'rpaHours' : 'hours_rpa';
		}

		if (compareRule == 'returnInHours') {
			sortable.sort((a, b) => b[1]['gain_in_hours'] - a[1]['gain_in_hours']);
		} else {
			sortable.sort((a, b) => b[1][objKey] - a[1][objKey]);
		}
		sortable.forEach((item) => (sortedInfo[item[0]] = item[1]));
	}

	return sortedInfo;
}

function getActiveDates() {
	let date_from = getDateFormat(document.querySelector('#filter_menu .from_datetime').value);
	let date_to = getDateFormat(document.querySelector('#filter_menu .to_datetime').value);
	if (
		document
			.querySelector('#filter_menu .custom_period.active')
			.classList.contains('set_interval')
	) {
		let rangeDate = updateDates({
			target: document.querySelector('#filter_menu .custom_period.active '),
		});
		date_from = rangeDate['date_from'];
		date_to = rangeDate['date_to'];
	}
	return { date_from, date_to };
}

function getDateFormat(dateString, needReverse = false) {
	let dateSplitted = dateString.split('/');
	let day = dateSplitted[0];
	let month = dateSplitted[1];
	let year = dateSplitted[2];
	if (dateSplitted.length < 2) {
		dateSplitted = dateString.split('-');
		day = dateSplitted[0];
		month = dateSplitted[1];
		year = dateSplitted[2];
	}

	return !needReverse ? `${year}-${month}-${day}` : `${day}-${month}-${year}`;
}

function updateDates(e) {
	let now = new Date();
	date_to = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
	now.setDate(now.getDate() - e.target.value);
	date_from = `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
	return { date_from, date_to };
}

function firstLetterToUppercase(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

async function downloadPlot(event) {
	// called from boostrap modal
	const targetButton = event.relatedTarget;
	const container = targetButton.closest('.dashboard');
	replaceWith(targetButton, getLoadingDiv(true, 'small'));
	const loading = document.querySelector('.loading_div');
	const targetPlot = container.querySelector('.js-plotly-plot');
	const targetPlotContent = container.querySelector('.scroll');
	const targetPlotHeading = container.querySelector('header');
	const targetPlotHeadingText = targetPlotHeading.querySelector('h5').textContent;
	const extraContent = container.querySelector('.js-extra-content');
	const isSpecialWidthPlot = targetPlot.classList.contains('canvas-special');

	container.style.height = `${
		(targetPlotHeading.offsetHeight + targetPlotContent.scrollHeight) * 1.2
	}px`;
	container.style.maxHeight = '1000rem';
	targetPlotContent.classList.remove('scroll');

	const containerHeightWithoutUnit = Number(
		container.style.height.replace(new RegExp('[a-z]', 'g'), '')
	);

	const plotCanvas = await html2canvas(container, {
		scrollX: -window.scrollX,
		scrollY: -window.scrollY,
		windowWidth: isSpecialWidthPlot
			? document.documentElement.offsetWidth
			: targetPlot.scrollWidth,
		windowHeight: document.documentElement.offsetHeight,
		width: targetPlot.scrollWidth,
		height: containerHeightWithoutUnit,
		logging: document.getElementById('is-prod-environment').value != 'True',
	});

	const plotFilename = getFileName('plot', targetPlotHeadingText);

	saveAs(plotCanvas.toDataURL('image/png'), plotFilename);

	container.style.height = '';
	container.style.maxHeight = '';
	targetPlotContent.classList.add('scroll');

	if (extraContent) {
		const extraContentHeading =
			extraContent.querySelector('th')?.textContent.toLowerCase() ||
			extraContent.dataset.heading;

		if (extraContent.tagName.toLowerCase() === 'table') {
			const tableBody = extraContent.querySelector('tbody');
			tableBody.style.height = 'auto';
		}

		const extraContentCanvas = await html2canvas(extraContent, {
			scrollX: -window.scrollX,
			scrollY: -window.scrollY,
			windowWidth: document.documentElement.offsetWidth,
			windowHeight: extraContent.scrollHeight,
			width: extraContent.offsetWidth,
			height: extraContent.scrollHeight,
			logging: document.getElementById('is-prod-environment').value != 'True',
		});

		if (extraContent.tagName.toLowerCase() === 'table') {
			const tableBody = extraContent.querySelector('tbody');
			tableBody.style.height = '';
		}
		const extraContentFilename = getFileName(
			'extraContent',
			targetPlotHeadingText,
			extraContentHeading
		);
		saveAs(extraContentCanvas.toDataURL('image/png'), extraContentFilename);
	}
	replaceWith(loading, targetButton.outerHTML);

	$(event.target).modal('hide');

	function getFileName(type, plotHeading, extraContentHeading) {
		const now = new Date(Date.now());
		const formattedNow = now
			.toLocaleString(language, {
				year: 'numeric',
				month: 'numeric',
				day: 'numeric',
			})
			.replaceAll('/', '-');

		if (type == 'plot') {
			return `${plotHeading}_${formattedNow}`;
		} else {
			return `${translate['table'][language]}_${extraContentHeading}_${plotHeading}_${formattedNow}`;
		}
	}
}

function saveAs(uri, filename) {
	const link = document.createElement('a');

	if (typeof link.download === 'string') {
		link.href = uri;
		link.download = filename;

		//Firefox requires the link to be in the body
		document.body.appendChild(link);

		//simulate click
		link.click();

		//remove the link when done
		document.body.removeChild(link);
	} else {
		window.open(uri);
	}
}

const scrollDownPlot = (element) => {
	element.scrollTo(0, 10000);
};

function monthCounter() {
	let currentMonth = 0;

	return (dateOrDateObj) => {
		const date = typeof dateOrDateObj === 'string' ? dateOrDateObj : dateOrDateObj.date;
		const month = getDate(date).getMonth() + 1;
		if (month > currentMonth || (month === 1 && currentMonth === 12)) {
			currentMonth = month;
			return true;
		} else {
			return false;
		}
	};
}

function getDate(date) {
	return new Date(new Date(date).setDate(new Date(date).getDate() + 1));
}
