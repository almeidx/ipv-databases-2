from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from django.conf import settings
from bson.objectid import ObjectId

db_settings = settings.DATABASES["default"]
client = MongoClient(
    host=db_settings["CLIENT"]["host"], port=db_settings["CLIENT"]["port"]
)
db = client[db_settings["NAME"]]
collection = db["objetos"]


def index(request):
    return render(request, "index.html")


def list(request):
    documents = collection.find()

    return render(request, "list.html", {"documents": documents})


def create(request):
    if request.method == "POST":
        designacao = request.POST.get("designacao")
        key = request.POST.get("key")
        value = request.POST.getlist("value")

        # remover valores vazios
        value = [val for val in value if val != ""]

        if len(value) == 1:
            value = value[0]

        if not key == "" and not value == "" and not value == []:
            collection.insert_one({"designacao": designacao, key: value})
        else:
            collection.insert_one({"designacao": designacao})

        return HttpResponse("Objeto criado com sucesso!")

    return render(request, "create.html")


def edit(request, id):
    if request.method == "POST":
        designacao = request.POST.get("designacao")
        key = request.POST.get("key")
        value = request.POST.getlist("value")

        # remover valores vazios
        value = [val for val in value if val != ""]

        if len(value) == 1:
            value = value[0]

        if not key == "" and not value == "" and not value == []:
            collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"designacao": designacao, key: value}}
            )
        else:
            collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"designacao": designacao}}
            )

        return HttpResponse("Objeto editado com sucesso!")

    document = collection.find_one({"_id": ObjectId(id)})

    # transformar values dinâmicos de tipo string em listas
    for key, value in document.items():
        if not key == "_id" and not key == "designacao" and isinstance(value, str):
            document[key] = [value]

    return render(request, "edit.html", {"document": document, "id": id})


def delete(_request, id):
    collection.delete_one({"_id": ObjectId(id)})
    return HttpResponse("Objeto eliminado com sucesso!")
