from django.urls import path

from project_module.apis import views

urlpatterns = [
     path("listing/", views.ModuleListView.as_view(), name="project_module-list"),
]
