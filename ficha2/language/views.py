from django.http import HttpResponse
from django.shortcuts import render, redirect
from language.forms import LanguageForm
from time import time
from math import floor


def index(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL insert_language(%s::character(20), to_timestamp(%s)::timestamp without time zone);",
                    [form.cleaned_data["name"], floor(time())],
                )

            return redirect("success")
    else:
        form = LanguageForm()

    return render(request, "language/index.html", {"form": form})


def success(request):
    return HttpResponse("Linguagem criada com sucesso!")
