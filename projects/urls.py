from django.urls import path
from . import views

urlpatterns = [
  path("interview/", views.interview_index, name="interview_index"),
  path("interview/<int:pk>/", views.interview_detail, name="interview_detail"),
  path("interview/speech_to_text/", views.interview_speech_to_text, name="interview_speech_to_text")
]