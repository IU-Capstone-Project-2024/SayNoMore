from vllm import LLM, SamplingParams

from request_analyzer.retreivers.arrival_retriever import ArrivalRetriever
from request_analyzer.retreivers.return_retriever import ReturnRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.budget_retriever import BudgetRetriever
from request_analyzer.retreivers.abstract_retriever import BaseRetriever


class InformationRetriever:
    def __init__(self, llm: LLM) -> None:
        self.retrievers = {}
        self.llm = llm
        
        # Register retrievers
        self.register_retriever("Arrival", ArrivalRetriever())
        self.register_retriever("Return", ReturnRetriever())
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
            field_name (str): The name of the field the retriever is responsible for.
            retriever (BaseRetriever): The retriever instance.
        """
        self.retrievers[field_name] = retriever

    def retrieve(self, request: str) -> dict:
        result_map = {}

        for field, retriever in self.retrievers.items():
            retrieved_data = retriever.retrieve(request)
            # TODO: add verification of retrieved data
            result_map[field] = retrieved_data
        
        return result_map
