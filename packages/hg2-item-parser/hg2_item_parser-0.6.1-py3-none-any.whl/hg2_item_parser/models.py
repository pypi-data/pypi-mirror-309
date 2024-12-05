from dataclasses import dataclass

from .enums import DamageType, WeaponType


class BaseItemModel:
    def __str__(self) -> str:
        return "\n".join(f"{name}: {value}" for name, value in self.__dict__.items())


@dataclass
class ItemInfo(BaseItemModel):
    id: int
    title_id: int
    title: str
    image_id: int
    image_url: str
    damage_type: DamageType
    rarity: int


@dataclass
class ItemProperties(BaseItemModel):
    max_lvl: int
    cost: int | None = None
    max_lvl_damage: int | None = None
    max_lvl_ammo: int | None = None
    max_lvl_atk_speed: float | None = None
    max_lvl_hp: int | None = None
    weapon_type: WeaponType | None = None
    deploy_limit: int | None = None
    duration: float | None = None
    crit_rate: float | None = None
    base_sync: int | None = None
    max_sync: int | None = None


@dataclass
class ItemSkill(BaseItemModel):
    id: int
    damage_type: DamageType
    title_id: int
    title: str
    description_template_id: int
    description_template: str
    description: str


@dataclass
class Item:
    info: ItemInfo
    properties: ItemProperties
    skills: list[ItemSkill]

    def __str__(self) -> str:
        border = "-" * 15
        skills_str = f"\n{border}\n".join(str(skill) for skill in self.skills)

        return (
            f"INFO\n{self.info}\n\n"
            f"PROPERTIES\n{self.properties}\n\n"
            f"SKILLS\n{skills_str or None}"
        )
