import champion as c

def get_status(blue_champ:c.Champion, red_champ:c.Champion, time_elapsed:float):
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
    initial_status = get_status(blue_side_champ, red_side_champ, time_elapsed)
    events = []
    blue_champ_hp = []
    red_champ_hp = []
    dt = 0.001
    while (blue_side_champ.hp > 0 and red_side_champ.hp > 0):
        this_event = {}
        if red_champ_must_wait < blue_champ_must_wait:
            # Time passes, then Red attacks Blue
            time_passes = red_champ_must_wait
            red_champ_must_wait = 0
            blue_champ_must_wait -= time_passes
            time_elapsed += time_passes
            blue_champ_hp.append({"x":time_elapsed-dt, "y":blue_side_champ.hp})
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            red_champ_must_wait += red_side_champ.get_attack_time()
        elif blue_champ_must_wait < red_champ_must_wait:
            # Time passes, then Blue attacks Red
            time_passes = blue_champ_must_wait
            blue_champ_must_wait = 0
            red_champ_must_wait -= time_passes
            time_elapsed += time_passes
            red_champ_hp.append({"x": time_elapsed-dt, "y":red_side_champ.hp})
            this_event["blue_attack"] = blue_side_champ.basic_attack(red_side_champ)
            red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait == 0:
            # No time passes, Both may attack
            # First Red attacks blue:
            blue_champ_hp.append({"x":time_elapsed-dt, "y":blue_side_champ.hp})
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            red_champ_must_wait += red_side_champ.get_attack_time()
            
            # Then blue attacks red:
            red_champ_hp.append({"x": time_elapsed-dt, "y":red_side_champ.hp})
            this_event["blue_attack"] = blue_side_champ.basic_attack(red_side_champ)
            red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait > 0:
            # Both wait for a time
            time_elapsed += blue_champ_must_wait
            red_champ_must_wait = 0
            blue_champ_must_wait = 0
        else: raise Exception
        this_event["new_status"] = get_status(blue_side_champ, red_side_champ, time_elapsed)
        events.append(this_event)
    winner = None
    if red_side_champ.hp > 0:
        winner = red_side_champ
    elif blue_side_champ.hp > 0:
        winner = blue_side_champ
    elif blue_side_champ.hp == red_side_champ.hp == 0:
        pass
    return {
        "blue_champ":blue_champion_name,
        "red_champ": red_champion_name,
        "initial": initial_status,
        "events": events,
        "winner": winner.name if winner else "draw",
        "winner_hp": winner.hp if winner else 0,
        "blue_champ_hp": blue_champ_hp,
        "red_champ_hp": red_champ_hp
    }
def main():
    x = run_combat("Ahri", "Veigar")
    print(f"It's {x['blue_champ']} on blue vs {x['red_champ']} on red.")
    print(x["initial"])
    for i in x["events"]:
        print(i)
    print(x["winner"] + " wins!")
if __name__ == "__main__":
    main()
