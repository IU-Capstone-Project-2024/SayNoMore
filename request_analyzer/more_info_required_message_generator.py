from vllm import LLM, SamplingParams
from typing import Dict, List, Tuple

from request_analyzer.request_fields_enum import RequestField
from request_analyzer.verifiers.abstract_verifier import ValueStages


class MoreInfoRequiredMessageGenerator():
    """
    This class generates a message asking users 
    to re-enter missing or incorrectly formatted 
    fields in their request.
    
    Attributes:
        llm (LLM): An instance of the Language Model
                   used for generating the message.
        sampling_params (SamplingParams): Parameters 
                   for controlling the generation process.
        prefix_prompt (str): A template string that will 
                   be filled with user request details 
                   and verification results.
    """
     
    def __init__(self,
                 llm: LLM) -> None:
        """
        Initializes the MoreInfoRequiredMessageGenerator 
        with a given language model instance.
        
        Args:
            llm (LLM): The language model instance 
                       to use for generating messages.
        """
        self.llm = llm
        self.sampling_params = SamplingParams(temperature=0, 
                                              min_tokens=35, 
                                              max_tokens=100, 
                                              stop='"')
        self.prefix_prompt = \
'''The user has sent his request. Not all fields received from the request passed the verification check. Your task is to generate a message to the user to make him re-enter the required fields correctly. Please note that the 'Budget' field is optional. Users can choose whether or not to fill it in. If the Budget field is left blank, you may suggest entering a value, but it is not mandatory. If some fields are not found, ask to enter only those fields. If some fields are in the wrong format, ask to enter them correctly. Examples:

Q: "User's request: 'Отправляюсь из Казани в город Казань c 15ое по 2ое сентября. Мой бюджет 200 тысяч.'
    RequestField.Arrival data retrieved from user's request: 15/09/2024. Verification status: OK; Description: Everything is good.
    RequestField.Return data retrieved from user's request: 02/09/2024. Verification status: OK; Description: Everything is good.
    RequestField.Departure data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good
    RequestField.Destination data retrieved from user's request: Казань. Verification status: OK; Description: Everything is good
    RequestField.Budget data retrieved from user's request: 200000. Verification status: OK; Description: Everything is good
    BUT: The time of return from a city is earlier than the time of arrival from that city. Destination and departure cities match"
A: "В вашем запросе есть некоторые проблемы. Пожалуйста, убедитесь, что города отправления и назначения не совпадают, а дата возвращения введена позднее даты прибытия. Не могли бы вы повторно ввести эти данные правильно? Спасибо!" 

Q: "User's request: 'Хочу сьездить в Волгоград через три дня'
    RequestField.Arrival data retrieved from user's request: 19/06/2024. Verification status: OK; Description: Everything is good.
    RequestField.Return data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field.
    RequestField.Departure data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field
    RequestField.Destination data retrieved from user's request: Волгоград. Verification status: OK; Description: Everything is good
    RequestField.Budget data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field"
A: "Похоже, что в вашем запросе не хватает некоторых деталей. Пожалуйста, укажите город вылета, дату вылета и дату возвращения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно."

Q: "User's request: 'Отправляюсь из Волгограда в другой город Волгоград. Даты с 12 по 19 февраля.'
    RequestField.Arrival data retrieved from user's request: 12/02/2025. Verification status: OK; Description: Everything is good.
    RequestField.Return data retrieved from user's request: 19/02/2025. Verification status: OK; Description: Everything is good.
    RequestField.Departure data retrieved from user's request: Волгоград. Verification status: OK; Description: Everything is good
    RequestField.Destination data retrieved from user's request: Волгоград. Verification status: OK; Description: Everything is good
    RequestField.Budget data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field
    BUT: Destination and departure cities match."
A: "В вашем запросе есть некоторые проблемы. Пожалуйста, убедитесь, что города отправления и назначения не совпадают. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!"

Q: "User's request: 'Поеду в Питер в середине мая. Обратно вернусь 23 июня.'
RequestField.Arrival data retrieved from user's request: 15/05/2024. Verification status: INCORRECT_VALUE; Description: The user entered outdated date.
RequestField.Return data retrieved from user's request: 23/06/2024. Verification status: OK; Description: Everything is good.
RequestField.Departure data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field
RequestField.Destination data retrieved from user's request: Санкт-Петербург. Verification status: OK; Description: Everything is good
RequestField.Budget data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field"
A: "Похоже, что я не получил все необходимые данные для вашего запроса. Убедитесь, что вы указали дату вылета. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!"

Q: "User's request: 'Уеду из города c 1ое по 7мое сентября'
RequestField.Arrival data retrieved from user's request: 01/09/2024. Verification status: OK; Description: Everything is good.
RequestField.Return data retrieved from user's request: 07/09/2024. Verification status: OK; Description: Everything is good.
RequestField.Departure data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field
RequestField.Destination data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field
RequestField.Budget data retrieved from user's request: None. Verification status: FIELD_NOT_FOUND; Description: The user has not entered this field"
A: "Похоже, что я не получил все необходимые данные для вашего запроса. Пожалуйста, укажите город вылета и город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!"

Q: "PASTE_DATA"
A: "'''

    def generate_message(self,
                         user_request: str,
                         field_verification_map: Dict[RequestField, str],
                         post_verif_result: List[Tuple[ValueStages, str]]) -> str:
        """
        Generates a message based on 
        the user's request and its 
        verification results.
        
        Args:
            user_request (str): The original 
                request made by the user.
            field_verification_map (Dict[RequestField, str]): A 
                dictionary mapping request fields to their 
                verification statuses.
            post_verif_result (List[Tuple[ValueStages, str]]): A list
                of tuples containing the verification stage 
                and result for each field.
            
        Returns:
            str: The generated message asking the user to re-enter 
                 missing or incorrectly formatted fields.
        """
        DATA_TO_PASTE = f"User's request: '{user_request}'\n" + \
                        "\n".join(field_verification_map[key] for key in field_verification_map)
        if post_verif_result:
            post_verif_text = ". ".join([pair[1] for pair in post_verif_result])
            DATA_TO_PASTE += f"\nBUT: {post_verif_text}."
        
        prompt = self.prefix_prompt.replace("PASTE_DATA", DATA_TO_PASTE)
        vllm_output = self.llm.generate(prompt, self.sampling_params)

        # Extract and return the generated text as
        # the return time from the destination city
        return vllm_output[0].outputs[0].text
        