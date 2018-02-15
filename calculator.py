from typing import Dict, Tuple, List, IO
import json
import sqlite3

class Champion:
    def __init__(self, name:str):
        conn = sqlite3.connect("data/champdata.sqlite")
        c = conn.cursor()
        r: Dict[str, float] = c.execute("SELECT").fetchone()

        # static quantities:
        self.hp_base = r["hp"]
        self.hp_perlevel = r["hpperlevel"]
        self.mp_base = r["mp"]
        self.mp_perlevel = r["mpperlevel"]
        self.base_movespeed = r["movespeed"]
        self.armor_base = r["armor"]
        self.armor_perlevel = r["armorperlevel"]
        self.spellblock_base = r["spellblock"]
        self.spellblock_perlevel = ["spellblockperlevel"]
        self.attackrange = r["attackrange"]
        self.hpregen_base = r["hpregen"]
        self.hpregen_perlevel = r["hpregenperlevel"]
        self.mpregen_base = r["mpregen"]
        self.mpregen_perlevel = r["mpregenperlevel"]
        self.crit_base = r["crit"]
        self.crit_perlevel = r["critperlevel"]
        self.attackdamage_base = r["attackdamage"]
        self.attackdamage_perlevel = r["attackdamageperlevel"]
        self.attackspeed_offset = r["attackspeedoffest"]
        self.attackspeed_perlevel = r["attackspeedperlevel"]
        
        # dynamic quantities:
        self.level = 1
        self.items = []
        self.buffs = []
        self.debuffs = []
    def get_maxhp(self) -> float:
        return self.hp_base + (self.level - 1) * self.hp_perlevel
    def get_maxmp(self) -> float:
        return self.mp_base + (self.level-1) * self.mp_perlevel
    def get_attackdamage(self) -> float:
        return self.attackdamage_base + (self.level-1) * self.attackdamage_perlevel

def load_data():
    champ_data: List[Dict]= []
    f: IO = open("champion.json")
    filecontents: Dict = json.loads(f.read())
    for champ in filecontents["data"]:
        champ_data.append(champ)
    return champ_data
def main():
    champ_data = load_data()
    print(champ_data)

main()