from typing import Literal

from .enums import ItemCategory, WeaponType
from .info_parser import InfoParser
from .models import ItemProperties
from .unificator import Unificator


class PropertyParser:
    @classmethod
    def parse_properties(cls, item_main_data: dict[str, str]) -> ItemProperties:
        max_lvl = cls.parse_max_lvl(item_main_data)
        cost = cls.parse_cost(item_main_data)
        max_lvl_damage = cls.parse_max_lvl_damage(item_main_data)
        max_lvl_ammo = cls.parse_max_lvl_ammo(item_main_data)
        max_lvl_atk_speed = cls.parse_max_lvl_atk_speed(item_main_data)
        max_lvl_hp = cls.parse_max_lvl_hp(item_main_data)
        weapon_type = cls.parse_weapon_type(item_main_data)
        deploy_limit = cls.parse_deploy_limit(item_main_data)
        duration = cls.parse_max_lvl_duration(item_main_data)
        crit_rate = cls.parse_crit_rate(item_main_data)
        base_sync = cls.parse_base_sync(item_main_data)
        max_sync = cls.parse_max_up_sync(item_main_data)

        properties = ItemProperties(
            max_lvl,
            cost,
            max_lvl_damage,
            max_lvl_ammo,
            max_lvl_atk_speed,
            max_lvl_hp,
            weapon_type,
            deploy_limit,
            duration,
            crit_rate,
            base_sync,
            max_sync,
        )

        return properties

    @classmethod
    def parse_max_lvl(cls, item_main_data: dict[str, str]) -> int:
        max_lvl = int(item_main_data["MaxLv"])

        return max_lvl

    @classmethod
    def parse_cost(cls, item_main_data: dict[str, str]) -> int | None:
        cost = cls._get_int_or_none(item_main_data, "Cost")

        return cost or None

    @classmethod
    def parse_weapon_type(cls, item_main_data: dict[str, str]) -> WeaponType | None:
        weapon_type = item_main_data.get("BaseType")
        if weapon_type is None:
            return None

        return Unificator.unificate_weapon_type(weapon_type)

    @classmethod
    def parse_deploy_limit(cls, item_main_data: dict[str, str]) -> int | None:
        deploy_limit = cls._get_int_or_none(item_main_data, "LimitedNumber")

        return deploy_limit or None

    @classmethod
    def parse_crit_rate(cls, item_main_data: dict[str, str]) -> float | None:
        if InfoParser.parse_category(item_main_data) == ItemCategory.PET:
            crit_rate = cls._get_float_or_none(item_main_data, "initCritRate")
        else:
            crit_rate = cls._get_float_or_none(item_main_data, "CriticalRate")

        return crit_rate or None

    @classmethod
    def parse_max_lvl_hp(cls, item_main_data: dict[str, str]) -> int | None:
        base_hp = cls.parse_base_hp(item_main_data)
        hp_per_level = cls.parse_hp_per_lvl(item_main_data)
        if base_hp is None or hp_per_level is None:
            return None
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_hp = cls._calculate_value_on_lvl(base_hp, hp_per_level, max_lvl)

        return int(max_lvl_hp) or None

    @classmethod
    def parse_base_hp(cls, item_main_data: dict[str, str]) -> float | None:
        base_hp = cls._get_float_or_none(item_main_data, "HPBase")

        return base_hp

    @classmethod
    def parse_hp_per_lvl(cls, item_main_data: dict[str, str]) -> float | None:
        hp_per_level = cls._get_float_or_none(item_main_data, "HPAdd")

        return hp_per_level

    @classmethod
    def parse_max_lvl_damage(cls, item_main_data: dict[str, str]) -> int | None:
        base_damage = cls.parse_base_damage(item_main_data)
        damage_per_level = cls.parse_damage_per_lvl(item_main_data)
        if base_damage is None or damage_per_level is None:
            return None
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_damage = cls._calculate_value_on_lvl(
            base_damage, damage_per_level, max_lvl
        )

        return int(max_lvl_damage) or None

    @classmethod
    def parse_base_damage(cls, item_main_data: dict[str, str]) -> float | None:
        if InfoParser.parse_category(item_main_data) == ItemCategory.PET:
            base_damage = cls._get_float_or_none(item_main_data, "Attack")
        else:
            base_damage = cls._get_float_or_none(item_main_data, "DamageBase")

        return base_damage

    @classmethod
    def parse_damage_per_lvl(cls, item_main_data: dict[str, str]) -> float | None:
        if InfoParser.parse_category(item_main_data) == ItemCategory.PET:
            damage_per_lvl = cls._get_float_or_none(item_main_data, "Attack_Add")
        else:
            damage_per_lvl = cls._get_float_or_none(item_main_data, "DamageAdd")

        return damage_per_lvl

    @classmethod
    def parse_max_lvl_ammo(
        cls, item_main_data: dict[str, str]
    ) -> int | Literal["∞"] | None:
        base_ammo = cls.parse_base_ammo(item_main_data)
        ammo_per_level = cls.parse_ammo_per_lvl(item_main_data)
        if base_ammo is None or ammo_per_level is None:
            return None
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_ammo = cls._calculate_value_on_lvl(base_ammo, ammo_per_level, max_lvl)
        if int(max_lvl_ammo) == -1:
            return "∞"

        return int(max_lvl_ammo) or None

    @classmethod
    def parse_base_ammo(cls, item_main_data: dict[str, str]) -> float | None:
        base_ammo = cls._get_float_or_none(item_main_data, "AmmoBase")

        return base_ammo

    @classmethod
    def parse_ammo_per_lvl(cls, item_main_data: dict[str, str]) -> float | None:
        ammo_per_lvl = cls._get_float_or_none(item_main_data, "AmmoAdd")

        return ammo_per_lvl

    @classmethod
    def parse_max_lvl_atk_speed(cls, item_main_data: dict[str, str]) -> float | None:
        base_atk_speed = cls.parse_base_atk_speed(item_main_data)
        atk_speed_per_lvl = cls.parse_atk_speed_per_lvl(item_main_data)
        if base_atk_speed is None or atk_speed_per_lvl is None:
            return None
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_atk_speed = cls._calculate_value_on_lvl(
            base_atk_speed, atk_speed_per_lvl, max_lvl, 3
        )

        return float(max_lvl_atk_speed) or None

    @classmethod
    def parse_base_atk_speed(cls, item_main_data: dict[str, str]) -> float | None:
        base_atk_speed = cls._get_float_or_none(item_main_data, "FireRateBase")

        return base_atk_speed

    @classmethod
    def parse_atk_speed_per_lvl(cls, item_main_data: dict[str, str]) -> float | None:
        atk_speed_per_lvl = cls._get_float_or_none(item_main_data, "FireRateAdd")

        return atk_speed_per_lvl

    @classmethod
    def parse_max_lvl_duration(cls, item_main_data: dict[str, str]) -> float | None:
        base_duration = cls.parse_base_duration(item_main_data)
        duration_per_lvl = cls.parse_duration_per_lvl(item_main_data)
        if base_duration is None or duration_per_lvl is None:
            return None
        max_lvl = cls.parse_max_lvl(item_main_data)
        max_lvl_duration = cls._calculate_value_on_lvl(
            base_duration, duration_per_lvl, max_lvl, 2
        )

        return float(max_lvl_duration) or None

    @classmethod
    def parse_base_duration(cls, item_main_data: dict[str, str]) -> float | None:
        base_duration = cls._get_float_or_none(item_main_data, "CountDownTime")

        return base_duration

    @classmethod
    def parse_duration_per_lvl(cls, item_main_data: dict[str, str]) -> float | None:
        duration_per_lvl = cls._get_float_or_none(item_main_data, "CountDownTimeAdd")

        return duration_per_lvl

    @classmethod
    def parse_max_up_sync(cls, item_main_data: dict[str, str]) -> int | None:
        base_sync = cls.parse_base_sync(item_main_data)
        sync_per_up = cls.parse_sync_per_up(item_main_data)
        max_sync = cls.parse_max_sync(item_main_data)
        if base_sync is None or sync_per_up is None or max_sync is None:
            return None
        max_up_sync = cls._calculate_value_on_lvl(base_sync, sync_per_up, max_sync + 1)

        return int(max_up_sync) or None

    @classmethod
    def parse_max_sync(cls, item_main_data: dict[str, str]) -> int | None:
        max_sync = cls._get_int_or_none(item_main_data, "SynMaxLevel")

        return max_sync

    @classmethod
    def parse_base_sync(cls, item_main_data: dict[str, str]) -> int | None:
        base_sync = cls._get_int_or_none(item_main_data, "SynInit")

        return base_sync

    @classmethod
    def parse_sync_per_up(cls, item_main_data: dict[str, str]) -> int | None:
        sync_per_lvl = cls._get_int_or_none(item_main_data, "SynAdd")

        return sync_per_lvl

    @staticmethod
    def _get_float_or_none(data: dict[str, str], key: str) -> float | None:
        value = data.get(key)
        if value is None:
            return None

        return float(value)

    @staticmethod
    def _get_int_or_none(data: dict[str, str], key: str) -> int | None:
        value = data.get(key)
        if value is None:
            return None

        return int(value)

    @staticmethod
    def _calculate_value_on_lvl(
        base_value: int | float,
        value_per_lvl: int | float,
        lvl: int,
        precision: int | None = None,
    ) -> int | float:
        value = round(base_value + value_per_lvl * (lvl - 1), precision)

        return value
