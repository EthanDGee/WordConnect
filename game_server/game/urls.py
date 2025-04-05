from django.urls import path

from . import views

urlpatterns = [
    path("", views.game_view, name="game"),
    path("check-word/", views.check_word, name="check-word"),
]
