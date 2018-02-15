from typing import Dict, List
import os
import urllib.request
import json
import sqlite3

latest_patch: str = "8.3.1"
text_attributes: List[str] = ["id", "name", "title", "blurb"]
int_attributes: List[str] = ["key"]
real_attributes: List[str] = [
    "hp", "hpperlevel", "mp", "mpperlevel", "movespeed", "armor", "armorperlevel","spellblock",
    "spellblockperlevel", "attackrange", "hpregen", "hpregenperlevel", "mpregen", "mpregenperlevel", 
    "crit", "critperlevel", "attackdamage","attackdamageperlevel", "attackspeedoffset","attackspeedperlevel"
]
def main() -> None:
    conn = sqlite3.connect('data/champdata.sqlite')
    json_local_filename = 'data/champion.json'
    c = conn.cursor()
    create_table_sql = "CREATE TABLE champions (" + \
        ", ".join(x+" TEXT" for x in text_attributes) + ", " + \
        ", ".join(x+" INTEGER" for x in int_attributes) + ", " + \
        ", ".join(x+" REAL" for x in real_attributes) + ")"
    try: c.execute(create_table_sql)
    except sqlite3.OperationalError as e:
        if str(e) == "table champions already exists": pass
        else: raise Exception()
    url: str = 'http://ddragon.leagueoflegends.com/cdn/'+latest_patch+'/data/en_US/champion.json'
    urllib.request.urlretrieve(url, filename=json_local_filename)
    data: Dict = json.load(open(json_local_filename))
    for _, champ in data["data"].items():
        sql_command = "INSERT INTO champions (" + \
            ",".join(text_attributes+int_attributes+real_attributes) + \
            ") VALUES (" + ",".join(
                "?" for i in range(len(text_attributes)+len(int_attributes)+len(real_attributes)))+")"
        c.execute(sql_command, [champ[x] for x in text_attributes+int_attributes] + [champ["stats"][x] for x in real_attributes])
    c.close()
    conn.commit()
    conn.close()
    #os.remove(json_local_filename)
    
main()