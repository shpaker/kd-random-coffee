import enum


class AppEnvironments(
    enum.StrEnum,
):
    LOCAL = enum.auto()
    PROD = enum.auto()
