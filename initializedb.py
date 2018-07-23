from typing import Dict, List
import os
import urllib.request
import json
import sqlite3
import os.path
from champ_statistics import ChampStatistic, get_stat_from_string

latest_patch: str = "8.13.1"
db_name:str = os.path.join("data", latest_patch, "league_data.db")
champion_json_filename:str = os.path.join("data", latest_patch, "champion.json")
item_json_filename:str = os.path.join("data", latest_patch, "items.json")

def check_directory() -> None:
    d: str = os.path.join("data", latest_patch)
    if not os.path.exists(d):
        os.makedirs(d)
def create_and_populate_table(table_name:str, columns:Dict[str,str], values:List[Dict[str, any]]) -> None:
    """replaces a table in the database with a given table with new data

    columns: key is the column name, value is the SQL data type along with other constraints
    values: list of records, each with keys for the name of the column and a value for the data content
    """
    assert(set(columns.keys())==set(values[0].keys()))
    conn = sqlite3.connect(f'file:{db_name}?mode=rwc', uri=True)
    def clear_table():
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table_name};")
        c.close()
        conn.commit()
    def create_table():
        c = conn.cursor()
        sql = f"CREATE TABLE {table_name} ({','.join(' '+k+' '+columns[k] for k in columns.keys())})"
        c.execute(sql)
        c.close()
        conn.commit()
    def insert_data():
        c = conn.cursor()
        preamble = f"INSERT INTO {table_name}"
        value_enumeration = "(" + ','.join(f":{k}" for k in columns.keys())+")"
        sql = f"{preamble} VALUES {value_enumeration}"
        c.executemany(sql, values)
        c.close()
        conn.commit()
    clear_table()
    create_table()
    insert_data()
    conn.close()
def set_champs_table() -> None:
    columns = {}
    text_attributes: List[str] = ["id", "name", "title", "blurb", "partype"]
    int_attributes: List[str] = ["key"]
    real_attributes: List[str] = [
        "hp", "hpperlevel", "mp", "mpperlevel", "movespeed", "armor", "armorperlevel","spellblock",
        "spellblockperlevel", "attackrange", "hpregen", "hpregenperlevel", "mpregen", "mpregenperlevel", 
        "crit", "critperlevel", "attackdamage","attackdamageperlevel", "attackspeedoffset","attackspeedperlevel"
    ]
    for x in text_attributes:
        columns[x] = "TEXT"
    for x in int_attributes:
        columns[x] = "INTEGER"
    for x in real_attributes:
        columns[x] = "FLOAT"
    url: str = 'http://ddragon.leagueoflegends.com/cdn/'+latest_patch+'/data/en_US/champion.json'
    if os.path.isfile(champion_json_filename): pass
    else: urllib.request.urlretrieve(url, filename=champion_json_filename)
    data: Dict = json.load(open(champion_json_filename, errors="replace"))['data']
    values:List[Dict] = []
    for champ in data.keys():
        champ_obj = {}
        for x in text_attributes + int_attributes:
            champ_obj[x] = data[champ][x]
        for x in real_attributes:
            champ_obj[x] = data[champ]['stats'][x]
        values.append(champ_obj)
    create_and_populate_table("champions", columns, values)
def set_statistics_table() -> None:
    stat_names:List[str] = [name for name, _ in ChampStatistic.__members__.items()]
    columns = {"name":"TEXT PRIMARY KEY"}
    values:List[Dict[str, str]] = []
    for i in stat_names:
        values.append({"name": i})
    create_and_populate_table("champ_statistics", columns, values)

def set_item_table() -> None:
    url: str = f"http://ddragon.leagueoflegends.com/cdn/{latest_patch}/data/en_US/item.json"
    if not os.path.isfile(item_json_filename):
        urllib.request.urlretrieve(url, filename=item_json_filename)
    data: Dict = json.load(open(item_json_filename))['data']
    columns = {
        "id":"INTEGER PRIMARY KEY",
        "name":"TEXT",
        "plaintext":"TEXT",
        "gold_base": "INTEGER",
        "gold_total": "INTEGER",
        "sell": "INTEGER",
        "component1": "INTEGER REFERENCES(items)",
        "component2": "INTEGER REFERENCES(items)",
        "component3": "INTEGER REFERENCES(items)",
        "component4": "INTEGER REFERENCES(items)",
    }
    values = []
    for id in data.keys():
        x = data[id]
        obj = {
            "id": id,
            "name": x["name"],
            "plaintext": x["plaintext"],
            "gold_base": x["gold"]["base"],
            "gold_total": x["gold"]["total"],
            "sell" : x["gold"]["sell"]
        }
        try:
            obj["component1"] = x["from"][0]
            obj["component2"] = x["from"][1]
            obj["component3"] = x["from"][2]
            obj["component4"] = x["from"][3]
        except: pass
        values.append(obj)
    create_and_populate_table("items", columns, values)
def set_item_stats() -> None:
    data: Dict = json.load(open(item_json_filename))['data']
    columns = {
        "item": "INTEGER REFERENCES items(id)",
        "stat": "TEXT REFERENCES statistics(name)",
        "mod": "INTEGER"
    }
    values = []
    for id in data.keys():
        x = data[id]
        offset = len("Champstatistic.")
        for stat_name,stat_mod in x["stats"].items():
            values.append({
                "item":str(id),
                "stat": str(get_stat_from_string(stat_name))[offset:],
                "mod": stat_mod
            })
    create_and_populate_table("item_stats", columns, values)

def main() -> None:
    check_directory()
    set_champs_table()
    set_statistics_table()
    set_item_table()
    set_item_stats()
if __name__ =="__main__":
    main()