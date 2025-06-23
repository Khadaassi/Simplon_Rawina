from django.urls import path

from .views import (
    DashboardView,
    StoryCreateView,
    StoryListView,
)
app_name = "rawina"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("stories/", StoryListView.as_view(), name="story_list"),
    path("stories/create/", StoryCreateView.as_view(), name="story_create"),
]