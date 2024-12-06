from sincpro_framework import ApplicationService as _ApplicationService
from sincpro_framework import DataTransferObject
from sincpro_framework import Feature as _Feature
from sincpro_framework import UseFramework as _UseFramework


class DependencyContextType:
    """Typing helper."""


class Feature(_Feature, DependencyContextType):
    pass


class ApplicationService(_ApplicationService, DependencyContextType):
    pass
