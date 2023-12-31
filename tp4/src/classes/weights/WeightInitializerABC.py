from abc import ABC, abstractmethod


class WeightInitializerABC(ABC):
    """
    Calculates initial weights
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def calculate(self, weights_qty: int) -> list[float]:
        pass
