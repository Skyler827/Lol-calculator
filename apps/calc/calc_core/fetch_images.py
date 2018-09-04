## fetches static images
import os
import urllib.request
import sqlite3
from functools import reduce

def splitpath(path, maxdepth=20):
    ( head, tail ) = os.path.split(path)
    return splitpath(head, maxdepth - 1) + [ tail ] \
        if maxdepth and head and head != path \
        else [ head or tail ]

latest_patch = "8.16.1"
this_folder = os.path.dirname(os.path.realpath(__file__))
app_folder = os.path.split(this_folder)[0]
static_foler = os.path.join(app_folder, "static")
# project root is the third parent of the static folder:
project_root_folder = os.path.sep.join(splitpath(static_foler)[:-3])[1:]
print(project_root_folder)

def load_champ_images(patch):
    db_file_path = os.path.join(project_root_folder, "data", patch, "league_data.db")
    print(db_file_path)
    print("os.path.exists(db_file_path): "+str(os.path.exists(db_file_path)))
    conn = sqlite3.connect(os.path.join(project_root_folder, "data", patch, "league_data.db"))
    cur = conn.cursor()
    cur.execute("SELECT id FROM champions")
    champ_ascii_names = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    champs_whose_img_exist = 0
    for champ_name in champ_ascii_names:
        file_path = os.path.join(static_foler, "calc", "img", "champ_square", champ_name+".png")
        if os.path.exists(file_path):
            champs_whose_img_exist += 1
            continue
        url = f"http://ddragon.leagueoflegends.com/cdn/{patch}/img/champion/{champ_name}.png"
        response = urllib.request.urlopen(url)
        image_file = open(file_path, mode='wb')
        image_file.write(response.read())
    if champs_whose_img_exist > 0:
        print(f"Images for {champs_whose_img_exist} champions already exist, skipping downloads")

def load_item_images(patch):
    conn = sqlite3.connect(os.path.join(project_root_folder, "data", patch, "league_data.db"))
    cur = conn.cursor()
    cur.execute("SELECT id FROM items")
    item_ascii_names = cur.fetchall()
    cur.close()
    conn.close()
    items_whose_img_exist = 0
    for item_name in item_ascii_names:
        file_path = os.path.join(static_foler, "calc", "img", "items", str(item_name[0])+".png")
        if os.path.exists(file_path):
            items_whose_img_exist += 1
            continue
        url = f"http://ddragon.leagueoflegends.com/cdn/{patch}/img/item/{str(item_name[0])}.png"
        response = urllib.request.urlopen(url)
        image_file = open(file_path, mode='wb')
        print("downloading "+url)
        image_file.write(response.read())
    print("done")

def load_rune_images():
    pass

def load_summoner_spell_images():
    pass

def load_champion_spell_images():
    pass
def main():
    load_champ_images(latest_patch)
    load_item_images(latest_patch)
if __name__ == "__main__":
    main()