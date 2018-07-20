from enum import Enum, auto
from typing import Union

# statistics that can be modified by items, spell effects, buffs, debuffs, or runes:
class ChampStatistic(Enum):
    # Offensive, other than lifesteal/drain (see below):
    ATTACK_DAMAGE = auto()
    ATTACK_DAMAGE_BONUS_PERCENT = auto()
    ATTACK_SPEED_PERCENT = auto()
    ABILITY_POWER = auto()
    ABILITY_POWER_PERCENT = auto()
    CRIT_CHANCE = auto()
    CRIT_DAMAGE = auto()

    # Defensive:
    HP = auto()
    HP_BONUS_PERCENT = auto()
    HP_REGEN = auto()
    HP_REGEN_PERCENT = auto()
    ARMOR = auto()
    ARMOR_PERCENT = auto()
    MAGIC_RESIST = auto()
    TENACITY = auto()
    SLOW_RESIST = auto()

    # Utility:
    COOLDOWN_REDUCTION = auto()
    MAX_COOLDOWN_REDUCTION = auto()
    MANA = auto()
    MANA_REGEN = auto()
    MANA_REGEN_PERCENT = auto()
    MANA_REGEN_IN_JUNGLE = auto()
    ENERGY_REGEN = auto()
    ENERGY_REGEN_PERCENT = auto()
    HEAL_AND_SHIELD_POWER = auto()
    MOVE_SPEED_FLAT = auto()
    MOVE_SPEED_PERCENT = auto()
    ATTACK_RANGE = auto()
    ATTACK_RANGE_PERCENT = auto()
    GOLD_GENERATION = auto()

    # Lifesteal and spell vamp
    ## (Vamp and drain are distinct because drain benefits from heal power,
    ## while vamp does not)
    # Autoattacks:
    AUTOATTACK_VAMP = auto()
    AUTOATTACK_DRAIN = auto()
    #Physical spell vamp:
    PHYSICAL_TARGETED_CHAMPION_SPELL_VAMP = auto()
    PHYSICAL_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    PHYSICAL_AOE_CHAMPION_SPELL_VAMP = auto()
    PHYSICAL_AOE_NONCHAMPION_SPELL_VAMP = auto()
    PHYSICAL_ONHIT_VAMP = auto()
    #Physical spell drain:
    PHYSICAL_TARGETED_CHAMPION_DRAIN = auto()
    PHYSICAL_TARGETED_NONCHAMPION_DRAIN = auto()
    PHYSICAL_AOE_CHAMPION_DRAIN = auto()
    PHYSICAL_AOE_NONCHAMPION_DRAIN = auto()
    PHYSICAL_ONHIT_DRAIN = auto()
    #Magical spell vamp:
    MAGICAL_TARGETED_CHAMPION_SPELL_VAMP = auto()
    MAGICAL_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    MAGICAL_AOE_CHAMPION_SPELL_VAMP = auto()
    MAGICAL_AOE_NONCHAMPION_SPELL_VAMP = auto()
    MAGICAL_ONHIT_VAMP = auto()
    #Magical spell drain:
    MAGICAL_TARGETED_CHAMPION_SPELL_DRAIN = auto()
    MAGICAL_TARGETED_NONCHAMPION_SPELL_DRAIN = auto()
    MAGICAL_AOE_CHAMPION_SPELL_DRAIN = auto()
    MAGICAL_AOE_NONCHAMPION_SPELL_DRAIN = auto()
    MAGICAL_ONHIT_DRAIN = auto()
    #True spell vamp:
    TRUE_TARGETED_CHAMPION_SPELL_VAMP = auto()
    TRUE_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    TRUE_AOE_CHAMPION_SPELL_VAMP = auto()
    TRUE_AOE_NONCHAMPION_SPELL_VAMP = auto()
    TRUE_ONHIT_VAMP = auto()
    #True spell drain:
    TRUE_TARGETED_CHAMPION_SPELL_DRAIN = auto()
    TRUE_TARGETED_NONCHAMPION_SPELL_DRAIN = auto()
    TRUE_AOE_CHAMPION_SPELL_DRAIN = auto()
    TRUE_AOE_NONCHAMPION_SPELL_DRAIN = auto()
    TRUE_ONHIT_DRAIN = auto()
class Virtual_Champ_Statistic(Enum):
    pass
def get_stat_from_string(s: str) -> Union[ChampStatistic, Virtual_Champ_Statistic]:
    c = ChampStatistic

    if s=="FlatMovementSpeedMod": return c.MOVE_SPEED_FLAT
    elif s=="FlatHPPoolMod": return c.HP
    elif s=="FlatMagicDamageMod": return c.ABILITY_POWER
    elif s=="FlatMPPoolMod": return c.MANA
    elif s=="FlatArmorMod": return c.ARMOR
    elif s=="FlatSpellBlockMod": return c.MAGIC_RESIST
    elif s=="FlatPhysicalDamageMod": return c.ATTACK_DAMAGE
    elif s=="Effect4Amount": return c.MANA_REGEN_IN_JUNGLE
    return c.ATTACK_DAMAGE
