from typing import Tuple
from request_analyzer.request_fields_enum import RequestField
from SayNoMore.request_analyzer.verifiers.abstract_verifier import BaseVerifier, ValueStages
from SayNoMore.request_analyzer.verifiers.departure_verifier import DepartureVerifier
from SayNoMore.request_analyzer.verifiers.destination_verifier import DestinationVerifier


class RequestVerifier:
    """
    A class to manage and utilize different
    verifiers for validating specific pieces
    of information extracted from user requests.

    Attributes:
        verifiers (Dict[str, BaseVerifier]): A 
            dictionary mapping field names to 
            their corresponding verifier instances.
    """

    def __init__(self) -> None:
        """
        Initializes the RequestVerification 
        instance and registers default verifiers.

        Note:
            Additional verifiers can be registered 
            dynamically using the register_verifier method.
        """
        self.verifiers = {}

        # Register verifiers
        # Example commented-out registrations for future expansion
        # self.register_verifier(RequestField.Arrival, ArrivalVerif())
        # self.register_verifier(RequestField.Return, ReturnVerif())
        self.register_verifier(RequestField.Departure, DepartureVerif())
        self.register_verifier(RequestField.Destination, DestinationVerif())
        # self.register_verifier(RequestField.Budget, BudgetVerif())

        # Placeholder for future implementation of verification classes initialization

    def register_verifier(self, field: RequestField,
                          verifier: BaseVerifier) -> None:
        """
        Registers a verifier for a specific field.

        Args:
            field (RequestField): The enum of field the
                verifier is responsible for.
            verifier (BaseVerifier): The verifier 
                instance.
        """
        self.verifiers[field] = verifier

    def verify(self, field: RequestField,
               retrieved_data: str) -> Tuple[str, str]:
        """
        Performs verification on a specific field 
        of a user request using the registered verifier.

        Args:
            field (RequestField): The enum of the field to verify.
            request (str): Retrieved data as a string
                           from user's request.

        Returns:
            Tuple[str, str]: 
                str: A formatted string containing 
                the verification status and description.
                str repr. of ValueStages: The status of the verification
                on that specific filed (eg. ValueStages.OK.name, which is "OK")
        """
        # Retrieve the verifier associated with the
        # specified field
        verifier = self.verifiers.get(field)
        if not verifier:
            raise ValueError(
                f"No verifier registered for field '{field.name}'")

        # Perform verification using
        # the selected verifier
        status, str_description = verifier.verify(retrieved_data)

        # Format and return the
        # verification result
        return (
            f"Verification status: {status.name}; Description: {str_description}",
            status.name)
