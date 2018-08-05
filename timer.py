import champion as c

def log_status(champ_1, champ_2, time_elapsed):
    print(f"{round(time_elapsed)} seconds passed, {champ_1.name} has {round(champ_1.hp)} HP, while {champ_2.name} has {round(champ_2.hp)} HP.")
def run_combat(blue_champion_name:str, red_champion_name:str):
    blue_side_champ = c.Champion(blue_champion_name)
    red_side_champ = c.Champion(red_champion_name)
    red_champ_must_wait = 0
    blue_champ_must_wait = 0
    time_elapsed = 0
    
    initial = {

    }
    events = []
    
    while (blue_side_champ.hp > 0 and red_side_champ.hp > 0):
        log_status(blue_side_champ, red_side_champ, time_elapsed)
        if red_champ_must_wait < blue_champ_must_wait:
            # Time passes, then Red attacks Blue
            time_passes = red_champ_must_wait
            red_champ_must_wait = 0
            blue_champ_must_wait -= time_passes
            time_elapsed += time_passes
            damage_done = red_side_champ.basic_attack(blue_side_champ)
            print(f"{red_side_champ.name} attacks, dealing {damage_done} damage!")
            red_champ_must_wait += red_side_champ.get_attack_time()

        elif blue_champ_must_wait < red_champ_must_wait:
            # Time passes, then Blue attacks Red
            time_passes = blue_champ_must_wait
            blue_champ_must_wait = 0
            red_champ_must_wait -= time_passes
            time_elapsed += time_passes
            damage_done = blue_side_champ.basic_attack(red_side_champ)
            print(f"{blue_side_champ.name} Attacks, dealing {damage_done} damage!")
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait == 0:
            #Both may attack, no time passes
            damage_on_blue = red_side_champ.basic_attack(blue_side_champ)
            print(f"{red_side_champ.name} Attack, dealing {damage_on_blue} damage!")
            red_champ_must_wait += red_side_champ.get_attack_time()
            damage_on_red = blue_side_champ.basic_attack(red_side_champ)
            print(f"{blue_side_champ.name} Attacks, dealing {damage_on_red} damage!")
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait > 0:
            red_champ_must_wait = 0
            blue_champ_must_wait = 0
            time_elapsed += blue_champ_must_wait
        else: raise Exception
    if red_side_champ.hp > 0:
        print(f"{red_side_champ.name} wins, with {red_side_champ.hp} HP to spare")
    elif blue_side_champ.hp > 0:
        print(f"{blue_side_champ.name} wins, with {blue_side_champ.hp} HP to spare")
    else:
        print("both of their HP went to 0 at the same time")
    return {
        "in": initial,
        "events": events,
        "winner": blue_side_champ.name,
        "winner_hp":blue_side_champ.hp
    }
def main():
    run_combat("Sona", "Lulu")
if __name__ == "__main__":
    main()
