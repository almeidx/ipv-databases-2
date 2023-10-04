from django.urls import path
import language.views as views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("create/", view=views.create),
    path("update/", view=views.update),
    path("update/<int:id>", view=views.update_real),
    path("read/", view=views.read),
    path("delete/", view=views.delete),
]
