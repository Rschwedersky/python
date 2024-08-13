document.addEventListener('DOMContentLoaded', createPlots);
document.addEventListener('filterApplied', createPlots);

const controller = (function () {
	const privateProperties = {
		currentAppliedDates: [],
		allDates: [],
		allData: [],
		currentAppliedData: [],
	};

	const getCurrentDates = () => privateProperties.currentAppliedDates;
	const setCurrentDates = (value) => (privateProperties.currentAppliedDates = value);

	const getAllDates = () => privateProperties.allDates;
	const setAllDates = (value) => (privateProperties.allDates = value);

	const getCurrentData = () => privateProperties.currentAppliedData;
	const setCurrentData = (value) => (privateProperties.currentAppliedData = value);
	const getAllData = () => privateProperties.allData;
	const setAllData = (value) => (privateProperties.allData = value);

	return {
		getCurrentDates,
		setCurrentDates,
		getAllDates,
		setAllDates,
		getCurrentData,
		setCurrentData,
		getAllData,
		setAllData,
	};
})();

function createPlots(event) {
	// const dadosReais = JSON.parse(document.getElementById('json-tasks').textContent);

	const jsonEl = document.getElementById('json-tasks');

	let tasks;
	if (jsonEl) {
		tasks = JSON.parse(jsonEl.textContent);
		document.getElementById('json-tasks').remove();
	} else {
		tasks = {};
	}
	const isDataTask = {};
	const successfulTasks = { axisX: [], axisY: [] };
	const applicationErrorTasks = { axisX: [], axisY: [] };
	const businessErrorTasks = { axisX: [], axisY: [] };
	const data = event.detail || tasks.data.tasks;

	let qntTotal = 0;

	updateData(data);
	plotStatusAutomation();
	plotBarraAutomation();
	boxResumedInfos();

	function getTaskNumber(statusString) {
		const statusInLowerCase = statusString.toLowerCase();
		if (statusInLowerCase == 'success') {
			return 1;
		} else if (statusInLowerCase == 'application_error') {
			return 2;
		} else if (statusInLowerCase == 'businnes_error') {
			return 3;
		}
	}

	function updateData(data) {
		const dates = new Set();

		Object.entries(data).map(([key, value]) => {
			qntTotal += value.length;
			return value.map((item) => {
				if (!isDataTask[key]) {
					isDataTask[key] = [];
				}
				const taskNumber = getTaskNumber(item.task_status);
				if (item.task_status.toLowerCase() == 'success') {
					successfulTasks.axisX.push(key);
					successfulTasks.axisY.push(taskNumber);
				} else if (item.task_status.toLowerCase() == 'application_error') {
					applicationErrorTasks.axisX.push(key);
					applicationErrorTasks.axisY.push(taskNumber);
				} else if (item.task_status.toLowerCase() == 'businnes_error') {
					businessErrorTasks.axisX.push(key);
					businessErrorTasks.axisY.push(taskNumber);
				} else {
					return false;
				}

				isDataTask[key].push(item.task_status);
				dates.add(key);

				return item.task_status;
			});
		});
		controller.setCurrentDates(dates);
		controller.setCurrentData(data);

		if (tasks.data?.tasks) {
			controller.setAllDates(dates);
			controller.setAllData(tasks.data.tasks);
		}
	}

	function boxResumedInfos() {
		// 	/**********************  CODE INFOS  ********************************/
		document.querySelectorAll('.resumed_infos .execution').forEach((box) => {
			box.querySelector('div .info').innerHTML = `${formatNumberToLanguage(qntTotal)}`;
			box.querySelector('div img').classList.remove('d-none');
			box.classList.add('light-bold');
		});

		document.querySelectorAll('.resumed_infos .sucess').forEach((box) => {
			box.querySelector('div .info').innerHTML = `${formatNumberToLanguage(
				percentageSuccess
			)}%`;
			box.querySelector('div img').classList.remove('d-none');
			box.classList.add('light-bold');
		});
	}

	function plotStatusAutomation() {
		const statusPlotId = 'bystatus_automation';
		const infosToAdd = [
			{
				qnt: successfulTasks,
				text: 'sucesso',
				hover: 'Indica sucesso na execução do seu modelo',
			},
			{
				qnt: applicationErrorTasks,
				text: 'erro aplicação',
				hover: 'Indica que algo deu errado na automação responsável pela execução do seu modelo. ',
			},
			{
				qnt: businessErrorTasks,
				text: 'erro negócio',
				hover: 'Indica erros externos, como informações inválidas no modelo em questão, ou que site consultado sofreu alterações.',
			},
		];

		percentageSuccess = Number(((successfulTasks.axisY.length / qntTotal) * 100).toFixed(1));
		infosToAdd[0]['qnt'] = successfulTasks.axisY.length;
		infosToAdd[1]['qnt'] = applicationErrorTasks.axisY.length;
		infosToAdd[2]['qnt'] = businessErrorTasks.axisY.length;

		document.querySelector(`#${statusPlotId} .half_donut_infos .percentage strong`).innerHTML =
			percentageSuccess ? `${formatNumberToLanguage(percentageSuccess)}%` : '-';

		let finalHtml = ``;
		infosToAdd.map((item) => {
			finalHtml += `
		<div class="dashboard_small_box_info">
			<b class="f-size-22">${formatNumberToLanguage(item.qnt)}</b>
			<p class="f-size-16 ">${item.text}
				<a class="c-pointer hasTooltip hover_dash f-size-12" >
					<img src="/static/img/info-circle.png" alt="info"> 
					<span>${item.hover}</span>
				</a> 
			</p>
			
		</div>
	`;
		});
		document.querySelector(`#${statusPlotId} .infos_content`).innerHTML = finalHtml;
		document.querySelector(`#${statusPlotId} .status_infos p b`).innerHTML =
			formatNumberToLanguage(qntTotal);
		document.documentElement.style.setProperty(
			'--status-circle-progress',
			`${180 - 180 * (percentageSuccess / 100)}deg`
		);
	}

	function plotBarraAutomation() {
		const plot = document.getElementById('resize_plotly');
		const width = plot.offsetWidth < 1245 ? plot.offsetWidth / 2.7 : plot.offsetWidth / 2.3;

		const traceSucess = {
			x: successfulTasks.axisX,
			y: successfulTasks.axisY,
			type: 'bar',
			name: 'Sucesso',
			marker: {
				color: '#17eaac',
			},
			hovertemplate: '<i>sucesso</i>' + '<br><b>Data</b>: %{x}<br>',
		};

		const traceApplicationError = {
			x: applicationErrorTasks.axisX,
			y: applicationErrorTasks.axisY,
			type: 'bar',
			name: 'Erro de aplicação',
			marker: {
				color: '#11067a',
			},
			hovertemplate: '<i>erro aplicação</i>' + '<br><b>Data</b>: %{x}<br>',
		};

		const traceBusinessError = {
			x: businessErrorTasks.axisX,
			y: businessErrorTasks.axisY,
			type: 'bar',
			name: 'Erro de negócio',
			marker: {
				color: 'rgb(204,204,204)',
			},
			hovertemplate: '<i>erro negócio</i>' + '<br><b>Data</b>: %{x}<br>',
		};

		const data = [traceSucess, traceApplicationError, traceBusinessError];

		const selectorOptions = {
			buttons: [
				{
					step: 'all',
					label: translate['general'][language],
				},
				{
					step: 'month',
					stepmode: 'todate',
					count: 1,
					label: translate['last_month'][language],
				},
				{
					step: 'year',
					stepmode: 'backward',
					count: 1,
					label: translate['last_year'][language],
				},
			],
			showactive: true,

			xanchor: 'left',
			x: 0.3,
			y: 1.0,
			active: 1,
			font: {
				family: 'Montserrat',
				size: 13,
				color: '#3424C4',
			},
			bgcolor: '#ffffff',
			bordercolor: '#3424C4',
			borderwidth: 0.2,
		};
		const margin = {
			t: 130,
			b: 100,
			r: 15,
			l: 60,
		};
		const layout = {
			margin,
			title: {
				xanchor: 'center',
				x: 0.5,
				y: 0.95,
				text: translate['execution_history'][language],
				font: {
					family: 'Montserrat',
					size: 26,
				},
			},

			xaxis: {
				tickangle: -45,
				autorange: true,
				range: 'auto',
				rangeselector: selectorOptions,
				type: 'date',
				tickfont: {
					family: 'Montserrat',
					size: 12,
					color: '#000000',
				},
			},
			yaxis: {
				autorange: true,
				range: 'auto',
				type: 'bar',
				tickfont: {
					family: 'Montserrat',
					size: 12,
					color: '#000000',
				},
			},
			showlegend: true,
			legend: {
				orientation: 'h',
				xanchor: 'left',
				yanchor: 'top',
				y: 1.35,
				side: 'v',

				font: {
					family: 'Montserrat',
					size: 14,
					color: '#000',
				},
			},
			barmode: 'stack',
			autosize: false,
		};
		const config = { displayModeBar: false };
		const updatedLayout = { ...layout };
		updatedLayout.width = width;
		updatedLayout.height = 400;
		Plotly.newPlot('bybarras_automation', data, updatedLayout, config);
	}
}
