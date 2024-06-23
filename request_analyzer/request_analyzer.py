from request_analyzer.llm import LLM
from request_analyzer.information_retriever import InformationRetriever
from request_analyzer.more_info_required_message_generator import MoreInfoRequiredMessageGenerator
import re
import json
from datetime import datetime
from typing import Tuple


class RequestAnalyzer:
    """
    Analyzes user requests to extract required 
    information and generates appropriate 
    feedback messages if user request is invalid.

    This class orchestrates the process of retrieving information 
    from user requests and generating feedback message based on the 
    verification results of the retrieved information. If data extracted 
    is correct, then it will return extracted data instead of feedback message.
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
        self.extracted_data = {}  # Stores extracted data from user requests
        self.are_all_fields_retrieved = [
        ]  # Tracks if all fields have been successfully retrieved
        self.fields_to_update = [
        ]  # Indicates which fields need to be updated with new data

    async def analyzer_step(self, user_request: str) -> Tuple[bool, str]:
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
        fields_verification_map, are_all_fields_correct, post_verif_result = \
            await self.information_retriever.retrieve(user_request)

        if not self.are_all_fields_retrieved:
            self.are_all_fields_retrieved = are_all_fields_correct
            self.fields_to_update = [True] * len(are_all_fields_correct)
        else:
            self.fields_to_update = [False] * len(self.fields_to_update)
            for idx, is_field_retireved in enumerate(
                    self.are_all_fields_retrieved):
                if are_all_fields_correct[
                        idx] is True and is_field_retireved is False:
                    self.are_all_fields_retrieved[idx] = True
                    self.fields_to_update[idx] = True

        # Compile a regular expression pattern to
        # extract field names and data from the
        # verification results
        pattern = re.compile(
            r"RequestField\.(\w+) data retrieved from user's request: (.+?)\. Verification status:"
        )

        # Iterate through the verification map
        # to extract and concatenate field names
        # and data
        for idx, key in enumerate(fields_verification_map):
            data_string = fields_verification_map[key]
            match = pattern.search(data_string)
            field_name, field_data = match.groups()
            if match and (self.fields_to_update[idx]
                          or self.extracted_data.get(field_name,
                                                     "None") == "None"):
                self.extracted_data[field_name] = field_data

        return_message = ""  # Initialize the return message
        if not all(self.are_all_fields_retrieved):
            # Generate a feedback message if
            # any field verification failed
            return_message = await self \
                           .message_generator \
                           .generate_message(user_request,
                                              fields_verification_map,
                                              post_verif_result)
            return False, return_message

        # Convert extracted data to the required JSON format
        json_output = {}
        for field_name, retr_data in self.extracted_data.items():
            if field_name in ["Arrival", "Return"]:
                # Convert dates to YYYY-MM-DD format
                date_obj = datetime.strptime(retr_data, "%d/%m/%Y")
                json_output[field_name] = date_obj.strftime("%Y-%m-%d")
            elif field_name == "Budget" and retr_data != "None":
                # Convert budget to integer
                json_output[field_name] = int(retr_data)
            else:
                # Add other fields as is
                json_output[field_name] = retr_data

        # Return true if all fields were correctly verified, along with the JSON output
        return True, json.dumps(json_output, ensure_ascii=False)
