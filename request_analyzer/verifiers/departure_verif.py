from typing import Tuple
from request_analyzer.verifiers.destination_verif import DestinationVerif
from request_analyzer.verifiers.abstract_verif import ValueStages


class DepartureVerif(DestinationVerif):
    """
    A verifier class specifically designed
    to validate the retrieved departure 
    information from user requests.

    !!!! Since the validation logic for 
    departure information is currently 
    identical to that of destination 
    information, this class inherits 
    from DestinationVerif and simply 
    delegates the verification process 
    to the parent class.
    """

    def __init__(self) -> None:
        """
        Initializes the DepartureVerif 
        instance by calling the superclass 
        constructor.
        """
        super().__init__()

    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved departure
        value by delegating the 
        verification process to the 
        parent class (DestinationVerif).

        Args:
            retrieved_value (str): The 
                departure value retrieved
                from the user request.

        Returns:
            Tuple[ValueStages, str]: A tuple containing
                the verification status and a descriptive 
                message.
                    - The first element indicates whether
                    the verification passed (ValueStages.OK)
                    or failed (ValueStages.FIELD_NOT_FOUND)
                    or incorrect data entered (ValueStages.INCORRECT_VALUE).

                    - The second element is a human-readable 
                    message describing the outcome of the 
                    verification. Will be used by LLM.

        !!!! Note:
            Currently, the verification logic 
            for departure information is the 
            same as for destination information.
            Therefore, this method simply calls 
            the verify method of the parent 
            class (DestinationVerif).
        """
        # Delegate the verification process to
        # the parent class
        return super().verify(retrieved_value)
