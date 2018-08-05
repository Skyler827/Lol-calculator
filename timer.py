import champion as c

def get_status(blue_champ, red_champ, time_elapsed):
    return {
        "time_passed": time_elapsed,
        "blue_champ_hp":blue_champ.hp,
        "red_champ_hp":red_champ.hp,
    }
def run_combat(blue_champion_name:str, red_champion_name:str):
    blue_side_champ = c.Champion(blue_champion_name)
    red_side_champ = c.Champion(red_champion_name)
    red_champ_must_wait = 0
    blue_champ_must_wait = 0
    time_elapsed = 0
    events = []
    while (blue_side_champ.hp > 0 and red_side_champ.hp > 0):
        this_event = {}
        this_event["old_status"] = get_status(blue_side_champ, red_side_champ, time_elapsed)
        if red_champ_must_wait < blue_champ_must_wait:
            # Time passes, then Red attacks Blue
            time_passes = red_champ_must_wait
            red_champ_must_wait = 0
            blue_champ_must_wait -= time_passes
            time_elapsed += time_passes
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            red_champ_must_wait += red_side_champ.get_attack_time()

        elif blue_champ_must_wait < red_champ_must_wait:
            # Time passes, then Blue attacks Red
            time_passes = blue_champ_must_wait
            blue_champ_must_wait = 0
            red_champ_must_wait -= time_passes
            time_elapsed += time_passes
            this_event["blue_attack"] = blue_side_champ.basic_attack(red_side_champ)
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait == 0:
            #Both may attack, no time passes
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            red_champ_must_wait += red_side_champ.get_attack_time()
            this_event["blue_attack"] = blue_side_champ.basic_attack(red_side_champ)
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait > 0:
            red_champ_must_wait = 0
            blue_champ_must_wait = 0
            time_elapsed += blue_champ_must_wait
        else: raise Exception
        events.append(this_event)
    winner = None
    if red_side_champ.hp > 0:
        winner = red_side_champ
    elif blue_side_champ.hp > 0:
        winner = blue_side_champ
    else:
        pass
    return {
        "events": events,
        "winner": winner.name,
        "winner_hp":winner.hp
    }
def main():
    x = run_combat("Shyvana", "Darius")
    for i in x["events"]:
        print(i)
    print(x["winner"])
if __name__ == "__main__":
    main()
