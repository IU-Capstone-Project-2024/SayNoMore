from vllm import LLM
from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.more_info_required_message_generator import MoreInfoRequiredMessageGenerator
import re
from typing import Tuple


class RequestAnalyzer:
    """
    Analyzes user requests to extract required 
    information and generates appropriate 
    feedback messages if user request is invalid.

    This class orchestrates the process of retrieving information 
    from user requests and generating feedback message based on the 
    verification results of the retrieved information. If data exctracted 
    is correct, then it will return extracted data instead of feedback message
    """

    def __init__(self, llm: LLM) -> None:
        """
        Initializes the RequestAnalyzer with a 
        Language Model instance.

        Args:
            llm (LLM): The language model 
                instance used for information 
                retrieval and message generation.
        """
        self.llm = llm 
        self.information_retriever = InformationRetriever(self.llm)
        self.message_generator = MoreInfoRequiredMessageGenerator(self.llm)
    
    def analyzer_step(self, user_request: str) -> Tuple[bool, str]:
        """
        Performs the analysis step for a
        given user request.

        This method retrieves information 
        from the user request, verifies the 
        correctness of the retrieved fields,
        and generates a feedback message 
        if any field verification fails.
        If the check is successful, the 
        received data will be returned.

        Args:
            user_request (str): The user's 
                request string to be 
                analyzed.

        Returns:
            Tuple[bool, str]: A tuple containing
                a boolean indicating whether 
                all fields were correctly 
                verified and a string
                representing the feedback 
                message or the retrieved 
                fields if verification 
                passed.
        """
        # Retrieve information and 
        # verification results from 
        # the user request
        fields_verification_map, is_all_fields_correct, post_verif_result = \
            self.information_retriever.retrieve(user_request)
        
        return_message = ""  # Initialize the return message
        if not is_all_fields_correct:
            # Generate a feedback message if 
            # any field verification failed
            return_message = self \
                            .message_generator \
                            .generate_message(user_request,
                                              fields_verification_map,
                                              post_verif_result)
            return False, return_message
        
        # Compile a regular expression pattern to 
        # extract field names and data from the 
        # verification results
        pattern = re.compile(r"RequestField\.(\w+) data retrieved from user's request: (.+?)\. Verification status:")
        fields_retrieved = ""  # Initialize the string to hold retrieved fields
        
        # Iterate through the verification map 
        # to extract and concatenate field names 
        # and data
        for key in fields_verification_map:
            data_string = fields_verification_map[key]
            match = pattern.search(data_string)
            if match:
                field_name = match.group(1)
                field_data = match.group(2)
                fields_retrieved += f"{field_name}:{field_data};"
        
        # Return true if all fields were correctly 
        # verified, along with the retrieved 
        # fields
        return True, fields_retrieved
