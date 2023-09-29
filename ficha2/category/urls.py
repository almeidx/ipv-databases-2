from django.urls import path
import category.views as views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("success/", view=views.success, name="success"),
]
