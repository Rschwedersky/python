let language = 'pt-BR';
document.addEventListener(
	'DOMContentLoaded',
	() => (language = document.querySelector('html').getAttribute('lang'))
);

const translate = {
	a_selected_item: {
		'pt-BR': 'Um item selecionado',
		en: 'A selected item',
		es: 'Un elemento seleccionado',
	},
	some_selected_items: {
		'pt-BR': 'Alguns itens selecionados',
		en: 'Some selected items',
		es: 'Algunos artículos seleccionados',
	},
	all_male: {
		'pt-BR': 'Todos',
		en: 'All',
		es: 'Todo',
	},
	all: {
		'pt-BR': 'Todas',
		en: 'All',
		es: 'Todo',
	},
	process_quantity: {
		'pt-BR': 'Quantidade de processos',
		en: 'Process quantity',
		es: 'Cantidad de procesos',
	},
	total_hours: {
		'pt-BR': 'Total de horas',
		en: 'Total hours',
		es: 'Total de horas',
	},
	rpa: {
		'pt-BR': 'RPA',
		en: 'RPA',
		es: 'RPA',
	},
	employee: {
		'pt-BR': 'Colaborador',
		en: 'Employee',
		es: 'colaborador',
	},
	human: {
		'pt-BR': 'Humano',
		en: 'Human',
		es: 'Humano',
	},
	state: {
		'pt-BR': 'State',
		en: 'State',
		es: 'Expresar',
	},
	process_by_status: {
		'pt-BR': 'Processo por Status',
		en: 'Process by Status',
		es: 'Proceso de estado',
	},
	date: {
		'pt-BR': 'Data',
		en: 'Date',
		es: 'Fecha',
	},
	robot: {
		'pt-BR': 'Robô',
		en: 'Robot',
		es: 'Robot',
	},
	occupancy_rate: {
		'pt-BR': 'Taxa de ocupação',
		en: 'Occupancy rate',
		es: 'Tasa de ocupación',
	},
	drag_the_file_or_click_the_upload_button: {
		'pt-BR': 'Arraste o arquivo ou clique no botão para fazer upload',
		en: 'Drag the file or click the upload button',
		es: 'Arrastre el archivo o haga clic en el botón para cargar',
	},
	file_upload_completed: {
		'pt-BR': 'Upload de arquivo finalizado:',
		en: 'File upload completed:',
		es: 'Carga de archivo fija:',
	},
	choose_file: {
		'pt-BR': 'Escolher Arquivo',
		en: 'Choose File',
		es: 'Elija el archivo',
	},
	success: {
		'pt-BR': 'Sucesso',
		en: 'Success',
		es: 'Éxito',
	},
	from: {
		'pt-BR': 'A partir de',
		en: 'From',
		es: 'Desde',
	},
	to: {
		'pt-BR': 'Até',
		en: 'To',
		es: 'Hasta',
	},
	it_is_not_possible_to_save_usage: {
		'pt-BR': 'Não é possível salvar a utilização',
		en: 'It is not possible to save execution',
		es: 'No se puede guardar el uso',
	},
	usage_created_successfuly: {
		'pt-BR': 'Modelo criado com sucesso',
		en: 'Successfully created template',
		es: 'Registro creado con éxito',
	},
	an_error_happened: {
		'pt-BR': 'Aconteceu um erro',
		en: 'An error happened',
		es: 'Pasó un error',
	},
	please_wait: {
		'pt-BR': 'Aguarde',
		en: 'Please wait',
		es: 'Sostener',
	},
	please_wait_p: {
		'pt-BR': 'Aguarde...',
		en: 'Please wait...',
		es: 'Sostener...',
	},
	department_saved_successfully: {
		'pt-BR': 'Área salva com sucesso',
		en: 'Department successfully saved',
		es: 'Área exitosa',
	},
	department_removed_successfully: {
		'pt-BR': 'Área removida com sucesso',
		en: 'Department successfully removed',
		es: 'Área exitosa eliminada',
	},
	fill_name_department: {
		'pt-BR': 'Preencha o nome da área',
		en: 'Fill in the department name',
		es: 'Rellene el nombre del área',
	},
	necessary_define_department: {
		'pt-BR': 'É necessário definir uma área',
		en: 'It is necessary to define an department',
		es: 'Debes definir un área',
	},
	necessary_define_process_name: {
		'pt-BR': 'É necessário definir um nome pro processo',
		en: 'It is necessary to define a name for the process',
		es: 'Es necesario definir un nombpre para el proceso',
	},
	necessary_define_process_name: {
		'pt-BR': 'É necessário definir um nome pro processo',
		en: 'It is necessary to define a name for the process',
		es: 'Es necesario definir un nombpre para el proceso',
	},
	necessary_define_process_name: {
		'pt-BR': 'É necessário definir um nome pro processo',
		en: 'It is necessary to define a name for the process',
		es: 'Es necesario definir un nombpre para el proceso',
	},
	no_subprocess_registered: {
		'pt-BR': 'Nenhum sub-processo cadastrado',
		en: 'No sub-process registered',
		es: 'No hay subproceso registrado',
	},
	edit_capital: {
		'pt-BR': 'EDITAR',
		en: 'EDIT',
		es: 'EDITAR',
	},
	edit: {
		'pt-BR': 'Editar',
		en: 'Edit',
		es: 'Editar',
	},
	save_capital: {
		'pt-BR': 'SALVAR',
		en: 'SAVE',
		es: 'AHORRAR',
	},
	it_is_necessary_to_inform_a_valid_name: {
		'pt-BR': 'É necessário informar um nome válido',
		en: 'It is necessary inform a valid name',
		es: 'Es necesario informar un nombre válido.',
	},
	it_is_necessary_to_inform_a_valid_email: {
		'pt-BR': 'É necessário informar um email válido',
		en: 'It is necessary inform a valid email',
		es: 'Debe informar un correo electrónico válido',
	},
	it_is_necessary_to_inform_a_valid_department: {
		'pt-BR': 'É necessário informar uma área válida',
		en: 'It is necessary inform a valid department',
		es: 'Es necesario informar a un área válida.',
	},
	it_is_necessary_to_inform_a_valid_position: {
		'pt-BR': 'É necessário informar um cargo válido',
		en: 'It is necessary to inform a valid position.',
		es: 'Es necesario informar una posición válida.',
	},
	it_is_necessary_to_confirm_lgpd: {
		'pt-BR': 'É necessário confirmar LGPD',
		en: 'It is necessary to confirm LGPD',
		es: 'Es necesario confirmar LGPD',
	},
	add_to_my_plan: {
		'pt-BR': 'Adicionar ao Meu Plano',
		en: 'Add to My Plan',
		es: 'Añadir a mi plan',
	},
	added: {
		'pt-BR': 'Adicionado',
		en: 'Added',
		es: 'Adicional',
	},
	see_more: {
		'pt-BR': 'ver mais',
		en: 'show more',
		es: 'ver más',
	},
	see_less: {
		'pt-BR': 'ver menos',
		en: 'show less',
		es: 'ver menos',
	},
	license: {
		'pt-BR': 'licença',
		en: 'license',
		es: 'licencia',
	},
	licenses: {
		'pt-BR': 'licenças',
		en: 'licenses',
		es: 'licencias',
	},
	it_in_only_possible_to_invite: {
		'pt-BR': 'Só é possível convidar',
		en: 'It is only possible to invite',
		es: 'Solo puedes invitar',
	},
	employee_small: {
		'pt-BR': 'colaborador',
		en: 'employee',
		es: 'colaborador',
	},
	employees: {
		'pt-BR': 'colaboradores',
		en: 'employees',
		es: 'contribuyentes',
	},
	employees_capitalized: {
		'pt-BR': 'Colaboradores',
		en: 'Employees',
		es: 'Contribuyentes',
	},
	warn_me: {
		'pt-BR': 'Avise-me',
		en: 'Warn me',
		es: 'Advierteme',
	},
	you_will_receive_news: {
		'pt-BR': 'Você receberá as novidades',
		en: 'You will receive the news',
		es: 'Recibirás las noticias.',
	},
	add: {
		'pt-BR': 'Adicionar',
		en: 'Add',
		es: 'Añadir',
	},
	to_your_plan: {
		'pt-BR': 'ao seu plano',
		en: 'to your plan',
		es: 'a tu plan',
	},
	choose_a_service: {
		'pt-BR': 'Escolha um serviço do seu plano para trocar licenças por',
		en: 'Choose a service from your plan to exchange licenses for',
		es: 'Elija un servicio de su plan para intercambiar licencias para',
	},
	make_exchange: {
		'pt-BR': 'Efetuar Troca',
		en: 'Make Exchange',
		es: 'Intercambio',
	},
	confirm: {
		'pt-BR': 'Confirmar',
		en: 'Confirm',
		es: 'Confirmar',
	},
	advance: {
		'pt-BR': 'Avançar',
		en: 'Next',
		es: 'Avanzar',
	},
	save_changes: {
		'pt-BR': 'Salvar Alterações',
		en: 'Save Changes',
		es: 'Guardar ediciones',
	},
	change_of_plan: {
		'pt-BR': 'Mudança de Plano',
		en: 'Change of Plan',
		es: 'Cambio de planes',
	},
	licenses_available: {
		'pt-BR': 'licenças disponíveis',
		en: 'available licenses',
		es: 'Licencias disponibles',
	},
	license_available: {
		'pt-BR': 'licença disponível',
		en: 'available license',
		es: 'licencia',
	},
	unable_complete_service_exchange: {
		'pt-BR': 'Não foi possível concluir a troca do serviço',
		en: 'Unable to complete service exchange',
		es: 'No se pudo completar el intercambio de servicios.',
	},
	please_try_again_later: {
		'pt-BR': 'Por favor, tente novamente mais tarde',
		en: 'Please try again later',
		es: 'Por favor, inténtelo de nuevo más tarde',
	},
	exchange_confirmed: {
		'pt-BR': 'Troca confirmada',
		en: 'Exchange confirmed',
		es: 'Intercambio confirmado',
	},
	soon_you_will_be_able_access_service: {
		'pt-BR':
			'Em breve você poderá acessar o seu novo serviço para convidar colaborares e ter acesso a todas as vantagens',
		en: 'You will soon be able to access your new service to invite collaborators and have access to all the benefits',
		es: 'Pronto podrá acceder a su nuevo servicio para invitar a colaborar y acceder a todas las ventajas.',
	},
	models_configured: {
		'pt-BR': 'Modelos configurados',
		en: 'Models configured',
		es: 'Registros configurados',
	},
	model_configured: {
		'pt-BR': 'Modelo configurado',
		en: 'Model configured',
		es: 'Registro configurado',
	},
	you_can_allocate_only: {
		'pt-BR': 'Você só pode alocar',
		en: 'You can only allocate',
		es: 'Solo puedes asignar',
	},
	services: {
		'pt-BR': 'serviços',
		en: 'services',
		es: 'servicios',
	},
	service: {
		'pt-BR': 'serviço',
		en: 'service',
		es: 'Servicio',
	},
	it_is_necessary_to_choose_at_most: {
		'pt-BR': 'É necessário escolher no máximo',
		en: 'It is necessary to choose at most',
		es: 'Es necesario elegir como máximo.',
	},
	when_confirmed_action_cant_be_undone: {
		'pt-BR': 'Ao confirmar, essa ação não poderá ser desfeita',
		en: 'When confirmed, this action cannot be undone and',
		es: 'Al confirmar, esta acción no se puede deshacer.',
	},
	when_confirmed_action_cant_be_undone_part_2: {
		'pt-BR':
			'todas as licenças e, consequentemente, o acesso ao serviço e os seus modelos salvos',
		en: 'all licenses and, consequently, access to the service and its saved templates',
		es: 'Todas las licencias y, en consecuencia, acceso al servicio y sus modelos guardados.',
	},
	when_confirmed_action_cant_be_undone_part_3: {
		'pt-BR':
			'Ao confirmar, essa ação não poderá ser desfeita, sendo necessária nova realocação dos serviços',
		en: 'When confirmed, this action cannot be undone, requiring a new reallocation of services',
		es: 'En confirmación, esta acción no se puede deshacer, con una nueva reubicación de servicios.',
	},
	when_confirmed_action_cant_be_undone_part_4: {
		'pt-BR': 'Ao confirmar, o serviço',
		en: 'When confirmed, the service',
		es: 'Al confirmar, el servicio.',
	},
	when_confirmed_action_cant_be_undone_part_5: {
		'pt-BR': 'será excluído do seu plano e seus modelos salvos serão perdidos',
		en: 'will be deleted from your plan and your saved templates will be lost.',
		es: 'será excluido de su plan y sus modelos guardados se perderán',
	},
	and_the_collaborator: {
		'pt-BR': 'e o colaborador',
		en: 'and the collaborator',
		es: 'y el empleado',
	},
	and_the_collaborators: {
		'pt-BR': 'e o colaboradores',
		en: 'and the collaborators',
		es: 'y los empleados',
	},
	will_lose: {
		'pt-BR': 'perderá',
		en: 'will lose',
		es: 'perder',
	},
	will_lose_plural: {
		'pt-BR': 'perderão',
		en: 'will lose',
		es: 'perder',
	},
	exclude: {
		'pt-BR': 'Excluir',
		en: 'Exclude',
		es: 'Borrar',
	},
	exchange_service: {
		'pt-BR': 'Trocar serviço',
		en: 'Exchange service',
		es: 'Servicio',
	},
	administrator: {
		'pt-BR': 'Administrador',
		en: 'Administrator',
		es: 'Administrador',
	},
	confirm_exclude_settings_crew: {
		'pt-BR':
			'Deseja excluir esses colaboradores da sua equipe? Essa ação não poderá ser desfeita e eles perderão o acesso a todos os serviços e modelos configurados.',
		en: 'Do you want to exclude these collaborators from your team? This action cannot be undone and they will lose access to all configured services and templates.',
		es: '¿Quieres eliminar a estos empleados de tu equipo?',
	},
	do_you_want_to_exclude_collaborator_1: {
		'pt-BR': 'Deseja excluir o colaborador',
		en: 'Do you want to delete the collaborator',
		es: 'Quiero eliminar al empleado',
	},
	do_you_want_to_exclude_collaborator_2: {
		'pt-BR': 'da sua equipe? Essa ação',
		en: 'of your team? this action',
		es: '¿De tu equipo?',
	},
	do_you_want_to_exclude_collaborator_3: {
		'pt-BR': 'não poderá ser desfeita',
		en: 'cannot be undone',
		es: 'no se puede deshacer',
	},
	do_you_want_to_exclude_collaborator_4: {
		'pt-BR': 'e ele perderá o acesso a todos os serviços e modelos configurados',
		en: 'and he will lose access to all services and configured models',
		es: 'Y perderá el acceso a todos los servicios y modelos configurados.',
	},
	delete_collaborator: {
		'pt-BR': 'Excluir Colaborador',
		en: 'Delete Collaborator',
		es: 'Colaborador',
	},
	delete_collaborator_plural: {
		'pt-BR': 'Excluir Colaboradores',
		en: 'Delete Collaborators',
		es: 'Eliminar empleados',
	},
	collaborator_successfully_deleted: {
		'pt-BR': 'Colaborador excluído com sucesso',
		en: 'Collaborator successfully deleted',
		es: 'Colaborador con éxito',
	},
	collaborator_successfully_deleted_plural: {
		'pt-BR': 'Colaboradores excluídos com sucesso',
		en: 'Collaborators successfully deleted',
		es: 'Colaboradores excluidos con éxito',
	},
	collaborator_not_deleted: {
		'pt-BR': 'Houve um erro ao realizar a exclusão',
		en: 'There was an error performing the deletion',
		es: 'Hubo un error al realizar la exclusión.',
	},
	collaborator_lost_access: {
		'pt-BR': 'perdeu acesso aos serviços e não consta mais em sua equipe no Smarthis Hub.',
		en: 'lost access to services and is no longer on your team in Smarthis Hub.',
		es: 'El acceso perdido a los servicios y ya no aparece en su equipo en SmartThis Hub.',
	},
	collaborator_lost_access_plural: {
		'pt-BR':
			'Com a exclusão, os colaboradores perderam o acesso aos serviços e não constam mais em sua equipe no Smarthis Hub.',
		en: 'With the exclusion, collaborators lost access to services and are no longer included in your team on Smarthis Hub.',
		es: 'Con la exclusión, los empleados han perdido acceso a los servicios y ya no están consistentes en su equipo en Smarthis Hub.',
	},
	finalizing_request: {
		'pt-BR': 'Finalizando solicitação',
		en: 'Finalizing request',
		es: 'Finalización de la solicitud',
	},
	choosing_permissions_header_text: {
		'pt-BR': 'Escolha os serviços que deseja utilizar ou compartilhar no seu Smarthis Hub',
		en: 'Choose the services you want to use or share on your Smarthis Hub',
		es: 'Elija los servicios que desea usar o compartir en su SmartThis Hub',
	},
	choose: {
		'pt-BR': 'Escolha',
		en: 'Choose',
		es: 'Elección',
	},
	up_to: {
		'pt-BR': 'Até',
		en: 'Up to',
		es: 'Hasta',
	},
	services_with_your_licenses: {
		'pt-BR': 'serviços com as suas licenças',
		en: 'services with your licenses',
		es: 'Servicios con sus licencias.',
	},
	edit_model: {
		'pt-BR': 'Editar Modelo',
		en: 'Edit Model',
		es: 'Editar Registro',
	},
	save_model: {
		'pt-BR': 'Salvar Modelo',
		en: 'Save Model',
		es: 'Registro',
	},
	apply_filters: {
		'pt-BR': 'Aplicar filtros',
		en: 'Apply filters',
		es: 'Filtrar',
	},
	no_department: {
		'pt-BR': 'Sem Área',
		en: 'No Depártment',
		es: 'Apuesta',
	},
	hour: {
		'pt-BR': 'Hora',
		en: 'Hour',
		es: 'Hora',
	},
	hours_capital: {
		'pt-BR': 'Horas',
		en: 'Hours',
		es: 'Hora',
	},
	processes_capital_plural: {
		'pt-BR': 'Processos',
		en: 'Processes',
		es: 'Demanda judicial',
	},
	processes_capital_singular: {
		'pt-BR': 'Processo',
		en: 'Process',
		es: 'Proceso',
	},
	operator: {
		'pt-BR': 'Operador',
		en: 'Operator',
		es: 'Operador',
	},
	missing_business_area: {
		'pt-BR': 'Área não cadastrada',
		en: 'Missing Business Area',
		es: 'Área no registrada',
	},
	unavailable: {
		'pt-BR': 'Indisponível',
		en: 'Unavailable',
		es: 'Indisponible',
	},
	dashboard_not_available_hover: {
		'pt-BR': 'Complete as informações sobre os seus processos para obter mais insights',
		en: 'Fill in the information about your processes for more insights',
		es: 'Información completa sobre sus procesos para obtener más información.',
	},
	hours_worked: {
		'pt-BR': 'Horas trabalhadas',
		en: 'Hours worked',
		es: 'Horas trabajadas',
	},
	minutes_worked: {
		'pt-BR': 'Minutos trabalhadas',
		en: 'Minutes worked',
		es: 'Minuto trabajado',
	},
	robots: {
		'pt-BR': 'Robôs',
		en: 'Robots',
		es: 'Robots',
	},
	rpa_runtime: {
		'pt-BR': 'Horas RPA',
		en: 'RPA Runtime',
		es: 'Horas RPA',
	},
	processes: {
		'pt-BR': 'Processos',
		en: 'Processes',
		es: 'Processos',
	},
	area_successfully_registered: {
		'pt-BR': 'Área cadastrada com sucesso!',
		en: 'Area successfully registered!',
		es: 'Área registrada con éxito!',
	},
	you_can_now_associate_processes_to_area: {
		'pt-BR': 'Você já pode associar processos a área',
		en: 'You can now associate processes to area',
		es: 'Ya puedes asociar procesos desde el área.',
	},
	in: {
		'pt-BR': 'em',
		en: 'in',
		es: 'en',
	},
	settings: {
		'pt-BR': 'Configurações',
		en: 'Settings',
		es: 'ajustes',
	},
	month_1: {
		'pt-BR': 'Janeiro',
		en: 'January',
		es: 'enero',
	},
	month_2: {
		'pt-BR': 'Fevereiro',
		en: 'February',
		es: 'febrero',
	},
	month_3: {
		'pt-BR': 'Março',
		en: 'March',
		es: 'marcha',
	},
	month_4: {
		'pt-BR': 'Abril',
		en: 'April',
		es: 'abril',
	},
	month_5: {
		'pt-BR': 'Maio',
		en: 'May',
		es: 'Mayo',
	},
	month_6: {
		'pt-BR': 'Junho',
		en: 'June',
		es: 'junio',
	},
	month_7: {
		'pt-BR': 'Julho',
		en: 'July',
		es: 'mes de julio',
	},
	month_8: {
		'pt-BR': 'Agosto',
		en: 'August',
		es: 'agosto',
	},
	month_9: {
		'pt-BR': 'Setembro',
		en: 'September',
		es: 'septiembre',
	},
	month_10: {
		'pt-BR': 'Outubro',
		en: 'October',
		es: 'octubre',
	},
	month_11: {
		'pt-BR': 'Novembro',
		en: 'November',
		es: 'noviembre',
	},
	month_12: {
		'pt-BR': 'Dezembro',
		en: 'December',
		es: 'diciembre',
	},
	month: {
		'pt-BR': 'Mês',
		en: 'Month',
		es: 'Mes',
	},
	week: {
		'pt-BR': 'Semana',
		en: 'Week',
		es: 'Semana',
	},
	completed: {
		'pt-BR': 'Concluídos',
		en: 'Completed',
		es: 'Completados',
	},
	faulted: {
		'pt-BR': 'falharam',
		en: 'Faulted',
		es: 'falto',
	},
	paused_stopped: {
		'pt-BR': 'Pausados',
		en: 'Stopped',
		es: 'Pausado',
	},
	busy_time: {
		'pt-BR': 'Tempo ocupado',
		en: 'Busy time',
		es: 'Tiempo ocupado',
	},
	minutes_minified: {
		'pt-BR': 'min',
		en: 'min',
		es: 'minuto',
	},
	and: {
		'pt-BR': 'e',
		en: 'and',
		es: 'y',
	},
	seconds: {
		'pt-BR': 'segundos',
		en: 'seconds',
		es: 'segundos',
	},
	second: {
		'pt-BR': 'segundo',
		en: 'second',
		es: 'segundo',
	},
	impact_on_roi_financial: {
		'pt-BR': 'Impacto no ROI (financeiro)',
		en: 'Impact on ROI (financial)',
		es: 'Impacto en el ROI (Financiero)',
	},
	return_in_hours_small: {
		'pt-BR': 'Impacto em horas retornadas',
		en: 'Impact on returned hours',
		es: 'Impacto en las horas devueltas',
	},
	roi_impact: {
		'pt-BR': 'impacto no ROI',
		en: 'ROI Impact',
		es: 'Impacto en el ROI',
	},
	between: {
		'pt-BR': 'Entre',
		en: 'From',
		es: 'Entre',
	},
	are_you_sure_you_want_to_remove_this_users_access: {
		'pt-BR': 'Você tem certeza que deseja remover o acesso desse usuário?',
		en: 'Are you sure you want to remove this user`s access?',
		es: '¿Está seguro de que desea eliminar el acceso de este usuario?',
	},
	yes: {
		'pt-BR': 'Sim',
		en: 'Yes',
		es: 'Sí',
	},
	no: {
		'pt-BR': 'Não',
		en: 'No',
		es: 'No',
	},
	table: {
		'pt-BR': 'Tabela',
		en: 'Table',
		es: 'Tabla',
	},
	minute: {
		'pt-BR': 'minuto',
		en: 'minute',
		es: 'minuto',
	},
	minutes: {
		'pt-BR': 'minutos',
		en: 'minutes',
		es: 'minuto',
	},
	this_user_has_already_been_added: {
		'pt-BR': 'Este usuário já foi adicionado',
		en: 'This user has already been added',
		es: 'Este usuario ya ha sido añadido.',
	},
	invite_group_updated_successfuly: {
		'pt-BR': 'Grupo de convites atualizado com sucesso',
		en: 'Invite group updated successfuly',
		es: 'Grupo de invitaciones actualizadas con éxito.',
	},
	complete: {
		'pt-BR': 'Completos',
		en: 'Complete',
		es: 'Completo',
	},
	data_complete: {
		'pt-BR': 'Informações Completas',
		en: 'Data Complete',
		es: 'Información completa',
	},
	incomplete_data: {
		'pt-BR': 'Informações Incompletas',
		en: 'Incomplete Data',
		es: 'Información incompleta',
	},
	year: {
		'pt-BR': 'Ano',
		en: 'Year',
		es: 'Año',
	},
	from_de: {
		'pt-BR': 'De',
		en: 'From',
		es: 'En',
	},
	of: {
		'pt-BR': 'de',
		en: 'of',
		es: 'de',
	},
	for: {
		'pt-BR': 'por',
		en: 'for',
		es: 'por',
	},
	you_have_reached_licenses_limit: {
		'pt-BR': 'Você atingiu o limite de licenças',
		en: 'You have reached the license limit',
		es: 'Has llegado al límite de las licencias.',
	},
	plan_registration_error_msg: {
		'pt-BR':
			'Não foi possível concluir o seu registro de Plano, por favor tente novamente. Caso o problema persista, entre em contato por:',
		en: 'Unable to complete your Plan registration, please try again. If the problem persists, please contact us by:',
		es: 'No se pudo completar el registro de su plan, inténtelo de nuevo.',
	},
	hub_contact_email: {
		'pt-BR': 'hub-contato@smarthis.com.br',
		en: 'hub-contato@smarthis.com.br',
		es: 'hub-contato@smarthis.com.br',
	},
	you_are_hiring_more_licenses_allowed: {
		'pt-BR': 'Você está contratando mais licenças do que o seu plano permite',
		en: 'You are hiring more licenses than your plan allows',
		es: 'Está contratando más licencias de las que su plan permite',
	},
	unable_add_service: {
		'pt-BR': 'Não foi possível adicionar o serviço',
		en: 'Unable to add the service',
		es: 'No se pudo agregar el servicio.',
	},
	unable_add_service_text: {
		'pt-BR': 'Ocorreu um erro ao adicionar o serviço. Por favor, tente novamente mais tarde.',
		en: 'There was an error adding the service. Please try again later.',
		es: 'Se produjo un error al agregar el servicio.',
	},
	you_will_be_notified: {
		'pt-BR': 'Você será notificado',
		en: 'You will be notified',
		es: 'Serás notificado',
	},
	notify_me_when_available: {
		'pt-BR': 'Avise-me quando estiver disponível',
		en: 'Notify me when available',
		es: 'Notifíqueme cuando esté disponible',
	},
	the_end_date_needs_to_be_grater_than_start_date: {
		'pt-BR': 'A data final necessita ser maior que a inicial',
		en: 'The end date needs to be grater than start date',
		es: 'La fecha final debe ser mayor que la inicial.',
	},
	the_start_date_needs_to_be_less_than_end_date: {
		'pt-BR': 'A data inicial necessita ser menor que a final',
		en: 'The start date needs to be less than end date',
		es: 'La fecha inicial debe ser menor que la',
	},
	you_have_reached_limit_available_licenses: {
		'pt-BR': 'Você atingiu o limite de licenças disponíveis',
		en: 'You have reached the limit of available licenses',
		es: 'Has llegado a los límites de las licencias disponibles.',
	},
	error_saving_interest: {
		'pt-BR': 'Ocorreu um erro ao salvar seu interesse. Por favor, tente novamente mais tarde',
		en: 'An error occurred saving your interest. Please try again later',
		es: 'Se produjo un error al guardar su interés.',
	},
	maximum_occupancy: {
		'pt-BR': 'Ocupação Máxima',
		en: 'Maximum Occupancy',
		es: 'Ocupación máxima',
	},
	please_enter_profissional_email_address: {
		'pt-BR': 'Por favor, insira um e-mail profissional',
		en: 'Please enter a professional email address',
		es: 'Por favor ingrese un correo electrónico profesional',
	},
	loading_my_services: {
		'pt-BR': 'Carregando meus serviços',
		en: 'Loading my services',
		es: 'Cargando mis servicios',
	},
	opening_upgrade_options: {
		'pt-BR': 'Abrindo opções de upgrade',
		en: 'Opening up upgrade options',
		es: 'Opciones de actualización de apertura',
	},
	loading_zip_code_information: {
		'pt-BR': 'Carregando Informações do CEP',
		en: 'Loading CEP information',
		es: 'Cargando información del CEP',
	},
	are_you_sure_you_entered_zip_code_correctly: {
		'pt-BR': 'Tem certeza que digitou o CEP corretamente?',
		en: 'Are you sure you entered zip code correctly',
		es: '¿Está seguro de que usted escribió el código postal correctamente?',
	},
	invalid_cnpj_please_type_again: {
		'pt-BR': 'CNPJ inválido. Por favor, digite novamente',
		en: 'Invalid CNPJ. Please, type again',
		es: 'CNPJ inválido.',
	},
	unsupported_file: {
		'pt-BR': 'Arquivo não suportado',
		en: 'Unsupported file',
		es: 'Archivo no admitido',
	},
	checking_your_input_file: {
		'pt-BR': 'Verificando seu arquivo de entrada',
		en: 'Checking your input file',
		es: 'Comprobando su archivo de entrada',
	},
	your_profile_has_been_updated: {
		'pt-BR': 'Seu perfil foi atualizado',
		en: 'Your profile has been updated',
		es: 'Tu perfil ha sido actualizado',
	},
	you_have_transferred_all_licenses: {
		'pt-BR': 'Você transferiu todas as suas licenças',
		en: 'You have transferred all your licenses',
		es: 'Tras transferías todas tus licencias',
	},
	to_use_this_service_you_need: {
		'pt-BR': 'Para utilizar esse serviço você precisa realocá-las ou fazer upgrade',
		en: 'To use this service you need to relocate or upgrade them',
		es: 'Para usar este servicio necesitas reubicarlos o actualizar',
	},
	the_date_must_be_greater_than_1_days_from_today: {
		'pt-BR': 'A data necessita ser maior que 1 dia a partir de hoje',
		en: 'The date must be greater than 1 day from today',
		es: 'La fecha debe ser mayor a 1 día a partir de hoy',
	},
	your_template_will_be_executed: {
		'pt-BR': 'Seu modelo será executado',
		en: 'Your template will be executed',
		es: 'Su registro se ejecutará',
	},
	monthly: {
		'pt-BR': 'mensalmente',
		en: 'monthly',
		es: 'mensual',
	},
	every_day: {
		'pt-BR': 'todo dia',
		en: 'every day',
		es: 'todos los días',
	},
	starting_in: {
		'pt-BR': 'começando em',
		en: 'starting in',
		es: 'comenzando en el',
	},
	weekly: {
		'pt-BR': 'semanalmente',
		en: 'weekly',
		es: 'semanalmente',
	},
	every_female: {
		'pt-BR': 'toda',
		en: 'every',
		es: 'cada',
	},
	every_male: {
		'pt-BR': 'todo',
		en: 'every',
		es: 'cada',
	},
	without_repeat: {
		'pt-BR': 'sem repetição',
		en: 'without repeat',
		es: 'sin repetición',
	},
	week_0: {
		'pt-BR': 'Domingo',
		en: 'Sunday',
		es: 'Domingo',
	},
	week_1: {
		'pt-BR': 'Segunda-feira',
		en: 'Monday',
		es: 'Lunes',
	},
	week_2: {
		'pt-BR': 'Terça-feira',
		en: 'Tuesday',
		es: 'Martes',
	},
	week_3: {
		'pt-BR': 'Quarta-feira',
		en: 'Wednesday',
		es: 'Miércoles',
	},
	week_4: {
		'pt-BR': 'Quinta-feira',
		en: 'Thursday',
		es: 'Jueves',
	},
	week_5: {
		'pt-BR': 'Sexta-feira',
		en: 'Friday',
		es: 'Viernes',
	},
	week_6: {
		'pt-BR': 'Sábado',
		en: 'Saturday',
		es: 'Sábado',
	},
	scheduled: {
		'pt-BR': 'Agendado',
		en: 'Scheduled',
		es: 'Programado',
	},
	today: {
		'pt-BR': 'Hoje',
		en: 'Today',
		es: 'Hoy',
	},
	day: {
		'pt-BR': 'Dia',
		en: 'Day',
		es: 'Dia',
	},
	with_capitalized: {
		'pt-BR': 'Com',
		en: 'With',
		es: 'Con',
	},
	executions: {
		'pt-BR': 'execuções',
		en: 'executions',
		es: 'ejecuciones',
	},
	begining_capitalized: {
		'pt-BR': 'Começando',
		en: 'Begining',
		es: 'A partir del',
	},
	ending_capitalized: {
		'pt-BR': 'Terminando',
		en: 'Ending',
		es: 'Hasta',
	},
	refresh_the_page_and_try_again: {
		'pt-BR': 'atualize a página e tente novamente',
		en: 'refresh the page and try again',
		es: 'actualice la página y vuelva a intentarlo',
	},
	was_executed_between: {
		'pt-BR': 'foi executado no intervalo das',
		en: 'was executed between',
		es: 'se ejecuto entre',
	},
	it_is_estimated_that_the_process_would_take: {
		'pt-BR': 'Estima-se que o processo demoraria',
		en: 'It is estimated that the process would take',
		es: 'Se estima que el proceso tomaría',
	},
	to_be_executed: {
		'pt-BR': 'para ser executado',
		en: 'to be executed',
		es: 'para ser ejecutado',
	},
	unable_to_calculate_estimate: {
		'pt-BR': 'Não foi possível calcular a estimativa',
		en: 'Unable to calculate estimate',
		es: 'No se puede calcular la estimación',
	},
	process_did_not_run_between: {
		'pt-BR': 'Processo não foi executado entre',
		en: 'Process did not run between',
		es: 'El proceso no se ejecutó entre',
	},
	contact_requested: {
		'pt-BR': 'Contato solicitado',
		en: 'Contact requested',
		es: 'Contacto solicitado',
	},
	unable_to_remove_execution_please_try_again: {
		'pt-BR': 'Não foi possível remover a utilização, por favor tente novamente',
		en: 'Unable to remove execution, please try again',
		es: 'No se puede eliminar el uso, inténtalo de nuevo',
	},
	only_one_file_can_be_added_at_a_time: {
		'pt-BR': 'Só é possível adicionar um arquivo por vez.',
		en: 'Only one file can be added at a time.',
		es: 'Solo se puede agregar un archivo a la vez.',
	},
	the_inserted_file_exceeds_the_size_limit: {
		'pt-BR':
			'O arquivo inserido ultrapassa o tamanho permitido. Insira um arquivo padrão de no máximo 2MB.',
		en: 'The inserted file exceeds the allowed size. Insert a default file of no more than 2MB.',
		es: 'El archivo insertado excede el tamaño permitido. Inserte un archivo predeterminado de no más de 2 MB.',
	},
	edit: {
		'pt-BR': 'Editar',
		en: 'Edit',
		es: 'Editar',
	},
	manage_appointments: {
		'pt-BR': 'Gerenciar agendamentos',
		en: 'Mange appointments',
		es: 'Gestionar horarios',
	},
	create_appointment: {
		'pt-BR': 'Criar agendamento',
		en: 'Create appointment',
		es: 'Crear horario',
	},
	edit_appointment: {
		'pt-BR': 'Editar agendamento',
		en: 'Edit appointment',
		es: 'Editar horario',
	},
	appointment_created_successfully: {
		'pt-BR': 'Agendamento criado com sucesso',
		en: 'Appointment created successfully',
		es: 'Horario creado con éxito',
	},
	appointment_edited_successfully: {
		'pt-BR': 'Agendamento editado com sucesso',
		en: 'Appointment edited successfully',
		es: 'Horario editado con éxito',
	},
	register_process: {
		'pt-BR': 'Cadastrar Processo',
		en: 'Register Process',
		es: 'Registrar Proceso',
	},
	all_male: {
		'pt-BR': 'Todos',
		en: 'All',
		es: 'Todo',
	},
	sub_processes_selected: {
		'pt-BR': 'sub-processos selecionados',
		en: 'sub-processes selected',
		es: 'subprocesos selecionados',
	},
	sub_process_selected: {
		'pt-BR': 'sub-processo selecionado',
		en: 'sub-process selected',
		es: 'subproceso selecionado',
	},
	select: {
		'pt-BR': 'Selecionar',
		en: 'Select',
		es: 'Seleccione',
	},
	edit_process: {
		'pt-BR': 'Editar Processo',
		en: 'Edit Process',
		es: 'Editar Proceso',
	},
	process_registered_successfully: {
		'pt-BR': 'Processo cadastrado com sucesso!',
		en: 'Process registered successfully!',
		es: '¡Proceso registrado con éxito!',
	},
	process_edited_successfully: {
		'pt-BR': 'Processo editado com sucesso!',
		en: 'Process edited successfully!',
		es: '¡Proceso editado con éxito!',
	},
	process_deleted_successfully: {
		'pt-BR': 'Processo excluído com sucesso!',
		en: 'Process deleted successfully!',
		es: '¡Proceso eliminado con éxito!',
	},
	error_deleting_process: {
		'pt-BR':
			'Não foi possível excluir o processo. Por favor atualize a página e tente novamente.',
		en: 'Could not delete process. Please refresh the page and try again.',
		es: 'No se pudo eliminar el proceso. Actualice la página y vuelva a intentarlo.',
	},
	it_was_not_possible_to_register_your_process_try_again: {
		'pt-BR': 'Não foi possível cadastrar o Processo. Tente novamente.',
		en: 'It was not possible to register your Process. Try again.',
		es: 'No fue posible registrar el Proceso. Inténtalo de nuevo.',
	},
	it_was_not_possible_to_register_your_subprocess_try_again: {
		'pt-BR': 'Não foi possível cadastrar o Sub-processo. Tente novamente.',
		en: 'It was not possible to register your Sub-process. Try again.',
		es: 'No fue posible registrar el Subproceso. Inténtalo de nuevo.',
	},
	subprocess_edited_successfully: {
		'pt-BR': 'Sub-processo editado com sucesso!',
		en: 'Sub-process edited successfully!',
		es: '¡Subproceso editado con éxito!',
	},
	it_is_necessary_to_inform_transaction_type: {
		'pt-BR': 'É necessário informar o tipo de transação',
		en: 'It is necessary to inform transaction type',
		es: 'Es necesario informar el tipo de transacción',
	},
	all_sub_processes_were_registered: {
		'pt-BR': 'Todos Sub-processos foram cadastrados',
		en: 'All Sub-processes were registered',
		es: 'Todos los Subprocesos han sido registrad',
	},
	now_your_dashboard_will_bring: {
		'pt-BR':
			'Agora o seu Dashboard vai trazer uma visualização ainda mais exata das execuções e retornos da sua operação',
		en: 'Now your Dashboard will bring an even more accurate view of the executions and returns related to your operation',
		es: 'Ahora tu Dashboard traerá una visión aún más precisa de las ejecuciones y devoluciones de tu operación',
	},
	go_to_dashboard: {
		'pt-BR': 'Ir para o Dashboard',
		en: 'Go to Dashboard',
		es: 'Ir al Dashboard',
	},
	one_or_more_fields_are_empty: {
		'pt-BR':
			'Um ou mais campos obrigatórios estão vazios. Preencha os campos indicados para completar seu cadastro.',
		en: 'One or more required fields are empty. Fill in the indicated fields to complete your registration.',
		es: 'Uno o más campos obligatorios están vacíos. Rellene los campos indicados para completar su registro.',
	},
	one_or_more_fields_are_invalid: {
		'pt-BR':
			'Um ou mais campos estão inválidos. Preencha os campos indicados para completar o seu cadastro.',
		en: 'One or more fields are invalid. Fill in the indicated fields to complete your registration.',
		es: 'Uno o más campos no son válidos. Rellene los campos indicados para completar su registro.',
	},
	appointment_removed_successfully: {
		'pt-BR': 'Agendamento removido com sucesso',
		en: 'Appointment removed successfully',
		es: 'Horario eliminado con éxito',
	},
	invalid_cell_phone: {
		'pt-BR': 'Celular inválido',
		en: 'Invalid cell phone',
		es: 'Celular inválido',
	},
	we_are_having_trouble_fetching_your_data: {
		'pt-BR':
			'Estamos com dificuldade para buscar os seus dados. Atualize a página e tente novamente. Caso o problema persista contate a equipe do HUB',
		en: "We're having trouble fetching your data. Please refresh the page and try again. If the problem persists, contact the HUB team.",
		es: 'Estamos teniendo problemas para obtener sus datos. Actualice la página y vuelva a intentarlo. Si el problema persiste, póngase en contacto con el equipo de HUB.',
	},
	area: {
		'pt-BR': 'Área',
		en: 'Area',
		es: 'Área',
	},
	days: {
		'pt-BR': 'dias',
		en: 'days',
		es: 'días',
	},
	until_the_positive_roi: {
		'pt-BR': 'até o ROI positivo',
		en: 'until the positive ROI',
		es: 'hasta el ROI positivo',
	},
	of_positive_roi: {
		'pt-BR': 'de ROI positivo',
		en: 'of positive ROI',
		es: 'de ROI positivo',
	},
	returned_hours: {
		'pt-BR': 'Horas Retornadas',
		en: 'Returned Hours',
		es: 'Horas devueltas',
	},
	rate: {
		'pt-BR': 'Taxa',
		en: 'Rate',
		es: 'Tarifa',
	},
	occupation: {
		'pt-BR': 'Ocupação',
		en: 'Occupation',
		es: 'Ocupación',
	},
	to: {
		'pt-BR': 'à',
		en: 'to',
		es: 'al',
	},
	execution_history: {
		'pt-BR': 'Histórico de execuções',
		en: 'Execution History',
		es: 'Historial de ejecución',
	},
	general: {
		'pt-BR': 'Geral',
		en: 'All',
		es: 'Todo',
	},
	last_month: {
		'pt-BR': 'Último mês',
		en: 'Last month',
		es: 'El mes pasado',
	},
	last_year: {
		'pt-BR': 'Último ano',
		en: 'Last year',
		es: 'El ano pasado',
	},
};

function getCSRFauth() {
	return $('input[name=csrfmiddlewaretoken]').val();
}

function getLoadingDiv(with_parent = true, small = '', parent_class = '', parent_style = '') {
	return with_parent
		? `<div class="loading_div d-flex justify-content-center align-items-center ${parent_class}" data-html2canvas-ignore style="${parent_style}"><div class="loader ${small}"></div></div>`
		: `<div class="loader${small}"></div>`;
}
