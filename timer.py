import champion as c



def log_status(champ_1, champ_2, time_elapsed):
    print(f"{round(time_elapsed)} seconds passed, {champ_1.name} has {round(champ_1.hp)} HP, while {champ_2.name} has {round(champ_2.hp)} HP.")
def main():
    leona = c.Champion("Leona")
    master_yi = c.Champion("Master Yi")
    master_yi_must_wait = 0
    leona_must_wait = 0
    time_elapsed = 0
    while (leona.hp > 0 and master_yi.hp > 0):
        log_status(leona, master_yi, time_elapsed)
        if master_yi_must_wait < leona_must_wait:
            # Time passes, then Yi attacks Leona
            time_passes = master_yi_must_wait
            master_yi_must_wait = 0
            leona_must_wait -= time_passes
            time_elapsed += time_passes
            print("Yi attacks!")
            master_yi.basic_attack(leona)
            master_yi_must_wait += master_yi.get_attack_time()

        elif leona_must_wait < master_yi_must_wait:
            # Time passes, then Leona attacks Yi
            time_passes = leona_must_wait
            leona_must_wait = 0
            master_yi_must_wait -= time_passes
            time_elapsed += time_passes
            print("Leona Attacks!")
            leona.basic_attack(master_yi)
            leona_must_wait += leona.get_attack_time()
        elif leona_must_wait == master_yi_must_wait == 0:
            #Both may attack, no time passes
            print("Yi Attacks!")
            master_yi.basic_attack(leona)
            master_yi_must_wait += master_yi.get_attack_time()
            print("Leona Attacks!")
            leona.basic_attack(master_yi)
            leona_must_wait += leona.get_attack_time()
        elif leona_must_wait == master_yi_must_wait > 0:
            master_yi_must_wait = 0
            leona_must_wait = 0
        else: raise Exception
    if master_yi.hp > 0:
        print(f"Master Yi won, with {master_yi.hp} HP to spare")
    elif leona.hp > 0:
        print(f"Leona won, with {leona.hp} HP to spare")
    else:
        print("both of their HP went to 0 at the same time")
main()