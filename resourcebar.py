from enum import Enum, auto

class ResourceBarType(Enum): 
    MANA = auto() # most champions
    ENERGY = auto() #Zed, Shen, Lee Sin, Kennen, Akali
    FEROCITY = auto() #Rengar
    FURY = auto() #Renekton, Tryndamere, Rek'Sai, Shyvana
    RAGE = auto() # Gnar
    COURAGE = auto() #Kled
    HEAT = auto() #Rumble
    BLOODWELL = auto() #Aatrox
    SHIELD = auto() #Mordekaiser
    BLOODTHIRST = auto() #Vladimir
    FLOW = auto() #Yasuo
    NO_BAR = auto() # Mundo, Garen, Katarina, Zac, Riven
def resourcebar_from_text(type: str) -> ResourceBarType:
    if type == "Mana": return ResourceBarType.MANA
    elif type == "Energy": return ResourceBarType.ENERGY
    elif type == "Ferocity": return ResourceBarType.FEROCITY
    elif type == "Fury": return ResourceBarType.FURY
    elif type == "Rage": return ResourceBarType.RAGE
    elif type == "Courage": return ResourceBarType.COURAGE
    elif type == "Heat": return ResourceBarType.HEAT
    elif type == "Blood Well": return ResourceBarType.BLOODWELL
    elif type == "Shield": return ResourceBarType.SHIELD
    elif type == "Bloodthirst": return ResourceBarType.BLOODTHIRST
    elif type == "Flow": return ResourceBarType.FLOW
    elif type == "None": return ResourceBarType.NO_BAR 
