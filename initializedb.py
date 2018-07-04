from typing import Dict, List
import os
import urllib.request
import json
import sqlite3

latest_patch: str = "8.13.1"
text_attributes: List[str] = ["id", "name", "title", "blurb"]
int_attributes: List[str] = ["key"]
real_attributes: List[str] = [
    "hp", "hpperlevel", "mp", "mpperlevel", "movespeed", "armor", "armorperlevel","spellblock",
    "spellblockperlevel", "attackrange", "hpregen", "hpregenperlevel", "mpregen", "mpregenperlevel", 
    "crit", "critperlevel", "attackdamage","attackdamageperlevel", "attackspeedoffset","attackspeedperlevel"
]
def main() -> None:
    conn = sqlite3.connect('file:champdata.db?mode=rwc', uri=True)
    json_local_filename = 'champion.json'
    c = conn.cursor()
    create_table_sql = "CREATE TABLE champions (" + \
        ", ".join(x+" TEXT" for x in text_attributes) + ", " + \
        ", ".join(x+" INTEGER" for x in int_attributes) + ", " + \
        ", ".join(x+" REAL" for x in real_attributes) + ")"
    print(create_table_sql)
    try: c.execute(create_table_sql)
    except sqlite3.OperationalError as e:
        if str(e) == "table champions already exists":
            print("table champions already exists, passing")
        else: raise Exception()
    c.close()
    conn.commit()
    conn.close()
    conn2 = sqlite3.connect('file:champdata.db?mode=rw', uri=True)
    c2 = conn2.cursor()
    url: str = 'http://ddragon.leagueoflegends.com/cdn/'+latest_patch+'/data/en_US/champion.json'
    if os.path.isfile(json_local_filename): pass
    else: urllib.request.urlretrieve(url, filename=json_local_filename)
    data: Dict = json.load(open(json_local_filename))
    no_of_champs = 0
    for _, champ in data["data"].items():
        sql_command = "INSERT INTO champions (" + \
            ",".join(text_attributes+int_attributes+real_attributes) + \
            ") VALUES (" + ",".join(
                "?" for i in range(len(text_attributes)+len(int_attributes)+len(real_attributes)))+")"
        c2.execute(sql_command, [champ[x] for x in text_attributes+int_attributes] + [champ["stats"][x] for x in real_attributes])
        no_of_champs += 1
        #print(sql_command)
        #print(champ["stats"])
    c2.close()
    conn2.commit()
    conn2.close()
    print(no_of_champs)
    #os.remove(json_local_filename)
    
main()