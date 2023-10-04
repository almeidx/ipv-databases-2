from django.shortcuts import render, redirect
from language.forms import LanguageForm, LanguageIdForm
from time import time
from math import floor


def index(request):
    return render(request, "language/index.html")


def create(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL insert_language(%s::character(20), to_timestamp(%s)::timestamp without time zone);",
                    [form.cleaned_data["name"], floor(time())],
                )

            return render(
                request,
                "success.html",
                {"message": "Linguagem criada com sucesso", "back": "/language/"},
            )
    else:
        form = LanguageForm()

    return render(request, "language/create.html", {"form": form})


def read(request):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT language_id, name FROM language ORDER BY language_id;")
        rows = cursor.fetchall()

    return render(request, "language/read.html", {"rows": rows})


def update(request):
    if request.method == "POST":
        form = LanguageIdForm(request.POST)
        if form.is_valid():
            return redirect(f"/language/update/{form.cleaned_data['id']}")
    else:
        form = LanguageIdForm()

    return render(request, "language/update.html", {"form": form})


def update_real(request, id):
    from django.db import connection

    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE language SET name = %s WHERE language_id = %s;",
                    [form.cleaned_data["name"], id],
                )

            return render(
                request,
                "success.html",
                {"message": "Linguagem atualizada com sucesso", "back": "/language/"},
            )
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT language_id, name FROM language WHERE language_id = %s;",
                [id],
            )
            row = cursor.fetchone()

        form = LanguageForm(initial={"name": row[1]})
        return render(request, "language/update_real.html", {"form": form, "row": row})


def delete(request):
    if request.method == "POST":
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM language WHERE language_id = %s;",
                [request.POST["id"]],
            )

        return render(
            request,
            "success.html",
            {"message": "Linguagem eliminada com sucesso", "back": "/language/"},
        )

    return render(request, "language/delete.html")
