document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', bindCrewPopupClick);

	function bindCrewPopupClick(event) {
		if (
			event.target.classList.contains('crew__popup-menu--icon') &&
			event.target.closest('#manage_areas_tab')
		) {
			handleCrewPopupMenu(event);
		}
	}

	function handleCrewPopupMenu(event) {
		const targetMenu = event.target;
		const targetPopup = targetMenu.parentNode.querySelector('.crew__popup-menu-container');
		const allPopups = Array.from(document.querySelectorAll('.crew__popup-menu-container'));

		allPopups.forEach((popup) => popup.classList.remove('crew__popup-menu-container--show'));
		targetPopup.classList.toggle('crew__popup-menu-container--show');
	}

	$('#root').on('submit', '#new_area_modal form', handleNewAreaSubmit);
	$('#root').on('submit', '#remove_area_modal form', handleRemoveAreaSubmit);
	$('#root').on('submit', '#edit_area_modal form', handleEditAreaSubmit);

	// Remove area
	$('#root').on('click', '.btn-remove-area', function (e) {
		let $this = $(this);
		table_colum = $this.closest('tr').find('th:first-child');

		let table_value = table_colum.html();
		$('#remove_area_modal .confirm_exclude_area').data('id', table_colum.data('area_id'));
		$('#remove_area .text_span-area').html(table_value);
	});

	// Editar area
	$('#root').on('click', '.btn-edit-area', function (e) {
		let $this = $(this);

		table_colum = $this.closest('tr').find('th:first-child');
		let table_value = table_colum.html();

		$('#edit_area_modal .btn__submit-area-edit').data('id', table_colum.data('area_id'));
		$('#edit_area input').val(table_value);
		const editAreaInput = document.querySelector('#edit_area input');
		if (editAreaInput) editAreaInput.dataset.old = table_value;
	});

	$('#root').on('click', '.button__register-area', function (e) {
		let table_value = $('#new_area_modal form input');
		document.querySelector('.modal__area-register input').dataset.old = table_value;
	});

	function handleNewAreaSubmit(event) {
		event.preventDefault();
		let $this = $(this);
		let rangeDate = getActiveDates();
		let date_from = rangeDate['date_from'];
		let date_to = rangeDate['date_to'];
		if ($this.find('input[name=area]').val().length > 0) {
			Swal.fire({
				title: translate['please_wait_p'][language],
				html: `<div class="d-flex justify-content-center align-items-center my-5">${getLoadingDiv()}</div>`,
				showConfirmButton: false,
			});
			$.post(
				'/new/area',
				`${$this.serialize()}&date_to=${date_to}&date_from=${date_from}`,
				function callbackPostRequest(data) {
					if (data.status === 'sucesso') {
						if ($this.find('input[name=area]').val().length > 0) {
							$('#manage_areas_tab .manage_areas_table').removeClass('d-none');
							$('#manage_areas_tab .include_empty_area').addClass('d-none');
						}
						addRowToTable();
						$('#new_area_modal').modal('hide');
						$('.modal-backdrop').remove();
						Swal.fire({
							title: `<strong class="f-size-18 success-register_area color000000">${translate['area_successfully_registered'][language]}</strong>`,
							html:
								`<div class="sub-text_swal color000000"><p class="f-size-16">${
									translate['you_can_now_associate_processes_to_area'][language]
								}<strong> ${$this.find('input[name=area]').val()}</strong> ${
									translate['in'][language]
								} <strong style="font-style: italic;">${
									translate['settings'][language]
								} > ${translate['processes'][language]}.</strong> </p></div>` +
								'<div class="d-flex link_area-process"><button type="button" class="btn_modal_link-area" ><a class="no__link" href="#">Ir para Processos</a></button></div>' +
								'<div class="position_img-check"><img class="img_check-area" src=static/dashboard/img/logo-check.png ></div>',
							customClass: 'swal2-popup swal-wide-area',
							showConfirmButton: false,
							showCloseButton: true,
							showCancelButton: true,
							cancelButtonText: 'Fechar',
							closeButtonHtml: '<span class="dark-gray__color">&times;</span>',
							buttonsStyling: true,
							cancelButtonClass: 'btn_link-area_cancel',
						});
						$this.find('input[name=area]').val('');
						document
							.querySelector('.btn_modal_link-area')
							.addEventListener('click', goToProcesseTabAfterCreatingArea);
						/*******/
						function addRowToTable() {
							$('#manage_areas_tab tbody').prepend(`<tr class='backgroundF8F8F8'>
							<th scope="row"  data-area_id="${data.id}">${$this.find('input[name=area]').val()}</th>
							<th scope="row" class="row_process"> 
							<div class="box__process-table-text"><p class=" f-size-12 text-process_table">0 Processos</p></div>
							<div class="d-flex gap-16 manage__areas-container">
							<div class="crew__popup-menu popup-menu__areas">
							<div class="crew__popup-menu-container crew__popup-menu-container--areas">
							<span class="btn btn-edit btn-edit-area" data-toggle="modal" data-target="#edit_area_modal">Editar </span>
							<span class="btn btn-remove btn-remove-area" data-toggle="modal" data-target="#remove_area_modal">Excluir</span></div>
							<img src="/static/dashboard/img/three-dots.svg" alt="Three dots to show more info" class="c-pointer opacity-hover px-2 crew__popup-menu--icon">
							</div>
							</div> </tr>`);
						}
					} else {
						Swal.fire('Oops..', data.msg, 'error');
					}
				}
			);
		} else {
			Swal.fire('Oops..', translate['fill_name_department'][language], 'warning');
		}
	}

	function handleRemoveAreaSubmit(event) {
		event.preventDefault();
		let $this = $(this);
		let area_id = $('#remove_area_modal .confirm_exclude_area').data('id');
		let rangeDate = getActiveDates();
		let date_from = rangeDate['date_from'];
		let date_to = rangeDate['date_to'];
		if ($this.find('span[name=area]').html().length > 0) {
			Swal.fire({
				title: translate['please_wait_p'][language],
				willOpen: () => {
					Swal.showLoading();
				},
			});
			$.post(
				`/remove/area/${area_id}`,
				`${$this.serialize()}&date_to=${date_to}&date_from=${date_from}`,
				function callbackPostRequest(data) {
					if (data.status === 'sucesso') {
						$(`#manage_areas_tab tr th[data-area_id=${area_id}]`)
							.closest('tr')
							.remove();
						if ($('.manage_areas_table tbody tr').val('tr').length == 0) {
							$('.include_empty_area').prepend().removeClass('d-none');
							$('#manage_areas_tab .manage_areas_table').addClass('d-none');
						}
						$('#remove_area_modal').modal('hide');
						$('.modal-backdrop').remove();
						Swal.fire(
							translate['success'][language],
							translate['department_removed_successfully'][language],
							'success'
						);
					} else {
						Swal.fire('Oops..', data.msg, 'error');
					}
				}
			);
		} else {
			Swal.fire('Oops..', translate['fill_name_department'][language], 'warning');
		}
	}

	function handleEditAreaSubmit(event) {
		event.preventDefault();
		let $this = $(this);
		let area_id = $('#edit_area_modal .btn__submit-area-edit').data('id');
		let rangeDate = getActiveDates();
		let date_from = rangeDate['date_from'];
		let date_to = rangeDate['date_to'];
		if ($this.find('input[name=area]').val().length > 0) {
			Swal.fire({
				title: `${translate['please_wait'][language]}..`,
				willOpen: () => {
					Swal.showLoading();
				},
			});

			$.post(
				`/edit/area/${area_id}`,
				`${$this.serialize()}&date_to=${date_to}&date_from=${date_from}`,
				function callbackPostRequest(data) {
					if (data.status === 'sucesso') {
						$(`th[data-area_id=${data.id}]`).html(data.area);
						$('#edit_area_modal').modal('hide');
						$('.modal-backdrop').remove();
						Swal.fire(
							translate['success'][language],
							translate['department_saved_successfully'][language],
							'success'
						);
					} else {
						Swal.fire('Oops..', data.msg, 'error');
					}
				}
			);
		} else {
			Swal.fire('Oops..', translate['fill_name_department'][language], 'warning');
		}
	}

	function goToProcesseTabAfterCreatingArea() {
		const button = document.querySelector('.btn_modal_link-area');
		replaceWith(button, getLoadingDiv());
		getProcess()
			.done(() => Swal.close())
			.then(updateJsAfterContentIsShown);
	}
});
