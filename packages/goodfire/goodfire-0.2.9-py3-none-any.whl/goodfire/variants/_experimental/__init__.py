from ...controller.controller import Controller
from ...utils.logger import logger
from ..variants import VariantInterface

has_warned = False


class ProgrammableVariant(VariantInterface):
    """A class representing a programmable variant of a base model."""

    def __init__(self, base_model: str):
        global has_warned

        if not has_warned:
            logger.warning(
                "ProgrammableVariants are an experimental feature and may change in the future."
            )
            has_warned = True

        self.base_model = base_model
        self._controller = Controller()

    @property
    def controller(self) -> Controller:
        return self._controller

    def reset(self):
        self._controller = Controller()
