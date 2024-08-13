from django.contrib import admin
from my_solutions.templatetags.mysolutions_tags import send_appropriate_email

from subscriptions.models import AutomationsClients

from .models import Automation, Schedule, Task


class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'automation',
        'user',
        'client',
        'get_state',
        'cron_expression',
        'execution_date'
    ]

    def get_state(self, instance):
        def translate_task_state_to_schedule_state(task_state):
            TASK_STATES = (
                (1, 'IDDLE'),
                (2, 'READY'),
                (3, 'PROCESSING'),
                (4, 'FAULTED'),
                (5, 'CANCELED'),
                (6, 'FINISHED'),
                (7, 'RESULTS SENT')
            )

            STATES_IN_TASKS_TO_SCHEDULE = {
                'IDDLE': 'IDDLE',
                'READY': 'RUNNING',
                'PROCESSING': 'RUNNING',
                'FAULTED': 'FAULTED',
                'CANCELED': 'IDDLE',
                'FINISHED': 'IDDLE',
                'RESULTS SENT': 'IDDLE'
            }
            task_state = TASK_STATES[task_state-1][1]
            return STATES_IN_TASKS_TO_SCHEDULE[task_state]

        task = Task.objects.filter(schedule=instance).latest('created_at')
        return translate_task_state_to_schedule_state(task.state)


admin.site.register(Schedule, ScheduleAdmin)


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = [
        'id',
        'schedule',
        'get_automation_name',
        'get_task_state',
        'get_task_owner',
        'get_send_results_to',
        'get_client_name',
    ]

    list_filter = ['schedule__user__profile__client',
                   'schedule__automation__name']

    def get_automation_name(self, instance):
        automation_name = instance.schedule.automation.name
        return automation_name
    get_automation_name.short_description = 'Automation'

    def get_task_state(self, instance):
        TASK_STATES = ((1, 'IDDLE'),
                       (2, 'READY'),
                       (3, 'PROCESSING'),
                       (4, 'FAULTED'),
                       (5, 'CANCELED'),
                       (6, 'FINISHED'),
                       (7, 'RESULTS SENT'))
        return TASK_STATES[instance.state - 1][1]
    get_task_state.short_description = 'State'

    def get_task_owner(self, instance):
        return f"{instance.schedule.user.first_name} {instance.schedule.user.last_name}"
    get_task_owner.short_description = 'Owner'

    def get_send_results_to(self, instance):
        return instance.schedule.email_to_send_results
    get_send_results_to.short_description = "Send results to"

    def get_client_name(self, instance):
        return instance.schedule.user.profile.client.name
    get_client_name.short_description = "Organization"


class AutomationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active',
                    'how_many_allocated', 'is_showcase']

    def how_many_allocated(self, obj):
        howmany_automations = AutomationsClients.objects.filter(
            automation__name=obj.name)
        how_many = 0
        for automation in howmany_automations:
            how_many += automation.qnt_automations
        return how_many

    def save_model(self, request, obj, form, change):
        what_has_changed = form.changed_data
        if change == True and what_has_changed == ['active']:
            send_appropriate_email(request, obj)
        return super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
admin.site.register(Automation, AutomationsAdmin)
