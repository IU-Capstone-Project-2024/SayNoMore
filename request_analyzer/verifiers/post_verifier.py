from request_analyzer.verifiers.abstract_verifier import BaseVerifier
from request_analyzer.request_fields_enum import RequestField
from request_analyzer.verifiers.abstract_verifier import ValueStages
from datetime import datetime

from typing import Dict, Tuple, List


class PostVerifier():
    """
    A verifier class responsible for validating
    requests based on specific criteria.

    Post is because it is called after verification 
    of each separate RequestField.
    """

    def verify_all_fields(
        self, verification_result: Dict[RequestField, Tuple[ValueStages, str]]
    ) -> List[Tuple[ValueStages, str]]:
        """
        Verifies all fields of a request and returns 
        a list of tuples indicating the status 
        and message will be passed to LLM for each
        incrorectly filled field.

        Args:
            verification_result (Dict[RequestField,
                                      Tuple[ValueStages, str]
                                     ]): A dictionary mapping
                                         each request field 
                                         to its verification 
                                         status and value.

        Returns:
            List[Tuple[ValueStages, str]]: A list of tuples 
                containing the verification status and 
                corresponding error message for each 
                failed verification.
        """
        result_verif_status = []
        if not self._time_verification(
                verification_result[RequestField.Arrival][0],
                verification_result[RequestField.Arrival][1],
                verification_result[RequestField.Return][0],
                verification_result[RequestField.Return][1]):
            result_verif_status.append((ValueStages.INCORRECT_VALUE,
                                        "The time of arrival in a city is "
                                        "earlier than the time of departure "
                                        "from that city."))
        if not self._cities_verification(
                verification_result[RequestField.Departure][0],
                verification_result[RequestField.Departure][1],
                verification_result[RequestField.Destination][0],
                verification_result[RequestField.Destination][1]):
            result_verif_status.append(
                (ValueStages.INCORRECT_VALUE, "Destination and departure "
                 "cities match"))
        return result_verif_status

    def _time_verification(self, arrival_status: ValueStages,
                           arrival_time_retrieved: str,
                           return_status: ValueStages,
                           return_time_retrieved: str) -> bool:
        """
        Internal method to verify the logical consistency
        between arrival and return times.

        Args:
            arrival_status (ValueStages): 
                The verification status of the 
                arrival time.
            arrival_time_retrieved (str): 
                The retrieved arrival time 
                string.
            return_status (ValueStages): 
                The verification status of 
                the return time.
            return_time_retrieved (str): 
                The retrieved return 
                time string.

        Returns:
            bool: True if the verification passes, otherwise False.
        """
        assert arrival_status == ValueStages.OK and return_status == ValueStages.OK

        arrival_time = datetime.strptime(arrival_time_retrieved, '%d/%m/%Y')
        return_time = datetime.strptime(return_time_retrieved, '%d/%m/%Y')
        # Check if arrival time is later than return time
        if arrival_time > return_time:
            return True
        return False

    def _cities_verification(self, departure_city_status: ValueStages,
                             departure_city_retrieved: str,
                             destination_city_status: ValueStages,
                             destination_city_retrieved: str) -> bool:
        """
        Internal method to verify the logical 
        consistency between departure 
        and destination cities.

        Args:
            departure_city_status (ValueStages):
                The verification status of
                the departure city.
            departure_city_retrieved (str): 
                The retrieved departure 
                city name.
            destination_city_status (ValueStages): 
                The verification status of 
                the destination city.
            destination_city_retrieved (str): 
                The retrieved destination 
                city name.

        Returns:
            bool: True if the verification 
                passes, otherwise False.
        """
        assert departure_city_status == ValueStages.OK and destination_city_status == ValueStages.OK
        # Check if departure and destination cities are different
        if destination_city_retrieved != departure_city_retrieved:
            return True
        return False
