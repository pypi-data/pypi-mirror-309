from typing import Any


class Empty:
    """
        Basically an equivalent class to Optional.Empty, but just to the Maybe class. Can be supplied the prevous
        value before turning to Empty, with a reason why we got an empty and the function call trace of the Maybe.
    """
    RED = '\033[1;4;91m'
    NORMAL = '\033[0;0m'
    NO_PREV_VALUE = object()

    def __init__(self, previousValue: Any = NO_PREV_VALUE, reason: str = "", trace: list[str] = []):
        """Create an Empty object

        :param previousValue: The previous value contained by the Maybe
        :param reason: The reason why an Empty was created
        :param trace: The function call trace of all the calls before spawning the Empty
        """
        self.reason = reason
        self.previously = previousValue
        self.functionCallTrace = trace

    def __str__(self) -> str:
        HAD_VALUE = self.previously != Empty.NO_PREV_VALUE  # Could be None
        HAS_REASON = self.reason != ''
        out = f"{Empty.RED}Empty (FunctionalMaybe.Empty){Empty.NORMAL}"
        if HAD_VALUE:
            out += "\n" + f'Value of the FunctionalMaybe before turning empty: {self.previously}'
        if HAS_REASON:
            out += "\nReason:\n"
            out += str(self.reason)

        return out

    def getFuncTrace(self) -> str:
        """Get the function calls performed by the Maybe before the Empty
        :return: The function calls as a string
        """
        return "\n".join(self.functionCallTrace)