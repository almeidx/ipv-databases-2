from django.urls import path
import category.views as views

urlpatterns = [
    path("", view=views.index, name="index"),
    path("create/", view=views.create),
    path("read/", view=views.read),
    path("update/", view=views.update),
    path("update/<int:id>", view=views.update_real),
    path("delete/", view=views.delete),
]
