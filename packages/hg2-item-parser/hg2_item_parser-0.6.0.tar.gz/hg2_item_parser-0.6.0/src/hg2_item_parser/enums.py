from enum import Enum


class ItemCategory(Enum):
    WEAPON = "weapon"
    COSTUME = "costume"
    BADGE = "badge"
    PET = "pet"


class SkillCategory(Enum):
    EQUIP = "equip"
    PET = "pet"


class DamageType(Enum):
    PHYSICAL = "Physical"
    FIRE = "Fire"
    ICE = "Ice"
    ENERGY = "Energy"
    LIGHT = "Light"
    POISON = "Poison"
    NONE = None


class WeaponType(Enum):
    AUTO_RIFLE = "Auto Rifle"
    MELEE = "Melee"
    PISTOL = "Pistol"
    HEAVY_PISTOL = "Heavy Pistol"
    DEPLOY_ANCIENT = "Deploy Ancient"
    DEPLOY_BATTERY = "Deploy Battery"
    DEPLOY_DOLLY = "Deploy Dolly"
    DEPLOY_TRAP = "Deploy Trap"
    DEPLOY_MINE = "Deploy Mine"
    DEPLOY_SPECIAL = "Deploy Special"
    RPG = "RPG"
    SPREAD_SHOTGUN = "Spread Shotgun"
    SINGLE_SHOTGUN = "Single Shotgun"
    SNIPER_RIFLE = "Sniper Rifle"
    SPECIAL = "Special"
    BOW = "Bow"
    SPRAY = "Spray"
    ACTIVATE_SPRAY = "Activate Spray"
    SWITCH_SPRAY = "Switch Spray"
    THROWN = "Thrown"
