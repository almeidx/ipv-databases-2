from django.http import HttpResponse
from django.shortcuts import render, redirect
from category.forms import CategoryForm
from time import time
from math import floor


def index(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL insert_categoria(%s::character(25), to_timestamp(%s)::timestamp without time zone);",
                    [form.cleaned_data["name"], floor(time())],
                )

            return redirect("success")
    else:
        form = CategoryForm()

    return render(request, "category/index.html", {"form": form})


def success(request):
    return HttpResponse("Categoria criada com sucesso!")
