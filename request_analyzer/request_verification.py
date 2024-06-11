from typing import Dict

from request_analyzer.verifiers.abstract_verif import BaseVerifier, ValueStages
from request_analyzer.verifiers.departure_verif import DepartureVerif
from request_analyzer.verifiers.destination_verif import DestinationVerif

class RequestVerification:
    def __init__(self) -> None:
        self.verifiers = {}

        # Register verifiers
        # self.register_verifier("Arrival", ArrivalVerif())
        # self.register_verifier("Return", ReturnVerif())
        self.register_verifier("Departure", DepartureVerif())
        self.register_verifier("Destination", DestinationVerif())
        # self.register_verifier("Budget", BudgetVerif())
        
        # TODO: Verification classes initialization

    
    def register_verifier(self, 
                          field_name: str,
                          verifier: BaseVerifier) -> None:
        """
        Registers a verifier for a specific field.

        Args:
            field_name (str): The name of the field the 
                verifier is responsible for.
            verifier (BaseVerifier): The verifier 
                instance.
        """
        self.verifiers[field_name] = verifier

    def verify(self, request: str) -> Dict[str, str]:
        """
        Retrieves information from a user request using
        registered retrievers.

        Args:
            request (str): The user's request as a 
                string.

        Returns:
            Dict[str, str]: A dictionary mapping 
                field names to the retrieved 
                information.
        """
        result_map = {}

        for field, verif in self.verifiers.items():
            status, str_description = verif.verify(request)
            result_map[field] = f"Verification status: {status.name};" + \
                                f"Description: {str_description}"
    
        return result_map