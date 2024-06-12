from typing import Tuple
from request_analyzer.verifiers.abstract_verif import BaseVerifier, ValueStages

class BudgetVerif(BaseVerifier):
    '''
    A verifier class specifically designed
    to validate the retrieved budget information
    from the users requests.

    Inherits from the BaseVerifier class,
    implementing the verify method to check
    the validity of the budget information.
    '''
    def __init__(self) -> None:
        super().__init__()
    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved arrival date
        against predefined criteria.

        Args:
            retrieved_value (str): The budget
            information retrieved from the user request.

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
        # Check if the budget is not provided
        if retrieved_value == 'None':
            return (ValueStages.FIELD_NOT_FOUND,
                    "The user has not entered this field")
        # Check if the budget is invalid
        # (not a digit or < 0)
        # isdigit() set False to strings like -5, -4, etc, so 2nd check
        # is not necessary
        retrieved_budget = retrieved_value.replace(" ","")
        if not retrieved_budget.isdigit():
            return (ValueStages.INCORRECT_VALUE,
                    "The user has entered wrong budget")
        # everything is fine
        return (ValueStages.OK,
                "Everything is good")
