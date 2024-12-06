import re

from .extractors import (  # noqa: F401
    BitAttackExtractor,
    BitboardExtractor,
    BitDefendExtractor,
    ExtractorBase,
    FenExtractor,
    NeighborhoodExtractor,
    SanExtractor,
    UnifiedNegBitboardExtractor,
    UnifiedValuedBitboardExtractor,
    ValuedAttackExtractor,
    ValuedBitboardExtractor,
    ValuedDefendExtractor,
    WhiteMovingExtractor,
)


class ExtractorFactory:
    def __init__(self) -> None:
        self.extractors = {}
        self._register()

    def camel_to_snake(self, name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def _register(self) -> None:
        for subclass in ExtractorBase.__subclasses__():
            extractor_name = self.camel_to_snake(subclass.__name__.replace("Extractor", ""))
            self.extractors[extractor_name] = subclass

    def create(self, name: str) -> ExtractorBase:
        return self.extractors[name]()
