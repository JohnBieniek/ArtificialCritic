from django.shortcuts import render
from django.views.decorators.http import require_safe

from src.critic_service import CriticService


@require_safe
def catalogue(request):
    return render(
        request,
        "catalogue.html",
        {"movies": CriticService().list_movies()},
    )
