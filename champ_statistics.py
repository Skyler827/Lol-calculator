from enum import Enum, auto
from typing import Union

# statistics that can be modified by items, spell effects, buffs, debuffs, or runes:
class ChampStatistic(Enum):
    # Offensive, other than lifesteal/drain (see below):
    ATTACK_DAMAGE = auto() #many items
    ATTACK_DAMAGE_BONUS_PERCENT = auto() #jhin passive, infernal dragon
    ATTACK_SPEED_PERCENT = auto() #many items
    ABILITY_POWER = auto() #many items
    ABILITY_POWER_PERCENT = auto() #deathcap, infernal dragon, ryze passive
    CRIT_CHANCE = auto() #crit items
    CRIT_DAMAGE = auto() #jhin/yasuo/ashe/shaco passives, fiora bladework

    # Defensive:
    HP = auto() #many items
    HP_BONUS_PERCENT = auto() #stoneplate active, several abilities
    HP_REGEN = auto() #dorans shield, guardian horn, potions
    HP_REGEN_PERCENT = auto() #many items
    ARMOR = auto() #many items
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
    AUTOATTACK_CHAMPION_VAMP = auto()
    AUTOATTACK_NONCHAMPION_VAMP = auto()
    AUTOATTACK_CHAMPION_DRAIN = auto()
    AUTOATTACK_NONCHAMPION_DRAIN = auto()
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
    LIFE_STEAL = auto()
    pass
def get_stat_from_string(s: str) -> Union[ChampStatistic, Virtual_Champ_Statistic]:
    c = ChampStatistic

    if s=="": return c.ATTACK_DAMAGE
    
    # # Offensive, other than lifesteal/drain (see below):
    # ATTACK_DAMAGE = auto()
    elif s=="FlatPhysicalDamageMod": return c.ATTACK_DAMAGE
    # ATTACK_DAMAGE_BONUS_PERCENT = auto()
    elif s=="PercentPhysicalDamageMod": return c.ATTACK_DAMAGE_BONUS_PERCENT
    # ATTACK_SPEED_PERCENT = auto()
    elif s=="PercentAttackSpeedMod": return c.ATTACK_SPEED_PERCENT
    # ABILITY_POWER = auto()
    elif s=="FlatMagicDamageMod": return c.ABILITY_POWER
    # ABILITY_POWER_PERCENT = auto()
    elif s=="PercentMagicDamageMod": return c.ABILITY_POWER_PERCENT
    # CRIT_CHANCE = auto()
    elif s=="FlatCritChanceMod": return c.CRIT_CHANCE
    # CRIT_DAMAGE = auto()
    elif s=="CritDamageMod": return c.CRIT_DAMAGE
    
    # # Defensive:
    # HP = auto()
    elif s=="FlatHPPoolMod": return c.HP
    # HP_BONUS_PERCENT = auto()
    elif s=="PercentHPPoolMod": return c.HP_BONUS_PERCENT
    # HP_REGEN = auto()
    elif s=="FlatHpRegenMod": return c.HP_REGEN
    # HP_REGEN_PERCENT = auto()
    elif s=="PercentHpRegenMod": return c.HP_REGEN_PERCENT
    # ARMOR = auto()
    elif s=="FlatArmorMod": return c.ARMOR
    # ARMOR_PERCENT = auto()
    elif s=="PercentArmorMod": return c.ARMOR_PERCENT
    # MAGIC_RESIST = auto()
    elif s=="FlatSpellBlockMod": return c.MAGIC_RESIST
    # TENACITY = auto()
    elif s=="Tenacity": return c.TENACITY
    # SLOW_RESIST = auto()
    elif s=="SlowResist": return c.SLOW_RESIST

    # # Utility:
    # COOLDOWN_REDUCTION = auto()
    elif s=="CooldownMod": return c.COOLDOWN_REDUCTION
    # MAX_COOLDOWN_REDUCTION = auto()
    elif s=="MaxCooldownMod": return c.MAX_COOLDOWN_REDUCTION
    # MANA = auto()
    elif s=="FlatMPPoolMod": return c.MANA
    # MANA_REGEN = auto()
    elif s=="FlatMPPoolRegenMod": return c.MANA_REGEN
    # MANA_REGEN_PERCENT = auto()
    elif s=="PercentMPPoolRegenMod": return c.MANA_REGEN_PERCENT
    # MANA_REGEN_IN_JUNGLE = auto()
    # ENERGY_REGEN = auto()
    elif s=="FlatEnergyPoolRegenMod": return c.ENERGY_REGEN
    # ENERGY_REGEN_PERCENT = auto()
    # HEAL_AND_SHIELD_POWER = auto()
    # MOVE_SPEED_FLAT = auto()
    elif s=="FlatMovementSpeedMod": return c.MOVE_SPEED_FLAT
    # MOVE_SPEED_PERCENT = auto()
    # ATTACK_RANGE = auto()
    # ATTACK_RANGE_PERCENT = auto()
    # GOLD_GENERATION = auto()

    # # Lifesteal and spell vamp
    # ## (Vamp and drain are distinct because drain benefits from heal power,
    # ## while vamp does not)
    # # Autoattacks:
    # AUTOATTACK_VAMP = auto()
    # AUTOATTACK_DRAIN = auto()
    # #Physical spell vamp:
    # PHYSICAL_TARGETED_CHAMPION_SPELL_VAMP = auto()
    # PHYSICAL_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    # PHYSICAL_AOE_CHAMPION_SPELL_VAMP = auto()
    # PHYSICAL_AOE_NONCHAMPION_SPELL_VAMP = auto()
    # PHYSICAL_ONHIT_VAMP = auto()
    # #Physical spell drain:
    # PHYSICAL_TARGETED_CHAMPION_DRAIN = auto()
    # PHYSICAL_TARGETED_NONCHAMPION_DRAIN = auto()
    # PHYSICAL_AOE_CHAMPION_DRAIN = auto()
    # PHYSICAL_AOE_NONCHAMPION_DRAIN = auto()
    # PHYSICAL_ONHIT_DRAIN = auto()
    # #Magical spell vamp:
    # MAGICAL_TARGETED_CHAMPION_SPELL_VAMP = auto()
    # MAGICAL_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    # MAGICAL_AOE_CHAMPION_SPELL_VAMP = auto()
    # MAGICAL_AOE_NONCHAMPION_SPELL_VAMP = auto()
    # MAGICAL_ONHIT_VAMP = auto()
    # #Magical spell drain:
    # MAGICAL_TARGETED_CHAMPION_SPELL_DRAIN = auto()
    # MAGICAL_TARGETED_NONCHAMPION_SPELL_DRAIN = auto()
    # MAGICAL_AOE_CHAMPION_SPELL_DRAIN = auto()
    # MAGICAL_AOE_NONCHAMPION_SPELL_DRAIN = auto()
    # MAGICAL_ONHIT_DRAIN = auto()
    # #True spell vamp:
    # TRUE_TARGETED_CHAMPION_SPELL_VAMP = auto()
    # TRUE_TARGETED_NONCHAMPION_SPELL_VAMP = auto()
    # TRUE_AOE_CHAMPION_SPELL_VAMP = auto()
    # TRUE_AOE_NONCHAMPION_SPELL_VAMP = auto()
    # TRUE_ONHIT_VAMP = auto()
    # #True spell drain:
    # TRUE_TARGETED_CHAMPION_SPELL_DRAIN = auto()
    # TRUE_TARGETED_NONCHAMPION_SPELL_DRAIN = auto()
    # TRUE_AOE_CHAMPION_SPELL_DRAIN = auto()
    # TRUE_AOE_NONCHAMPION_SPELL_DRAIN = auto()
    # TRUE_ONHIT_DRAIN = auto()
    else: return c.ATTACK_DAMAGE
