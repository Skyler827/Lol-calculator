from typing import Dict, List
import os
import urllib.request
import json
import sqlite3
from champ_statistics import ChampStatistic

latest_patch: str = "8.13.1"

def set_champs_table() -> None:
    text_attributes: List[str] = ["id", "name", "title", "blurb", "partype"]
    int_attributes: List[str] = ["key"]
    real_attributes: List[str] = [
        "hp", "hpperlevel", "mp", "mpperlevel", "movespeed", "armor", "armorperlevel","spellblock",
        "spellblockperlevel", "attackrange", "hpregen", "hpregenperlevel", "mpregen", "mpregenperlevel", 
        "crit", "critperlevel", "attackdamage","attackdamageperlevel", "attackspeedoffset","attackspeedperlevel"
    ]
    def create_champs_table() -> None:
        conn = sqlite3.connect('file:champdata.db?mode=rwc', uri=True)
        c = conn.cursor()
        create_table_sql = "CREATE TABLE champions (" + \
            ", ".join(x+" TEXT" for x in text_attributes) + ", " + \
            ", ".join(x+" INTEGER" for x in int_attributes) + ", " + \
            ", ".join(x+" REAL" for x in real_attributes) + ")"
        try: c.execute(create_table_sql)
        except sqlite3.OperationalError as e:
            if str(e) == "table champions already exists":
                c.execute("DELETE FROM champions")
            else: raise e
        c.close()
        conn.commit()
        conn.close()
    def enter_champ_data():
        conn = sqlite3.connect('file:champdata.db?mode=rw', uri=True)
        c = conn.cursor()
        url: str = 'http://ddragon.leagueoflegends.com/cdn/'+latest_patch+'/data/en_US/champion.json'
        json_local_filename = 'champion.json'
        if os.path.isfile(json_local_filename): pass
        else: urllib.request.urlretrieve(url, filename=json_local_filename)
        data: Dict = json.load(open(json_local_filename))
        for _, champ in data["data"].items():
            sql_command = "INSERT INTO champions (" + \
                ",".join(text_attributes+int_attributes+real_attributes) + \
                ") VALUES (" + ",".join(
                    "?" for i in range(len(text_attributes)+len(int_attributes)+len(real_attributes)))+")"
            c.execute(sql_command, [champ[x] for x in text_attributes+int_attributes] + [champ["stats"][x] for x in real_attributes])
            #print(sql_command)
            #print(champ["stats"])
        c.close()
        conn.commit()
        conn.close()
    create_champs_table()
    enter_champ_data()

def set_statistics_table() -> None:
    def create_statistics_table() -> None:
        conn = sqlite3.connect('file:champdata.db?mode=rwc', uri=True)
        c = conn.cursor()
        create_table_sql = "CREATE TABLE statistics (name);"
        try:
            c.execute(create_table_sql)
        except sqlite3.OperationalError as e:
            if str(e) == "table statistics already exists":
                c.execute("DELETE FROM statistics;")
            else: raise e
        c.close()
        conn.commit()            
        conn.close()
    def set_statistics_data() -> None:
        conn = sqlite3.connect('file:champdata.db?mode=rw', uri=True)
        c = conn.cursor()
        stat_names = [name for name, _ in ChampStatistic.__members__.items()]
        c.executemany("INSERT INTO statistics (name) VALUES (?)", stat_names)
        c.close()
        conn.commit()            
        conn.close()
    create_statistics_table()
    set_statistics_data()
def create_item_table() -> None:
    # Need to create 
    conn = sqlite3.connect('file:champdata.db?mode=rwc', uri=True)
    c = conn.cursor()
    create_table_sql = "CREATE TABLE items ();"
    try: c.execute(create_table_sql)
    except sqlite3.OperationalError as e:
        if str(e) == "table items already exists":
            c.execute("DELETE FROM items;")
            print("table champions already exists, passing")
        else: raise e
    c.close()
    conn.commit()
    conn.close()
def main() -> None:
    set_champs_table()
    set_statistics_table()
    
main()