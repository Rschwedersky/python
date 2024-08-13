let invitedUsers = [];
let excludedUsers = {};
document.addEventListener('DOMContentLoaded', () => {
	loadInvitedUsers();

	const csrftoken = getCookie('csrftoken');

	const emailInviteForm = document.querySelector('.invite_form input[type=email]');
	const inviteForm = document.querySelector('.invite_form');

	emailInviteForm.addEventListener('keyup', handleInviteInputKeyup);
	inviteForm.addEventListener('submit', handleInviteUser);
	document.addEventListener('click', handleDocumentOutsideClick);
	document.addEventListener('click', handleBindedClicks);

	function handleInviteInputKeyup(e) {
		shouldDisabledInviteBtn(e.currentTarget.value);
	}

	async function handleInviteUser(e) {
		e.preventDefault();
		const formElement = e.currentTarget;
		let email_input = formElement.querySelector('input[type=email]');
		if (isUserAdded(email_input.value)) {
			Swal.fire('Oops..', translate['this_user_has_already_been_added'][language], 'warning');
		} else {
			const settings = {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrftoken,
				},
				body: JSON.stringify({
					email: email_input.value,
				}),
			};

			const response = await fetch('/get/user', settings);
			const responseJson = await response.json();
			if (responseJson.status == 200) {
				handleUserInvited(responseJson);
				document.querySelector('.invite__modal-footer .btn__submit').disabled = false;
			} else {
				Swal.fire('Oops..', responseJson.msg, 'warning');
			}

			function handleUserInvited(responseJson) {
				const dashboardViewExample = document.getElementById('clone_view_type');
				const copyDashboardView = dashboardViewExample.firstElementChild;
				let cloneDashboardView = copyDashboardView.cloneNode(true);
				cloneDashboardView.dataset.user = responseJson.id;
				cloneDashboardView.querySelector('.topinfo_checkbox').innerHTML = responseJson.name;
				cloneDashboardView.querySelector('.bottominfo_checkbox').innerHTML =
					email_input.value;
				cloneDashboardView.querySelector(
					'.border__circle.border__circle--permissions'
				).innerHTML = responseJson.initials;

				let singleTypeElement = '';
				let chosenType = formElement
					.querySelector('.view_header .chosen_text')
					.innerHTML.trim();
				cloneDashboardView
					.querySelectorAll('.single_type__info--title')
					.forEach((single_type) => {
						if (single_type.innerHTML.trim() == chosenType) {
							singleTypeElement = single_type.closest('.single_type');
						}
					});
				handleChooseInviteType(singleTypeElement);

				document
					.querySelector('.dashboard_invite_modal .permissions__modal-email--list')
					.appendChild(cloneDashboardView);
				email_input.value = '';
				shouldDisabledInviteBtn(email_input.value);
			}
		}
	}

	function handleDocumentOutsideClick(e) {
		const openedInvite = document.querySelector('.dashboard_view_type.open');
		if (
			!e.target.classList.contains('dashboard_view_type') &&
			!e.target.closest('.dashboard_view_type') &&
			openedInvite
		) {
			closeInviteViewType(openedInvite);
		}
	}

	function handleBindedClicks(e) {
		const isExcludeClick =
			(e.target.classList.contains('exclude') &&
				e.target.classList.contains('single_type')) ||
			e.target.closest('.exclude');
		const isInviteViewOpen =
			e.target.closest('.dashboard_view_type .view_header') ||
			e.target.classList.contains('.view_header');
		const isChooseInvite = e.target.closest('.single_type');

		if (isExcludeClick) {
			let liElement = e.target.closest('.permissions__modal-email--item');
			excludedUsers[liElement.querySelector('.bottominfo_checkbox').innerHTML.trim()] =
				liElement.dataset.user;
			liElement.remove();
			document.querySelector('.invite__modal-footer .btn__submit').disabled =
				!canSaveInvites();
		} else if (isChooseInvite) {
			handleChooseInviteType(e.target.closest('.single_type'));
		} else if (isInviteViewOpen) {
			const chosenInviteClickable = e.target.classList.contains('.view_header')
				? e.target.classList.contains('.view_header')
				: e.target.closest('.dashboard_view_type .view_header');
			document.querySelector('.dashboard_view_type.open')?.classList.remove('open');
			handleClickChosenInvite(chosenInviteClickable);
		} else if (
			e.target.classList.contains('btn__submit') &&
			e.target.closest('.invite__modal-footer')
		) {
			submitInviteGroup();
		}
	}

	function handleClickChosenInvite(chosenInviteClickable) {
		const chosenInvite = chosenInviteClickable.closest('.dashboard_view_type');
		if (chosenInvite.classList.contains('open')) {
			closeInviteViewType(chosenInvite);
		} else {
			chosenInvite.classList.add('open');
		}
	}

	function handleChooseInviteType(single_type) {
		const inviteViewType = single_type.closest('.dashboard_view_type');
		if (!single_type.classList.contains('exclude')) {
			single_type
				.closest('.dashboard_view_type')
				.querySelector('.single_type.active')
				.classList.remove('active');
			single_type.classList.add('active');
			const chosenTypeString = single_type.querySelector(
				'.single_type__info--title'
			).innerHTML;
			inviteViewType.querySelector('.view_header span').innerHTML = chosenTypeString;
			inviteViewType.querySelector('input[name=invite_type]').value =
				chosenTypeString.toLowerCase();
		} else {
		}
		closeInviteViewType(inviteViewType);
	}

	function closeInviteViewType(inviteViewType) {
		inviteViewType.classList.remove('open');
	}

	async function submitInviteGroup() {
		let data = {};
		let allEmailAdded = [];
		document.querySelectorAll('.permissions__modal-email--item').forEach((liElement) => {
			allEmailAdded.push(liElement.querySelector('.bottominfo_checkbox').innerHTML.trim());
			data[liElement.dataset.user] = liElement.querySelector(
				'.dashboard_view_type input[name=invite_type]'
			).value;
		});
		let deleted_group = [];
		invitedUsers.map((email) => {
			if (allEmailAdded.indexOf(email) === -1) {
				deleted_group.push(excludedUsers[email]);
			}
		});

		const submitBtn = document.querySelector('.invite__modal-footer .btn__submit');
		replaceWith(
			submitBtn,
			getLoadingDiv(true, 'medium', '', `width:${submitBtn.offsetWidth}px`)
		);

		const settings = {
			method: 'POST',
			headers: {
				'X-CSRFToken': csrftoken,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ invite_group: data, deleted_group }),
		};
		const response = await fetch('/dashboard/post/invite-group', settings);
		const responseJson = await response.json();

		replaceWith(document.querySelector('.loading_div'), submitBtn.outerHTML);
		if (responseJson.status == 200) {
			Swal.fire({
				icon: 'success',
				title: translate['success'][language],
				text: translate['invite_group_updated_successfuly'][language],
				confirmButtonText: 'OK',
			}).then(() => {
				closeInviteModal();
				document.querySelector('.invite__modal-footer .btn__submit').disabled = true;
				loadInvitedUsers();
			});
		} else {
			Swal.fire('Oops..', responseJson.msg, 'error');
		}
	}

	function shouldDisabledInviteBtn(email) {
		document.querySelector('.invite_form .btn__submit').disabled = !validateEmail(email);
	}

	function validateEmail(email) {
		const re =
			/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		return re.test(String(email).toLowerCase());
	}

	function isUserAdded(email) {
		let isAlreadyAdded = false;
		document
			.querySelectorAll('.permissions__modal-email--list .bottominfo_checkbox')
			.forEach((singleEmail) => {
				if (singleEmail.innerHTML.trim() == email) {
					isAlreadyAdded = true;
				}
			});
		return isAlreadyAdded;
	}

	function loadInvitedUsers() {
		invitedUsers = [];
		document
			.querySelectorAll(
				'.dashboard_invite_modal .permissions__modal-email--item .bottominfo_checkbox'
			)
			.forEach((email) => {
				invitedUsers.push(email.innerHTML.trim());
			});
	}

	function canSaveInvites() {
		let canSave = false;
		const allEmails = document.querySelectorAll(
			'.dashboard_invite_modal .permissions__modal-email--item .bottominfo_checkbox'
		);

		if (allEmails.length != invitedUsers.length) {
			return true;
		}

		allEmails.forEach((email) => {
			if (invitedUsers.indexOf(email.innerHTML.trim()) === -1) {
				canSave = true;
			}
		});
		return canSave;
	}

	function closeInviteModal() {
		const targetBtn = document.querySelector('.dashboard_invite_modal .modal__close');
		const targetModal = document.querySelectorAll(targetBtn.dataset.close);

		document.querySelector('html').style.overflow = '';
		targetModal.forEach((modal) => (modal.style.display = ''));
	}
});
