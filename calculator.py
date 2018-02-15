from typing import Dict, Tuple, List
import json

class Champion_Data:
    def __init__(self, data: Dict):
        data = json.loads(json)
        self.id = data["id"]
        self.key = data["key"]
        self.name = data["name"]
        self.title = data["title"]
        self.blurb = data["blurb"]
        self.stats = data["stats"]
class Champion_imp():
    def __init__(self, champid):
        self.champid = ""

def load_data():
    champ_data = []
    f = open("champion.json")
    filecontents = json.loads(f.read())
    for champ in filecontents["data"]:
        champ_data.append(champ)
    return champ_data
def main():
    champ_data = load_data()

main()