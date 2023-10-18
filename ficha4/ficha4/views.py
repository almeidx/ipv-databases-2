from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from django.conf import settings

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
        value = request.POST.get("value")

        if not key == "" and not value == "":
            collection.insert_one({"designacao": designacao, key: value})
        else:
            collection.insert_one({"designacao": designacao})

        return HttpResponse("Objeto criado com sucesso!")

    return render(request, "create.html")
