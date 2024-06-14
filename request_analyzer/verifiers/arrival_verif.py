# import required libraries
from typing import Tuple
from request_analyzer.verifiers.abstract_verif import ValueStages, BaseVerifier
from datetime import datetime


# function to check validity of the data
def is_valid_date(retrieved_value: str):
    # Attempt to parse the string according
    # to the format specified in the
    # arrival_retriever
    try:
        # parse retrieved string
        # to the datetime information
        arr_time = datetime.strptime(retrieved_value, '%d/%m/%Y')
        # check current date
        present_time = datetime.now()
        # If the user time is not outdated
        # then it is valid
        # else it is outdated
        if arr_time >= present_time:
            return True
        else:
            return False
    # if we cannot parse the data
    except ValueError:
        return False


class ArrivalVerif(BaseVerifier):
    '''
    A verifier class specifically designed
    to validate the retrieved arrival time
    from the users requests.

    Inherits from the BaseVerifier class,
    implementing the verify method to check
    the validity of the arrival information.
    '''

    def __init__(self) -> None:
        """
        Initializes the Arrivalverif instance
        by calling the superclass constructor.
        """
        super().__init__()

    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved arrival time
        against predefined criteria.

        Args:
            retrieved_value (str): The arrival
            time retrieved from the user request.

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
        # arrival field was not provided
        if retrieved_value == 'None':
            return (ValueStages.FIELD_NOT_FOUND,
                    "The user has not entered this field")
        # check if something wrong with the time
        # (outdated or worng format)
        if not is_valid_date(retrieved_value):
            return (ValueStages.INCORRECT_VALUE,
                    "The user entered wrong arrival time")
        # Return ok if everything is fine
        return (ValueStages.OK, "Everything is good")
