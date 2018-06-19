from typing import Dict, Tuple, List, IO
from enum import Enum
import math
import json
import sqlite3
import abc

class DamageType(Enum):
    PHYSICAL = 1
    MAGICAL = 2
    TRUE = 3
    PURE = 4
class ResourceBar(Enum):
    MANA = 1
    ENERGY = 2
    NONE = 3
class DamageRatio(Enum):
    FLAT = 1
    PERCENT_MAX_HP = 2
    PERCENT_MISSING_HP = 3
    PERCENT_CURRENT_HP = 4
class Damage:
    def __init__(self, type:DamageType, amount:float=0, pen_armor_percent:List[float]=[], 
    pen_lethality:float=0, pen_magic_flat:float=0, pen_magic_percent:List[float]=[]):
        self.pen_armor_percent: List[float] = pen_armor_percent
        self.pen_lethality: float = pen_lethality
        self.pen_magic_flat: float = pen_magic_flat
        self.pen_magic_percent: List[float] = pen_magic_percent
        self.type: DamageType = type
        self.amount: float = amount
class onHitEffect():
    def __init__(self, type:DamageType, damageamount:float, damageRatio:DamageRatio):
        self.type = type
        pass
    def getDamage(self, target) -> Damage:
        if self.type == DamageRatio.FLAT:
            pass
        elif self.type == DamageRatio.PERCENT_MAX_HP:
            pass
        elif self.type == DamageRatio.PERCENT_MISSING_HP:
            pass
        elif self.type == DamageRatio.PERCENT_CURRENT_HP:
            pass
        return Damage(self.type)
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
        self.mp:float = 0
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
    def gain_exp(self, exp_amount: int) -> None:
        assert(exp_amount > 0)
        self.exp += exp_amount
        should_be_level = math.floor(50*self.exp**2+130*self.exp-180)
        while (self.level < should_be_level):
            self.level_up()
        assert(self.level == should_be_level)
    def level_up(self) -> None:
        hp_percent = self.hp / self.get_maxhp()
        mp_percent = self.mp / self.get_maxmp()
        self.level += 1
        self.hp = hp_percent * self.get_maxhp()
        self.mp = mp_percent * self.get_maxmp()
    @abc.abstractmethod
    def take_damage(self, attack: Damage) -> None:
        pass
class Champion(AbstractMinion):
    def __init__(self, name:str):
        conn = sqlite3.connect("data/champdata.sqlite")
        c = conn.cursor()
        r: Dict[str, float] = c.execute("SELECT * FROM champions WHERE id=? OR name=?", name).fetchone()

        # static quantities:
        self.hp_base = r["hp"]
        self.hp_perlevel = r["hpperlevel"]
        self.hp_bonus = 0
        self.hp_bonus_percent = 0
        self.mp_base = r["mp"]
        self.mp_perlevel = r["mpperlevel"]
        self.mp_bonus = 0
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
        self.attackspeed_offset = r["attackspeedoffest"]
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
        self.items = []
        self.buffs = []
        self.debuffs = []
        self.hp = self.get_maxhp()
        self.mp = self.get_maxmp()
        self.exp: int = 0
        self.gold: int = 0
        self.shield = []
        self.onHitEffects = [onHitEffect]
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
    def gain_exp(self, exp_amount: int) -> None:
        assert(exp_amount > 0)
        self.exp += exp_amount
        should_be_level = math.floor(50*self.exp**2+130*self.exp-180)
        while (self.level < should_be_level):
            self.level_up()
        assert(self.level == should_be_level)
    def level_up(self) -> None:
        hp_percent = self.hp / self.get_maxhp()
        mp_percent = self.mp / self.get_maxmp()
        self.level += 1
        self.hp = hp_percent * self.get_maxhp()
        self.mp = mp_percent * self.get_maxmp()
    def take_damage(self, attack: Damage) -> None:
        if attack.type == DamageType.PHYSICAL:
            armor = self.get_armor()
            # Armor penetration stacks multiplicatively, so we combine with a loop:
            for i in attack.pen_armor_percent:
                armor *= 1-i/100
            armor -= attack.pen_lethality * (0.6 + 0.4 * self.level/18)
            damage = (attack.amount) * (100/(armor+100))
            damage *= (1-self.damagereduction_percent/100)
            self.hp -=  damage
        elif attack.type == DamageType.MAGICAL:
            magic_resist = self.get_magic_resist()
            for i in attack.pen_magic_percent:
                magic_resist *= 1 - i/100
            magic_resist -= attack.pen_magic_flat
            damage = (attack.amount) * (100/magic_resist)
            damage *= (1-self.damagereduction_percent/100)
            self.hp -=  damage
        elif attack.type == DamageType.TRUE:
            self.hp -= (attack.amount) * (1-self.damagereduction_percent/100)
        else:
            raise Exception
        if self.hp <= 0:
            self.die()
    def basic_attack(self, target: AbstractMinion) -> None:
        attack = Damage(DamageType.PHYSICAL, amount=self.get_attackdamage(), \
            pen_armor_percent=self.pen_armor_percent, pen_lethality=self.pen_lethality)
        target.take_damage(attack)
        for effect in self.onHitEffects:
            effect.getDamage(effect, target)
    def buy_item(self, item):
        pass
    def sell_item(self, item):
        pass
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

#Buffs and debuffs
class ChampStatusModifier:
    def __init__(self, AbstractMinion):
        pass

def main():
    pass
main()