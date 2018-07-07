from enum import Enum, auto
class ChampStatistic(Enum):
    # statistics that can be modified by items, spell effects, buffs, or debuffs
    HP = auto()
    HP_BONUS_PERCENT = auto()
    MANA = auto()
    MOVE_SPEED_FLAT = auto()
    MOVE_SPEED_PERCENT = auto()
    TENACITY = auto()
    SLOW_RESIST = auto()
    ARMOR = auto()
    ARMOR_PERCENT = auto()
    MAGIC_RESIST = auto()
    ATTACK_RANGE = auto()
    ATTACK_RANGE_PERCENT = auto()
    HP_REGEN = auto()
    HP_REGEN_PERCENT = auto()
    MANA_REGEN = auto()
    MANA_REGEN_PERCENT = auto()
    CRIT_CHANCE = auto()
    CRIT_DAMAGE = auto()
    ATTACK_DAMAGE = auto()
    ATTACK_SPEED_PERCENT = auto()
    ABILITY_POWER = auto()
    ABILITY_POWER_PERCENT = auto()
    HEAL_AND_SHIELD_POWER = auto()

    # _____Lifesteal and spell vamp___________
    # Vamp and drain are distinct because drain benefits from heal power,
    # while vamp does not
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