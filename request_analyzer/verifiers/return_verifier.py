from typing import Tuple
from SayNoMore.request_analyzer.verifiers.arrival_verifier import ArrivalVerifier
from SayNoMore.request_analyzer.verifiers.abstract_verifier import ValueStages


class ReturnVerifier(ArrivalVerifier):
    """
    A verifier class specifically designed
    to validate the retrieved return date
    information from user requests.

    !!!! Since the validation logic for
    return date information is currently
    identical to that of arrival date
    information, this class inherits
    from ArrivalVerif and simply
    delegates the verification process
    to the parent class.
    """

    def __init__(self) -> None:
        super().__init__()

    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved return date
        against predefined criteria.

        Args:
            retrieved_value (str): The return date
            retrieved from the user request.

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
            for return date is the
            same as for arrival date.
            Therefore, this method simply calls
            the verify method of the parent
            class (ArrivalVerif).
        """
        # Delegate the verification process to
        # the parent class
        return super().verify(retrieved_value)
