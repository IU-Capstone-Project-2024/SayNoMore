from typing import Tuple
from request_analyzer.verifiers.abstract_verifier import ValueStages, BaseVerifier
from datetime import datetime
import re
from enum import Enum


class DateInfo(Enum):
    OK = "Everything is good."
    WRONG_DATE_FORMAT = "The user entered wrong date format."
    DATE_IS_OUTDATED = "The user entered outdated date."

    def __init__(self, message: str):
        self.message = message


class ArrivalVerifier(BaseVerifier):
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

    # Check is date follows expected format or not
    def _check_date(self, retrieved_value: str):
        # create regexp for expected format
        right_data_format = r'^\d\d/\d\d/\d\d\d\d'
        # check if parsed date follows required format
        if re.match(right_data_format, retrieved_value):
            return DateInfo.OK
        else:
            return DateInfo.WRONG_DATE_FORMAT

    def _is_valid_date(self, retrieved_value: str):
        # Attempt to parse the string according
        # to the format specified in the
        # arrival_retriever
        # parse retrieved string
        # to the datetime
        try:
            arr_time = datetime.strptime(retrieved_value, '%d/%m/%Y')
            # check current date
            present_time = datetime.now()
            # If the user time is not outdated
            # then it is valid
            # else it is outdated
            if arr_time >= present_time:
                return DateInfo.OK
            else:
                return DateInfo.DATE_IS_OUTDATED
        except ValueError:
            return DateInfo.WRONG_DATE_FORMAT

    def verify(self, retrieved_value: str) -> Tuple[ValueStages, str]:
        """
        Verifies the retrieved arrival date
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
                    "The user has not entered this field.")
        # check if something wrong with the time
        # (outdated or wrong format)
        # Fields containing possible state of the check

        check_date_reply = self._check_date(retrieved_value)
        is_valid_date_reply = self._is_valid_date(retrieved_value)

        # If data is in wrong format
        if check_date_reply == DateInfo.WRONG_DATE_FORMAT:
            return (ValueStages.INCORRECT_VALUE, check_date_reply.message)

        # Outdated data check
        if is_valid_date_reply == DateInfo.DATE_IS_OUTDATED or \
           is_valid_date_reply == DateInfo.WRONG_DATE_FORMAT:
            return (ValueStages.INCORRECT_VALUE, is_valid_date_reply.message)

        # Return ok if everything is fine
        return (ValueStages.OK, DateInfo.OK.message)
