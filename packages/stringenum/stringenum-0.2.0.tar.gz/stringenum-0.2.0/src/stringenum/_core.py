from __future__ import annotations

from typing import TYPE_CHECKING

from stringenum._compat import EnumType, StrEnum

if TYPE_CHECKING:
    from typing_extensions import Self


class _CaseInsensitiveGetItem(EnumType):
    def __getitem__(self, name: str) -> Self:  # type: ignore[explicit-override, misc, override]
        if not isinstance(name, str):
            raise KeyError(name)

        for key, value in super().__dict__["_member_map_"].items():
            if key.casefold() == name.casefold():
                return value  # type: ignore[no-any-return]
        raise KeyError(name)


class CaseInsensitiveStrEnum(StrEnum, metaclass=_CaseInsensitiveGetItem):
    """A subclass of `StrEnum` that supports case-insensitive lookup."""

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if member.value.casefold() == value.casefold():
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


class _DoubleSidedGetItem(EnumType):
    def __getitem__(self, name: str) -> Self:  # type: ignore[explicit-override, misc, override]
        if not isinstance(name, str):
            raise KeyError(name)

        for key, member in super().__dict__["_member_map_"].items():
            if (key == name) or (member.value == name):
                return member  # type: ignore[no-any-return]
        raise KeyError(name)


class DoubleSidedStrEnum(StrEnum, metaclass=_DoubleSidedGetItem):
    """
    A subclass of `StrEnum` that supports double-sided lookup, allowing
    both member values and member names to be used for lookups.
    It also ensures that each member has a unique value.
    """

    def __init__(self, *args: object) -> None:
        cls = self.__class__
        if any(self.value == member.value for member in cls):
            a = self.name
            e = cls(self.value).name
            msg = f"Aliases not allowed in {self.__class__.__name__}:  {a!r} --> {e!r}"
            raise ValueError(msg)

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if (member.value == value) or (member.name == value):
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


class _DoubleSidedCaseInsensitiveGetItem(EnumType):
    def __getitem__(self, name: str) -> Self:  # type: ignore[explicit-override, misc, override]
        if not isinstance(name, str):
            raise KeyError(name)

        for key, member in super().__dict__["_member_map_"].items():
            if (key.casefold() == name.casefold()) or (member.value.casefold() == name.casefold()):
                return member  # type: ignore[no-any-return]
        raise KeyError(name)


class DoubleSidedCaseInsensitiveStrEnum(StrEnum, metaclass=_DoubleSidedCaseInsensitiveGetItem):
    """
    A subclass of `StrEnum` that supports case-insenitive double-sided lookup,
    allowing both member values and member names to be used for lookups.
    It also ensures that each member has a unique value.
    """

    def __init__(self, *args: object) -> None:
        cls = self.__class__
        if any(self.value == member.value for member in cls):
            a = self.name
            e = cls(self.value).name
            msg = f"Aliases not allowed in {self.__class__.__name__}:  {a!r} --> {e!r}"
            raise ValueError(msg)

    @classmethod
    def _missing_(cls, value: object) -> Self:
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if (member.value.casefold() == value.casefold()) or (member.name.casefold() == value.casefold()):
                    return member
            raise ValueError(msg)
        raise ValueError(msg)
