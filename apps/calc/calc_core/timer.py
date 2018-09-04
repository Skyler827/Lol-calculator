from typing import List, Dict
import champion as c

def get_status(blue_champ:c.Champion, red_champ:c.Champion, time_elapsed:float) ->Dict:
    return {
        "time_passed": time_elapsed,
        "blue_champ_hp":blue_champ.hp,
        "red_champ_hp":red_champ.hp,
    }
def output_stats(champ:c.Champion) -> Dict:
    return {
        "AD": champ.get_attackdamage(),
        "AP": champ.get_abilitypower(),
        "AS": 1/champ.get_attack_time(),
        "CDR":champ.cooldown_reduction_spells,
        "Armor":champ.get_armor(),
        "MR": champ.get_magic_resist(),
        "AttackRange": champ.get_attack_range(),
        "MS": champ.get_movespeed()
    }
def run_combat(blue_champion_name:str="Ahri", blue_champ_level:str='1', blue_champ_items:List[str]=[], 
        red_champion_name:str="Veigar", red_champ_level:str='1', red_champ_items:List[str]=[]):
    ## declaration:
    blue_side_champ = c.Champion(blue_champion_name)
    red_side_champ = c.Champion(red_champion_name)
    ## levels
    blue_side_champ.set_level(blue_champ_level)
    red_side_champ.set_level(red_champ_level)

    ## items
    for item_id in blue_champ_items:
        item_obj:c.Item = c.load_item(item_id)
        for stat, mod in item_obj.attribute_modifiers:
            blue_side_champ.add_stat_mod(stat, mod)
    for item_id in red_champ_items:
        for stat, mod in c.load_item(item_id).attribute_modifiers:
            red_side_champ.add_stat_mod(stat, mod)

    red_champ_must_wait:float = 0
    blue_champ_must_wait:float = 0
    time_elapsed:float = 0
    initial_status = get_status(blue_side_champ, red_side_champ, time_elapsed)
    events:List[Dict] = []
    blue_champ_hp:List[Dict] = []
    red_champ_hp:List[Dict] = []
    while (blue_side_champ.hp > 0 and red_side_champ.hp > 0):
        this_event = {}
        if red_champ_must_wait < blue_champ_must_wait:
            # Time passes, then Red attacks Blue
            time_passes = red_champ_must_wait
            red_champ_must_wait = 0
            blue_champ_must_wait -= time_passes
            time_elapsed += time_passes
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            red_champ_must_wait += red_side_champ.get_attack_time()
        elif blue_champ_must_wait < red_champ_must_wait:
            # Time passes, then Blue attacks Red
            time_passes = blue_champ_must_wait
            blue_champ_must_wait = 0
            red_champ_must_wait -= time_passes
            time_elapsed += time_passes
            red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
            this_event["blue_attack"] = blue_side_champ.basic_attack(red_side_champ)
            red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
            blue_champ_must_wait += blue_side_champ.get_attack_time()
        elif blue_champ_must_wait == red_champ_must_wait == 0:
            # No time passes, Both may attack
            # First Red attacks blue:
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            this_event["red_attack"] = red_side_champ.basic_attack(blue_side_champ)
            blue_champ_hp.append({"x":time_elapsed, "y":blue_side_champ.hp})
            red_champ_must_wait += red_side_champ.get_attack_time()
            # Then blue attacks red:
            red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
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
        if time_elapsed > 60:
            break
    winner = None
    if red_side_champ.hp > 0:
        winner = red_side_champ
        red_champ_hp.append({"x": time_elapsed, "y":red_side_champ.hp})
        blue_champ_hp[-1]["y"] = 0
    elif blue_side_champ.hp > 0:
        winner = blue_side_champ
        blue_champ_hp.append({"x": time_elapsed, "y": blue_side_champ.hp})
        red_champ_hp[-1]["y"] = 0
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
