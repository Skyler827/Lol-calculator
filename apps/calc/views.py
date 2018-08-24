import sqlite3
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .calc_core import initializedb as init
latest_patch: str = "8.16.1"
db_name:str = os.path.join("data", latest_patch, "league_data.db")

# Create your views here.
def index(request):
    return render(request, "calc/base.html")
def initializedb(request):
    init.main()
    return HttpResponse("data initialized")
def champion_id_names(request):
    conn = sqlite3.connect(f'file:{db_name}?mode=rwc', uri=True)
    c = conn.cursor()
    c.execute(f"SELECT id, name FROM champions")
    data = c.fetchall()
    c.close()
    conn.commit()
    return JsonResponse(data, safe=False)
def get_item_ids(request):
    conn = sqlite3.connect(f'file:{db_name}?mode=rwc', uri=True)
    c = conn.cursor()
    c.execute(f"SELECT id, name FROM items WHERE gold_total > 49")
    data = c.fetchall()
    c.close()
    conn.commit()
    return JsonResponse(data, safe=False)
def simulate_combat(request):
    return JsonResponse({
        "red-champ": [
            {"x":0, "y":150},
            {"x":1, "y":20},
            {"x":2, "y":10},
            {"x":3, "y":30},
            {"x":4, "y":5},
            {"x":5, "y":0}
        ], "blue-champ": [
            {"x":0, "y":100},
            {"x":1, "y":85},
            {"x":2, "y":70},
            {"x":3, "y":100},
            {"x":4, "y":50},
            {"x":5, "y":20}
        ]
    })