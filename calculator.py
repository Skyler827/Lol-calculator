from typing import Dict, Tuple, List, IO
import json

class Champion_Data:
    def __init__(self, data: Dict):
        data = json.loads(json)
        self.id: str = data["id"]
        self.key: int = data["key"]
        self.name: str = data["name"]
        self.title: str = data["title"]
        self.blurb: str = data["blurb"]
        self.stats: str = data["stats"]
class Champion_imp():
    def __init__(self, champid: str):
        self.champid = ""

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