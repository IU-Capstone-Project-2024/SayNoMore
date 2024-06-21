from vllm import LLM
from typing import Dict, Tuple, List

from request_analyzer.request_fields_enum import RequestField
from request_analyzer.retreivers.arrival_retriever import ArrivalRetriever
from request_analyzer.retreivers.return_retriever import ReturnRetriever
from request_analyzer.retreivers.departure_retriever import DepartureRetriever
from request_analyzer.retreivers.destination_retriever import DestinationRetriever
from request_analyzer.retreivers.budget_retriever import BudgetRetriever
from request_analyzer.retreivers.abstract_retriever import BaseRetriever
from request_analyzer.verifiers.abstract_verifier import ValueStages
from request_analyzer.request_verifier import RequestVerifier
from request_analyzer.verifiers.post_verifier import PostVerifier
from request_analyzer.utils.embedding_city_search import EmbeddingCitySearch


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

        self.verifier = RequestVerifier()
        self.searcher = EmbeddingCitySearch()

        # Register retrievers
        self.register_retriever(RequestField.Arrival, ArrivalRetriever(llm))
        self.register_retriever(RequestField.Return, ReturnRetriever(llm))
        self.register_retriever(RequestField.Departure,
                                DepartureRetriever(llm, self.searcher))
        self.register_retriever(RequestField.Destination,
                                DestinationRetriever(llm, self.searcher))
        self.register_retriever(RequestField.Budget, BudgetRetriever(llm))

    def register_retriever(self, field_name: str,
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

    def retrieve(
        self, request: str
    ) -> Tuple[Dict[RequestField, str], bool, List[Tuple[ValueStages, str]]]:
        """
        Retrieves information from a user request using
        registered retrievers.

        Args:
            request (str): The user's request as a 
                string.

        Returns:
            Tuple[Dict[str, str], bool]: 
                Dict: A dictionary mapping 
                field names to the retrieved 
                information.
                bool: True if all required
                    fields are retrieved and
                    retrieved correctly.
        """
        result_map = {}
        are_all_fields_correct = []
        map_for_post_verification = {}
        for field, retriever in self.retrievers.items():
            retrieved_data = retriever.retrieve(request)
            verification_result, status = self.verifier.verify(
                field, retrieved_data)

            map_for_post_verification[field] = (status, retrieved_data)

            result_map[field] = f"{field} data retrieved from user's " + \
                                f"request: {retrieved_data}. " + \
                                verification_result

            if field.is_required and status != ValueStages.OK:
                are_all_fields_correct.append(False)
            else:
                are_all_fields_correct.append(True)

        post_verif_res = []
        if all(are_all_fields_correct):
            post_verif_res = PostVerifier().verify_all_fields(
                map_for_post_verification)
            are_all_fields_correct.append(post_verif_res == [])

        return result_map, are_all_fields_correct, post_verif_res
