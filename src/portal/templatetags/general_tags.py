from django import template

register = template.Library()

# pra manter mais organizado, deixar essa função sempre por último


@register.filter
def translate(name, language):
    dictionary = {
        "overview_capital": {
            "pt-BR": "VISÃO GERAL",
            "en": "OVERVIEW",
            "es": "VISIÓN GENERAL"
        },
        "total_hours_rpa": {
            "pt-BR": "Total de Horas RPA",
            "en": "RPA Total hours",
            "es": "Horas totales de RPA"
        },
        "by_area": {
            "pt-BR": "por Área",
            "en": "by Department",
            "es": "por Área"
        },
        "roi_ by_area": {
            "pt-BR": "ROI por Área",
            "en": "ROI by Department",
            "es": "ROI por Área"
        },
        "employee": {
            "pt-BR": "Colaborador",
            "en": "Employee",
            "es": "Colaborador"
        },
        "rpa": {
            "pt-BR": "RPA",
            "en": "RPA",
            "es": "RPA"
        },
        "average_execution_time_par_min_dot_par_by_process": {
            "pt-BR": "Tempo médio de Execução (Min.) por Processos",
            "en": "Average Execution Time (Min.) by Process",
            "es": "Tiempo Promedio de Ejecución (Min.) por Proceso"
        },
        "average_time_par_min_par": {
            "pt-BR": "Tempo Médio (minutos)",
            "en": "Average time (minutes)",
            "es": "Tiempo promedio (minutos)"
        },
        "total_hours_par_rpa_par_by_day": {
            "pt-BR": "Total de Horas (RPA) por Dia",
            "en": "RPA total daily hours",
            "es": "Horas totales (RPA) por día"
        },
        "execution_time_of_processes_by_day": {
            "pt-BR": "Tempo de execução dos processos por dia",
            "en": "Daily process execution time",
            "es": "Tiempo de ejecución de procesos por día."
        },
        "total_exempt_hours": {
            "pt-BR": "Total de Horas que colaboradores gastariam",
            "en": "Executors Total Hours would spent",
            "es": "Horas totales que los empleados pasarían"
        },
        "gain_in_hours": {
            "pt-BR": "Total de horas retornadas (%)",
            "en": "Freed up time (%)",
            "es": "Horas totales devueltas (%)"
        },
        "operation_performance": {
            "pt-BR": "Performance Operacional",
            "en": "Operation Performance",
            "es": "Desempeño operativo"
        },
        "average_occupancy_per_hour_par_in_minutes_par": {
            "pt-BR": "Ocupação Média por Hora (em minutos)",
            "en": "Average Occupancy per Hour (in minutes)",
            "es": "Ocupación promedio por hora (en minutos)"
        },
        "process_by_status": {
            "pt-BR": "Processo por Status",
            "en": "Process by Status",
            "es": "Proceso por Estado"
        },
        "successful": {
            "pt-BR": "Sucesso",
            "en": "Successful",
            "es": "Éxito"
        },
        "faulted": {
            "pt-BR": "Falhou",
            "en": "Faulted",
            "es": "Fallido"
        },
        "stopped": {
            "pt-BR": "Parado",
            "en": "Stopped",
            "es": "Detenido"
        },
        "robot_utilization_rate": {
            "pt-BR": "Taxa de Ocupação por Robô",
            "en": "Robot Utilization Rate",
            "es": "Tasa de ocupación por robot"
        },
        "filters": {
            "pt-BR": "Filtros",
            "en": "Filters",
            "es": "Filtros"
        },
        "from": {
            "pt-BR": "A partir de",
            "en": "From",
            "es": "Desde"
        },
        "to": {
            "pt-BR": "e",
            "en": "to",
            "es": "y"
        },
        "clean_filters": {
            "pt-BR": "Limpar Filtros",
            "en": "Clean Filters",
            "es": "Borrar Filtros"
        },
        "business_area": {
            "pt-BR": "Área",
            "en": "Business Area",
            "es": "Área"
        },
        "select_department": {
            "pt-BR": "Selecione a Área",
            "en": "Select Department",
            "es": "Seleccionar Departamento"
        },
        "process": {
            "pt-BR": "Processo",
            "en": "Process",
            "es": "Proceso"
        },
        "process_capital": {
            "pt-BR": "PROCESSO",
            "en": "PROCESS",
            "es": "PROCESO"
        },
        "status": {
            "pt-BR": "Status",
            "en": "Status",
            "es": "Estado"
        },
        "host_machine": {
            "pt-BR": "Robô",
            "en": "Robot",
            "es": "Robot"
        },
        "all_male": {
            "pt-BR": "Todos",
            "en": "All",
            "es": "Todo"
        },
        "clean": {
            "pt-BR": "Limpar",
            "en": "Clean",
            "es": "Limpiar"
        },
        "add_business_area": {
            "pt-BR": "Cadastrar Nova Área",
            "en": "Add Business Area",
            "es": "Registrar Nuevo Departamento"
        },
        "add_new_business_area": {
            "pt-BR": "Cadastrar nova Área de Negócio",
            "en": "Add new Business Area",
            "es": "Registrar nueva Área de Negocio"
        },
        "remove_area": {
            "pt-BR": "Remover Área",
            "en": "Remove Department",
            "es": "Quitar Departamento"
        },
        "close": {
            "pt-BR": "Fechar",
            "en": "Close",
            "es": "Cerca"
        },
        "register": {
            "pt-BR": "Cadastrar",
            "en": "Register",
            "es": "Registrar"
        },
        "register_capital": {
            "pt-BR": "CADASTRAR",
            "en": "REGISTER",
            "es": "REGISTRAR"
        },
        "select_area": {
            "pt-BR": "Seleciona a Área",
            "en": "Select Department",
            "es": "Seleccionar Departamento"
        },
        "remove": {
            "pt-BR": "Remover",
            "en": "Remove",
            "es": "Quitar"
        },
        "process_name_on_the_machine": {
            "pt-BR": "Nome do Processo na máquina",
            "en": "Process Name",
            "es": "Nombre del proceso en la máquina"
        },
        "process_translate": {
            "pt-BR": "Tradução do Processo",
            "en": "Process Translate",
            "es": "Traducción de Procesos"
        },
        "average_time_in_min_dot_of_employee": {
            "pt-BR": "Tempo médio do colaborador (minutos)",
            "en": "Employee average time (minutes)",
            "es": "Tiempo promedio de empleado (minutos)"
        },
        "save_changes": {
            "pt-BR": "Salvar Alterações",
            "en": "Save Changes",
            "es": "Guardar Ediciones"
        },
        "save_changes_capital": {
            "pt-BR": "SALVAR ALTERAÇÕES",
            "en": "SAVE CHANGES",
            "es": "GUARDAR EDICIONES"
        },
        "home_start": {
            "pt-BR": "Início",
            "en": "Home",
            "es": "Comienzo"
        },
        "services": {
            "pt-BR": "Serviços",
            "en": "Services",
            "es": "Servicios"
        },
        "my_services": {
            "pt-BR": "Meus Serviços",
            "en": "My Services",
            "es": "Mis Servicios"
        },
        "configure_new_template": {
            "pt-BR": "Configurar Novo Modelo",
            "en": "Configure New Template",
            "es": "Configurar el Nuevo Registro"
        },
        "model_name": {
            "pt-BR": "Nome do modelo:",
            "en": "Model name:",
            "es": "Nombre Registro:"
        },
        "instructions_and_standard_file": {
            "pt-BR": "INSTRUÇÕES E ARQUIVO PADRÃO",
            "en": "INSTRUCTIONS AND STANDARD FILE",
            "es": "INSTRUCCIONES Y ARCHIVO ESTÁNDAR"
        },
        "instructions": {
            "pt-BR": "INSTRUÇÕES",
            "en": "INSTRUCTIONS",
            "es": "INSTRUCCIONES"
        },
        "cancel": {
            "pt-BR": "Cancelar",
            "en": "Cancel",
            "es": "Cancelar"
        },
        "to_save": {
            "pt-BR": "Salvar",
            "en": "Save changes",
            "es": "Guardar"
        },
        "consult": {
            "pt-BR": "Consulta",
            "en": "Read",
            "es": "Consulta"
        },
        "how_would_you_like_to_call_this": {
            "pt-BR": "Como você gostaria de chamar essa utilização",
            "en": "How would you like to call this execution",
            "es": "¿Cómo te gustaría llamar a este modelo?"
        },
        "format": {
            "pt-BR": "Formato",
            "en": "Format",
            "es": "Formato"
        },
        "of_the_resulting_files": {
            "pt-BR": "Do arquivo com resultados",
            "en": "Of the resulting files",
            "es": "Desde archivo con resultados"
        },
        "file_upload": {
            "pt-BR": "Upload de arquivo",
            "en": "File Upload",
            "es": "Carga de archivos"
        },
        "questions_about_file_format": {
            "pt-BR": "Dúvidas sobre o formato do arquivo?",
            "en": "Questions about the file format?",
            "es": "¿Dudas sobre el formato de los archivos?"
        },
        "click_here_small": {
            "pt-BR": "clique aqui",
            "en": "click here",
            "es": "haga clic aquí"
        },
        "download_the_example_here": {
            "pt-BR": "Baixe o exemplo aqui",
            "en": "Download the example here",
            "es": "Descargue el ejemplo aquí"
        },
        "no": {
            "pt-BR": "Não",
            "en": "No",
            "es": "No"
        },
        "exclude": {
            "pt-BR": "Excluir",
            "en": "Remove",
            "es": "Borrar"
        },
        "by_clicking": {
            "pt-BR": "Ao clicar em",
            "en": "By clicking at",
            "es": "Al hacer clic en"
        },
        "delete_the_template": {
            "pt-BR": "“Excluir”, o modelo",
            "en": "\"Delete\", the template",
            "es": "“Eliminar”, el registro"
        },
        "will_be_permanently_deleted_and_cannot_be_recovered": {
            "pt-BR": "será apagado permanentemente e não poderá mais ser recuperado.",
            "en": "will be permanently deleted and cannot be recovered.",
            "es": "se eliminará de forma permanente y ya no se podrá recuperar."
        },
        "delete_this_template": {
            "pt-BR": "Excluir este modelo?",
            "en": "Delete this template?",
            "es": "¿Eliminar este registro?"
        },
        "welcome_to": {
            "pt-BR": "Bem-Vindo ao",
            "en": "Welcome to",
            "es": "Bienvenido al"
        },
        "edit": {
            "pt-BR": "Editar",
            "en": "Edit",
            "es": "Editar"
        },
        "delete": {
            "pt-BR": "Excluir",
            "en": "Delete",
            "es": "Eliminar"
        },
        "start": {
            "pt-BR": "Iniciar",
            "en": "Start",
            "es": "Comienzo"
        },
        "name_model": {
            "pt-BR": "Nomear Modelo",
            "en": "Name Model",
            "es": "Nombre Registro"
        },
        "advance": {
            "pt-BR": "Avançar",
            "en": "Next",
            "es": "Avanzar"
        },
        "back": {
            "pt-BR": "Voltar",
            "en": "Back",
            "es": "Regreso"
        },
        "cancel_this_template": {
            "pt-BR": "Cancelar este modelo?",
            "en": "Cancel this template?",
            "es": "¿Cancelar esta registro?"
        },
        "cancel_the_template": {
            "pt-BR": "\"Cancelar \", o modelo",
            "en": "\"Cancel\", the template",
            "es": "\"Cancelar\", la registro"
        },
        "will_be_stopped_and_you_will_not_receive_any_results": {
            "pt-BR": "será interrompido e você não receberá resultados.",
            "en": "will be stopped and you will not receive results.",
            "es": "será interrumpido y no recibirá resultados."
        },
        "english": {
            "pt-BR": "Inglês",
            "en": "English",
            "es": "Inglés"
        },
        "portuguese": {
            "pt-BR": "Português",
            "en": "Portuguese",
            "es": "Portugués"
        },
        "spanish": {
            "pt-BR": "Espanhol",
            "en": "Spanish",
            "es": "Español"
        },
        "results_settings": {
            "pt-BR": "Configurações de Resultados",
            "en": "Results Settings",
            "es": "Configuración de Resultados"
        },
        "how_would_you_like_to_call_this_model": {
            "pt-BR": "Como você gostaria de chamar esse modelo?",
            "en": "What would you like to call this model?",
            "es": "¿Cómo te gustaría llamar a este registro?"
        },
        "settings": {
            "pt-BR": "Configurações",
            "en": "Settings",
            "es": "Ajustes"
        },
        "business_areas": {
            "pt-BR": "Áreas",
            "en": "Business Areas",
            "es": "Departamentos"
        },
        "appearence": {
            "pt-BR": "Aparência",
            "en": "Appearence",
            "es": "Apariencia"
        },
        "do_not_worry": {
            "pt-BR": "Não se preocupe, ",
            "en": "Do not worry, ",
            "es": "No te preocupes, "
        },
        "your_data_is_safe": {
            "pt-BR": " seus dados estão seguros.",
            "en": " your data is safe.",
            "es": " tus datos están a salvo."
        },
        "check_credentials": {
            "pt-BR": "VERIFICAR CREDENCIAIS",
            "en": "CHECK CREDENTIALS",
            "es": "VERIFICAR CREDENCIALES"
        },
        "compatible_with_google_sheets": {
            "pt-BR": "Compatível com Google Sheets*",
            "en": "Compatible with Google Sheets *",
            "es": "Compatible con Google Sheets*"
        },
        "email_to_receive_results": {
            "pt-BR": "E-mail para recebimento de resultados:",
            "en": "E-mail to receive results:",
            "es": "Correo electrónico para recibir los resultados:"
        },
        "you_havent_used_any_solutions_yet": {
            "pt-BR": "Você ainda não utilizou nenhuma solução",
            "en": "You havent used any solutions yet",
            "es": "Aún no has usado ninguna solución."
        },
        "upload": {
            "pt-BR": "Upload",
            "en": "Upload",
            "es": "Subir"
        },
        "credentials": {
            "pt-BR": "Credenciais",
            "en": "Credentials",
            "es": "Credenciales"
        },
        "history": {
            "pt-BR": "Histórico",
            "en": "History",
            "es": "Histórico"
        },
        "filter_notes": {
            "pt-BR": "Filtrar notas",
            "en": "Filter notes",
            "es": "Filtrar notas"
        },
        "use_the_options_on_the_side_to_search_for_all_service_notes_issued_within_the_selected_period": {
            "pt-BR": "Utilize as opções ao lado para buscar todas as notas de serviços emitidas dentro do período selecionado.",
            "en": "Use the options on the side to search for all service notes issued within the selected period.",
            "es": "Use las opciones al costado para buscar todas las notas de servicio disponibles para buscar dentro del período seleccionado."
        },
        "filter_notes_by": {
            "pt-BR": "Filtrar notas por:",
            "en": "Filter notes by:",
            "es": "Filtrar notas por:"
        },
        "period": {
            "pt-BR": "Período",
            "en": "Period",
            "es": "Curso del tiempo"
        },
        "duration": {
            "pt-BR": "Período",
            "en": "Duration",
            "es": "Duración"
        },
        "project_cost": {
            "pt-BR": "Custo do Projeto",
            "en": "Project Cost",
            "es": "Costo del Proyecto"
        },
        "executors": {
            "pt-BR": "Executores",
            "en": "Executors",
            "es": "Albaceas"
        },
        "contributors_capital": {
            "pt-BR": "COLABORADORES",
            "en": "CONTRIBUTORS",
            "es": "CONTRIBUYENTES"
        },
        "amount": {
            "pt-BR": "Quantidade",
            "en": "Amount",
            "es": "La cantidad"
        },
        "average_task_time": {
            "pt-BR": "Tempo médio na tarefa",
            "en": "Average task time",
            "es": "Tiempo promedio en la tarea"
        },
        "average_cost": {
            "pt-BR": "Custo médio",
            "en": "Average cost",
            "es": "Costo promedio"
        },
        "hours_per_day": {
            "pt-BR": "Horas por dia",
            "en": "Hours per day",
            "es": "Horas al dia"
        },
        "informations_came_empty": {
            "pt-BR": "Informações vieram vazias",
            "en": "Informations came empty",
            "es": "Algunas informaciones vino vacía"
        },
        "process_saved_successfully": {
            "pt-BR": "Processo salvo com sucesso",
            "en": "Process saved successfully",
            "es": "Proceso guardado con éxito"
        },
        "unable_to_save_department": {
            "pt-BR": "Não foi possível salvar a área",
            "en": "Unable to save department",
            "es": "No se puede guardar el área"
        },
        "unable_to_save_process": {
            "pt-BR": "Não foi possível salvar o processo",
            "en": "Unable to save process",
            "es": "No se pudo guardar el proceso"
        },
        "client_not_found": {
            "pt-BR": "Cliente não encontrado",
            "en": "Client not found",
            "es": "Cliente no encontrado"
        },
        "are_you_sure_this_is_your_account": {
            "pt-BR": "Tem certeza que essa é sua conta?",
            "en": "Are you sure this is your account?",
            "es": "¿Estás seguro de que esta es tu cuenta?"
        },
        "department_removed_successfully": {
            "pt-BR": "Área removida com sucesso",
            "en": "Department removed successfully",
            "es": "Departamento eliminado con éxito"
        },
        "department_not_found": {
            "pt-BR": "Área não foi encontrada",
            "en": "Department not found",
            "es": "Departamento no encontrado"
        },
        "department_saved_successfully": {
            "pt-BR": "Área salva com sucesso",
            "en": "Department saved successfully",
            "es": "Departamento guardado con éxito"
        },
        "processes_history": {
            "pt-BR": "Histórico de Processos",
            "en": "Processes History",
            "es": "Historial de Procesos"
        },
        "manage_licenses": {
            "pt-BR": "Gerenciar Licenças",
            "en": "Manage Licenses",
            "es": "Administrar Licencias"
        },
        "do_upgrade": {
            "pt-BR": "Fazer Upgrade",
            "en": "Upgrade",
            "es": "Ascender de Categoría"
        },
        "all_rights_reserved": {
            "pt-BR": "Todos os direitos reservados",
            "en": "All rights reserved",
            "es": "Todos los derechos reservados"
        },
        "in_execution": {
            "pt-BR": "Em execução",
            "en": "In execution",
            "es": "En ejecución"
        },
        "finished_with_success": {
            "pt-BR": "Finalizado com sucesso",
            "en": "Successfully completed",
            "es": "Completado con éxito"
        },
        "finished_with_error": {
            "pt-BR": "Erro!",
            "en": "Error!",
            "es": "¡Error!"
        },
        "execution_edited_successfully": {
            "pt-BR": "Modelo editado com sucesso",
            "en": "Successfully edited template",
            "es": "Registro editada con éxito"
        },
        "automation_not_found": {
            "pt-BR": "Automação não encontrada",
            "en": "Automation not found",
            "es": "Automatización no encontrada"
        },
        "it_was_not_possible_to_update_the_credential_in_previous_configuration": {
            "pt-BR": "Não foi possivel atualizar a credencial na configuração anterior",
            "en": "It was not possible to update the credential in previous configuration",
            "es": "No se puede actualizar la credencial en la configuración anterior"
        },
        "it_was_not_possible_to_remove_file_in_previous_configuration": {
            "pt-BR": "Não foi possivel remover o arquivo, na configuração anterior",
            "en": "It was not possible to remove file, in previous configuration",
            "es": "No se puede eliminar el archivo, en la configuración anterior"
        },
        "the_credential_related_to_this_execution_wasnt_found": {
            "pt-BR": "Não foi encontrada a credencial relacionada a essa utilização",
            "en": "The credential related to this execution wasn`t found",
            "es": "No se encontró la credencial relacionada con este uso"
        },
        "execution_with_that_name_already_exists": {
            "pt-BR": "Já existe utilização com esse nome",
            "en": "Execution with that name already exists",
            "es": "Ya se usa con ese nombre."
        },
        "execution_with_that_name_already_exists_related_to_your_user": {
            "pt-BR": "Já existe uma utilização com esse nome relacionada ao seu usuário",
            "en": "Execution with that name already exists related to your user",
            "es": "Ya existe un uso con ese nombre relacionado con tu usuario"
        },
        "could_not_save_execution": {
            "pt-BR": "Não foi possível salvar a utilização",
            "en": "Could not save execution",
            "es": "No se puede guardar el uso"
        },
        "we_were_unable_to_remove_your_old_file_please_try_again": {
            "pt-BR": "Não foi possível remover seu antigo arquivo, por favor tente novamente",
            "en": "We were unable to remove your old file, please try again",
            "es": "No se pudo eliminar el archivo antiguo, inténtalo de nuevo"
        },
        "error_saving_information": {
            "pt-BR": "Erro salvando informações",
            "en": "Error saving information",
            "es": "Error al guardar informaciones"
        },
        "unable_to_remove_execution_please_try_again": {
            "pt-BR": "Não foi possível remover a utilização, por favor tente novamente",
            "en": "Unable to remove execution, please try again",
            "es": "No se puede eliminar el uso, inténtalo de nuevo"
        },
        "execution_removed_successfully": {
            "pt-BR": "Modelo removido com sucesso",
            "en": "Model successfully removed",
            "es": "Registro eliminado con éxito"
        },
        "unable_to_remove_file_please_try_again": {
            "pt-BR": "Não foi possível remover o arquivo, por favor tente novamente",
            "en": "Unable to remove file, please try again",
            "es": "No se puede eliminar el archivo, inténtalo de nuevo"
        },
        "unable_to_update_credentials_please_try_again": {
            "pt-BR": "Não foi possível atualizar as credenciais, por favor tente novamente",
            "en": "Unable to update credentials, please try again",
            "es": "No se pueden actualizar las credenciales, inténtelo de nuevo"
        },
        "unable_to_start_execution_please_try_again": {
            "pt-BR": "Não foi possível iniciar a utilização, por favor tente novamente",
            "en": "Unable to start execution, please try again",
            "es": "No se puede comenzar a usar, inténtalo de nuevo"
        },
        "execution_started": {
            "pt-BR": "Utilização iniciada",
            "en": "Execution started",
            "es": "Uso iniciado"
        },
        "unable_to_cancel_execution_please_try_again": {
            "pt-BR": "Não foi possível cancelar a utilização, por favor tente novamente",
            "en": "Unable to cancel execution please try again",
            "es": "No se puede cancelar la suscripción, inténtalo de nuevo"
        },
        "execution_canceled": {
            "pt-BR": "Utilização cancelada",
            "en": "Execution canceled",
            "es": "Uso cancelado"
        },
        "unable_to_update_credential_in_previous_configuration": {
            "pt-BR": "Não foi possivel atualizar a credencial na configuração anterior",
            "en": "Unable to update credential in previous configuration",
            "es": "No se puede actualizar la credencial en la configuración anterior"
        },
        "execution_created_successfully": {
            "pt-BR": "Utilização criada com sucesso",
            "en": "Execution created successfully",
            "es": "Uso creado con éxito"
        },
        "error_saving_credentials": {
            "pt-BR": "Erro salvando credenciais",
            "en": "Error saving credentials",
            "es": "Error al guardar las credenciales"
        },
        "error_saving_new_credential": {
            "pt-BR": "Erro ao salvar nova credencial",
            "en": "Error saving new credential",
            "es": "Error al guardar nueva credencial"
        },
        "automation_is_not_classified": {
            "pt-BR": "A automação não está classificada",
            "en": "Automation is not classified",
            "es": "La automatización no está clasificada"
        },
        "licenses": {
            "pt-BR": "licenças",
            "en": "licenses",
            "es": "licencias"
        },
        "licenses_first_capital": {
            "pt-BR": "Licenças",
            "en": "Licenses",
            "es": "Licencias"
        },
        "solution": {
            "pt-BR": "Solução",
            "en": "Solution",
            "es": "Solución"
        },
        "you_have_no_licenses_available": {
            "pt-BR": "Você não possui licenças disponíveis.",
            "en": "You have no licenses available.",
            "es": "No tienes licencias disponibles."
        },
        "to_use_this_solution_manage_your_licenses_or_upgrade_the_plan": {
            "pt-BR": "Para utilizar esta solução, gerencie suas licenças ou faça upgrade do plano",
            "en": "To use this solution, manage your licenses or upgrade the plan",
            "es": "Para usar esta solución, administre sus licencias o actualice su plan"
        },
        "filter_by": {
            "pt-BR": "Filtrar por:",
            "en": "Filter by:",
            "es": "Filtrar por:"
        },
        "same_login_used_on_enel_website": {
            "pt-BR": "Mesmo login utilizado no site da Enel",
            "en": "Same login used on Enel website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Enel"
        },
        "same_password_used_on_enel_website": {
            "pt-BR": "Mesma senha utilizada no site da Enel",
            "en": "Same password used on the Enel website",
            "es": "Misma contraseña utilizada en el sitio web de Enel"
        },
        "same_login_used_on_copasa_website": {
            "pt-BR": "Mesmo login utilizado no site da Copasa",
            "en": "Same login used on Copasa website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Copasa"
        },
        "same_password_used_on_copasa_website": {
            "pt-BR": "Mesma senha utilizada no site da Copasa",
            "en": "Same password used on the Copasa website",
            "es": "Misma contraseña utilizada en el sitio web de Copasa"
        },
        "same_login_used_on_vivo_website": {
            "pt-BR": "Mesmo login utilizado no site da Vivo",
            "en": "Same login used on Vivo website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Vivo"
        },
        "same_password_used_on_vivo_website": {
            "pt-BR": "Mesma senha utilizada no site da Vivo",
            "en": "Same password used on the Vivo website",
            "es": "Misma contraseña utilizada en el sitio web de Vivo"
        },
        "same_login_used_on_light_website": {
            "pt-BR": "Mesmo login utilizado no site da Light",
            "en": "Same login used on Light website",
            "es": "El mismo acceso utilizado en el sitio web de Light"
        },
        "same_password_used_on_light_website": {
            "pt-BR": "Mesma senha utilizada no site da Light",
            "en": "Same password used on the Light website",
            "es": "Misma contraseña utilizada en el sitio web de Light"
        },
        "same_login_used_on_claro_website": {
            "pt-BR": "Mesmo login utilizado no site da Claro",
            "en": "Same login used on Claro website",
            "es": "El mismo acceso utilizado en el sitio web de Claro"
        },
        "same_password_used_on_claro_website": {
            "pt-BR": "Mesma senha utilizada no site da Claro",
            "en": "Same password used on the Claro website",
            "es": "Misma contraseña utilizada en el sitio web de Claro"
        },
        "same_login_used_on_nota_carioca_website": {
            "pt-BR": "Mesmo login utilizado no site da Nota Carioca",
            "en": "Same login used on Nota Carioca website",
            "es": "El mismo acceso utilizado en el sitio web de Nota Carioca"
        },
        "same_password_used_on_nota_carioca_website": {
            "pt-BR": "Mesma senha utilizada no site da Nota Carioca",
            "en": "Same password used on the Nota Carioca website",
            "es": "Misma contraseña utilizada en el sitio web de Nota Carioca"
        },
        "same_login_used_on_the_sao_paulo_city_hall_website": {
            "pt-BR": "Mesmo login utilizado no site da Prefeitura de São Paulo",
            "en": "Same login used on the São Paulo City Hall website",
            "es": "Mismo acceso utilizado en el sitio web del Ayuntamiento de São Paulo"
        },
        "same_password_used_on_the_sao_paulo_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de São Paulo",
            "en": "Same password used on the São Paulo City Hall website",
            "es": "Misma contraseña utilizada en el sitio web del Ayuntamiento de São Paulo"
        },
        "same_password_used_on_the_ipojuca_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura do Ipojuca",
            "en": "Same password used on the Ipojuca City Hall website",
            "es": "Misma contraseña utilizada en el sitio web del Ayuntamiento de Ipojuca"
        },
        "same_cpf_cnpj_used_on_the_ipojuca_city_hall_website": {
            "pt-BR": "Mesmo CPF/CNPJ utilizado no site da Prefeitura do Ipojuca",
            "en": "Same CPF/CNPJ used on the Ipojuca City Hall website",
            "es": "Mismo CPF/CNPJ utilizado en el sitio web del Ayuntamiento de Ipojuca"
        },
        "same_ccm_used_on_the_rio_grande_city_hall_website": {
            "pt-BR": "Mesmo CCM utilizado no site da Prefeitura De Rio Grande",
            "en": "Same CCM used on the Rio Grande City Hall website.",
            "es": "Mismo CCM utilizado en el sitio web del Ayuntamiento de Río Grande"
        },
        "same_password_used_on_the_website_of_the_municipality_of_rio_grande": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura De Rio Grande.",
            "en": "Same password used on the website of the Municipality of Rio Grande.",
            "es": "Misma contraseña utilizada en el sitio web del Ayuntamiento de Rio Grande."
        },
        "same_cpf_used_on_the_website_of_the_municipality_of_barcarena": {
            "pt-BR": "Mesmo CPF utilizado no site da Prefeitura de Barcarena",
            "en": "Same CPF used on the website of the Municipality of Barcarena",
            "es": "Mismo CPF utilizado en la web del Ayuntamiento de Barcarena"
        },
        "same_password_used_on_the_website_of_the_municipality_of_barcarena": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Barcarena",
            "en": "Same password used on the website of the Municipality of Barcarena",
            "es": "Misma contraseña utilizada en la web del Ayuntamiento de Barcarena"
        },
        "same_cpf_used_on_the_website_of_the_municipality_of_oriximina": {
            "pt-BR": "Mesmo CPF utilizado no site da Prefeitura de Oriximiná",
            "en": "Same CPF used on the website of the Municipality of Oriximiná",
            "es": "Mismo CPF utilizado en el sitio web del Ayuntamiento de Oriximiná"
        },
        "same_password_used_on_the_website_of_the_municipality_of_oriximina": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Oriximiná",
            "en": "Same password used on the website of the Municipality of Oriximiná",
            "es": "Misma contraseña utilizada en el sitio web del Ayuntamiento de Oriximiná"
        },
        "same_user_used_on_the_sefaz_rio_de_janeiro_website": {
            "pt-BR": "Mesmo usuário utilizado no site da Sefaz Rio de Janeiro",
            "en": "Same user used on the Sefaz Rio de Janeiro website",
            "es": "Mismo usuario utilizado en el sitio web de Sefaz Rio de Janeiro"
        },
        "same_password_used_on_the_sefaz_rio_de_janeiro_website": {
            "pt-BR": "Mesma senha utilizada no site da Sefaz Rio de Janeiro",
            "en": "Same password used on the Sefaz Rio de Janeiro website",
            "es": "Misma contraseña utilizada en el sitio web de Sefaz Rio de Janeiro"
        },
        "enel_credentials": {
            "pt-BR": "Credenciais da Enel",
            "en": "Enel Credentials",
            "es": "Credenciales Enel"
        },
        "credentials_of_the_city_hall_of_oriximina": {
            "pt-BR": "Credenciais da Prefeitura de Oriximiná",
            "en": "Credentials of the City Hall of Oriximiná",
            "es": "Credenciales del Ayuntamiento de Oriximiná"
        },
        "barcarena_city_hall_credentials": {
            "pt-BR": "Credenciais da Prefeitura de Barcarena",
            "en": "Barcarena City Hall Credentials",
            "es": "Credenciales del Ayuntamiento de Barcarena"
        },
        "ipojuca_city_hall_credentials": {
            "pt-BR": "Credenciais da Prefeitura do Ipojuca",
            "en": "Ipojuca City Hall Credentials",
            "es": "Credenciales del Ayuntamiento de Ipojuca"
        },
        "credentials_city_hall_of_rio_grande": {
            "pt-BR": "Credenciais Prefeitura De Rio Grande",
            "en": "Credentials City Hall of Rio Grande",
            "es": "Credenciales del Ayuntamiento de Rio Grande"
        },
        "vivo_credentials": {
            "pt-BR": "Credenciais da Vivo",
            "en": "Vivo Credentials",
            "es": "Credenciales Vivo"
        },
        "light_credentials": {
            "pt-BR": "Credenciais da Light",
            "en": "Light Credentials",
            "es": "Credenciales Light"
        },
        "claro_credentials": {
            "pt-BR": "Credenciais da Claro",
            "en": "Claro Credentials",
            "es": "Credenciales Claro"
        },
        "credentials_nota_carioca": {
            "pt-BR": "Credenciais Nota Carioca",
            "en": "Credentials Nota Carioca",
            "es": "Credenciales Nota Carioca"
        },
        "credentials_city_hall_sp": {
            "pt-BR": "Credenciais Prefeitura São Paulo",
            "en": "Credentials São Paulo City Hall",
            "es": "Credenciales Ayuntamiento de São Paulo"
        },
        "omie_credentials": {
            "pt-BR": "Credenciais da OMIE",
            "en": "OMIE Credentials",
            "es": "Credenciales OMIE"
        },
        "see_all_capital": {
            "pt-BR": "VER TODOS",
            "en": "SEE ALL",
            "es": "VER TODO"
        },
        "name": {
            "pt-BR": "Nome",
            "en": "Name",
            "es": "Nombre"
        },
        "occupation_department": {
            "pt-BR": "Área de atuação",
            "en": "Occupation department",
            "es": "Área de actuación"
        },
        "job_title": {
            "pt-BR": "Cargo",
            "en": "Job title",
            "es": "Oficina"
        },
        "choose_department": {
            "pt-BR": "Escolher área",
            "en": "Choose department",
            "es": "Eligir departamento"
        },
        "select_position": {
            "pt-BR": "Selecione Cargo",
            "en": "Select Position",
            "es": "Seleccionar Posición"
        },
        "password": {
            "pt-BR": "Senha",
            "en": "Password",
            "es": "Clave"
        },
        "rpa_dashboard": {
            "pt-BR": "Dashboard de RPA",
            "en": "RPA Dashboard",
            "es": "Tablero RPA"
        },
        "manage_your_rpa_operation": {
            "pt-BR": "Faça gestão da sua operação RPA UiPath com o Dashboard de RPA Smarthis Hub.",
            "en": "Manage your UiPath RPA operation with the Smarthis Hub RPA Dashboard.",
            "es": "Administre su operación RPA UiPath con Smarthis Hub RPA Dashboard."
        },
        "track_and_compare_your_robots": {
            "pt-BR": "Acompanhe e compare seus robôs e processos por períodos, áreas e mais, tirando insights valiosos para o seu negócio.",
            "en": "Track and compare your robots and processes by periods, departments and more, gaining valuable insights for your business.",
            "es": "Rastree y compare sus robots y procesos por períodos, departamentos y más, obteniendo información valiosa para su negocio."
        },
        "rpa_dashboard_can_be_added": {
            "pt-BR": "O dashboard de RPA pode ser adicionado ao seu pacote sem custos extras, apenas consumindo 01 licença.",
            "en": "The RPA dashboard can be added to your package at no extra cost, just consuming 01 license.",
            "es": "El panel de RPA se puede agregar a su paquete sin costo adicional, solo consumiendo 01 licencia."
        },
        "add_to_my_plan": {
            "pt-BR": "Adicionar ao Meu Plano",
            "en": "Add to My Plan",
            "es": "Agregar a mi plan"
        },
        "uipath_operations_are_required": {
            "pt-BR": "*É necessário possuir operações com UiPath para utilzar essa solução.",
            "en": "*UiPath operations are required to use this solution.",
            "es": "*Es necesario tener operaciones con UiPath para utilizar esta solución"
        },
        "financial_accounting": {
            "pt-BR": "Financeiro/Contábil",
            "en": "Financial/Accounting",
            "es": "Financiero/Contabilidad"
        },
        "legal": {
            "pt-BR": "Jurídico",
            "en": "Legal",
            "es": "Legal"
        },
        "see_more": {
            "pt-BR": "ver mais",
            "en": "show more",
            "es": "ver más"
        },
        "license": {
            "pt-BR": "licença",
            "en": "license",
            "es": "licencia"
        },
        "executed_on": {
            "pt-BR": "Executado em",
            "en": "Executed on",
            "es": "Realizado en"
        },
        "help": {
            "pt-BR": "Ajuda",
            "en": "Help",
            "es": "Ayuda"
        },
        "discover": {
            "pt-BR": "Descobrir",
            "en": "Discover",
            "es": "Descubrir"
        },
        "energy": {
            "pt-BR": "Energia",
            "en": "Energy",
            "es": "Energía"
        },
        "gas": {
            "pt-BR": "Gás",
            "en": "Gas",
            "es": "Gas"
        },
        "sanitation_water": {
            "pt-BR": "Saneamento/Água",
            "en": "Sanitation/Water",
            "es": "Saneamiento/Agua"
        },
        "telephony": {
            "pt-BR": "Telefonia",
            "en": "Telephony",
            "es": "Telefonía"
        },
        "hire": {
            "pt-BR": "Contratar",
            "en": "Hire",
            "es": "Contratar"
        },
        "learn_more": {
            "pt-BR": "Saiba Mais",
            "en": "Learn More",
            "es": "Aprende Más"
        },
        "know_more": {
            "pt-BR": "Saiba mais",
            "en": "Know more",
            "es": "Sepa mas"
        },
        "here": {
            "pt-BR": "aqui",
            "en": "here",
            "es": "aquí"
        },
        "discover_services": {
            "pt-BR": "Descubra serviços",
            "en": "Discover services",
            "es": "Descubre servicios"
        },
        "to_boost": {
            "pt-BR": "para impulsionar o seu",
            "en": "to boost your",
            "es": "para impulsar tu"
        },
        "work": {
            "pt-BR": "trabalho",
            "en": "work",
            "es": "trabajo"
        },
        "discover_services_available": {
            "pt-BR": "Conheça os serviços disponíveis e fique por dentro dos que estão por vir",
            "en": "Discover the services available and stay on top of the ones to come",
            "es": "Descubra los servicios disponibles y manténgase al tanto de los que están por venir"
        },
        "did_not_find": {
            "pt-BR": "Não encontrou o que buscava?",
            "en": "Did not find what you were looking for?",
            "es": "¿No has encontrado lo que estabas buscando?"
        },
        "always_working_new_services": {
            "pt-BR": "Estamos sempre trabalhando em serviços novos e gostaríamos de ouvir você.",
            "en": "We are always working on new services and would love to hear from you.",
            "es": "Siempre estamos trabajando en nuevos servicios y nos encantaría saber de usted."
        },
        "leave_suggestion": {
            "pt-BR": "Deixar uma sugestão",
            "en": "Leave a suggestion",
            "es": "Deja una sugerencia"
        },
        "coming_soon": {
            "pt-BR": "Em breve",
            "en": "Coming soon",
            "es": "Proximamente"
        },
        "more_services_to_come": {
            "pt-BR": "Mais serviços estão por vir. Clique em “Avise-me” e receba notícias do lançamento.",
            "en": "More services are to come. Click on \"Notify me\" and receive news of the launch.",
            "es": "Más servicios están por venir. Haga clic en \"Notificarme\" y reciba noticias del lanzamiento."
        },
        "warn_me": {
            "pt-BR": "Avise-me",
            "en": "Warn me",
            "es": "Advierteme"
        },
        "subject": {
            "pt-BR": "Assunto",
            "en": "Subject",
            "es": "Tema en cuestion"
        },
        "message": {
            "pt-BR": "Mensagem",
            "en": "Message",
            "es": "mensaje"
        },
        "write_a_message_send_question": {
            "pt-BR": "Escreva uma mensagem para poder enviar sua dúvida.",
            "en": "Write a message so you can send your question.",
            "es": "Escribe un mensaje para poder enviar tu consulta."
        },
        "send_question": {
            "pt-BR": "Enviar dúvida",
            "en": "Send question",
            "es": "Enviar pregunta"
        },
        "shopee_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os termos de pesquisa e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the search keywords and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los términos de búsqueda y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "cpom_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CNPJs e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJs and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los CNPJ y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "rg_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os RGs e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the RGs and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los RG y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "cpom_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre o cadastro e os códigos dos serviços registrados pelas empresas consultadas.",
            "en": "After using the service, the results arrive by e-mail with information about the registration and the codes of the services registered by the consulted companies.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre el registro y los códigos de servicio registrados por las empresas consultadas."
        },
        "simples_nacional_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com informações sobre o contribuinte, situação no Simples Nacional, no SIMEI, períodos anteriores e futuros e o comprovantes.",
            "en": "After using the service, the results arrive by e-mail, with information about the taxpayer, status at Simples Nacional, at SIMEI, previous and future periods and vouchers.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con información sobre el contribuyente, estado en Simples Nacional, SIMEI, períodos anteriores y futuros y recibos."
        },
        "cpf_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CPFs que deseja consultar para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You populate the upload file with the CPFs you want to look up to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida con los CPF que quieres consultar para configurar un registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "cpf_cnpj_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações solicitadas.",
            "en": "After using the service, the results arrive by email with the requested information.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con la información solicitada."
        },
        "cnpj_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CNPJs que deseja consultar para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJs you want to consult to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el fichero de subida con los CNPJ que quieres consultar para configurar un modelo. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "nfe_sp_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CNPJs dos prestadores de serviço e número das notas que deseja realizar download para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJs of the service providers and the number of notes you want to download to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida con los CNPJs de los proveedores de servicios y el número de las notas que quieres descargar para configurar un registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "nfe_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com informações sobre o CNPJ e suas respectivas NFS-e.",
            "en": "After using the service, the results arrive by email with information about the CNPJ and their respective NFS-e.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre el CNPJ y su respectivo NFS-e."
        },
        "nfe_rj_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do Nota Carioca para buscar por todas as NFS-e emitidas em um período ou por notas específicas preenchendo um arquivo de entrada com as informações necessárias.",
            "en": "With a few clicks, you configure a template with your Nota Carioca credentials to search for all NFS-e issued in a period or for specific notes by filling an input file with the necessary information.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales de Nota Carioca para buscar todos los NFS-e emitidos en un período o notas específicas llenando un archivo de entrada con la información necesaria."
        },
        "enel_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da Enel e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials from the Enel website and can reuse it whenever you need it.",
            "es": "Con unos pocos clics configuras un registro con tus credenciales desde la web de Enel y puedes reutilizarla cuando lo necesites."
        },
        "enel_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com as contas e informações sobre valor, período de referência, apelido da instalação.",
            "en": "After using the service, the results arrive by email, with the bills and information about value, reference period, nickname of the installation.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con las facturas e información sobre valor, período de referencia, apodo de la instalación."
        },
        "light_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da Light e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your Light website credentials and can reuse it whenever you need it.",
            "es": "Con unos pocos clics, configura un registro con las credenciales de su sitio web Light y puede reutilizarla cuando lo necesite."
        },
        "light_sabesp_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com as contas e informações sobre valor, período de referência, endereço.",
            "en": "After using the service, the results arrive by email, with accounts and information about value, reference period, address.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con las facturas e información sobre valor, período de referencia, dirección."
        },
        "sabesp_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os RGIs e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You populate the upload file with the RGIs and set up a template that is saved to reuse whenever you need to.",
            "es": "Llena el archivo de carga con los RGI y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "comgas_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload (com os CPF e códigos dos usuários) e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file (with the CPF and user codes) and set up a template that is saved to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida (con el CPF y los códigos de usuario) y configuras un registro que se guarda para reutilizarla cuando la necesites."
        },
        "comgas_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com informações sobre data de vencimento, status da conta, período vigente e os boletos a serem pagos.",
            "en": "After using the service, the results arrive by email, with information on the expiration date, account status, current period and the payment slips to be paid.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con información sobre la fecha de vencimiento, el estado de la cuenta, el período actual y las facturas a pagar."
        },
        "vivo_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais no site da Vivo e o reutiliza sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials on the Vivo website and reuse it whenever you need it.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales en el sitio web de Vivo y la reutiliza cuando lo necesite."
        },
        "telephony_ipva_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com informações sobre os débitos, vencimentos e seus respectivos boletos.",
            "en": "After using the service, the results arrive by email, with information about debts, maturities and their respective bills.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con información sobre deudas, vencimientos y sus respectivos recibos."
        },
        "claro_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais no site da Claro e o reutiliza sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials on Claro's website and reuse it whenever you need it.",
            "es": "Con unos pocos clics, configuras un registro con tus credenciales en el sitio web de Claro y la reutilizas cuando lo necesitas."
        },
        "ipva_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os RENAVAMs e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill the upload file with the RENAVAMs and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los RENAVAM y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "cpf_trf2_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CPFs que deseja consultar no TRF2 para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You populate the upload file with the CPFs you want to look up in TRF2 to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida con los CPF que quieres consultar en TRF2 para configurar un registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "cpf_trf_inidoneos_cnd_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre as certidões e seus respectivos arquivos.",
            "en": "After using the service, the results arrive by email with information about the certificates and their respective files.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los certificados y sus respectivos archivos."
        },
        "rg_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre os RGs e seus respectivos arquivos.",
            "en": "After using the service, the results arrive by email with information about the RGs and their respective files.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los RGs y sus respectivos archivos."
        },
        "cpf_trf3_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com o CPF e nome completo que deseja realizar a consulta da certidão no TRF3 para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CPF and full name you want to query the certificate in TRF3 to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el fichero de subida con el CPF y nombre completo que quieres consultar el certificado en TRF3 para configurar un modelo. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "inidoneos_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com o CNPJ que deseja realizar a emissão da Certidão de Inidôneos para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJ that you want to issue the Certificate of Disability to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con el CNPJ que desea emitir el Certificado de Inidôneos para configurar un modelo. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "cnd_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com o CNPJ da matriz que deseja realizar a emissão da Certidão de Negativa para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJ of the head office that you want to issue the Certificate of Clearance to configure a model. This information is saved for you to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida con el CNPJ de la casa matriz a la que quieres emitir un Certificado de Autorización para configurar un modelo. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "gnre_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com as informações das NFS-e necessárias e configura um modelo que fica pronto para ser utilizado.",
            "en": "You populate the upload file with the necessary NFS-e information and set up a template that is ready to use.",
            "es": "Rellena el archivo de carga con la información NFS-e necesaria y configura un registro que está lista para usar."
        },
        "gnre_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, de acordo com o modelo que você configurou. Nele você encontra as guias e informações sobre inscrição estadual, período de referência, vencimento, juros, etc..",
            "en": "After using the service, the results arrive by email, according to the template you have configured. In it you will find guides and information about state registration, reference period, maturity, interest, etc..",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, según el modelo que haya configurado. En él encontrarás guías e información sobre registro estatal, periodo de referencia, vencimiento, interés, etc.."
        },
        "icms_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com as informações necessárias e configura um modelo que fica pronto para ser utilizado.",
            "en": "You populate the upload file with the necessary information and set up a template that is ready to use.",
            "es": "Rellenas el archivo de subida con la información necesaria y configuras un registro que está lista para usar."
        },
        "icms_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, de acordo com o modelo que você configurou. Nele você encontra as guias e informações sobre inscrição estadual, período de referência, vencimento, juros, etc..",
            "en": "After using the service, the results arrive by email, according to the template you have configured. In it you will find guides and information about state registration, reference period, maturity, interest, etc..",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, según el modelo que haya configurado. En él encontrarás guías e información sobre registro estatal, periodo de referencia, vencimiento, interés, etc.."
        },
        "content_not_available": {
            "pt-BR": "Conteúdo temporariamente indisponível. Tente novamente mais tarde ou entre em contato por",
            "en": "Content temporarily unavailable. Please try again later or contact us via",
            "es": "Contenido temporalmente no disponible. Vuelva a intentarlo más tarde o contáctenos por"
        },
        "doubts": {
            "pt-BR": "Dúvidas",
            "en": "Doubts",
            "es": "Dudas"
        },
        "any_doubt_about_hub": {
            "pt-BR": "Tem alguma dúvida sobre esse serviço ou o Hub",
            "en": "Do you have any questions about this service or the Hub",
            "es": "Tiene una pregunta sobre este servicio o el Hub"
        },
        "contact_us_we_will_help": {
            "pt-BR": "Entre em contato, que iremos ajudar",
            "en": "Get in touch, we will help",
            "es": "Ponte en contacto, te ayudaremos"
        },
        "contact_us": {
            "pt-BR": "Entrar em Contato",
            "en": "Get in touch",
            "es": "Entrar en contacto"
        },
        "how_does_it_works": {
            "pt-BR": "Como funciona?",
            "en": "How it works?",
            "es": "¿Como funciona?"
        },
        "fill_upload_file": {
            "pt-BR": "Preencha o arquivo de upload",
            "en": "Fill in the upload file",
            "es": "Rellene el archivo de carga"
        },
        "fill_upload_file_if_necessary": {
            "pt-BR": "Preencha o arquivo de upload se necessário",
            "en": "Fill in the upload file if necessary",
            "es": "Complete el archivo de carga si es necesario"
        },
        "set_up_reusable_template": {
            "pt-BR": "Configure um modelo reutilizável",
            "en": "Set up a reusable template",
            "es": "Configurar un registro reutilizable"
        },
        "set_up_template": {
            "pt-BR": "Configure um modelo",
            "en": "Set up a template",
            "es": "configurar una registro"
        },
        "use_the_template_one_click": {
            "pt-BR": "Use o modelo com apenas um clique",
            "en": "Use the template with only oneclick",
            "es": "Utilice el registro con un solo clic"
        },
        "receive_results_by_email": {
            "pt-BR": "Receba os resultados por e-mail",
            "en": "Receive results by email",
            "es": "Recibir resultados por correo electrónico"
        },
        "save_time_advantages_1": {
            "pt-BR": "Economize tempo",
            "en": "Save time",
            "es": "Ahorrar tiempo"
        },
        "avoid_mistakes_rework_advantages_2": {
            "pt-BR": "Evite erros e retrabalhos",
            "en": "Avoid mistakes and rework",
            "es": "Evite errores y reelaboraciones"
        },
        "get_all_results_in_one_place_advantages_3": {
            "pt-BR": "Receba todos resultados em um só lugar",
            "en": "Get all results in one place",
            "es": "Obtenga todos los resultados en un solo lugar"
        },
        "get_all_guides_in_one_place_advantages_3": {
            "pt-BR": "Receba todas as guias em um só lugar",
            "en": "Get all guides in one place",
            "es": "Reciba todas las guías en un solo lugar"
        },
        "avoid_delays_and_fines_advantages_2": {
            "pt-BR": "Evite atrasos e multas",
            "en": "Avoid delays and fines",
            "es": "Evita retrasos y multas"
        },
        "regularize_your_situation_advantages_2": {
            "pt-BR": "Regularize sua situação",
            "en": "Regularize your situation",
            "es": "Regulariza tu situación"
        },
        "get_all_your_bills_in_one_place_advantages_3": {
            "pt-BR": "Receba todas as contas em um só lugar",
            "en": "Get all your bills in one place",
            "es": "Obtenga todas sus facturas en un solo lugar"
        },
        "avoid_delays_cuts_and_fines": {
            "pt-BR": "Evite atrasos, cortes e multas",
            "en": "Avoid delays, cuts and fines",
            "es": "Evita retrasos, cortes y multas"
        },
        "receive_all_information_and_tickets_in_one_place": {
            "pt-BR": "Receba todas as informações e boletos em um só lugar",
            "en": "Receive all information and tickets in one place",
            "es": "Recibe toda la información y entradas en un solo lugar"
        },
        "there_is_already_an_email_for_this_user": {
            "pt-BR": "Já existe um e-mail para esse usuário",
            "en": "There is already an email for this user",
            "es": "Ya existe un correo electrónico para este usuario"
        },
        "there_is_already_an_email_for_this_invite": {
            "pt-BR": "Já existe um e-mail para esse convidado",
            "en": "There is already an email for this invite",
            "es": "Ya existe un correo electrónico para este invitado"
        },
        "add_email": {
            "pt-BR": "Adicionar E-mail",
            "en": "Add Email",
            "es": "Agregar correo"
        },
        "there_was_a_problem_encrypting_your_file": {
            "pt-BR": "Houve um problema ao encriptar seu arquivo",
            "en": "There was a problem encrypting your file",
            "es": "Hubo un problema al encriptar su archivo"
        },
        "problem_deleting_old_licenses": {
            "pt-BR": "Problema ao deletar antigas licenças",
            "en": "Problem deleting old licenses",
            "es": "Problema al eliminar licencias antiguas"
        },
        "licenses_reset_successfully": {
            "pt-BR": "licenças resetadas com sucesso",
            "en": "licenses reset successfully",
            "es": "reinicio de licencias con éxito"
        },
        "in_the_annual_plan_or_starter_in_the_monthly_plan": {
            "pt-BR": "Ou 1x de R$ 2.999,90 no plano anual, desconto equivalente à 2 meses grátis",
            "en": "Or 1x of R$ 2,999.90 in the annual plan, discount equivalent to 2 free months",
            "es": "O 1x de R$ 2.999,90 en el plan anual, descuento equivalente a 2 meses gratis"
        },
        "in_the_annual_plan_or_399_in_the_monthly_plan": {
            "pt-BR": "Ou 1x de R$ 6.499,90 no plano anual, desconto equivalente à 2 meses grátis",
            "en": "Or 1x of R$ 6,499.90 in the annual plan, discount equivalent to 2 free months",
            "es": "O 1x de R$ 6.499,90 en el plan anual, descuento equivalente a 2 meses gratis"
        },
        "in_the_annual_plan_or_599_in_the_monthly_plan": {
            "pt-BR": "Ou 1x de R$ 34.999,90 no plano anual, desconto equivalente à 2 meses grátis",
            "en": "Or 1x of R$ 34,999.90 in the annual plan, discount equivalent to 2 free months",
            "es": "O 1x de R$ 34.999,90 en el plan anual, descuento equivalente a 2 meses gratis"
        },
        "up_to": {
            "pt-BR": "Até",
            "en": "Up to",
            "es": "Hasta"
        },
        "monthly_consultation": {
            "pt-BR": "consultas mensais nos serviços contratados",
            "en": "monthly consultations on contracted services",
            "es": "consultas mensuales sobre los servicios contratados"
        },
        "unlimited_consultations_on_services_contracted": {
            "pt-BR": "Consultas mensais ilimitadas nos serviços contratados",
            "en": "Unlimited consultations on services contracted",
            "es": "Consultas mensuales ilimitadas sobre los servicios contratados"
        },
        "register_your_team": {
            "pt-BR": "Cadastre sua equipe",
            "en": "Register your team",
            "es": "Registra tu equipo"
        },
        "maintenance_and_updates_on_our_own": {
            "pt-BR": "Manutenção e Atualizações por nossa conta",
            "en": "Maintenance and Updates on our own",
            "es": "Mantenimiento y actualizaciones sobre nosotros"
        },
        "pay_with_more_than_one_card": {
            "pt-BR": "Pague com mais de um cartão",
            "en": "Pay with more than one card",
            "es": "Paga con más de una tarjeta"
        },
        "best_value_for_money": {
            "pt-BR": "Melhor custo benefício",
            "en": "Best value for money",
            "es": "Mejor relación calidad-precio"
        },
        "month": {
            "pt-BR": "mês",
            "en": "month",
            "es": "mes"
        },
        "divida_ativa_rj_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload (com o CNPJ e informações sobre a guia de pagamento) e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file (with CNPJ and payment slip information) and set up a template that is saved to reuse whenever you need it.",
            "es": "Rellenas el archivo de subida (con el CNPJ e información sobre el comprobante de pago) y configuras una registro que se guarda para reutilizar cuando lo necesites."
        },
        "divida_ativa_rj_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com informações sobre ano de exercício, situação, cotas de pagamento e seus respectivos boletos.",
            "en": "After using the service, the results arrive by email, with information on the year of exercise, status, payment quotas and their respective slips.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con información sobre el año de ejercicio, estado, cuotas de pago y sus respectivos recibos."
        },
        "cnd_sp_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CPFs e CNPJs que deseja realizar a emissão da Certidão de Negativa no Estado de São Paulo para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CPFs and CNPJs that you want to issue the Certificate of Clearance in the State of São Paulo to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Complete el archivo de carga con los CPF y CNPJ que desea emitir el Certificado de Autorización en el Estado de São Paulo para configurar una registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "cnd_rj_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CPFs e CNPJs que deseja realizar a emissão da Certidão de Negativa no Estado do Rio de Janeiro para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CPFs and CNPJs that you want to issue the Certificate of Clearance in the State of Rio de Janeiro to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los CPF y CNPJ que desea emitir el Certificado de Negativo en el Estado de Río de Janeiro para configurar una registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "have_access_more_services": {
            "pt-BR": "E ter acesso a mais serviços",
            "en": "And have access to more services",
            "es": "Y acceda a más servicios"
        },
        "switch_service": {
            "pt-BR": "Trocar serviço",
            "en": "Switch service",
            "es": "Cambiar servicio"
        },
        "replace_service_with_this_one": {
            "pt-BR": "Substitua um serviço do seu plano por esse",
            "en": "Replace a service in your plan with this one",
            "es": "Reemplaza un servicio de tu plan por este"
        },
        "add": {
            "pt-BR": "Adicionar",
            "en": "Add",
            "es": "Para agregar"
        },
        "to_your_plan": {
            "pt-BR": "ao seu plano",
            "en": "to your plan",
            "es": "a tu plan"
        },
        "looks_like_you_used_all_licenses": {
            "pt-BR": "Parece que você já utilizou todas as licenças disponíveis",
            "en": "Looks like you've used all available licenses",
            "es": "Parece que ha utilizado todas las licencias disponibles."
        },
        "to_have_this_service_you_can": {
            "pt-BR": "Para ter esse serviço no seu plano, você pode",
            "en": "To have this service on your plan, you can",
            "es": "Para tener este servicio en tu plan, puedes"
        },
        "go_back": {
            "pt-BR": "Voltar",
            "en": "Go Back",
            "es": "Regreso"
        },
        "cpf_receita_hover": {
            "pt-BR": "Com este Serviço você consegue consultar vários CPFs na Receita Federal simultaneamente.",
            "en": "With this Service you can consult several CPFs in the Internal Revenue Service simultaneously.",
            "es": "Con este Servicio puede consultar varios CPF en la Receita Federal simultáneamente."
        },
        "opening_upgrade_options": {
            "pt-BR": "Abrindo opções de upgrade",
            "en": "Opening up upgrade options",
            "es": "Apertura de opciones de actualización"
        },
        "choose_a_service_exchange_license": {
            "pt-BR": "Escolha um serviço do seu plano para trocar licenças por",
            "en": "Choose a service from your plan to exchange licenses for",
            "es": "Elija un servicio de su plan para intercambiar licencias por"
        },
        "current_service": {
            "pt-BR": "Serviço Atual",
            "en": "Current Service",
            "es": "Servicio actual"
        },
        "choose_a_service": {
            "pt-BR": "Escolha um serviço",
            "en": "Choose a service",
            "es": "Elige un servicio"
        },
        "to_take_licenses": {
            "pt-BR": "para tirar licenças",
            "en": "to take licenses",
            "es": "tomar licencias"
        },
        "change_all": {
            "pt-BR": "Trocar todas",
            "en": "Change all",
            "es": "Cambiar todo"
        },
        "no_licenses_available": {
            "pt-BR": "Nenhuma licença disponível",
            "en": "No licenses available",
            "es": "No hay licencia disponible"
        },
        "select_a_service_above": {
            "pt-BR": "Selecione um serviço acima para visualizar e trocar licenças",
            "en": "Select a service above to view and change licenses",
            "es": "Seleccione un servicio de arriba para ver y cambiar licencias"
        },
        "new_service": {
            "pt-BR": "Novo Serviço",
            "en": "New Service",
            "es": "Nuevo servicio"
        },
        "hiring": {
            "pt-BR": "Em contratação",
            "en": "Hiring",
            "es": "Contratación"
        },
        "return_all": {
            "pt-BR": "Devolver todas",
            "en": "Return all",
            "es": "Devolver todo"
        },
        "request_sent_successfully": {
            "pt-BR": "Solicitação enviada com sucesso",
            "en": "Request sent successfully",
            "es": "Solicitud enviada con éxito"
        },
        "dont_worry_soon_receive_email": {
            "pt-BR": "Não se preocupe, breve você receberá em seu e-mail todas as informações sobre a mudança de plano e pagamento.",
            "en": "Don't worry, you will soon receive in your email all the information about the change of plan and payment.",
            "es": "No te preocupes, pronto recibirás toda la información sobre el cambio de plan y el pago en tu correo electrónico."
        },
        "choose_how_many_licenses_to_use": {
            "pt-BR": "Escolha quantas licenças usar nesse serviço",
            "en": "Choose how many licenses to use in this service",
            "es": "Elija cuántas licencias usar para este servicio"
        },
        "available": {
            "pt-BR": "disponíveis",
            "en": "available",
            "es": "disponible"
        },
        "available_singular": {
            "pt-BR": "disponível",
            "en": "available",
            "es": "disponible"
        },
        "confirm_exchange": {
            "pt-BR": "Confirmar troca",
            "en": "Confirm exchange",
            "es": "Confirmar intercambio"
        },
        "finalizing_request": {
            "pt-BR": "Finalizando solicitação",
            "en": "Finalizing request",
            "es": "Finalizando solicitud"
        },
        "exchange_confirmed": {
            "pt-BR": "Troca confirmada",
            "en": "Exchange confirmed",
            "es": "Intercambio confirmado"
        },
        "you_can_already_access_your_service": {
            "pt-BR": "Você já pode acessar e gerenciar seu novo serviço",
            "en": "You can now access and manage your new service",
            "es": "Ya puedes acceder y gestionar tu nuevo servicio"
        },
        "confirm": {
            "pt-BR": "Confirmar",
            "en": "Confirm",
            "es": "Confirmar"
        },
        "privacy_policy": {
            "pt-BR": "Política de Privacidade",
            "en": "Privacy Policy",
            "es": "Política de privacidad"
        },
        "terms_of_use": {
            "pt-BR": "Termos de Uso",
            "en": "Terms of use",
            "es": "Terminos de uso"
        },
        "developed_by": {
            "pt-BR": "Desenvolvido por",
            "en": "Developed by",
            "es": "Desarrollado por"
        },
        "contact": {
            "pt-BR": "Contato",
            "en": "Contact",
            "es": "Contacto"
        },
        "illustration_by": {
            "pt-BR": "Ilustração por ",
            "en": "Illustration by",
            "es": "Ilustración por"
        },
        "profile": {
            "pt-BR": "Perfil",
            "en": "Profile",
            "es": "Perfil"
        },
        "plan": {
            "pt-BR": "Plano",
            "en": "Plan",
            "es": "Plan"
        },
        "advanced": {
            "pt-BR": "Avançadas",
            "en": "Advanced",
            "es": "Avanzado"
        },
        "crew": {
            "pt-BR": "Equipe",
            "en": "Crew",
            "es": "Equipo"
        },
        "my_configurations": {
            "pt-BR": "Minhas Configurações",
            "en": "My Configurations",
            "es": "Mi configuración"
        },
        "visualize": {
            "pt-BR": "Visualizar",
            "en": "Visualize",
            "es": "Para ver"
        },
        "executed": {
            "pt-BR": "Executados",
            "en": "Executed",
            "es": "Ejecutados"
        },
        "finalized": {
            "pt-BR": "Finalizados",
            "en": "Finalized",
            "es": "Finalizado"
        },
        "error": {
            "pt-BR": "Erro",
            "en": "Error",
            "es": "Error"
        },
        "federal_revenue": {
            "pt-BR": "Receita Federal",
            "en": "Federal Revenue",
            "es": "Receta Federal"
        },
        "info_will_appear_here": {
            "pt-BR": "Ao utilizar um serviço, suas informações irão aparecer aqui",
            "en": "When using a service, your information will appear here",
            "es": "Al usar un servicio, su información aparecerá aquí."
        },
        "unsubscribe": {
            "pt-BR": "Cancelar assinatura",
            "en": "Unsubscribe",
            "es": "Cancelar firma"
        },
        "you_signed_the_plan": {
            "pt-BR": "Você contratou o plano",
            "en": "You signed the plan",
            "es": "Usted contrató el plan"
        },
        "with_it_you_receive": {
            "pt-BR": "Com ele, você recebe",
            "en": "With it, you receive",
            "es": "Con él, obtienes"
        },
        "to_use_or_distribute_among_your_team": {
            "pt-BR": "para utilizar ou distribuir entre a sua equipe",
            "en": "to use or distribute among your team",
            "es": "Usar o distribuir entre su equipo."
        },
        "see_plans_and_values": {
            "pt-BR": "Ver planos e valores",
            "en": "See plans and values",
            "es": "Ver planes y valores."
        },
        "do_you_want_to_hire_more_services": {
            "pt-BR": "Deseja contratar mais serviços?",
            "en": "Do you want to hire more services?",
            "es": "¿Quieres contratar más servicios?"
        },
        "see_the": {
            "pt-BR": "Veja a",
            "en": "See the",
            "es": "ver el"
        },
        "complete_list_of_services_here": {
            "pt-BR": "lista completa de serviços aqui",
            "en": "complete list of services here",
            "es": "Lista completa de servicios aquí."
        },
        "at_the_end_of_the_trial_period_you_will_receive_the_payment_slip_by_email": {
            "pt-BR": "Ao final do período de teste, você receberá o boleto de pagamento por e-mail",
            "en": "At the end of the trial period you will receive the payment slip by email",
            "es": "Al final del período de prueba, recibirá el boleto de pago por correo electrónico."
        },
        "for_more_information_send_a_message_to": {
            "pt-BR": "Para mais informações envie uma mensagem para",
            "en": "For more information send a message to",
            "es": "Para más información envíe un mensaje a"
        },
        "used_by": {
            "pt-BR": "Utilizado por",
            "en": "Used by",
            "es": "Usado por"
        },
        "configured_models": {
            "pt-BR": "Modelos configurados",
            "en": "Configured models",
            "es": "Modelos configurados"
        },
        "licenses_available": {
            "pt-BR": "licenças disponíveis",
            "en": "licenses available",
            "es": "Licencias disponibles"
        },
        "license_available": {
            "pt-BR": "licença disponível",
            "en": "license available",
            "es": "licencia"
        },
        "cnd_federal_revenue": {
            "pt-BR": "CND Receita Federal",
            "en": "CND Federal Revenue",
            "es": "CND Ingresos Federales"
        },
        "change_of_plan": {
            "pt-BR": "Mudança de Plano",
            "en": "Change of Plan",
            "es": "Cambio de planes"
        },
        "hub_contact_email": {
            "pt-BR": "hub-contato@smarthis.com.br",
            "en": "hub-contato@smarthis.com.br",
            "es": "hub-contato@smarthis.com.br"
        },
        "current_plan": {
            "pt-BR": "Plano Atual",
            "en": "Current Plan",
            "es": "Avión actual"
        },
        "service": {
            "pt-BR": "serviço",
            "en": "service",
            "es": "Servicio"
        },
        "monthly_appointments_to_your_plan": {
            "pt-BR": "consultas mensais ao seu plano por mais",
            "en": "monthly appointments to your plan for more",
            "es": "Consultas mensuales a su plan para más"
        },
        "contact_us_by": {
            "pt-BR": "Entre em contato por",
            "en": "Contact us by",
            "es": "Consultas mensuales a su plan para más"
        },
        "to_receive_personalized_review": {
            "pt-BR": "para receber uma análise personalizada",
            "en": "to receive a personalized review",
            "es": "Para recibir un análisis personalizado."
        },
        "login_capital": {
            "pt-BR": "ENTRAR",
            "en": "LOGIN",
            "es": "INICIAR SESIÓN"
        },
        "still_without_registry_create_your_account": {
            "pt-BR": "Ainda não tem cadastro? Crie sua conta",
            "en": "Still without registry? Create your account",
            "es": "¿Todavía no tienes registro?"
        },
        "i_forgot_my_password": {
            "pt-BR": "Esqueci a senha",
            "en": "I forgot my password",
            "es": "Olvidé la contraseña"
        },
        "access_denied_exclamation": {
            "pt-BR": "Acesso negado!",
            "en": "Access denied!",
            "es": "¡Acceso denegado!"
        },
        "your_username_and_password_didnt_match_please_try_again": {
            "pt-BR": "Seu username e senha não conferem. Por favor, tente novamente",
            "en": "Your username and password didn`t match. Please try again.",
            "es": "Su nombre de usuario y contraseña no confieren."
        },
        "old_password_does_not_match": {
            "pt-BR": "Antiga senha não confere",
            "en": "Old password does not match",
            "es": "La contraseña antigua no confiere"
        },
        "of": {
            "pt-BR": "de",
            "en": "of",
            "es": "en"
        },
        "change_password": {
            "pt-BR": "Mudar minha senha",
            "en": "Change password",
            "es": "Cambia mi contraseña"
        },
        "hello": {
            "pt-BR": "Olá",
            "en": "Hello",
            "es": "Hola"
        },
        "invited_to_his_team_on": {
            "pt-BR": "te convidou para o seu time no",
            "en": "invited to his team on",
            "es": "te invitó a tu equipo en el"
        },
        "click_on_the_button_bellow_to_complete_register": {
            "pt-BR": "Clique no botão abaixo para confirmar seu email e começar a transformar a sua maneira de trabalhar!",
            "en": "Click the button below to confirm your email and start transforming the way you work!",
            "es": "¡Haga clic en el botón a continuación para confirmar su correo electrónico y comenzar a transformar su forma de trabajar!"
        },
        "if_you_cannot_access_the_link": {
            "pt-BR": "Caso não consiga acessar o link",
            "en": "If you cannot access the link",
            "es": "Si no puedes acceder al enlace."
        },
        "with_smarthis_hub_you": {
            "pt-BR": "Com o Smarthis Hub, você",
            "en": "With Smarthis Hub, you",
            "es": "Con smartthis hub, tu"
        },
        "gain_more_freedom_to_focus_on_strategic_tasks": {
            "pt-BR": "Ganha mais liberdade para focar em tarefas estratégicas",
            "en": "Gain more freedom to focus on stratefic tasks",
            "es": "Gana más libertad para centrarse en tareas estratégicas."
        },
        "enjoy_ready_made_solutions_for_different_areas_of_expertise": {
            "pt-BR": "Desfruta de soluções prontas para diferentes áreas de atuação",
            "en": "Enjoy ready-made solutions for different areas of expertise",
            "es": "Disfruta de soluciones listas para diferentes áreas de actividad."
        },
        "minimizes_errors_and_avoids_delays": {
            "pt-BR": "Minimiza erros e evita atrasos",
            "en": "Minimizes errors and avoids delays",
            "es": "Minimiza los errores y evita retrasos."
        },
        "centralizes_tasks_and_results": {
            "pt-BR": "Centraliza tarefas e resultados",
            "en": "Centralizes tasks and results",
            "es": "Centraliza las tareas y los resultados."
        },
        "about_the": {
            "pt-BR": "Sobre o",
            "en": "About",
            "es": "Sobre el"
        },
        "smarthis_hub_is_a_smarthis_platform_that_seeks": {
            "pt-BR": "O Smarthis Hub é uma plataforma da Smarthis que busca trazer soluções plug-and-play para necessidades compartilhadas das companhias",
            "en": "Smarthis Hub is a Smarthis platform that seeks to bring plug-and-play solutions for shared needs and companies",
            "es": "SmartThis Hub es una plataforma SmartHis que busca traer soluciones de plug-and-Play a las empresas compartidas"
        },
        "we_take_digital_transformation_to_several_areas": {
            "pt-BR": "Levamos a transformação digital a diversas áreas de atuação no formato de assinatura (SaaS), facilitando o consumo desses serviços e permitindo que o cliente preocupe com infraestrutura",
            "en": "We take digital transformation to several areas of activity in the subscription format(Saas), facilitating the consumption of these services and allowing the costumer to worry about infrastructure",
            "es": "Tomamos la transformación digital a varias áreas de actividad en el formato de firma (SAA), lo que facilita el consumo de estos servicios y permitiendo que el cliente se preocupe por la infraestructura."
        },
        "questions_interrogation": {
            "pt-BR": "Dúvidas?",
            "en": "Questions?",
            "es": "¿Dudas?"
        },
        "problems_with_the_result_interrogation": {
            "pt-BR": "Problemas com o resultado?",
            "en": "Problems with the result?",
            "es": "¿Problemas con el resultado?"
        },
        "you_have_been_invited_to_smarthis_hub": {
            "pt-BR": "Você foi convidado para o Smarthis Hub",
            "en": "You have been invited to Smarthis Hub",
            "es": "Fuiste invitado a SmartThis Hub"
        },
        "the_female": {
            "pt-BR": "A",
            "en": "The",
            "es": "EL"
        },
        "is_now_part_of_smarthis_hub": {
            "pt-BR": "agora faz parte do Smarthis Hub",
            "en": "is now part of Smarthis Hub",
            "es": "Ahora es parte de SmartThis Hub"
        },
        "complete_your_registration_and": {
            "pt-BR": "Complete seu cadastro e acelere a transformação digital da sua empresa!",
            "en": "Complete your registration and accelerate your company`s digital transformation!",
            "es": "¡Complete su registro y acelere la transformación digital de su empresa!"
        },
        "make_exchange": {
            "pt-BR": "Efetuar troca",
            "en": "Make Exchange",
            "es": "Intercambio"
        },
        "no_more_results": {
            "pt-BR": "Não há mais resultados",
            "en": "No more results",
            "es": "No hay más resultados"
        },
        "save_and_exit": {
            "pt-BR": "Salvar e Sair",
            "en": "Save and Exit",
            "es": "Guardar y Salir"
        },
        "delete_collaborator": {
            "pt-BR": "Excluir colaborador",
            "en": "Delete collaborator",
            "es": "Colaborador"
        },
        "please_contact_admin": {
            "pt-BR": "Para solicitar esse serviço, entre em contato com o seu administrador",
            "en": "To request this service, please contact your administrator",
            "es": "Para solicitar este servicio, comuníquese con su administrador."
        },
        "please_contact_admin_2": {
            "pt-BR": "responsável pelo seu plano",
            "en": "responsible for your plan",
            "es": "Responsable de tu plan"
        },
        "please_contact_admin_3": {
            "pt-BR": "Para solicitar esse serviço, entre em contato com o  administrador do seu plano",
            "en": "To request this service, contact your plan administrator",
            "es": "Para solicitar este servicio, comuníquese con su plan administrador."
        },
        "delete_selected": {
            "pt-BR": "Excluir selecionados",
            "en": "Delete selected",
            "es": "Eliminar seleccionado"
        },
        "password_change": {
            "pt-BR": "Mudança de Senha",
            "en": "Password Change",
            "es": "Cambio de contraseña"
        },
        "current_password": {
            "pt-BR": "Senha Atual",
            "en": "Current password",
            "es": "Contraseña actual"
        },
        "new_password": {
            "pt-BR": "Senha nova",
            "en": "New password",
            "es": "Nueva contraseña"
        },
        "strong_password": {
            "pt-BR": "Senha forte",
            "en": "Strong password",
            "es": "Contraseña segura"
        },
        "invalid_password": {
            "pt-BR": "Senha inválida",
            "en": "Invalid password",
            "es": "contraseña invalida"
        },
        "repeat_new_password": {
            "pt-BR": "Repetir senha nova",
            "en": "Repeat new password",
            "es": "repita la nueva contraseña"
        },
        "passwords_dont_match": {
            "pt-BR": "Senhas não coincidem",
            "en": "Passwords don't match",
            "es": "Las contraseñas no coinciden."
        },
        "passwords_requirements": {
            "pt-BR": "Sua senha deve ter no mínimo 8 caracteres entre letras maiúsculas, minúsculas, números e símbolos",
            "en": "Your password must have at least 8 characters between uppercase and lowercase letters, numbers and a symbol",
            "es": "Su contraseña debe tener al menos 8 caracteres entre mayúsculas, minúsculas, números y un símbolo"
        },
        "declaration_and_issuance_of_idt_sefaz": {
            "pt-BR": "Declaração e Emissão de ITD Sefaz",
            "en": "Declaration and Issuance of ITD Sefaz",
            "es": "Declaración y Emisión de ITD SEFAZ"
        },
        "template_with_your_sefaz_rj_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do Sefaz-RJ, buscando guias específicos e preenchendo um arquivo de entrada com as informações necessárias.",
            "en": "With a few clicks, you configure a template with your Sefaz-RJ credentials, searching for specific guides and filling an input file with the necessary information.",
            "es": "Con unos pocos clics, configuró un modelo con sus credenciales SEFAZ-RJ, buscando guías específicas y cumpliendo con un archivo de entrada con la información requerida."
        },
        "their_respective_itd_declaration_works_1": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com informações sobre o CNPJ/CPF e suas respectivas declaração de ITD .",
            "en": "After using the service, the results arrive by email with information about the CNPJ/CPF and their respective ITD declaration.",
            "es": "Después de usar el servicio, los resultados llegaron por correo electrónico con información sobre CNPJ / CPF y su declaración ITD respectiva."
        },
        "sefaz_credentials_rj": {
            "pt-BR": "Credenciais Sefaz - Rio de Janeiro",
            "en": "Sefaz Credentials - Rio de Janeiro",
            "es": "Sefaz Credenciales - Río de Janeiro"
        },
        "user": {
            "pt-BR": "Usuário",
            "en": "User",
            "es": "Usuario"
        },
        "your_smarthis_hub_trial_period_has_begun": {
            "pt-BR": "Seu período de testes do Smarthis Hub começou!",
            "en": "Your Smarthis Hub trial period has begun!",
            "es": "¡Su período de prueba de Smarthis Hub ha comenzado!"
        },
        "your_free_trial_started_exclamation": {
            "pt-BR": "O seu período de teste no Smarthis Hub começou!",
            "en": "Your trial period on Smarthis Hub has begun!",
            "es": "¡Ha comenzado su período de prueba en Smarthis Hub!"
        },
        "start_using_smarthis_hub_and_accelerate": {
            "pt-BR": "Comece a usar o Smarthis Hub e acelere",
            "en": "Start using Smarthis Hub and accelerate",
            "es": "Comience a usar SmartHis Hub y acelerar"
        },
        "your_companys_digital_transformation": {
            "pt-BR": "a transformação digital da sua empresa",
            "en": "your company`s digital transformation",
            "es": "La transformación digital de su empresa."
        },
        "you_will_have_full_access_and": {
            "pt-BR": "Você terá acesso completo e",
            "en": "You will have full access and",
            "es": "Tendrás acceso completo y"
        },
        "free_to": {
            "pt-BR": "gratuito ao",
            "en": "free to",
            "es": "gratis"
        },
        "over_the_next_14_days": {
            "pt-BR": "durante os próximos 14 dias",
            "en": "over the next 14 days",
            "es": "Durante los próximos 14 días."
        },
        "find_out_how_to_get_the_most_out_of_your_trial_period": {
            "pt-BR": "Saiba como aproveitar melhor o seu período de teste",
            "en": "Find out how to get the most out of your trial period",
            "es": "Aprenda cómo mejorar su período de prueba"
        },
        "check_and_provide_input_files_if_necessary_for_your_services": {
            "pt-BR": "Confira e providencie os arquivos de entrada, caso necessários para os seus serviços",
            "en": "Check and provide input files, if necessary for your services",
            "es": "Verifique y organice los archivos de entrada si es necesario para sus servicios"
        },
        "configure_models_according_to_your_needs": {
            "pt-BR": "Configure modelos de acordo com o que precisa",
            "en": "Configure models according to your needs",
            "es": "Configure las registros según lo que necesita."
        },
        "use_the_models_as_ofter_as_you_like": {
            "pt-BR": "Use os modelos quantas vezes quiser, sem cobranças extras",
            "en": "Use the models as often as you like, no extra charges",
            "es": "Usa los modelos tantas veces como quieras, sin cargos adicionales."
        },
        "you_can_also": {
            "pt-BR": "Você também pode",
            "en": "You can also",
            "es": "Tú también puedes"
        },
        "invite_and_transfer_services_for_employees": {
            "pt-BR": "Convidar e transferir serviços para colaboradores da sua equipe (nos planos Area ou Business)",
            "en": "Invite and transfer services for employees of your team (in Area or Business plans)",
            "es": "Invitar y transferir servicios a empleados de su equipo (en el área o aviones de negocios)"
        },
        "set_up_a_model_that_automatically_sends_results": {
            "pt-BR": "Configurar um modelo que envie automaticamente os resultados para mais pessoas da sua empresa",
            "en": "Set up a model that automatically sends results to more people in your company ",
            "es": "Configure una registro que envíe automáticamente los resultados para más personas en su empresa."
        },
        "notification_of": {
            "pt-BR": "Notificação de",
            "en": "Notification of",
            "es": "Configure una registro que envíe automáticamente los resultados para más personas en su empresa."
        },
        "your_password_access_on_smarthis_hub_was_changed": {
            "pt-BR": "A sua senha de acesso no Smarthis Hub foi alterada",
            "en": "Your password access on Smarthis Hub was changed",
            "es": "Su contraseña de acceso en SmartThis Hub ha cambiado"
        },
        "new_service_available_for_you_on_smarthis_hub_exclamation": {
            "pt-BR": "Novo serviço disponível para você no Smarthis Hub!",
            "en": "New service available for you on Smarthis Hub!",
            "es": "¡Nuevo servicio disponible para usted en Smarthis Hub!"
        },
        "you_received_access_to_the_service": {
            "pt-BR": "Você recebeu acesso ao serviço",
            "en": "You received access to the service",
            "es": "Recibió acceso al servicio."
        },
        "if_you_cant": {
            "pt-BR": "Caso não consiga",
            "en": "If you can`t",
            "es": "Si tu no puedes"
        },
        "new_service_available": {
            "pt-BR": "Novo serviço disponível",
            "en": "New service available",
            "es": "Nuevo servicio disponible"
        },
        "you_used": {
            "pt-BR": "Você utilizou",
            "en": "You used",
            "es": "Usaste"
        },
        "free_days": {
            "pt-BR": "dias grátis",
            "en": "free days",
            "es": "Días libres"
        },
        "sign_up_and_experience": {
            "pt-BR": "Cadastre-se e experimente o que a transformação digital pode fazer pela sua empresa",
            "en": "Sign up and experience what digital transformation can do for your company",
            "es": "Regístrate y experimenta lo que la transformación digital puede hacer para su empresa"
        },
        "more_freedom_strategic_tasks": {
            "pt-BR": "Mais liberdade para focar em tarefas estratégicas",
            "en": "More freedom to focus on strategic tasks",
            "es": "Más libertad para centrarse en tareas estratégicas."
        },
        "error_reduction": {
            "pt-BR": "Redução de erros",
            "en": "Error reduction",
            "es": "Error"
        },
        "cost_reduction": {
            "pt-BR": "Redução de custos",
            "en": "Cost reduction",
            "es": "Reducción de costos"
        },
        "and_more": {
            "pt-BR": "E mais",
            "en": "And more",
            "es": "Y más"
        },
        "affirm_that_i_read_and_agree": {
            "pt-BR": "Afirmo que li e concordo com a ",
            "en": "I affirm that I read and agree with the ",
            "es": "Afirmo que leí y estoy de acuerdo con el"
        },
        "of_masculine": {
            "pt-BR": "do",
            "en": "of",
            "es": "del"
        },
        "choose": {
            "pt-BR": "Escolha",
            "en": "Choose",
            "es": "Elección"
        },
        "services_with_your_licenses": {
            "pt-BR": "serviços com as suas licenças",
            "en": "services with your licenses",
            "es": "Servicios con sus licencias."
        },
        "dashboards": {
            "pt-BR": "Dashboards",
            "en": "Dashboards",
            "es": "Tablero"
        },
        "invite_collaborator": {
            "pt-BR": "Convidar Colaborador",
            "en": "Invite Collaborator",
            "es": "Invitación colaboradora"
        },
        "upgrade_imperative": {
            "pt-BR": "faça um upgrade",
            "en": "upgrade",
            "es": "Hacer una actualización"
        },
        "you_can_distribute_up_to": {
            "pt-BR": "Você pode distribuir até",
            "en": "You can distribute up to",
            "es": "Hacer una actualización"
        },
        "you_can_distribute_up_to_2": {
            "pt-BR": "para este serviço. Para ter acesso à mais licenças,",
            "en": "for this service. To access more licenses,",
            "es": "Para este servicio."
        },
        "invite": {
            "pt-BR": "Convidar",
            "en": "Invite",
            "es": "Invitar"
        },
        "my_licenses": {
            "pt-BR": "minhas licenças",
            "en": "my licenses",
            "es": "Mis licencias"
        },
        "administrator": {
            "pt-BR": "Administrador",
            "en": "Administrator",
            "es": "Administrador"
        },
        "restore_licenses": {
            "pt-BR": "restaurar licenças",
            "en": "restore licenses",
            "es": "restaurar licencias"
        },
        "invite_collaborators": {
            "pt-BR": "Convidar colaboradores",
            "en": "Invite collaborators",
            "es": "Invitar a los empleados"
        },
        "invited_collaborators": {
            "pt-BR": "Colaboradores convidados",
            "en": "Invited collaborators",
            "es": "Empleados de invitados"
        },
        "you_have_transferred_all_licenses": {
            "pt-BR": "Você transferiu todas as suas licenças",
            "en": "You have transferred all your licenses",
            "es": "Tras transferías todas tus licencias."
        },
        "you_have_transferred_all_licenses_2": {
            "pt-BR": "Para utilizar esse serviço você precisa realocá-las ou fazer upgrade",
            "en": "To use this service you need to relocate or upgrade them",
            "es": "Para usar este servicio necesitas reubicarlos o actualizar."
        },
        "enter_email_you_wish_invite": {
            "pt-BR": "Digite o e-mail de quem deseja convidar",
            "en": "Enter the email of who you want to invite",
            "es": "Ingrese el correo electrónico que desea invitar"
        },
        "choose_from_your_team_or_invite": {
            "pt-BR": "Escolha pessoas do seu time ou convide por e-mail",
            "en": "Choose people from your team or invite by email",
            "es": "Elija personas de su equipo o invite por correo electrónico."
        },
        "invalid_email": {
            "pt-BR": "O email enviado é inválido.",
            "en": "The email sent is invalid.",
            "es": "El correo electrónico enviado no es válido."
        },
        "invitation_not_found": {
            "pt-BR": "O seu convite não foi encontrado, favor entrar em contato com ",
            "en": "Your invitation was not found, please contact ",
            "es": "No se encontró su invitación, por favor contacte"
        },
        "welcome_hub": {
            "pt-BR": "Agora você faz parte do Smarthis Hub",
            "en": "You are now part of Smarthis Hub",
            "es": "Ahora eres parte del SmartThis Hub"
        },
        "welcome_hub_2": {
            "pt-BR": "Você já pode conhecer o site e acelerar a transformação digital da sua empresa",
            "en": "You can now visit the site and accelerate your company's digital transformation",
            "es": "Ya puede conocer el sitio y acelerar la transformación digital de su empresa."
        },
        "hire_more_services": {
            "pt-BR": "Contratar mais serviços",
            "en": "Hire more services",
            "es": "Contrata mas servicios"
        },
        "enter_email_here": {
            "pt-BR": "Insira o e-mail aqui",
            "en": "Enter e-mail here",
            "es": "Ingrese el correo electrónico aquí"
        },
        "save_model": {
            "pt-BR": "Salvar Modelo",
            "en": "Save Model",
            "es": "Guardar Registro"
        },
        "email_does_not_exist": {
            "pt-BR": "O e-mail não existe",
            "en": "The email does not exist",
            "es": "El correo electrónico no existe"
        },
        "please_try_again": {
            "pt-BR": "Por favor, tente novamente",
            "en": "Please try again",
            "es": "Inténtalo de nuevo"
        },
        "areas": {
            "pt-BR": "Áreas",
            "en": "Areas",
            "es": "Zonas"
        },
        "employee_working_hours": {
            "pt-BR": "Horas Colaborador",
            "en": "Employee Working Hours",
            "es": "Colaborador de horas"
        },
        "rpa_runtime": {
            "pt-BR": "Horas RPA",
            "en": "RPA Runtime",
            "es": "Horas RPA"
        },
        "hours_saved": {
            "pt-BR": "Retorno em Horas",
            "en": "Hours Saved",
            "es": "Regreso en horas"
        },
        "begin_from": {
            "pt-BR": "Início",
            "en": "From",
            "es": "Comienzo"
        },
        "end": {
            "pt-BR": "Fim",
            "en": "To",
            "es": "Fin"
        },
        "custom": {
            "pt-BR": "Personalizado",
            "en": "Custom",
            "es": "Personalizado"
        },
        "today": {
            "pt-BR": "Hoje",
            "en": "Today",
            "es": "Hoy dia"
        },
        "yesterday": {
            "pt-BR": "Ontem",
            "en": "Yesterday",
            "es": "Ayer"
        },
        "last": {
            "pt-BR": "Última",
            "en": "Last",
            "es": "Ultimo"
        },
        "days": {
            "pt-BR": "dias",
            "en": "days",
            "es": "días"
        },
        "nfe_generation_and_download": {
            "pt-BR": "Geração e download de NF-e",
            "en": "NF-e generation and download",
            "es": "días"
        },
        "text_nfe_generation_and_download": {
            "pt-BR": "Gere e faça download de diversas notas fiscais de produtos de forma simultânea, com apenas alguns cliques.",
            "en": "Generate and download multiple product invoices simultaneously, with just a few clicks.",
            "es": "Genere y descargue varias notas fiscales del producto simultáneamente, con solo unos pocos clics."
        },
        "bank_reconciliation": {
            "pt-BR": "Conciliação bancária",
            "en": "Bank reconciliation",
            "es": "Conciliación bancaria"
        },
        "text_bank_reconciliation": {
            "pt-BR": "Centralize as contas a pagar e a receber da sua empresa com o serviço de conciliação bancária do Smarthis Hub. ",
            "en": "Centralize your company's accounts payable and receivable with Smarthis Hub's bank reconciliation service.",
            "es": "Centraliza las cuentas pagaderas y cobrarias de su empresa con el servicio de conciliación del banco SmartThis Hub."
        },
        "checking_presence_of_signature_on_documents": {
            "pt-BR": "Verificação de presença de assinatura em documentos",
            "en": "Checking the presence of signature on documents",
            "es": "Verificación de la presencia de la firma en documentos."
        },
        "text_checking_presence_of_signature_on_documents": {
            "pt-BR": "Verifique rapidamente a presença de assinaturas em grandes volumes de documentos. ",
            "en": "Quickly check for signatures on large volumes of documents.",
            "es": "Verifique rápidamente la presencia de firmas en grandes volúmenes de documentos."
        },
        "intelligent_document_processing": {
            "pt-BR": "Processamento inteligente de documentos",
            "en": "Intelligent document processing",
            "es": "Procesamiento inteligente de documentos"
        },
        "text_intelligent_document_processing": {
            "pt-BR": "Transforme dados digitalizados em estruturados de forma automática, facilitando a organização e correlação da informação na sua empresa.",
            "en": "Automatically transform digitized data into structured data, facilitating the organization and correlation of information in your company.",
            "es": "Transforme los datos digitalizados en estructurado automáticamente, lo que facilita la organización y la correlación de la información en su empresa."
        },
        "recomendation_algorithm_ecommerce": {
            "pt-BR": "Algoritmo de recomendação para E-commerce",
            "en": "Recommendation Algorithm for E-commerce",
            "es": "Algoritmo de recomendación para el comercio electrónico"
        },
        "text_recomendation_algorithm_ecommerce": {
            "pt-BR": "Aumente a conversão e o ticket médio do seu e-commerce com a assertividade do nosso algoritmo de recomendação de produtos.",
            "en": "Increase your e-commerce conversion and average ticket with the assertiveness of our product recommendation algorithm.",
            "es": "Aumente la conversión y el boleto promedio de su comercio electrónico con la asertividad de nuestro algoritmo de recomendación de productos."
        },
        "text_chatbot": {
            "pt-BR": "Torne seu atendimento mais eficaz e melhore a satisfação dos clientes com o nosso serviço de chatbots.",
            "en": "Make your service more effective and improve customer satisfaction with our chatbot service.",
            "es": "Haga que su servicio sea más efectivo y mejore la satisfacción del cliente con nuestro servicio de chatbots."
        },
        "verification_of_decrees_ordinances": {
            "pt-BR": "Verificação de decretos e portarias",
            "en": "Verification of decrees and ordinances",
            "es": "Verificación de decretos y concusiones."
        },
        "text_verification_of_decrees_ordinances": {
            "pt-BR": "Fique por dentro das mudanças em decretos e portarias mais relevantes para o seu negócio com o nosso serviço de verificação contínua.",
            "en": "Stay on top of changes in decrees and ordinances that are most relevant to your business with our continuous verification service.",
            "es": "Manténgase dentro de los cambios en los decretos y las ordenanzas más relevantes para su negocio con nuestro servicio de cheques continuo."
        },
        "integrated_dashboards_ecommerce": {
            "pt-BR": "Dashboards integrados para e-commerce",
            "en": "Integrated dashboards for e-commerce",
            "es": "Tableros integrados para e-commerce"
        },
        "text_integrated_dashboards_ecommerce": {
            "pt-BR": "Tome decisões para o seu e-commerce, acompanhando as principais métricas para gerir o seu negócio e impulsionar as suas vendas.",
            "en": "Make decisions for your e-commerce, following the main metrics to manage your business and boost your sales.",
            "es": "Tome decisiones para su comercio electrónico, siguiendo las principales métricas para administrar su negocio y aumentar sus ventas."
        },
        "you_will_receive_news": {
            "pt-BR": "Você receberá as novidades",
            "en": "You will receive the news",
            "es": "Recibirás las noticias."
        },
        "inactive": {
            "pt-BR": "Inativa",
            "en": "Inactive",
            "es": "Inactivo"
        },
        "apply_filters": {
            "pt-BR": "Aplicar filtros",
            "en": "Apply filters",
            "es": "Filtrar"
        },
        "january": {
            "pt-BR": "Janeiro",
            "en": "January",
            "es": "enero"
        },
        "february": {
            "pt-BR": "Fevereiro",
            "en": "February",
            "es": "febrero"
        },
        "march": {
            "pt-BR": "Março",
            "en": "March",
            "es": "marcha"
        },
        "april": {
            "pt-BR": "Abril",
            "en": "April",
            "es": "abril"
        },
        "may": {
            "pt-BR": "Maio",
            "en": "May",
            "es": "Mayo"
        },
        "june": {
            "pt-BR": "Junho",
            "en": "June",
            "es": "junio"
        },
        "july": {
            "pt-BR": "Julho",
            "en": "July",
            "es": "mes de julio"
        },
        "august": {
            "pt-BR": "Agosto",
            "en": "August",
            "es": "agosto"
        },
        "september": {
            "pt-BR": "Setembro",
            "en": "September",
            "es": "septiembre"
        },
        "october": {
            "pt-BR": "Outubro",
            "en": "October",
            "es": "octubre"
        },
        "november": {
            "pt-BR": "Novembro",
            "en": "November",
            "es": "noviembre"
        },
        "december": {
            "pt-BR": "Dezembro",
            "en": "December",
            "es": "diciembre"
        },
        "sunday_first_letter": {
            "pt-BR": "D",
            "en": "S",
            "es": "D"
        },
        "monday_first_letter": {
            "pt-BR": "S",
            "en": "M",
            "es": "s"
        },
        "tuesday_first_letter": {
            "pt-BR": "T",
            "en": "T",
            "es": "T"
        },
        "wednessday_first_letter": {
            "pt-BR": "Q",
            "en": "W",
            "es": "Q"
        },
        "thursday_first_letter": {
            "pt-BR": "Q",
            "en": "T",
            "es": "Q"
        },
        "friday_first_letter": {
            "pt-BR": "S",
            "en": "F",
            "es": "s"
        },
        "saturday_first_letter": {
            "pt-BR": "S",
            "en": "S",
            "es": "s"
        },
        "order_by": {
            "pt-BR": "Ordenar por",
            "en": "Order by",
            "es": "Ordenar"
        },
        "rpa_runtime_history": {
            "pt-BR": "Histórico de Horas de Execução RPA",
            "en": "RPA Runtime History",
            "es": "HORAS HISTORIA RPA"
        },
        "view_by": {
            "pt-BR": "Detalhar por",
            "en": "View by",
            "es": "Detalle por"
        },
        "day": {
            "pt-BR": "Dia",
            "en": "Day",
            "es": "Día"
        },
        "hour": {
            "pt-BR": "Hora",
            "en": "Hour",
            "es": "Hora"
        },
        "hours": {
            "pt-BR": "Horas",
            "en": "Hours",
            "es": "Hora"
        },
        "delete_area": {
            "pt-BR": "Excluir área?",
            "en": "Delete area?",
            "es": "Eliminar área?"
        },
        "do_you_want_to_delete_the_area": {
            "pt-BR": "Deseja excluir a área",
            "en": "Do you want to delete the area",
            "es": "Quiero eliminar el"
        },
        "by_clicking_delete_this_area_will_be_permanently_deleted": {
            "pt-BR": "Ao clicar em \"Excluir\" essa área será apagada permanentemente.",
            "en": "By clicking “Delete” this area will be permanently deleted.",
            "es": "Al hacer clic en \"Eliminar\", esta área se borrará permanentemente."
        },
        "area_name": {
            "pt-BR": "Nome da área de Negócio",
            "en": "Business Area",
            "es": "Al hacer clic en \"Eliminar\", esta área se borrará permanentemente."
        },
        "edit_area": {
            "pt-BR": "Editar Área",
            "en": "Edit Area",
            "es": "Área de edición"
        },
        "name_the_business_area_you_would_like_to_add": {
            "pt-BR": "Digite o nome da área que deseja cadastrar",
            "en": "Name the Business Area you would like to add",
            "es": "Ingrese el nombre del área que desea registrar"
        },
        "register_area": {
            "pt-BR": "Cadastrar Área",
            "en": "Add Business Area",
            "es": "Registrar Area"
        },
        "number_of_processes": {
            "pt-BR": "Nº de Processos",
            "en": "Number of Processes",
            "es": "Número de procesos"
        },
        "there_are_no_more_business_areas": {
            "pt-BR": "Você não possui mais áreas cadastradas",
            "en": "There are no more Business Areas",
            "es": "No tienes más áreas registradas."
        },
        "week": {
            "pt-BR": "Semana",
            "en": "Week",
            "es": "Semana"
        },
        "month_capital": {
            "pt-BR": "Mês",
            "en": "Month",
            "es": "Mes"
        },
        "robot_utilization_per_hour": {
            "pt-BR": "Ocupação dos Robôs em 24h",
            "en": "Robot Utilization per Hour",
            "es": "Ocupación de robots por rango de tiempo."
        },
        "general_rate": {
            "pt-BR": "Média geral",
            "en": "General Rate",
            "es": "Promedio general"
        },
        "individual_rate": {
            "pt-BR": "Média individual",
            "en": "Individual Rate",
            "es": "Promedio individual"
        },
        "successfully_edited_area": {
            "pt-BR": "Área editada com sucesso",
            "en": "Successfully edited area",
            "es": "Área editada exitosa"
        },
        "executed_processes": {
            "pt-BR": "processos executados",
            "en": "Executed Processes",
            "es": "Procesos realizados"
        },
        "completion_rate": {
            "pt-BR": "Taxa de Conclusão",
            "en": "Completion rate",
            "es": "Tasa de Finalización"
        },
        "create_processes_to_group_sub_processes_that_perform_the_same_taks": {
            "pt-BR": "Crie Processos para agrupar Sub-processos que executam uma mesma tarefa. Assim, você fornece as informações necessárias apenas uma vez e consegue uma visualização mais exata das execuções e retornos no seu Dashboard RPA.",
            "en": "Create Processes to group Sub-processes that perform the same task. This way, you provide necessary informations only once and can get a more accurate view of executions and returns in your RPA Dashboard.",
            "es": "Cree procesos para agrupar subprocesos que realizan la misma tarea. De esa forma, solo proporciona la información que necesita una vez y obtiene una vista más precisa de las ejecuciones y devoluciones en su panel de RPA."
        },
        "original_name": {
            "pt-BR": "Nome Original",
            "en": "Process Name",
            "es": "Nombre original"
        },
        "area": {
            "pt-BR": "Área",
            "en": "Area",
            "es": "Área"
        },
        "individual_roi_by_processes": {
            "pt-BR": "ROI Individual por Processos",
            "en": "Individual ROI by Processes",
            "es": "ROI Individual por Procesos"
        },
        "impact_on_returned_hours": {
            "pt-BR": "Impacto em horas retornadas",
            "en": "Impact on returned hours",
            "es": "Impacto en las horas devueltas"
        },
        "individual_roi": {
            "pt-BR": "ROI Individual",
            "en": "Individual ROI",
            "es": "ROI individual"
        },
        "return_by_business_area": {
            "pt-BR": "Retorno por Áreas",
            "en": "Return by Business Area",
            "es": "Retorno por áreas"
        },
        "you_do_not_have_registered_areas_yet": {
            "pt-BR": "Você ainda não possui áreas cadastradas",
            "en": "You do not have registered areas yet",
            "es": "Todavía no tienes áreas registradas."
        },
        "register_business_areas_of_your_company_and_link_to_processes": {
            "pt-BR": "Cadastre áreas de negócio da sua empresa e associe aos processos para obter insights ainda mais valiosos.",
            "en": "Register business areas of your company and link to processes to gain even more valuable insights.",
            "es": "Registre áreas de negocio de su empresa y asocie los procesos para obtener información aún más valiosa."
        },
        "return_on_investment": {
            "pt-BR": "Retorno por Investimento",
            "en": "Return on Investment",
            "es": "Retorno de la inversión"
        },
        "roi_investment": {
            "pt-BR": "de ROI",
            "en": "of ROI",
            "es": "de ROI"
        },
        "of_rpa_runtime": {
            "pt-BR": "de execução RPA",
            "en": "of RPA runtime",
            "es": "RPA"
        },
        "of_time_saved": {
            "pt-BR": "de horas retornadas",
            "en": "of time saved",
            "es": "RPA"
        },
        "freed_up_from_employees": {
            "pt-BR": "liberadas dos colaboradores",
            "en": "freed up from employees",
            "es": "liberado de los empleados"
        },
        "tooltip_this_is_the_name_of_the_process_in_th_uiPath_orchestrator": {
            "pt-BR": "Este é o nome do processo no orquestrador UiPath. Ele não pode ser editado, mas você pode criar um apelido para esse processo.",
            "en": "This is the name of the process from your UiPath Orchestrator. It can not be changed, but you can create a Process Alias bellow.",
            "es": "Este es el nombre del proceso en el orquestador UIPATH."
        },
        "you_can_associate_processes_to_areas_in": {
            "pt-BR": "Você pode associar processos às áreas em ",
            "en": "You can link processes to business areas in",
            "es": "Puede asociar procesos con áreas en"
        },
        "settings_processes": {
            "pt-BR": "Configurações > Processos.",
            "en": "Settings > Processes.",
            "es": "Configuración> Procesos."
        },
        "this_helps_us_provide_more_complete_information_on_the_rpa_dashboard": {
            "pt-BR": "Isso nos ajuda a fornecer informações mais completas no Dashboard de RPA",
            "en": "This helps the RPA Dashboard show graphs with complete data",
            "es": "Esto nos ayuda a proporcionar información más completa en el Panel de RPA"
        },
        "editor": {
            "pt-BR": "Editor",
            "en": "Can edit",
            "es": "Editor"
        },
        "can_view": {
            "pt-BR": "Leitor",
            "en": "Can view",
            "es": "Lector"
        },
        "admin": {
            "pt-BR": "Admin",
            "en": "Admin",
            "es": "Administración"
        },
        "invite_staff_members_with_their_email": {
            "pt-BR": "Convide colaboradores por e-mail",
            "en": "Invite staff members with their e-mail",
            "es": "Invitar a los colaboradores de correo electrónico"
        },
        "can_view_graphs_edit_settings_and_invite_staff_members": {
            "pt-BR": "Pode visualizar gráficos, editar configurações e convidar colaboradores",
            "en": "Can view graphs, edit settings and invite staff members",
            "es": "Puede ver gráficos, editar configuraciones e invitar a colaboradores"
        },
        "can_view_graphs_but_can_not_edit_settings_or_invite_staff_members": {
            "pt-BR": "Pode visualizar gráficos mas não pode editar configurações ou convidar colaboradores",
            "en": "Can view graphs, but can not edit settings or invite staff members",
            "es": "Puede ver gráficos, pero no puede editar la configuración o invitar a colaboradores"
        },
        "email": {
            "pt-BR": "Email",
            "en": "Email",
            "es": "Correo electrónico"
        },
        "highlights": {
            "pt-BR": "destaques",
            "en": "highlights",
            "es": "Destacar"
        },
        "table": {
            "pt-BR": "tabela",
            "en": "table",
            "es": "tabla"
        },
        "capturing_graph": {
            "pt-BR": "Capturando gráfico",
            "en": "Capturing graph",
            "es": "Carta de captura"
        },
        "please_wait_capture_chart": {
            "pt-BR": "Por favor, aguarde alguns instantes enquanto preparamos o seu gráfico",
            "en": "Please, wait a few moments while we generate your chart",
            "es": "Por favor, espere unos momentos mientras preparamos su tabla."
        },
        "general_information": {
            "pt-BR": "Informações Gerais",
            "en": "General information",
            "es": "Informaciones generales"
        },
        "before_rpa": {
            "pt-BR": "Antes do RPA",
            "en": " Before RPA Implementation",
            "es": "Antes del RPA"
        },
        "summary": {
            "pt-BR": "Resumo",
            "en": "Summary",
            "es": "Resumen"
        },
        "edit_process": {
            "pt-BR": "Editar Processo",
            "en": "Edit Process",
            "es": "Editar Proceso"
        },
        "delete_process": {
            "pt-BR": "Excluir Processo",
            "en": "Delete Process",
            "es": "Eliminar Proceso"
        },
        "edit_subprocess": {
            "pt-BR": "Editar Sub-processo",
            "en": "Edit Sub-process",
            "es": "Editar Subproceso"
        },
        "save_process": {
            "pt-BR": "Salvar processo",
            "en": "Save process",
            "es": "Proceso"
        },
        "exit": {
            "pt-BR": "Sair",
            "en": "Close",
            "es": "Salir"
        },
        "process_nickname": {
            "pt-BR": "Apelido do processo",
            "en": "Process alias",
            "es": "Apodo de proceso"
        },
        "rpa_project_cost": {
            "pt-BR": "Custo do projeto RPA",
            "en": "RPA Project's Cost",
            "es": "Costo del proyecto RPA"
        },
        "example_process_nickname": {
            "pt-BR": "Exemplo: “Download de Contas a Pagar”, “Emissão de Boletos”",
            "en": "Exemple: \"Supplier Reputation Check\"",
            "es": "Ejemplo: \"Descargar cuentas pagaderas\", \"Emisión de boletos\""
        },
        "fill_in_the_data_before_rpa_implementation": {
            "pt-BR": "Por favor, preencha os dados ao lado de acordo com como o processo era feito antes da implementação do RPA",
            "en": "Please fill in the data according to the way the process used to be done before the RPA implementation",
            "es": "Llene los datos junto a cómo se realizó el proceso antes de la implementación del RPA"
        },
        "we_need_this_info_calculate_roi": {
            "pt-BR": "Precisamos desses dados para calcular o ROI e trazer informações mais completas no Dashboard",
            "en": "We need this data to calculate the ROI and bring better insights to your Dashboard",
            "es": "Necesitamos estos datos para calcular el ROI y traer información más completa en el tablero"
        },
        "minutes_per_task": {
            "pt-BR": "Minutos por tarefa",
            "en": "Minutes per task",
            "es": "Minutos por tarea"
        },
        "by_staff_member": {
            "pt-BR": "por colaborador",
            "en": "per employee",
            "es": "por colaborador"
        },
        "average_time_staff_member_performs_task": {
            "pt-BR": "Tempo médio que um colaborador gasta para executar essa tarefa uma vez.",
            "en": "Average time an employee spends to perform this task once.",
            "es": "Tiempo promedio que un colaborador gasta para realizar esta tarea una vez."
        },
        "average_time_staff_member_performs_task_example": {
            "pt-BR": "Se um colaborador leva em média 5 minutos para lançar uma nota fiscal, responda “5 minutos”.",
            "en": "If a collaborator takes an average of 5 minutes to upload a document, answer “5 minutes“.",
            "es": "Si un empleado tarda un promedio de 5 minutos en publicar una nota, responda “5 minutos“."
        },
        "minutes": {
            "pt-BR": "minutos",
            "en": "minutes",
            "es": "minuto"
        },
        "zero_minutes": {
            "pt-BR": "0 minutos",
            "en": "0 minutes",
            "es": "0 minuto"
        },
        "there_was_a_problem_saving_your_process": {
            "pt-BR": "Houve um problema ao salvar seu processo. Por favor, tente novamente ou entre em contato por",
            "en": "There was a problem saving your process. Please try again or contact us by",
            "es": "Hubo un problema al guardar su proceso."
        },
        "all_done": {
            "pt-BR": "Informações completas",
            "en": "All done!",
            "es": "Información completa"
        },
        "you_have_filled_in_all_necessary_info": {
            "pt-BR": "Você preencheu todas as informações necessárias desse processo",
            "en": "You have filled in all the necessary information for this process",
            "es": "Ha completado toda la información necesaria en este proceso."
        },
        "now_your_dashboard_can_show_more": {
            "pt-BR": "Agora seu dashboard poderá mostrar ainda mais detalhes da sua operação RPA",
            "en": "Now your dashboard can show even better graphs of your RPA operation",
            "es": "Ahora su panel de control puede mostrar aún más detalles de su operación de RPA"
        },
        "you_have_not_completed_all_necessary_info": {
            "pt-BR": "Você não preencheu todas as informações necessárias para seu dashboard mostrar detalhes desta operação RPA",
            "en": "You have not filled in all the necessary information for your dashboard to show details of this Process",
            "es": "No ha completado toda la información que necesita para su panel de control Mostrar detalles de esta operación de RPA"
        },
        "you_can_edit_and_add_more_process_info": {
            "pt-BR": "Você pode editar o processo para adicionar mais informações a qualquer momento",
            "en": "You may edit the process to add more information at any time",
            "es": "Puede editar el proceso para agregar más información en cualquier momento."
        },
        "process_name": {
            "pt-BR": "Nome do Processo",
            "en": "Process Name",
            "es": "Nombre del proceso"
        },
        "nickname": {
            "pt-BR": "Apelido",
            "en": "Nickname",
            "es": "Apellido"
        },
        "employees": {
            "pt-BR": "Colaboradores",
            "en": "Employees",
            "es": "Contribuyentes"
        },
        "quantity": {
            "pt-BR": "Quantidade",
            "en": "Quantity",
            "es": "La cantidad"
        },
        "hours_by_day": {
            "pt-BR": "Horas/dia",
            "en": "Working hours per day",
            "es": "Horas / día"
        },
        "time_on_task": {
            "pt-BR": "Tempo na tarefa",
            "en": "Time worked in task",
            "es": "Tiempo de trabajo"
        },
        "invite_to_rpa_dashboard": {
            "pt-BR": "Convidar para o Dashboard RPA",
            "en": "Invite to RPA Dashboard",
            "es": "Invitar a Dashboard RPA"
        },
        "user_not_found": {
            "pt-BR": "Usuário não encontrado",
            "en": "User not found",
            "es": "Usuario no encontrado"
        },
        "are_you_sure_this_user_works_with_you": {
            "pt-BR": "Tem certeza que esse usuário trabalha com você?",
            "en": "Are you sure this user works with you?",
            "es": "¿Estás seguro de que este usuario trabaja contigo?"
        },
        "error_updating_users": {
            "pt-BR": "Erro atualizando usuários",
            "en": "Error updating users",
            "es": "Error al actualizar los usuarios"
        },
        "data_complete": {
            "pt-BR": "Informações Completas",
            "en": "Data Complete",
            "es": "Información completa"
        },
        "incomplete_data": {
            "pt-BR": "Informações Incompletas",
            "en": "Incomplete Data",
            "es": "Información incompleta"
        },
        "initial_date": {
            "pt-BR": "Data inicial",
            "en": "Initial date",
            "es": "La fecha de inicio"
        },
        "final_date": {
            "pt-BR": "Data final",
            "en": "Final date",
            "es": "Fecha final"
        },
        "free_trial": {
            "pt-BR": "Teste grátis",
            "en": "Free trial",
            "es": "Prueba gratis"
        },
        "type_your_password": {
            "pt-BR": "Digite sua senha",
            "en": "Type your password",
            "es": "Escribe tu contraseña"
        },
        "unlimited_access": {
            "pt-BR": "acesso ilimitado",
            "en": "unlimited access",
            "es": "acceso ilimitado"
        },
        "begin_button": {
            "pt-BR": "Começar",
            "en": "Start",
            "es": "Empezar"
        },
        "decrease_error_avoid_delays": {
            "pt-BR": "Diminui erros e evita atrasos, cortes e multas",
            "en": "Decreases errors and avoids delays, cuts and fines",
            "es": "Disminuye los errores y evita retrasos, cortes y multas."
        },
        "centralizes_information_one_place": {
            "pt-BR": "Centraliza suas informações em um só lugar",
            "en": "Centralizes your information in one place",
            "es": "Centraliza tu información en un solo lugar"
        },
        "choose_services_to_test": {
            "pt-BR": "Adicione licenças aos serviços que gostaria de testar.",
            "en": "Add licenses to the services you would like to test.",
            "es": "Agregue licencias a los servicios que le gustaría probar."
        },
        "registration_choosing_subtitle": {
            "pt-BR": "Você poderá adicionar novos serviços à sua conta depois.",
            "en": "You can add new services to your account later.",
            "es": "Puede agregar nuevos servicios a su cuenta más adelante."
        },
        "manage_your_rpa_with_our_dashboard": {
            "pt-BR": "Gerencie sua operação RPA UiPath com o nosso dashboard",
            "en": "Manage your RPA UiPath operation with our dashboard",
            "es": "Administre su operación de UIPATH RPA con nuestro tablero"
        },
        "test_selected_services": {
            "pt-BR": "Testar serviços selecionados",
            "en": "Test selected services",
            "es": "Prueba de servicios seleccionados"
        },
        "choose_at_least_3_to_proceed": {
            "pt-BR": "Escolha pelo menos 3 para prosseguir",
            "en": "Choose at least 3 to proceed",
            "es": "Elija al menos 3 para proceder."
        },
        "track_compare_robots_insights_business": {
            "pt-BR": "Acompanhe e compare seus robôs e processos, áreas e mais, tirando insights valiosos para o seu negócio",
            "en": "Track and compare your robots and processes, areas and more, gaining valuable insights for your business",
            "es": "Siga y compare sus robots y procesos, áreas y más, tomando información valiosa a su negocio"
        },
        "areas_and_processes": {
            "pt-BR": "Áreas e Processos",
            "en": "Areas and Processes",
            "es": "Áreas y procesos."
        },
        "areas_and_processes_subtitle": {
            "pt-BR": "Cadastre áreas, associe aos processos e crie apelidos para eles, facilitando a análise de dados e a comunicação da equipe",
            "en": "Register areas, associate them with processes and create nicknames for them, facilitating data analysis and team communication",
            "es": "Las áreas de registro, asocian los procesos y crean apodos para ellos, facilitando el análisis de datos y la comunicación del equipo."
        },
        "graphs_and_analytics": {
            "pt-BR": "Gráficos e Análises",
            "en": "Graphs and Analytics",
            "es": "Gráficos y análisis"
        },
        "graphs_and_analytics_subtitle": {
            "pt-BR": "Acompanhe horas trabalhadas por área (Colaborador x RPA), tempo de execução dos processos, ocupação de robôs e mais",
            "en": "Track hours worked by area (Employee x RPA), process execution time, robot occupation and more",
            "es": "Siga las horas trabajadas por el área (colaborador x RPA), el tiempo de ejecución del proceso, la ocupación de robots y más"
        },
        "integration_with_uipath_orchestrator": {
            "pt-BR": "Integração com o Orquestrador UiPath",
            "en": "Integration with UiPath Orchestrator",
            "es": "Integración con el Orcherator de Uipath."
        },
        "integration_with_uipath_orchestrator_subtitle": {
            "pt-BR": "Não é preciso cadastrar novos processos manualmente. As informações são recebidas diretamente do seu orquestrador UiPath e os dados atualizados em tempo real",
            "en": "It is not necessary to register new processes manually. Information is received directly from your UiPath Orchestrator and the data is updated in real time",
            "es": "No es necesario registrar nuevos procesos manualmente."
        },
        "end_free_trial_warning_1": {
            "pt-BR": "Parece que seu período de teste chegou ao fim",
            "en": "Looks like your trial period has come to an end",
            "es": "Parece que su período de prueba ha llegado a su fin."
        },
        "check_our_plans": {
            "pt-BR": "Confira nossos planos",
            "en": "Check out our plans",
            "es": "Echa un vistazo a nuestros planes"
        },
        "end_free_trial_warning_2": {
            "pt-BR": "para continuar utilizando o Smarthis Hub",
            "en": "to continue using Smarthis Hub",
            "es": "Para continuar usando SmartThis Hub"
        },
        "end_free_trial_warning_3": {
            "pt-BR": "Confira quanto tempo você economizou e escolha um plano para continuar usando o Smarthis Hub",
            "en": "Check how much time you've saved and choose a plan to continue using Smarthis Hub",
            "es": "Echa un vistazo al tiempo que guardó y elija un plan para continuar usando Smarthis Hub"
        },
        "end_free_trial_button": {
            "pt-BR": "Ver Meu Resumo e Planos Disponíveis",
            "en": "View My Summary and Available Plans",
            "es": "Ver mi resumen y planes disponibles."
        },
        "you_dont_have_services_yet": {
            "pt-BR": "Você ainda não tem serviços",
            "en": "You don't have services yet",
            "es": "Todavía no tienes servicios."
        },
        "to_gain_access_talk_to_your_administrator_or_contact_us_via": {
            "pt-BR": "Para ter acesso, converse com o seu administrador ou entre em contato por",
            "en": "To gain access, talk to your administrator or contact us via",
            "es": "Para acceder, hable con su administrador o contacto."
        },
        "to_hire_a_plan": {
            "pt-BR": "para contratar um plano",
            "en": "to hire a plan",
            "es": "Alquilar un plan"
        },
        "service_added_successfully": {
            "pt-BR": "Serviço adicionado com sucesso",
            "en": "Service added successfully",
            "es": "Servicio añadido con éxito"
        },
        "you_have_no_permission_to_perform_this_action": {
            "pt-BR": "Você não tem permissão para executar essa ação",
            "en": "You have no permission to perform this action",
            "es": "No se le permite realizar esta acción."
        },
        "summary_trial_period": {
            "pt-BR": "Resumo do seu período de teste",
            "en": "Summary of your trial period",
            "es": "Resumen de su período de prueba"
        },
        "plan_and_services": {
            "pt-BR": "Plano e serviços",
            "en": "Plan and services",
            "es": "Plan y Servicios"
        },
        "payment_data": {
            "pt-BR": "Dados de Pagamento",
            "en": "Payment data",
            "es": "Datos de pago"
        },
        "your_free_trial_period_ended": {
            "pt-BR": "Seu período de teste chegou ao fim",
            "en": "Your trial period has come to an end",
            "es": "Su período de prueba ha llegado a su fin."
        },
        "your_free_trial_period_ended_subtitle": {
            "pt-BR": "Veja o resumo do seu período de teste e confira o plano recomendado para continuar aproveitando todas as vantagens que a sua empresa precisa",
            "en": "See the summary of your trial period and check out the recommended plan to continue enjoying all the benefits your business needs",
            "es": "Consulte el resumen de su período de prueba y verifique el plan recomendado para continuar aprovechando todas las ventajas que su empresa necesita"
        },
        "you_saved": {
            "pt-BR": "Você economizou",
            "en": "You saved",
            "es": "Salvaste"
        },
        "without_the_hub_you_would_take": {
            "pt-BR": "Sem o Hub você levaria",
            "en": "Without the Hub you would take",
            "es": "Sin el centro que tomarías"
        },
        "with_the_hub_you_took": {
            "pt-BR": "Com o Hub, você levou ",
            "en": "With the Hub, you took",
            "es": "Con el centro, tomaste"
        },
        "queries_lowercase": {
            "pt-BR": "consultas",
            "en": "queries",
            "es": "consultas"
        },
        "continue_with": {
            "pt-BR": "Continuar com",
            "en": "Continue with",
            "es": "Seguir con"
        },
        "or_compare_all_plans": {
            "pt-BR": "Ou compare todos os planos",
            "en": "Or compare all plans",
            "es": "O comparar todos los planes"
        },
        "or_compare_with_other_plans": {
            "pt-BR": "Ou compare com outros planos",
            "en": "Or compare with other plans",
            "es": "O comparar con otros planes"
        },
        "discount_on_annual_payment": {
            "pt-BR": "de desconto no pagamento anual",
            "en": "discount on annual payment",
            "es": "Descuento en el pago anual"
        },
        "starter_plan_subtitle": {
            "pt-BR": "Ideal para dar início a transformação digital",
            "en": "Ideal for starting the digital transformation",
            "es": "Ideal para iniciar la transformación digital."
        },
        "advanced_plan_subtitle": {
            "pt-BR": "Ideal para um departamento ou pequena empresa",
            "en": "Ideal for a department or small business",
            "es": "Ideal para un pequeño departamento de empresa."
        },
        "business_plan_subtitle_1": {
            "pt-BR": "Monte um",
            "en": "Build a",
            "es": "Andar en"
        },
        "bespoke_plan": {
            "pt-BR": "plano sob medida",
            "en": "bespoke plan",
            "es": "hecho a medida"
        },
        "business_plan_subtitle_2": {
            "pt-BR": "e leve a sua empresa ainda mais longe",
            "en": "and take your company even further",
            "es": "y lleva a tu empresa aún más lejos"
        },
        "continue_with_this_plan": {
            "pt-BR": "Continuar com este plano",
            "en": "Continue with this plan",
            "es": "Continuar con este plan."
        },
        "choose_this_plan": {
            "pt-BR": "Escolher este plano",
            "en": "Choose this plan",
            "es": "Elige este plan"
        },
        "continue_and_receive_evaluation": {
            "pt-BR": "Continuar e receber avaliação",
            "en": "Continue and receive evaluation",
            "es": "Continuar y recibir evaluación."
        },
        "receive_evaluation": {
            "pt-BR": "Receber avaliação",
            "en": "Receive evaluation",
            "es": "Recibir"
        },
        "available_to_choose_any_service": {
            "pt-BR": "disponível para escolher qualquer serviço",
            "en": "available to choose any service",
            "es": "Disponible para elegir cualquier servicio"
        },
        "available_to_hire_different_services": {
            "pt-BR": "disponíveis para contratar diferentes serviços",
            "en": "available to hire different services",
            "es": "Disponible para contratar diferentes servicios."
        },
        "monthly_for_licenses": {
            "pt-BR": "mensais por licenças",
            "en": "monthly for licenses",
            "es": "mensual por licencias"
        },
        "invite_your_team": {
            "pt-BR": "Convide sua equipe",
            "en": "Invite your team",
            "es": "Invita a tu equipo"
        },
        "according_to_your_need": {
            "pt-BR": "de acordo com a sua necessidade",
            "en": "according to your need",
            "es": "De acuerdo a tu necesidad"
        },
        "more_limit_options_of_consultations": {
            "pt-BR": "Mais opções de limites de consultas",
            "en": "More limit options of consultations",
            "es": "Más opciones para los límites de consulta."
        },
        "get_17%_off": {
            "pt-BR": "Ganhe 17% de desconto",
            "en": "Get 17% off",
            "es": "Ganar 17% de descuento"
        },
        "17%_off": {
            "pt-BR": "17% de desconto",
            "en": "17% off",
            "es": "17% de descuento"
        },
        "annual_billing": {
            "pt-BR": "na cobrança anual",
            "en": "annual billing",
            "es": "En cobro anual"
        },
        "recommended_capitalized": {
            "pt-BR": "recomendado",
            "en": "recommended",
            "es": "recomendado"
        },
        "need_help_choosing_your_plan": {
            "pt-BR": "Precisa de ajuda para escolher o seu plano",
            "en": "Need help choosing your plan",
            "es": "Necesita ayuda para elegir su plan"
        },
        "can_i_change_my_plan_after_hiring": {
            "pt-BR": "Posso alterar meu plano após a contratação",
            "en": "Can I change my plan after hiring",
            "es": "Puedo cambiar mi plan después de la contratación"
        },
        "can_i_change_my_plan_after_hiring_answer_1": {
            "pt-BR": "Sim, é possível editar seu plano a qualquer momento em",
            "en": "Yes, you can edit your plan at any time in",
            "es": "Sí, es posible editar su plan en cualquier momento en"
        },
        "can_i_change_my_plan_after_hiring_answer_2": {
            "pt-BR": "Configurações > Plano",
            "en": "Settings > Plan",
            "es": "Configuración> Plan"
        },
        "what_forms_of_payment_hub_accepts": {
            "pt-BR": "Quais formas de pagamento o Smarthis Hub aceita",
            "en": "What forms of payment does Smarthis Hub accept",
            "es": "¿Qué formas de pago aceptan el SmartThis HUB?"
        },
        "what_forms_of_payment_hub_accepts_answer_1": {
            "pt-BR": "É possível pagar pela sua assinatura no Smarthis Hub com cartão de crédito ou por boleto. Você fornece as informações no momento da contratação do seu plano e logo depois recebe um e-mail informando se o pagamento foi processado. No caso de pagamento por boleto, este e-mail pode demorar até 24h.",
            "en": "You can pay for your subscription on Smarthis Hub by credit card or by bank transfer. You provide the information when you sign up for your plan and shortly afterward you receive an email informing you if the payment has been processed. In the case of payment by boleto, this email can take up to 24h.",
            "es": "Puede pagar su firma en SmartThis Hub con tarjeta de crédito o boleto."
        },
        "what_forms_of_payment_hub_accepts_answer_2": {
            "pt-BR": "Todos os pagamentos realizados no Smarthis Hub são processado pela",
            "en": "All payments made on Smarthis Hub are processed by",
            "es": "Todos los pagos realizados en SmartThis Hub se procesan por"
        },
        "will_i_receive_an_invoice_after_hiring": {
            "pt-BR": "Posso trocar os serviços que contratei",
            "en": "Can I change the services I have hired",
            "es": "Puedo intercambiar los servicios que contraté."
        },
        "will_i_receive_an_invoice_after_hiring_answer": {
            "pt-BR": "Sim, você poderá trocar seus serviços por quaisquer outros acessando nosso catálogo na pagina Descobrir",
            "en": "Yes, you can exchange your services for any others by accessing our catalog on the Discover page",
            "es": "Sí, puede intercambiar sus servicios para cualquier otro accediendo a nuestro catálogo en la página para descubrir"
        },
        "or_get_2_months_free_subscribing": {
            "pt-BR": "Ou ganhe 2 meses grátis assinando o plano anual por",
            "en": "Or get 2 free months by subscribing to the annual plan for",
            "es": "O ganar 2 meses firmando gratis el plan anual para"
        },
        "set_up_your_plan_receive_personalized_assessment": {
            "pt-BR": "Configure seu plano e receba uma avaliação personalizada",
            "en": "Set up your plan and receive a personalized assessment",
            "es": "Configure su plan y reciba una evaluación personalizada."
        },
        "yearly": {
            "pt-BR": "Anual",
            "en": "Yearly",
            "es": "Anual"
        },
        "which_licenses_keep_plan": {
            "pt-BR": "Quais licenças deseja manter no seu plano?",
            "en": "Which licenses do you want to keep in your plan?",
            "es": "¿Qué licencias desean mantener en su plan?"
        },
        "build_bespoke_plan_receie_our_assessment_email": {
            "pt-BR": "Monte um plano sob medida e receba a nossa avaliação por e-mail",
            "en": "Build a bespoke plan and receive our assessment via email",
            "es": "Monte un plan personalizado y reciba nuestra evaluación por correo electrónico."
        },
        "tailor_made_plan_needs": {
            "pt-BR": "Plano sob medida de acordo com as suas necessidades",
            "en": "Tailor-made plan according to your needs",
            "es": "Avión de tamaño según sus necesidades."
        },
        "charge": {
            "pt-BR": "Cobrança",
            "en": "Charge",
            "es": "Cargo"
        },
        "monthly_consultations": {
            "pt-BR": "consultas mensais",
            "en": "monthly consultations",
            "es": "consultas mensuales"
        },
        "monthly_consultations_by_license": {
            "pt-BR": "consultas mensais por licença",
            "en": "monthly consultations by license",
            "es": "Consultas mensuales por licencia."
        },
        "sign_plan": {
            "pt-BR": "Assinar Plano",
            "en": "Sign Plan",
            "es": "Firmar"
        },
        "not_used": {
            "pt-BR": "Não utilizado",
            "en": "Not used",
            "es": "No utilizado"
        },
        "number_of_licenses": {
            "pt-BR": "Quantidade de licenças",
            "en": "Number of licenses",
            "es": "Cantidad de licencias"
        },
        "request_evaluation": {
            "pt-BR": "Solicitar avaliação",
            "en": "Request evaluation",
            "es": "Evaluación de solicitud"
        },
        "you_can_choose_up_to": {
            "pt-BR": "Você pode escolher até",
            "en": "You can choose up to",
            "es": "Puedes elegir hasta"
        },
        "unlimited": {
            "pt-BR": "ilimitadas",
            "en": "unlimited",
            "es": "ilimitado"
        },
        "you_will_able_exchange_service_no_cost": {
            "pt-BR": "Você poderá trocar seus serviços por outros a qualquer momento sem custo extra",
            "en": "You will be able to exchange your services for others at any time at no extra cost",
            "es": "Puede intercambiar sus servicios por otros en cualquier momento sin costo adicional"
        },
        "the_plan": {
            "pt-BR": "O Plano",
            "en": "The Plan",
            "es": "El plan"
        },
        "entitles_you_to": {
            "pt-BR": "dá direito a",
            "en": "entitles you to",
            "es": "da derecho a"
        },
        "for_more_licenses_choose_business": {
            "pt-BR": "Para mais licenças, escolha o plano Business",
            "en": "For more licenses, choose the Business plan",
            "es": "Para más licencias, elija el plan de negocios."
        },
        "per_month": {
            "pt-BR": "por mês",
            "en": "per month",
            "es": "por mes"
        },
        "value": {
            "pt-BR": "Valor",
            "en": "Value",
            "es": "Valor"
        },
        "waiting_evaluation": {
            "pt-BR": "Aguardando Avaliação",
            "en": "Waiting Evaluation",
            "es": "Evaluación de la calificación"
        },
        "plan_details": {
            "pt-BR": "Detalhes do Plano",
            "en": "Plan Details",
            "es": "Detalles del plan."
        },
        "services_dashboards_changed_extra_charges": {
            "pt-BR": "Serviços e Dashboards contratados poderão ser alterados pelo contratante sem cobranças extras",
            "en": "Services and Dashboards contracted may be changed by the contracting party without extra charges",
            "es": "Los servicios y los paneles contratados pueden ser modificados por el contratista sin cargos adicionales."
        },
        "successfully_contracted_plan": {
            "pt-BR": "Plano contratado com sucesso",
            "en": "Successfully contracted plan",
            "es": "Planifica con éxito"
        },
        "you_will_soon_receive_evaluation_email": {
            "pt-BR": "Em breve você receberá nossa avaliação por e-mail",
            "en": "You will soon receive our evaluation by email",
            "es": "Pronto recibirá nuestra evaluación por correo electrónico."
        },
        "you_can_now_use_your_services_again": {
            "pt-BR": "Você já pode voltar a utilizar os seus serviços",
            "en": "You can now use your services again",
            "es": "Pronto recibirá nuestra evaluación por correo electrónico."
        },
        "use_my_services": {
            "pt-BR": "Utilizar Meus Serviços",
            "en": "Use My Services",
            "es": "Usa mis servicios"
        },
        "service_under_maintenance": {
            "pt-BR": "Serviço em manutenção",
            "en": "Service under maintenance",
            "es": "Servicio de mantenimiento"
        },
        "will_soon_be_back": {
            "pt-BR": "Em breve ele estará de volta",
            "en": "Will soon be back",
            "es": "Pronto volverá"
        },
        "dont_worry_will_soon_be_back": {
            "pt-BR": "Não se preocupe, em breve ele estará de volta e você receberá notificação",
            "en": "Don't worry, it will be back soon and you'll receive notification",
            "es": "No se preocupe, pronto volverá y recibirá notificación."
        },
        "back_to_my_services": {
            "pt-BR": "Voltar para Meus Serviços",
            "en": "Back to My Services",
            "es": "De vuelta a mis servicios"
        },
        "notify_me_when_available": {
            "pt-BR": "Avise-me quando estiver disponível",
            "en": "Notify me when available",
            "es": "Notifíqueme cuando esté disponible"
        },
        "you_will_be_notified": {
            "pt-BR": "Você será notificado",
            "en": "You will be notified",
            "es": "Serás notificado"
        },
        "requested_automation_does_not_exist": {
            "pt-BR": "A automação solicitada não existe",
            "en": "The requested automation does not exist",
            "es": "La automatización solicitada no existe."
        },
        "your_service_is_under_maintenance": {
            "pt-BR": "Seu serviço está em manutenção",
            "en": "Your service is under maintenance",
            "es": "Su servicio está en mantenimiento."
        },
        "your_service": {
            "pt-BR": "O seu serviço",
            "en": "Your service",
            "es": "Tu servicio"
        },
        "is_under_maintenance": {
            "pt-BR": "está em manutenção",
            "en": "is under maintenance",
            "es": "Está en mantenimiento"
        },
        "during_this_period_not_run_models": {
            "pt-BR": "Durante este período, não será possível executar os seus modelos",
            "en": "During this period, you will not be able to run your models",
            "es": "Durante este período, no podrá ejecutar sus modelos."
        },
        "as_soon_your_service_available_notified": {
            "pt-BR": "Assim que seu serviço estiver disponível novamente, você receberá um novo e-mail avisando",
            "en": "As soon as your service is available again, you will receive a new email notifying you",
            "es": "Tan pronto como su servicio esté disponible nuevamente, recibirá una nueva advertencia de correo electrónico"
        },
        "your_service_has_been_updated": {
            "pt-BR": "Seu serviço foi atualizado",
            "en": "Your service has been updated",
            "es": "Su servicio fue actualizado"
        },
        "has_been_updated_is_available_for_use": {
            "pt-BR": "foi atualizado e já está disponível para uso no seu Smarthis Hub",
            "en": "has been updated and is now available for use on your Smarthis Hub",
            "es": "se ha actualizado y ya está disponible para su uso en su HUB SMARTTHIS"
        },
        "start_using": {
            "pt-BR": "Começar a usar",
            "en": "Start using",
            "es": "Empieza a usar"
        },
        "hire_service": {
            "pt-BR": "Contratar serviço",
            "en": "Hire service",
            "es": "Servicio de alquiler"
        },
        "the_service": {
            "pt-BR": "O serviço",
            "en": "The service",
            "es": "El servicio"
        },
        "has_been_updated_is_available": {
            "pt-BR": "foi atualizado e já está disponível",
            "en": "has been updated and is now available",
            "es": "Se ha actualizado y ya está disponible."
        },
        "access_hub_to_finalize_start_using": {
            "pt-BR": "Acesse o Smarthis Hub para finalizar a contratação e começar a utilizar",
            "en": "Access Smarthis Hub to finalize the contract and start using",
            "es": "Accede a Smarthis Hub para finalizar la contratación y comenzar a usar"
        },
        "service_available_for_contracting": {
            "pt-BR": "Serviço disponível para contratação",
            "en": "Service available for contracting",
            "es": "Servicio disponible para la contratación."
        },
        "you_can_use_up_to": {
            "pt-BR": "Você pode usar até",
            "en": "You can use up to",
            "es": "Puedes usar hasta que"
        },
        "you_have_extra_package_queries": {
            "pt-BR": "Você possui pacote de consultas extras e pode usar até",
            "en": "You have an extra queries package and you can even use",
            "es": "Usted tiene un paquete de consultas adicionales y puede usar hasta que"
        },
        "in_your_business_plan_1": {
            "pt-BR": "No seu plano business, personalizado de acordo com as necessidades da sua empresa, você possui",
            "en": "In your business plan, customized according to your company's needs, you have",
            "es": "En su plan de negocios, personalizado de acuerdo con las necesidades de su empresa, usted posee"
        },
        "in_your_business_plan_2": {
            "pt-BR": "para utilizar ou distribuir entre sua equipe e",
            "en": "to use or distribute among your team and",
            "es": "usar o distribuir entre su equipo y"
        },
        "unlimited_queries": {
            "pt-BR": "consultas ilimitadas",
            "en": "unlimited queries",
            "es": "Consultas ilimitadas"
        },
        "runtime_by_process": {
            "pt-BR": "Horas RPA por Processos",
            "en": "Runtime RPA by Process",
            "es": "Tiempo de RPA por procesos."
        },
        "runtime_by_business_area": {
            "pt-BR": "Horas RPA por Áreas",
            "en": "Runtime RPA by Business Area",
            "es": "Tiempo de RPA por áreas"
        },
        "administrative": {
            "pt-BR": "Administrativo",
            "en": "Administrative",
            "es": "Administrativo"
        },
        "customer_service": {
            "pt-BR": "Atendimento ao Cliente",
            "en": "Customer service",
            "es": "Atención al cliente"
        },
        "center_of_excellence_in_rpa": {
            "pt-BR": "Centro de Excelência (CoE) em RPA",
            "en": "Center of Excellence (CoE) in RPA",
            "es": "Centro de Excelencia (COE) en RPA"
        },
        "purchasing_and_supplies": {
            "pt-BR": "Compras e Suprimentos",
            "en": "Purchasing and Supplies",
            "es": "Compras y suministros"
        },
        "consultancy": {
            "pt-BR": "Consultoria",
            "en": "Consultancy",
            "es": "Consultoría"
        },
        "finance_and_accounting": {
            "pt-BR": "Finanças e Contabilidade",
            "en": "Finance and Accounting",
            "es": "Finanzas y Contabilidad"
        },
        "supervisor": {
            "pt-BR": "Fiscal",
            "en": "Supervisor",
            "es": "Supervisor"
        },
        "operations": {
            "pt-BR": "Operações",
            "en": "Operations",
            "es": "Operaciones"
        },
        "human_resources": {
            "pt-BR": "Recursos Humanos",
            "en": "Human Resources",
            "es": "Recursos humanos"
        },
        "information_technology": {
            "pt-BR": "Tecnologia da Informação",
            "en": "Information Technology",
            "es": "Tecnología de la informacion"
        },
        "another_area": {
            "pt-BR": "Outra área",
            "en": "another area",
            "es": "Otra área"
        },
        "analyst": {
            "pt-BR": "Analista",
            "en": "Analyst",
            "es": "Analista"
        },
        "manager": {
            "pt-BR": "Gerente",
            "en": "Manager",
            "es": "Gerente"
        },
        "director": {
            "pt-BR": "Diretor",
            "en": "Director",
            "es": "Principal"
        },
        "specialist": {
            "pt-BR": "Especialista",
            "en": "Specialist",
            "es": "Especialista"
        },
        "other": {
            "pt-BR": "Outro",
            "en": "Other",
            "es": "Otro"
        },
        "404_message": {
            "pt-BR": "Talvez esta página tenha mudado? Foi excluída? Está se escondendo em quarentena? Nunca existiu em primeiro lugar?",
            "en": "Maybe this page moved? Got deleted? Is hiding out in quarantine? Never existed in the first place?",
            "es": "Tal vez esta página ha cambiado?"
        },
        "lets_go": {
            "pt-BR": "Vamos para a",
            "en": "Let's go",
            "es": "Vamos a ir a la"
        },
        "home_initial_page": {
            "pt-BR": "página inicial",
            "en": "home",
            "es": "página de inicio"
        },
        "and_try_from_there": {
            "pt-BR": "e tentar a partir daí",
            "en": "and try from there",
            "es": "página de inicio"
        },
        "unexpected_error": {
            "pt-BR": "Erro inesperado",
            "en": "Unexpected Error",
            "es": "error inesperado"
        },
        "same_cpf_cnpj_used_on_the_cabedelo_city_hall_website": {
            "pt-BR": "Mesmo CPF/CNPJ utilizado no site da Prefeitura de Cabedelo",
            "en": "Same CPF/CNPJ used on the Cabedelo City Hall website",
            "es": "Incluso CPF / CNPJ utilizado en el sitio web de la Prefectura de Cabedelo"
        },
        "same_password_used_on_cabedelo_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Cabedelo",
            "en": "Same password used on Cabedelo City Hall website",
            "es": "La misma contraseña utilizada en el sitio web de la prefectura de Cabedelo."
        },
        "credentials_of_cabedelo_city_hall": {
            "pt-BR": "Credenciais da Prefeitura de Cabedelo",
            "en": "Credentials of Cabedelo City Hall",
            "es": "Para utilizar este servicio, debe proporcionar sus credenciales de la Prefectura de Cabedelo."
        },
        "only_numbers": {
            "pt-BR": "Apenas números",
            "en": "Only numbers",
            "es": "Sólo números"
        },
        "sign": {
            "pt-BR": "Assinar",
            "en": "Assinar",
            "es": "Para firmar"
        },
        "cnpj": {
            "pt-BR": "CNPJ",
            "en": "CNPJ",
            "es": "Cnpj"
        },
        "telephone": {
            "pt-BR": "Telefone",
            "en": "Telephone",
            "es": "Teléfono"
        },
        "company_data": {
            "pt-BR": "Dados da Empresa",
            "en": "Company Data",
            "es": "Datos de la empresa"
        },
        "address": {
            "pt-BR": "Endereço",
            "en": "Address",
            "es": "Habla a"
        },
        "payment": {
            "pt-BR": "Pagamento",
            "en": "Payment",
            "es": "Pago"
        },
        "proceed": {
            "pt-BR": "Prosseguir",
            "en": "Proceed",
            "es": "Continuar"
        },
        "invoices_and_subscription_information_will_be_sent_to_this_email": {
            "pt-BR": "Faturas e informações da assinatura serão enviadas para este e-mail",
            "en": "Invoices and subscription information will be sent to this email",
            "es": "Las facturas y la información de suscripción se enviarán a este correo electrónico."
        },
        "zip_code": {
            "pt-BR": "CEP",
            "en": "CEP",
            "es": "Código postal"
        },
        "consult_my_zip_code": {
            "pt-BR": "Consultar meu CEP",
            "en": "Consult my zip code",
            "es": "Consulte mi código postal"
        },
        "street": {
            "pt-BR": "Logradouro",
            "en": "Street",
            "es": "Lugar público"
        },
        "avenue_etc": {
            "pt-BR": "Rua, Avenida...",
            "en": "Avenue...",
            "es": "Avenida calle ..."
        },
        "number": {
            "pt-BR": "Número",
            "en": "Number",
            "es": "Número"
        },
        "complement": {
            "pt-BR": "Complemento",
            "en": "Complement",
            "es": "Complemento"
        },
        "district": {
            "pt-BR": "Bairro",
            "en": "District",
            "es": "Barrio"
        },
        "city": {
            "pt-BR": "Cidade",
            "en": "City",
            "es": "Ciudad"
        },
        "uf_capital": {
            "pt-BR": "UF",
            "en": "UF",
            "es": "UF"
        },
        "understand_what_times_throughout_the_day_your_robots_are_working_the_most": {
            "pt-BR": "Entenda em quais horários ao longo do dia os seus robôs estão trabalhando mais.",
            "en": "Understand what times throughout the day your robots are working the most.",
            "es": "Comprende qué ocasiones a lo largo del día tus robots están trabajando más duro."
        },
        "company": {
            "pt-BR": "Empresa",
            "en": "Company",
            "es": "Empresa"
        },
        "your_bespoke_plan": {
            "pt-BR": "Seu plano sob medida",
            "en": "Your bespoke plan",
            "es": "Tu plano de tamaño"
        },
        "to_take_your_company_even_further": {
            "pt-BR": "para levar sua empresa ainda mais longe",
            "en": "to take your company even further",
            "es": "para llevar a su empresa aún más lejos"
        },
        "from_your_order_we_made_a_personalized_evaluation": {
            "pt-BR": "A partir do seu pedido, fizemos uma avaliação personalizada",
            "en": "From your order, we made a personalized evaluation",
            "es": "Desde su solicitud, hicimos una evaluación personalizada."
        },
        "your_business_plan": {
            "pt-BR": "Seu Plano Business",
            "en": "Your Business Plan",
            "es": "Su plan de negocios"
        },
        "you_chose": {
            "pt-BR": "Você escolheu",
            "en": "You chose",
            "es": "Usted escogió"
        },
        "payment_every_year": {
            "pt-BR": "Pagamento a cada ano",
            "en": "Payment every year",
            "es": "Pago cada año"
        },
        "payment_every_month": {
            "pt-BR": "Pagamento a cada mês",
            "en": "Payment every month",
            "es": "Pago cada mes"
        },
        "sign_anual_plan": {
            "pt-BR": "Assinar plano anual",
            "en": "Sign anual plan",
            "es": "Firmar plan anual"
        },
        "sign_monthly_plan": {
            "pt-BR": "Assinar plano mensal",
            "en": "Sign monthly plan",
            "es": "Señal"
        },
        "to_per": {
            "pt-BR": "por",
            "en": "to",
            "es": "por"
        },
        "year": {
            "pt-BR": "ano",
            "en": "year",
            "es": "año"
        },
        "to_use_in_the_services_you_want": {
            "pt-BR": "para usar nos serviços que quiser",
            "en": "to use in the serivces you want",
            "es": "Para usar en los servicios que quieras."
        },
        "still_not_sure_if_this_is_what_you_need": {
            "pt-BR": "Ainda não sabe se é o que você precisa?",
            "en": "Still not sure if this is what you need?",
            "es": "¿Todavía no sabes si es lo que necesitas?"
        },
        "we_will_be_happy_to_help_you_find_the_ideal_plan_for_your_business": {
            "pt-BR": "Ficaremos felizes em te ajudar a encontrar o plano ideal para o seu negócio",
            "en": "We will be happy to help you find the ideal plan for your business",
            "es": "Estaremos encantados de ayudarlo a encontrar el plan ideal para su negocio."
        },
        "other_doubts_and_inquiries_are_also_very_welcome": {
            "pt-BR": "Outras dúvidas e questionamentos também são muito bem vindos",
            "en": "Other doubts and inquiries are also very welcome",
            "es": "Otras preguntas y preguntas también son muy bienvenidas."
        },
        "talk_with_us": {
            "pt-BR": "Fale Conosco",
            "en": "Contact Us",
            "es": "Hable con nosotros"
        },
        "your": {
            "pt-BR": "Seu",
            "en": "Your",
            "es": "Tu"
        },
        "my_dashboards": {
            "pt-BR": "Meus dashboards",
            "en": "my dashboards",
            "es": "Mis tableros"
        },
        "available_in_your_plan": {
            "pt-BR": "Disponível no seu plano",
            "en": "available in your plan",
            "es": "Disponible en su plan"
        },
        "install_your_rpa_dashboard_and_get_started": {
            "pt-BR": "Instale seu Dashboard de RPA e comece a usar",
            "en": "Install your RPA Dashboard and get started",
            "es": "Instale su panel de RPA y comience a usar"
        },
        "install": {
            "pt-BR": "Instalar",
            "en": "Install",
            "es": "Instalar en pc"
        },
        "what_analytics_impact_your_business": {
            "pt-BR": "Quais análises impactam o seu negócio?",
            "en": "What analytics impact your business?",
            "es": "¿Qué análisis afectan su negocio?"
        },
        "we_seek_to_improve_our_work_and_offer_more_solutions_to_our_customers": {
            "pt-BR": "Buscamos melhorar o nosso trabalho e oferecer mais soluções aos nossos clientes. Envie dúvidas, sugestões de melhorias, de gráficos e até de outros dashboards para",
            "en": "We seek to improve our work and offer more solutions to our customers. Send questions, suggestions for improvements, graphics and even other dashboards to",
            "es": "Buscamos mejorar nuestro trabajo y ofrecernos más soluciones a nuestros clientes."
        },
        "digital_transformation_as_your_company_needs": {
            "pt-BR": "Transformação Digital na medida que a sua empresa precisa, com",
            "en": "Digital Transformation as your company needs, with",
            "es": "Transformación digital como su negocio necesita, con"
        },
        "more_options_for_your_queries_limit": {
            "pt-BR": "mais opções para o seu limite de consultas",
            "en": "more options for your queries limit",
            "es": "Más opciones para su límite de consultas"
        },
        "for_licenses": {
            "pt-BR": "por licenças",
            "en": "for licenses",
            "es": "por licencia"
        },
        "edit_my_plan": {
            "pt-BR": "Editar meu plano",
            "en": "Edit my plan",
            "es": "Editar mi plan"
        },
        "plan_info_text_1": {
            "pt-BR": "Dê os primeiros passos na transformação digital, utilizando",
            "en": "Take the first steps in the digital transformation, using",
            "es": "Tome los primeros pasos en la transformación digital utilizando"
        },
        "in": {
            "pt-BR": "em",
            "en": "in",
            "es": "en"
        },
        "plan_info_text_2": {
            "pt-BR": "sem se preocupar com infraestrutura e licenças",
            "en": "without worrying about infrastructure and licenses",
            "es": "Sin preocuparse por la infraestructura y las licencias."
        },
        "and": {
            "pt-BR": "e",
            "en": "and",
            "es": "y"
        },
        "according_to_your_needs": {
            "pt-BR": "de acordo com as suas necessidades",
            "en": "according to your needs",
            "es": "Según sus necesidades"
        },
        "build_your_plan_and": {
            "pt-BR": "Monte seu plano e",
            "en": "Build your plan and",
            "es": "Monte su plan y"
        },
        "receive_our_evaluation_by_email": {
            "pt-BR": "receba nossa avaliação por e-mail",
            "en": "receive our evaluation by email",
            "es": "Obtenga nuestra evaluación por correo electrónico"
        },
        "change_plan": {
            "pt-BR": "Mudar de Plano",
            "en": "Change Plan",
            "es": "Cambio de Plan"
        },
        "unsupported_file": {
            "pt-BR": "Arquivo não suportado",
            "en": "Unsupported file",
            "es": "Archivo no admitido"
        },
        "file_was_not_received_error": {
            "pt-BR": "O arquivo não foi recebido. Por favor, Tente enviar novamente e caso não funcione, recarregue a página e tente mais uma vez",
            "en": "The file was not received. Please try uploading again and if it doesn't work, reload the page and try again",
            "es": "El archivo no fue recibido."
        },
        "not_all_columns_are_filled": {
            "pt-BR": "Nem todas as colunas foram preenchidas",
            "en": "Not all all columns are filled",
            "es": "No todas las columnas se llenaron"
        },
        "there_were_problems_with_the_following_fields": {
            "pt-BR": "Houveram problemas com os seguintes campos",
            "en": "There were problems with the following fields",
            "es": "Hubo problemas con los siguientes campos"
        },
        "there_was_problem_encrypting_your_file": {
            "pt-BR": "Ocorreu um problema ao criptografar seu arquivo",
            "en": "There was a problem encrypting your file",
            "es": "Hubo un problema cifrado tu archivo."
        },
        "invalid_credit_card_are_you_sure_typed_it_correctly": {
            "pt-BR": "Cartão de crédito inválido, tem certeza que você digitou corretamente?",
            "en": "Invalid credit card, are you sure you typed it correctly?",
            "es": "Tarjeta de crédito no válida, ¿está seguro de que usted escribió correctamente?"
        },
        "you_fill_in_the_upload_file_with_the_cnpj_that_you_want_to_issue_the_labor_debt_certificate_works_2": {
            "pt-BR": "Você preenche o arquivo de upload com o CNPJ que deseja realizar a emissão da Certidão de Débitos Trabalhistas para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar",
            "en": "You fill in the upload file with the CNPJ that you want to issue the Labor Debt Certificate to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Llene el archivo de carga con CNPJ que desea emitir el certificado de débitos de trabajo para configurar una registro."
        },
        "there_was_an_error_saving_your_profile": {
            "pt-BR": "houve um erro ao salvar seu perfil",
            "en": "there was an error saving your profile",
            "es": "Había un error al salvar tu perfil."
        },
        "your_profile_has_been_updated": {
            "pt-BR": "Seu perfil foi atualizado",
            "en": "Your profile has been updated",
            "es": "Tu perfil ha sido actualizado"
        },
        "line": {
            "pt-BR": "Linha",
            "en": "Line",
            "es": "Línea"
        },
        "lines": {
            "pt-BR": "Linhas",
            "en": "Lines",
            "es": "Líneas"
        },
        "integrated_with_your_uipath_operation": {
            "pt-BR": "Integrado com sua operação UiPath",
            "en": "Integrated with your UiPath operation",
            "es": "Integrado con su funcionamiento de UIPATH"
        },
        "spreadsheet_entered_does_not_belong_to_service": {
            "pt-BR": "A planilha inserida não é deste serviço",
            "en": "The spreadsheet entered does not belong to this service",
            "es": "La hoja de trabajo insertada no es de este servicio."
        },
        "confirm_your_email_address": {
            "pt-BR": "Confirme seu endereço de email",
            "en": "Confirm your email address",
            "es": "Confirme su dirección de correo electrónico"
        },
        "to_use_hub": {
            "pt-BR": "para usar o HUB",
            "en": "to use HUB",
            "es": "Usar el centro"
        },
        "click_the_button_below_to_verify_your_email_address": {
            "pt-BR": "Clique no botão abaixo para verificar o seu endereço de email",
            "en": "Click the button below to verify your email address",
            "es": "Haga clic en el botón de abajo para verificar su dirección de correo electrónico"
        },
        "verify_hub_account": {
            "pt-BR": "Verificar conta do HUB",
            "en": "Verify the HUB account",
            "es": "Revise la cuenta de HUB"
        },
        "your_email_has_been_successfully_verified": {
            "pt-BR": "Tudo certo! Seu e-mail foi verificado com sucesso",
            "en": "All right! Your email has been successfully verified",
            "es": "¡Todo cierto!"
        },
        "now_you_can_enjoy_hub_with_security": {
            "pt-BR": "Agora você já pode aproveitar o melhor do Hub com segurança e acesso a tudo o que você precisa",
            "en": "Now you can enjoy the best of the Hub with security and access to everything you need",
            "es": "Ahora ya puede aprovechar el mejor centro con seguridad y acceso a todo lo que necesita"
        },
        "back_to_hub": {
            "pt-BR": "Voltar para o Hub",
            "en": "Back to Hub",
            "es": "Volver al centro"
        },
        "first": {
            "pt-BR": "Primeira",
            "en": "First",
            "es": "Primero"
        },
        "previous": {
            "pt-BR": "Anterior",
            "en": "Previous",
            "es": "Anterior"
        },
        "next": {
            "pt-BR": "Próxima",
            "en": "Next",
            "es": "Proxima"
        },
        "next_male": {
            "pt-BR": "Próximo",
            "en": "Next",
            "es": "Proximo"
        },
        "page": {
            "pt-BR": "Página",
            "en": "Page",
            "es": "Página"
        },
        "integrate_smarthis_hub_services_with_your_business_operation": {
            "pt-BR": "Integre os serviços do Smarthis Hub com a operação da sua empresa",
            "en": "Integrate Smarthis Hub services with your business operation",
            "es": "Integrar los servicios de SmartThis Hub con la operación de su empresa."
        },
        "develop_with_our_api_to_create_and_manage_models_automatically": {
            "pt-BR": "Desenvolva com nossa API para criar e gerenciar modelos de forma automática e extrair resultados da forma mais eficiente para a sua empresa.",
            "en": "Develop with our API to create and manage models automatically and extract results in the most efficient way for your company.",
            "es": "Desarrolle con nuestra API para crear y administrar modelos automáticamente y extraer los resultados en la forma más eficiente de su empresa."
        },
        "go_to_documentation": {
            "pt-BR": "Ir para Documentação",
            "en": "Go to Documentation",
            "es": "Ir a la documentación"
        },
        "requirements": {
            "pt-BR": "Requisitos",
            "en": "Requirements",
            "es": "Requisitos"
        },
        "active_account_on_smarthis_hub": {
            "pt-BR": "Conta ativa no Smarthis Hub",
            "en": "Active account on Smarthis Hub",
            "es": "Cuenta activa en SmartThis Hub"
        },
        "to_use_the_hub_api_you_must_have_an_active_account": {
            "pt-BR": "Para utilizar a Hub API é necessário ter uma conta ativa no Smarthis Hub com os serviços que deseja acessar.",
            "en": "To use the Hub API you must have an active account on Smarthis Hub with the services you want to access.",
            "es": "Para usar la API del HUB, debe tener una cuenta activa en SmartHis Hub con los servicios que desea acceder."
        },
        "you_will_not_be_able_to_access_services_that_are_not_subscribed": {
            "pt-BR": "Não será possível acessar serviços que não estejam contratados pela sua conta Smarthis Hub.",
            "en": "You will not be able to access services that are not subscribed to by your Smarthis Hub account.",
            "es": "No podrá acceder a los servicios que no son contratados por su cuenta de SmartThis Hub."
        },
        "input_data_and_file_upload": {
            "pt-BR": "Dados de entrada e upload de arquivos",
            "en": "Input data and file upload",
            "es": "Datos de entrada y carga."
        },
        "in_order_for_the_services_to_be_performed_it_is_necessary_to_provide_some_data_which_varies_from_service": {
            "pt-BR": "Para que os serviços sejam executados, é necessário fornecer alguns dados que variam de serviço para serviço.",
            "en": "In order for the services to be performed, it is necessary to provide some data which varies from service to service.",
            "es": "Para que se ejecuten servicios, es necesario proporcionar algunos datos que van desde el servicio hasta el servicio."
        },
        "you_can_use_our_spreadsheet_templates_or_set_up_a_csv_following_the_necessary_standards": {
            "pt-BR": "Você pode utilizar os nossos modelos de planilhas ou configurar um CSV seguindo os padrões necessários.",
            "en": "You can use our spreadsheet templates or set up a CSV following the necessary standards.",
            "es": "Puede usar nuestra hoja de cálculo o configurar las registros de CSV siguiendo los estándares requeridos."
        },
        "view_data_and_input_files": {
            "pt-BR": "Ver Dados e Arquivos de Entrada",
            "en": "View Data and Input Files",
            "es": "Ver datos y archivos"
        },
        "support": {
            "pt-BR": "Suporte",
            "en": "Support",
            "es": "Soporte"
        },
        "access_issues": {
            "pt-BR": "Acessar Issues",
            "en": "Access Issues",
            "es": "Asunto"
        },
        "help_center": {
            "pt-BR": "Central de Ajuda",
            "en": "help Center",
            "es": "centro de ayuda"
        },
        "api_for_development": {
            "pt-BR": "API para Desenvolvimento",
            "en": "API for Development",
            "es": "API DE DESARROLLO"
        },
        "security": {
            "pt-BR": "segurança",
            "en": "security",
            "es": "seguridad"
        },
        "documentation": {
            "pt-BR": "Documentação",
            "en": "Documentation",
            "es": "Documentación"
        },
        "takes_care_of_your_repetitive_tasks_so_you_can_focus_on_what_matters": {
            "pt-BR": "cuida das suas tarefas repetitivas para que você possa se dedicar ao que importa.",
            "en": "takes care of your repetitive tasks so you can focus on what matters.",
            "es": "Cuida tus tareas repetitivas para que puedas dedicarse a lo que importa."
        },
        "privacy": {
            "pt-BR": "Privacidade",
            "en": "Privacy",
            "es": "Intimidad"
        },
        "issuance_of_the_fgts_certificate_of_good_standing": {
            "pt-BR": "Emissão do Certificado de Regularidade do CND",
            "en": "Issuance of the CND Certificate of Good Standing",
            "es": "Emisión del CND Certificado de regularidad."
        },
        "fgts_crf_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com o CNPJ que deseja realizar a emissão do Certificado de Regularidade do FGTS para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar",
            "en": "You fill in the upload file with the CNPJ that you want to issue the FGTS Certificate of Regularity to configure a template. This information is saved for you to reuse whenever you need it",
            "es": "Llene el archivo de carga con CNPJ que desea emitir el certificado de regularidad FGTS para configurar una registro."
        },
        "fgts_crf_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre os certificados e seus respectivos arquivos.",
            "en": "After using the service, the results arrive by email with information about the certificates and their respective files.",
            "es": "Después de usar el servicio, los resultados llegan por correo electrónico con la información sobre los certificados y sus archivos respectivos."
        },
        "you_can_transfer_licenses_to_other_members_on_team": {
            "pt-BR": "Você pode utilizar e/ou transferir suas licenças para outros colaboradores da sua equipe",
            "en": "You can use and/or transfer your licenses to other members on your team",
            "es": "Puede usar y / o transferir sus licencias a otros empleados de su equipo."
        },
        "waters_of_the_river_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CPFs ou CNPJs que deseja baixar as contas e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CPFs or CNPJs you want to download accounts and set up a template that is saved to reuse whenever you need.",
            "es": "Llene el archivo de carga con CPFS o CNPJS que desea descargar las cuentas y configurar una registro que se guarda para reutilizarlo cada vez que lo necesite."
        },
        "waters_of_the_river_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com informações sobre o consumo e os boletos de pagamento.",
            "en": "After using the service, the results arrive by email with information about consumption and payment slips.",
            "es": "Después de usar el servicio, los resultados llegan por correo electrónico con información sobre los boletos de consumo y pago."
        },
        "note_niteroi": {
            "pt-BR": "Nota Niterói",
            "en": "Note Niterói",
            "es": "Nota nacional"
        },
        "niteroi_city_hall_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Niterói.",
            "en": "With a few clicks you configure a model to search and issue ISS guides in Niterói City Hall.",
            "es": "Con unos pocos clics, configura una registro para buscar y emitir guías de ISS en la ciudad de Niterói."
        },
        "credentials_from_the_city_of_niteroi": {
            "pt-BR": "Credenciais da Prefeitura de Niterói.",
            "en": "Credentials from the City of Niterói.",
            "es": "Credenciales de la ciudad de Niterói."
        },
        "same_cpf_cnpj_used_on_the_niteroi_city_hall_website": {
            "pt-BR": "Mesmo CPF/CNPJ utilizado no site da Prefeitura de Niterói.",
            "en": "Same CPF/CNPJ used on the Niterói City Hall website.",
            "es": "Incluso CPF / CNPJ utilizado en el sitio web de la prefectura de Niterói."
        },
        "same_password_used_on_the_niteroi_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Niterói.",
            "en": "Same password used on the Niterói City Hall website.",
            "es": "La misma contraseña utilizada en el sitio web de la prefectura de Niterói."
        },
        "note_salvador": {
            "pt-BR": "Nota Salvador",
            "en": "Note Salvador",
            "es": "el Salvador"
        },
        "iss_guides_in_salvador_city_hall_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Salvador.",
            "en": "With a few clicks you configure a model to search and issue ISS guides in Salvador City Hall.",
            "es": "Con unos pocos clics, configuró una registro para buscar y emitir guías de ISS en la prefectura de Salvador."
        },
        "iss_guides_in_salvador_city_hall_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, de acordo com o modelo que você configurou. Nele você encontra as guias, assim como um descritivo das informações gerais.",
            "en": "After using the service, the results arrive by email, according to the model you have configured. In it you will find the guides, as well as a description of the general information.",
            "es": "Después de usar el servicio, los resultados llegan por correo electrónico, según la registro que ha configurado."
        },
        "same_cpf_cnpj_used_on_the_salvador_city_hall_website": {
            "pt-BR": "Mesmo CPF/CNPJ utilizado no site da Prefeitura de Salvador",
            "en": "Same CPF/CNPJ used on the Salvador City Hall website",
            "es": "Incluso CPF / CNPJ utilizado en el sitio web de la Prefectura de Salvador"
        },
        "same_password_used_on_the_salvador_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Salvador",
            "en": "Same password used on the Salvador City Hall website",
            "es": "La misma contraseña utilizada en el sitio de la prefectura de Salvador."
        },
        "salvador_city_hall_credentials": {
            "pt-BR": "Credenciais da Prefeitura de Salvador",
            "en": "Salvador City Hall Credentials",
            "es": "Credenciales de la Prefectura de Salvador"
        },
        "credentials_of_the_municipality_of_maceio": {
            "pt-BR": "Credenciais da Prefeitura de Maceió",
            "en": "Credentials of the Municipality of Maceió",
            "es": "Credenciales de la prefectura de Maceió."
        },
        "iss_guides_in_maceio_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Maceió.",
            "en": "With a few clicks you can configure a model to search and issue ISS guides in Maceió City Hall.",
            "es": "Con unos pocos clics, configura una registro para buscar y emitir guías de ISS en la prefectura de Maceió."
        },
        "same_login_used_on_the_maceio_city_hall_website": {
            "pt-BR": "Mesmo login utilizado no site da Prefeitura de Maceió",
            "en": "Same login used on the Maceió City Hall website",
            "es": "Incluso el inicio de sesión utilizado en el sitio de la prefectura de Maceió"
        },
        "same_password_used_on_the_maceio_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Maceió",
            "en": "Same password used on the Maceió City Hall website",
            "es": "La misma contraseña utilizada en el sitio web de la prefectura de Maceió."
        },
        "credentials_of_the_city_hall_of_guaruja": {
            "pt-BR": "Credenciais da Prefeitura de Guarujá",
            "en": "Credentials of the City Hall of Guarujá",
            "es": "Credenciales de la prefectura de Guaruja"
        },
        "iss_guides_in_guaruja_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Guarujá.",
            "en": "With a few clicks, you configure a model to search and issue ISS guides in Guarujá City Hall.",
            "es": "Con unos pocos clics, configura una registro para buscar y emitir guías de ISS en el Ayuntamiento de Guarujá."
        },
        "same_login_used_on_the_guaruja_city_hall_website": {
            "pt-BR": "Mesmo login utilizado no site da Prefeitura de Guarujá.",
            "en": "Same login used on the Guarujá City Hall website.",
            "es": "Incluso el inicio de sesión utilizado en el sitio de la prefectura de Guarujá."
        },
        "same_password_used_on_the_guaruja_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Guarujá.",
            "en": "Same password used on the Guarujá City Hall website.",
            "es": "La misma contraseña utilizada en el sitio de la prefectura de Guarujá."
        },
        "iss_guides_in_santos_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Santos.",
            "en": "With a few clicks you can configure a model to search and issue ISS guides in Santos City Hall.",
            "es": "Con unos pocos clics, configura una registro para buscar y emitir guías de ISS en el Ayuntamiento de Santos."
        },
        "credentials_of_the_municipality_of_santos": {
            "pt-BR": "Credenciais da Prefeitura de Santos",
            "en": "Credentials of the Municipality of Santos",
            "es": "Credenciales del Ayuntamiento de Santos."
        },
        "same_login_used_on_the_santos_city_hall_website": {
            "pt-BR": "Mesmo login utilizado no site da Prefeitura de Santos.",
            "en": "Same login used on the Santos City Hall website.",
            "es": "Incluso el inicio de sesión utilizado en el sitio del Ayuntamiento de Santos."
        },
        "same_password_used_on_the_santos_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Santos.",
            "en": "Same password used on the Santos City Hall website.",
            "es": "La misma contraseña utilizada en el sitio del Ayuntamiento de Santos."
        },
        "saint_sndrew": {
            "pt-BR": "Santo André",
            "en": "Santo André",
            "es": "Santo André"
        },
        "iss_guides_in_santo_andre_works_1": {
            "pt-BR": "Com alguns cliques você configura um modelo para buscar e emitir guias de ISS na Prefeitura de Santo André.",
            "en": "With a few clicks, you configure a model to search and issue ISS guides in Santo André City Hall.",
            "es": "Con este servicio puede buscar y emitir guías de ISS en el Ayuntamiento de Santo André."
        },
        "credentials_from_the_city_of_santo_andre": {
            "pt-BR": "Credenciais da Prefeitura de Santo André",
            "en": "Credentials from the City of Santo André",
            "es": "Credenciales del Ayuntamiento de Santo André."
        },
        "same_login_used_on_the_santo_andre_city_hall_website": {
            "pt-BR": "Mesmo login utilizado no site da Prefeitura de Santo André.",
            "en": "Same login used on the Santo André City Hall website.",
            "es": "Incluso el inicio de sesión utilizado en el sitio web del Ayuntamiento de Santo André."
        },
        "same_password_used_on_the_santo_andre_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Santo André.",
            "en": "Same password used on the Santo André City Hall website.",
            "es": "La misma contraseña utilizada en el sitio del ayuntamiento de Santo André."
        },
        "time_reduction": {
            "pt-BR": "Redução de Tempo",
            "en": "Time Reduction",
            "es": "Reducción del tiempo"
        },
        "no_charges_scheduled": {
            "pt-BR": "Nenhuma cobrança agendada.",
            "en": "No charges scheduled.",
            "es": "Sin cargos programados."
        },
        "same_cuit_cuil_used_on_the_afip_website": {
            "pt-BR": "Mesmo CUIT/CUIL usado no site da AFIP",
            "en": "Same CUIT/CUIL used on the AFIP website",
            "es": "Mismo CUIT/CUIL utilizado en la página web de la AFIP"
        },
        "same_password_used_on_the_afip_website": {
            "pt-BR": "Mesma SENHA usada no site da AFIP",
            "en": "Same PASSWORD used on the AFIP website",
            "es": "Misma CLAVE utilizada en la página web de la AFIP"
        },
        "afip_credentials": {
            "pt-BR": "Credenciais AFIP",
            "en": "AFIP credentials",
            "es": "Credenciales AFIP"
        },
        "withholding_consultation": {
            "pt-BR": "Consulta de retenção",
            "en": "Withholding Consultation",
            "es": "Consulta de Retenciones de"
        },
        "social_security": {
            "pt-BR": "Segurança social",
            "en": "Social Security",
            "es": "Seguridad Social"
        },
        "afip_advantages_1": {
            "pt-BR": "Com alguns cliques, um registro é configurado com as credenciais AFIP, completando um arquivo de entrada com as informações necessárias.",
            "en": "With a few clicks, a registry is configured with the AFIP credentials, completing an input file with the required information.",
            "es": "Con unos pocos clicks, se configura un registro con las credenciales de la AFIP, completando un archivo de entrada con las informaciones requeridas."
        },
        "afip_advantages_2": {
            "pt-BR": "Após a utilização do serviço, os resultados chegam por e-mail com informações sobre retenções previdenciárias e seus respectivos arquivos.",
            "en": "After using the service, the results arrive by email with information on social security withholdings and their respective files.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con informaciones sobre las retenciones de seguridad social y sus respectivos archivos."
        },
        "arba_advantages_1": {
            "pt-BR": "Com alguns cliques, configure um registro com suas credenciais no site da ARBA e reutilize-o sempre que precisar.",
            "en": "With a few clicks, set up a registry with your credentials on the ARBA website and reuse it whenever you need it.",
            "es": "Con unos pocos clicks, configure un registro con sus credenciales en la página web de ARBA y lo reutiliza cuando lo necesite."
        },
        "arba_advantages_2": {
            "pt-BR": "Após a utilização do serviço, os resultados chegam por e-mail com informações sobre o Cadastro de Arrecadação - alíquota por assunto.",
            "en": "After using the service, the results arrive by email with information on the Collection Register - aliquot per subject.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con informaciones sobre el Padrón de Recaudación - alícuota por sujeto."
        },
        "same_cuit_cuil_used_on_the_arba_website": {
            "pt-BR": "Mesmo CUIT/CUIL usado no site da ARBA",
            "en": "Same CUIT/CUIL used on the ARBA website",
            "es": "Mismo CUIT/CUIL utilizado en la página web de la ARBA"
        },
        "same_password_used_on_the_arba_website": {
            "pt-BR": "Mesma SENHA usada no site da ARBA",
            "en": "Same PASSWORD used on the ARBA website",
            "es": "Misma CLAVE utilizada en la página web de la ARBA"
        },
        "arba_credentials": {
            "pt-BR": "Credenciais ARBA",
            "en": "ARBA credentials",
            "es": "Credenciales de ARBA"
        },
        "consultation_of_the_register_of_the_collection_regime_aliquot_by_subject": {
            "pt-BR": "Consulta do Registo do Regime de Cobrança - Alíquota por Assunto",
            "en": "Consultation of the Register of the Collection Regime - Aliquot by Subject",
            "es": "Consulta del Padrón de Régimen de Recaudación - Alícuota por Sujeto"
        },
        'seconds': {
            'pt-BR': 'segundos',
            'en': 'seconds',
            'es': 'segundos'
        },
        'average_time_of_1_robot_transaction': {
            'pt-BR': 'Tempo médio de 1 transação do robô',
            'en': 'Average time of 1 robot transaction',
            'es': 'Tiempo promedio de 1 transacción de robot'
        },
        'if_you_do_not_know_average_transaction_time_per_robot': {
            'pt-BR': 'Se não sabe o tempo médio de transação por robô, deixe zerado, que iremos desconsiderar no cálculo',
            'en': 'If you do not know the average transaction time per robot, leave it zero, which we will disregard in the calculation',
            'es': 'Si no conoce el tiempo promedio de transacción por robot, déjelo en  cero, que no tomaremos en cuenta en el cálculo'
        },
        'you_already_have_the_biggest_plan': {
            'pt-BR': 'Você já possui o maior plano',
            'en': 'You already have the biggest plan',
            'es': 'Ya tienes el plan más grande'
        },
        'if_you_want_to_upgrade_send_a_message_to': {
            'pt-BR': 'Se deseja realizar um upgrade, envie uma mensagem para',
            'en': 'If you want to upgrade, send a message to',
            'es': 'Si desea actualizar, envíe un mensaje a'
        },
        'no_charges_scheduled': {
            'pt-BR': 'Nenhuma cobrança agendada.',
            'en': 'No charges scheduled.',
            'es': 'No hay cargos programados.'
        },
        'manage_plan': {
            'pt-BR': 'Gerenciar Plano',
            'en': 'Manage Plan',
            'es': 'Administrar el Plan'
        },
        'hire_plan': {
            'pt-BR': 'Contratar Plano',
            'en': 'Hire Plan',
            'es': 'Plan de Alquiler'
        },
        'back_to_home': {
            'pt-BR': 'Voltar à pagina inicial',
            'en': 'Back to home',
            'es': 'Volver a la página de inicio'
        },
        'last_male': {
            'pt-BR': 'Últimos',
            'en': 'Last',
            'es': 'Últimos'
        },
        'register_of_general_regimes': {
            'pt-BR': 'Registro de Regimes Gerais',
            'en': 'Register of General Regimes',
            'es': 'Padrón de Regímenes Generales'
        },
        'agip_how_it_works_1': {
            'pt-BR': 'Com alguns cliques, configure um registo anexando o modelo com o mês e ano de validade que pretende consultar o Registo de Regimes Gerais da AGIP. Essas informações são salvas para que possam ser reutilizadas quando você precisar.',
            'en': 'With a few clicks, configure a record by attaching the template with the month and year of validity that you want to consult the Register of General Regimes of the AGIP. This information is saved so that it can be reused when you need it.',
            'es': 'Con unos pocos clicks, configure un registro adjuntando un registro con el mes y año de vigencia que quieras consultar el Padrón de Regímenes Generales de la AGIP. Esta información se guarda para que pueda reutilizarse cuando la necesite.'
        },
        'agip_how_it_works_2': {
            'pt-BR': 'Após a utilização do serviço, os resultados chegam por e-mail com informações sobre o Cadastro de Regimes Gerais - AGIP.',
            'en': 'After using the service, the results arrive by email with information on the Register of General Regimes - AGIP.',
            'es': 'Después de utilizar el servicio, los resultados llegan por correo electrónico con informaciones sobre el Padrón de Regímenes Generales - AGIP.'
        },
        "cepom_rj_enrollment_verification": {
            "pt-BR": "Verificação de Inscrição no CEPOM",
            "en": "CEPOM Enrollment Verification",
            "es": "Verificación de inscripción de CEPOM"
        },
        "cepom_rj_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral no CEPOM | Rio de Janeiro",
            "en": "Verification of Registration Status at CEPOM | Rio de Janeiro",
            "es": "Verificación del Estado de Registro en CEPOM | Rio de Janeiro"
        },
        "cepom_rj_text_example_input": {
            "pt-BR": "Exemplo: \"CEPOM RJ - Novos Fornecedores\"",
            "en": "Example: \"CEPOM RJ - New Providers\"",
            "es": "Ejemplo: \"CEPOM RJ - Nuevos Proveedores\""
        },
        "cepom_rj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja verificar a inscrição no CEPOM do Rio de Janeiro. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs who wish to verify their registration with the CEPOM in Rio de Janeiro. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que deseen verificar su registro en la CEPOM en Río de Janeiro. Luego configure un modelo utilizando el archivo completo."
        },
        "cepom_rj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Comprovante de Inscrição no CEPOM do Rio de Janeiro de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads the Proof of Enrollment in the CEPOM of Rio de Janeiro of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga el Comprobante de Inscripción en el CEPOM de Río de Janeiro de diferentes CNPJ simultáneamente."
        },
        "cpom_sp_enrollment_verification": {
            "pt-BR": "Verificação de Inscrição no CPOM",
            "en": "CPOM Enrollment Verification",
            "es": "Verificación de inscripción de CPOM"
        },
        "cpom_sp_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral no CPOM | São Paulo",
            "en": "Verification of Cadastral Status on CPOM | Sao Paulo",
            "es": "Verificación del estado de registro en CPOM | San Pablo"
        },
        "cpom_sp_text_example_input": {
            "pt-BR": "Exemplo: \"CPOM SP - Novos Fornecedores\"",
            "en": "Example: \"CPOM SP - New Providers\"",
            "es": "Ejemplo: \"CPOM SP - Nuevos proveedores\""
        },
        "cpom_sp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja verificar a inscrição no CEPOM de São Paulo. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that you want to verify the registration in the CEPOM of São Paulo. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea verificar el registro en el CEPOM de São Paulo. Luego configure un modelo utilizando el archivo completo."
        },
        "cpom_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Comprovante de Inscrição no CEPOM de São Paulo de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads Proof of Enrollment in the CEPOM of São Paulo of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga Comprobante de Inscripción en el CEPOM de São Paulo desde diferentes CNPJ simultáneamente."
        },
        "ibama_title_and_subtitle": {
            "pt-BR": "Emissão de CND | IBAMA",
            "en": "CND issuance | IBAMA",
            "es": "Emisión de CND | IBAMA"
        },
        "ibama_text_example_input": {
            "pt-BR": "Exemplo: \"IBAMA - CNPJ\"",
            "en": "Example: \"IBAMA - CNPJ\"",
            "es": "Ejemplo: \"IBAMA - CNPJ\""
        },
        "ibama_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja verificar débitos no IBAMA. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs who wish to verify their debts with the IBAMA. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que deseen verificar su débitos en la IBAMA Luego configure un modelo utilizando el archivo completo."
        },
        "ibama_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Comprovante de Débito no IBAMA de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads the Proof of Debt in the IBAMA of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga el Comprobante de Débito en el IBAMA de diferentes CNPJ simultáneamente."
        },
        "antecedentes_sp_title_and_subtitle": {
            "pt-BR": "Verificação de Antecedentes Criminais | SP",
            "en": "Criminal History Verification | SP",
            "es": "Verificación de antecedentes penales | SP"
        },
        "antecedentes_sp_text_example_input": {
            "pt-BR": "Exemplo: \"SP - DADOS DO RG \"",
            "en": "Example: \"SP - RG DATA \"",
            "es": "Ejemplo: \"SP - DATOS RG \""
        },
        "antecedentes_sp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os dados do RG que deseja verificar os antecedentes criminais em SP. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the RG data from who you wish to verify the criminal history in SP. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los datos RG que deseen verificar su antecedentes penales SP. Luego configure un modelo utilizando el archivo completo."
        },
        "antecedentes_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos antecedentes criminais em São Paulo de diferentes RGs simultaneamente.",
            "en": "This service issues and downloads the criminal history in the São Paulo of different RGs simultaneously.",
            "es": "Este servicio emite y descarga el antecedentes penales en São Paulo de diferentes RGs simultáneamente."
        },
        "antecedentes_federal_title_and_subtitle": {
            "pt-BR": "Verificação de Antecedentes Criminais | Brasil",
            "en": "Criminal History Verification | Brasil",
            "es": "Verificación Antecedentes penales | Brasil"
        },
        "antecedentes_federal_text_example_input": {
            "pt-BR": "Exemplo: \"Brasil - DADOS DO CPF \"",
            "en": "Example: \"Brasil - CPF DATA \"",
            "es": "Ejemplo: \"Brasil - DATOS CPF \""
        },
        "antecedentes_federal_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os dados do CPF que deseja verificar os antecedentes criminais no Brasil. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CPF data from who you wish to verify the criminal history in Brazil. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los datos CPF que deseen verificar su antecedentes penales Brasil. Luego configure un modelo utilizando el archivo completo."
        },
        "antecedentes_federal_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos antecedentes criminais no Brasil de diferentes CPFs simultaneamente.",
            "en": "This service issues and downloads the criminal history in the Brasil of different CPFs simultaneously.",
            "es": "Este servicio emite y descarga el antecedentes penales en Brasil de diferentes CPFs simultáneamente."
        },
        "sabesp_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Água | Sabesp",
            "en": "Issuance of Water Bills | Sabesp",
            "es": "Emisión de Facturas de Agua | Sabesp"
        },
        "sabesp_text_example_input": {
            "pt-BR": "Exemplo: \"Contas de Água - Sabesp\"",
            "en": "Example: \"Water bills - Sabesp\"",
            "es": "Ejemplo: \"Facturas de Agua - Sabesp\""
        },
        "sabesp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os RGIs relacionados aos imóveis que deseja obter a conta de água. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File provided below with the RGIs related to the properties you wish to obtain the water bill. Then configure a model using the filled file.",
            "es": "Descarga y rellena el Archivo Tipo que se proporciona a continuación con los RGI relacionados con las fincas de las que deseas obtener la factura del agua. Luego configure un modelo utilizando el archivo completo."
        },
        "sabesp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de água da Sabesp de diversos imóveis simultaneamente.",
            "en": "This service issues and downloads Sabesp water bills for several properties simultaneously.",
            "es": "Este servicio emite y descarga las facturas de agua de Sabesp para varias propiedades simultáneamente."
        },
        "consumption_accounts_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os boletos para pagamento das contas, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive the bills for payment of the bills, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá las facturas para el pago de las facturas, así como un archivo resumen de la información."
        },
        "shopee_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as informações de produtos de cada termos de busca, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the product information for each search keyword, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá la Información del Producto de cada términos de búsqueda, así como un archivo resumen de la información."
        },
        "rg_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os antecedentes criminais de cada RG, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the criminal history of each RG, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá los antecedentes criminales de cada Rg, así como un archivo resumen de la información."
        },
        "cnpj_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os comprovantes de cada CNPJs, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the receipts of each CNPJs, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá los comprobantes de cada CNPJ, así como un archivo resumen de la información."
        },
        "cpf_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os comprovantes de cada CPF, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive receipts for each CPF, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá los comprobantes de cada CPF, así como un archivo resumen de la información."
        },
        "service_invoices_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as NFS-e de cada prestador, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the NFS-e from each provider, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá el NFS-e de cada proveedor, así como un archivo resumen de la información."
        },
        "cpf_certificates_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as certidões de cada CPF, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive the certificates of each CPF, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá los certificados de cada CPF, así como un archivo resumen de la información."
        },
        "iss_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as guias de ISS solicitadas, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the requested ISS guides, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá las guías ISS solicitadas, así como un archivo resumen de la información."
        },
        "icms_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as guias solicitadas assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the requested guides as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá las guías solicitadas así como un archivo resumen de la información."
        },
        "ipva_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os boletos para pagamento do imposto, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive the tax payment slips, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá los comprobantes de pago de impuestos, así como un archivo resumen de la información."
        },
        "cnd_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as certidões de cada CNPJs, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive the certificates of each CNPJs, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá los certificados de cada CNPJ, así como un archivo resumen de la información."
        },
        "gnre_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as GNREs solicitadas assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the requested GNREs as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá las GNRE solicitadas así como un archivo resumen de la información."
        },
        "divida_ativa_rj_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber o comprovante das consultas para os CNPJs que não possuem dívida, e o DARJ para pagamento dos CNPJs que possuem dívida, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive proof of consultations for CNPJs that do not have debt, and the DARJ for payment of CNPJs that have debt, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá el comprobante de consultas para CNPJ que no tienen deuda, y el DARJ para pago de CNPJ que tienen deuda, así como un archivo resumen de la información."
        },
        "declaraciones_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as declarações, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the declarations, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá las declaraciones, así como un archivo resumen de la información."
        },
        "afip_argentina_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber as retenções da Segurança Social, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive Social Security withholdings, as well as a summary file of the information.",
            "es": "Al finalizar el servicio, recibirá las retenciones de la Seguridad Social, así como un archivo resumen de la información."
        },
        "arba_argentina_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber o Cadastro de Arrecadação - alíquota por assunto, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service, you will receive the Collection Registration - rate per subject, as well as a summary file of the information.",
            "es": "Al final del servicio, recibirá el Padrón de Recaudación - alícuota por sujeto, así como un archivo resumen de la información."
        },
        "issuance_of_proof_of_registration_status_in_the_cpf": {
            "pt-BR": "Emissão de Comprovante de Situação Cadastral no CPF",
            "en": "Issuance of Proof of Registration Status in the CPF",
            "es": "Emisión de Comprobante de Situación de Registro en el CPF"
        },
        "receita_federal_cpf_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral de CPFs | Receita Federal",
            "en": "Verification of CPF Registration Status | IRS",
            "es": "Verificación del estado de registro de CPF | Receta Federal"
        },
        "receita_federal_cpf_text_example_input": {
            "pt-BR": "Exemplo: \"CPFs - Receita Federal\"",
            "en": "Example: \"CPFs - Receta Federal\"",
            "es": "Ejemplo: \"CPF - IRS\""
        },
        "receita_federal_cpf_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CPFs que deseja emitir o Comprovante de Situação Cadastral. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CPFs you wish to issue the Proof of Registration Status. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CPF que desea emitir el Comprobante de Estado de Registro. Luego configure un modelo utilizando el archivo completo."
        },
        "cpf_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Comprovantes de Situação Cadastral de diferentes CPFs simultaneamente.",
            "en": "This service issues and downloads Proofs of Cadastral Status of different CPFs simultaneously.",
            "es": "Este servicio emite y descarga Pruebas de Estado Catastral de diferentes CPFs simultáneamente."
        },
        "enel_sao_paulo_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | Enel",
            "en": "Issuance of Energy Bills | Enel",
            "es": "Emisión de Facturas de Energía | Enel"
        },
        "enel_sp_text_example_input": {
            "pt-BR": "Exemplo: \"Luz - lojas SP\"",
            "en": "Example: \"Luz - SP stores\"",
            "es": "Ejemplo: \"Luz - tiendas SP\""
        },
        "enel_sp_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Enel.",
            "en": "Configure a template by entering your Enel login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales de inicio de sesión y contraseña de Enel."
        },
        "enel_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da Enel informada.",
            "en": "This service issues and downloads energy bills related to the informed Enel credential.",
            "es": "Este servicio emite y descarga las facturas de energía relacionadas con la credencial informada de Enel."
        },
        "notas_servico_sp_title_and_subtitle": {
            "pt-BR": "Emissão de Notas Fiscais de Serviço (NFS-e) | São Paulo",
            "en": "Issue of Service Invoices (NFS-e) | São Paulo",
            "es": "Emisión de Facturas de Servicios (NFS-e) | San Pablo"
        },
        "notas_servico_sp_example_input": {
            "pt-BR": "Exemplo: \"Notas - SP\"",
            "en": "Example: \"Notes - SP\"",
            "es": "Ejemplo: \"Notas - SP\""
        },
        "notas_servico_sp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com as informações do prestador de serviços que deseja emitir a NFS-e no Estado de São Paulo. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the information of the service provider who wants to issue the NFS-e in the State of São Paulo. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con la información del proveedor de servicios que desea emitir el NFS-e en el Estado de São Paulo. Luego configure un modelo utilizando el archivo completo."
        },
        "notas_servico_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das NFS-e de diferentes prestadores de serviço no Estado de São Paulo simultaneamente.",
            "en": "This service issues and downloads NFS-e from different service providers in the State of São Paulo simultaneously.",
            "es": "Este servicio emite y descarga NFS-e de diferentes proveedores de servicios en el Estado de São Paulo simultáneamente."
        },
        "comgas_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Gás | Comgás",
            "en": "Issuance of Gas Bills | Comgás",
            "es": "Emisión de Facturas de Gas | Comgás"
        },
        "comgas_example_input": {
            "pt-BR": "Exemplo: \"Comgás - SP\"",
            "en": "Example: \"Comgás - SP\"",
            "es": "Ejemplo: \"Comgas - SP\""
        },
        "comgas_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CPFs e Códigos dos Usuários dos imóveis que deseja obter a conta de gás. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CPFs and User Codes of the properties you wish to obtain the gas bill. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CPF y Códigos de Usuario de las propiedades que desea obtener la factura de gas. Luego configure un modelo utilizando el archivo completo."
        },
        "comgas_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de gás da Comgás de diversos imóveis simultaneamente.",
            "en": "This service issues and downloads Comgás gas bills for several properties simultaneously.",
            "es": "Este servicio emite y descarga las facturas de gas Comgás de varios inmuebles de forma simultánea."
        },
        "trf2_title_and_subtitle": {
            "pt-BR": "Emissão de Certidão | TRF2",
            "en": "Certificate Issuance | TRF2",
            "es": "Emisión de Certificados | TRF2"
        },
        "trf2_example_input": {
            "pt-BR": "Exemplo: \"Certidão - TRF2\"",
            "en": "Example: \"TRF2 - certificate\"",
            "es": "Ejemplo: \"Certificado - TRF2\""
        },
        "trf2_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CPFs que deseja emitir a Certidão Negativa de Distribuição de Ações Cíveis. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CPFs that you wish to issue the Civil Action Clearance Certificate. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CPF que desea emitir el Certificado de Liquidación de Acción Civil. Luego configure un modelo utilizando el archivo completo."
        },
        "trf2_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Certidões Negativas de Distribuição de Ações Cíveis no TRF2 de diferentes CPFs simultaneamente.",
            "en": "This service issues and downloads the Clearance Certificates of Distribution of Civil Actions in the TRF2 of different CPFs simultaneously.",
            "es": "Este servicio emite y descarga los Certificados de Liquidación de Distribución de Acciones Civiles en el TRF2 de diferentes CPFs simultáneamente."
        },
        "trf3_title_and_subtitle": {
            "pt-BR": "Emissão de Certidão | TRF3",
            "en": "Certificate Issuance | TRF3",
            "es": "Emisión de Certificados | TRF3"
        },
        "trf3_example_input": {
            "pt-BR": "Exemplo: \"Certidão - TRF3\"",
            "en": "Example: \"TRF3 - certificate\"",
            "es": "Ejemplo: \"Certificado - TRF3\""
        },
        "trf3_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os nome completos e CPFs que deseja emitir a Certidão Negativa de Distribuição de Ações Cíveis. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the full names and CPFs that you want to issue the Civil Action Clearance Certificate. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los nombres completos y CPF que desea emitir el Certificado de Autorización de Acción Civil. Luego configure un modelo utilizando el archivo completo."
        },
        "trf3_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Certidões Negativas de Distribuição de Ações Cíveis no TRF3 de diferentes CPFs simultaneamente.",
            "en": "This service issues and downloads Clearance Certificates of Distribution of Civil Actions in the TRF3 of different CPFs simultaneously.",
            "es": "Este servicio emite y descarga Certificados de Liquidación de Distribución de Acciones Civiles en el TRF3 de diferentes CPFs simultáneamente."
        },
        "inidoneos_title_and_subtitle": {
            "pt-BR": "Emissão de Certidão de Inidôneos | TCU",
            "en": "Issuance of Certificate of Inidôneos | TCU",
            "es": "Emisión de Certificado de Inidóneos | TCU"
        },
        "inidoneos_example_input": {
            "pt-BR": "Exemplo: \"Certidão - Inidoneidade\"",
            "en": "Example: \"Certificate - Disability\"",
            "es": "Ejemplo: \"Certificado - Discapacidad\""
        },
        "inidoneos_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja emitir a Certidão de Inidôneos no Tribunal de Contas da União (TCU). Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that want to issue the Certificate of Inidôneos at the Federal Court of Auditors (TCU). Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desean emitir el Certificado de Inidôneos en el Tribunal de Cuentas Federal (TCU). Luego configure un modelo utilizando el archivo completo."
        },
        "inidoneos_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download da Certidão de Inidôneos no Tribunal de Contas da União (TCU) de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads the Certificate of Inidóneos at the Federal Audit Court (TCU) of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga el Certificado de Inidóneos en el Tribunal de Cuentas Federal (TCU) de diferentes CNPJ simultáneamente."
        },
        "vivo_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Telefone | Vivo",
            "en": "Issuance of Telephone Bills | Vivo",
            "es": "Emisión de Facturas Telefónicas | Vivo"
        },
        "vivo_example_input": {
            "pt-BR": "Exemplo: \"Telefone - Vivo\"",
            "en": "Example: \"Phone - Vivo\"",
            "es": "Ejemplo: \"Teléfono - Vivo\""
        },
        "vivo_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Vivo.",
            "en": "Configure a template informing your Vivo login credentials and password.",
            "es": "Configure un registro que informe sus credenciales de inicio de sesión y contraseña de Vivo."
        },
        "vivo_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de telefonia relacionadas às credenciais da Vivo informadas.",
            "en": "This service issues and downloads telephony bills related to the informed Vivo credentials.",
            "es": "Este servicio emite y descarga las facturas de telefonía relacionadas con las credenciales de Vivo informadas."
        },
        "light_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | Light",
            "en": "Issuance of Energy Bills | Light",
            "es": "Emisión de Facturas de Energía | Light"
        },
        "light_example_input": {
            "pt-BR": "Exemplo: \"Luz - lojas ZS\"",
            "en": "Example: \"Light - ZS stores\"",
            "es": "Ejemplo: \"Light - Tiendas ZS\""
        },
        "light_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Light.",
            "en": "Set up a template by entering your Light login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales y contraseña de inicio de sesión de Light."
        },
        "light_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da Light informada.",
            "en": "This service issues and downloads energy bills related to the informed Light credential.",
            "es": "Este servicio emite y descarga las facturas de energía relacionadas con la credencial Light informada."
        },
        "claro_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Telefone | Claro",
            "en": "Issuance of Telephone Bills | Claro",
            "es": "Emisión de Facturas Telefónicas | Claro"
        },
        "claro_example_input": {
            "pt-BR": "Exemplo: \"Conta - Claro\"",
            "en": "Example: \"Bill - Claro\"",
            "es": "Ejemplo: \"Cuenta - Claro\""
        },
        "claro_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Claro.",
            "en": "Configure a template informing your Claro login credentials and password.",
            "es": "Configure una registro informando sus credenciales de inicio de sesión y contraseña de Claro."
        },
        "claro_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de telefonia relacionadas à credencial da Claro informada.",
            "en": "This service issues and downloads the telephone bills related to the informed Claro credential.",
            "es": "Este servicio emite y descarga las facturas telefónicas relacionadas con la credencial Claro informada."
        },
        "iss_rj_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Rio de Janeiro | Nota Carioca",
            "en": "Issuance of ISS Guides | Rio de Janeiro | Nota Carioca",
            "es": "Emisión de Guías ISS | Rio de Janeiro | Nota Carioca"
        },
        "iss_rj_example_input": {
            "pt-BR": "Exemplo: \"Guia ISS - Rio de Janeiro\"",
            "en": "Example: \"ISS Guide - Rio de Janeiro\"",
            "es": "Ejemplo: \"Guía ISS - Río de Janeiro\""
        },
        "iss_rj_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha do Nota Carioca. Para fornecer as outras informações necessárias pra emissão das guias de ISS, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Configure a template informing your Nota Carioca login credentials and password. To provide the other information necessary for the issuance of ISS guides, download and fill in the Standard File provided below and use the filled file in the model configuration.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de Nota Carioca. Para proporcionar la otra información necesaria para la emisión de guías ISS, descargue y complete el archivo estándar que se proporciona a continuación y use el archivo completo en la configuración del modelo."
        },
        "iss_rj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de diferentes guias de ISS na Prefeitura do Rio de Janeiro simultaneamente.",
            "en": "This service issues and downloads different ISS guides at the City Hall of Rio de Janeiro simultaneously.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS en la Municipalidad de Río de Janeiro."
        },
        "iss_sp_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | São Paulo",
            "en": "Issuance of ISS Guides | São Paulo",
            "es": "Emisión de Guías ISS | São Paulo"
        },
        "iss_sp_example_input": {
            "pt-BR": "Exemplo: \"Empresas - Receita\"",
            "en": "Example: \"ISS Guide - São Paulo\"",
            "es": "Ejemplo: \"Empresas - Receita\""
        },
        "iss_sp_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha no site da Prefeitura de São Paulo. Para fornecer as outras informações necessárias pra emissão das guias de ISS, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "At the end of the service execution, you will receive the requested ISS guides, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá las guías ISS solicitadas, así como un archivo resumen de la información."
        },
        "iss_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de diferentes guias de ISS na Prefeitura de São Paulo simultaneamente.",
            "en": "This service issues and downloads different ISS guides at the City Hall of São Paulo simultaneously.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS en la Municipalidad de São Paulo."
        },
        "receita_federal_cnpj_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral de CNPJs | Receita Federal",
            "en": "Verification of CNPJ Registration Status | IRS",
            "es": "Verificación del estado de registro de CNPJ | Receta Federal"
        },
        "receita_federal_cnpj_example_input": {
            "pt-BR": "Exemplo: \"Receita Federa - CNPJs \"",
            "en": "Example: \"Federal Revenue - CNPJ\"",
            "es": "Ejemplo: \"Ingresos Federales - CNPJ\""
        },
        "receita_federal_cnpj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs deseja emitir o Comprovante de Inscrição e Situação Cadastral. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to issue the Proof of Enrollment and Registration Status. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ a los que desea emitir el Comprobante de Inscripción y Estado de Registro. Luego configure un modelo utilizando el archivo completo."
        },
        "receita_federal_cnpj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Comprovante de Inscrição e Situação Cadastral de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads Proof of Enrollment and Registration Status of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga Comprobantes de Inscripción y Estado de Registro de diferentes CNPJ simultáneamente."
        },
        "issuance_of_icms_guide": {
            "pt-BR": "Emissão de Guia de ICMS",
            "en": "Issuance of ICMS Guide",
            "es": "Emisión de Guía ICMS"
        },
        "icms_mg_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | MG",
            "en": "Issuance of ICMS Guide | MG",
            "es": "Emisión de Guía ICMS | MG"
        },
        "icms_mg_example_input": {
            "pt-BR": "Exemplo: \"ICMS-MG\"",
            "en": "Example: \"ICMS-MG\"",
            "es": "Ejemplo: \"ICMS-MG\""
        },
        "icms_sp_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | SP",
            "en": "Issuance of ICMS Guide | SP",
            "es": "Emisión de Guía ICMS | SP"
        },
        "icms_sp_example_input": {
            "pt-BR": "Exemplo: \"ICMS-SP\"",
            "en": "Example: \"ICMS-SP\"",
            "es": "Ejemplo: \"ICMS-SP\""
        },
        "icms_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com CNPJ, entre outras informações, das guias de ICMS que deseja emitir. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with CNPJ, among other information, of the ICMS tax forms you wish to issue. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con CNPJ, entre otra información, de los formularios de impuestos ICMS que desea emitir. Luego configure un modelo utilizando el archivo completo."
        },
        "icms_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de diferentes guias do Imposto sobre Circulação de Mercadorias e Serviços (ICMS) simultaneamente.",
            "en": "This service issues and downloads different Tax on the Circulation of Goods and Services (ICMS) guides simultaneously.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías del Impuesto a la Circulación de Mercancías y Servicios (ICMS)."
        },
        "icms_rj_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | RJ",
            "en": "Issuance of ICMS Guide | RJ",
            "es": "Emisión de Guía ICMS | RJ"
        },
        "icms_rj_example_input": {
            "pt-BR": "Exemplo: \"ICMS-RJ\"",
            "en": "Example: \"ICMS-RJ\"",
            "es": "Ejemplo: \"ICMS-RJ\""
        },
        "ipva_rj_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de IPVA | Detran RJ",
            "en": "Issuance of IPVA Guide | detran RJ",
            "es": "Emisión de Guía IPVA | detran RJ"
        },
        "ipva_rj_example_input": {
            "pt-BR": "Exemplo: \"IPVA-RJ\"",
            "en": "Example: \"IPVA-RJ\"",
            "es": "Ejemplo: \"IPVA-RJ\""
        },
        "ipva_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os RENAVAM dos veículos que deseja emitir a Guia de Regularização do IPVA. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the RENAVAM of the vehicles you wish to issue the IPVA Regularization Guide. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con el RENAVAM de los vehículos que desea emitir la Guía de Regularización IPVA. Luego configure un modelo utilizando el archivo completo."
        },
        "ipva_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Guia de Regularização do IPVA de diversos automóveis simultaneamente.",
            "en": "This service issues and downloads the IPVA Regularization Guide for several cars simultaneously.",
            "es": "Este servicio emite y descarga la Guía de Regularización IPVA para varios autos simultáneamente."
        },
        "ipva_sp_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de IPVA | SP",
            "en": "Issuance of IPVA Guide | SP",
            "es": "Emisión de Guía IPVA | SP"
        },
        "ipva_sp_example_input": {
            "pt-BR": "Exemplo: \"IPVA-SP\"",
            "en": "Example: \"IPVA-SP\"",
            "es": "Ejemplo: \"IPVA-SP\""
        },
        "notas_servicos_rj_title_and_subtitle": {
            "pt-BR": "Emissão de Notas Fiscais de Serviço (NFS-e) | Rio de Janeiro",
            "en": "Issue of Service Invoices (NFS-e) | Rio de Janeiro",
            "es": "Emisión de Facturas de Servicios (NFS-e) | Rio de Janeiro"
        },
        "notas_servicos_rj_example_input": {
            "pt-BR": "Exemplo: \"Notas - RJ\"",
            "en": "Example: \"Notes - RJ\"",
            "es": "Ejemplo: \"Notas - RJ\""
        },
        "notas_servicos_rj_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha do Nota Carioca. Se necessário, informe o período de emissão das notas que deseja buscar na configuração do modelo.",
            "en": "Configure a template informing your Nota Carioca login credentials and password. If necessary, inform the period of issue of the notes that you want to search in the configuration of the model.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de Nota Carioca. Si es necesario, informe el período de emisión de los billetes que desea buscar en la configuración de la registro."
        },
        "notas_servicos_rj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das NFS-e relacionadas à credencial da Nota Carioca informada.",
            "en": "This service issues and downloads the NFS-e related to the Nota Carioca credential informed.",
            "es": "Este servicio emite y descarga el NFS-e relacionado con la credencial Nota Carioca informada."
        },
        "cnd_federal_revenue_title_and_subtitle": {
            "pt-BR": "Emissão de CND | Receita Federal",
            "en": "CND issuance | Federal Revenue",
            "es": "Emisión de CND | Receta Federal"
        },
        "cnd_federal_revenue_example_input": {
            "pt-BR": "Exemplo: \"CND - Receita Federal\"",
            "en": "Example: \"CND -  Federal Revenue\"",
            "es": "Ejemplo: \"CND - Receta Federal\""
        },
        "cnd_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja emitir a CND. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that you wish to issue the CND. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea emitir el CND. Luego configure un modelo utilizando el archivo completo."
        },
        "cnd_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Certidões de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads Certificates from different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga Certificados de diferentes CNPJ simultáneamente."
        },
        "gnre_sp_title_and_subtitle": {
            "pt-BR": "Emissão de GNRE | SP",
            "en": "GNRE emission | SP",
            "es": "Emisión de GNRE | SP"
        },
        "gnre_sp_example_input": {
            "pt-BR": "Exemplo: \"GNRE-SP\"",
            "en": "Example: \"GNRE-SP\"",
            "es": "Ejemplo: \"GNRE-SP\""
        },
        "gnre_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com a Inscrição Estadual ou CNPJ, entre outras informações, das notas que deseja emitir o GNRE. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the State Registration or CNPJ, among other information, of the notes you wish to issue the GNRE. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con el Registro Estatal o CNPJ, entre otra información, de las notas que desea emitir la GNRE. Luego configure un modelo utilizando el archivo completo."
        },
        "gnre_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Guias Nacionais de Recolhimento de Tributos Estaduais (GNRE) no estado de São Paulo de diferentes notas simultaneamente.",
            "en": "This service issues and downloads the National Guides for the Collection of State Taxes (GNRE) in the state of São Paulo of different notes simultaneously.",
            "es": "Este servicio emite y descarga las Guías Nacionales para la Recaudación de Impuestos Estatales (GNRE) en el estado de São Paulo de diferentes billetes simultáneamente."
        },
        "emission_of_gnre": {
            "pt-BR": "Emissão de GNRE",
            "en": "Emission of GNRE",
            "es": "Emisión de GNRE"
        },
        "gnre_title_and_subtitle": {
            "pt-BR": "Emissão de GNRE | Todos os estados (exceto ES e SP)",
            "en": "Issue of GNRE | All states (except ES and SP)",
            "es": "Emisión de GNRE | Todos los estados (excepto ES y SP)"
        },
        "gnre_example_input": {
            "pt-BR": "Exemplo: \"GNRE - UF\"",
            "en": "Example: \"GNRE - UF\"",
            "es": "Ejemplo: \"GNRE - UF\"",
        },
        "gnre_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Guias Nacionais de Recolhimento de Tributos Estaduais (GNRE) em todos os estados (exceto ES e SP), de diferentes notas simultaneamente.",
            "en": "This service issues and downloads the National Guides for the Collection of State Taxes (GNRE) in all states (except ES and SP), of different notes simultaneously.",
            "es": "Este servicio emite y descarga las Guías Nacionales para la Recaudación de Impuestos Estatales (GNRE) en todos los estados (excepto ES y SP), de diferentes notas simultáneamente."
        },
        "cedae_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Água | CEDAE",
            "en": "Issuance of Water Bills | CEDAE",
            "es": "Emisión de Facturas de Agua | CEDAE"
        },
        "cedae_example_input": {
            "pt-BR": "Exemplo: \"Contas de Água - Cedae\"",
            "en": "Example: \"Water bills - Cedae\"",
            "es": "Ejemplo: \"Facturas de Agua - Cedae\""
        },
        "water_bill_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os RGIs dos imóveis que deseja obter a conta de água. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the RGIs of the properties you wish to obtain the water bill. Then configure a model using the filled file.",
            "es": "Descarga y rellena el Fichero Tipo disponible a continuación con los RGI de las viviendas de las que deseas obtener la factura del agua. Luego configure un modelo utilizando el archivo completo."
        },
        "cedae_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de água da CEDAE de diversos imóveis simultaneamente.",
            "en": "This service issues and downloads CEDAE water bills from several properties simultaneously.",
            "es": "Este servicio emite y descarga las facturas de agua de CEDAE de varias propiedades simultáneamente."
        },
        "naturgy_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Gás | Naturgy",
            "en": "Issuance of Gas Bills | Naturgy",
            "es": "Emisión de Facturas de Gas | Naturgy"
        },
        "naturgy_example_input": {
            "pt-BR": "Exemplo: \"Gás - Naturgy\"",
            "en": "Example: \"Gas - Naturgy\"",
            "es": "Ejemplo: \"Gas - Naturgy\""
        },
        "naturgy_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os Números dos Clientes, entre outras informações, dos imóveis que deseja obter a conta de gás. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File provided below with the Customer Numbers, among other information, of the properties you wish to obtain a gas bill. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar que se proporciona a continuación con los Números de Cliente, entre otra información, de las propiedades que desea obtener una factura de gas. Luego configure un modelo utilizando el archivo completo."
        },
        "naturgy_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de gás da Naturgy de diversos imóveis simultaneamente.",
            "en": "This service issues and downloads Naturgy gas bills for several properties simultaneously.",
            "es": "Este servicio emite y descarga las facturas de gas de Naturgy para varios inmuebles de forma simultánea."
        },
        "iss_rio_grande_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS |  Rio Grande",
            "en": "Issuing of Guides | ISS Rio Grande",
            "es": "Emisión de Guías | ISS Río Grande"
        },
        "iss_rio_grande_example_input": {
            "pt-BR": "Exemplo: “ISS - Rio Grande”",
            "en": "Example: “ISS - Rio Grande”",
            "es": "Ejemplo: “ISS - Río Grande”"
        },
        "iss_rio_grande_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura De Rio Grande.",
            "en": "Configure a template informing your login credentials and password for the City Hall of Rio Grande.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Río Grande."
        },
        "iss_rio_grande_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura De Rio Grande informada.",
            "en": "This service issues and simultaneously downloads different ISS guides related to the informed Rio Grande City Hall credential.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Rio Grande."
        },
        "active_debt_consultation_and_regulation": {
            "pt-BR": "Consulta e Regulamentação de Dívida Ativa",
            "en": "Active Debt Consultation and Regulation",
            "es": "Consulta y Regulación de Deuda Activa"
        },
        "divida_ativa_rj_title_and_subtitle": {
            "pt-BR": "Consulta e Regulamentação de Dívida Ativa | RJ",
            "en": "Active Debt Consultation and Regulation | RJ",
            "es": "Consulta y Regulación de Deuda Activa | RJ"
        },
        "divida_ativa_rj_example_input": {
            "pt-BR": "Exemplo: \"Dívida ativa - RJ\"",
            "en": "Example: \"Active debt - RJ\"",
            "es": "Ejemplo: \"Deuda activa - RJ\""
        },
        "divida_ativa_rj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja consultar de Divida Ativa e emitir DARJ de pagamento. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to consult for Active Debt and issue payment DARJ. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea consultar para Deuda Activa y emitir DARJ de pago. Luego configure un modelo utilizando el archivo completo."
        },
        "divida_ativa_rj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de débitos na Dívida Ativa de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads debts in the Active Debt of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga deudas en Deuda Activa de diferentes CNPJs simultáneamente."
        },
        "divida_ativa_sp_title_and_subtitle": {
            "pt-BR": "Consulta e Regulamentação de Dívida Ativa | SP",
            "en": "Active Debt Consultation and Regulation | SP",
            "es": "Consulta y Regulación de Deuda Activa | SP"
        },
        "divida_ativa_sp_example_input": {
            "pt-BR": "Exemplo: \"Dívida ativa - SP\"",
            "en": "Example: \"Active debt - SP\"",
            "es": "Ejemplo: \"Deuda activa - SP\""
        },
        "divida_ativa_sp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja consultar de Divida Ativa São Paulo. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to consult for Active Debt and issue payment DARJ. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea consultar para Deuda Activa y emitir DARJ de pago. Luego configure un modelo utilizando el archivo completo."
        },
        "cnd_sp_title_and_subtitle": {
            "pt-BR": "Emissão de CND | SP",
            "en": "CND Issuance | SP",
            "es": "Emisión de CND | SP"
        },
        "cnd_sp_example_input": {
            "pt-BR": "Exemplo: \"CND - SP\"",
            "en": "Example: \"CND - SP\"",
            "es": "Ejemplo: \"CND - SP\""
        },
        "cnd_rj_title_and_subtitle": {
            "pt-BR": "Emissão de CND | RJ",
            "en": "CND Issuance | RJ",
            "es": "Emisión de CND | RJ"
        },
        "cnd_rj_example_input": {
            "pt-BR": "Exemplo: \"CND - RJ\"",
            "en": "Example: \"CND - RJ\"",
            "es": "Ejemplo: \"CND - RJ\""
        },
        "iss_ipojuca_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Ipojuca",
            "en": "Issuing of ISS Guides | Ipojuca",
            "es": "Emisión de Guías ISS | Ipojuca"
        },
        "iss_ipojuca_example_input": {
            "pt-BR": "Exemplo: \"ISS - Ipojuca”",
            "en": "Example: \"ISS - Ipojuca”",
            "es": "Ejemplo: \"ISS - Ipojuca\""
        },
        "iss_ipojuca_wilson_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura do Ipojuca.",
            "en": "Configure a template informing your login credentials and password for the Municipality of Ipojuca.",
            "es": "Configure un registro informando sus credenciales de acceso y contraseña para el Municipio de Ipojuca."
        },
        "iss_ipojuca_wilson_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura do Ipojuca informada. ",
            "en": "This service issues and downloads different ISS guides related to the informed Ipojuca City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Ipojuca."
        },
        "simples_nacional_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral | Simples Nacional",
            "en": "Verification of Registration Status | Simples Nacional",
            "es": "Verificación del estado de registro | Simples Nacional"
        },
        "simples_nacional_example_input": {
            "pt-BR": "Exemplo: \"CNPJ - Simples Nacional\"",
            "en": "Example: \"CNPJ - Simple Nacional\"",
            "es": "Ejemplo: \"CNPJ - Simples Nacionales\""
        },
        "simples_nacional_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja consultar no Simples Nacional. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to consult in Simples Nacional. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea consultar en Simples Nacional. Luego configure un modelo utilizando el archivo completo."
        },
        "simples_nacional_title_about_the_service": {
            "pt-BR": "Com esse Serviço você consegue consultar simultaneamente a situação cadastral de diversos CNPJs no Simples Nacional.",
            "en": "With this Service you can simultaneously consult the registration status of several CNPJs in Simples Nacional.",
            "es": "Con este Servicio se puede consultar simultáneamente el estado de registro de varios CNPJ en el Simples Nacional."
        },
        "iss_barcarena_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Barcarena",
            "en": "Issuing of ISS Guides | Barcarena",
            "es": "Emisión de Guías ISS | barcarena"
        },
        "iss_barcarena_example_input": {
            "pt-BR": "Exemplo: \"ISS - Barcarena\"",
            "en": "Example: \"ISS - Barcarena\"",
            "es": "Ejemplo: \"ISS - Barcarena\""
        },
        "iss_barcarena_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Barcarena.",
            "en": "Set up a template informing your Barcarena City Hall login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña del Ayuntamiento de Barcarena."
        },
        "iss_barcarena_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Barcarena informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Barcarena City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Barcarena."
        },
        "iss_oriximina_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Oriximiná",
            "en": "Issuing of ISS Guides | Oriximiná",
            "es": "Emisión de Guías ISS | Oriximiná"
        },
        "iss_oriximina_example_input": {
            "pt-BR": "Exemplo: \"ISS - Oriximiná\"",
            "en": "Example: \"ISS - Oriximiná\"",
            "es": "Ejemplo: \"ISS - Oriximiná\""
        },
        "iss_oriximina_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Oriximiná.",
            "en": "Configure a template informing your login credentials and password for the City Hall of Oriximiná.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Oriximiná."
        },
        "iss_oriximina_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Oriximiná informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Oriximiná City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Oriximiná."
        },
        "sefaz_rj_title_and_subtitle": {
            "pt-BR": "Declaração e Emissão de ITD | Sefaz Rio de Janeiro",
            "en": "ITD Declaration and Issuance | Sefaz Rio de Janeiro",
            "es": "Declaración y Emisión de ITD | Sefaz Rio de Janeiro"
        },
        "sefaz_rj_example_input": {
            "pt-BR": "Exemplo: \"Sefaz - RJ\"",
            "en": "Example: \"Sefaz - RJ\"",
            "es": "Ejemplo: \"Sefaz - RJ\""
        },
        "sefaz_rj_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha do site da Sefaz RJ. Para fornecer as outras informações necessárias pra emissão da declaração de ITD, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Configure a template informing your login credentials and password from the Sefaz RJ website. To provide the other information necessary for the issuance of the ITD declaration, download and fill in the Standard File provided below and use the filled file in the model configuration.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña desde el sitio web de Sefaz RJ. Para proporcionar la otra información necesaria para la emisión de la declaración de DTI, descargue y complete el Archivo estándar que se proporciona a continuación y use el archivo completo en la configuración del modelo."
        },
        "sefaz_rj_title_about_the_service": {
            "pt-BR": "Este serviço faz a declaração e emite diferentes guias de ITD simultaneamente.",
            "en": "This service makes the declaration and issues different ITD guides simultaneously.",
            "es": "Este servicio realiza la declaración y expide las diferentes guías ITD simultáneamente."
        },
        "iss_cabedelo_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Cabedelo",
            "en": "Issuing of ISS Guides | Cabedelo",
            "es": "Emisión de ISS Guías| Cabedelo"
        },
        "iss_cabedelo_example_input": {
            "pt-BR": "Exemplo: \"ISS - Cabedelo\"",
            "en": "Example: \"ISS - Cabedelo\"",
            "es": "Ejemplo: \"ISS - CABEDELO\""
        },
        "iss_cabedelo_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Cabedelo.",
            "en": "Configure a template informing your login credentials and password for the Municipality of Cabedelo.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Municipio de Cabedelo."
        },
        "iss_cabedelo_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Cabedelo informada.",
            "en": "This service issues and simultaneously downloads different ISS guides related to the informed Cabedelo City Hall credential.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Cabedelo."
        },
        "certidao_mte_title_and_subtitle": {
            "pt-BR": "EEmissão Certidão de Débitos Trabalhistas | MTE-SIT",
            "en": "Issuance of Labor Debt Certificate | MTE-SIT",
            "es": "Certificado de emisión de las deudas laborales | MTE-SIT"
        },
        "certidao_mte_example_input": {
            "pt-BR": "Exemplo: \"Débitos Trabalhistas - MTE\"",
            "en": "Example: \"Labor Debts - MTE\"",
            "es": "Ejemplo: \"Deudas laborales - MTE\""
        },
        "certidao_mte_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja emitir as certidões. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to issue the certificates. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea emitir los certificados. Luego configure un modelo utilizando el archivo completo."
        },
        "certidao_mte_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de diferentes Certidões de Débitos Trabalhistas na Secretaria de Inspeção do Trabalho (SIT) do MTE simultaneamente.",
            "en": "This service issues and downloads different Labor Debt Certificates from the MTE's Labor Inspection Secretariat (SIT) simultaneously.",
            "es": "Este servicio emite y descarga simultáneamente diferentes Certificados de Deuda Laboral de la Secretaría de Inspección del Trabajo (SIT) del MTE."
        },
        "inidoneos_ceis_title_and_subtitle": {
            "pt-BR": "Emissão de Certidão de Inidôneos | CEIS",
            "en": "Issuance of Certificate of Inidôneos | CEIS",
            "es": "Emisión de Certificado de Inidóneos | CEIS"
        },
        "inidoneos_ceis_example_input": {
            "pt-BR": "Exemplo: \"Certidão de Inidôneos - CEIS\"",
            "en": "Example: \"Certificate of Disability - CEIS\"",
            "es": "Ejemplo: \"Certificado de INIDIONEOS - CEIS\""
        },
        "inidoneos_ceis_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja emitir a Certidão de Inidôneos no Tribunal de Contas da União. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that you wish to issue the Certificate of Inidôneos at the Federal Court of Auditors. Then configure a template using the completed file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea emitir el Certificado de Inidôneos en el Tribunal de Cuentas Federal, luego configure un registro utilizando el archivo completo."
        },
        "inidoneos_ceis_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download da Certidão de Inidôneos no Cadastro de Empresas Inidôneas e Suspensas (CEIS) de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads the Certificate of Disabled Persons in the Registry of Disabled and Suspended Companies (CEIS) of different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga el Certificado de Personas Inválidas en el Registro de Empresas Inválidas y Suspendidas (CEIS) de diferentes CNPJ simultáneamente."
        },
        "cnd_fgts_title_and_subtitle": {
            "pt-BR": "Emissão do Certificado de Regularidade | FGTS",
            "en": "Issuance of the Certificate of Regularity | FGTS",
            "es": "Emisión del Certificado de Regularidad | FGTS"
        },
        "cnd_fgts_example_input": {
            "pt-BR": "Exemplo: \"Certificado - FGTS\"",
            "en": "Example: \"Certificate - FGTS\"",
            "es": "Ejemplo: \"Certificado - FGTS\""
        },
        "cnd_fgts_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja emitir o Certificado de Regularidade do FGTS. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that you wish to issue the FGTS Certificate of Regularity. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea emitir el Certificado de Regularidad FGTS. Luego configure un modelo utilizando el archivo completo."
        },
        "cnd_fgts_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos Certificado de Regularidade do FGTS de diferentes CNPJs simultaneamente.",
            "en": "This service issues and downloads FGTS Regularity Certificates from different CNPJs simultaneously.",
            "es": "Este servicio emite y descarga Certificados de Regularidad FGTS de diferentes CNPJ simultáneamente."
        },
        "aguas_rio_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Água | Águas do Rio",
            "en": "Issuance of Water Bills | river waters",
            "es": "Emisión de Facturas de Agua | aguas del rio"
        },
        "aguas_rio_example_input": {
            "pt-BR": "Exemplo: \"Contas - Águas do Rio\"",
            "en": "Example: \"Accounts - Waters of the River\"",
            "es": "Ejemplo: \"Cuentas - Aguas de río\""
        },
        "aguas_rio_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CPFs ou CNPJs relacionados aos imóveis que deseja obter a conta de água. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CPFs or CNPJs related to the properties you wish to obtain the water bill. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CPF o CNPJ relacionados con las propiedades que desea obtener la factura del agua. Luego configure un modelo utilizando el archivo completo."
        },
        "aguas_rio_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de água da Águas do Rio de diversos imóveis simultaneamente",
            "en": "This service issues and downloads Águas do Rio water bills from several properties simultaneously",
            "es": "Este servicio emite y descarga facturas de agua de Águas do Rio de varias propiedades simultáneamente"
        },
        "iss_niteroi_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Niterói",
            "en": "Issuance of ISS Guides | Niterói",
            "es": "Emisión de Guías ISS | Niterói"
        },
        "iss_niteroi_example_input": {
            "pt-BR": "Exemplo: \"ISS - Niterói\"",
            "en": "Example: \"ISS - Niterói\"",
            "es": "Ejemplo: \"ISS - NITERÓI\""
        },
        "iss_niteroi_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Niterói.",
            "en": "Configure a template informing your Niterói City Hall login credentials and password.",
            "es": "Configure una plantilla informando sus credenciales de inicio de sesión y contraseña del Ayuntamiento de Niterói."
        },
        "iss_niteroi_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Niterói informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Niterói City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Niterói."
        },
        "iss_salvador_title_and_subtitle": {
            "pt-BR": "Emissão de guias de ISS | Nota Salvador",
            "en": "Issuance of ISS guides | Note Salvador",
            "es": "Problema de emisión | Nota Salvador"
        },
        "iss_salvador_example_input": {
            "pt-BR": "Exemplo: \"ISS - Salvador\"",
            "en": "Example: \"ISS - Salvador\"",
            "es": "Ejemplo: \"ISS - Salvador\""
        },
        "iss_salvador_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Salvador.",
            "en": "Set up a template informing your Salvador City Hall login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña del Ayuntamiento de Salvador."
        },
        "iss_salvador_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Salvador informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Salvador City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Salvador."
        },
        "iss_maceio_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Maceió",
            "en": "Issuance of ISS Guides | Maceió",
            "es": "Problema de emisión | Maceió"
        },
        "iss_maceio_example_input": {
            "pt-BR": "Exemplo: \"ISS - Maceió\"",
            "en": "Example: \"ISS - Maceió\"",
            "es": "Ejemplo: \"ISS - MACEIÓ\""
        },
        "iss_maceio_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Maceió.",
            "en": "Set up a template informing your Maceió City Hall login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de la Municipalidad de Maceió."
        },
        "iss_maceio_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Maceió informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Maceió City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Maceió."
        },
        "iss_guaruja_title_and_subtitle": {
            "pt-BR": "Emissão de Guias ISS | Guarujá",
            "en": "Issuance of ISS Guides | Guarujá",
            "es": "Emisión de Guías ISS | Guarujá"
        },
        "iss_guaruja_example_input": {
            "pt-BR": "Exemplo: \"ISS - Guarujá\"",
            "en": "Example: \"ISS - Guarujá\"",
            "es": "Ejemplo: \"ISS - Guarujá\""
        },
        "iss_guaruja_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Guarujá.",
            "en": "Configure a template informing your login credentials and password for the City of Guarujá.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Guarujá."
        },
        "iss_guaruja_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Guarujá informada.",
            "en": "This service issues and simultaneously downloads different ISS guides related to the informed Guarujá City Hall credential.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Guarujá."
        },
        "iss_santos_title_and_subtitle": {
            "pt-BR": "Emissão de guias de ISS | Santos",
            "en": "Issuance of ISS guides | Santos",
            "es": "Problema de emisión | Santos"
        },
        "iss_santos_example_input": {
            "pt-BR": "Exemplo: \"ISS - Santos\"",
            "en": "Example: \"ISS - Santos\"",
            "es": "Ejemplo: \"ISS - SANTOS\""
        },
        "iss_santos_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Santos.",
            "en": "Set up a template informing your Santos City Hall login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña del Ayuntamiento de Santos."
        },
        "iss_santos_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Santos informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Santos City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Santos."
        },
        "iss_santo_andre_title_and_subtitle": {
            "pt-BR": "Emissão de Guias de ISS | Santo André",
            "en": "Issuance of ISS Guides | Saint Andrew",
            "es": "Problema de emisión | Santo André"
        },
        "iss_santo_andre_example_input": {
            "pt-BR": "Exemplo: \"ISS - Santo André\"",
            "en": "Example: \"ISS - Santo André\"",
            "es": "Ejemplo: \"ISS - Santo André"
        },
        "iss_santo_andre_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Santo André.",
            "en": "Set up a template informing your login credentials and password for the City of Santo André.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Santo André."
        },
        "iss_santo_andre_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download simultâneo de diferentes guias de ISS relacionadas à credencial da Prefeitura de Santo André informada.",
            "en": "This service issues and downloads different ISS guides related to the informed Santo André City Hall credential at the same time.",
            "es": "Este servicio emite y descarga al mismo tiempo diferentes guías ISS relacionadas con la credencial informada del Ayuntamiento de Santo André."
        },
        "afip_argentina_title_and_subtitle": {
            "pt-BR": "Consulta de Retenção de Segurança Social",
            "en": "Social Security Withholding Consultation",
            "es": "Consulta de Retenciones del Seguro Social"
        },
        "afip_argentina_example_input": {
            "pt-BR": "Exemplo: \"AFIP-Segurança Social\"",
            "en": "Example: \"AFIP- Social Security\"",
            "es": "Ejemplo: \"AFIP- Seguridad Social"
        },
        "afip_argentina_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da AFIP. Para fornecer as outras informações necessárias pra consultar as retenções da Segurança Social, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Configure a template by entering your AFIP login credentials and password. To provide the other information necessary to consult Social Security withholdings, download and fill in the Standard File provided below and use the completed file in the template configuration.",
            "es": "Configure un registro ingresando sus credenciales de ingreso y contraseña de la AFIP. Para facilitar el resto de información necesaria para consultar las retenciones de la Seguridad Social, descargue y rellene el Fichero Tipo que se facilita a continuación y utilice el fichero cumplimentado en la configuración de la registro."
        },
        "afip_argentina_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das retenções da Segurança Social relacionadas à credencial da AFIP informada.",
            "en": "This service issues and downloads Social Security withholdings related to the reported AFIP credential.",
            "es": "Este servicio emite y descarga las retenciones del Seguro Social relacionadas con la credencial AFIP reportada."
        },
        "arba_argentina_title_and_subtitle": {
            "pt-BR": "Consulta do Registo do Regime de Cobrança - Alíquota por Assunto | ARBA",
            "en": "Consultation of the Register of the Collection Regime - Aliquot by Subject | ARBA",
            "es": "Consulta del Padrón de Régimen de Recaudación - Alícuota por Sujeto | ARBA"
        },
        "arba_argentina_example_input": {
            "pt-BR": "Exemplo: \"ARBA- Alíquota por assunto\"",
            "en": "Example: \"ARBA- Aliquot per subject\"",
            "es": "Ejemplo: \"ARBA- Alícuota por sujeto\""
        },
        "arba_argentina_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da ARBA . Para fornecer as outras informações necessárias (prazo de validade) para consultar o Cadastro de Arrecadação - alíquota por assunto, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Set up a template by providing your ARBA login and password credentials. To provide the other necessary information (expiration period) to consult the Collection Register - rate by subject, download and fill in the Standard File available below and use the filled file in the model configuration.",
            "es": "Configure un registro proporcionando sus credenciales de inicio de sesión y contraseña de ARBA. Para proporcionar la otra información necesaria (plazo de caducidad) para consultar el Padrón de Recaudación - alícuota por sujeto, descargue y complete el Archivo Estándar disponible a continuación y use el archivo completo en la configuración del modelo."
        },
        "arba_argentina_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download do Cadastro de Arrecadação - alíquota por assunto, relacionadas à credencial da ARBA informada.",
            "en": "This service issues and downloads the Collection Registry - rate per subject, related to the informed ARBA credential.",
            "es": "Este servicio emite y descarga el Padrón de Recaudación - alícuota por sujeto, relacionado con la credencial ARBA informada."
        },
        'agip_argentina_title_and_subtitle': {
            'pt-BR': 'Registro de Regimes Gerais | AGIP',
            'en': 'Register of General Regimes | AGIP',
            'es': 'Padrón de Regímenes Generales | AGIP'
        },
        'agip_argentina_example_input': {
            'pt-BR': 'Exemplo: "AGIP - Regimes Gerais"',
            'en': 'Example: "AGIP- General Regimes"',
            'es': 'Ejemplo: "AGIP- Regímenes Generales"'
        },
        'agip_argentina_instructions': {
            'pt-BR': 'Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os campos de mês e ano do período de validade que deseja consultar. Importante: no caso de execução em modo agendado, este arquivo deve ser carregado sem dados no Registro (ou seja, vazio), sendo considerado o mês e ano atual. Em seguida configure um modelo utilizando o arquivo preenchido.',
            'en': 'Download and fill in the Standard File provided below with the month and year fields of the validity period you wish to consult. Important: in the case of execution in scheduled mode, this file must be loaded without data in the Registry (ie, empty), considering the current month and year. Then configure a model using the filled file.',
            'es': 'Descargue y complete el Archivo Estándar disponible a continuación con los campos de mes y año del período de vigencia que desea consultar. Importante: en el caso de ejecución en modo programado, este archivo debe cargarse sin datos en el Registro (es decir, vacío), considerando el mes y año en curso. Luego configure un modelo utilizando el archivo completo.'
        },
        'agip_argentina_title_about_the_service': {
            'pt-BR': 'Com esse Serviço você consegue consultar simultaneamente o Registo de Regimes Gerais no AGIP.',
            'en': 'With this Service you can simultaneously consult the General Regimes Registry at AGIP.',
            'es': 'Con este Servicio puede consultar simultáneamente el Registro de Regímenes Generales en la AGIP.'
        },
        'agip_argentina_subtitle_about_the_service': {
            'pt-BR': 'Ao final da execução do serviço, você irá receber os comprovantes do Registo de Regimes Gerais , assim como um arquivo de resumo das informações.',
            'en': 'At the end of the service, you will receive receipts from the General Regimes Registry, as well as a summary file of the information.',
            'es': 'Al finalizar el servicio, recibirá comprobantes del Registro de Regímenes Generales, así como un expediente resumen de la información.'
        },
        'standard_file_download': {
            'pt-BR': 'Download de Arquivo Padrão',
            'en': 'Standard File Download',
            'es': 'Descarga de archivos estándar'
        },
        'about_the_service': {
            'pt-BR': 'SOBRE O SERVIÇO',
            'en': 'ABOUT THE SERVICE',
            'es': 'SOBRE EL SERVICIO'
        },
        'schedule_execution': {
            'pt-BR': 'Agendar execução',
            'en': 'Schedule execution',
            'es': 'Progamar la ejecucción'
        },
        'run_now': {
            'pt-BR': 'Executar agora',
            'en': 'Run now',
            'es': 'Corre ahora'
        },
        'run_template': {
            'pt-BR': 'Executar modelo',
            'en': 'Run template',
            'es': 'Corre registro'
        },
        'starting': {
            'pt-BR': 'Iniciando',
            'en': 'Starting',
            'es': 'A partir de'
        },
        'status': {
            'pt-BR': 'Status',
            'en': 'Status',
            'es': 'Estado'
        },
        'in_progress': {
            'pt-BR': 'Em andamento',
            'en': 'In progress',
            'es': 'En proceso'
        },
        'email_sent': {
            'pt-BR': 'E-mail enviado',
            'en': 'E-mail sent',
            'es': 'Email enviado'
        },
        'template_not_found': {
            'pt-BR': 'Modelo não encontrado',
            'en': 'Template not found',
            'es': 'Registro no encontrado'
        },
        'unable_to_save_appointment': {
            'pt-BR': 'Não foi possível salvar o agendamento',
            'en': 'Unable to save appointment',
            'es': 'No fue posible guardar el horario'
        },
        'you_have_scheduled_the_next_runs_of_your_template': {
            'pt-BR': 'Você agendou as próximas execuções do seu modelo',
            'en': 'You have scheduled the next runs of your template',
            'es': 'Programaste las próximas ejecuciones de su registro'
        },
        'check_the_information_below': {
            'pt-BR': 'Confira abaixo as informações',
            'en': 'Check the information below',
            'es': 'Revisa la información a continuación'
        },
        'template_model': {
            'pt-BR': 'Modelo',
            'en': 'Template',
            'es': 'Registro'
        },
        'template_model_small': {
            'pt-BR': 'modelo',
            'en': 'template',
            'es': 'registro'
        },
        'service': {
            'pt-BR': 'Serviço',
            'en': 'Service',
            'es': 'Servicio'
        },
        'start_date': {
            'pt-BR': 'Data de inicio',
            'en': 'Start date',
            'es': 'Fecha de inicio'
        },
        'recurrence': {
            'pt-BR': 'Recorrência',
            'en': 'Recurrence',
            'es': 'Reaparición'
        },
        'this_means_that_your_template_will_run': {
            'pt-BR': 'Isso quer dizer que seu modelo será executado',
            'en': 'This means that your template will run',
            'es': 'Esto significa que su registro se ejecutará'
        },
        'monthly': {
            'pt-BR': 'mensalmente',
            'en': 'monthly',
            'es': 'mensual'
        },
        'monthly_capitalized': {
            'pt-BR': 'Mensalmente',
            'en': 'Monthly',
            'es': 'Mensual'
        },
        'monthly_capitalized_small_portuguese': {
            'pt-BR': 'Mensal',
            'en': 'Monthly',
            'es': 'Mensual'
        },
        'weekly': {
            'pt-BR': 'semanalmente',
            'en': 'weekly',
            'es': 'semanalmente'
        },
        'weekly_capitalized': {
            'pt-BR': 'Semanalmente',
            'en': 'Weekly',
            'es': 'Semanalmente'
        },
        'does_not_repeat': {
            'pt-BR': 'Não se repete',
            'en': 'Does not repeat',
            'es': 'No repite'
        },
        'you_will_receive_your_results_via_email_as_usual_as_soon_as_they_are_available': {
            'pt-BR': 'Você receberá seus resultados por e-mail normalmente assim que eles estiverem disponíveis',
            'en': 'You will receive your results via email as usual as soon as they are available',
            'es': 'Recibirá sus resultados por correo electrónico como de costumbre tan pronto como estén disponibles'
        },
        'appointment_created_successfully': {
            'pt-BR': 'Agendamento criado com sucesso!',
            'en': 'Appointment created successfully!',
            'es': '¡Horario creado con éxito!'
        },
        'every_day': {
            'pt-BR': 'todo dia',
            'en': 'every day',
            'es': 'todos los dias'
        },
        'every_female': {
            'pt-BR': 'toda',
            'en': 'every',
            'es': 'cada'
        },
        'every_male': {
            'pt-BR': 'todo',
            'en': 'every',
            'es': 'todos los'
        },
        'week_6': {
            'pt-BR': 'Domingo',
            'en': 'Sunday',
            'es': 'Domingo',
        },
        'week_0': {
            'pt-BR': 'Segunda-feira',
            'en': 'Monday',
            'es': 'Lunes',
        },
        'week_1': {
            'pt-BR': 'Terça-feira',
            'en': 'Tuesday',
            'es': 'Martes',
        },
        'week_2': {
            'pt-BR': 'Quarta-feira',
            'en': 'Wednesday',
            'es': 'Miércoles',
        },
        'week_3': {
            'pt-BR': 'Quinta-feira',
            'en': 'Thursday',
            'es': 'Jueves',
        },
        'week_4': {
            'pt-BR': 'Sexta-feira',
            'en': 'Friday',
            'es': 'Viernes',
        },
        'week_5': {
            'pt-BR': 'Sábado',
            'en': 'Saturday',
            'es': 'Sábado',
        },
        'of': {
            'pt-BR': 'de',
            'en': 'of',
            'es': 'de',
        },
        'starting_in': {
            'pt-BR': 'começando em',
            'en': 'starting in',
            'es': 'comenzando en el',
        },
        'next_female': {
            'pt-BR': 'na próxima',
            'en': 'next',
            'es': 'el próximo',
        },
        'in_next_male': {
            'pt-BR': 'no próximo',
            'en': 'next',
            'es': 'el próximo',
        },
        'scheduled': {
            'pt-BR': 'Agendado',
            'en': 'Scheduled',
            'es': 'Programado',
        },
        'template_schedule': {
            'pt-BR': 'Agendamento de Modelo',
            'en': 'Template Schedule',
            'es': 'Planificación de Registro',
        },
        'scheduling': {
            'pt-BR': 'Agendamento',
            'en': 'Scheduling',
            'es': 'Planificación',
        },
        'what_day_do_you_want_your_model_to_run': {
            'pt-BR': 'Que dia deseja que seu modelo seja executado?',
            'en': 'What day do you want your model to run?',
            'es': '¿Qué día quieres que funcione tu modelo?',
        },
        'your_model_will_run': {
            'pt-BR': 'Seu modelo será executado',
            'en': 'Your model will run',
            'es': 'Su modelo se ejecutará',
        },
        'on': {
            'pt-BR': 'em',
            'en': 'on',
            'es': 'en',
        },
        'create_schedule': {
            'pt-BR': 'Criar agendamento',
            'en': 'create schedule',
            'es': 'crear horario',
        },
        'repeat': {
            'pt-BR': 'Repetir',
            'en': 'Repeat',
            'es': 'Repetir',
        },
        'confirm_appointment': {
            'pt-BR': 'Confirmar Agendamento?',
            'en': 'Confirm Appointment?',
            'es': '¿Confirmar cita?',
        },
        'you_will_receive_your_results_via_email_as_usual_as_soon_as_they_are_available': {
            'pt-BR': 'Você receberá seus resultados por e-mail normalmente assim que eles estiverem disponíveis.',
            'en': 'You will receive your results via email as usual as soon as they are available.',
            'es': 'Recibirá sus resultados por correo electrónico como de costumbre tan pronto como estén disponibles.',
        },
        "copasa_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Água | Copasa",
            "en": "Issuance of Water Bills | Copasa",
            "es": "Emisión de Facturas de Agua | Copasa"
        },
        "copasa_text_example_input": {
            "pt-BR": "Exemplo: \"Água - COPASA\"",
            "en": "Example: \"Water - COPASA\"",
            "es": "Ejemplo: \"Agua - COPASA\""
        },
        "copasa_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Copasa.",
            "en": "Configure a template by entering your Copasa login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales de inicio de sesión y contraseña de Copasa."
        },
        "copasa_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de água da Copasa de diversos imóveis simultaneamente.",
            "en": "This service issues and downloads Copasa's water bills from several properties simultaneously.",
            "es": "Este servicio emite y descarga las facturas de agua de Copasa de varias propiedades simultáneamente."
        },
        "copasa_credentials": {
            "pt-BR": "Credenciais da COPASA ",
            "en": "COPASA credentials",
            "es": "Credenciales COPASA"
        },
        "comprot_title_and_subtitle": {
            "pt-BR": "Consulta de Processos | COMPROT",
            "en": "Process Consultation | COMPROT",
            "es": "Consulta de Procesos | COMPROT"
        },
        "comprot_text_example_input": {
            "pt-BR": "Exemplo: \"Processos - COMPROT\"",
            "en": "Example: \"Process - COMPROT\"",
            "es": "Ejemplo: \"Processos - COMPROT\""
        },
        "comprot_text_input_small": {
            "pt-BR": "Processos - COMPROT",
            "en": "Process - COMPROT",
            "es": "Processos - COMPROT"
        },
        "comprot_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja realizar a Consulta de Processos na COMPROT. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to carry out the Process Consultation at COMPROT. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJs que desea realizar la Consulta de Procesos en la COMPROT. Luego configure un modelo utilizando el archivo completo."
        },
        "comprot_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre processos dos respectivos CNPJs inserido no modelo.",
            "en": "After using the service, the results arrive by e-mail with information about the registration and the codes of the services registered by the consulted companies.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre el registro y los códigos de servicio registrados por las empresas consultadas."
        },
        "comprot_title_about_the_service": {
            "pt-BR": "Este serviço faz a consulta de processo no site da COMPROT de diversos CNPJs simultaneamente.",
            "en": "This service issues and consults the process on the COMPROT website of several CNPJs simultaneously.",
            "es": "Este servicio emite y consulta el proceso en la página web COMPROT de varios CNPJ simultáneamente."
        },
        "iss_rj_wilson_title_and_subtitle": {
            "pt-BR": "Emissão de guias ISS | Rio de Janeiro",
            "en": "Issuance of ISS guides | Rio de Janeiro",
            "es": "Emisión de guías ISS | Rio de Janeiro"
        },
        "iss_rj_wilson_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha do Nota Carioca.",
            "en": "Configure a template informing your Nota Carioca login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de Nota Carioca."
        },
        "service_requested": {
            "pt-BR": "Serviço Solicitado",
            "en": "Service Requested",
            "es": "Servicio solicitado"
        },
        "issuance_of": {
            "pt-BR": "Emissão de",
            "en": "Issuance of",
            "es": "Emisión de"
        },
        "bank_statement": {
            "pt-BR": "Extrato Bancário",
            "en": "Bank statement",
            "es": "Extracto de cuenta"
        },
        "extrato_bancario_title_and_subtitle": {
            "pt-BR": "Emissão de | Extrato Bancário",
            "en": "Issue of | Bank statement",
            "es": "Emisión de | Extracto de cuenta"
        },
        "extrato_bancario_text_example_input": {
            "pt-BR": "Exemplo: \"Extrato - Bancário\"",
            "en": "Example: \"Extract - Banking\"",
            "es": "Ejemplo: \"Extracto - oficial bancario\""
        },
        "same_login_used_on_the_bank_statement_website": {
            "pt-BR": "Mesmo login utilizado no site de Extrato Bancário",
            "en": "Same login used on the Bank Statement website",
            "es": "El mismo inicio de sesión utilizado en el sitio web del extracto bancario"
        },
        "same_password_used_on_the_bank_statement_website": {
            "pt-BR": "Mesma senha utilizada no site de Extrato Bancário",
            "en": "Same password used on the Bank Statement website",
            "es": "Misma contraseña utilizada en el sitio web del extracto bancario"
        },
        "extrato_bancario_instructions": {
            "pt-BR": "Para configurar um modelo, clique no botão ao lado e solicite o contato dos nossos especialistas: eles irão te auxiliar nas etapas iniciais.",
            "en": "To configure a model, click on the button to the side and request the contact of our specialists: they will help you in the initial steps.",
            "es": "Para configurar un modelo, haga clic en el botón al costado y solicite el contacto de nuestros especialistas: ellos lo ayudarán en los pasos iniciales."
        },
        "after_that_your_model_is_saved_to_use_whenever_you_need_it": {
            "pt-BR": "Depois disso, seu modelo fica salvo para utilizar sempre que precisar.",
            "en": "After that, your model is saved to use whenever you need it.",
            "es": "Después de eso, su modelo se guarda para usarlo cuando lo necesite."
        },
        "banking_credentials": {
            "pt-BR": "Credenciais Bancárias",
            "en": "Banking Credentials",
            "es": "Credenciales Bancarias"
        },
        "extrato_bancario_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz download do extrato bancário da conta e banco que foi configurado.",
            "en": "This service issues and downloads the bank statement for the account and bank that has been configured.",
            "es": "Este servicio emite y descarga el extracto bancario de la cuenta y banco que se haya configurado."
        },
        "extrato_bancario_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber o extrato, assim como um arquivo de resumo das informações.",
            "en": "At the end of the service execution, you will receive the extract, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución del servicio, recibirá el extracto, así como un archivo resumen de la información."
        },
        "template_configuration_request": {
            "pt-BR": "Solicitação de configuração de modelo",
            "en": "Template configuration request",
            "es": "Solicitud de configuración de registro"
        },
        "issuance_of_bank_statement": {
            "pt-BR": "Emissão de Extrato Bancário",
            "en": "Issuance of Bank Statement",
            "es": "Emisión de Extracto Bancario"
        },
        "to_configure_a_template_for_this_service_we_need_to_contact_you_to_help_you_with_some_steps": {
            "pt-BR": "Para configurar um modelo deste serviço, precisamos entrar em contato para te auxiliar em algumas etapas.",
            "en": "To configure a template for this service, we need to contact you to help you with some steps.",
            "es": "Para configurar un registro para este servicio, necesitamos contactarlo para ayudarlo con algunos pasos."
        },
        "do_you_want_to_confirm_this_request_our_experts_will_contact_you_within_24_hours": {
            "pt-BR": "Deseja confirmar essa solicitação? Nossos especialistas irão entrar em contato em até 24 horas.",
            "en": "Do you want to confirm this request? Our experts will contact you within 24 hours.",
            "es": "¿Quieres confirmar esta solicitud? Nuestros expertos se comunicarán con usted dentro de las 24 horas."
        },
        "request_contact": {
            "pt-BR": "Solicitar Contato",
            "en": "Request Contact",
            "es": "Solicitar contacto"
        },
        "request_received": {
            "pt-BR": "Solicitação recebida",
            "en": "Request received",
            "es": "Solicitud recibida"
        },
        "our_experts_will_contact_you_within_24_hours_to_assist_you_with_the_initial_setup_steps": {
            "pt-BR": "Nossos especialistas irão entrar em contato em até 24 horas para te auxiliar nas etapas iniciais de configuração.",
            "en": "Our experts will contact you within 24 hours to assist you with the initial setup steps.",
            "es": "Solicitud recibida"
        },
        'seconds': {
            'pt-BR': 'segundos',
            'en': 'seconds',
            'es': 'segundos'
        },
        'second': {
            'pt-BR': 'segundo',
            'en': 'second',
            'es': 'segundo'
        },
        'minute': {
            'pt-BR': 'minuto',
            'en': 'minute',
            'es': 'minuto'
        },
        'process_took': {
            'pt-BR': 'O processo precisou de',
            'en': 'Process took',
            'es': 'El proceso tomó'
        },
        'to_be_executed': {
            'pt-BR': 'para ser executado',
            'en': 'to be executed',
            'es': 'para ser ejecutado'
        },
        "cnd_pe_title_and_subtitle": {
            "pt-BR": "Emissão de CND | PE",
            "en": "CND Issuance | PE",
            "es": "Emisión de CND | PE"
        },
        "cnd_pe_example_input": {
            "pt-BR": "Exemplo: \"CND - PE\"",
            "en": "Example: \"CND - PE\"",
            "es": "Ejemplo: \"CND - PE\""
        },
        "cnd_pe_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CNPJs para realizar a emissão da Certidão de Negativa e configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJs to issue the Clearance Certificate and configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los CNPJ para emitir el Certificado de Autorización y configurar un registro. Esta información se guarda para que la reutilice cuando la necesite"
        },
        "cnd_bahia_title_and_subtitle": {
            "pt-BR": "Emissão de CND | BA",
            "en": "CND Issuance | BA",
            "es": "Emisión de CND | BA"
        },
        "cnd_bahia_example_input": {
            "pt-BR": "Exemplo: \"CND - Bahia\"",
            "en": "Example: \"CND - Bahia\"",
            "es": "Ejemplo: \"CND - Bahia\""
        },
        "cnd_mg_title_and_subtitle": {
            "pt-BR": "Emissão de CND | MG",
            "en": "CND Issuance | MG",
            "es": "Emisión de CND | MG"
        },
        "cnd_mg_example_input": {
            "pt-BR": "Exemplo: \"CND - MG\"",
            "en": "Example: \"CND - MG\"",
            "es": "Ejemplo: \"CND - MG\""
        },
        "cnd_mg_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os CNPJs que deseja realizar a emissão da Certidão de Negativa no Estado de Minas Gerais para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJs that you want to issue the Certificate of Clearance in the State of Minas Gerais to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Complete el archivo de carga con los CNPJ que desea emitir el Certificado de Autorización en el Estado de Minas Gerais para configurar una registro. Esta información se guarda para que la reutilice cuando la necesite."
        },
        'scheduled_plural': {
            'pt-BR': 'Agendados',
            'en': 'Scheduled',
            'es': 'Programados'
        },
        'there_are_no_scheduled_services': {
            'pt-BR': 'Não há serviços agendados',
            'en': 'There are no scheduled services',
            'es': 'No hay servicios programados'
        },
        'schedule_the_execution_of_the_services_and_follow_them_here': {
            'pt-BR': 'Agende a execução dos serviços e acompanhe eles por aqui. Os agendamento só serão mostrados nessa página 1 mês antes da data programada.',
            'en': 'Schedule the execution of the services and follow them here. Appointments will only be shown on this page 1 month before the scheduled date.',
            'es': 'Programa la ejecución de los servicios y síguelos aquí. Las citas solo se mostrarán en esta página 1 mes antes de la fecha programada.'
        },
        'schedule_the_execution_of_the_services_and_follow_them_here_simplified': {
            'pt-BR': 'Agende seus serviços e escolha quando deseja receber os resultados.',
            'en': 'Schedule your services and choose when you want to receive the results.',
            'es': 'Programa tus servicios y elige cuándo quieres recibir los resultados.'
        },
        'go_to': {
            'pt-BR': 'Ir para',
            'en': 'Go to',
            'es': 'Ir para'
        },
        'until': {
            'pt-BR': 'Até',
            'en': 'Until',
            'es': 'Hasta'
        },
        'forecast': {
            'pt-BR': 'Previsão',
            'en': 'Forecast',
            'es': 'Pronóstico'
        },
        'month_01': {
            'pt-BR': 'Janeiro',
            'en': 'January',
            'es': 'enero',
        },
        'month_02': {
            'pt-BR': 'Fevereiro',
            'en': 'February',
            'es': 'febrero',
        },
        'month_03': {
            'pt-BR': 'Março',
            'en': 'March',
            'es': 'marcha',
        },
        'month_04': {
            'pt-BR': 'Abril',
            'en': 'April',
            'es': 'abril',
        },
        'month_05': {
            'pt-BR': 'Maio',
            'en': 'May',
            'es': 'Mayo',
        },
        'month_06': {
            'pt-BR': 'Junho',
            'en': 'June',
            'es': 'junio',
        },
        'month_07': {
            'pt-BR': 'Julho',
            'en': 'July',
            'es': 'mes de julio',
        },
        'month_08': {
            'pt-BR': 'Agosto',
            'en': 'August',
            'es': 'agosto',
        },
        'month_09': {
            'pt-BR': 'Setembro',
            'en': 'September',
            'es': 'septiembre',
        },
        'month_10': {
            'pt-BR': 'Outubro',
            'en': 'October',
            'es': 'octubre',
        },
        'month_11': {
            'pt-BR': 'Novembro',
            'en': 'November',
            'es': 'noviembre',
        },
        'month_12': {
            'pt-BR': 'Dezembro',
            'en': 'December',
            'es': 'diciembre',
        },
        'repeats_every_day': {
            'pt-BR': 'Repete todo dia',
            'en': 'Repeats every day',
            'es': 'Se repite todos los días',
        },
        'at': {
            'pt-BR': 'às',
            'en': 'at',
            'es': 'a las',
        },
        "pending_configuration_request_sent": {
            "pt-BR": "Pendente - Solicitação de configuração enviada",
            "en": "Pending - Configuration request sent",
            "es": "Pendiente - Solicitud de configuración enviada"
        },
        'contact_requested': {
            'pt-BR': 'Contato solicitado',
            'en': 'Contact requested',
            'es': 'Contacto solicitado'
        },
        "mpf_title_and_subtitle": {
            "pt-BR": "Consulta de Processos | MPF",
            "en": "Legal proceeding consultation | MPF",
            "es": "Consulta de demanda judicial | MPF"
        },
        "mpf_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução, você irá receber arquivos com informações sobre os processos encontrados.",
            "en": "At the end of the execution, you will receive files with information on the matching legal proceedings",
            "es": "Al finalizar la ejecución, recibirá archivos con información sobre el demanda judicial encontradas."
        },
        "mpf_text_example_input": {
            "pt-BR": "Exemplo: \"MPF - Termos de Pesquisa\"",
            "en": "Example: \"MPF - Search Terms\"",
            "es": "Ejemplo: \"MPF - Términos de Búsqueda\""
        },
        "mpf_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os termos de pesquisa que deseja verificar a situação dos processos na MPF. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the search keywords that you want to verify the legal proceeding status on MPF. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los términos de búsqueda que desea verificar la situación de demanda judicial an MPF. Luego configure un modelo utilizando el archivo completo."
        },
        "mpf_title_about_the_service": {
            "pt-BR": "Este serviço faz a consulta de processos no site da MPF para diferentes termos de pesquisa simultaneamente.",
            "en": "This service consults legal proceedings on the MPF website for different search keywords simultaneously.",
            "es": "Este servicio consulta demanda judicial en el sitio web de MPF para diferentes términos de búsqueda simultáneamente."
        },
        "mpf_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre os processos consultados.",
            "en": "After using the service, the results will arrive by e-mail with information of the consulted legal proceedings.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los demanda judicial consultados."
        },
        "der_title_and_subtitle": {
            "pt-BR": "Consulta de Infrações de Transito | DER SP",
            "en": "Traffic Infractions Inquiry | DER SP",
            "es": "Consulta de Infracciones de Tránsito | DER SP"
        },
        "der_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução, você irá receber arquivos com informações sobre as infrações de trânsito encontradas.",
            "en": "At the end of the execution, you will receive files with information on the matching traffic violations",
            "es": "Al finalizar la ejecución, recibirá archivos con información sobre el infraciones encontradas."
        },
        "der_text_example_input": {
            "pt-BR": "Exemplo: \"DER São Paulo - RENAVAM\"",
            "en": "Example: \"DER São Paulo - RENAVAM\"",
            "es": "Ejemplo: \"DER São Paulo - RENAVAM\""
        },
        "der_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os RENAVAM que deseja verificar a situação das infrações de trânsito na DER São Paulo. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the search keywords that you want to verify the traffic violation status on DER São Paulo. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los RENAVAM que desea verificar la situación de infraciones an DER São Paulo. Luego configure un modelo utilizando el archivo completo."
        },
        "der_title_about_the_service": {
            "pt-BR": "Este serviço faz a consulta de infrações de trânsito no site da DER São Paulo para diferentes RENAVAM simultaneamente.",
            "en": "This service consults traffic violations on the DER São Paulo website for different search keywords simultaneously.",
            "es": "Este servicio consulta infraciones en el sitio web de DER São Paulo para diferentes RENAVAM simultáneamente."
        },
        "der_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre as infrações de trânsito consultadas.",
            "en": "After using the service, the results will arrive by e-mail with information of the consulted traffic violations.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los infraciones consultados."
        },
        "shopee_title_and_subtitle": {
            "pt-BR": "Pesquisa e Monitoramento de preços | SHOPEE",
            "en": "Price Research and Monitoring | SHOPEE",
            "es": "Investigación y seguimiento de precios | SHOPEE"
        },
        "shopee_text_example_input": {
            "pt-BR": "Exemplo: \"SHOPEE - Termos de Pesquisa\"",
            "en": "Example: \"SHOPEE - Search Terms\"",
            "es": "Ejemplo: \"SHOPEE - Términos de Búsqueda\""
        },
        "shopee_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os termos de pesquisa que deseja verificar a situação dos produtos na SHOPEE. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the search keywords that you want to verify the product status on SHOPEE. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los términos de búsqueda que desea verificar la situación de productos an SHOPEE. Luego configure un modelo utilizando el archivo completo."
        },
        "shopee_title_about_the_service": {
            "pt-BR": "Este serviço faz a consulta de produtos no site da SHOPEE para diferentes termos de pesquisa simultaneamente.",
            "en": "This service consults products on the SHOPEE website for different search keywords simultaneously.",
            "es": "Este servicio consulta productos en el sitio web de SHOPEE para diferentes términos de búsqueda simultáneamente."
        },
        "shopee_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre os produtos consultados.",
            "en": "After using the service, the results will arrive by e-mail with information of the consulted products.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los productos consultados."
        },
        "anvisa_title_and_subtitle": {
            "pt-BR": "Consulta de Processos | ANVISA",
            "en": "Lawsuit Consultation | ANVISA",
            "es": "Consulta de Procesos | ANVISA"
        },
        "anvisa_text_example_input": {
            "pt-BR": "Exemplo: \"ANVISA - Processos de Fornecedores\"",
            "en": "Example: \"ANVISA - Provider lawsuits\"",
            "es": "Ejemplo: \"ANVISA - Procesos de Proveedores\""
        },
        "anvisa_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja verificar a situação na ANVISA. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs that you want to verify the status on ANVISA. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea verificar la situación an ANVISA. Luego configure un modelo utilizando el archivo completo."
        },
        "anvisa_title_about_the_service": {
            "pt-BR": "Este serviço faz a consulta de processos no site da ANVISA para diferentes CNPJs simultaneamente.",
            "en": "This service consults processes on the ANVISA website for different CNPJs simultaneously.",
            "es": "Este servicio consulta procesos en el sitio web de ANVISA para diferentes CNPJ simultáneamente."
        },
        "anvisa_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as informações sobre os processos das empresas consultadas.",
            "en": "After using the service, the results arrive by e-mail with information about the processes of the companies consulted.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con información sobre los procesos de las empresas consultadas."
        },
        "process_consultation": {
            "pt-BR": "Consulta de Processos",
            "en": "Process Consultation",
            "es": "Consulta de Processos"
        },
        "traffic_violation_consultation": {
            "pt-BR": "Consulta de Infrações de Transito",
            "en": "Traffic Violations Verification",
            "es": "Consulta de infracciones de tráfico"
        },
        "carf_title_and_subtitle": {
            "pt-BR": "Consulta de Processos | CARF",
            "en": "Process Consultation | CARF",
            "es": "Consulta de Procesos | CARF"
        },
        "carf_example_input": {
            "pt-BR": "Exemplo: \"Consulta de Processos - CARF\"",
            "en": "Example: \"Consultation of Processes - CARF\"",
            "es": "Ejemplo: \"Consulta de Procesos - CARF\""
        },
        "carf_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs e o intervalo de datas (mês/ano) que deseja consultar o Acompanhamento Processual de Recursos Fiscais. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs and the range of dates (month/year) that you wish to consult the Procedural Monitoring of Tax Appeals. Then configure a template using the completed file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ y el rango de fechas (mes/año) que desea consultar el Seguimiento Procesal de Recursos Tributarios. Luego configure un registro utilizando el archivo completo."
        },
        "carf_title_about_the_service": {
            "pt-BR": "Este serviço consulta e faz o download dos processos do Conselho Administrativo de Recursos Fiscais (CARF) de diferentes CNPJs simultaneamente.",
            "en": "This service consults and downloads the processes of the Administrative Council of Tax Appeals (CARF) of different CNPJs simultaneously.",
            "es": "Este servicio consulta y descarga los procesos del Consejo Administrativo de Recursos Fiscales (CARF) de diferentes CNPJ simultáneamente."
        },
        "carf_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com o CNPJ e o intervalo de datas que deseja realizar a consulta de processos do CARF para configurar um modelo. Essas informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the CNPJ and the date range that you wish to carry out the query of CARF processes to configure a template. This information is saved for you to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con el CNPJ y el rango de fechas que desea realizar la consulta de procesos CARF para configurar un modelo. Esta información se guarda para que la reutilice cuando la necesite."
        },
        "consultation_of_tax_appeals_processes": {
            "pt-BR": "Consulta de Processos de Recursos Fiscais",
            "en": "Consultation of Tax Appeals Processes",
            "es": "Consulta de Procesos de Recursos Fiscales"
        },
        "divida_ativa_mg_title_and_subtitle": {
            "pt-BR": "Consulta e Regulamentação de Dívida Ativa | MG",
            "en": "Consultation and Regulation of Active Debt | MG",
            "es": "Consulta y Regulación de Deuda Activa | MG"
        },
        "divida_ativa_mg_example_input": {
            "pt-BR": "Exemplo: \"Dívida ativa - MG\"",
            "en": "Example: \"Active debt - MG\"",
            "es": "Ejemplo: \"Deuda activa - MG\""
        },
        "divida_ativa_mg_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs que deseja consultar de Divida Ativa e emitir documento de pagamento. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs you wish to consult for Active Debt and issue payment document. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los CNPJ que desea consultar para Deuda Activa y emitir documento de pago. Luego configure un modelo utilizando el archivo completo."
        },
        "divida_ativa_mg_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com informações sobre o código PTA, tipo de tributo, data de atuação, qualificação, valores totais e seus respectivos boletos.",
            "en": "After using the service, the results arrive by e-mail, with information about the PTA code, type of tax, date of operation, qualification, total amounts and their respective slips.",
            "es": "Luego de utilizar el servicio, los resultados llegan por correo electrónico, con información sobre el código PTA, tipo de impuesto, fecha de operación, calificación, montos totales y sus respectivos comprobantes."
        },
        "divida_ativa_mg_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução, você irá receber arquivos com informações sobre o código PTA, tipo de tributo, data de atuação, qualificação, valores totais e boletos, assim como um arquivo de resumo das informações.",
            "en": "At the end of the execution, you will receive files with information about the PTA code, type of tax, date of operation, qualification, total amounts and slips, as well as a summary file of the information.",
            "es": "Al finalizar la ejecución, recibirá archivos con información sobre el código PTA, tipo de impuesto, fecha de operación, calificación, montos totales y boletas, así como un archivo resumen de la información."
        },
        "cemig_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da CEMIG.",
            "en": "Set up a template by entering your CEMIG login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales y contraseña de inicio de sesión de CEMIG."
        },
        "cemig_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | CEMIG",
            "en": "Issuance of Energy Bills | CEMIG",
            "es": "Emisión de Facturas de Energía | CEMIG"
        },
        "cemig_text_example_input": {
            "pt-BR": "Exemplo: \"Luz - CEMIG\"",
            "en": "Example: \"Light - CEMIG\"",
            "es": "Ejemplo: \"Luz - CEMIG\""
        },
        "same_login_used_on_the_cemig_website": {
            "pt-BR": "Mesmo login utilizado no site da CEMIG",
            "en": "Same login used on the CEMIG website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de CEMIG"
        },
        "same_password_used_on_the_cemig_website": {
            "pt-BR": "Mesma senha utilizada no site da CEMIG",
            "en": "Same password used on the CEMIG website",
            "es": "Misma contraseña utilizada en el sitio web de CEMIG"
        },
        "cemig_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da CEMIG informada.",
            "en": "This service issues and downloads energy bills related to the CEMIG credential informed.",
            "es": "Este servicio emite y descarga facturas de energía relacionadas con la credencial CEMIG informada."
        },
        "cemig_credentials": {
            "pt-BR": "Credenciais da CEMIG",
            "en": "CEMIG Credentials",
            "es": "Credenciales CEMIG"
        },
        "cemig_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da CEMIG e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your CEMIG website credentials and can reuse it whenever you need it.",
            "es": "Con unos pocos clics, configura un registro con las credenciales de su sitio web CEMIG y puede reutilizarla cuando lo necesite."
        },
        "cpfl_paulista_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | CPFL",
            "en": "Issuance of Energy Bills | CPFL",
            "es": "Emisión de Facturas de Energía | CPFL"
        },
        "cpfl_paulista_text_example_input": {
            "pt-BR": "Exemplo: \"CPFL - Emissão de faturas de luz\"",
            "en": "Example: \"CPFL - Issuance power bills\"",
            "es": "Ejemplo: \"CPFL - Emisión facturas de luz\""
        },
        "cpfl_paulista_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os CNPJs e códigos de cliente dos quais deseja baixar as contas no site da CPFL. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the CNPJs and customer codes from which you would like to download the bills from the CPFL website. Then configure a model using the filled file.",
            "es": "Descargue y complete el archivo estándar que se proporciona a continuación con los CNPJ y los códigos de cliente desde los que desea descargar las cuentas de CPFL. Luego configure un registro usando el archivo completo.",
        },
        "cpfl_paulista_title_about_the_service": {
            "pt-BR": "Este serviço faz o download de faturas de luz no site da CPFL para diferentes códigos de cliente e CNPJs simultaneamente.",
            "en": "This service downloads electricity bills from the CPFL website for different customer codes and CNPJs simultaneously.",
            "es": "Este servicio descarga las facturas de electricidad del sitio web de CPFL para diferentes códigos de clientes y CNPJ simultáneamente."
        },
        "cpfl_paulista_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber arquivos PDF para cada código de cliente, assim como um arquivo de resumo das informações da execução.",
            "en": "At the end of the service execution, you will receive PDF files for each client code, as well as a summary file of the execution information.",
            "es": "Al final de la ejecución del servicio, recibirá archivos PDF para cada código de cliente, así como un archivo de resumen de la información de ejecución."
        },
        "cpfl_paulista_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os códigos de cliente e CNPJs e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the customer codes and CNPJs and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los códigos de cliente y CNPJ y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "cpfl_paulista_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com os arquivos PDF das faturas baixadas.",
            "en": "After using the service, the results arrive by e-mail with the downloaded bill PDF files.",
            "es": "Después de usar el servicio, los resultados llegan por e-mail con archivos PDF de las facturas descargadas."
        },
        "consulta_antt_rntrc_title_and_subtitle": {
            "pt-BR": "Consulta Pública de Transportadores | ANTT",
            "en": "Public Hauler Consultation | ANTT",
            "es": "Consulta Pública de Transportistas | ANTT"
        },
        "consulta_antt_rntrc_text_example_input": {
            "pt-BR": "Exemplo: \"ANTT - Consulta de RNTRC\"",
            "en": "Example: \"ANTT - RNTRC Consultation\"",
            "es": "Ejemplo: \"ANTT - Consulta Pública de RNTRC\""
        },
        "consulta_antt_rntrc_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com Códigos de RNTRC dos quais deseja consultar no site da ANTT. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File provided below with the RNTRC Codes that you want to consult on the ANTT website. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar que se proporciona a continuación con los Códigos RNTRC que desea consultar en el sitio web de la ANTT. Luego configure un modelo utilizando el archivo completado."
        },
        "consulta_antt_rntrc_title_about_the_service": {
            "pt-BR": "Este serviço consulta no site da ANTT a aptidão de transportadores para realizar o transporte remunerado de cargas.",
            "en": "This service checks on the ANTT website the ability of haulers to carry out remunerated cargo transportation.",
            "es": "Este servicio consulta en el sitio web de la ANTT la capacidad de los transportistas para realizar transportes de carga remunerados."
        },
        "consulta_antt_rntrc_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber arquivos PDF como comprovante das consultas de transportadores, assim como um arquivo de resumo das informações da execução.",
            "en": "At the end of the execution of the service, you will receive PDF files as hauler consultation statements, as well as a summary file of the execution information.",
            "es": "Al finalizar la ejecución del servicio, recibirá archivos PDF como comprobantes de las consultas de transportistas, así como un archivo resumen de la información de ejecución."
        },
        "consulta_antt_rntrc_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os códigos de RNTRC e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the RNTRC codes and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los códigos de RNTRC y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "consulta_antt_rntrc_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com os arquivos PDF das consultas realizadas.",
            "en": "After using the service, the results arrive by e-mail with the downloaded PDF files.",
            "es": "Después de usar el servicio, los resultados llegan por e-mail con archivos PDF de las consultas realizadas."
        },
        "public_hauler_consultation": {
            "pt-BR": "Consulta Pública de Transportadores",
            "en": "Public Hauler Consultation",
            "es": "Consulta Pública de Transportistas"
        },
        'drag_the_file_or_click_the_upload_button': {
            'pt-BR': 'Arraste o arquivo ou clique no botão para fazer upload',
            'en': 'Drag the file or click the upload button',
            'es': 'Arrastre el archivo o haga clic en el botón para cargar',
        },
        'choose_file': {
            'pt-BR': 'Escolher Arquivo',
            'en': 'Choose File',
            'es': 'Elija el archivo',
        },
        'file_upload_completed': {
            'pt-BR': 'Upload de arquivo finalizado:',
            'en': 'File upload completed:',
            'es': 'Carga de archivo fija:',
        },
        "in_the_next_14_days_enjoy_hub": {
            "pt-BR": "Nos próximos 14 dias, você poderá aproveitar todas as vantagens da plataforma de maneira ilimitada.",
            "en": "In the next 14 days, you will be able to enjoy all the advantages of the platform in an unlimited way.",
            "es": "En los próximos 14 días podrás disfrutar de todas las ventajas de la plataforma de forma ilimitada."
        },
        "how_to_begin": {
            "pt-BR": "Como começar",
            "en": "How to begin",
            "es": "Como empezar"
        },
        "here_are_some_tips_lets_check": {
            "pt-BR": "Separamos aqui algumas dicas para te ajudar nos primeiros passos dentro da plataforma e aproveitar ao máximo o Smarthis Hub. Vamos conferir?",
            "en": "Here are some tips to help you with your first steps within the platform and make the most of Smarthis Hub. Shall we check?",
            "es": "Aquí hay algunos consejos para ayudarlo en sus primeros pasos dentro de la plataforma y aprovechar al máximo Smarthis Hub. ¿Vamos a comprobar?"
        },
        "check_tips": {
            "pt-BR": "Conferir dicas",
            "en": "Check tips",
            "es": "Consultar consejos"
        },
        "only_with_hub_you": {
            "pt-BR": "Apenas com o Hub você...",
            "en": "Only with the Hub you...",
            "es": "Solo con el Hub usted..."
        },
        "by_clicking_here": {
            "pt-BR": "clicando aqui",
            "en": "by clicking here",
            "es": "haciendo clic aquí"
        },
        "we_hope_you_are_enjoying_your_trial_period": {
            "pt-BR": "Esperamos que você esteja aproveitando o seu período de teste!",
            "en": "We hope you are enjoying your trial period!",
            "es": "¡Esperamos que estés disfrutando de tu período de prueba!"
        },
        "you_still_have": {
            "pt-BR": "Você ainda tem",
            "en": "You still have",
            "es": "Todavía tienes"
        },
        "to_continue_discovering_advantages": {
            "pt-BR": "para continuar conhecendo todas as vantagens do Smarthis Hub. Acesse sua conta agora",
            "en": "to continue discovering all the advantages of Smarthis Hub. Access your account now",
            "es": "para seguir descubriendo todas las ventajas de Smarthis Hub. Acceda a su cuenta ahora"
        },
        "to_continue_transforming_the_way_you_work": {
            "pt-BR": "para continuar transformando a maneira que você trabalha.",
            "en": "to continue transforming the way you work.",
            "es": "para continuar transformando su forma de trabajar."
        },
        "can_we_help": {
            "pt-BR": "Podemos ajudar?",
            "en": "Can we help?",
            "es": "¿Podemos ayudar?"
        },
        "how_about_scheduling_a_conversation_...": {
            "pt-BR": "Que tal agendar uma conversa para te ajudar a usufruir ainda mais desses dias? Estamos aqui para tirar dúvidas e potencializar o seu período de teste. Sinta-se à vontade para convidar outras áreas da sua empresa para o nosso bate-papo.",
            "en": "How about scheduling a conversation to help you enjoy these days even more? We are here to answer questions and enhance your trial period. Feel free to invite other areas of your company to our chat.",
            "es": "¿Qué tal programar una conversación que te ayude a disfrutar aún más estos días? Estamos aquí para responder preguntas y mejorar su período de prueba. No dude en invitar a otras áreas de su empresa a nuestro chat."
        },
        "schedule_a_conversation": {
            "pt-BR": "Agendar uma conversa",
            "en": "Schedule a conversation",
            "es": "Programar una conversación"
        },
        "we_ve_noticed_you_havent_used_hub": {
            "pt-BR": "Percebemos que você ainda não utilizou os serviços que selecionou no início do seu período de teste. ",
            "en": "We've noticed that you haven't used the services you selected at the beginning of your trial period.",
            "es": "Hemos notado que no ha utilizado los servicios que seleccionó al comienzo de su período de prueba."
        },
        "we_are_here_for_you": {
            "pt-BR": "estamos aqui para você!",
            "en": "we are here for you!",
            "es": "¡Estamos aquí para ti!"
        },
        "we_are_passing_by_let_you_know_two_days_left_trial_...": {
            "pt-BR": "Estamos passando para avisar que o seu período de testes do Smarthis Hub irá acabar depois de amanhã, Isso significa que você tem apenas mais 02 dias para aproveitar suas licenças ilimitadas!",
            "en": "We are passing by to let you know that your Smarthis Hub trial period will end the day after tomorrow, which means you only have 2 more days to enjoy your unlimited licenses!",
            "es": "Estamos de paso para informarle que su período de prueba de Smarthis Hub finalizará pasado mañana, lo que significa que solo tiene 2 días más para disfrutar de sus licencias ilimitadas."
        },
        "learn_more_about_available_plans": {
            "pt-BR": "Conheça mais sobre os planos disponíveis com antecendência e se prepare para escolher aquele que se adequa mais às necessidades da sua equipe.",
            "en": "Learn more about the available plans in advance and get ready to choose the one that best suits your team's needs.",
            "es": "Conoce con anticipación los planes disponibles y prepárate para elegir el que mejor se adapte a las necesidades de tu equipo."
        },
        "brespoke_plans": {
            "pt-BR": "Planos sob medida",
            "en": "Bespoke plans",
            "es": "Planes a medida"
        },
        "didnt_find_the_ideal_plan_...": {
            "pt-BR": "Não encontrou o plano ideal para potencializar os processos da sua empresa? Nós estamos disponíveis para te auxiliar neste momento tão importante. Clique no botão abaixo para agendar uma conversa com um dos nossos especialistas:",
            "en": "Didn't find the ideal plan to enhance your company's processes? We are available to assist you at this important time. Click the button below to schedule a conversation with one of our experts:",
            "es": "¿No encontraste el plan ideal para potenciar los procesos de tu empresa? Estamos disponibles para ayudarle en este momento importante. Haga clic en el botón a continuación para programar una conversación con uno de nuestros expertos:"
        },
        "talk_to_expert": {
            "pt-BR": "Falar com especialista",
            "en": "Talk to expert",
            "es": "Hablar con un experto"
        },
        "discover_hub_plans": {
            "pt-BR": "Conhecer planos do Hub",
            "en": "Discover Hub plans",
            "es": "Descubre los planes Hub"
        },
        "your_trial_period_ended": {
            "pt-BR": "O seu período de testes no Smarthis Hub chegou ao fim.",
            "en": "Your trial period on Smarthis Hub has come to an end.",
            "es": "Su período de prueba en Smarthis Hub ha llegado a su fin."
        },
        "it_was_incredible_14_days_...": {
            "pt-BR": "Foram 14 dias incríveis utilizando os serviços de maneira ilimitada e conhecendo mais das possiblidades que só Hub pode te oferecer.",
            "en": "It was an incredible 14 days using the services in an unlimited way and getting to know more about the possibilities that only Hub can offer you.",
            "es": "Fueron 14 días increíbles usando los servicios de manera ilimitada y conociendo más de las posibilidades que solo Hub te puede ofrecer."
        },
        "now_find_perfect_plan_...": {
            "pt-BR": "Agora é só encontrar o plano perfeito para continuar aproveitando todas as vantagens! Conheça mais sobre os planos disponíveis e escolha aquele que se adequa mais às necessidades da sua equipe.  ",
            "en": "Now all you have to do is find the perfect plan to continue enjoying all the benefits! Learn more about the available plans and choose the one that best suits your team's needs.",
            "es": "¡Ahora solo te queda encontrar el plan perfecto para seguir disfrutando de todos los beneficios! Conoce más sobre los planes disponibles y elige el que mejor se adapte a las necesidades de tu equipo."
        },
        "we_know_that_choosing_the_perfect_plan_is_hard_...": {
            "pt-BR": "Sabemos que escolher o plano perfeito para atender as necessidades da sua equipe pode ser uma tarefa difícil.",
            "en": "We know that choosing the perfect plan to meet your team's needs can be a daunting task.",
            "es": "Sabemos que elegir el plan perfecto para satisfacer las necesidades de su equipo puede ser una tarea abrumadora."
        },
        "so_we_thought_in_asking_you_...": {
            "pt-BR": "Por isso, pensamos em entrar em contato para perguntar:",
            "en": "So we thought we'd get in touch to ask:",
            "es": "Así que pensamos en ponernos en contacto para preguntar:"
        },
        "we_are_available_to_chat_...": {
            "pt-BR": "Estamos à disposição para bater um papo e te auxiliar a entender qual plano vai continuar potencializando a maneira que você trabalha. Clique no botão abaixo para agendar uma conversa com um dos nossos especialistas:",
            "en": "We are available to chat and help you understand which plan will continue to enhance the way you work. Click the button below to schedule a conversation with one of our experts:",
            "es": "Estamos disponibles para chatear y ayudarlo a comprender qué plan continuará mejorando su forma de trabajar. Haga clic en el botón a continuación para programar una conversación con uno de nuestros expertos:"
        },
        "manage_appointments": {
            "pt-BR": "Gerenciar agendamentos",
            "en": "Manage appointments",
            "es": "Gestionar horarios"
        },
        "appointments": {
            "pt-BR": "Agendamentos",
            "en": "Appointments",
            "es": "Horarios"
        },
        "repeats": {
            "pt-BR": "Repete",
            "en": "Repeats",
            "es": "Repite"
        },
        "no_starting_date_was_selected": {
            "pt-BR": "Nenhuma data de início foi selecionada",
            "en": "No starting date was selected",
            "es": "No se ha seleccionado ninguna fecha de inicio"
        },
        'unable_to_remove_appointment': {
            'pt-BR': 'Não foi possível remover o agendamento',
            'en': 'Unable to remove appointment',
            'es': 'No fue posible eliminar el horario'
        },
        "public_hauler_consultation": {
            "pt-BR": "Consulta Pública de Transportadores",
            "en": "Public Hauler Consultation",
            "es": "Consulta Pública de Transportistas"
        },
        "how_to_begin": {
            "pt-BR": "Como começar",
            "en": "How to begin",
            "es": "Como empezar"
        },
        "check_tips": {
            "pt-BR": "Conferir dicas",
            "en": "Check tips",
            "es": "Consultar consejos"
        },
        "only_with_hub_you": {
            "pt-BR": "Apenas com o Hub você...",
            "en": "Only with the Hub you...",
            "es": "Solo con el Hub usted..."
        },
        "if_you_have_questions_reply_email_...": {
            "pt-BR": "Caso tenha alguma dúvida, fique à vontade para responder este e-mail. Ou, caso prefira, agende um bate papo com um dos nossos especialistas",
            "en": "If you have any questions, feel free to reply to this email. Or, if you prefer, schedule a chat with one of our experts",
            "es": "Si tiene alguna pregunta, no dude en responder a este correo electrónico. O, si lo prefiere, programe una charla con uno de nuestros expertos"
        },
        "if_you_have_questions_reply_email": {
            "pt-BR": "Caso tenha alguma dúvida, fique à vontade para responder este e-mail.",
            "en": "If you have any questions, feel free to reply to this email.",
            "es": "Si tiene alguna pregunta, no dude en responder a este correo electrónico."
        },
        "by_clicking_here": {
            "pt-BR": "clicando aqui",
            "en": "by clicking here",
            "es": "haciendo clic aquí"
        },
        "we_can_help": {
            "pt-BR": "Podemos ajudar?",
            "en": "We can help?",
            "es": "¿Podemos ayudar?"
        },
        "how_about_scheduling_a_conversation_...": {
            "pt-BR": "Que tal agendar uma conversa para te ajudar a usufruir ainda mais desses dias? Estamos aqui para tirar dúvidas e potencializar o seu período de teste. Sinta-se à vontade para convidar outras áreas da sua empresa para o nosso bate-papo.",
            "en": "How about scheduling a conversation to help you enjoy these days even more? We are here to answer questions and enhance your trial period. Feel free to invite other areas of your company to our chat.",
            "es": "¿Qué tal programar una conversación que te ayude a disfrutar aún más estos días? Estamos aquí para responder preguntas y mejorar su período de prueba. No dude en invitar a otras áreas de su empresa a nuestro chat."
        },
        "schedule_a_conversation": {
            "pt-BR": "Agendar uma conversa",
            "en": "Schedule a conversation",
            "es": "Programar una conversación"
        },
        "we_ve_noticed_you_havent_used_hub": {
            "pt-BR": "Percebemos que você ainda não utilizou os serviços que selecionou no início do seu período de teste. ",
            "en": "We've noticed that you haven't used the services you selected at the beginning of your trial period.",
            "es": "Hemos notado que no ha utilizado los servicios que seleccionó al comienzo de su período de prueba."
        },
        "we_are_here_for_you": {
            "pt-BR": "estamos aqui para você!",
            "en": "we are here for you!",
            "es": "¡Estamos aquí para ti!"
        },
        "brespoke_plans": {
            "pt-BR": "Planos sob medida",
            "en": "Bespoke plans",
            "es": "Planes a medida"
        },
        "talk_to_expert": {
            "pt-BR": "Falar com especialista",
            "en": "Talk to expert",
            "es": "Hablar con un experto"
        },
        "discover_hub_plans": {
            "pt-BR": "Conhecer planos do Hub",
            "en": "Discover Hub plans",
            "es": "Descubre los planes Hub"
        },
        "credit_card": {
            "pt-BR": "Cartão de crédito",
            "en": "Credit card",
            "es": "Tarjeta de crédito"
        },
        "boleto": {
            "pt-BR": "Boleto Bancário",
            "en": "Brazilian Boleto Bancário",
            "es": "Boleto Bancario brasileño"
        },
        "your_plan_subscription": {
            "pt-BR": "A contratação do seu plano",
            "en": "Your plan subscription",
            "es": "Su suscripción al plan"
        },
        "has_been_confirmed": {
            "pt-BR": "foi confirmada!",
            "en": "has been confirmed!",
            "es": "ha sido confirmada!"
        },
        "we_are_very_happy_to_receive_you_...": {
            "pt-BR": "Ficamos muito felizes de poder te receber oficialmente no Smarthis Hub e agradecemos por contar com a gente nos próximos passos da transformação digital da sua empresa.",
            "en": "We are very happy to be able to officially welcome you to Smarthis Hub and thank you for counting on us in the next steps of your company's digital transformation.",
            "es": "Estamos muy contentos de poder darle la bienvenida oficialmente a Smarthis Hub y le agradecemos que cuente con nosotros en los próximos pasos de la transformación digital de su empresa."
        },
        "check_the_information_below_carefully_...": {
            "pt-BR": "Confira as informações abaixo com atenção. Se notar alguma inconsistência, entre em contato para que possamos solucionar o quanto antes.",
            "en": "Check the information below carefully. If you notice something wrong, please contact us so we can resolve it as soon as possible.",
            "es": "Verifique cuidadosamente la siguiente información. Si nota algún problema, póngase en contacto con nosotros para que podamos solucionarlo lo antes posible."
        },
        "license_sharing": {
            "pt-BR": "Compartilhamento de licenças",
            "en": "License sharing",
            "es": "Uso compartido de licencias"
        },
        "signature_date": {
            "pt-BR": "Data da assinatura",
            "en": "Signature date",
            "es": "Fecha de firma"
        },
        "modality": {
            "pt-BR": "Modalidade",
            "en": "Modality",
            "es": "Modalidad"
        },
        "welcome_to_hub": {
            "pt-BR": "Bem vindo ao HUB",
            "en": "Welcome to HUB",
            "es": "Bienvenido a HUB"
        },
        "tooltip_phone_register": {
            "pt-BR": "Gostaríamos de uma comunicação mais rápida para novidades e suporte. Este número não sera divulgado e nem utilizado para SPAM.",
            "en": "We would like faster communication for news and support. This number will not be disclosed nor used for SPAM.",
            "es": "Nos gustaría una comunicación más rápida para noticias y soporte. Este número no será divulgado ni utilizado para SPAM."
        },
        "cell": {
            "pt-BR": "Celular",
            "en": "Cell",
            "es": "Celúla"
        },
        "correios_title_and_subtitle": {
            "pt-BR": "Monitoramento de Entregas | Correios",
            "en": "Delivery Monitoring | Correios",
            "es": "Monitoreo de Entregas | Correios"
        },
        "correios_text_example_input": {
            "pt-BR": "Exemplo: \"Correios - Monitoramento\"",
            "en": "Example: \"Correios - Monitoring\"",
            "es": "Ejemplo: \"Correios - Monitoreo\""
        },
        "correios_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os Códigos de Rastreamento que deseja verificar nos Correios. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the Tracking Codes who wish to verify their registration with the Correios. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los Códigos de Seguimiento que deseen verificar en los Correios. Luego configure un modelo utilizando el archivo completo."
        },
        "correios_title_about_the_service": {
            "pt-BR": "Este serviço monitora os produtos transportados pelos Correios, com diferentes Códigos de Rastreamento simultaneamente.",
            "en": "This service monitors the products transported by Correios, with different Tracking Codes simultaneously.",
            "es": "Este servicio monitorea los productos transportados por Correios, con diferentes Códigos de Seguimiento simultáneamente."
        },
        "correios_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber um arquivo de resumo das informações sobre a localização e o status mais recente de cada código de rastreamento.",
            "en": "At the end of the service, you will receive a summary file of information about the location and the most recent status of each tracking code.",
            "es": "Al final del servicio, recibirá un archivo de resumen de información sobre la ubicación y el estado más actual de cada código de seguimiento."
        },
        "correios_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os Códigos de Rastreamento e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the Tracking Codes and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los Códigos de Seguimiento y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "correios_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, o resultado chega por e-mail informando a localização e o status mais recente de cada código de rastreamento.",
            "en": "After using the service, the result arrives by e-mail informing the location and most recent status of each tracking code.",
            "es": "Después de utilizar el servicio, el resultado llega por correo electrónico informando la ubicación y el estado más reciente de cada código de seguimiento."
        },
        "delivery_monitoring": {
            "pt-BR": "Monitoramento de Entregas",
            "en": "Delivery Monitoring",
            "es": "Monitoreo de Entregas"
        },
        "register_process": {
            "pt-BR": "Cadastrar Processo",
            "en": "Register Process",
            "es": "Registrar Proceso"
        },
        "registered": {
            "pt-BR": "Cadastrados",
            "en": "Registered",
            "es": "Registrados"
        },
        "not_registered": {
            "pt-BR": "Não cadastrados",
            "en": "Not registered",
            "es": "No registrados"
        },
        "sub_hyphen_processes": {
            "pt-BR": "Sub-processos",
            "en": "Sub-processes",
            "es": "Subprocesos"
        },
        "sub_hyphen_process": {
            "pt-BR": "Sub-processo",
            "en": "Sub-process",
            "es": "Subproceso"
        },
        "action": {
            "pt-BR": "Ação",
            "en": "Action",
            "es": "Acción"
        },
        "general": {
            "pt-BR": "Geral",
            "en": "General",
            "es": "General"
        },
        "investment": {
            "pt-BR": "Investimento",
            "en": "Investment",
            "es": "Inversión"
        },
        "select": {
            "pt-BR": "Selecionar",
            "en": "Select",
            "es": "Seleccione"
        },
        "no_process_registered_so_far": {
            "pt-BR": "Nenhum Processo cadastrado até o momento",
            "en": "No Process registered so far",
            "es": "Ningún proceso registrado hasta el momento"
        },
        "start_registering_to_improve_visualization_of_your_dashboard_executions_and_returns": {
            "pt-BR": "Comece a cadastrar para melhorar a visualização de execuções e retornos no seu Dashboard",
            "en": "Start registering to improve visualization of your Dashboard executions and returns",
            "es": "Comienza a registrarte para mejorar la visualización de ejecuciones y devoluciones en tu Dashboard"
        },
        "all_sub_processes_were_registered": {
            "pt-BR": "Todos Sub-processos foram cadastrados",
            "en": "All Sub-processes were registered",
            "es": "Todos los Subprocesos han sido registrad"
        },
        "now_your_dashboard_will_bring": {
            "pt-BR": "Agora o seu Dashboard vai trazer uma visualização ainda mais exata das execuções e retornos da sua operação",
            "en": "Now your Dashboard will bring an even more accurate view of the executions and returns related to your operation",
            "es": "Ahora tu Dashboard traerá una visión aún más precisa de las ejecuciones y devoluciones de tu operación"
        },
        "go_to_dashboard": {
            "pt-BR": "Ir para o Dashboard",
            "en": "Go to Dashboard",
            "es": "Ir al Dashboard"
        },
        "transactions_by_execution": {
            "pt-BR": "Transações por execução",
            "en": "Transactions by execution",
            "es": "Transacciones por ejecución"
        },
        "unique": {
            "pt-BR": "Única",
            "en": "Unique",
            "es": "Singular"
        },
        "inform_in_seconds": {
            "pt-BR": "Informe em segundos",
            "en": "Inform in seconds",
            "es": "Informe en segundos"
        },
        "multiple": {
            "pt-BR": "Múltipla",
            "en": "Multiple",
            "es": "Múltiple"
        },
        "information_unavailable": {
            "pt-BR": "Informação indisponível",
            "en": "Information unavailable",
            "es": "Información no disponible"
        },
        "average_time_per_transaction": {
            "pt-BR": "Tempo médio por transação",
            "en": "Average time per transaction",
            "es": "Tiempo promedio por transacción"
        },
        "provide_information_about_this_subprocess": {
            "pt-BR": "Forneça as informações sobre este sub-processo para gerar uma visualização mais exata no Dashboard RPA",
            "en": "Provide information about this sub-process to generate a more accurate view in Dashboard RPA",
            "es": "Proporcione información sobre este subproceso para generar una vista más precisa en Dashboard RPA"
        },
        "only_one_invoice_is_generated_during_execution": {
            "pt-BR": "Apenas uma nota fiscal é gerada durante a execução",
            "en": "Only one invoice is generated during execution",
            "es": "Solo se genera una factura durante la ejecución"
        },
        "multiple_invoices_are_generated_during_execution": {
            "pt-BR": "Várias notas fiscais são geradas durante a execução",
            "en": "Multiple invoices are generated during execution",
            "es": "Se generan varias facturas durante la ejecución"
        },
        "to_edit_a_sub_process_first_register_in_a_process": {
            "pt-BR": "Para editar um Sub-processo, primeiro realize seu cadastro em um Processo",
            "en": "To edit a Sub-process, first register in a Process",
            "es": "Para editar un Sub-Proceso, primero regístrese en un Proceso"
        },
        "select_all_that_apply": {
            "pt-BR": "Selecione todos que se aplicam",
            "en": "Select all that apply",
            "es": "Seleccione todas las que correspondan"
        },
        "tell_us_how_this_process_was_performed_prior_to_rpa_implementation": {
            "pt-BR": "Informe os valores médios em relação a como este processo era realizado antes da implementação do RPA.",
            "en": "Please provide average values ​​for how this process was performed prior to implementing RPA.",
            "es": "Proporcione valores promedio de cómo se realizó este proceso antes de implementar RPA."
        },
        "select_the_subprocesses_that_make_up_this_process": {
            "pt-BR": "Selecione os Sub-processos que compõem este Processo",
            "en": "Select the Sub-Processes that make up this Process",
            "es": "Seleccione los Subprocesos que componen este Proceso"
        },

        "to_start_using_selected_services_1": {
            "pt-BR": "Para começar a utilizar os serviços selecionados, entre na página de",
            "en": "To start using the selected services, enter the",
            "es": "Para comenzar a usar los servicios seleccionados, ingrese a la página"
        },
        "to_start_using_selected_services_2": {
            "pt-BR": "ou encontre todas as opções disponíveis na página de",
            "en": "page, or find all available options on the page",
            "es": "o busque todas las opciones disponibles en la página "
        },
        "omie_title_and_subtitle": {
            "pt-BR": "Lançamento de Contas a Pagar | OMIE",
            "en": "Launching Accounts Payable | OMIE",
            "es": "Lanzamiento de Cuentas por Pagar | OMIE"
        },
        "omie_text_example_input": {
            "pt-BR": "Exemplo: \"OMIE - Contas a Pagar\"",
            "en": "Example: \"OMIE - Accounts Payable\"",
            "es": "Ejemplo: \"OMIE - Cuentas por Pagar\""
        },
        "omie_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da OMIE.",
            "en": "Set up a template by entering your OMIE login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales y contraseña de inicio de sesión de OMIE."
        },
        "omie_title_about_the_service": {
            "pt-BR": "Este serviço monitora um email programado afim de realizar o lançamento das contas a pagar na plataforma OMIE.",
            "en": "This service monitors a scheduled email in order to launch accounts payable on the OMIE platform.",
            "es": "Este servicio monitoriza un correo electrónico programado para lanzar cuentas por pagar en la plataforma OMIE."
        },
        "omie_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber um arquivo de resumos das informações sobre o remetente, anexos baixados, processo executado e as observações da execução.",
            "en": "At the end of the service execution, you will receive a summary file of information about the sender, downloaded attachments, executed process and execution notes.",
            "es": "Al final de la ejecución del servicio, recibirá un archivo de resumen de información sobre el remitente, archivos adjuntos descargados, proceso ejecutado y notas de ejecución."
        },
        "omie_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da OMIE e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials from the OMIE website and can reuse it whenever you need it.",
            "es": "Con unos pocos clics configuras un registro con tus credenciales desde la web de OMIE y puedes reutilizarla cuando lo necesites."
        },
        "omie_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, o resultado chega por e-mail informando o remetente, os anexos recebidos, o processo executado e suas observações.",
            "en": "After using the service, the result arrives by e-mail informing the sender, the attachments received, the process performed and its observations.",
            "es": "Después de utilizar el servicio, el resultado llega por correo electrónico informando al remitente, los archivos adjuntos recibidos, el proceso realizado y sus observaciones."
        },
        "same_email_used_on_the_omie_website": {
            "pt-BR": "Mesmo email utilizado no site da OMIE.",
            "en": "Same email used on the OMIE website.",
            "es": "Incluso email utilizado en el sitio web de la OMIE."
        },
        "same_password_used_on_omie_website": {
            "pt-BR": "Mesma senha utilizada no site OMIE",
            "en": "Same password used on the OMIE website",
            "es": "Misma contraseña utilizada en el sitio web de OMIE"
        },
        "omie_credentials": {
            "pt-BR": "Credenciais da OMIE",
            "en": "OMIE Credentials",
            "es": "Credenciales OMIE"
        },
        "launching_accounts_payable": {
            "pt-BR": "Lançamento de Contas a Pagar",
            "en": "Launching Accounts Payable",
            "es": "Lanzamiento de Cuentas por Pagar"
        },
        "used_for_roi_calculation": {
            "pt-BR": "Utilizado para os cálculos do ROI",
            "en": "Used for ROI calculation",
            "es": "Utilizado para los cálculos de ROI"
        },
        "create_your_account_on_hub": {
            "pt-BR": "Crie a sua conta no Smarthis Hub",
            "en": "Create your account on Smarthis Hub",
            "es": "Crea tu cuenta en Smarthis Hub"
        },
        "to_enjoy_14_day_trial": {
            "pt-BR": "para aproveitar 14 dias de teste grátis.",
            "en": "to enjoy a 14-day free trial.",
            "es": "para disfrutar de una prueba gratuita de 14 días."
        },
        "execution_error": {
            "pt-BR": "Erro na execução",
            "en": "Execution error",
            "es": "Error de ejecución"
        },

        "delete_scheduling": {
            "pt-BR": "Excluir agendamento",
            "en": "Remove scheduling",
            "es": "Borrar horario"
        },
        "you_will_no_longer_automatically_receive_results_on_scheduled_dates": {
            "pt-BR": "Você não irá mais receber os resultados automaticamente nas datas programadas",
            "en": "You will no longer automatically receive results on scheduled dates",
            "es": "Ya no recibirás automáticamente los resultados en las fechas programadas"
        },
        "question_are_you_sure_you_want_to_exclude_the_appointment_execution_of_the_model": {
            "pt-BR": "Tem certeza que deseja excluir o agendamento de execução do modelo",
            "en": "Are you sure you want to exclude the appointment execution of the model",
            "es": "¿Está seguro de que desea eliminar el programa de ejecución del modelo"
        },
        "unable_to_start_scheduling": {
            "pt-BR": "Não foi possível dar início ao agendamento",
            "en": "Unable to start scheduling",
            "es": "No se puede comenzar el horario"
        },
        "price_research_and_monitoring": {
            "pt-BR": "Pesquisa e monitoramento de preços",
            "en": "Price research and monitoring",
            "es": "Investigación y seguimiento de precios"
        },
        "antecedentes_rj_title_and_subtitle": {
            "pt-BR": "Verificação de Antecedentes Criminais | RJ",
            "en": "Criminal History Verification | RJ",
            "es": "Verificación de antecedentes penales | RJ"
        },
        "antecedentes_rj_text_example_input": {
            "pt-BR": "Exemplo: \"RJ - DADOS DO RG \"",
            "en": "Example: \"RJ - RG DATA \"",
            "es": "Ejemplo: \"RJ - DATOS RG \""
        },
        "antecedentes_rj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os dados do RG que deseja verificar os antecedentes criminais no RJ. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the RG data from who you wish to verify the criminal history in RJ. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los datos RG que deseen verificar su antecedentes penales RJ. Luego configure un modelo utilizando el archivo completo."
        },
        "antecedentes_rj_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download dos antecedentes criminais no Rio de Janeiro de diferentes RGs simultaneamente.",
            "en": "This service issues and downloads the criminal history in the Rio de Janeiro of different RGs simultaneously.",
            "es": "Este servicio emite y descarga el antecedentes penales en Rio de Janeiro de diferentes RGs simultáneamente."
        },
        "delete_process_confirmation_1": {
            "pt-BR": "Todos os Sub-processos relacionados com este Processo serão movidos para aba de “Não cadastrados” e as informações fornecidas serão perdidas.",
            "en": 'All Sub-Processes related to this Process will be moved to the “Unregistered” tab and the information provided will be lost.',
            "es": 'Todos los Subprocesos relacionados con este Proceso se moverán a la pestaña "No registrados" y la información proporcionada se perderá.'
        },
        "delete_process_confirmation_2": {
            "pt-BR": "Tem certeza que deseja excluir este processo?",
            "en": 'Are you sure you want to delete this process?',
            "es": 'Todos los Subprocesos relacionados con este Proceso se moverán a la pestaña "¿Está seguro de que desea eliminar este proceso?'
        },

        "cnd_bocaina_title_and_subtitle": {
            "pt-BR": "Emissão de CND | Bocaina",
            "en": "CND Issuance | Bocaina",
            "es": "Emisión de CND | Bocaina"
        },
        "cnd_bocaina_example_input": {
            "pt-BR": "Exemplo: \"CND - BOCAINA\"",
            "en": "Example: \"CND - BOCAINA\"",
            "es": "Ejemplo: \"CND - BOCAINA\""
        },
        "cnd_ce_revenue_title_and_subtitle": {
            "pt-BR": "Emissão de CND | CE",
            "en": "CND issuance | CE",
            "es": "Emisión de CND | CE"
        },
        "cnd_ce_revenue_example_input": {
            "pt-BR": "Exemplo: \"CND - Ceará\"",
            "en": "Example: \"CND -  Ceará\"",
            "es": "Ejemplo: \"CND - Ceará\""
        },
        "iss_ipojuca_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha no site da Prefeitura do Ipojuca. Para fornecer as outras informações necessárias pra emissão das guias de ISS, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Configure a template informing your login credentials and password on the Ipojuca City Hall website. To provide the other information necessary for the issuance of ISS guides, download and fill in the Standard File provided below and use the filled file in the model configuration.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña en el sitio web del Ayuntamiento de Ipojuca. Para proporcionar la otra información necesaria para la emisión de guías ISS, descargue y complete el archivo estándar que se proporciona a continuación y use el archivo completo en la configuración del modelo."
        },
        "iss_ipojuca_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download de diferentes guias de ISS na Prefeitura do Ipojuca simultaneamente.",
            "en": "This service issues and downloads different ISS guides at the Ipojuca City Hall simultaneously.",
            "es": "Este servicio emite y descarga simultáneamente diferentes guías ISS en la Municipalidad de Ipojuca."
        },
        "cnd_fortaleza_revenue_title_and_subtitle": {
            "pt-BR": "Emissão de CND | Fortaleza",
            "en": "CND issuance | Fortaleza",
            "es": "Emisión de CND | Fortaleza"
        },
        "cnd_fortaleza_revenue_example_input": {
            "pt-BR": "Exemplo: \"CND - Fortaleza\"",
            "en": "Example: \"CND -  Fortaleza\"",
            "es": "Ejemplo: \"CND - Fortaleza\""
        },
        "clean_all": {
            "pt-BR": "Limpar todos",
            "en": "Clean all",
            "es": "Limpiar todo"
        },
        "marketing": {
            "pt-BR": "Marketing",
            "en": "Marketing",
            "es": "Marketing"
        },
        "fill_in_your_position": {
            "pt-BR": "Insira o cargo",
            "en": "Fill in your position",
            "es": "Introduce tu posición"
        },
        "sector_of_activity": {
            "pt-BR": "Setor de atuação",
            "en": "Sector of activity",
            "es": "Sector de actividad"
        },
        "select_sector_of_activity": {
            "pt-BR": "Selecione Setor de atuação",
            "en": "Select the sector of activity",
            "es": "Seleccione el sector de actividad"
        },
        "fill_in_the_sector_of_activity": {
            "pt-BR": "Insira o Setor de atuação",
            "en": "Fill in the sector of activity",
            "es": "Llenar el sector de actividad"
        },
        "You_must_agree_before_submitting": {
            "pt-BR": "Você deve concordar antes de enviar.",
            "en": "You must agree before submitting.",
            "es": "Debe aceptar antes de enviar."
        },
        "email_requirements": {
            "pt-BR": "Por favor, insira um email válido.",
            "en": "Please enter a valid email.",
            "es": "Por favor, introduzca un correo electrónico válido."
        },
        "name_requirements": {
            "pt-BR": "Por favor, insira um nome e sobrenome.",
            "en": "Please enter a first and last name.",
            "es": "Por favor ingrese un nombre y apellido."
        },
        "almost_ready": {
            "pt-BR": "Quase pronto",
            "en": "Almost ready",
            "es": "Casi listo"
        },
        "for_a_more_personalized_experience": {
            "pt-BR": "Para uma experiência mais personalizada, continue respondendo.",
            "en": "For a more personalized experience, continue filling the form",
            "es": "Para una experiencia más personalizada, sigue respondiendo"
        },
        "please_wait_finalizing_registration": {
            "pt-BR": "Um momento, estamos  finalizando seu cadastro e preparando os próximos passos... ",
            "en": "Please wait, we are finalizing your registration and preparing the next steps...",
            "es": "Espera un minuto, estamos finalizando tu registro y preparando los próximos pasos..."
        },
        "great_choices_wait_while_we_prepare": {
            "pt-BR": "Ótimas escolhas! Aguarde enquanto preparamos os serviços para você.",
            "en": "Great choices! Please wait while we prepare the services for you.",
            "es": "¡Grandes elecciones! Espere mientras preparamos los servicios para usted."
        },
        "with_them_you_will": {
            "pt-BR": "Com eles, você:",
            "en": "With them you:",
            "es": "Con ellos tú:"
        },
        "name_surname": {
            "pt-BR": "Nome e sobrenome",
            "en": "Name and surname",
            "es": "Nombre y apellido"
        },
        "already_have_regsitration": {
            "pt-BR": "Já possuo cadastro",
            "en": "I already have registration",
            "es": "Ya tengo registro"
        },
        "energisa_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | Energisa",
            "en": "Issuance of Energy Bills | Energisa",
            "es": "Emisión de Facturas de Energía | Energisa"
        },
        "energisa_text_example_input": {
            "pt-BR": "Exemplo: \"Energisa\"",
            "en": "Example: \"Energisa\"",
            "es": "Ejemplo: \"Energisa\""
        },
        "same_login_used_on_energisa_website": {
            "pt-BR": "Mesmo login utilizado no site da Energisa",
            "en": "Same login used on Energisa website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Energisa"
        },
        "same_password_used_on_energisa_website": {
            "pt-BR": "Mesma senha utilizada no site da Energisa",
            "en": "Same password used on the Energisa website",
            "es": "Misma contraseña utilizada en el sitio web de Energisa"
        },
        "energisa_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Energisa.",
            "en": "Configure a template by entering your Energisa login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales de inicio de sesión y contraseña de Energisa."
        },
        "energisa_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da Energisa informada.",
            "en": "This service issues and downloads energy bills related to the informed Energisa credential.",
            "es": "Este servicio emite y descarga las facturas de energía relacionadas con la credencial informada de Energisa."
        },
        "energisa_credentials": {
            "pt-BR": "Credenciais da Energisa",
            "en": "Energisa Credentials",
            "es": "Credenciales Energisa"
        },
        "energisa_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da Energisa e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials from the Energisa website and can reuse it whenever you need it.",
            "es": "Con unos pocos clics configuras un registro con tus credenciales desde la web de Energisa y puedes reutilizarla cuando lo necesites."
        },
        "elektro_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | Elektro",
            "en": "Issuance of Energy Bills | Elektro",
            "es": "Emisión de Facturas de Energía | Elektro"
        },
        "elektro_text_example_input": {
            "pt-BR": "Exemplo: \"Luz - Elektro\"",
            "en": "Example: \"Luz - Elektro\"",
            "es": "Ejemplo: \"Luz - Elektro\""
        },
        "same_login_used_on_elektro_website": {
            "pt-BR": "Mesmo login utilizado no site da Elektro",
            "en": "Same login used on Elektro website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Elektro"
        },
        "same_password_used_on_elektro_website": {
            "pt-BR": "Mesma senha utilizada no site da Elektro",
            "en": "Same password used on the Elektro website",
            "es": "Misma contraseña utilizada en el sitio web de Elektro"
        },
        "elektro_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Elektro.",
            "en": "Configure a template by entering your Elektro login credentials and password.",
            "es": "Configure una registro ingresando sus credenciales de inicio de sesión y contraseña de Elektro."
        },
        "elektro_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da Elektro informada.",
            "en": "This service issues and downloads energy bills related to the informed Elektro credential.",
            "es": "Este servicio emite y descarga las facturas de energía relacionadas con la credencial informada de Elektro."
        },
        "elektro_credentials": {
            "pt-BR": "Credenciais da Elektro",
            "en": "Elektro Credentials",
            "es": "Credenciales Elektro"
        },
        "elektro_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da Elektro e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials from the Elektro website and can reuse it whenever you need it.",
            "es": "Con unos pocos clics configuras un registro con tus credenciales desde la web de Elektro y puedes reutilizarla cuando lo necesites."
        },
        "elektro_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail, com as contas e informações sobre valor, período de referência, código identificador.",
            "en": "After using the service, the results arrive by e-mail, with the bills and information about value, reference period, identifier code.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico, con las cuentas e información sobre valor, período de referencia, código identificador."
        },
        "confirm_email": {
            "pt-BR": "Confirmar e-mail",
            "en": "Confirm email",
            "es": "Confirmar correo electrónico"
        },
        "qty_of_monthly_tasks": {
            "pt-BR": "Qtd. de tarefas mensais",
            "en": "Qty of monthly tasks",
            "es": "Cantidad de tareas mensuales"
        },
        "zero_monthly_tasks": {
            "pt-BR": "0 tarefas mensais",
            "en": "0 monthly tasks",
            "es": "0 tareas mensuales"
        },
        "average_hourly_value": {
            "pt-BR": "Valor médio da hora",
            "en": "Average hourly value",
            "es": "Valor medio por hora"
        },
        "average_salary_meployees_divided_by_hours": {
            "pt-BR": "Média do salário dos colaboradores envolvidos dividida pelo número de horas mensais.",
            "en": "Average salary of the employees involved divided by the number of hours per month.",
            "es": "Salario promedio de los empleados involucrados dividido por el número de horas por mes."
        },
        "important_average_salary_meployees_divided_by_hours_with_html": {
            "pt-BR": "<strong>Importante</strong>: o valor será automaticamente multiplicado por 1,5 para aproximar ao custo real.",
            "en": "<strong>Important</strong>: the value will be automatically multiplied by 1.5 to approximate the actual cost.",
            "es": "<strong>Importante</strong>: el valor se multiplicará automáticamente por 1,5 para aproximar el costo real."
        },
        "larger": {
            "pt-BR": "Maior",
            "en": "Larger",
            "es": "Mayor"
        },
        "smallest": {
            "pt-BR": "Menor",
            "en": "Smallest",
            "es": "Menor"
        },
        "roi_history": {
            "pt-BR": "Histórico de ROI",
            "en": "ROI history",
            "es": "Historial de ROI"
        },
        "history_and_evolution_roi": {
            "pt-BR": "Acompanhe o histórico e a evolução do ROI geral do seu Dashboard. Também é possível escolher diferentes períodos de tempo, ou selecionar apenas um processo para realizar diferentes análises.",
            "en": "Track the history and evolution of your Dashboard's overall ROI. It is also possible to choose different time periods, or select just one process to perform different analyses.",
            "es": "Realice un seguimiento del historial y la evolución del ROI general de su panel. También es posible elegir diferentes periodos de tiempo, o seleccionar un solo proceso para realizar diferentes análisis."
        },
        "horizontal_lines_roi": {
            "pt-BR": "As linhas horizontais representam o crescimento dos valores dos processos manual e automatizado ao longo do tempo.",
            "en": "The horizontal lines represent the growth of manual and automated process values ​​over time.",
            "es": "Las líneas horizontales representan el crecimiento de los valores de los procesos manuales y automatizados a lo largo del tiempo."
        },
        "vertical_lines_roi": {
            "pt-BR": "As linhas verticais indicam o momento atual do seu ROI, assim como o momento em que as linhas horizontais irão se encontar. Quando isso acontecer, o valor do processo manual será equivalente ao que foi investido na automatização do processo. ",
            "en": "The vertical lines indicate the current moment of your ROI, as well as when the horizontal lines will meet. When that happens, the value of the manual process will be equivalent to what was invested in automating the process.",
            "es": "Las líneas verticales indican el momento actual de su ROI, así como también cuándo se encontrarán las líneas horizontales. Cuando eso suceda, el valor del proceso manual será equivalente a lo que se invirtió en la automatización del proceso."
        },
        "from_this_moment_roi": {
            "pt-BR": "A partir deste momento, o seu ROI será positivo, ou seja, você estará obtendo lucro com a implementação do processo automatizado.",
            "en": "From this moment on, your ROI will be positive, that is, you will be making a profit with the implementation of the automated process.",
            "es": "A partir de este momento, tu ROI será positivo, es decir, estarás obteniendo beneficios con la implementación del proceso automatizado."
        },
        "important_roi": {
            "pt-BR": "Importante: possuir o ROI negativo durante os primeiros meses da implementação é esperado de praticamente todos investimentos. A velocidade com que o ROI se torna positivo depende da complexidade dos diferentes processos, assim como variações na sua demanda.",
            "en": "Important: Having a negative ROI during the first few months of implementation is expected from virtually all investments. The speed at which ROI becomes positive depends on the complexity of the different processes, as well as variations in their demand.",
            "es": "Importante: Se espera tener un ROI negativo durante los primeros meses de implementación de prácticamente todas las inversiones. La velocidad a la que el ROI se vuelve positivo depende de la complejidad de los diferentes procesos, así como de las variaciones en su demanda."
        },
        "roi_breakdown": {
            "pt-BR": "O Retorno por investimento (ROI) é obtido pelo valor do processo manual subtraído do investimento no processo automatizado, dividido pelo investimento no processo automatizado. Ou seja: ",
            "en": "Return on Investment (ROI) is the value of the manual process minus the investment in the automated process, divided by the investment in the automated process. Ie:",
            "es": "El retorno de la inversión (ROI) es el valor del proceso manual menos la inversión en el proceso automatizado, dividido por la inversión en el proceso automatizado. O sea:"
        },
        "roi_formula_top": {
            "pt-BR": "Montante do Processo manual - Montante  do Investimento",
            "en": "Manual Process Amount - Investment Amount",
            "es": "Importe del proceso manual - Importe de la inversión"
        },
        "roi_formula_bottom": {
            "pt-BR": "Montante  do Investimento",
            "en": "Investment Amount",
            "es": "Importe de la inversión"
        },
        "with_this_formula_roi": {
            "pt-BR": "Com essa fórmula, ao longo do tempo, é possível entender em que momento o processo  automatizado passa a ser mais economico que o processo manual. ",
            "en": "With this formula, over time, it is possible to understand when the automated process becomes more economical than the manual process.",
            "es": "Con esta fórmula, con el tiempo, es posible comprender cuándo el proceso automatizado se vuelve más económico que el proceso manual."
        },
        "start_viewing_roi": {
            "pt-BR": "Para começar a visualizar essas informações é preciso cadastar os dados necessários para o cálculo na página de Configurações > Processos. Quanto mais exatas as informações fornecidas, mais exato será o valor demonstrado.",
            "en": "To start viewing this information, it is necessary to register the data necessary for the calculation on the Settings > Processes page. The more accurate the information provided, the more accurate the displayed value.",
            "es": "Para comenzar a visualizar esta información, es necesario registrar los datos necesarios para el cálculo en la página Configuración > Procesos. Cuanto más precisa sea la información proporcionada, más preciso será el valor mostrado."
        },
        "know_roi": {
            "pt-BR": "Conheça o ROI obtido individualmente por cada processo ou área cadastrada dentro do período filtrado. Entenda também quanto cada processo ou área cadastrada representam do ROI geral do seu Dashboard RPA.",
            "en": "Know the ROI obtained individually by each process or area registered within the filtered period. Also understand how much each process or registered area represents of the overall ROI of your Dashboard RPA.",
            "es": "Conozca el ROI obtenido individualmente por cada proceso o área registrada dentro del periodo filtrado. También comprenda cuánto representa cada proceso o área registrada del ROI general de su Dashboard RPA."
        },
        "roi_summary": {
            "pt-BR": "Nos Resumos, visualize os valores em forma de lista pra contribuir para as suas análises.",
            "en": "In Summaries, view the values ​​as a list to contribute to your analysis.",
            "es": "En Resúmenes, vea los valores como una lista para contribuir a su análisis."
        },
        "graphics": {
            "pt-BR": "Gráficos",
            "en": "Graphics",
            "es": "Gráficos"
        },
        "manual_costs": {
            "pt-BR": "Custos manuais",
            "en": "Manual costs",
            "es": "Costos manuales"
        },
        "automated_costs": {
            "pt-BR": "Custos automatizados",
            "en": "Automated costs",
            "es": "Costos automatizados"
        },
        "correios_cas_title_and_subtitle": {
            "pt-BR": "Emissão de Fatura Eletrônica | Correios",
            "en": "Electronic Invoice Issue | Correios",
            "es": "Emisión de Factura Electrónica | Correo"
        },
        "correios_cas_text_example_input": {
            "pt-BR": "Exemplo: \"Fatura - Correios\"",
            "en": "Example: \"Invoice - Post Office\"",
            "es": "Ejemplo: \"Factura - Oficina de correos\""
        },
        "same_login_used_on_the_correios_website_cas": {
            "pt-BR": "Mesmo login utilizado no site dos Correios - CAS",
            "en": "Same login used on the Correios website - CAS",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Correios - CAS"
        },
        "same_password_used_on_the_correios_website_cas": {
            "pt-BR": "Mesma senha utilizada no site dos Correios - CAS",
            "en": "Same password used on the Correios website - CAS",
            "es": "Misma contraseña utilizada en el sitio web de Correios - CAS"
        },
        "correios_cas_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha dos Correios - CAS.",
            "en": "Configure a template informing your Post Office login credentials and password - CAS",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de la oficina de correos - CAS"
        },
        "correios_cas_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das faturas eletrônicas relacionadas à credencial dos Correios - CAS informada.",
            "en": "This service issues and downloads electronic invoices related to the Correios - CAS credential informed.",
            "es": "Este servicio emite y descarga facturas electrónicas relacionadas con la credencial Correios - CAS informada."
        },
        "postal_credentials_cas": {
            "pt-BR": "Credenciais dos Correios - CAS",
            "en": "Postal Credentials - CAS",
            "es": "Credenciales Postales - CAS"
        },
        "correios_cas_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site dos Correios - CAS e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials from the Correios - CAS website and you can reuse it whenever you need to.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales desde el sitio web de Correios - CAS y puede reutilizarla cuando lo necesite."
        },
        "edp_brasil_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Energia | EDP",
            "en": "Issuance of Energy Bills | EDP",
            "es": "Emisión de Facturas de Energía | EDP"
        },
        "edp_brasil_text_example_input": {
            "pt-BR": "Exemplo: \"Luz - EDP Brasil\"",
            "en": "Example: \"Light - EDP Brasil\"",
            "es": "Ejemplo: \"Luz - EDP Brasil\""
        },
        "same_login_used_on_the_edp_website": {
            "pt-BR": "Mesmo login utilizado no site da EDP",
            "en": "Same login used on the EDP website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de EDP"
        },
        "same_password_used_on_the_edp_website": {
            "pt-BR": "Mesma senha utilizada no site da EDP",
            "en": "Same password used on the EDP website",
            "es": "Misma contraseña utilizada en el sitio web de EDP"
        },
        "edp_brasil_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da EDP.",
            "en": "Configure a template informing your EDP login credentials and password.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña de EDP."
        },
        "edp_brasil_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de energia relacionadas à credencial da EDP informada.",
            "en": "This service issues and downloads energy bills related to the informed EDP credential.",
            "es": "Este servicio emite y descarga las facturas de energía relacionadas con la credencial EDP informada."
        },
        "edp_brasil_credentials": {
            "pt-BR": "Credenciais da EDP",
            "en": "EDP credentials",
            "es": "Credenciales EDP"
        },
        "edp_brasil_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da EDP e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials from the EDP website and can reuse it whenever you need to.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales desde el sitio web de EDP y puede reutilizarla cuando lo necesite."
        },
        "all_states_except_es_and_sp": {
            "pt-BR": "Todos os estados (exceto ES e SP)",
            "en": "All states (except ES and SP)",
            "es": "Todos los estados (excepto ES y SP)"
        },
        'solicitacao_nf_instructions': {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com as informações do fornecedor ou prestador, que você deseja solicitar o envio da NF-e ou NFS-e. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the default file provided below with the supplier or provider information that you want to request the sending of NF-e or NFS-e.Then set up a model using the filled file.",
            "es": "Descargue y rellene el archivo predeterminado que se proporciona a continuación con la información del proveedor o suministrador que desea solicitar el envío de NF-e o NFS-e. Luego configure un modelo utilizando el archivo completo."
        },
        "solicitacao_nf_title_about_the_service": {
            "pt-BR": "Este serviço envia um e-mail solicitando aos fornecedores e prestadores cadastrados o envio das NF-e ou NFS-e pendentes.",
            "en": "This service sends an email asking for registered suppliers and providers to send NF-e or NFS-e pending.",
            "es": "Este servicio envía un correo electrónico solicitando a los proveedores y suministradores registrados que envíen NF-e o NFS-e pendientes."
        },
        "solicitacao_nf_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você recebe um arquivo com resumo dos e-mails que foram contatados.",
            "en": "At the end of the service execution, you receive a file with a summary of the emails that were contacted.",
            "es": "Al final de la ejecución del servicio, usted recibe un archivo con un resumen de los correos electrónicos que fueron contactados."
        },
        "solicitacao_nf_discover_how_it_works_1": {
            "pt-BR": "Você preenche o Arquivo Padrão disponibilizado com as informações dos fornecedores/prestadores que deseja solicitar o envio das NF-e e NFS-e. Em seguida configure um modelo utilizando o arquivo preenchido. Assim, as informações ficam salvas para você reutilizar sempre que precisar.",
            "en": "You fill out the default file provided with the information from the suppliers/providers who want to request the sending of NF-e and NFS-e.Then set up a model using the filled file.Thus, the information is saved for you to reuse whenever you need it.",
            "es": "Usted rellena el fichero por defecto que se le proporciona con la información de los proveedores que quieren solicitar el envío de NF-e y NFS-e.A continuación, configura un modelo utilizando el fichero rellenado.Así, la información queda guardada para que pueda reutilizarla siempre que la necesite."
        },
        "solicitacao_nf_title_and_subtitle": {
            "pt-BR": "Solicitação de Envio de Notas Ficais | Fornecedores e Prestadores",
            "en": "Request for Invoice Submission | Suppliers and Providers",
            "es": "Solicitud de presentación de facturas | Proveedores y suministradores"
        },
        "solicitacao_nf_text_example_input": {
            "pt-BR": "Exemplo: \"Solicitação de Envio de Notas Ficais - Fornecedores e Prestadores\"",
            "en": "Example: \"Request for Invoice Submission - Suppliers and Providers\"",
            "es": "Ejemplo: \"Solicitud de presentación de facturas - Proveedores y suministradores\""
        },
        "request_for_invoice_submission": {
            "pt-BR": "Solicitação de Envio de Notas Ficais",
            "en": "Request for Invoice Submission",
            "es": "Solicitud de presentación de facturas"
        },
        "onboarding_welcome_text_one": {
            "pt-BR": "Para te dar boas-vindas ao Smarthis Hub, preparamos um passo a passo para te ajudar a conhecer todas as vantagens e aproveitar 100% do seu período de testes.",
            "en": "To welcome you to Smarthis Hub, we have prepared a step-by-step guide to help you discover all the advantages and enjoy 100% of your trial period.",
            "es": "Para darte la bienvenida a Smarthis Hub, hemos preparado una guía paso a paso para ayudarte a descubrir todas las ventajas y disfrutar al 100% de tu periodo de prueba."
        },
        "onboarding_welcome_text_two": {
            "pt-BR": "E tem mais! A cada passo completo, você ganha pontos.",
            "en": "And there's more! With each complete step, you earn points.",
            "es": "¡Y hay más! Con cada paso completo, ganas puntos."
        },
        "onboarding_welcome_text_two_bold": {
            "pt-BR": " Quando alcançar 100 pontos, vamos te presentear com 6 dias extras no seu período de teste grátis!",
            "en": "When you reach 100 points, we'll gift you an extra 6 days in your free trial period!",
            "es": "¡Cuando alcance los 100 puntos, le regalaremos 6 días adicionales en su período de prueba gratuito!"
        },
        "step_by_step": {
            "pt-BR": "Passo a passo",
            "en": "Step by step",
            "es": "Paso a paso"
        },
        "use_a_service": {
            "pt-BR": "Utilize um Serviço",
            "en": "Use a Service",
            "es": "usar un servicio"
        },
        "choose_a_new_service": {
            "pt-BR": "Escolha um novo serviço",
            "en": "Choose a new service",
            "es": "Elige un nuevo servicio"
        },
        "confirm_your_email": {
            "pt-BR": "Confirme seu e-mail",
            "en": "Confirm your email",
            "es": "confirme su email"
        },
        "points": {
            "pt-BR": "pontos",
            "en": "points",
            "es": "puntos"
        },
        "text_one_use_a_service": {
            "pt-BR": "Vá até \"Meus Serviços\" e escolha um para começar. Siga as instruções que estão do lado direito da página do serviço para configurar um modelo com os dados necessários.",
            "en": "Go to \"My Services\" and choose one to get started. Follow the instructions on the right side of the service page to configure a template with the necessary data.",
            "es": "Vaya a \"Mis servicios\" y elija uno para comenzar. Siga las instrucciones en el lado derecho de la página del servicio para configurar un registro con los datos necesarios."
        },
        "text_two_use_a_service": {
            "pt-BR": "Agora é só dar play e aguardar enquanto o Hub utiliza os dados fornecidos para trazer seus resultados até você!",
            "en": "Now just play and wait while the Hub uses the data provided to bring your results to you!",
            "es": "¡Ahora solo juegue y espere mientras Hub usa los datos proporcionados para traerle sus resultados!"
        },
        "text_three_use_a_service": {
            "pt-BR": "Caso seja uma demanda recorrente, você também pode agendar a execução para receber os resultados automaticamente na data que decidir.",
            "en": "If it is a recurring demand, you can also schedule the execution to receive the results automatically on the date you decide.",
            "es": "Si es una demanda recurrente, también puedes programar la ejecución para recibir los resultados automáticamente en la fecha que decidas."
        },
        "text_one_choose_a_new_service": {
            "pt-BR": "Fique por dentro de todo os serviços e novidades do Smarthis Hub visitando a página  \"Descobrir\".",
            "en": "Stay on top of all Smarthis Hub services and news by visiting the \"Discover\" page.",
            "es": "Manténgase al tanto de todos los servicios y noticias de Smarthis Hub visitando la página \"Descubrir\"."
        },
        "text_two_choose_a_new_service": {
            "pt-BR": "Quando encontrar um serviço que tem interesse, clique em \"Adicionar ao meu plano\" e ele será automaticamente adicionado a sua conta. Simples assim!",
            "en": "When you find a service that interests you, click on \"Add to my plan\" and it will automatically be added to your account. That simple!",
            "es": "Cuando encuentre un servicio que le interese, haga clic en \"Agregar a mi plan\" y automáticamente se agregará a su cuenta. ¡Simples así!"
        },
        "text_one_invite_your_team": {
            "pt-BR": "A sua equipe também pode aproveitar as vantagens do Smarthis Hub com você!",
            "en": "Your team can also take advantage of Smarthis Hub with you!",
            "es": "¡Tu equipo también puede aprovechar Smarthis Hub contigo!"
        },
        "text_two_invite_your_team": {
            "pt-BR": "Clique abaixo para ir até a aba de \"Gerenciar Licenças\" e convide os seus colaboradores diretamente no serviço que eles gostariam de utilizar.",
            "en": "Click below to go to the \"Manage Licenses\" tab and invite your employees directly to the service they would like to use.",
            "es": "Haga clic a continuación para ir a la pestaña \"Administrar licencias\" e invite a sus empleados directamente al servicio que les gustaría usar."
        },
        "text_one_confirm_your_email": {
            "pt-BR": "Confira sua caixa de entrada e clique na mensagem de boas vindas do Hub para confirmar seu e-mail para começar a aproveitar todas as vantagens dos serviços!",
            "en": "Check your inbox and click on the Hub welcome message to confirm your email to start taking full advantage of the services!",
            "es": "¡Revise su bandeja de entrada y haga clic en el mensaje de bienvenida de Hub para confirmar su correo electrónico y comenzar a aprovechar al máximo los servicios!"
        },
        "go_to_manage_licenses": {
            "pt-BR": "Ir até Gerenciar Licenças",
            "en": "Go to Manage Licenses",
            "es": "Vaya a Administrar licencias"
        },
        "go_to_discover": {
            "pt-BR": "Ir até Descobrir",
            "en": "Go to Discover",
            "es": "Ir a Descubrir"
        },
        "go_to_my_services": {
            "pt-BR": "Ir até Meus Serviços",
            "en": "Go to My Services",
            "es": "Ir a Mis Servicios"
        },
        "current_roi": {
            "pt-BR": "ROI Atual",
            "en": "Current ROI",
            "es": "ROI Actual"
        },
        "start_of_positive_roi": {
            "pt-BR": "Inicio de ROI Positivo",
            "en": "Start of Positive ROI",
            "es": "Comienzo del ROI positivo"
        },
        "tj_sp_title_and_subtitle": {
            "pt-BR": "Consulta de Processos TJSP",
            "en": "Process Monitoring TJSP",
            "es": "Seguimiento de Procesos TJSP"
        },
        "tj_sp_text_example_input": {
            "pt-BR": "Exemplo: \"TJ-SP - Monitoramento \"",
            "en": "Example: \"TJ-SP - Monitoring \"",
            "es": "Ejemplo: \"TJ-SP - Monitoreamento \""
        },
        "tj_sp_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com os dados solicitados para monitorar os processos de 1º e 2º grau do Tribunal de Justiça em São Paulo. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the requested data to monitor the 1st and 2nd degree processes of the Court of Justice in São Paulo. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con los datos solicitados para monitorear los procesos de 1° y 2° grado de la Corte de Justicia en São Paulo. Luego configure un modelo utilizando el archivo completo."
        },
        "tj_sp_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz consultas no Tribunal de Justiça de São Paulo com diferentes processos simultaneamente.",
            "en": "This service issues and consults at the São Paulo Court of Justice with different processes simultaneously.",
            "es": "Este servicio emite y consulta en el Tribunal de Justicia de São Paulo con diferentes procesos simultáneamente."
        },
        "tj_sp_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber um resumo das movimentações dos processos envolvidos.",
            "en": "At the end of the service execution, you will receive a summary of the movements of the processes involved.",
            "es": "Al finalizar la ejecución del servicio, recibirá un resumen de los movimientos de los procesos involucrados."
        },
        "tj_sp_discover_how_it_works_1": {
            "pt-BR": "Você preenche o arquivo de upload com os dados solicitados e configura um modelo que fica salvo para reutilizar sempre que precisar.",
            "en": "You fill in the upload file with the requested data and set up a template that is saved to reuse whenever you need it.",
            "es": "Usted llena el archivo de carga con los datos solicitados y configura un registro que se guarda para reutilizarla cuando la necesite."
        },
        "tj_sp_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as movimentações mais recentes dos processos.",
            "en": "After using the service, the results arrive by email with the most recent movements of the processes.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con los movimientos más recientes de los procesos."
        },
        "process_consultation_tj": {
            "pt-BR": "Consulta de Processos TJ",
            "en": "Process Consultation TJ",
            "es": "Consulta de Proceso TJ"
        },
        "you_have_completed_all_the_steps": {
            "pt-BR": "Você completou todos os passos!",
            "en": "You have completed all the steps!",
            "es": "¡Has completado todos los pasos!"
        },
        "text_completed_onboarding": {
            "pt-BR": "Você completou todos os passos e garantiu 6 dias extras para sua equipe continuar conhecendo o Smarthis Hub!",
            "en": "You have completed all the steps and guaranteed 6 extra days for your team to continue getting to know the Smarthis Hub!",
            "es": "¡Has completado todos los pasos y tienes garantizados 6 días extra para que tu equipo siga conociendo Smarthis Hub!"
        },
        "text_two_full_onboarding": {
            "pt-BR": "Agora você já conhece os principais caminhos para aproveitar todas as vantagens oferecidas! Configure novos modelos nos seus serviços para receber os resultados com apenas um clique, agende as execuções e continue descobrindo novos serviços.",
            "en": "Now you know the main ways to take advantage of all the advantages offered! Set up new templates in your services to get results with just one click, schedule runs and keep discovering new services.",
            "es": "¡Ya conoces las principales formas de aprovechar todas las ventajas que ofrece! Configure nuevas plantillas en sus servicios para obtener resultados con un solo clic, programe ejecuciones y siga descubriendo nuevos servicios."
        },
        "text_three_full_onboarding": {
            "pt-BR": "Caso ainda tenha alguma dúvida, encontre mais respostas acessando a nossa ",
            "en": "If you still have any questions, find more answers by visiting our ",
            "es": "Si todavía tiene alguna pregunta, encuentre más respuestas visitando nuestro "
        },
        "tj_rj_title_and_subtitle": {
            "pt-BR": "Consulta de Processos TJ | Rio de Janeiro",
            "en": "Process Consultation TJ | Rio de Janeiro",
            "es": "Consulta de Proceso TJ | Rio de Janeiro"
        },
        "tj_rj_text_example_input": {
            "pt-BR": "Exemplo: \"TJ - RJ - Monitoramento \"",
            "en": "Example: \"TJ - RJ - Monitoring \"",
            "es": "Ejemplo: \"TJ - RJ - Monitoreamento \""
        },
        "tj_rj_instructions": {
            "pt-BR": "Faça download e preencha o arquivo disponibilizado, com os dados solicitados para monitorar os processos no Tribunal de Justiça do Rio de Janeiro. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the available file, with the data requested to monitor the processes at the Court of Justice of Rio de Janeiro. Then configure a model using the filled file.",
            "es": "Descargue y complete el archivo disponible, con los datos solicitados para el seguimiento de los procesos en el Tribunal de Justicia de Río de Janeiro. Luego configure un modelo utilizando el archivo completo."
        },
        "tj_rj_title_about_the_service": {
            "pt-BR": "Este serviço faz diferentes tipos de consultas no Tribunal de Justiça do Rio de Janeiro simultaneamente.",
            "en": "This service makes different types of consultations at the Court of Justice of Rio de Janeiro simultaneously.",
            "es": "Este servicio realiza simultáneamente diferentes tipos de consultas en el Tribunal de Justicia de Río de Janeiro."
        },
        "tj_rj_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os dados de movimentações dos processos.",
            "en": "At the end of the service execution, you will receive process movement data.",
            "es": "Al final de la ejecución del servicio, recibirá datos de movimiento del proceso."
        },
        "icms_alagoas_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | AL",
            "en": "Issuance of ICMS Guide | AL",
            "es": "Emisión de Guía ICMS | AL"
        },
        "icms_alagoas_example_input": {
            "pt-BR": "Exemplo: \"ICMS - AL\"",
            "en": "Example: \"ICMS - AL\"",
            "es": "Ejemplo: \"ICMS - AL\""
        },
        "hours_returned_by_process": {
            "pt-BR": "Horas Retornadas por processo",
            "en": "Hours Returned by Process",
            "es": "Horas devueltas por proceso"
        },
        "hours_returned_by_area": {
            "pt-BR": "Horas Retornadas por Área",
            "en": "Hours Returned by Area",
            "es": "Horas Devueltas por Área"
        },
        "returned_hours_history": {
            "pt-BR": "Histórico de Horas Retornadas",
            "en": "Returned Hours History",
            "es": "Historial de horas devueltas"
        },
        "returned_hours": {
            "pt-BR": "Horas Retornadas",
            "en": "Returned Hours",
            "es": "Horas devueltas"
        },
        "the_number_of_hours_returned_is_obtained_by_the": {
            "pt-BR": "A quantidade das horas retornadas é obtida pelo",
            "en": "The number of hours returned is obtained by the",
            "es": "El número de horas devueltas se obtiene mediante el"
        },
        "how_returned_hours_works": {
            "pt-BR": "tempo médio da tarefa manual multiplicado pela quantidade média de tarefas mensais. O valor obtido é múltiplicado pela taxa se sucesso do processo automatizado.",
            "en": "average manual task time multiplied by the average number of monthly tasks. The value obtained is multiplied by the success rate of the automated process.",
            "es": "tiempo medio de tareas manuales multiplicado por el número medio de tareas mensuales. El valor obtenido se multiplica por la tasa de éxito del proceso automatizado."
        },
        "in_other_words_returned_hours": {
            "pt-BR": "Ou seja",
            "en": "In other words",
            "es": "O sea"
        },
        "formula_hours_returned": {
            "pt-BR": "Min. por Tarefa Manual * Qtd. Média de Tarefas * Taxa de Sucesso do Processo Automatizado",
            "en": "min. per Manual Task * Qty. Average Tasks * Automated Process Success Rate",
            "es": "mín. por tarea manual * Cant. Tareas promedio * Tasa de éxito del proceso automatizado"
        },
        "formula_it_is_possible_to_understand_hours_returned": {
            "pt-BR": "Com essa fórmula é possível entender quanto tempo foi retornado para os seus colaboradores que não precisam mais se dedicar a execução manual desta tarefa.",
            "en": "With this formula it is possible to understand how much time was returned to your employees who no longer need to dedicate themselves to the manual execution of this task.",
            "es": "Con esta fórmula es posible comprender cuánto tiempo se devolvió a sus empleados que ya no necesitan dedicarse a la ejecución manual de esta tarea."
        },
        "to_start_viewing_this_information_hours_returned": {
            "pt-BR": "Para começar a visualizar essas informações é preciso cadastrar os dados necessários para o cálculo na página de",
            "en": "To start viewing this information, it is necessary to register the data necessary for the calculation on the",
            "es": "Para comenzar a visualizar esta información, es necesario registrar los datos necesarios para el cálculo en la"
        },
        "the_more_accurate_the_information_provided": {
            "pt-BR": "Quanto mais exatas as informações fornecidas, mais exato será o valor demonstrado.",
            "en": "The more accurate the information provided, the more accurate the displayed value.",
            "es": "Cuanto más precisa sea la información proporcionada, más preciso será el valor mostrado."
        },
        "view_the_number_of_hours_returned_individually": {
            "pt-BR": "Visualize a quantidade de horas retornadas individualmente pelos seus processos RPA e áreas cadastradas. Acompanhe os Resumos para entender qual a porcentagem do total de horas retornadas que aquele processo representa.",
            "en": "View the number of hours returned individually by your RPA processes and registered areas. Follow the Summaries to understand what percentage of the total hours returned that process represents.",
            "es": "Visualiza el número de horas devueltas individualmente por tus procesos RPA y áreas registradas. Siga los resúmenes para comprender qué porcentaje del total de horas devueltas representa ese proceso."
        },
        "also_have_access_to_the_history_of_the_hours_returned": {
            "pt-BR": "Tenha também acesso ao histórico das horas retornadas por dia ou por mês desde a implementação do seu Dashboard.",
            "en": "Also have access to the history of the hours returned per day or per month since the implementation of your Dashboard.",
            "es": "También ten acceso al historial de las horas devueltas por día o por mes desde la implementación de tu Dashboard."
        },
        "having_fewer_hours_returned": {
            "pt-BR": "Ter menos horas retornadas não significa que seu processo esteja com um desempenho ruim. Isso pode significar que sua demanda é menor ou que ele é menos complexo que outros processos. O mesmo vale para a situação inversa.",
            "en": "Having fewer hours returned doesn't mean your process is performing poorly. This may mean that its demand is lower or that it is less complex than other processes. The same goes for the reverse situation.",
            "es": "tener menos horas devueltas no significa que su proceso esté funcionando mal. Esto puede significar que su demanda es menor o que es menos complejo que otros procesos. Lo mismo ocurre con la situación inversa."
        },
        "important": {
            "pt-BR": "Importante",
            "en": "Important",
            "es": "Importante"
        },
        "occupation_and_executions": {
            "pt-BR": "Ocupação e Execuções",
            "en": "Occupation and Executions",
            "es": "Ocupación y ejecuciones"
        },
        "robots": {
            "pt-BR": "Robôs",
            "en": "Robots",
            "es": "robots"
        },
        "icms_pr_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | PR",
            "en": "Issuance of ICMS Guide | PR",
            "es": "Emisión de Guía ICMS | PR"
        },
        "icms_pr_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com CAD/ICMS, entre outras informações, das guias de ICMS que deseja emitir. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with CAD/ICMS, among other information, of the ICMS guides you wish to issue. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con CAD/ICMS, entre otra información, de las guías ICMS que desea emitir. Luego configure un modelo utilizando el archivo completo."
        },
        "icms_pr_example_input": {
            "pt-BR": "Exemplo: \"ICMS - PR\"",
            "en": "Example: \"ICMS - PR\"",
            "es": "Ejemplo: \"ICMS - PR\""
        },
        "nfse_londrina_title_and_subtitle": {
            "pt-BR": "Emissão de Notas Fiscais de Serviço (NFS-e) | Londrina",
            "en": "Issue of Service Invoices (NFS-e) | Londrina",
            "es": "Emisión de Facturas de Servicios (NFS-e) | Londrina"
        },
        "nfse_londrina_example_input": {
            "pt-BR": "Exemplo: \"Londrina - PR\"",
            "en": "Example: \"London - PR\"",
            "es": "Ejemplo: \"Londres - PR\""
        },
        "same_login_used_on_the_city_hall_of_londrina_pr_website": {
            "pt-BR": "Mesmo login utilizado no site Prefeitura de Londrina/PR.",
            "en": "Same login used on the City Hall of Londrina/PR website.",
            "es": "Mismo inicio de sesión utilizado en el sitio web de la Alcaldía de Londrina/PR."
        },
        "same_password_used_on_the_website_of_the_city_hall_of_londrina_pr": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Londrina/PR.",
            "en": "Same password used on the website of the City Hall of Londrina/PR.",
            "es": "Misma contraseña utilizada en el sitio web de la Alcaldía de Londrina/PR."
        },
        "nfse_londrina_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de Londrina/PR. Para fornecer as outras informações necessárias pra emissão das notas Fiscais de Serviço, faça download e preencha o Arquivo Padrão disponibilizado abaixo e utilize o arquivo preenchido na configuração do modelo.",
            "en": "Set up a template informing your login credentials and password for the City Hall of Londrina/PR. To provide the other information necessary for the issuance of Service Invoices, download and fill in the Standard File available below and use the filled file in the template configuration.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Londrina/PR. Para proporcionar la otra información necesaria para la emisión de Facturas de Servicios, descargue y complete el Archivo Estándar disponible a continuación y utilice el archivo completo en la configuración de la registro."
        },
        "nfse_londrina_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Notas Fiscais de Serviços Eletrônica – NFS-e relacionadas à credencial da Prefeitura de Londrina/PR informada.",
            "en": "This service issues and downloads the Electronic Service Invoices – NFS-e related to the informed Londrina/PR City Hall credential.",
            "es": "Este servicio emite y descarga las Facturas Electrónicas de Servicios – NFS-e relacionadas con la credencial informada del Ayuntamiento de Londrina/PR."
        },
        "londrina_pr_credentials": {
            "pt-BR": "Credenciais Londrina/PR",
            "en": "Londrina/PR Credentials",
            "es": "Credenciales de Londrina/PR"
        },
        "nfse_londrina_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais da Prefeitura de Londrina/PR para buscar por todas as NFS-e emitidas em um período ou por notas específicas preenchendo um arquivo de entrada com as informações necessárias.",
            "en": "With a few clicks, you configure a template with your credentials from the City Hall of Londrina/PR to search for all NFS-e issued in a period or for specific notes by filling in an input file with the necessary information.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales de la Alcaldía de Londrina/PR para buscar todos los NFS-e emitidos en un período o para notas específicas llenando un archivo de entrada con la información necesaria."
        },
        "rpa_modal_1": {
            "pt-BR": "Visualize a quantidade de horas executadas individualmente pelos seus processos RPA e áreas cadastradas. Acompanhe os Resumos para entender qual a porcentagem do total de horas executadas que aquele processo representa.",
            "en": "View the number of hours performed individually by your RPA processes and registered areas. Follow the Summaries to understand what percentage of the total hours executed that process represents.",
            "es": "Visualiza el número de horas realizadas individualmente por tus procesos RPA y áreas registradas. Siga los Resúmenes para comprender qué porcentaje del total de horas ejecutadas representa ese proceso."
        },
        "rpa_modal_2": {
            "pt-BR": "Tenha também acesso ao histórico das horas RPA por dia ou por mês desde a implementação do seu Dashboard.",
            "en": "Also get access to the history of RPA hours per day or per month since the implementation of your Dashboard.",
            "es": "Accede también al historial de horas de RPA por día o por mes desde la implementación de tu Dashboard."
        },
        "rpa_modal_3": {
            "pt-BR": "Importante: Apresentar mais ou menos horas de execução não é um indicador de desempenho positivo ou negativo do seu processo.",
            "en": "Important: Having more or less running hours is not a positive or negative performance indicator of your process.",
            "es": "Importante: tener más o menos horas de funcionamiento no es un indicador de rendimiento positivo o negativo de su proceso."
        },
        "rpa_modal_4": {
            "pt-BR": "A quantidade de horas acumuladas pode depender da complexidade dos diferentes processos, assim como variações na sua demanda.",
            "en": "The amount of accumulated hours may depend on the complexity of the different processes, as well as variations in their demand.",
            "es": "La cantidad de horas acumuladas puede depender de la complejidad de los diferentes procesos, así como de variaciones en su demanda."
        },
        "get_access_to_your_robot_occupancy": {
            "pt-BR": "Tenha acesso às informações de ocupação do seu (s) robô (s) em diferentes horas do dia, semanalmente, ou mensalmente.",
            "en": "Get access to your robot(s) occupancy information at different times of the day, weekly, or monthly.",
            "es": "Obtenga acceso a la información de ocupación de su(s) robot(es) en diferentes momentos del día, semanalmente o mensualmente."
        },
        "robot_occupancy_use_these_insights_to_better_schedule": {
            "pt-BR": "Utilize esses insights para programar melhor as execução dos seus processos e aproveitar melhor o tempo do seu robô. Caso tenha mais de um robô, também é possível identificar qual deles é mais indicado para cada execução.",
            "en": "Use these insights to better schedule the execution of your processes and make better use of your robot's time. If you have more than one robot, it is also possible to identify which one is most suitable for each execution.",
            "es": "Utilice estos conocimientos para programar mejor la ejecución de sus procesos y hacer un mejor uso del tiempo de su robot. Si tiene más de un robot, también es posible identificar cuál es el más adecuado para cada ejecución."
        },
        "view_the_history_of_the_status_of_all_the_executions_of_your_processes": {
            "pt-BR": "Vizualize o histórico dos status de todas as execuções dos seus processos.",
            "en": "View the history of the status of all the executions of your processes.",
            "es": "Visualiza el historial del estado de todas las ejecuciones de tus procesos."
        },
        "completed_processes": {
            "pt-BR": "Processos concluídos",
            "en": "Completed processes",
            "es": "procesos completados"
        },
        "failed_processes": {
            "pt-BR": "Processos que falharam",
            "en": "Failed processes",
            "es": "Procesos fallidos"
        },
        "are_those_that_managed_to_run_to_the_scheduled_end": {
            "pt-BR": "são aqueles conseguiram ser executados até o final programado.",
            "en": "are those that managed to run to the scheduled end.",
            "es": "son aquellos que lograron ejecutarse hasta el final programado."
        },
        "encountered_a_problem_that_prevented_the_execution": {
            "pt-BR": "encontraram algum problema que impossibilitou a que a execução chegasse até o final.",
            "en": "encountered a problem that prevented the execution from reaching the end.",
            "es": "se encontró un problema que impedía que la ejecución llegara al final"
        },
        "paused_processes": {
            "pt-BR": "Processos pausados",
            "en": "Paused processes",
            "es": "procesos en pausa"
        },
        "are_those_currently_on_hold_in_your_orchestrator_ui_path": {
            "pt-BR": "são aqueles que atualmente estão em espera no seu Orquestrador UI Path.",
            "en": "are those currently on hold in your Orchestrator UI Path.",
            "es": "son los que se encuentran actualmente en espera en la ruta de la interfaz de usuario de Orchestrator."
        },
        "nfse_maringa_title_and_subtitle": {
            "pt-BR": "Emissão de Notas Fiscais de Serviço (NFS-e) | Maringá",
            "en": "Issue of Service Invoices (NFS-e) | Maringá",
            "es": "Emisión de Facturas de Servicios (NFS-e) | Maringá"
        },
        "nfse_maringa_example_input": {
            "pt-BR": "Exemplo: \"Maringá - PR\"",
            "en": "Example: \"Maringá - PR\"",
            "es": "Ejemplo: \"Maringá - PR\""
        },
        "same_login_used_on_the_city_hall_of_maringa_pr_website": {
            "pt-BR": "Mesmo login utilizado no site Prefeitura de Maringá/PR.",
            "en": "Same login used on the City Hall of Maringá/PR website.",
            "es": "Mismo inicio de sesión utilizado en el sitio web de la Alcaldía de Maringá/PR."
        },
        "same_password_used_on_the_maringa_pr_city_hall_website": {
            "pt-BR": "Mesma senha utilizada no site da Prefeitura de Maringá/PR.",
            "en": "Same password used on the Maringá/PR City Hall website.",
            "es": "Misma contraseña utilizada en el sitio web del Ayuntamiento de Maringá/PR."
        },
        "nfse_maringa_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Prefeitura de  Maringá/PR. Se necessário, informe o período de emissão das notas que deseja buscar na configuração do modelo.",
            "en": "Configure a template informing your login credentials and password for the City Hall of Maringá/PR. If necessary, inform the period of issue of the notes that you want to search in the configuration of the model.",
            "es": "Configure un registro informando sus credenciales de inicio de sesión y contraseña para el Ayuntamiento de Maringá/PR. Si es necesario, informe el período de emisión de los billetes que desea buscar en la configuración del modelo."
        },
        "nfse_maringa_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das Notas Fiscais de Serviços Eletrônica – NFS-e relacionadas à credencial da Prefeitura de Maringá/PR informada.",
            "en": "This service issues and downloads the Electronic Service Invoices – NFS-e related to the informed Maringá/PR City Hall credential.",
            "es": "Este servicio emite y descarga las Facturas Electrónicas de Servicios – NFS-e relacionadas con la credencial informada del Ayuntamiento de Maringá/PR."
        },
        "maringa_pr_credentials": {
            "pt-BR": "Credenciais Maringá/PR",
            "en": "Maringá/PR Credentials",
            "es": "Credenciales Maringá/PR"
        },
        "nfse_maringa_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais da Prefeitura de Maringá/PR para buscar por todas as NFS-e emitidas em um período ou por notas específicas, o modelo fica salvo para reutilizar sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials from the Maringá/PR City Hall to search for all NFS-e issued in a period or for specific notes, the template is saved to reuse whenever you need it.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales del Ayuntamiento de Maringá/PR para buscar todos los NFS-e emitidos en un período o para notas específicas, la registro se guarda para reutilizarla cuando lo necesite."
        },
        "icms_ce_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | CE",
            "en": "Issuance of ICMS Guide | CE",
            "es": "Emisión de Guía ICMS | CE"
        },
        "icms_ce_example_input": {
            "pt-BR": "Exemplo: \"ICMS - CE\"",
            "en": "Example: \"ICMS - CE\"",
            "es": "Ejemplo: \"ICMS - CE\""
        },
        "search_by_services_or_terms": {
            "pt-BR": "Busque por serviços ou termos",
            "en": "Search by services or terms",
            "es": "Buscar por servicios o términos"
        },
        "banking": {
            "pt-BR": "Bancário",
            "en": "Banking",
            "es": "Bancario"
        },
        "cadastral_status": {
            "pt-BR": "Situação Cadastral",
            "en": "Cadastral Status",
            "es": "Estado de Registro"
        },
        "cars_and_transit": {
            "pt-BR": "Automóveis/Transito",
            "en": "Cars/Transit",
            "es": "Coches/Tránsito"
        },
        "consumption_accounts": {
            "pt-BR": "Contas de Consumo",
            "en": "Consumption Accounts",
            "es": "Cuentas de consumo"
        },
        "criminal_record": {
            "pt-BR": "Antecedentes Criminais",
            "en": "Criminal Record",
            "es": "Antecedentes criminales"
        },
        "debt_certificates": {
            "pt-BR": "Certidões de Débitos",
            "en": "Debt Certificates",
            "es": "Certificados de Deuda"
        },
        "international": {
            "pt-BR": "Internacional",
            "en": "International",
            "es": "Internacional"
        },
        "management": {
            "pt-BR": "Gestão",
            "en": "Management",
            "es": "Administración"
        },
        "nfe_and_nfse": {
            "pt-BR": "NF-e / NFS-e",
            "en": "NF-e / NFS-e",
            "es": "NF-e / NFS-e"
        },
        "processes": {
            "pt-BR": "Processos",
            "en": "Processes",
            "es": "Procesos "
        },
        "taxes": {
            "pt-BR": "Impostos",
            "en": "Taxes",
            "es": "Impuestos"
        },
        "icms_sc_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | SC",
            "en": "Issuance of ICMS Guide | SC",
            "es": "Emisión de Guía ICMS | SC"
        },
        "icms_sc_example_input": {
            "pt-BR": "Exemplo: \"ICMS - SC\"",
            "en": "Example: \"ICMS - SC\"",
            "es": "Ejemplo: \"ICMS - SC\""
        },
        "icms_pe_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | PE",
            "en": "Issuance of ICMS Guide | PE",
            "es": "Emisión de Guía ICMS | PE"
        },
        "icms_pe_example_input": {
            "pt-BR": "Exemplo: \"ICMS - PE\"",
            "en": "Example: \"ICMS - PE\"",
            "es": "Ejemplo: \"ICMS - PE\""
        },
        "nibo_credentials": {
            "pt-BR": "Credenciais da Nibo",
            "en": "Nibo credentials",
            "es": "Credenciales Nibo"
        },
        "nibo_title_and_subtitle": {
            "pt-BR": "Emissão de Relatórios Contábeis | Nibo",
            "en": "Issuance of Accounting Reports | Nibo",
            "es": "Emisión de Informes Contables | Nibo"
        },
        "nibo_example_input": {
            "pt-BR": "Exemplo: \"Relatório - Nibo\"",
            "en": "Example: \"Report - Nibo\"",
            "es": "Ejemplo: \"Informe - Nibo\""
        },
        "email_used_on_the_nibo_website": {
            "pt-BR": "E-mail utilizado no site da Nibo.",
            "en": "Email used on the Nibo website.",
            "es": "Correo electrónico utilizado en el sitio web de Nibo."
        },
        "password_used_on_the_nibo_website": {
            "pt-BR": "Senha utilizada no site da Nibo.",
            "en": "Password used on the Nibo website.",
            "es": "Contraseña utilizada en el sitio web de Nibo."
        },
        "nibo_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz download dos relatórios contábeis relacionados à credencial da Nibo informada.",
            "en": "This service issues and downloads accounting reports related to the informed Nibo credential.",
            "es": "Este servicio emite y descarga informes contables relacionados con la credencial Nibo informada."
        },
        "nibo_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais do site da Nibo e pode reutilizá-lo sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials from the Nibo website and can reuse it whenever you need to.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales desde el sitio web de Nibo y puede reutilizarla cuando lo necesite."
        },
        "nibo_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os relatórios chegam no link do OneDrive que você indicar no momento de configurar o modelo.",
            "en": "After using the service, the reports arrive at the OneDrive link that you indicate when configuring the model.",
            "es": "Después de utilizar el servicio, los informes llegan al enlace de OneDrive que indiques al configurar el modelo."
        },
        "nibo_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Nibo e um link do OneDrive para recebimento do arquivo.",
            "en": "Set up a template providing your Nibo login credentials and password and a OneDrive link to download the file.",
            "es": "Configure un registro que proporcione sus credenciales de inicio de sesión y contraseña de Nibo y un enlace de OneDrive para descargar el archivo."
        },
        "nibo_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os relatórios solicitados no OneDrive.",
            "en": "At the end of the service execution, you will receive the requested reports on OneDrive.",
            "es": "Al finalizar el servicio, recibirá los informes solicitados en OneDrive."
        },
        "get_all_reports_in_one_place_advantages_3": {
            "pt-BR": "Receba todos os relatórios em um só lugar",
            "en": "Get all reports in one place",
            "es": "Obtenga todos los informes en un solo lugar"
        },
        "so": {
            "pt-BR": "E aí",
            "en": "So",
            "es": "Entonces"
        },
        "hows_your_smarthis_hub_experience": {
            "pt-BR": "como está sua experiência no Smarthis Hub?",
            "en": "how's your Smarthis Hub experience?",
            "es": "¿cómo es tu experiencia Smarthis Hub?"
        },
        "can_we_help_you": {
            "pt-BR": "podemos te ajudar?",
            "en": "can we help you?",
            "es": "¿podemos ayudarte?"
        },
        "weve_set_up_important_information_for_you_to_enjoy_the_last_days_of_testing": {
            "pt-BR": "Separamos informações importantes para você aproveitar os últimos dias de teste!",
            "en": "We've set up important information for you to enjoy the last days of testing!",
            "es": "¡Hemos configurado información importante para que disfrutes de los últimos días de pruebas!"
        },
        "next_steps_what_to_do_now_that_the_trial_period_is_over": {
            "pt-BR": "Próximos passos: o que fazer agora que período de testes chegou ao fim?",
            "en": "Next steps: what to do now that the trial period is over?",
            "es": "Próximos pasos: ¿Qué hacer ahora qué período de prueba ha llegado a su fin?"
        },
        "can_we_talk_to_you": {
            "pt-BR": "podemos conversar com você?",
            "en": "can we talk to you?",
            "es": "¿podemos hablar contigo?"
        },
        "congrats_subscription_to_the_following_plan": {
            "pt-BR": "Sucesso! Contratação do plano",
            "en": "Congrats! Subscription to the following plan",
            "es": "¡Éxito! Contratación del plan"
        },
        "confirmed": {
            "pt-BR": "confirmada",
            "en": "confirmed",
            "es": "confirmado"
        },
        "how_to_calculate": {
            "pt-BR": "Como calcular?",
            "en": "How to calculate?",
            "es": "¿Como calcular?"
        },
        "calculator": {
            "pt-BR": "Calculadora",
            "en": "Calculator",
            "es": "Calculadora"
        },
        "calculator_subtitle_one": {
            "pt-BR": "Informe a quantidade, os salários e a porcentagem de dedicação de cada colaborador envolvido nesta tarefa. Assim será possível calcular o valor médio da hora deste Processo antes da implementação do RPA.",
            "en": "Inform the amount, salaries and percentage of dedication of each employee involved in this task. Thus, it will be possible to calculate the average hourly value of this Process before RPA implementation.",
            "es": "Informar el monto, salarios y porcentaje de dedicación de cada empleado involucrado en esta tarea. Así, será posible calcular el valor horario promedio de este Proceso antes de la implementación de RPA."
        },
        "calculator_subtitle_two": {
            "pt-BR": "para chegar à um valor mais apoximado de custo por colaborador, o resultado encontrado será multiplicado automaticamente por 1,5.",
            "en": "to arrive at a more approximate value of cost per employee, the result found will be automatically multiplied by 1.5.",
            "es": "para llegar a un valor más aproximado de coste por empleado, el resultado obtenido se multiplicará automáticamente por 1,5."
        },
        "columns": {
            "pt-BR": "Colunas",
            "en": "Columns",
            "es": "Columnas"
        },
        "qty": {
            "pt-BR": "Qtd.",
            "en": "Qty.",
            "es": "Cantidad"
        },
        "wage": {
            "pt-BR": "Salário",
            "en": "Wage",
            "es": "Salario"
        },
        "dedication": {
            "pt-BR": "Dedicação",
            "en": "Dedication",
            "es": "Dedicación"
        },
        "use_value": {
            "pt-BR": "Utilizar valor",
            "en": "Use value",
            "es": "Usar el valor"
        },
        "calculator_tooltip": {
            "pt-BR": "Para calcular o Valor médio da hora preencha primeiro os dois campos anteriores.",
            "en": "To calculate the Average Hourly Value, first fill in the two previous fields.",
            "es": "Para calcular el Valor Promedio por Hora, primero complete los dos campos anteriores."
        },
        "icms_pi_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | PI",
            "en": "Issuance of ICMS Guide | PI",
            "es": "Emisión de Guía ICMS | PI"
        },
        "icms_pi_example_input": {
            "pt-BR": "Exemplo: \"ICMS - PI\"",
            "en": "Example: \"ICMS - PI\"",
            "es": "Ejemplo: \"ICMS - PI\""
        },
        "icms_df_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | Distrito Federal",
            "en": "Issuance of ICMS Guide | Federal District",
            "es": "Emisión de Guía ICMS | Distrito Federal"
        },
        "icms_df_example_input": {
            "pt-BR": "Exemplo: \"ICMS - DF\"",
            "en": "Example: \"ICMS - DF\"",
            "es": "Ejemplo: \"ICMS - DF\""
        },
        "to_receive_the_file_you_need_to_create_a_folder_on_onedrive": {
            "pt-BR": "Para receber o arquivo é necessário criar uma pasta no OneDrive e configurar o compartilhamento para “Qualquer pessoa com link pode editar”. Depois, copie o link e cole neste campo.",
            "en": "To receive the file, you need to create a folder on OneDrive and set the sharing to “Anyone with a link can edit”. Then copy the link and paste in this field.",
            "es": "Para recibir el archivo, debe crear una carpeta en OneDrive y configurar el uso compartido en ”Cualquier persona con un enlace puede editar”. Luego copie el enlace y péguelo en este campo."
        },
        "onedrive_link_to_receive_the_file": {
            "pt-BR": "Link do OneDrive para receber o arquivo.",
            "en": "OneDrive link to receive the file.",
            "es": "Enlace de OneDrive para recibir el archivo."
        },
        "onedrive_link": {
            "pt-BR": "Link do OneDrive",
            "en": "OneDrive Link",
            "es": "Enlace de OneDrive"
        },
        "yes": {
            "pt-BR": "Sim",
            "en": "Yes",
            "es": "Sí"
        },
        "no": {
            "pt-BR": "Não",
            "en": "No",
            "es": "No"
        },
        "icms_pa_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | PA",
            "en": "Issuance of ICMS Guide | PA",
            "es": "Emisión de Guía ICMS | PA"
        },
        "icms_pa_example_input": {
            "pt-BR": "Exemplo: \"ICMS - PA\"",
            "en": "Example: \"ICMS - PA\"",
            "es": "Ejemplo: \"ICMS - PA\""
        },
        "cremerj_example_input": {
            "pt-BR": "Exemplo: \"CREMERJ\"",
            "en": "Example: \"CREMERJ\"",
            "es": "Ejemplo: \"CREMERJ\""
        },
        "cremerj_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral | CREMERJ",
            "en": "Verification of Cadastral Status | CREMERJ",
            "es": "Verificación del estado de registro | CREMERJ"
        },
        "cremerj_title_about_the_service": {
            "pt-BR": "Este serviço faz diferentes tipos de consultas no CREMERJ simultaneamente.",
            "en": "This service makes different types of queries in CREMERJ simultaneously.",
            "es": "Este servicio realiza diferentes tipos de consultas en CREMERJ simultáneamente."
        },
        "cremerj_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os dados de situação cadastral dos profissionais da área médica.",
            "en": "At the end of the service execution, you will receive the registration status data of the medical professionals.",
            "es": "Al finalizar la ejecución del servicio, recibirá los datos del estado de registro de los profesionales médicos."
        },
        "cremerj_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as situação cadastral dos profissionais da área médica.",
            "en": "After using the service, the results arrive by email with the registration status of medical professionals.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con el estado de registro de los profesionales médicos."
        },
        "cremerj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com o nome ou CRM do Médico que deseja verificar o status. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the name or CRM of the Doctor who wants to check the status. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con el nombre o CRM del Médico que desea consultar el estado. Luego configure un modelo utilizando el archivo completo."
        },
        "coren_rj_example_input": {
            "pt-BR": "Exemplo: \"COREN - RJ\"",
            "en": "Example: \"COREN - RJ\"",
            "es": "Ejemplo: \"COREN - RJ\""
        },
        "coren_rj_title_and_subtitle": {
            "pt-BR": "Verificação de Situação Cadastral COREN | RJ",
            "en": "Verification of Cadastral Status COREN | RJ",
            "es": "Verificación del estado de registro COREN | RJ"
        },
        "coren_rj_title_about_the_service": {
            "pt-BR": "Este serviço faz diferentes tipos de consultas no COREN do Rio de Janeiro simultaneamente.",
            "en": "This service makes different types of queries in COREN in Rio de Janeiro simultaneously.",
            "es": "Este servicio realiza simultáneamente diferentes tipos de consultas en el COREN de Río de Janeiro."
        },
        "coren_rj_discover_how_it_works_2": {
            "pt-BR": "Após utilizar o serviço, os resultados chegam por e-mail com as situação cadastral dos profissionais da área de enfermagem. ",
            "en": "After using the service, the results arrive by e-mail with the registration status of nursing professionals.",
            "es": "Después de utilizar el servicio, los resultados llegan por correo electrónico con el estado de registro de los profesionales de enfermería."
        },
        "coren_rj_instructions": {
            "pt-BR": "Faça download e preencha o Arquivo Padrão disponibilizado abaixo com o Nº de Inscrição, entre outras informações, do COREN - RJ que deseja verificar o status. Em seguida configure um modelo utilizando o arquivo preenchido.",
            "en": "Download and fill in the Standard File available below with the Registration Number, among other information, of the COREN - RJ that you want to check the status. Then configure a model using the filled file.",
            "es": "Descargue y complete el Archivo Estándar disponible a continuación con el Número de Registro, entre otros datos, del COREN - RJ cuyo estado desea consultar. Luego configure un modelo utilizando el archivo completo."
        },
        "coren_rj_subtitle_about_the_service": {
            "pt-BR": "Ao final da execução do serviço, você irá receber os dados de situação cadastral dos profissionais da área de enfermagem.",
            "en": "At the end of the service execution, you will receive the registration status data of nursing professionals.",
            "es": "Al finalizar la ejecución del servicio, recibirá los datos del estado de registro de los profesionales de enfermería."
        },
        "ready_we_resend_the_message": {
            "pt-BR": "Pronto! Reenviamos a mensagem",
            "en": "Ready! We resend the message",
            "es": "¡Listo! Reenviamos el mensaje"
        },
        "please_access_the_inbox_of": {
            "pt-BR": "Por favor, acesse a caixa de entrada de",
            "en": "Please access the inbox of",
            "es": "Accede a la bandeja de entrada de"
        },
        "open_the_welcome_message": {
            "pt-BR": "abra a mensagem de boas vindas e clique no botão para confirmar seu e-mail de cadastro no Smarthis Hub",
            "en": "open the welcome message and click the button to confirm your registration email on Smarthis Hub",
            "es": "abra el mensaje de bienvenida y haga clic en el botón para confirmar su correo electrónico de registro en Smarthis Hub"
        },
        "we_sent_the_message_to": {
            "pt-BR": "Enviamos a mensagem para",
            "en": "We sent the message to",
            "es": "Enviamos el mensaje a"
        },
        "if_you_havent_received_it_click": {
            "pt-BR": "Caso não tenha recebido, clique",
            "en": "If you haven't received it, click",
            "es": "Si no lo ha recibido, haga clic en"
        },
        "here_to_resend": {
            "pt-BR": "aqui para reenviar",
            "en": "here to resend",
            "es": "aquí para reenviar"
        },
        "or": {
            "pt-BR": "ou",
            "en": "or",
            "es": "o"
        },
        "here_to_edit_the_address": {
            "pt-BR": "aqui para editar o endereço",
            "en": "here to edit the address",
            "es": "aquí para editar la dirección"
        },
        "embratel_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Internet | Embratel",
            "en": "Issuance of Internet Accounts | Embratel",
            "es": "Emisión de Cuentas Internet | Embratel"
        },
        "embratel_example_input": {
            "pt-BR": "Exemplo: \"Internet - Embratel\"",
            "en": "Example: \"Internet - Embratel\"",
            "es": "Ejemplo: \"Internet - Embratel\""
        },
        "same_login_used_on_embratel_website": {
            "pt-BR": "Mesmo login utilizado no site da Embratel",
            "en": "Same login used on Embratel website",
            "es": "Mismo inicio de sesión utilizado en el sitio web de Embratel"
        },
        "same_password_used_on_embratel_website": {
            "pt-BR": "Mesma senha utilizada no site da Embratel",
            "en": "Same password used on the Embratel website",
            "es": "Misma contraseña utilizada en el sitio web de Embratel"
        },
        "embratel_credentials": {
            "pt-BR": "Credenciais da Embratel",
            "en": "Embratel Credentials",
            "es": "Credenciales Embratel"
        },
        "embratel_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais no site da Embratel e o reutiliza sempre que precisar.",
            "en": "With a few clicks, you set up a template with your credentials on the Embratel website and reuse it whenever you need it.",
            "es": "Con unos pocos clics, configura un registro con sus credenciales en el sitio web de Embratel y la reutiliza cuando lo necesite."
        },
        "embratel_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Embratel.",
            "en": "Configure a template informing your Embratel login credentials and password.",
            "es": "Configure un registro que informe sus credenciales de inicio de sesión y contraseña de Embratel."
        },
        "embratel_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de telefonia relacionadas às credenciais da Embratel informadas.",
            "en": "This service issues and downloads telephony bills related to the informed Embratel credentials.",
            "es": "Este servicio emite y descarga las facturas de telefonía relacionadas con las credenciales de Embratel informadas."
        },
        "congratulations_you_have_completed_all_the_steps_and_secured": {
            "pt-BR": "Parabéns, você completou todos os passos e garantiu",
            "en": "Congratulations, you have completed all the steps and secured",
            "es": "Felicitaciones, ha completado todos los pasos y asegurado"
        },
        "six_extra_days_in_your_trial_period": {
            "pt-BR": "6 dias extras no seu período de testes",
            "en": "6 extra days in your trial period",
            "es": "6 días adicionales en su período de prueba"
        },
        "to_continue_enjoying_all_the_benefits_of_the_hub_in_an_unlimited_way": {
            "pt-BR": "para continuar aproveitando todas as vantagens do Hub de maneira ilimitada!",
            "en": "to continue enjoying all the benefits of the Hub in an unlimited way!",
            "es": "para seguir disfrutando de todos los beneficios del Hub de forma ilimitada!"
        },
        "login_to_your_account_now": {
            "pt-BR": "Acesse sua conta agora",
            "en": "Login to your account now",
            "es": "Ingrese a su cuenta ahora"
        },
        "if_you_prefer_feel_free_to_reply_to_this_email_with_questions_or_suggestions": {
            "pt-BR": "Caso prefira, também fique à vontade para responder este e-mail com dúvidas ou sugestões.",
            "en": "If you prefer, feel free to reply to this email with questions or suggestions.",
            "es": "Si lo prefiere, no dude en responder a este correo electrónico con preguntas o sugerencias."
        },
        "see_you_later": {
            "pt-BR": "Até logo!",
            "en": "See you later!",
            "es": "¡Hasta luego!"
        },
        "congratulations_youve_earned_6_extra_days": {
            "pt-BR": "Parabéns: você ganhou 6 dias extras para usar o Hub sem limites!",
            "en": "Congratulations: you've earned 6 extra days to use the Hub without limits!",
            "es": "Felicitaciones: ¡ha ganado 6 días adicionales para usar el Hub sin límites!"
        },
        "icms_to_title_and_subtitle": {
            "pt-BR": "Emissão de Guia de ICMS | TO",
            "en": "Issuance of ICMS Guide | TO",
            "es": "Emisión de Guía ICMS | TO"
        },
        "icms_to_example_input": {
            "pt-BR": "Exemplo: \"ICMS-TO\"",
            "en": "Example: \"ICMS-TO\"",
            "es": "Ejemplo: \"ICMS-TO\""
        },
        "oi_title_and_subtitle": {
            "pt-BR": "Emissão de Contas de Telefone | Oi",
            "en": "Issuance of Telephone Bills | Oi",
            "es": "Emisión de Facturas Telefónicas | Oi"
        },
        "oi_example_input": {
            "pt-BR": "Exemplo: \"Conta - Oi\"",
            "en": "Example: \"Bill - Oi\"",
            "es": "Ejemplo: \"Cuenta - Oi\""
        },
        "same_login_used_on_oi_website": {
            "pt-BR": "Mesmo login utilizado no site da Oi",
            "en": "Same login used on Oi website",
            "es": "El mismo acceso utilizado en el sitio web de Oi"
        },
        "same_password_used_on_oi_website": {
            "pt-BR": "Mesma senha utilizada no site da Oi",
            "en": "Same password used on the Oi website",
            "es": "Misma contraseña utilizada en el sitio web de Oi"
        },
        "oi_instructions": {
            "pt-BR": "Configure um modelo informando as suas credenciais de login e senha da Oi.",
            "en": "Configure a template informing your Oi login credentials and password.",
            "es": "Configure una registro informando sus credenciales de inicio de sesión y contraseña de Oi."
        },
        "oi_title_about_the_service": {
            "pt-BR": "Este serviço emite e faz o download das contas de telefonia relacionadas à credencial da Oi informada.",
            "en": "This service issues and downloads the telephone bills related to the informed Oi credential.",
            "es": "Este servicio emite y descarga las facturas telefónicas relacionadas con la credencial Oi informada."
        },
        "oi_credentials": {
            "pt-BR": "Credenciais da Oi",
            "en": "Oi Credentials",
            "es": "Credenciales Oi"
        },
        "oi_discover_how_it_works_1": {
            "pt-BR": "Com alguns cliques, você configura um modelo com as suas credenciais no site da Oi e o reutiliza sempre que precisar.",
            "en": "With a few clicks, you configure a template with your credentials on Oi website and reuse it whenever you need it.",
            "es": "Con unos pocos clics, configuras un registro con tus credenciales en el sitio web de Oi y la reutilizas cuando lo necesitas."
        },

    }
    return dictionary[name][language]


@register.filter
def get_automation_display_name(automation_obj, language):
    if language == 'pt-BR':
        return automation_obj.display_name_pt_br
    elif language == 'es':
        return automation_obj.display_name_es
    else:
        return automation_obj.display_name_en


@register.filter
def check_if_automation_name_is_in_query(automation_name, query):
    automation_name_is_in_list = False
    for item in query:
        try:
            if item.name == automation_name:
                automation_name_is_in_list = True
        except AttributeError:
            if item.get('name', None) == automation_name:
                automation_name_is_in_list = True

    return automation_name_is_in_list
