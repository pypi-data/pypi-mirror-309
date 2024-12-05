from typing import overload
from enum import Enum
import typing

import System
import System.Runtime.Versioning

System_Runtime_Versioning_FrameworkName = typing.Any


class ResourceScope(Enum):
    """This class has no documentation."""

    NONE = 0

    MACHINE = ...

    PROCESS = ...

    APP_DOMAIN = ...

    LIBRARY = ...

    PRIVATE = ...

    ASSEMBLY = ...


class ResourceExposureAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def resource_exposure_level(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    def __init__(self, exposureLevel: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class VersioningHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    @overload
    def make_version_safe_name(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope) -> str:
        ...

    @staticmethod
    @overload
    def make_version_safe_name(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope, type: typing.Type) -> str:
        ...


class ResourceConsumptionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def resource_scope(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    @property
    def consumption_scope(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    @overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...

    @overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope, consumptionScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class FrameworkName(System.Object, System.IEquatable[System_Runtime_Versioning_FrameworkName]):
    """This class has no documentation."""

    @property
    def identifier(self) -> str:
        ...

    @property
    def version(self) -> System.Version:
        ...

    @property
    def profile(self) -> str:
        ...

    @property
    def full_name(self) -> str:
        ...

    @overload
    def __init__(self, identifier: str, version: System.Version) -> None:
        ...

    @overload
    def __init__(self, identifier: str, version: System.Version, profile: str) -> None:
        ...

    @overload
    def __init__(self, frameworkName: str) -> None:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.Versioning.FrameworkName) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_string(self) -> str:
        ...


class ComponentGuaranteesOptions(Enum):
    """This class has no documentation."""

    NONE = 0

    EXCHANGE = ...

    STABLE = ...

    SIDE_BY_SIDE = ...


class ComponentGuaranteesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def guarantees(self) -> System.Runtime.Versioning.ComponentGuaranteesOptions:
        ...

    def __init__(self, guarantees: System.Runtime.Versioning.ComponentGuaranteesOptions) -> None:
        ...


class TargetFrameworkAttribute(System.Attribute):
    """Identifies the version of .NET that a particular assembly was compiled against."""

    @property
    def framework_name(self) -> str:
        ...

    @property
    def framework_display_name(self) -> str:
        ...

    @property.setter
    def framework_display_name(self, value: str) -> None:
        ...

    def __init__(self, frameworkName: str) -> None:
        ...


