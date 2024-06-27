from typing import Tuple
from request_analyzer.verifiers.abstract_verifier import BaseVerifier, ValueStages


class DestinationVerifier(BaseVerifier):
    """
    A verifier class specifically designed
    to validate the retrieved destination 
    information from user requests.

    Inherits from the BaseVerifier class, 
    implementing the verify method to check 
    the validity of the destination information.
    """

    def __init__(self) -> None:
        """
        Initializes the DestinationVerif instance 
        by calling the superclass constructor.
        """
        super().__init__()

    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved destination value 
        against predefined criteria.

        Args:
            retrieved_value (str): The destination 
            value retrieved from the user request.

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
        """
        # Check if the retrieved value indicates that the
        # destination field was not provided
        if retrieved_value == "None":
            # Return FIELD_NOT_FOUND status along with
            # a descriptive message
            return (ValueStages.FIELD_NOT_FOUND,
                    "The user has not entered this field")

        # If the retrieved value passes the initial check,
        # assume everything is good
        return (ValueStages.OK, "Everything is good")
