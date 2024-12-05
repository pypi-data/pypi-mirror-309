from .enums import DamageType, WeaponType


class Unificator:
    WEAPON_TYPES = {
        "autogun": WeaponType.AUTO_RIFLE,
        "near_sword": WeaponType.MELEE,
        "near_saw": WeaponType.MELEE,
        "pistol_fast": WeaponType.PISTOL,
        "pistol_heavy": WeaponType.HEAVY_PISTOL,
        "place_ancient": WeaponType.DEPLOY_ANCIENT,
        "place_battery": WeaponType.DEPLOY_BATTERY,
        "place_doll": WeaponType.DEPLOY_DOLLY,
        "place_induce": WeaponType.DEPLOY_TRAP,
        "place_mine": WeaponType.DEPLOY_MINE,
        "place_special": WeaponType.DEPLOY_SPECIAL,
        "rpg": WeaponType.RPG,
        "shotgun_multi": WeaponType.SPREAD_SHOTGUN,
        "shotgun_single": WeaponType.SINGLE_SHOTGUN,
        "sniper": WeaponType.SNIPER_RIFLE,
        "special": WeaponType.SPECIAL,
        "special_bow": WeaponType.BOW,
        "spray": WeaponType.SPRAY,
        "spray_active": WeaponType.ACTIVATE_SPRAY,
        "spray_enchanting": WeaponType.SPRAY,
        "spray_switch": WeaponType.SWITCH_SPRAY,
        "throw": WeaponType.THROWN,
    }

    DAMAGE_TYPES = {
        "1": DamageType.PHYSICAL,
        "physic": DamageType.PHYSICAL,
        "pure": DamageType.PHYSICAL,
        "2": DamageType.FIRE,
        "fire": DamageType.FIRE,
        "3": DamageType.ICE,
        "snow": DamageType.ICE,
        "ice": DamageType.ICE,
        "4": DamageType.ENERGY,
        "power": DamageType.ENERGY,
        "5": DamageType.LIGHT,
        "light": DamageType.LIGHT,
        "6": DamageType.POISON,
        "poison": DamageType.POISON,
        "none": DamageType.NONE,
        "null": DamageType.NONE,
        ";": DamageType.NONE,
    }

    @classmethod
    def unificate_weapon_type(cls, weapon_type: str) -> WeaponType:
        return cls.WEAPON_TYPES[weapon_type]

    @classmethod
    def unificate_damage_type(cls, damage_type: str) -> DamageType:
        return cls.DAMAGE_TYPES[damage_type]
