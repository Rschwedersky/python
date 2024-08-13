from subscriptions.templatetags.subscriptions_tags import get_progress_points


def onboarding_processor(request):
    try:
        subscription = request.subscription
    except AttributeError:
        return {}

    is_free_trial = subscription.plan.name == 'Free Trial'

    if not is_free_trial:
        return {'is_free_trial': False}

    total_points, reference = get_progress_points(request)
    confirm_email = request.email_was_verified

    return {
        'is_free_trial': is_free_trial,
        'total_progress': total_points,
        'reference': reference,
        'confirm_email': confirm_email,
    }
