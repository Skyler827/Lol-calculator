import sqlite3
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .calc_core import initializedb as init
from .calc_core.timer import run_combat
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
    x = run_combat(
        blue_champion_name=request.GET["blue_champ"],
        blue_champ_level=request.GET["blue_level"],
        blue_champ_items=request.GET.getlist("blue_items[]"),
        red_champion_name=request.GET["red_champ"],
        red_champ_level=request.GET["red_level"],
        red_champ_items=request.GET.getlist("red_items[]")
    )
    return JsonResponse({
        "blue-champ": x["blue_champ_hp"],
        "red-champ": x["red_champ_hp"],
    })