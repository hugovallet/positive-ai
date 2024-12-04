from typing import List

from positive_ai.utils.ppt import Deck, ExtendedSlide


class ReferentStarterPack(Deck):
    @property
    def slides(self) -> List[ExtendedSlide]:
        return []
