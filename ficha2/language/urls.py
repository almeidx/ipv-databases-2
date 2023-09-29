from django.urls import path
import language.views as views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("success/", view=views.success, name="success"),
]
