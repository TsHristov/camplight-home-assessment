from enum import Enum


class StyleEnum(str, Enum):
    """Supported rewrite styles."""

    PIRATE = "pirate"
    HAIKU = "haiku"
    FORMAL = "formal"
