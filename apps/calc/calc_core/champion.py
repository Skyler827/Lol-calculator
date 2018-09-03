from typing import Dict, Tuple, List, IO, NamedTuple
from enum import Enum, auto
import math
import os.path
import json
import sqlite3
import abc
from collections import namedtuple
from champ_statistics import ChampStatistic, get_stat_from_string
from damage_type import DamageType
from damage_ratio import DamageRatio
from resourcebar import ResourceBarType, resourcebar_from_text
from initializedb import latest_patch, db_name

class Damage():
    def __init__(self, type:DamageType, ratio:DamageRatio=DamageRatio.FLAT, amount:float=0, pen_armor_percent:List[float]=[], 
    pen_lethality:float=0, pen_magic_flat:float=0, pen_magic_percent:List[float]=[]):
        self.pen_armor_percent: List[float] = pen_armor_percent
        self.pen_lethality: float = pen_lethality
        self.pen_magic_flat: float = pen_magic_flat
        self.pen_magic_percent: List[float] = pen_magic_percent
        self.type: DamageType = type
        self.amount: float = amount
        self.ratio = ratio
class AbstractMinion(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self, name:str):
        # static quantities:
        self.hp_base:float = 0
        self.hp_perlevel:float = 0
        self.hp_bonus:float = 0
        self.hp_bonus_percent:float = 0
        self.mp_base:float = 0
        self.mp_perlevel:float = 0
        self.mp_bonus:float = 0
        self.movespeed_base:float = 0
        self.movespeed_bonus_flat:float = 0
        self.movespeed_bonus_percent:float = 0
        self.armor_base:float = 0
        self.armor_perlevel:float = 0
        self.armor_bonus:float = 0
        self.armor_bonus_percent:float = 0
        self.armor_reduction_flat:float = 0
        self.armor_reduction_percent:float = 0
        self.spellblock_base:float = 0
        self.spellblock_perlevel:float = 0
        self.spellblock_bonus:float = 0
        self.spellblock_bonus_percent:float = 0
        self.spellblock_reduction_flat:float = 0
        self.spellblock_reduction_percent:float = 0
        self.attackrange:float = 0
        self.attackrange_bonus_percent:float = 0
        self.hpregen_base:float = 0
        self.hpregen_perlevel:float = 0
        self.hpregen_bonus_percent:float = 0
        self.mpregen_base:float = 0
        self.mpregen_perlevel:float = 0
        self.mpregen_bonus_percent:float = 0
        self.crit_base:float = 0
        self.crit_perlevel:float = 0
        self.crit_bonus:float = 0
        self.attackdamage_base:float = 0
        self.attackdamage_perlevel:float = 0
        self.attackdamage_bonus:float = 0
        self.attackspeed_offset:float = 0
        self.attackspeed_perlevel:float = 0
        self.abilitypower_flat:float = 0
        self.abilitypower_percent:float = 0

        # dynamic quantities:
        self.level: int = 1
        self.buffs = [ChampStatusModifier]
        self.debuffs = [ChampStatusModifier]
        self.hp:float = 0
        self.exp: int = 0
    def get_maxhp(self) -> float:
        return (self.hp_base + (self.level - 1) * self.hp_perlevel + self.hp_bonus) * self.hp_bonus_percent
    def get_maxmp(self) -> float:
        return self.mp_base + (self.level-1) * self.mp_perlevel
    def get_attackdamage(self) -> float:
        return self.attackdamage_base + (self.level-1) * self.attackdamage_perlevel
    def get_abilitypower(self) -> float:
        return self.abilitypower_flat * (1 + self.abilitypower_percent/100)
    def get_armor(self) -> float:
        x = self.armor_base
        x += self.armor_perlevel*self.level
        x += self.armor_bonus
        x *= (1+self.armor_bonus_percent/100)
        x -= self.armor_reduction_flat
        x *= (1- self.armor_reduction_percent)
        return x 
    def get_magic_resist(self) -> float:
        x = self.spellblock_base
        x += self.spellblock_perlevel*self.level
        x += self.spellblock_bonus
        x *= (1+self.spellblock_bonus_percent/100)
        x -= self.spellblock_reduction_flat
        x *= (1 - self.spellblock_reduction_percent)
        return x
    @abc.abstractmethod
    def take_damage(self, attack: Damage) -> float:
        pass
class ChampStatusModifier:
    def __init__(self, name:str, attribute_modifiers:Dict[ChampStatistic, int], condition):
        self.name = name
        self.attribute_modifiers = attribute_modifiers
class Buff(ChampStatusModifier):
    def __init__(self):
        super()
class Debuff(ChampStatusModifier):
    def __init__(self):
        super()
class onHitEffect():
    def __init__(self, type:DamageType, damageamount:float, damageRatio:DamageRatio, debuff:Debuff, origin:AbstractMinion):
        self.type:DamageType = type
        self.damageamount:float = damageamount
        self.damageRatio:DamageRatio = damageRatio
        self.debuff = debuff
        self.origin = origin
    def apply_effect(self, target):
        target
class Item:
    def __init__(self, attribute_modifiers:List[Tuple[ChampStatistic, float]], 
    unique_passives:List[Tuple[str,Tuple[ChampStatistic, int]]]=[], passive_effect:Buff=None):

        self.attribute_modifiers = attribute_modifiers
        self.unique_passives = unique_passives
        self.passive_effect = passive_effect
def load_item(item_id:str) -> Item:
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    sql = "SELECT champ_statistics.name AS stat, item_stats.mod AS mod FROM champ_statistics " + \
        "JOIN item_stats ON item_stats.stat=champ_statistics.id WHERE item_stats.item=:id"
    stats = c.execute(sql, {"id":item_id}).fetchall()
    attr:List[Tuple[ChampStatistic, float]] = list(map(lambda row: (eval("ChampStatistic."+row[0]), float(row[1])), stats))
    return Item(attribute_modifiers=attr)
class Tenacity_obj():
    """
    all values are unit fractions, such as 0.05 + 0.05 = 0.1 implies 90% CC duration
    """
    def __init__(self):
        self.elixirs_unflinching_ss_cd: float = 0
        self.merc_treads_steraks: float = 0
        self.garen_mundo_W_unflinching_10s_ss: float = 0
        self.other: float = 0
    def overall_cc_length(self) -> float:
        t1 = self.elixirs_unflinching_ss_cd
        t2 = self.merc_treads_steraks
        t3 = self.garen_mundo_W_unflinching_10s_ss
        t4 = self.other
        return (1-t1)*(1-t2)*(1-t3)*(1-t4)
class Champion(AbstractMinion):
    def __init__(self, name:str):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        r:sqlite3.Row = c.execute("SELECT * FROM champions WHERE id=:name OR name=:name", {"name":name}).fetchone()
        self.name = name
        self.bartype:ResourceBarType = resourcebar_from_text(r["partype"])

        # static quantities:
        # only change when an item/buff/debuff is applied or removed
        # Offensive
        self.attackdamage_base:float = r["attackdamage"]
        self.attackdamage_perlevel:float = r["attackdamageperlevel"]
        self.attackdamage_bonus:float = 0
        self.attackdamage_bonus_percent:float = 0

        self.attackspeed_offset:float = r["attackspeedoffset"]
        self.attackspeed_perlevel:float = r["attackspeedperlevel"]
        self.attackspeed_bonus_percent:float = 0

        self.attackrange:float = r["attackrange"]
        self.attackrange_bonus_flat: float = 0
        self.attackrange_bonus_percent:float = 0

        self.abilitypower_flat:float = 0
        self.abilitypower_percent:float = 0
        
        self.crit_base:float = r["crit"]
        self.crit_perlevel:float = r["critperlevel"]
        self.crit_bonus:float = 0
        self.crit_damage_modifier:float = 2

        self.pen_armor_percent:List[float] = []
        self.pen_lethality = 0

        self.pen_magic_flat = 0
        self.pen_magic_percent: List[float] = []

        # Defensive
        self.hp_base:float = r["hp"]
        self.hp_perlevel:float = r["hpperlevel"]
        self.hp_bonus:float = 0
        self.hp_bonus_percent:float = 0

        self.hpregen_base:float = r["hpregen"]
        self.hpregen_perlevel:float = r["hpregenperlevel"]
        self.hpregen_bonus_base:float = 0
        self.hpregen_bonus_percent:float = 0

        self.armor_base:float = r["armor"]
        self.armor_perlevel:float = r["armorperlevel"]
        self.armor_bonus:float = 0
        self.armor_bonus_percent:float = 0
        self.armor_reduction_flat:float = 0
        self.armor_reduction_percent:float = 0

        self.spellblock_base:float = r["spellblock"]
        self.spellblock_perlevel:float = ["spellblockperlevel"]
        self.spellblock_bonus:float = 0
        self.spellblock_bonus_percent:float = 0
        self.spellblock_reduction_flat:float = 0
        self.spellblock_reduction_percent:float = 0

        self.damagereduction_percent = 0
        
        # Utility
        self.mp_base:float = r["mp"]
        self.mp_perlevel:float = r["mpperlevel"]
        self.mp_bonus:float = 0

        self.mpregen_base:float = r["mpregen"]
        self.mpregen_perlevel:float = r["mpregenperlevel"]
        self.mpregen_bonus_flat:float = 0
        self.mpregen_bonus_percent:float = 0
        self.tooth:bool = False # Jungle item mana regen in jungle

        # cooldown reduction values are in terms of unit fractions, not percents
        self.cooldown_reduction_spells = 0
        self.cooldown_reduction_spells_max = 0.4
        self.cooldown_reduction_ultumate = 0 #stacks multiplicatevly with spell cdr, without regard to spell cdr cap
        self.cooldown_reduction_items = 0
        self.cooldown_reduction_summoners = 0
        
        self.movespeed_base:float = r["movespeed"]
        self.movespeed_bonus_flat:float = 0
        self.movespeed_bonus_percent:float = 0
        self.tenacity:Tenacity_obj = Tenacity_obj()
        self.slow_resist = 0

        #heal and shield power:
        self.heal_shield_power = 0
        self.health_restoration = 0 #spirit visage
        self.revitalize = 0 # revitalize rune
        self.grievous_wounds = 0
        self.gp5 = 0

        conn.commit()
        conn.close()

        # dynamic quantities:
        self.level: int = 1
        self.items: [Item] = []
        self.buffs: [Buff] = []
        self.debuffs: [Debuff] = []
        self.hp: float = self.get_maxhp()
        self.mp: float = self.get_maxmp()
        self.exp: int = 0
        self.gold: int = 0
        self.shield = []
        self.onHitEffects: List[onHitEffect] = []
        self.in_jungle:bool = False

    def get_maxhp(self) -> float:
        b = self.hp_base
        g = self.hp_perlevel
        n = self.level
        bonus = self.hp_bonus
        return b + g * (n-1) * (0.7025 + 0.0175 * (n-1)) + bonus
    def get_maxmp(self) -> float:
        b = self.mp_base
        g = self.mp_perlevel
        n = self.level
        bonus = self.mp_bonus if self.bartype == ResourceBarType.MANA else 0
        return b + g * (n-1) * (0.7025 + (n-1)) + bonus
    def get_attackdamage(self) -> float:
        b = self.attackdamage_base
        g = self.attackdamage_perlevel
        n = self.level
        bonus = self.attackdamage_bonus
        mult = self.attackdamage_bonus_percent
        return (b + g * (n-1) * (0.7025 + (n-1)) + bonus) * (1+mult)
    def get_abilitypower(self) -> float:
        return self.abilitypower_flat * (1 + self.abilitypower_percent)
    def get_attack_time(self) -> float:
        base_attack_speed = 0.625/(1+self.attackspeed_offset)
        l = self.level
        level_bonus = self.attackspeed_perlevel/100 * ((7/400)*(l**2)+(267/400)*(l-1))
        total_attack_speed = base_attack_speed * (1+level_bonus+self.attackspeed_bonus_percent)
        return 1/total_attack_speed
    def get_attack_range(self) -> float:
        return (self.attackrange + self.attackrange_bonus_flat) * (1+self.attackrange_bonus_percent)
    def get_movespeed() -> float:
        return (self.movespeed_base + self.movespeed_bonus_flat) * (1+self.movespeed_bonus_percent)
    def gain_exp(self, exp_amount: int) -> None:
        assert(exp_amount > 0)
        self.exp += exp_amount
        should_be_level = math.floor(50*self.exp**2+130*self.exp-180)
        while (self.level < should_be_level):
            self.level_up()
        assert(self.level == should_be_level)
    def set_level(self, level:str):
        self.level = int(level)
        self.hp = self.get_maxhp()
    def level_up(self) -> None:
        hp_percent = self.hp / self.get_maxhp()
        self.level += 1
        self.hp = hp_percent * self.get_maxhp()
    def add_stat_mod(self, stat:ChampStatistic, mod: float):
        #Offensive:
        if stat == ChampStatistic.ATTACK_DAMAGE:
            self.attackdamage_bonus += mod
        elif stat == ChampStatistic.ATTACK_DAMAGE_BONUS_PERCENT:
            self.attackdamage_bonus_percent += mod
        elif stat == ChampStatistic.ATTACK_SPEED_PERCENT:
            self.attackrange_bonus_percent += mod
        elif stat == ChampStatistic.ABILITY_POWER:
            self.abilitypower_flat += mod
        elif stat == ChampStatistic.ABILITY_POWER_PERCENT:
            self.abilitypower_percent += mod
        elif stat == ChampStatistic.CRIT_CHANCE: #crit items
            self.crit_bonus += mod
        elif stat == ChampStatistic.CRIT_DAMAGE: #jhin/yasuo/shaco passives, fiora bladework
            self.crit_damage_modifier += mod
        
        # Defensive:
        elif stat == ChampStatistic.HP: #many items
            self.hp_bonus += mod
        elif stat == ChampStatistic.HP_BONUS_PERCENT: #stoneplate active, several abilities
            self.hp_bonus_percent
        elif stat == ChampStatistic.HP_REGEN: #dorans shield, guardian horn, potions
            self.hpregen_bonus_base += mod
        elif stat == ChampStatistic.HP_REGEN_PERCENT: #many items
            self.hpregen_bonus_percent
        elif stat == ChampStatistic.ARMOR: #many items
            self.armor_bonus += mod
        elif stat == ChampStatistic.ARMOR_PERCENT:
            self.armor_bonus_percent += mod 
        elif stat == ChampStatistic.MAGIC_RESIST:
            self.spellblock_bonus += mod
        elif stat == ChampStatistic.TENACITY:
            self.tenacity += mod
        elif stat == ChampStatistic.SLOW_RESIST:
            self.slow_resist += mod
        
        # Utility:
        elif stat == ChampStatistic.COOLDOWN_REDUCTION:
            self.cooldown_reduction_spells += mod
        elif stat == ChampStatistic.MAX_COOLDOWN_REDUCTION:
            self.cooldown_reduction_spells_max += mod
        elif stat == ChampStatistic.MANA:
            if self.bartype == ResourceBarType.MANA:
                self.mp_bonus += mod
        elif stat == ChampStatistic.MANA_REGEN:
            if self.bartype == ResourceBarType.MANA:
                self.mpregen_bonus_flat += mod
        elif stat == ChampStatistic.MANA_REGEN_PERCENT:
            if self.bartype == ResourceBarType.MANA:
                self.mpregen_bonus_percent += mod
        elif stat == ChampStatistic.MANA_REGEN_IN_JUNGLE:
            if self.bartype == ResourceBarType.MANA:
                self.tooth = True
        elif stat == ChampStatistic.ENERGY_REGEN:
            if self.bartype == ResourceBarType.ENERGY:
                self.mpregen_bonus_flat += mod
        elif stat == ChampStatistic.ENERGY_REGEN_PERCENT:
            if self.bartype == ResourceBarType.ENERGY:
                self.mpregen_bonus_percent += mod
        elif stat == ChampStatistic.HEAL_AND_SHIELD_POWER:
            self.heal_shield_power += mod
        elif stat == ChampStatistic.MOVE_SPEED_FLAT:
            self.movespeed_bonus_flat += mod
        elif stat == ChampStatistic.MOVE_SPEED_PERCENT:
            self.movespeed_bonus_percent += mod
        elif stat == ChampStatistic.ATTACK_RANGE:
            self.attackrange_bonus_flat += mod
        elif stat == ChampStatistic.ATTACK_RANGE_PERCENT:
            self.attackrange_bonus_percent
        elif stat == ChampStatistic.GOLD_GENERATION:
            self.gp5 += mod
    def add_item(self, item:Item):
        pass
    def take_damage(self, attack: Damage) -> float:
        if attack.type == DamageType.PHYSICAL:
            armor = self.get_armor()
            # Armor penetration stacks multiplicatively, so we combine with a loop:
            for i in attack.pen_armor_percent:
                armor *= 1-i/100
            armor -= attack.pen_lethality * (0.6 + 0.4 * self.level/18)
            damage = (attack.amount) * (100/(armor+100))
            damage *= (1-self.damagereduction_percent/100)
            self.hp -=  damage
            if self.hp <= 0:
                self.die()
            return damage
        elif attack.type == DamageType.MAGICAL:
            magic_resist = self.get_magic_resist()
            for i in attack.pen_magic_percent:
                magic_resist *= 1 - i/100
            magic_resist -= attack.pen_magic_flat
            damage = (attack.amount) * (100/magic_resist)
            damage *= (1-self.damagereduction_percent/100)
            self.hp -=  damage
            if self.hp <= 0:
                self.die()
            return damage
        elif attack.type in DamageType.TRUE or DamageType.PURE:
            self.hp -= attack.amount
            return damage
        else:
            raise Exception
    def basic_attack(self, target: AbstractMinion) -> float:
        damage_done = 0
        attack = Damage(DamageType.PHYSICAL, amount=self.get_attackdamage(), \
            pen_armor_percent=self.pen_armor_percent, pen_lethality=self.pen_lethality)
        damage_done += target.take_damage(attack)
        for effect in self.onHitEffects:
            damage_done += target.take_damage(effect.getDamage(effect, target))
        return damage_done
    def Spell1(self, target):
        pass
    def Spell2(self, target):
        pass
    def Spell3(self, target):
        pass
    def Spell4(self, target):
        pass
    def die(self) -> None:
        pass
