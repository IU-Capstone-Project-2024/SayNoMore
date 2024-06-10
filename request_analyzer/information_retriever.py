from vllm import LLM
from typing import Dict

from request_analyzer.retreivers.arrival_retriever import ArrivalRetriever
from request_analyzer.retreivers.return_retriever import ReturnRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.budget_retriever import BudgetRetriever
from request_analyzer.retreivers.abstract_retriever import BaseRetriever


class InformationRetriever:
    """
    A class to manage and utilize different retrievers 
    for extracting specific pieces of information from 
    user requests.

    Attributes:
        retrievers (Dict[str, BaseRetriever]): A dictionary 
            mapping field names to their corresponding 
            retriever instances.
        llm (LLM): An instance of a VLLM used by retrievers
            for generating text based on prompts.
    """

    def __init__(self, llm: LLM) -> None:
        """
        Initializes the InformationRetriever with a given 
        VLLM instance and registers default retrievers.

        Args:
            llm (LLM): The VLLM instance to be used by 
                retrievers for text generation.
        """
        self.retrievers = {}
        self.llm = llm
        
        # Register retrievers
        self.register_retriever("Arrival", ArrivalRetriever(llm))
        self.register_retriever("Return", ReturnRetriever(llm))
        self.register_retriever("Departure", DepartureRetriever(llm))
        self.register_retriever("Destination", DestinationRetriever(llm))
        self.register_retriever("Budget", BudgetRetriever(llm))
        
        # TODO: Verification classes initialization

    def register_retriever(self, 
                           field_name: str,
                           retriever: BaseRetriever) -> None:
        """
        Registers a retriever for a specific field.

        Args:
            field_name (str): The name of the field the 
                retriever is responsible for.
            retriever (BaseRetriever): The retriever 
                instance.
        """
        self.retrievers[field_name] = retriever

    def retrieve(self, request: str) -> Dict[str, str]:
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

        for field, retriever in self.retrievers.items():
            retrieved_data = retriever.retrieve(request)
            # TODO: add verification of retrieved data
            result_map[field] = retrieved_data
        
        return result_map