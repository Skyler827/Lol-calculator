from typing import Dict, Tuple, List, IO
from enum import Enum, auto
import math
import os.path
import json
import sqlite3
import abc
from champ_statistics import ChampStatistic
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
    def __init__(self, attribute_modifiers:List[Tuple[ChampStatistic, float]], unique_passives:List[Tuple[str, Tuple[ChampStatistic, int]]], passive_effect:Buff):
        self.attribute_modifiers = attribute_modifiers
        self.unique_passives = unique_passives
        self.passive_effect = passive_effect
class Champion(AbstractMinion):
    def __init__(self, name:str):
        print(db_name)
        print(name)
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        r:sqlite3.Row = c.execute("SELECT * FROM champions WHERE id=:name OR name=:name", {"name":name}).fetchone()
        # static quantities:
        self.name = name
        self.hp_base = r["hp"]
        self.hp_perlevel = r["hpperlevel"]
        self.hp_bonus = 0
        self.hp_bonus_percent = 0
        self.mp_base = r["mp"]
        self.mp_perlevel = r["mpperlevel"]
        self.mp_bonus = 0
        self.bartype:ResourceBarType = resourcebar_from_text(r["partype"])
        self.movespeed_base = r["movespeed"]
        self.movespeed_bonus_flat = 0
        self.movespeed_bonus_percent = 0
        self.armor_base = r["armor"]
        self.armor_perlevel = r["armorperlevel"]
        self.armor_bonus = 0
        self.armor_bonus_percent = 0
        self.armor_reduction_flat = 0
        self.armor_reduction_percent = 0
        self.spellblock_base = r["spellblock"]
        self.spellblock_perlevel = ["spellblockperlevel"]
        self.spellblock_bonus = 0
        self.spellblock_bonus_percent = 0
        self.spellblock_reduction_flat = 0
        self.spellblock_reduction_percent = 0
        self.attackrange = r["attackrange"]
        self.attackrange_bonus_percent = 0
        self.hpregen_base = r["hpregen"]
        self.hpregen_perlevel = r["hpregenperlevel"]
        self.hpregen_bonus_percent = 0
        self.mpregen_base = r["mpregen"]
        self.mpregen_perlevel = r["mpregenperlevel"]
        self.mpregen_bonus_percent = 0
        self.crit_base = r["crit"]
        self.crit_perlevel = r["critperlevel"]
        self.crit_bonus = 0
        self.attackdamage_base = r["attackdamage"]
        self.attackdamage_perlevel = r["attackdamageperlevel"]
        self.attackdamage_bonus = 0
        self.attackspeed_offset = r["attackspeedoffset"]
        self.attackspeed_perlevel = r["attackspeedperlevel"]
        self.abilitypower_flat = 0
        self.abilitypower_percent = 0
        self.pen_armor_percent:List[float] = []
        self.pen_magic_flat = 0
        self.pen_magic_percent: List[float] = []
        self.pen_lethality = 0
        self.gp5 = 0
        self.damagereduction_percent = 0

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
        conn.commit()
        conn.close()
    def get_maxhp(self) -> float:
        return (self.hp_base + (self.level - 1) * self.hp_perlevel + self.hp_bonus) * (1 + self.hp_bonus_percent)
    def get_maxmp(self) -> float:
        return self.mp_base + (self.level-1) * self.mp_perlevel
    def get_attackdamage(self) -> float:
        return self.attackdamage_base + (self.level-1) * self.attackdamage_perlevel
    def get_abilitypower(self) -> float:
        return self.abilitypower_flat * (1 + self.abilitypower_percent/100)
    def get_attack_time(self) -> float:
        atk_spd = ChampStatistic.ATTACK_SPEED_PERCENT
        base_attack_speed = 0.625/(1+self.attackspeed_offset)
        l = self.level
        level_bonus = self.attackspeed_perlevel/100 * ((7/400)*(l**2)+(267/400)*(l-1))
        items_bonus = 0
        for item in self.items:
            for attribute in item.attribute_modifiers:
                if attribute == atk_spd:
                    items_bonus += attribute
        buff_bonus = 0
        for buff in self.buffs:
            if atk_spd in buff.attribute_modifiers:
                buff_bonus += buff.attribute_modifiers[atk_spd]
        total_attack_speed = base_attack_speed * (1+level_bonus+items_bonus+buff_bonus)
        return 1/total_attack_speed
    def gain_exp(self, exp_amount: int) -> None:
        assert(exp_amount > 0)
        self.exp += exp_amount
        should_be_level = math.floor(50*self.exp**2+130*self.exp-180)
        while (self.level < should_be_level):
            self.level_up()
        assert(self.level == should_be_level)
    def set_level(self, level:int):
        print(level)
        print(type(level))
        self.level = int(level)
        self.hp = self.get_maxhp()
    def level_up(self) -> None:
        hp_percent = self.hp / self.get_maxhp()
        self.level += 1
        self.hp = hp_percent * self.get_maxhp()
    
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
