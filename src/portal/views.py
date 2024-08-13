from django.shortcuts import render, reverse

from dashboard.templatetags.dashboard_tags import getLanguage


def handler404(request, exception):
    language = getLanguage(request)

    context = {
        'status': 400,
        'language': language,
        'hidenavbar': 1,
        'hidehole_navbar': True,
        'hide_warnings': True,
    }

    return render(request, 'error/404.html', context)


def handler500(request):
    language = getLanguage(request)

    context = {
        'status': 500,
        'language': language,
        'hidenavbar': 1,
        'hidehole_navbar': True,
        'hide_warnings': True,
    }
    return render(request, 'error/500.html', context)
