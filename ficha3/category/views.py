from django.shortcuts import render, redirect
from category.forms import CategoryForm, CategoryIdForm
from time import time
from math import floor


def index(request):
    return render(request, "category/index.html")


def create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL insert_categoria(%s::character(25), to_timestamp(%s)::timestamp without time zone);",
                    [form.cleaned_data["name"], floor(time())],
                )

            return render(
                request,
                "success.html",
                {"message": "Categoria criada com sucesso", "back": "/category/"},
            )
    else:
        form = CategoryForm()

    return render(request, "category/create.html", {"form": form})


def read(request):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT category_id, name FROM category ORDER BY category_id;")
        rows = cursor.fetchall()

    return render(request, "category/read.html", {"rows": rows})


def update(request):
    if request.method == "POST":
        form = CategoryIdForm(request.POST)
        if form.is_valid():
            return redirect(f"/category/update/{form.cleaned_data['id']}")
    else:
        form = CategoryIdForm()

    return render(request, "category/update.html", {"form": form})


def update_real(request, id):
    from django.db import connection

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE category SET name = %s WHERE category_id = %s;",
                    [form.cleaned_data["name"], id],
                )

            return render(
                request,
                "success.html",
                {"message": "Categoria atualizada com sucesso", "back": "/category/"},
            )
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT category_id, name FROM category WHERE category_id = %s;",
                [id],
            )
            row = cursor.fetchone()

        form = CategoryForm(initial={"name": row[1]})
        return render(request, "category/update_real.html", {"form": form, "row": row})


def delete(request):
    if request.method == "POST":
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM category WHERE category_id = %s;",
                [request.POST["id"]],
            )

        return render(
            request,
            "success.html",
            {"message": "Categoria eliminada com sucesso", "back": "/category/"},
        )

    return render(request, "category/delete.html")
