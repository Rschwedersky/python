from django.http import JsonResponse

from django.views.decorators.http import require_http_methods

from .models import Schedule, Task

# [GET]/api/schedule/{id}


def get_state(request, id):
    try:
        schedule = Schedule.objects.get(pk=id, user=request.user)

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

        try:
            task = Task.objects.filter(schedule=schedule).latest('created_at')
            response = {
                "schedule_id": schedule.id,
                "state": translate_task_state_to_schedule_state(task.state)
            }
            return JsonResponse(response)
        except Task.DoesNotExist:
            return JsonResponse({
                "schedule_id": schedule.id,
                "state": 'IDDLE'
            })

    except Schedule.DoesNotExist:
        return JsonResponse({"error": "schedule not fould"}, status=404)
