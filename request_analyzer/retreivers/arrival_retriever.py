from request_analyzer.llm import LLM
from datetime import datetime
from request_analyzer.retreivers.abstract_retriever import BaseRetriever
from request_analyzer.utils.extract_data import extract_data


# retrieve the time of arrival
class ArrivalRetriever(BaseRetriever):
    """
    A class designed to retreive arrival time
    from user travel requests for a VLLM
    """

    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        # Setting up sampling parameters for deterministic output
        self.json_input = {"temperature": 0, "stop": '\n\n'}
        # Defining a prompt template to guide the model towards
        # extracting arrival cities
        self.prefix_prompt = \
'''Today is June 9, 2024. Sunday. Your task is to extract the arrival time to the destination city from the user's request. Examples:
Q: "Планирую сгонять в Хабаровск через три недели."
A: Arrival Time: "30/06/2024"

Q: "Хочу уехать из Москвы куда-нибудь на три дня, есть двадцать тысяч"
A: Arrival Time: "None"

Q: "Поеду в Альметьевск в середине августа"
A: Arrival Time: "15/08/2024"

Q: "Уеду в Питер из Казани в июле с 12 по 17 числа +- 300000 рублей"
A: Arrival Time: "12/07/2024"

Q: "Уеду в Москву из Рязани в августе с 10 по 30. Бюджет 70 тысяч."
A: Arrival Time: "10/08/2024"

Q: "Уеду из Рязани в августе с 10 по 30. Есть 70 тысяч."
A: Arrival Time: "10/08/2024"

Q: "Я в Тольятти. Мне срочно надо достать билеты в Кисловодск"
A: Arrival Time: "None"

Q: "Я в Москву в среду"
A: Arrival Time: "12/06/2024"

Q: "Я в Москву в с 1ое по 5ое мая"
A: Arrival Time: "01/05/2025"

Today is INSERT_DATE Your task is to extract the arrival time to the destination city from the user's request.

Q: "USER_REQUEST"
A: Arrival Time: "'''

    async def retrieve(self, request: str) -> str:
        """
        Generates a response from the VLLM based
        on the user's travel request, aiming to
        extract the arrival city.

        Args:
            request (str): The user's travel
                           request as a string.

        Returns:
            str: The extracted destination city
                 as a string, or a message indicating
                 no destination was found.
        """
        # Put actual information about the date in the prompt
        cur_day = datetime.now()
        prompt = self.prefix_prompt.replace("INSERT_DATE",
                                            cur_day.strftime('%B %d, %Y. %A.'))
        # Replace the placeholder in the prompt
        # template with the actual user request
        prompt = prompt.replace("USER_REQUEST", request)
        # Generate a response from the LLM using
        # the customized prompt and sampling parameters
        self.json_input["prompt"] = prompt
        result = await self.llm.get_response(self.json_input)
        result = extract_data(result)
        return result
